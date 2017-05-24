# -*- coding: UTF-8 -*-
from django.http import JsonResponse
from scipy.stats.stats import pearsonr
from scipy.stats import rankdata
from scipy.spatial.distance import euclidean
from datetime import date, datetime, timedelta
from django.core.cache import cache

import numpy
from parlalize.utils import *
import requests
import json
from datetime import datetime
from django.http import HttpResponse
import string
from kvalifikatorji.scripts import numberOfWords, countWords, getScore, getScores, problematicno, privzdignjeno, preprosto, TFIDF, getCountList
from collections import Counter
from parlalize.settings import LAST_ACTIVITY_COUNT
from .models import *
from parlalize.settings import API_URL, API_DATE_FORMAT, API_OUT_DATE_FORMAT
from parlaseje.models import Session, Question
from utils.speech import WordAnalysis
from raven.contrib.django.raven_compat.models import client
from slugify import slugify
from django.views.decorators.csrf import csrf_exempt

from utils.compass import getData as getCompassData

from parlalize.utils import tryHard


# get List of MPs
def getMPsList(request, date_=None):
    output = []
    data = None
    if date_:
        while data is None:
            try:
                data = tryHard(API_URL+'/getMPs/'+date_)
            except:
                pass
    else:
        while data is None:
            try:
                data = tryHard(API_URL+'/getMPs/')
            except:
                pass

    data = data.json()

    output = [{'id': i['id'],
               'image': i['image'],
               'name': i['name'],
               'membership': i['membership'],
               'acronym': i['acronym'],
               'district': i['district']} for i in data]

    return JsonResponse(output, safe=False)


# returns MP static data like PoliticalParty, age, ....
def setMPStaticPL(request, person_id, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
        data = tryHard(API_URL+'/getMPStatic/' + person_id + "/" + date_).json()
    else:
        date_of = datetime.now().date()
        data = tryHard(API_URL+'/getMPStatic/' + person_id).json()

    person = Person.objects.get(id_parladata=int(person_id))
    if not data:
        return JsonResponse({"status": 'Nothing iz well', "saved": False})
    dic = dict()

    wbfs = data['working_bodies_functions']

    result = saveOrAbortNew(model=MPStaticPL,
                            created_for=date_of,
                            person=person,
                            voters=data['voters'], age=data['age'],
                            mandates=data['mandates'],
                            party_id=data['party_id'],
                            education=data['education'],
                            previous_occupation=data['previous_occupation'],
                            name=data['name'],
                            district=data['district'],
                            facebook=data['social']['facebook'],
                            twitter=data['social']['twitter'],
                            linkedin=data['social']['linkedin'],
                            party_name=data['party'],
                            acronym=data['acronym'],
                            gov_id=data['gov_id'],
                            gender=data['gender'],
                            working_bodies_functions=wbfs)

    if result:
        for group in data['groups']:
            new_group = MPStaticGroup(person=MPStaticPL.objects.filter(person__id_parladata=int(person_id)).latest('created_at'), groupid=int(group['id']), groupname=group['name'])
            new_group.save()

    return JsonResponse({"status":'All iz well', "saved":result})


def getMPStaticPL(request, person_id, date_=None):
    """
    * @api {get} /p/getMPStatic/{id}/{?date} MP's static info
    * @apiName getMPStatic
    * @apiGroup MPs
    * @apiDescription This function returns an object with all 
      "static" data belonging to an MP. By static we mean that it
      is entered and maintained by hand and rarely, if ever, changes.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object} results
    * @apiSuccess {Integer} results.voters Number of voters who voted for this MP at the last election.
    * @apiSuccess {String} results.acronym This MP's party acronym.
    * @apiSuccess {Integer} results.mandate Number of this MP's mandates in the national assembly (including their current one).
    * @apiSuccess {Integer} results.party_id This MP's party's Parladata (organization) id.
    * @apiSuccess {Object[]} results.groups List of groups this MP is a member of (other than their party). #TODO refactor
    * @apiSuccess {Integer} results.groups.id Group's Parladata (organization) id.
    * @apiSuccess {String} results.groups.group_name Group's name.
    * @apiSuccess {String} results.education A string describing the education of this person.
    * @apiSuccess {Object[]} results.working_bodies_functions
    * @apiSuccess {String} results.working_bodies_functions.role The person's role in this working body.
    * @apiSuccess {Object} results.working_bodies_functions.wb Working body object.
    * @apiSuccess {String} results.working_bodies_functions.wb.acronym Working body's acronym (usually an empty string).
    * @apiSuccess {Boolean} results.working_bodies_functions.wb.is_coalition Answers the question: Does this working body belong to the coalition?
    * @apiSuccess {Integer} results.working_bodies_functions.wb.id Working body's Parladata (organization) id.
    * @apiSuccess {String} results.working_bodies_functions.wb.name The working body's name.
    * @apiSuccess {String} results.previous_occupation MP's occupation before becoming an MP.
    * @apiSuccess {String} results.name MP's name.
    * @apiSuccess {String[]} results.district List of strings representing district names.
    * @apiSuccess {Integer} results.age MP's age calculated from their birthday.
    * @apiSuccess {Object[]} results.social An array containing the object with social keys. #TODO refactor
    * @apiSuccess {String} results.social.twitter MP's Twitter url.
    * @apiSuccess {String} results.social.facebook MP's Facebook url.
    * @apiSuccess {String} results.social.linkedin MP's Linkedin url.
    * @apiSuccess {String} results.party MP's party name.

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getMPStatic/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getMPStatic/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": true,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "08.03.2017",
        "created_for": "06.08.2014",
        "results": {
            "voters": 919,
            "acronym": "ZL",
            "mandates": 1,
            "party_id": 8,
            "groups": [{
            "group_id": 9,
            "group_name": "Kolegij predsednika dr\u017eavnega zbora"
            }, {
            "group_id": 34,
            "group_name": "Delegacija Dr\u017eavnega zbora v Parlamentarni skup\u0161\u010dini Unije za Sredozemlje"
            }],
            "education": "diplomant univerzitetnega programa\r\n",
            "working_bodies_functions": [{
            "role": "vice_president",
            "wb": {
                "acronym": "",
                "is_coalition": false,
                "id": 10,
                "name": "Komisija za nadzor javnih financ"
            }
            }],
            "previous_occupation": "\u0161tudent",
            "name": "Luka Mesec",
            "district": ["Trbovlje"],
            "age": 29,
            "social": [{
            "twitter": "https://twitter.com/lukamesec",
            "facebook": "https://www.facebook.com/mesec.luka",
            "linkedin": null
            }],
            "party": "PS Zdru\u017eena Levica"
        }
    }
    """
    card = getPersonCardModelNew(MPStaticPL, person_id, date_)

    if card.twitter == 'False':
        print card.twitter

    wbfs = []
    for funct in card.working_bodies_functions:
        org = Organization.objects.filter(id_parladata=funct['org_id'])
        if org:
            wbfs.append({'wb': org[0].getOrganizationData(),
                         'role': funct['role']})

    data = {
        'created_at': card.created_at.strftime(API_DATE_FORMAT),
        'created_for': card.created_for.strftime(API_DATE_FORMAT),
        'person': getPersonData(person_id, date_),
        'results': {
            'voters': card.voters,
            'age': card.age,
            'mandates': card.mandates,
            'party_id': card.party_id,
            'acronym': card.acronym,
            'education': card.education,
            'previous_occupation': card.previous_occupation,
            'name': card.name,
            'district': [District.objects.get(id_parladata=dist).name for dist in card.district] if card.district else None,
            'party': card.party_name,
            'social': [{'facebook': card.facebook if card.facebook != 'False' else None, 'twitter': card.twitter if card.twitter != 'False' else None, 'linkedin': card.linkedin if card.linkedin != 'False' else None}],
            'groups': [{'group_id': group.groupid, 'group_name': group.groupname} for group in card.mpstaticgroup_set.all()],
            'working_bodies_functions': wbfs,
        }
    }

    return JsonResponse(data)


# returns MP static data like PoliticalParty, age, ....
def setMinsterStatic(request, person_id, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
        data = tryHard(API_URL+'/getMinistrStatic/' + person_id + "/" + date_).json()
    else:
        date_of = datetime.now().date()
        data = tryHard(API_URL+'/getMinistrStatic/' + person_id).json()

    person = Person.objects.get(id_parladata=int(person_id))
    if not data:
        return JsonResponse({"status": 'Nothing iz well', "saved": False})
    dic = dict()

    if data['party']:
        party = Organization.objects.get(id_parladata=data['party']['id'])
    else:
        party = None

    if data['ministry']:
        ministry = Organization.objects.get(id_parladata=data['ministry']['id'])
    else:
        ministry = None

    result = saveOrAbortNew(model=MinisterStatic,
                            created_for=date_of,
                            person=person,
                            age=data['age'],
                            party=party,
                            education=data['education'],
                            previous_occupation=data['previous_occupation'],
                            name=data['name'],
                            district=data['district'],
                            facebook=data['social']['facebook'],
                            twitter=data['social']['twitter'],
                            linkedin=data['social']['linkedin'],
                            gov_id=data['gov_id'],
                            gender=data['gender'],
                            ministry=ministry)

    return JsonResponse({"status":'All iz well', "saved":result})


# Saves to DB percent of attended sessions of MP and
# maximum and average of attended sessions
def setPercentOFAttendedSession(request, person_id, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = findDatesFromLastCard(Presence,
                                        person_id,
                                        datetime.now().date())[0]
        date_ = date_of.strftime(API_DATE_FORMAT)

    isNewVote = tryHard(API_URL + '/isVoteOnDay/'+date_).json()['isVote']
    print isNewVote
    if not isNewVote:
        return JsonResponse({'alliswell': True,
                             'status': 'Ni glasovanja na ta dan',
                             'saved': False})

    data = tryHard(API_URL+'/getNumberOfAllMPAttendedSessions/'+date_).json()

    if not data["votes"].values():
        return JsonResponse({'alliswell': False})

    if person_id in data["sessions"].keys():
        thisMP = data["sessions"][person_id]
    else:
        # ta member se ni obstajal
        thisMP = 0
        return JsonResponse({'alliswell': False,
                             'status': 'ta member se ni obstajal',
                             'saved': False})

    maximum = max(data["sessions"].values())
    maximumMP = [pId for pId in data["sessions"]
                 if data["sessions"][pId] == maximum]
    average = sum(data["sessions"].values()) / len(data["sessions"])

    if person_id in data["votes"].keys():
        thisMPVotes = data["votes"][person_id]
    else:
        thisMPVotes = 0

    maximumVotes = max(data["votes"].values())
    maximumMPVotes = [pId for pId in data["votes"]
                      if data["votes"][pId] == maximumVotes]

    averageVotes = sum(data["votes"].values()) / len(data["votes"])

    person = Person.objects.get(id_parladata=int(person_id))

    result = saveOrAbortNew(model=Presence,
                            created_for=date_of,
                            person=person,
                            person_value_sessions=thisMP,
                            maxMP_sessions=maximumMP,
                            average_sessions=average,
                            maximum_sessions=maximum,
                            person_value_votes=thisMPVotes,
                            maxMP_votes=maximumMPVotes,
                            average_votes=averageVotes,
                            maximum_votes=maximumVotes)

    return JsonResponse({'alliswell': True, "status": 'OK', "saved": result})


def getPercentOFAttendedSession(request, person_id, date=None):
    """
    * @api {get} /p/getPresence/{id}/{?date} MP's presence
    * @apiName getPresence
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs
      calculated presence scores. There are two scores, one for their presence
      at voting events and one for their presence at sessions overall. The function
      returns the score as it was calculated for a given date, if no date is
      supplied the date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object} results

    * @apiSuccess {Object} results.votes MP's calculated presence at voting events.    
    * @apiSuccess {Object} results.votes.max MP (or MPs) who has the highest attendance and their score.
    * @apiSuccess {Float} results.votes.max.score Max MP's score.
    * @apiSuccess {Object[]} results.votes.max.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.votes.max.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.votes.max.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.votes.max.mps.name MP's full name.
    * @apiSuccess {String} results.votes.max.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.votes.max.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.votes.max.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.votes.max.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.votes.max.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.votes.max.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.votes.max.mps.party.name The party's name.
    * @apiSuccess {String} results.votes.max.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.votes.max.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Float} results.votes.average The average score for this metric accross the parliament.
    * @apiSuccess {Float} results.votes.score Score for the MP in question.
    
    * @apiSuccess {Object} results.sessions MP's calculated presence at sessions.
    * @apiSuccess {Object} results.sessions.max MP (or MPs) who has the highest attendance and their score.
    * @apiSuccess {Float} results.sessions.max.score Max MP's score.
    * @apiSuccess {Object[]} results.sessions.max.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.sessions.max.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.sessions.max.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.sessions.max.mps.name MP's full name.
    * @apiSuccess {String} results.sessions.max.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.sessions.max.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.sessions.max.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.sessions.max.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.sessions.max.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.sessions.max.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.sessions.max.mps.party.name The party's name.
    * @apiSuccess {String} results.sessions.max.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.sessions.max.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).

    * @apiSuccess {Float} results.votes.average The average score for this metric accross the parliament.
    * @apiSuccess {Float} results.votes.score Score for the MP in question.
    

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getPresence/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getPresence/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "21.03.2017",
        "created_for": "17.02.2017",
        "results": {
            "votes": {
            "max": {
                "score": 98.5804416403786,
                "mps": [{
                "is_active": false,
                "district": [8],
                "name": "Ur\u0161ka Ban",
                "gov_id": "P240",
                "gender": "f",
                "party": {
                    "acronym": "SMC",
                    "is_coalition": true,
                    "id": 1,
                    "name": "PS Stranka modernega centra"
                },
                "type": "mp",
                "id": 3,
                "has_function": false
                }]
            },
            "average": 80.5083236752256,
            "score": 76.9716088328076
            },
            "sessions": {
            "max": {
                "score": 100.0,
                "mps": [{
                "is_active": false,
                "district": [84],
                "name": "Vlasta Po\u010dkaj",
                "gov_id": "P303",
                "gender": "f",
                "party": {
                    "acronym": "SMC",
                    "is_coalition": true,
                    "id": 1,
                    "name": "PS Stranka modernega centra"
                },
                "type": "mp",
                "id": 2934,
                "has_function": false
                }, {
                "is_active": false,
                "district": [85],
                "name": "Teja Ljubi\u010d",
                "gov_id": "P304",
                "gender": "f",
                "party": {
                    "acronym": "SMC",
                    "is_coalition": true,
                    "id": 1,
                    "name": "PS Stranka modernega centra"
                },
                "type": "mp",
                "id": 2933,
                "has_function": false
                }, {
                "is_active": false,
                "district": [48],
                "name": "Jasna Murgel",
                "gov_id": "P274",
                "gender": "f",
                "party": {
                    "acronym": "SMC",
                    "is_coalition": true,
                    "id": 1,
                    "name": "PS Stranka modernega centra"
                },
                "type": "mp",
                "id": 60,
                "has_function": false
                }, {
                "is_active": false,
                "district": [66],
                "name": "Julijana Bizjak Mlakar",
                "gov_id": "P158",
                "gender": "f",
                "party": {
                    "acronym": "DeSUS",
                    "is_coalition": true,
                    "id": 3,
                    "name": "PS Demokratska Stranka Upokojencev Slovenije"
                },
                "type": "mp",
                "id": 5,
                "has_function": false
                }]
            },
            "average": 88.5490589303276,
            "score": 85.5072463768116
            }
        }
    }
    """
    equalVoters = getPersonCardModelNew(Presence, person_id, date)

    out  = {
        'person': getPersonData(person_id, date),
        'created_at': equalVoters.created_at.strftime(API_DATE_FORMAT),
        'created_for': equalVoters.created_for.strftime(API_DATE_FORMAT),
        'results': {
            "sessions":{
                "score": equalVoters.person_value_sessions,
                "average": equalVoters.average_sessions,
                "max": {
                    "mps": [getPersonData(person, date) for person in equalVoters.maxMP_sessions],
                    "score": equalVoters.maximum_sessions,
                }
            },
            "votes": {
                "score": equalVoters.person_value_votes,
                "average": equalVoters.average_votes,
                "max": {
                    "mps": [getPersonData(person, date) for person in equalVoters.maxMP_votes],
                    "score": equalVoters.maximum_votes,
                }
            }
        }
    }
    return JsonResponse(out)


#Deprecated
#Saves to DB number of spoken word of MP and maximum and average of spoken words
def setNumberOfSpokenWordsALL(request, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_=""
    print '[INFO] Getting MPs'
    mps = tryHard(API_URL+'/getMPs/'+date_).json()

    mp_results = []

    for mp in mps:
        print '[INFO] Pasting speeches for MP ' + str(mp['id'])
        speeches = tryHard(API_URL+'/getSpeeches/' + str(mp['id']) + "/" + date_).json()

        text = ''.join([speech['content'] for speech in speeches])

        mp_results.append({'person_id': mp['id'], 'wordcount': numberOfWords(text)})

    print '[INFO] Sorting MPs'
    mps_sorted = sorted(mp_results, key=lambda k: k['wordcount'])

    print '[INFO] Getting all speeches'
    all_speeches = tryHard(API_URL+'/getAllSpeeches/'+date_).json()
    print '[INFO] Joining all speeches'
    text = ''.join([speech['content'] for speech in all_speeches])

    print '[INFO] Calculating total words'
    total_words = numberOfWords(text)
    print '[INFO] Calculating average words'
    average_words = total_words/len(mps)

    for result in mp_results:
        print '[INFO] Saving or updating MP\'s results'
        print saveOrAbortNew(model=SpokenWords,
                             created_for=date_of,
                             person=Person.objects.get(id_parladata=int(result['person_id'])),
                             score=int(result['wordcount']),
                             maxMP=Person.objects.get(id_parladata=int(mps_sorted[-1]['person_id'])),
                             average=average_words,
                             maximum=mps_sorted[-1]['wordcount'])

    return HttpResponse('All iz well')

def getNumberOfSpokenWords(request, person_id, date=None):
    """
    * @api {get} /p/getNumberOfSpokenWords/{id}/{?date} MP's number of spoken words
    * @apiName getNumberOfSpokenWords
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs
      calculated number of spoken words. The function
      returns the score as it was calculated for a given date, if no date is
      supplied the date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object} results MP's number of spoken words.
    * @apiSuccess {Object} results.max MP (or MPs) who has the highest number of spoken words and their score.
    * @apiSuccess {Float} results.max.score Max MP's score.
    * @apiSuccess {Object[]} results.max.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.max.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.max.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.max.mps.name MP's full name.
    * @apiSuccess {String} results.max.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.max.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.max.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.max.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.max.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.max.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.max.mps.party.name The party's name.
    * @apiSuccess {String} results.max.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.max.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Float} results.average The average score for this metric accross the parliament.
    * @apiSuccess {Float} results.score Score for the MP in question.
    

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getNumberOfSpokenWords/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getNumberOfSpokenWords/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "21.03.2017",
        "created_for": "20.03.2017",
        "results": {
            "max": {
            "score": 672449,
            "mps": [{
                "is_active": false,
                "district": [17],
                "name": "Jo\u017eef Horvat",
                "gov_id": "P020",
                "gender": "m",
                "party": {
                "acronym": "NSI",
                "is_coalition": false,
                "id": 6,
                "name": "PS Nova Slovenija"
                },
                "type": "mp",
                "id": 32,
                "has_function": false
            }]
            },
            "average": 177115,
            "score": 381389
        }
    }
    """

    card = getPersonCardModelNew(SpokenWords, person_id, date)

    results = {
        'person': getPersonData(person_id, date),
        'created_at': card.created_at.strftime(API_DATE_FORMAT),
        'created_for': card.created_for.strftime(API_DATE_FORMAT),
        'results': {
            'score': card.score,
            'average': card.average,
            'max': {
                'mps': [
                    getPersonData(card.maxMP.id_parladata, date)
                ],
                'score': card.maximum
            }
        }
    }
    return JsonResponse(results)

def setLastActivity(request, person_id):
    out = []
    activites = {date: [activity.get_child()
                        for activity
                        in Activity.objects.filter(person__id_parladata=person_id,
                                                   start_time__range=[date, date+timedelta(days=1)])]
                 for date in Activity.objects.filter(person__id_parladata=person_id).order_by("start_time").datetimes('start_time', 'day')}
    result = []
    for date in activites.keys():
        avtivity_ids = []
        options = []
        result = []
        vote_name = []
        types = []
        sessions = []
        for acti in activites[date]:
            #print acti.id_parladata
            if type(acti) == Speech:
                #print "Speech"
                avtivity_ids.append(acti.id_parladata)
                types.append("speech")
                vote_name.append(acti.session.name)
                result.append("None")
                options.append("None")
                sessions.append(str(acti.session.id_parladata))
            elif type(acti) == Ballot:
                #print "Ballot"
                avtivity_ids.append(acti.vote.id_parladata)
                types.append("ballot")
                vote_name.append(acti.vote.motion)
                result.append(acti.vote.result)
                options.append(acti.option)
                sessions.append("None")
            elif type(acti) == Question:
                print 'question'
                avtivity_ids.append(acti.id_parladata)
                types.append("question")
                vote_name.append(acti.title)
                result.append("None")
                options.append("None")
                sessions.append("None")

        out.append(saveOrAbortNew(model=LastActivity,
                                  person=Person.objects.get(id_parladata=int(person_id)),
                                  created_for=date,
                                  activity_id=";".join(map(str, avtivity_ids)),
                                  option=";".join(map(str, options)),
                                  result=";".join(map(str, result)),
                                  vote_name=";".join(vote_name),
                                  typee=";".join(types),
                                  session_id=";".join(sessions)))

    return JsonResponse(out, safe=False)


def getLastActivity(request, person_id, date_=None):
    """
    * @api {get} /p/getLastActivity/{id}/{?date} MP's last activity
    * @apiName getLastActivity
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs "last activity".
      This includes all ballots cast, questions asked and speeches spoken in the past
      ten days. This function returns the activity as it was calculated for a given
      date, if no date is supplied the date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person
      was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in
      coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the
      president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object[]} results
    * @apiSuccess {date} results.date The date of the events in this object.
    * @apiSuccess {Object[]} results.events List of event objects for this date.
    
    * @apiSuccess {String} results.events.option The option on the ballot, if the event was
      a ballot.
    * @apiSuccess {Integer} results.session_id Parladata id of the session at which the event
      took place, if the event was a ballot.
    * @apiSuccess {Boolean} results.result Returns true if the motion was passed, if the event
      was a ballot.
    * @apiSuccess {String} results.vote_name The name of the vote / text of the motion, if the
      event was a ballot.
    * @apiSuccess {Integer} results.vote_id Parladata id of the vote, if the event was a ballot.
    
    * @apiSuccess {String} results.recipient_text Who was the question addressed to, if the
      event was a question.
    * @apiSuccess {String} results.title The title of the question, if the event was a question.
    * @apiSuccess {String} results.content_url The url to the PDF of the question, if the
      event was a question.
    * @apiSUccess {Object} results.session Session object, if the event was a question. Currently returns null.
    * @apiSuccess {Integer} results.question_id Parladata id of the question, if the event was
      a question.

    * @apiSuccess {Object} results.session Session object, if the event was a speech.
    * @apiSuccess {String} results.session.name Session name, if the event was a speech.
    * @apiSuccess {date} results.session.date_ts UTF-8 date, if the event was a speech.
    * @apiSuccess {Object[]} results.session.orgs List of organizations this session belongs to, if the event was a speech.
    * @apiSuccess {String} results.session.orgs.acronym Organization acronym, if the event was a speech.
    * @apiSuccess {Boolean} results.session.orgs.is_coalition If the event was a speech answers the question: Is this organization in coalition with the government?
    * @apiSuccess {Integer} results.session.orgs.id Parladata id of the organization, if the event was a speech.
    * @apiSuccess {String} results.session.orgs.name Name of the organization, if the event was a speech.
    * @apiSuccess {date} results.session.date Slovenian date of the session, if the event was a speech.
    * @apiSuccess {Object} results.session.org The primary organization for this session, if the event was a speech.
    * @apiSuccess {String} results.session.org.acronym Organization acronym, if the event was a speech.
    * @apiSuccess {Boolean} results.session.org.is_coalition If the event was a speech answers the question: Is this organization in coalition with the government?
    * @apiSuccess {Integer} results.session.org.id Parladata id of the organization, if the event was a speech.
    * @apiSuccess {String} results.session.org.name Name of the organization, if the event was a speech.
    * @apiSuccess {Integer} results.session.id Parladata id of the session, if the event ws a speech.
    
    * @apiSuccess {String} results.type Denotes the type of event (ballot/speech/question).
    
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getLastActivity/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getLastActivity/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "20. 3. 2017",
        "created_for": "20. 3. 2017",
        "results": [{
            "date": "20. 3. 2017",
            "events": [{
            "option": "za",
            "session_id": 9379,
            "result": true,
            "vote_name": "Dnevni red v celoti",
            "vote_id": 6900,
            "type": "ballot"
            }]
        }, {
            "date": "17. 3. 2017",
            "events": [{
            "recipient_text": "ministrica za zdravje",
            "title": "v zvezi z zakonskim omejevanjem vsebnosti transma\u0161\u010dob v \u017eivilh",
            "content_url": "http://imss.dz-rs.si/IMiS/ImisAdmin.nsf/ImisnetAgent?OpenAgent&2&DZ-MSS-01/ca20e0052e10f59269cd589241144a04f18728b6e6935124c6df30d7331d1f5f",
            "session": null,
            "type": "question",
            "question_id": 10180
            }]
        }, {
            "date": "10. 3. 2017",
            "events": [{
            "session": {
                "name": "88. redna seja",
                "date_ts": "2017-03-10T01:00:00",
                "orgs": [{
                "acronym": "",
                "is_coalition": false,
                "id": 9,
                "name": "Kolegij predsednika dr\u017eavnega zbora"
                }],
                "date": "10. 3. 2017",
                "org": {
                "acronym": "",
                "is_coalition": false,
                "id": 9,
                "name": "Kolegij predsednika dr\u017eavnega zbora"
                },
                "id": 9358,
                "in_review": true
            },
            "speech_id": 1118501,
            "type": "speech"
            }]
        }]
    }
    """
    print date

    def parseDayActivites(day_activites):
        data = []
        types = day_activites.typee.split(';')
        vote_names = day_activites.vote_name.split(';')
        results = day_activites.result.split(';')
        options = day_activites.option.split(';')
        activity_ids = day_activites.activity_id.split(';')
        sessions_ids = day_activites.session_id.split(';')
        for i in range(len(day_activites.typee.split(';'))):
            if types[i] == 'ballot':
                data.append({
                    'option': options[i],
                    'result': Vote.objects.filter(id_parladata=activity_ids[i]).order_by('-created_at')[0].result,
                    'vote_name': vote_names[i],
                    'vote_id': int(activity_ids[i]),
                    'type': types[i],
                    'session_id': Vote.objects.filter(id_parladata=int(activity_ids[i])).order_by('-created_at')[0].session.id_parladata
                    })
            elif types[i] == 'speech':
                data.append({
                    'speech_id': int(activity_ids[i]),
                    'type': types[i],
                    'session': Session.objects.get(id_parladata=sessions_ids[i]).getSessionData(),
                    })
            elif types[i] == 'question':
                print "getQuest"
                question = Question.objects.get(id_parladata=activity_ids[i])
                if question.session:
                    sesData = question.session.getSessionData()
                else:
                    sesData = None
                persons = []
                orgs = []
                for person in question.recipient_persons.all():
                    persons.append(getMinistryData(person.id_parladata, question.start_time.strftime(API_DATE_FORMAT)))
                for org in question.recipient_organizations.all():
                    orgs.append(org.getOrganizationData())
                data.append({
                    'question_id': int(activity_ids[i]),
                    'type': types[i],
                    'session': sesData,
                    'title': question.title,
                    'recipient_text': question.recipient_text,
                    'content_url': question.content_link,
                    'recipient_persons': persons,
                    'recipient_orgs': orgs,
                    })
        return {'date': day_activites.created_for.strftime(API_OUT_DATE_FORMAT), 'events': data}

    out = []

    lastActivites = getPersonCardModelNew(LastActivity, person_id, date_)
    lastDay = lastActivites.created_for.strftime(API_OUT_DATE_FORMAT)
    out.append(parseDayActivites(lastActivites))
    for i in range(LAST_ACTIVITY_COUNT - 1):
        startDate = lastActivites.created_for - timedelta(days=1)
        try:
            lastActivites = getPersonCardModelNew(LastActivity, person_id, datetime.strftime(startDate, "%d.%m.%Y"))
        except:
            break
        if lastActivites == None:
            break
        out.append(parseDayActivites(lastActivites))

    static = getPersonCardModelNew(MPStaticPL, person_id, date_)

    result = {
        'created_at': lastDay,
        'created_for': lastDay,
        'person': getPersonData(person_id, date_),
        'results': out
        }
    return JsonResponse(result, safe=False)


# TODO date
def getAllSpeeches(request, person_id, date_=None):
    """
    * @api {get} /p/getAllSpeeches/{id}/{?date} MP's speeches
    * @apiName getAllSpeeches
    * @apiGroup MPs
    * @apiDescription This function returns a list of all dates when the MP spoke
      as well as speech ids that happened on those days. The function returns the
      list as it was compiled on a given date, if no date is supplied the date is
      today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object[]} results MP's speeches.
    * @apiSuccess {date} results.date The date of the speech.
    * @apiSuccess {Object[]} results.speeches List of speeches that happened on this day.
    * @apiSuccess {String} results.speeches.session_name The name of the session at which the speech took place.
    * @apiSuccess {Integer} results.speech_id Parladata id of the speech.
    * @apiSuccess {Integer} results.session_id Parladata id of the session at which the speech took place.

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getAllSpeeches/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getAllSpeeches/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "22. 11. 2016",
        "created_for": "28. 8. 2014",
        "results": [{
            "date": "28. 8. 2014",
            "speeches": [{
            "session_name": "2. izredna seja",
            "speech_id": 524522,
            "session_id": 5619
            }, {
            "session_name": "2. izredna seja",
            "speech_id": 524403,
            "session_id": 5619
            }]
        }, {
            "date": "25. 8. 2014",
            "speeches": [{
            "session_name": "1. izredna seja",
            "speech_id": 524582,
            "session_id": 5620
            }, {
            "session_name": "1. izredna seja",
            "speech_id": 524665,
            "session_id": 5620
            }, {
            "session_name": "1. izredna seja",
            "speech_id": 524690,
            "session_id": 5620
            }]
        }, {
            "date": "22. 8. 2014",
            "speeches": [{
            "session_name": "1. redna seja",
            "speech_id": 529141,
            "session_id": 5729
            }, {
            "session_name": "1. redna seja",
            "speech_id": 529131,
            "session_id": 5729
            }]
        }]
    }
    """
    if date_:
        fdate = datetime.strptime(date_, '%d.%m.%Y')
        speeches = Speech.getValidSpeeches(fdate)
        speeches = speeches.filter(person__id_parladata=person_id)
        speeches = [[speech for speech in speeches.filter(start_time__range=[t_date, t_date+timedelta(days=1)])] for t_date in speeches.filter(start_time__lte=fdate).order_by("start_time").datetimes('start_time', 'day')]
    else:
        fdate = datetime.now()
        speeches = Speech.getValidSpeeches(datetime.now())
        speeches = speeches.filter(person__id_parladata=person_id)
        speeches = [[speech for speech in speeches.filter(start_time__range=[t_date, t_date+timedelta(days=1)])] for t_date in speeches.order_by("start_time").datetimes('start_time', 'day')]
    out = []
    lastDay = None
    created_at = []
    for day in speeches:
        dayData = {"date": day[0].start_time.strftime(API_OUT_DATE_FORMAT), "speeches":[]}
        lastDay = day[0].start_time.strftime(API_OUT_DATE_FORMAT)
        for speech in day:
            created_at.append(speech.created_at)
            dayData["speeches"].append({
                "session_name": speech.session.name,
                "speech_id": speech.id_parladata,
                "session_id": speech.session.id_parladata})
        out.append(dayData)

    result = {
        'person': getPersonData(person_id, date_),
        'created_at': max(created_at).strftime(API_OUT_DATE_FORMAT) if created_at else datetime.today().strftime("API_DATE_FORMAT"),
        'created_for': lastDay if lastDay else datetime.today().strftime("API_DATE_FORMAT"),
        'results': list(reversed(out))
        }
    return JsonResponse(result, safe=False)


#method returns percent, how similar does the members vote
def getEqualVoters(request, id, date_=None):
    print id
    if date_:
        votes = getLogicVotes(date_)
        date_of = datetime.strptime(date_, '%d.%m.%Y')
    else:
        votes = getLogicVotes()
        date_of = datetime.now().date()

    members = getMPsList(request, date_)
    membersDict = {str(mp['id']):mp for mp in json.loads(members.content)}
    tempVotes = {voter: votes_ for voter, votes_ in votes.items() if voter in membersDict.keys()}
    votes = tempVotes
    try:
        out = {vote:euclidean(votes[str(id)].values(), votes[str(vote)].values()) for vote in sorted(votes.keys()) if str(vote) != str(id)}
    except:
        client.captureException()
        return JsonResponse({'alliswell': False})

    keys = sorted(out, key=out.get)

    for key in keys:
        membersDict[key].update({'ratio':out[str(key)]})
        membersDict[key].update({'id':key})
    return membersDict, keys, date_of


# Method return json with most similar voters to this voter
def setMostEqualVoters(request, person_id, date_=None):
    if date_:
        #if run setter for date check if exist vote on this day
        isNewVote = tryHard(API_URL +'/isVoteOnDay/'+date_).json()["isVote"]
        print isNewVote
        if not isNewVote:
            return JsonResponse({'alliswell': True, "status":'Ni glasovanja na ta dan', "saved": False})
        members, keys, date_of = getEqualVoters(request, person_id, date_)
    else:
        members, keys, date_of = getEqualVoters(request, person_id)

    out = {index: members[key] for key, index in zip(keys[:5], [1, 2, 3, 4, 5])}

    result = saveOrAbortNew(model=EqualVoters,
                            created_for=date_of,
                            person=Person.objects.get(id_parladata=int(person_id)),
                            person1=Person.objects.get(id_parladata=int(out[1]['id'])),
                            votes1=out[1]['ratio'],
                            person2=Person.objects.get(id_parladata=int(out[2]['id'])),
                            votes2=out[2]['ratio'],
                            person3=Person.objects.get(id_parladata=int(out[3]['id'])),
                            votes3=out[3]['ratio'],
                            person4=Person.objects.get(id_parladata=int(out[4]['id'])),
                            votes4=out[4]['ratio'],
                            person5=Person.objects.get(id_parladata=int(out[5]['id'])),
                            votes5=out[5]['ratio'])
    return JsonResponse({'alliswell': True, "status":'OK', "saved": result})


def getMostEqualVoters(request, person_id, date_=None):
    """
    * @api {get} /p/getMostEqualVoters/{id}/{?date} MP's most similar voters
    * @apiName getMostEqualVoters
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs
      top 5 most similar voters. The function
      returns the score as it was calculated for a given date, if no date is
      supplied the date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object[]} results List of 5 person objects representing MP's most similar voters.
    * @apiSuccess {Object} results.person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} results.person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.person.name MP's full name.
    * @apiSuccess {String} results.person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.person.party.name The party's name.
    * @apiSuccess {String} results.person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} results.person.id The person's Parladata id.
    * @apiSuccess {Boolean} results.person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Float} results.ratio The euclidean distance between the chosen MP and this one.

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getMostEqualVoters/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getMostEqualVoters/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "03.11.2016",
        "created_for": "28.08.2014",
        "results": [{
            "person": {
            "is_active": false,
            "district": [103],
            "name": "Violeta Tomi\u0107",
            "gov_id": "P289",
            "gender": "f",
            "party": {
                "acronym": "ZL",
                "is_coalition": false,
                "id": 8,
                "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 80,
            "has_function": false
            },
            "ratio": 0.584624087008587
        }, {
            "person": {
            "is_active": false,
            "district": [49],
            "name": "Franc Tr\u010dek ",
            "gov_id": "P290",
            "gender": "m",
            "party": {
                "acronym": "ZL",
                "is_coalition": false,
                "id": 8,
                "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 82,
            "has_function": false
            },
            "ratio": 0.541776627164668
        }, {
            "person": {
            "is_active": false,
            "district": [76],
            "name": "Matja\u017e Han\u017eek",
            "gov_id": "P256",
            "gender": "m",
            "party": {
                "acronym": "ZL",
                "is_coalition": false,
                "id": 8,
                "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 31,
            "has_function": false
            },
            "ratio": 0.538931817860966
        }, {
            "person": {
            "is_active": false,
            "district": [83],
            "name": "Matej Ta\u0161ner Vatovec",
            "gov_id": "P288",
            "gender": "m",
            "party": {
                "acronym": "ZL",
                "is_coalition": false,
                "id": 8,
                "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 79,
            "has_function": false
            },
            "ratio": 0.494254483850995
        }, {
            "person": {
            "is_active": false,
            "district": [46],
            "name": "Branislav Raji\u0107",
            "gov_id": "P281",
            "gender": "m",
            "party": {
                "acronym": "SMC",
                "is_coalition": true,
                "id": 1,
                "name": "PS Stranka modernega centra"
            },
            "type": "mp",
            "id": 70,
            "has_function": false
            },
            "ratio": 0.384675997982625
        }]
    }
    """
    equalVoters = getPersonCardModelNew(EqualVoters, person_id, date_)

    print equalVoters.person1.id_parladata

    out = {
        'created_at': equalVoters.created_at.strftime(API_DATE_FORMAT),
        'created_for': equalVoters.created_for.strftime(API_DATE_FORMAT),
        'person': getPersonData(person_id, date_),
        'results': [
            {
                "ratio": equalVoters.votes1,
                "person": getPersonData(equalVoters.person1.id_parladata, date_),
            },
            {
                "ratio": equalVoters.votes2,
                "person": getPersonData(equalVoters.person2.id_parladata, date_),
            },
            {
                "ratio": equalVoters.votes3,
                "person": getPersonData(equalVoters.person3.id_parladata, date_),
            },
            {
                "ratio": equalVoters.votes4,
                "person": getPersonData(equalVoters.person4.id_parladata, date_),
            },
            {
                "ratio": equalVoters.votes5,
                "person": getPersonData(equalVoters.person5.id_parladata, date_),
            }
        ]
    }

    #data = getPersonCardModel(EqualVoters, person_id)
    return JsonResponse(out, safe=False)


# Method return json with less similar voters to this voter
def setLessEqualVoters(request, person_id, date_=None):
    if date_:
        #if run setter for date check if exist vote on this day
        isNewVote = tryHard(API_URL +'/isVoteOnDay/'+date_).json()["isVote"]
        print isNewVote
        if not isNewVote:
            return JsonResponse({'alliswell': True, "status":'Ni glasovanja na ta dan', "saved": False})
        members, keys, date_of = getEqualVoters(request, person_id, date_)
    else:
        members, keys, date_of = getEqualVoters(request, person_id)
    out = {index: members[key] for key, index in zip(keys[-6:-1], [5, 4, 3, 2, 1])}

    result = saveOrAbortNew(model=LessEqualVoters,
                            created_for=date_of,
                            person=Person.objects.get(id_parladata=int(person_id)),
                            person1=Person.objects.get(id_parladata=int(out[1]['id'])),
                            votes1=out[1]['ratio'],
                            person2=Person.objects.get(id_parladata=int(out[2]['id'])),
                            votes2=out[2]['ratio'],
                            person3=Person.objects.get(id_parladata=int(out[3]['id'])),
                            votes3=out[3]['ratio'],
                            person4=Person.objects.get(id_parladata=int(out[4]['id'])),
                            votes4=out[4]['ratio'],
                            person5=Person.objects.get(id_parladata=int(out[5]['id'])),
                            votes5=out[5]['ratio'])
    return JsonResponse({'alliswell': True, "status":'OK', "saved": result})


def getLessEqualVoters(request, person_id, date_=None): # TODO refactor rename
    """
    * @api {get} /p/getLeastEqualVoters/{id}/{?date} MP's least similar voters
    * @apiName getLeastEqualVoters
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs
      top 5 least similar voters. The function
      returns the score as it was calculated for a given date, if no date is
      supplied the date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object[]} results List of 5 person objects representing MP's least similar voters.
    * @apiSuccess {Object} results.person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} results.person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.person.name MP's full name.
    * @apiSuccess {String} results.person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.person.party.name The party's name.
    * @apiSuccess {String} results.person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} results.person.id The person's Parladata id.
    * @apiSuccess {Boolean} results.person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Float} results.ratio The euclidean distance between the chosen MP and this one.

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getLeastEqualVoters/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getLeastEqualVoters/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "03.11.2016",
        "created_for": "28.08.2014",
        "results": [{
            "person": {
            "is_active": false,
            "district": [60],
            "name": "Branko Grims",
            "gov_id": "P016",
            "gender": "m",
            "party": {
                "acronym": "SDS",
                "is_coalition": false,
                "id": 5,
                "name": "PS Slovenska Demokratska Stranka"
            },
            "type": "mp",
            "id": 26,
            "has_function": false
            },
            "ratio": -0.588580815327302
        }, {
            "person": {
            "is_active": false,
            "district": [94],
            "name": "An\u017ee Logar",
            "gov_id": "P238",
            "gender": "m",
            "party": {
                "acronym": "SDS",
                "is_coalition": false,
                "id": 5,
                "name": "PS Slovenska Demokratska Stranka"
            },
            "type": "mp",
            "id": 54,
            "has_function": false
            },
            "ratio": -0.475334337037446
        }, {
            "person": {
            "is_active": false,
            "district": [26],
            "name": "Suzana Lep \u0160imenko",
            "gov_id": "P268",
            "gender": "f",
            "party": {
                "acronym": "SDS",
                "is_coalition": false,
                "id": 5,
                "name": "PS Slovenska Demokratska Stranka"
            },
            "type": "mp",
            "id": 51,
            "has_function": false
            },
            "ratio": -0.475334337037446
        }, {
            "person": {
            "is_active": false,
            "district": [44],
            "name": "Bojan Podkraj\u0161ek",
            "gov_id": "P277",
            "gender": "m",
            "party": {
                "acronym": "SDS",
                "is_coalition": false,
                "id": 5,
                "name": "PS Slovenska Demokratska Stranka"
            },
            "type": "mp",
            "id": 64,
            "has_function": false
            },
            "ratio": -0.475334337037446
        }, {
            "person": {
            "is_active": false,
            "district": [7],
            "name": "Anja Bah \u017dibert",
            "gov_id": "P239",
            "gender": "f",
            "party": {
                "acronym": "SDS",
                "is_coalition": false,
                "id": 5,
                "name": "PS Slovenska Demokratska Stranka"
            },
            "type": "mp",
            "id": 2,
            "has_function": false
            },
            "ratio": -0.475334337037446
        }]
    }
    """
    equalVoters = getPersonCardModelNew(LessEqualVoters, person_id, date_)
    out = {
        'created_at': equalVoters.created_at.strftime(API_DATE_FORMAT),
        'created_for': equalVoters.created_for.strftime(API_DATE_FORMAT),
        'person': getPersonData(person_id, date_),
        'results': [
            {
                "ratio": equalVoters.votes1,
                "person": getPersonData(equalVoters.person1.id_parladata, date_),
            },
            {
                "ratio": equalVoters.votes2,
                "person": getPersonData(equalVoters.person2.id_parladata, date_),
            },
            {
                "ratio": equalVoters.votes3,
                "person": getPersonData(equalVoters.person3.id_parladata, date_),
            },
            {
                "ratio": equalVoters.votes4,
                "person": getPersonData(equalVoters.person4.id_parladata, date_),
            },
            {
                "ratio": equalVoters.votes5,
                "person": getPersonData(equalVoters.person5.id_parladata, date_),
            }
        ]
    }

    #data = getPersonCardModel(EqualVoters, person_id)
    return JsonResponse(out, safe=False)

#get speech and data of speaker
def getSpeech(request, id): # TODO refactor remove?
    speech=tryHard(API_URL+'/getSpeech/'+id+'/')
    speech = speech.json()
    memList = getMPsList(request)
    members = json.loads(memList.content)
    speech['name'] = members[str(speech['speeker'])]['Name']
    speech['image'] = members[str(speech['speeker'])]['Image']
    return JsonResponse(speech)

#TODO
#/id/percent/prisotniAliVsi
#/34/66/1
def getMPsWhichFitsToPG(request, id): # TODO refactor remove?
    r=tryHard(API_URL+'/getVotes/')
    votes = r.json()
    r=tryHard(API_URL+'/getMembersOfPGs/')
    membersInPGs = r.json()

    votesToLogical(votes, len(Vote.objects.all()))
    #calculate mean
    votesLists = [votes[str(pgMember)] for pgMember in membersInPGs[id]]
    votesArray = numpy.array(votesLists)
    mean = numpy.mean(votesArray, axis=0)

    #TODO discretization for
    #mean = [for m in mean]

    #delete members of PR from votes list
    map(votes.__delitem__, [str(member) for member in membersInPGs[id]])

    out = {vote:pearsonr(votes[vote], mean)[0] for vote in votes.keys()}
    keys = sorted(out, key=out.get)
    print out
    members = getMPsList(request)
    members= json.loads(members.content)
    print members
    for member in members:
        #TODO: check members group
        try:
            member.update({'ratio': out[str(member["id"])]})
        except:
            member.update({'ratio': 0})
    #for key in keys:
    #   members[key].update({'ratio':out[key]})
    outs = sorted(members, key=lambda k: k['ratio'])

    #outs = {key:members[key] for key in keys[-5:]}
    return JsonResponse(outs[-5:], safe=False)


def setCutVotes(request, person_id, date_=None):
    print "cut"
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT)
    else:
        date_of = datetime.now().date()
        date_ = date_of.strftime(API_DATE_FORMAT)

    isNewVote = tryHard(API_URL +'/isVoteOnDay/'+date_).json()["isVote"]
    print isNewVote
    if not isNewVote:
        return JsonResponse({'alliswell': True, "status":'Ni glasovanja na ta dan', "saved": False})

    r=tryHard(API_URL+'/getCoalitionPGs/')
    coalition = r.json()

    coal_pgs = [str(pg) for pg in coalition["coalition"]]
    oppo_pgs = [str(pg) for pg in coalition["opposition"]]

    pg_score_C, membersInPGs, votes, all_votes = getRangeVotes(coal_pgs, date_, "plain")
    pg_score_O, membersInPGs, votes, all_votes = getRangeVotes(oppo_pgs, date_, "plain")

    coal_avg = {}
    oppo_avg = {}


    # Calculate coalition and opposition average
    coal_avg["for"] = float(sum(map(voteFor, pg_score_C))) / (float(len(pg_score_C))) * 100 if len(pg_score_C) != 0 else 0
    oppo_avg["for"] = float(sum(map(voteFor, pg_score_O))) / (float(len(pg_score_O)))*100 if len(pg_score_O) != 0 else 0
    coal_avg["against"] = float(sum(map(voteAgainst, pg_score_C))) / (float(len(pg_score_C))) * 100 if len(pg_score_C) != 0 else 0
    oppo_avg["against"] = float(sum(map(voteAgainst, pg_score_O))) / (float(len(pg_score_O))) * 100 if len(pg_score_O) != 0 else 0
    coal_avg["abstain"] = float(sum(map(voteAbstain, pg_score_C))) / (float(len(pg_score_C))) * 100 if len(pg_score_C) != 0 else 0
    oppo_avg["abstain"] = float(sum(map(voteAbstain, pg_score_O))) / (float(len(pg_score_O))) * 100 if len(pg_score_O) != 0 else 0
    coal_avg["absent"] = float(sum(map(voteAbsent, pg_score_C))) / (float(len(pg_score_C))) * 100 if len(pg_score_C) != 0 else 0
    oppo_avg["absent"] = float(sum(map(voteAbsent, pg_score_O))) / (float(len(pg_score_O))) * 100 if len(pg_score_O) != 0 else 0

    out = dict()
    out["for"] = dict()
    out["against"] = dict()
    out["abstain"] = dict()
    out["absent"] = dict()
    #Calculations for this member
    try:
        out["for"]["this"]=float(sum(map(voteFor, votes[person_id].values())))/float(len(votes[person_id].values())) * 100 if len(votes[person_id].values()) != 0 else 0
        out["against"]["this"]=float(sum(map(voteAgainst, votes[person_id].values())))/float(len(votes[person_id].values())) * 100 if len(votes[person_id].values()) != 0 else 0
        out["abstain"]["this"]=float(sum(map(voteAbstain, votes[person_id].values())))/float(len(votes[person_id].values())) * 100 if len(votes[person_id].values()) != 0 else 0
        out["absent"]["this"]=float(sum(map(voteAbsent, votes[person_id].values())))/float(len(votes[person_id].values())) * 100 if len(votes[person_id].values()) != 0 else 0
    except:
        client.captureException()
        return JsonResponse({'alliswell': False})

    #Calculations for coalition
    try:
        idsForCoal, coalFor = zip(*[(member, float(sum(map(voteFor,votes[str(member)].values()))) / float(len(votes[str(member)].values())) * 100 if len(votes[str(member)].values()) != 0 else 0 ) for i in coalition['coalition'] for member in membersInPGs[str(i)] if len(votes[str(member)].values()) > 0])
        idsCoalAgainst, coalAgainst = zip(*[(member, float(sum(map(voteAgainst,votes[str(member)].values()))) / float(len(votes[str(member)].values())) * 100 if len(votes[str(member)].values()) != 0 else 0 ) for i in coalition['coalition'] for member in membersInPGs[str(i)] if len(votes[str(member)].values()) > 0])
        idsCoalAbstain, coalAbstain = zip(*[(member,float(sum(map(voteAbstain,votes[str(member)].values()))) / float(len(votes[str(member)].values())) * 100 if len(votes[str(member)].values()) != 0 else 0 ) for i in coalition['coalition'] for member in membersInPGs[str(i)] if len(votes[str(member)].values()) > 0])
        idsCoalAbsent, coalAbsent = zip(*[(member,float(sum(map(voteAbsent,votes[str(member)].values()))) / float(len(votes[str(member)].values())) * 100 if len(votes[str(member)].values()) != 0 else 0 ) for i in coalition['coalition'] for member in membersInPGs[str(i)] if len(votes[str(member)].values()) > 0])
    except:
        client.captureException()
        return JsonResponse({'alliswell': False})

    coalMaxPercentFor = max(coalFor)
    coalMaxPercentAgainst = max(coalAgainst)
    coalMaxPercentAbstain = max(coalAbstain)
    coalMaxPercentAbsent = max(coalAbsent)

    out["for"]["maxCoal"]=coalMaxPercentFor
    idsMaxForCoal = numpy.array(idsForCoal)[numpy.where(numpy.array(coalFor) == coalMaxPercentFor)[0]]
    out["for"]["maxCoalID"] = list(idsMaxForCoal)

    out["against"]["maxCoal"]=coalMaxPercentAgainst
    idsMaxAgainstCoal = numpy.array(idsCoalAgainst)[numpy.where(numpy.array(coalAgainst) == coalMaxPercentAgainst)[0]]
    out["against"]["maxCoalID"] = list(idsMaxAgainstCoal)

    out["abstain"]["maxCoal"]=coalMaxPercentAbstain
    idsMaxAbstainCoal = numpy.array(idsCoalAbstain)[numpy.where(numpy.array(coalAbstain) == coalMaxPercentAbstain)[0]]
    out["abstain"]["maxCoalID"] = list(idsMaxAbstainCoal)

    out["absent"]["maxCoal"]=coalMaxPercentAbsent
    idsMaxAbsentCoal = numpy.array(idsCoalAbsent)[numpy.where(numpy.array(coalAbsent) == coalMaxPercentAbsent)[0]]
    out["absent"]["maxCoalID"] = list(idsMaxAbsentCoal)

    #Calculations for opozition
    #delete coalition groups from members in PGs
    map(membersInPGs.__delitem__, [str(coalitionIds) for coalitionIds in coalition['coalition']])
    try:
        idsForOpp, oppFor = zip(*[(member, float(sum(map(voteFor, votes[str(member)].values()))) / float(len(votes[str(member)].values())) * 100 if len(votes[str(member)].values()) != 0 else 0 ) for i in membersInPGs.keys() for member in membersInPGs[str(i)] if len(votes[str(member)].values()) > 0])
        idsOppAgainst, oppAgainst = zip(*[(member, float(sum(map(voteAgainst, votes[str(member)].values()))) / float(len(votes[str(member)].values())) * 100 if len(votes[str(member)].values()) != 0 else 0 ) for i in membersInPGs.keys() for member in membersInPGs[str(i)] if len(votes[str(member)].values()) > 0])
        idsOppAbstain, oppAbstain = zip(*[(member, float(sum(map(voteAbstain, votes[str(member)].values()))) / float(len(votes[str(member)].values())) * 100 if len(votes[str(member)].values()) != 0 else 0 ) for i in membersInPGs.keys() for member in membersInPGs[str(i)] if len(votes[str(member)].values()) > 0])
        idsOppAbsent, oppAbsent = zip(*[(member, float(sum(map(voteAbsent, votes[str(member)].values()))) / float(len(votes[str(member)].values())) * 100 if len(votes[str(member)].values()) != 0 else 0 ) for i in membersInPGs.keys() for member in membersInPGs[str(i)] if len(votes[str(member)].values()) > 0])
    except:
        client.captureException()
        return JsonResponse({'alliswell': False})

    oppMaxPercentFor = max(oppFor)
    oppMaxPercentAgainst = max(oppAgainst)
    oppMaxPercentAbstain = max(oppAbstain)
    oppMaxPercentAbsent = max(oppAbsent)

    out["for"]["maxOpp"]=oppMaxPercentFor

    idsMaxForOppo = numpy.array(idsForOpp)[numpy.where(numpy.array(oppFor) == oppMaxPercentFor)[0]]
    out["for"]["maxOppID"] = list(idsMaxForOppo)

    out["against"]["maxOpp"]=oppMaxPercentAgainst
    idsMaxAgainstOppo = numpy.array(idsOppAgainst)[numpy.where(numpy.array(oppAgainst) == oppMaxPercentAgainst)[0]]
    out["against"]["maxOppID"] = list(idsMaxAgainstOppo)

    out["abstain"]["maxOpp"]=oppMaxPercentAbstain
    idsMaxAbstainOppo = numpy.array(idsOppAbstain)[numpy.where(numpy.array(oppAbstain) == oppMaxPercentAbstain)[0]]
    out["abstain"]["maxOppID"] = list(idsMaxAbstainOppo)

    out["absent"]["maxOpp"]=oppMaxPercentAbsent
    idsMaxAbsentOppo = numpy.array(idsOppAbsent)[numpy.where(numpy.array(oppAbsent) == oppMaxPercentAbsent)[0]]
    out["absent"]["maxOppID"] = list(idsMaxAbsentOppo)

    final_response = saveOrAbortNew(
        CutVotes,
        created_for=date_of,
        person = Person.objects.get(id_parladata=person_id),
        this_for = out["for"]["this"],
        this_against = out["against"]["this"],
        this_abstain = out["abstain"]["this"],
        this_absent = out["absent"]["this"],
        coalition_for = coal_avg["for"],
        coalition_against = coal_avg["against"],
        coalition_abstain = coal_avg["abstain"],
        coalition_absent = coal_avg["absent"],
        coalition_for_max = out["for"]["maxCoal"],
        coalition_against_max = out["against"]["maxCoal"],
        coalition_abstain_max = out["abstain"]["maxCoal"],
        coalition_absent_max = out["absent"]["maxCoal"],
        coalition_for_max_person = ','.join(map(str, out["for"]["maxCoalID"])),
        coalition_against_max_person = ','.join(map(str, out["against"]["maxCoalID"])),
        coalition_abstain_max_person = ','.join(map(str, out["abstain"]["maxCoalID"])),
        coalition_absent_max_person = ','.join(map(str, out["absent"]["maxCoalID"])),
        opposition_for = oppo_avg["for"],
        opposition_against = oppo_avg["against"],
        opposition_abstain = oppo_avg["abstain"],
        opposition_absent= oppo_avg["absent"],
        opposition_for_max =out["for"]["maxOpp"],
        opposition_against_max = out["against"]["maxOpp"],
        opposition_abstain_max = out["abstain"]["maxOpp"],
        opposition_absent_max = out["absent"]["maxOpp"],
        opposition_for_max_person = ','.join(map(str, out["for"]["maxOppID"])),
        opposition_against_max_person = ','.join(map(str, out["against"]["maxOppID"])),
        opposition_abstain_max_person = ','.join(map(str, out["abstain"]["maxOppID"])),
        opposition_absent_max_person = ','.join(map(str, out["absent"]["maxOppID"]))
    )

    return JsonResponse({'alliswell': True, "status":'OK', "saved": final_response})


def getCutVotes(request, person_id, date=None):
    """
    * @api {get} /p/getCutVotes/{id}/{?date} [DEPRECATED] MP's vote numbers by option
    * @apiName getCutVotes
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs
      ballots categorised based on which option the ballot represented (for, against,
      abstain, not present). The function returns percentages as they were
      calculated for a given date, if no date is supplied it is assumed the
      date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object} results MP's percentage of each particular ballot type.
    
    * @apiSuccess {Object} results.absent Results (percentage of ballots) for "absent" ballot option.
    * @apiSuccess {Object} results.absent.avgCoalition Average coalition percentage of "absent" ballots.
    * @apiSuccess {Float} results.absent.avgCoalition.score The actual percentage.
    * @apiSuccess {Object} results.absent.avgOpposition Average opposition percentage of "absent" ballots.
    * @apiSuccess {Float} results.absent.avgOpposition.score The actual percentage.
    * @apiSuccess {Float} results.absent.score This MP's score.
    * @apiSuccess {Object} results.absent.maxCoalition MPs with the maximum score and their score.
    * @apiSuccess {Float} results.absent.maxCoalition.score Maximum score inside the coalition.
    * @apiSuccess {Object[]} results.absent.maxCoalition.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.absent.maxCoalition.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.absent.maxCoalition.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.absent.maxCoalition.mps.name MP's full name.
    * @apiSuccess {String} results.absent.maxCoalition.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.absent.maxCoalition.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.absent.maxCoalition.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.absent.maxCoalition.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.absent.maxCoalition.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.absent.maxCoalition.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.absent.maxCoalition.mps.party.name The party's name.
    * @apiSuccess {String} results.absent.maxCoalition.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.absent.maxCoalition.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Object} results.absent.maxOpposition MPs with the maximum score and their score.
    * @apiSuccess {Float} results.absent.maxOpposition.score Maximum score inside the opposition.
    * @apiSuccess {Object[]} results.absent.maxOpposition.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.absent.maxOpposition.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.absent.maxOpposition.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.absent.maxOpposition.mps.name MP's full name.
    * @apiSuccess {String} results.absent.maxOpposition.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.absent.maxOpposition.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.absent.maxOpposition.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.absent.maxOpposition.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.absent.maxOpposition.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.absent.maxOpposition.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.absent.maxOpposition.mps.party.name The party's name.
    * @apiSuccess {String} results.absent.maxOpposition.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.absent.maxOpposition.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).

    * @apiSuccess {Object} results.abstain Results (percentage of ballots) for "abstain" ballot option.
    * @apiSuccess {Object} results.abstain.avgCoalition Average coalition percentage of "abstain" ballots.
    * @apiSuccess {Float} results.abstain.avgCoalition.score The actual percentage.
    * @apiSuccess {Object} results.abstain.avgOpposition Average opposition percentage of "abstain" ballots.
    * @apiSuccess {Float} results.abstain.avgOpposition.score The actual percentage.
    * @apiSuccess {Float} results.abstain.score This MP's score.
    * @apiSuccess {Object} results.abstain.maxCoalition MPs with the maximum score and their score.
    * @apiSuccess {Float} results.abstain.maxCoalition.score Maximum score inside the coalition.
    * @apiSuccess {Object[]} results.abstain.maxCoalition.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.abstain.maxCoalition.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.abstain.maxCoalition.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.abstain.maxCoalition.mps.name MP's full name.
    * @apiSuccess {String} results.abstain.maxCoalition.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.abstain.maxCoalition.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.abstain.maxCoalition.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.abstain.maxCoalition.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.abstain.maxCoalition.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.abstain.maxCoalition.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.abstain.maxCoalition.mps.party.name The party's name.
    * @apiSuccess {String} results.abstain.maxCoalition.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.abstain.maxCoalition.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Object} results.abstain.maxOpposition MPs with the maximum score and their score.
    * @apiSuccess {Float} results.abstain.maxOpposition.score Maximum score inside the opposition.
    * @apiSuccess {Object[]} results.abstain.maxOpposition.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.abstain.maxOpposition.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.abstain.maxOpposition.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.abstain.maxOpposition.mps.name MP's full name.
    * @apiSuccess {String} results.abstain.maxOpposition.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.abstain.maxOpposition.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.abstain.maxOpposition.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.abstain.maxOpposition.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.abstain.maxOpposition.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.abstain.maxOpposition.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.abstain.maxOpposition.mps.party.name The party's name.
    * @apiSuccess {String} results.abstain.maxOpposition.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.abstain.maxOpposition.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).

    * @apiSuccess {Object} results.for Results (percentage of ballots) for "for" ballot option.
    * @apiSuccess {Object} results.for.avgCoalition Average coalition percentage of "for" ballots.
    * @apiSuccess {Float} results.for.avgCoalition.score The actual percentage.
    * @apiSuccess {Object} results.for.avgOpposition Average opposition percentage of "for" ballots.
    * @apiSuccess {Float} results.for.avgOpposition.score The actual percentage.
    * @apiSuccess {Float} results.for.score This MP's score.
    * @apiSuccess {Object} results.for.maxCoalition MPs with the maximum score and their score.
    * @apiSuccess {Float} results.for.maxCoalition.score Maximum score inside the coalition.
    * @apiSuccess {Object[]} results.for.maxCoalition.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.for.maxCoalition.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.for.maxCoalition.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.for.maxCoalition.mps.name MP's full name.
    * @apiSuccess {String} results.for.maxCoalition.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.for.maxCoalition.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.for.maxCoalition.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.for.maxCoalition.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.for.maxCoalition.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.for.maxCoalition.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.for.maxCoalition.mps.party.name The party's name.
    * @apiSuccess {String} results.for.maxCoalition.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.for.maxCoalition.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Object} results.for.maxOpposition MPs with the maximum score and their score.
    * @apiSuccess {Float} results.for.maxOpposition.score Maximum score inside the opposition.
    * @apiSuccess {Object[]} results.for.maxOpposition.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.for.maxOpposition.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.for.maxOpposition.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.for.maxOpposition.mps.name MP's full name.
    * @apiSuccess {String} results.for.maxOpposition.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.for.maxOpposition.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.for.maxOpposition.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.for.maxOpposition.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.for.maxOpposition.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.for.maxOpposition.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.for.maxOpposition.mps.party.name The party's name.
    * @apiSuccess {String} results.for.maxOpposition.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.for.maxOpposition.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).

    * @apiSuccess {Object} results.against Results (percentage of ballots) for "against" ballot option.
    * @apiSuccess {Object} results.against.avgCoalition Average coalition percentage of "against" ballots.
    * @apiSuccess {Float} results.against.avgCoalition.score The actual percentage.
    * @apiSuccess {Object} results.against.avgOpposition Average opposition percentage of "against" ballots.
    * @apiSuccess {Float} results.against.avgOpposition.score The actual percentage.
    * @apiSuccess {Float} results.against.score This MP's score.
    * @apiSuccess {Object} results.against.maxCoalition MPs with the maximum score and their score.
    * @apiSuccess {Float} results.against.maxCoalition.score Maximum score inside the coalition.
    * @apiSuccess {Object[]} results.against.maxCoalition.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.against.maxCoalition.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.against.maxCoalition.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.against.maxCoalition.mps.name MP's full name.
    * @apiSuccess {String} results.against.maxCoalition.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.against.maxCoalition.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.against.maxCoalition.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.against.maxCoalition.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.against.maxCoalition.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.against.maxCoalition.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.against.maxCoalition.mps.party.name The party's name.
    * @apiSuccess {String} results.against.maxCoalition.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.against.maxCoalition.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Object} results.against.maxOpposition MPs with the maximum score and their score.
    * @apiSuccess {Float} results.against.maxOpposition.score Maximum score inside the opposition.
    * @apiSuccess {Object[]} results.against.maxOpposition.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.against.maxOpposition.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.against.maxOpposition.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.against.maxOpposition.mps.name MP's full name.
    * @apiSuccess {String} results.against.maxOpposition.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.against.maxOpposition.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.against.maxOpposition.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.against.maxOpposition.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.against.maxOpposition.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.against.maxOpposition.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.against.maxOpposition.mps.party.name The party's name.
    * @apiSuccess {String} results.against.maxOpposition.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.against.maxOpposition.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getCutVotes/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getCutVotes/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "03.11.2016",
        "created_for": "28.08.2014",
        "results": {
            "absent": {
            "avgCoalition": {
                "score": 0.000599547511312217
            },
            "avgOpposition": {
                "score": 0.00142414860681115
            },
            "score": 29.4117647058824,
            "maxCoalition": {
                "score": 0.00470588235294118,
                "mps": [{
                "is_active": false,
                "district": [34],
                "name": "Karl Viktor Erjavec",
                "gov_id": "G20",
                "gender": "m",
                "party": {
                    "acronym": "DeSUS",
                    "is_coalition": true,
                    "id": 3,
                    "name": "PS Demokratska Stranka Upokojencev Slovenije"
                },
                "type": "mp",
                "id": 20,
                "has_function": false
                }]
            },
            "maxOpposition": {
                "score": 70.5882352941177,
                "mps": [{
                "is_active": false,
                "district": [25],
                "name": "Marijan Pojbi\u010d",
                "gov_id": "P098",
                "gender": "m",
                "party": {
                    "acronym": "SDS",
                    "is_coalition": false,
                    "id": 5,
                    "name": "PS Slovenska Demokratska Stranka"
                },
                "type": "mp",
                "id": 66,
                "has_function": false
                }]
            }
            },
            "abstain": {
            "avgCoalition": {
                "score": 1.13122171945701e-05
            },
            "avgOpposition": {
                "score": 0.00185758513931889
            },
            "score": 11.7647058823529,
            "maxCoalition": {
                "score": 0.000588235294117647,
                "mps": [{
                "is_active": false,
                "district": [76],
                "name": "Milan Brglez",
                "gov_id": "P243",
                "gender": "m",
                "party": {
                    "acronym": "SMC",
                    "is_coalition": true,
                    "id": 1,
                    "name": "PS Stranka modernega centra"
                },
                "type": "mp",
                "id": 11,
                "has_function": true
                }]
            },
            "maxOpposition": {
                "score": 35.2941176470588,
                "mps": [{
                "is_active": false,
                "district": [65],
                "name": "\u017dan Mahni\u010d",
                "gov_id": "P270",
                "gender": "m",
                "party": {
                    "acronym": "SDS",
                    "is_coalition": false,
                    "id": 5,
                    "name": "PS Slovenska Demokratska Stranka"
                },
                "type": "mp",
                "id": 55,
                "has_function": false
                }, {
                "is_active": false,
                "district": [71],
                "name": "Janez Jan\u0161a",
                "gov_id": "P025",
                "gender": "m",
                "party": {
                    "acronym": "SDS",
                    "is_coalition": false,
                    "id": 5,
                    "name": "PS Slovenska Demokratska Stranka"
                },
                "type": "mp",
                "id": 36,
                "has_function": false
                }, {
                "is_active": false,
                "district": [12],
                "name": "Toma\u017e Lisec",
                "gov_id": "P187",
                "gender": "m",
                "party": {
                    "acronym": "SDS",
                    "is_coalition": false,
                    "id": 5,
                    "name": "PS Slovenska Demokratska Stranka"
                },
                "type": "mp",
                "id": 53,
                "has_function": false
                }]
            }
            },
            "for": {
            "avgCoalition": {
                "score": 0.00780542986425339
            },
            "avgOpposition": {
                "score": 0.00501547987616099
            },
            "score": 35.2941176470588,
            "maxCoalition": {
                "score": 0.00941176470588235,
                "mps": [{
                "is_active": false,
                "district": [52],
                "name": "Ivan Prelog",
                "gov_id": "P279",
                "gender": "m",
                "party": {
                    "acronym": "SMC",
                    "is_coalition": true,
                    "id": 1,
                    "name": "PS Stranka modernega centra"
                },
                "type": "mp",
                "id": 68,
                "has_function": false
                }]
            },
            "maxOpposition": {
                "score": 82.3529411764706,
                "mps": [{
                "is_active": false,
                "district": [90],
                "name": "Roberto Battelli",
                "gov_id": "P005",
                "gender": "m",
                "party": {
                    "acronym": "IMNS",
                    "is_coalition": false,
                    "id": 2,
                    "name": "PS italijanske in mad\u017earske narodne skupnosti"
                },
                "type": "mp",
                "id": 4,
                "has_function": false
                }, {
                "is_active": false,
                "district": [91],
                "name": "L\u00e1szl\u00f3 G\u00f6ncz",
                "gov_id": "P117",
                "gender": "m",
                "party": {
                    "acronym": "IMNS",
                    "is_coalition": false,
                    "id": 2,
                    "name": "PS italijanske in mad\u017earske narodne skupnosti"
                },
                "type": "mp",
                "id": 24,
                "has_function": false
                }]
            }
            },
            "against": {
            "avgCoalition": {
                "score": 0.00158371040723982
            },
            "avgOpposition": {
                "score": 0.00170278637770898
            },
            "score": 23.5294117647059,
            "maxCoalition": {
                "score": 0.00333333333333333,
                "mps": [{
                "is_active": false,
                "district": [99],
                "name": "Du\u0161an Verbi\u010d",
                "gov_id": "P296",
                "gender": "m",
                "party": {
                    "acronym": "SMC",
                    "is_coalition": true,
                    "id": 1,
                    "name": "PS Stranka modernega centra"
                },
                "type": "mp",
                "id": 92,
                "has_function": false
                }]
            },
            "maxOpposition": {
                "score": 23.5294117647059,
                "mps": [{
                "is_active": false,
                "district": [28],
                "name": "Andrej \u010cu\u0161",
                "gov_id": "P225",
                "gender": "m",
                "party": {
                    "acronym": "SDS",
                    "is_coalition": false,
                    "id": 5,
                    "name": "PS Slovenska Demokratska Stranka"
                },
                "type": "mp",
                "id": 15,
                "has_function": false
                }, {
                "is_active": false,
                "district": [89],
                "name": "Eva Irgl",
                "gov_id": "P023",
                "gender": "f",
                "party": {
                    "acronym": "SDS",
                    "is_coalition": false,
                    "id": 5,
                    "name": "PS Slovenska Demokratska Stranka"
                },
                "type": "mp",
                "id": 35,
                "has_function": false
                }, {
                "is_active": false,
                "district": [9],
                "name": "Zvonko Lah",
                "gov_id": "P129",
                "gender": "m",
                "party": {
                    "acronym": "SDS",
                    "is_coalition": false,
                    "id": 5,
                    "name": "PS Slovenska Demokratska Stranka"
                },
                "type": "mp",
                "id": 49,
                "has_function": false
                }, {
                "is_active": false,
                "district": [65],
                "name": "\u017dan Mahni\u010d",
                "gov_id": "P270",
                "gender": "m",
                "party": {
                    "acronym": "SDS",
                    "is_coalition": false,
                    "id": 5,
                    "name": "PS Slovenska Demokratska Stranka"
                },
                "type": "mp",
                "id": 55,
                "has_function": false
                }, {
                "is_active": false,
                "district": [30],
                "name": "Jelka Godec",
                "gov_id": "P252",
                "gender": "f",
                "party": {
                    "acronym": "SDS",
                    "is_coalition": false,
                    "id": 5,
                    "name": "PS Slovenska Demokratska Stranka"
                },
                "type": "mp",
                "id": 23,
                "has_function": false
                }, {
                "is_active": false,
                "district": [55],
                "name": "Danijel Krivec",
                "gov_id": "P040",
                "gender": "m",
                "party": {
                    "acronym": "SDS",
                    "is_coalition": false,
                    "id": 5,
                    "name": "PS Slovenska Demokratska Stranka"
                },
                "type": "mp",
                "id": 47,
                "has_function": false
                }, {
                "is_active": false,
                "district": [12],
                "name": "Toma\u017e Lisec",
                "gov_id": "P187",
                "gender": "m",
                "party": {
                    "acronym": "SDS",
                    "is_coalition": false,
                    "id": 5,
                    "name": "PS Slovenska Demokratska Stranka"
                },
                "type": "mp",
                "id": 53,
                "has_function": false
                }, {
                "is_active": false,
                "district": [34],
                "name": "Ljubo \u017dnidar",
                "gov_id": "P212",
                "gender": "m",
                "party": {
                    "acronym": "SDS",
                    "is_coalition": false,
                    "id": 5,
                    "name": "PS Slovenska Demokratska Stranka"
                },
                "type": "mp",
                "id": 91,
                "has_function": false
                }, {
                "is_active": false,
                "district": [64],
                "name": "Miha Kordi\u0161",
                "gov_id": "P262",
                "gender": "m",
                "party": {
                    "acronym": "ZL",
                    "is_coalition": false,
                    "id": 8,
                    "name": "PS Zdru\u017eena Levica"
                },
                "type": "mp",
                "id": 42,
                "has_function": false
                }, {
                "is_active": false,
                "district": [15],
                "name": "Luka Mesec",
                "gov_id": "P273",
                "gender": "m",
                "party": {
                    "acronym": "ZL",
                    "is_coalition": false,
                    "id": 8,
                    "name": "PS Zdru\u017eena Levica"
                },
                "type": "mp",
                "id": 58,
                "has_function": false
                }]
            }
            }
        }
    }
    """
    cutVotes = getPersonCardModelNew(CutVotes, person_id, date)

    out = {
        'person': getPersonData(person_id, date),
        'created_at': cutVotes.created_at.strftime(API_DATE_FORMAT),
        'created_for': cutVotes.created_for.strftime(API_DATE_FORMAT),
        'results': {
            'abstain': {
                'score': cutVotes.this_abstain,
                'maxCoalition': {
                    'mps': [getPersonData(textid, date) for textid in cutVotes.coalition_abstain_max_person.split(',')],
                    'score': cutVotes.coalition_abstain_max
                },
                'maxOpposition': {
                    'mps': [getPersonData(textid, date)  for textid in cutVotes.opposition_abstain_max_person.split(',')],
                    'score': cutVotes.opposition_abstain_max
                },
                "avgOpposition": {'score': cutVotes.opposition_abstain},
                "avgCoalition": {'score': cutVotes.coalition_abstain},
            },
            "against": {
                'score': cutVotes.this_against,
                'maxCoalition': {
                    'mps': [getPersonData(textid, date) for textid in cutVotes.coalition_against_max_person.split(',')],
                    'score': cutVotes.coalition_against_max
                },
                'maxOpposition': {
                    'mps': [getPersonData(textid, date) for textid in cutVotes.opposition_against_max_person.split(',')],
                    'score': cutVotes.opposition_against_max
                },
                "avgOpposition": {'score': cutVotes.opposition_against},
                "avgCoalition": {'score': cutVotes.coalition_against},
            },
            "absent": {
                'score': cutVotes.this_absent,
                'maxCoalition': {
                    'mps': [getPersonData(textid, date) for textid in cutVotes.coalition_absent_max_person.split(',')],
                    'score': cutVotes.coalition_absent_max
                },
                'maxOpposition': {
                    'mps': [getPersonData(textid, date) for textid in cutVotes.opposition_absent_max_person.split(',')],
                    'score': cutVotes.opposition_absent_max
                },
                "avgOpposition": {'score': cutVotes.opposition_absent},
                "avgCoalition": {'score': cutVotes.coalition_absent},
            },
            'for': {
                'score': cutVotes.this_for,
                'maxCoalition': {
                    'mps': [getPersonData(textid, date) for textid in cutVotes.coalition_for_max_person.split(',')],
                    'score': cutVotes.coalition_for_max
                },
                'maxOpposition': {
                    'mps': [getPersonData(textid, date) for textid in cutVotes.opposition_for_max_person.split(',')],
                    'score': cutVotes.opposition_for_max
                },
                "avgOpposition": {'score': cutVotes.opposition_for},
                "avgCoalition": {'score': cutVotes.coalition_for},
            },
        }
    }
    return JsonResponse(out)


def getStyleScores(request, person_id, date_=None):
    """
    * @api {get} /p/getStyleScores/{id}/{?date} MP's style scores
    * @apiName getStyleScores
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs
      style scores. The function returns the scores as they were calculated
      for a given date. If no date is supplied it is assumed the date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object} results MP's style scores.
    * @apiSuccess {Float} results.problematicno MP's "problematic" language score.
    * @apiSuccess {Float} results.preprosto MP's "simple" language score.
    * @apiSuccess {Float} results.privzdignjeno MP's "fancy" language score.
    

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getStyleScores/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getStyleScores/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "02.11.2016",
        "created_for": "06.09.2014",
        "results": {
            "problematicno": 0.6451263190481497,
            "preprosto": 1.0269481824385878,
            "privzdignjeno": 0
        }
    }
    """
    card = getPersonCardModelNew(StyleScores, int(person_id), date_)

    privzdignjeno = 0
    problematicno = 0
    preprosto = 0

    if card.privzdignjeno != 0 and card.privzdignjeno_average != 0:
        privzdignjeno = card.privzdignjeno/card.privzdignjeno_average
    
    if card.problematicno != 0 and card.problematicno_average != 0:
        problematicno = card.problematicno/card.problematicno_average
    
    if card.preprosto != 0 and card.preprosto_average != 0:
        preprosto = card.preprosto/card.preprosto_average

    out = {
        'created_at': card.created_at.strftime(API_DATE_FORMAT),
        'created_for': card.created_for.strftime(API_DATE_FORMAT),
        'person': getPersonData(person_id, card.created_for.strftime(API_DATE_FORMAT)),
        'results': {
            'privzdignjeno': privzdignjeno,
            'problematicno': problematicno,
            'preprosto': preprosto
            # 'average': {
            #     'privzdignjeno': card.privzdignjeno_average*10000,
            #     'problematicno': card.problematicno_average*10000,
            #     'preprosto': card.preprosto_average*10000
            # }
        }
    }

    return JsonResponse(out, safe=False)

def getTotalStyleScores(request): # TODO refactor remove?
#    speeches = tryHard(API_URL+'/getAllSpeeches/').json()
#    speeches_content = [speech['content'] for speech in speeches]
#    speeches_megastring = string.join(speeches_content)
#
#    counter = Counter()
#    counter = countWords(speeches_megastring, counter)
#    total = sum(counter.values())

    data = tryHard('http://parlameter.si:8983/solr/knedl/admin/luke?fl=content_t&numTerms=200000&wt=json').json()

    wordlist = data['fields']['content_t']['topTerms']

    wordlist_new = {}
    i = 0
    limit = len(wordlist)/2

    while i < limit:

        if wordlist[i + 1] > 0:
            wordlist_new[wordlist[i]] = wordlist[i + 1]
        else:
            break

        i = i + 2

    counter = Counter(wordlist_new)
    total = sum(counter.values())

    output = getScores([problematicno, privzdignjeno, preprosto], counter, total)
#    output = {'problematicno': getScore(problematicno, counter, total),
#              'privzdignjeno': getScore(privzdignjeno, counter, total),
#              'preprosto': getScore(preprosto, counter, total),
##              'total': total
#             }

    return JsonResponse(output, safe=False)

def makeAverageStyleScores(date_): # TODO refactor cleanup
#    speeches = tryHard(API_URL+'/getAllSpeeches/').json()
#    speeches_content = [speech['content'] for speech in speeches]
#    speeches_megastring = string.join(speeches_content)

    #data = tryHard('http://parlameter.si:8983/solr/knedl/admin/luke?fl=content_t&numTerms=200000&wt=json').json()
    data = tryHard('https://isci.parlameter.si/dfall/'+date_).json()

    #wordlist = data['fields']['content_t']['topTerms']

    wordlist_new = {word["term"]: word["df"] for word in data}


    counter = Counter(wordlist_new)
#    counter = countWords(speeches_megastring, counter)
    total = sum(counter.values())
    print total

    output = getScores([problematicno, privzdignjeno, preprosto], counter, total)

#    output = {'problematicno': getScore(problematicno, counter, total),
#              'privzdignjeno': getScore(privzdignjeno, counter, total),
#              'preprosto': getScore(preprosto, counter, total),
#             }

    return output

def setTFIDFold(request, person_id): # TODO refactor remove?

    mps = tryHard(API_URL+'/getMPs/').json()

    person = Person.objects.get(id_parladata=int(person_id))

    mp_ids = [mp['id'] for mp in mps]

    speeches_grouped = [{'person_id': mp, 'speeches': tryHard(API_URL+'/getSpeeches/' + str(mp)).json()} for mp in mp_ids]

    tfidf = TFIDF(speeches_grouped, person_id)

    print tfidf[:10]

    newtfidf = []
    for i, term in enumerate(tfidf[:10]):
        term['rank'] = i + 1
        newtfidf.append(term)

    if saveOrAbort(Tfidf, person=person, data=newtfidf):

        return HttpResponse('All iz well')

    else:
        return HttpResponse('All waz well');

def setTFIDF(request, person_id, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT)
    else:
        date_of = datetime.now().date()
        date_ = date_of.strftime(API_DATE_FORMAT)

    print "TFIDF", person_id
    data = tryHard("https://isci.parlameter.si/tfidf/nodigrams/p/"+person_id).json()
    is_saved = saveOrAbortNew(Tfidf,
                              person=Person.objects.get(id_parladata=person_id),
                              created_for=date_of,
                              is_visible=False,
                              data=data["results"])

    return JsonResponse({"alliswell": True,
                         "saved": is_saved})

def getTFIDF(request, person_id, date_=None):
    """
    * @api {get} /p/getTFIDF/{id}/{?date} MP's top TFIDF terms
    * @apiName getTFIDF
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs
      top TFIDF terms. It returns between 10 and 15 terms, depending on the
      topical overlap of the top 15 terms. The function returns the score as
      it was calculated for a given date, if no date is supplied it is assumed
      the date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object[]} results MP's top TFIDF words (between 10 and 15).
    * @apiSuccess {String} results.term The term in question.
    * @apiSuccess {Object} results.scores TFIDF scores
    * @apiSuccess {Integer} results.scores.tf Term frequency.
    * @apiSuccess {Integer} results.scores.df Document frequency.
    * @apiSuccess {Float} results.scores.tf-idf TF/DF.

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getTFIDF/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getTFIDF/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "20.02.2017",
        "created_for": "20.02.2017",
        "results": [{
            "term": "transma\u0161\u010doba",
            "scores": {
            "tf": 27,
            "df": 30,
            "tf-idf": 0.9
            }
        }, {
            "term": "transma\u0161\u010doben",
            "scores": {
            "tf": 12,
            "df": 14,
            "tf-idf": 0.8571428571428571
            }
        }, {
            "term": "borznoposredni\u0161ki",
            "scores": {
            "tf": 47,
            "df": 59,
            "tf-idf": 0.7966101694915254
            }
        }, {
            "term": "soupravljanje",
            "scores": {
            "tf": 82,
            "df": 126,
            "tf-idf": 0.6507936507936508
            }
        }, {
            "term": "trgovalen",
            "scores": {
            "tf": 49,
            "df": 80,
            "tf-idf": 0.6125
            }
        }, {
            "term": "Cinven",
            "scores": {
            "tf": 35,
            "df": 63,
            "tf-idf": 0.5555555555555556
            }
        }, {
            "term": "borzen",
            "scores": {
            "tf": 60,
            "df": 114,
            "tf-idf": 0.5263157894736842
            }
        }, {
            "term": "Alpina",
            "scores": {
            "tf": 37,
            "df": 82,
            "tf-idf": 0.45121951219512196
            }
        }, {
            "term": "kislina",
            "scores": {
            "tf": 14,
            "df": 32,
            "tf-idf": 0.4375
            }
        }, {
            "term": "obvezni\u010dar",
            "scores": {
            "tf": 11,
            "df": 26,
            "tf-idf": 0.4230769230769231
            }
        }, {
            "term": "registrski",
            "scores": {
            "tf": 73,
            "df": 175,
            "tf-idf": 0.41714285714285715
            }
        }, {
            "term": "Lahovnikov zakon",
            "scores": {
            "tf": 20,
            "df": 49,
            "tf-idf": 0.40816326530612246
            }
        }, {
            "term": "\u010cate\u017e",
            "scores": {
            "tf": 12,
            "df": 30,
            "tf-idf": 0.4
            }
        }, {
            "term": "cigareta",
            "scores": {
            "tf": 32,
            "df": 81,
            "tf-idf": 0.3950617283950617
            }
        }, {
            "term": "progresija",
            "scores": {
            "tf": 15,
            "df": 43,
            "tf-idf": 0.3488372093023256
            }
        }, {
            "term": "neizpla\u010dan",
            "scores": {
            "tf": 28,
            "df": 82,
            "tf-idf": 0.34146341463414637
            }
        }, {
            "term": "delavski",
            "scores": {
            "tf": 197,
            "df": 582,
            "tf-idf": 0.3384879725085911
            }
        }, {
            "term": "Helios",
            "scores": {
            "tf": 38,
            "df": 116,
            "tf-idf": 0.3275862068965517
            }
        }, {
            "term": "predkupen",
            "scores": {
            "tf": 25,
            "df": 80,
            "tf-idf": 0.3125
            }
        }, {
            "term": "Telekom",
            "scores": {
            "tf": 201,
            "df": 648,
            "tf-idf": 0.3101851851851852
            }
        }, {
            "term": "Siriza",
            "scores": {
            "tf": 14,
            "df": 46,
            "tf-idf": 0.30434782608695654
            }
        }, {
            "term": "prekeren",
            "scores": {
            "tf": 33,
            "df": 109,
            "tf-idf": 0.30275229357798167
            }
        }, {
            "term": "pregrevanje",
            "scores": {
            "tf": 27,
            "df": 90,
            "tf-idf": 0.3
            }
        }, {
            "term": "klasificirati",
            "scores": {
            "tf": 25,
            "df": 84,
            "tf-idf": 0.2976190476190476
            }
        }]
    }
    """

    card = getPersonCardModelNew(Tfidf, int(person_id), date=date_, is_visible=True)

    out = {
        'person': getPersonData(person_id, date_),
        'results': card.data,
        "created_for": card.created_for.strftime(API_DATE_FORMAT), 
        "created_at": card.created_at.strftime(API_DATE_FORMAT)
    }

    return JsonResponse(out)

def setVocabularySizeAndSpokenWords(request, date_=None):
    sw = WordAnalysis(count_of="members", date_=date_)

    if not sw.isNewSpeech:
        return JsonResponse({'alliswell': False})

    #Vocabolary size
    all_score = sw.getVocabularySize()
    max_score, maxMPid = sw.getMaxVocabularySize()
    avg_score = sw.getAvgVocabularySize()
    date_of = sw.getDate()
    maxMP = Person.objects.get(id_parladata=maxMPid)

    print "[INFO] saving vocabulary size"
    for p in all_score:
        saveOrAbortNew(model=VocabularySize,
                       person=Person.objects.get(id_parladata=int(p['counter_id'])),
                       created_for=date_of,
                       score=int(p['coef']),
                       maxMP=maxMP,
                       average=avg_score,
                       maximum=max_score)

    #Unique words
    all_score = sw.getUniqueWords()
    max_score, maxMPid = sw.getMaxUniqueWords()
    avg_score = sw.getAvgUniqueWords()
    date_of = sw.getDate()
    maxMP = Person.objects.get(id_parladata=maxMPid)

    print "[INFO] saving unique words"
    for p in all_score:
        saveOrAbortNew(model=VocabularySizeUniqueWords,
                       person=Person.objects.get(id_parladata=int(p['counter_id'])),
                       created_for=date_of,
                       score=int(p['unique']),
                       maxMP=maxMP,
                       average=avg_score,
                       maximum=max_score)

    #Spoken words
    all_words = sw.getSpokenWords()
    max_words, maxWordsMPid = sw.getMaxSpokenWords()
    avgSpokenWords = sw.getAvgSpokenWords()
    date_of = sw.getDate()
    maxMP = Person.objects.get(id_parladata=maxWordsMPid)

    print "[INFO] saving spoken words"
    for p in all_words:
        saveOrAbortNew(model=SpokenWords,
                       created_for=date_of,
                       person=Person.objects.get(id_parladata=int(p['counter_id'])),
                       score=int(p['wordcount']),
                       maxMP=maxMP,
                       average=avgSpokenWords,
                       maximum=max_words)

    return HttpResponse('All MPs updated.')

#Depricated
def setVocabularySizeALL(request, date_): # TODO refactor remove? 
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_=""

#    thisperson = Person.objects.get(id_parladata=int(person_id))

    mps = tryHard(API_URL+'/getMPs/'+date_).json()

    vocabulary_sizes = []
    result = {}

    for mp in mps:

        speeches = tryHard(API_URL+'/getSpeeches/' + str(mp['id']) + ("/"+date_) if date_ else "").json()

        text = ''.join([speech['content'] for speech in speeches])

        vocabulary_sizes.append({'person_id': mp['id'], 'vocabulary_size': len(countWords(text, Counter()))})

#        if int(mp['id']) == int(person_id):
#            result['person'] = len(countWords(text, Counter()))

    vocabularies_sorted = sorted(vocabulary_sizes, key=lambda k: k['vocabulary_size'])

    scores = [person['vocabulary_size'] for person in vocabulary_sizes]

    result['average'] = float(sum(scores))/float(len(scores))

    result['max'] = vocabularies_sorted[-1]['vocabulary_size']
    maxMP = Person.objects.get(id_parladata=vocabularies_sorted[-1]['person_id'])

#    result.append({'person_id': vocabularies_sorted[-1]['person_id'], 'vocabulary_size': vocabularies_sorted[-1]['vocabulary_size']})

    for p in vocabularies_sorted:
        saveOrAbortNew(
            VocabularySize,
            person=Person.objects.get(id_parladata=int(p['person_id'])),
            created_for=date_of,
            score=[v['vocabulary_size'] for v in vocabularies_sorted if v['person_id'] == p['person_id']][0],
            maxMP=maxMP,
            average=result['average'],
            maximum=result['max'])

    return HttpResponse('All MPs updated.')

#    if saveOrAbort(VocabularySize, person=thisperson, score=result['person'], maxMP=maxMP, average=result['average'], maximum=result['max']):
#        return HttpResponse('All iz well')
#    else:
#        return HttpResponse('All was well')
#
#    result_ = saveOrAbort(model=VocabularySize, person=Person.objects.get(id_parladata=int(person_id)), this_person=result[0]['vocabulary_size'], maxMP=Person.objects.get(id_parladata=int(vocabularies_sorted[-1]['person_id'])), average=float(sum(scores))/float(len(scores)), maximum=vocabularies_sorted[-1]['vocabulary_size'])
#
#    return JsonResponse(result, safe=False)

def setVocabularySize(request, person_id, date_=None): # TODO refactor cleanup
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = findDatesFromLastCard(VocabularySize, person_id, datetime.now().strftime(API_DATE_FORMAT))[0]
        date_=""

    thisperson = Person.objects.get(id_parladata=int(person_id))

    mps = tryHard(API_URL+'/getMPs/'+date_).json()

    vocabulary_sizes = []
    result = {}

    for mp in mps:

        speeches = tryHard(API_URL+'/getSpeeches/'+date_ + str(mp['id'])).json()

        text = ''.join([speech['content'] for speech in speeches])

        vocabulary_sizes.append({'person_id': mp['id'], 'vocabulary_size': len(countWords(text, Counter()))})

        if int(mp['id']) == int(person_id):
            result['person'] = len(countWords(text, Counter()))

    vocabularies_sorted = sorted(vocabulary_sizes, key=lambda k: k['vocabulary_size'])

    scores = [person['vocabulary_size'] for person in vocabulary_sizes]

    result['average'] = float(sum(scores))/float(len(scores))

    result['max'] = vocabularies_sorted[-1]['vocabulary_size']
    maxMP = Person.objects.get(id_parladata=vocabularies_sorted[-1]['person_id'])

#    result.append({'person_id': vocabularies_sorted[-1]['person_id'], 'vocabulary_size': vocabularies_sorted[-1]['vocabulary_size']})

#    for p in vocabularies_sorted:
#        saveOrAbort(
#            VocabularySize,
#            person=Person.objects.get(id_parladata=int(p['person_id'])),
#            score=[v['vocabulary_size'] for v in vocabularies_sorted if v['person_id'] == p['person_id']][0],
#            maxMP=maxMP,
#            average=result['average'],
#            maximum=result['max'])
#
#    return HttpResponse('All MPs updated.')

    if saveOrAbortNew(VocabularySize,
                      person=thisperson,
                      created_for=date_of,
                      score=result['person'],
                      maxMP=maxMP,
                      average=result['average'],
                      maximum=result['max']):
        return HttpResponse('All iz well')
    else:
        return HttpResponse('All was well')


def getVocabularySize(request, person_id, date_=None):
    """
    * @api {get} /p/getVocabularySize/{id}/{?date} MP's vocabulary size
    * @apiName getVocabularySize
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs
      calculated vocabulary size. The function returns the score as it was
      calculated for a given date, if no date is supplied it is assumed
      the date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object} results MP's vocabulary size.
    * @apiSuccess {Object} results.max MP (or MPs) who has the highest vocabulary size and their score.
    * @apiSuccess {Float} results.max.score Max MP's score.
    * @apiSuccess {Object[]} results.max.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.max.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.max.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.max.mps.name MP's full name.
    * @apiSuccess {String} results.max.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.max.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.max.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.max.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.max.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.max.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.max.mps.party.name The party's name.
    * @apiSuccess {String} results.max.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.max.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Float} results.average The average score for this metric accross the parliament.
    * @apiSuccess {Float} results.score Score for the MP in question.
    

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getVocabularySize/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getVocabularySize/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "14.11.2016",
        "created_for": "10.09.2014",
        "results": {
            "max": {
            "score": 744.915094339623,
            "mps": [{
                "is_active": false,
                "district": [40],
                "name": "Benedikt Kopmajer",
                "gov_id": "P261",
                "gender": "m",
                "party": {
                "acronym": "DeSUS",
                "is_coalition": true,
                "id": 3,
                "name": "PS Demokratska Stranka Upokojencev Slovenije"
                },
                "type": "mp",
                "id": 41,
                "has_function": false
            }]
            },
            "average": 388.298609949473,
            "score": 592.0
        }
    }
    """

    card = getPersonCardModelNew(VocabularySize, person_id, date_)

    out = {
        'person': getPersonData(person_id, date_),
        'created_at': card.created_at.strftime(API_DATE_FORMAT),
        'created_for': card.created_for.strftime(API_DATE_FORMAT),
        'results': {
            'max': {
                'score': card.maximum,
                'mps': [getPersonData(card.maxMP.id_parladata, date_)]
            },
            'average': card.average,
            'score': card.score
        }
    }

    return JsonResponse(out, safe=False)


def getVocabolarySizeLanding(request, date_=None): # TODO refactor typo getVocabularySize
    """
    * @api {get} /p/getVocabularySizeLanding/{?date} Vocabulary sizes of all MPs
    * @apiName getVocabularySizeLanding
    * @apiGroup Other
    * @apiDescription This function returns a list of objects representing
      MPs and their vocabulary size scores. The function
      returns the scores as it was calculated for a given date, if no date
      is supplied it is assumed the date is today.
    * @apiParam {date} date Optional date.

    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object[]} data list of MPs and their coordinates

    * @apiSuccess {Object} data.person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} data.person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} data.person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} data.person.name MP's full name.
    * @apiSuccess {String} data.person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} data.person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} data.person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} data.person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} data.person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} data.person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} data.person.party.name The party's name.
    * @apiSuccess {String} data.person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} data.person.id The person's Parladata id.
    * @apiSuccess {Boolean} data.person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).

    * @apiSucces {Float} data.score MP's vocabulary size
    
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getVocabularySizeLanding/
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getVocabularySizeLanding/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "created_at": "21.03.2017",
        "created_for": "20.03.2017",
        "data": [{
            "person": {
            "is_active": false,
            "district": [71],
            "name": "Janez Jan\u0161a",
            "gov_id": "P025",
            "gender": "m",
            "party": {
                "acronym": "SDS",
                "is_coalition": false,
                "id": 5,
                "name": "PS Slovenska Demokratska Stranka"
            },
            "type": "mp",
            "id": 36,
            "has_function": false
            },
            "score": 81.0
        }, {
            "person": {
            "is_active": false,
            "district": [83],
            "name": "Marko Ferluga",
            "gov_id": "P250",
            "gender": "m",
            "party": {
                "acronym": "SMC",
                "is_coalition": true,
                "id": 1,
                "name": "PS Stranka modernega centra"
            },
            "type": "mp",
            "id": 21,
            "has_function": false
            },
            "score": 84.0
        }, {
            "person": {
            "is_active": false,
            "district": [40],
            "name": "Ivan \u0160kodnik",
            "gov_id": "P286",
            "gender": "m",
            "party": {
                "acronym": "SMC",
                "is_coalition": true,
                "id": 1,
                "name": "PS Stranka modernega centra"
            },
            "type": "mp",
            "id": 76,
            "has_function": false
            },
            "score": 87.0
        }]
    }
    """
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        person_id=None
        if not VocabularySize.objects.all():
            raise Http404("Nismo našli kartice")
        date_of = VocabularySize.objects.latest("created_for").created_for
        date_ = date_of.strftime(API_DATE_FORMAT)
    mps = tryHard(API_URL+'/getMPs/'+date_).json()
    datas = []
    for mp in mps: 
        try:
            datas.append(getPersonCardModelNew(VocabularySize, mp["id"], date_))
        except:
            print "ni se goborila"
    print datas
    return JsonResponse({"created_for": date_, 
                         "created_at": datas[0].created_at.strftime(API_DATE_FORMAT) if datas else date_, 
                         "data": sorted([{"person": getPersonData(data.person.id_parladata, date_), 
                            "score": data.score} for data in datas if data.score > 0], key=lambda k: k['score'])}, 
                         safe=False)


def getVocabolarySizeUniqueWordsLanding(request, date_=None): # TODO refactor typo getVocabularySize
    """
    * @api {get} /p/getUniqueWordsLanding/{?date} [DEPRECATED] Number of unique words spoken by MPs
    * @apiName getUniqueWordsLanding
    * @apiGroup Other
    * @apiDescription This function returns a list of objects representing
      MPs and the number of unique words. The function
      returns the scores as it was calculated for a given date, if no date
      is supplied it is assumed the date is today.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object[]} / list of MPs and their scores

    * @apiSuccess {Object} /.person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} /.person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} /.person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} /.person.name MP's full name.
    * @apiSuccess {String} /.person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} /.person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} /.person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} /.person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} /.person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} /.person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} /.person.party.name The party's name.
    * @apiSuccess {String} /.person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} /.person.id The person's Parladata id.
    * @apiSuccess {Boolean} /.person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).

    * @apiSucces {Integer} /.score MP's number of unique spoken words.
    
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getUniqueWordsLanding/
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getUniqueWordsLanding/12.12.2016

    * @apiSuccessExample {json} Example response:
    [
        {
            "person": {
            "is_active": false,
            "district": [84],
            "name": "Vlasta Po\u010dkaj",
            "gov_id": "P303",
            "gender": "f",
            "party": {
                "acronym": "SMC",
                "is_coalition": true,
                "id": 1,
                "name": "PS Stranka modernega centra"
            },
            "type": "mp",
            "id": 2934,
            "has_function": false
            },
            "score": 263.0
        }, {
            "person": {
            "is_active": false,
            "district": [85],
            "name": "Teja Ljubi\u010d",
            "gov_id": "P304",
            "gender": "f",
            "party": {
                "acronym": "SMC",
                "is_coalition": true,
                "id": 1,
                "name": "PS Stranka modernega centra"
            },
            "type": "mp",
            "id": 2933,
            "has_function": false
            },
            "score": 310.0
        }, {
            "person": {
            "is_active": false,
            "district": [52],
            "name": "Ivan Prelog",
            "gov_id": "P279",
            "gender": "m",
            "party": {
                "acronym": "SMC",
                "is_coalition": true,
                "id": 1,
                "name": "PS Stranka modernega centra"
            },
            "type": "mp",
            "id": 68,
            "has_function": false
            },
            "score": 2007.0
        }
    ]
    """
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        person_id=None
        date_of = VocabularySizeUniqueWords.objects.all().order_by("-created_for")[0].created_for
        date_ = date_of.strftime(API_DATE_FORMAT)
    mps = tryHard(API_URL+'/getMPs/'+date_).json()
    datas = [getPersonCardModelNew(VocabularySizeUniqueWords, mp["id"], date_) for mp in mps]
    print datas
    return JsonResponse(sorted([{"person": getPersonData(data.person.id_parladata, date_), 
                                 "score": data.score} for data in datas], key=lambda k: k['score']), safe=False)


#just method ALL is edited for date
def setAverageNumberOfSpeechesPerSession(request, person_id): # TODO refactor remove?

    person = Person.objects.get(id_parladata=int(person_id))
    speeches = tryHard(API_URL+'/getSpeechesOfMP/' + person_id).json()
    no_of_speeches = len(speeches)

    # fix for "Dajem besedo"
    #no_of_speeches = no_of_speeches - int(tryHard(API_URL + '/getNumberOfFormalSpeeches/' + person_id))

    no_of_sessions = tryHard(API_URL+ '/getNumberOfPersonsSessions/' + person_id).json()['sessions_with_speech']

    score = no_of_speeches/no_of_sessions

    mps = tryHard(API_URL+'/getMPs/').json()
    mp_scores = []

    for mp in mps:
        mp_no_of_speeches = len(tryHard(API_URL+'/getSpeechesOfMP/' + str(mp['id'])).json())

        mp_no_of_sessions = tryHard(API_URL+ '/getNumberOfPersonsSessions/' + str(mp['id'])).json()['sessions_with_speech']

        mp_scores.append({'id': mp['id'], 'score': mp_no_of_speeches/mp_no_of_sessions})


    mp_scores_sorted = sorted(mp_scores, key=lambda k: k['score'])

    average = sum([mp['score'] for mp in mp_scores])/len(mp_scores)

    saveOrAbort(model=AverageNumberOfSpeechesPerSession, person=person, score=score, average=average, maximum=mp_scores_sorted[-1]['score'], maxMP=Person.objects.get(id_parladata=int(mp['id'])))

    return HttpResponse('All iz well')

def setAverageNumberOfSpeechesPerSessionAll(request, date_=None): # TODO refactor check if float
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = findDatesFromLastCard(Presence, person_id, datetime.now().date())[0]
        date_=""

    mps = tryHard(API_URL+'/getMPs/'+date_).json()
    mp_scores = []

    for mp in mps:
        mp_no_of_speeches = len(tryHard(API_URL+'/getSpeechesOfMP/' + str(mp['id'])  + ("/"+date_) if date_ else "").json())

        # fix for "Dajem besedo"
        #mp_no_of_speeches = mp_no_of_speeches - int(tryHard(API_URL + '/getNumberOfFormalSpeeches/' + str(mp['id']) + ("/"+date_) if date_ else "").text)

        mp_no_of_sessions = tryHard(API_URL+ '/getNumberOfPersonsSessions/' + str(mp['id']) + ("/"+date_) if date_ else "").json()['sessions_with_speech']

        if mp_no_of_sessions > 0:
            mp_scores.append({'id': mp['id'], 'score': mp_no_of_speeches/mp_no_of_sessions})
        else:
            mp_scores.append({'id': mp['id'], 'score': 0})


    mp_scores_sorted = sorted(mp_scores, key=lambda k: k['score'])

    average = sum([mp['score'] for mp in mp_scores])/len(mp_scores)

    for mp in mp_scores_sorted:
        person = Person.objects.get(id_parladata=int(mp['id']))
        score = mp['score']


        saveOrAbortNew(
            model=AverageNumberOfSpeechesPerSession,
            created_for=date_of,
            person=person,
            score=score,
            average=average,
            maximum=mp_scores_sorted[-1]['score'],
            maxMP=Person.objects.get(id_parladata=int(mp_scores_sorted[-1]['id'])))

    return HttpResponse('All iz well')

def getAverageNumberOfSpeechesPerSession(request, person_id, date=None):
    """
    * @api {get} /p/getAverageNumberOfSpeechesPerSession/{id}/{?date} MP's average number of speeches per session
    * @apiName getAverageNumberOfSpeechesPerSession
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs
      calculated average number of speeches per session. The function
      returns the score as it was calculated for a given date, if no date is
      supplied the date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object} results MP's average number of speeches per session.
    * @apiSuccess {Object} results.max MP (or MPs) who has the highest speeches per session and their score.
    * @apiSuccess {Integer} results.max.score Max MP's score.
    * @apiSuccess {Object[]} results.max.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.max.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.max.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.max.mps.name MP's full name.
    * @apiSuccess {String} results.max.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.max.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.max.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.max.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.max.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.max.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.max.mps.party.name The party's name.
    * @apiSuccess {String} results.max.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.max.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Integer} results.average The average score for this metric accross the parliament.
    * @apiSuccess {Integer} results.score Score for the MP in question.
    

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getAverageNumberOfSpeechesPerSession/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getAverageNumberOfSpeechesPerSession/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "02.11.2016",
        "created_for": "06.09.2014",
        "results": {
            "max": {
            "score": 31.0,
            "mps": [{
                "is_active": false,
                "district": [76],
                "name": "Milan Brglez",
                "gov_id": "P243",
                "gender": "m",
                "party": {
                "acronym": "SMC",
                "is_coalition": true,
                "id": 1,
                "name": "PS Stranka modernega centra"
                },
                "type": "mp",
                "id": 11,
                "has_function": true
            }]
            },
            "average": 2.0,
            "score": 2.0
        }
    }
    """

    card = getPersonCardModelNew(AverageNumberOfSpeechesPerSession, person_id, date)
    #static = getPersonCardModelNew(MPStaticPL, person_id, date)

    out = {
        'person': getPersonData(person_id, date),
        'created_at': card.created_at.strftime(API_DATE_FORMAT),
        'created_for': card.created_for.strftime(API_DATE_FORMAT),
        'results': {
            'max': {
                'score': card.maximum,
                'mps': [getPersonData(card.maxMP.id_parladata, date)]
            },
            'average': card.average,
            'score': card.score
        }
    }

    return JsonResponse(out, safe=False)


# get MPs IDs
def getMPsIDs(request): # TODO document understand?
    output = []
    data = tryHard(API_URL+'/getMPs/')
    data = data.json()

    output = {"list": [i['id'] for i in data], "lastDate": Session.objects.all().order_by("-start_time")[0].start_time.strftime(API_DATE_FORMAT)}

    return JsonResponse(output, safe=False)


def setCompass(request, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_ = date_of.strftime(API_DATE_FORMAT)

    isNewVote = tryHard(API_URL +'/isVoteOnDay/'+date_).json()["isVote"]
    print isNewVote
    if not isNewVote:
        return JsonResponse({'alliswell': True, "status":'Ni glasovanja na ta dan', "saved": False})

    data = getCompassData(date_of)
    if data == []:
        return JsonResponse({"status": "no data"})
    #print data
    existing_compas = Compass.objects.filter(created_for=date_of)
    if existing_compas:
        existing_compas[0].data = data
        existing_compas[0].save()
    else:
        Compass(created_for=date_of,
                data=data).save()

    return JsonResponse({'alliswell': True, "status":'OK', "saved": True})

def getCompass(request, date_=None): # TODO make proper setters and getters
    """
    * @api {get} /p/getCompass/{?date} Political compass
    * @apiName getCompass
    * @apiGroup Other
    * @apiDescription This function returns a list of objects representing
      MPs and their coordinates on the "political compass". The function
      returns the scores as it was calculated for a given date, if no date
      is supplied it is assumed the date is today.
    * @apiParam {date} date Optional date.

    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object[]} data list of MPs and their coordinates

    * @apiSuccess {Object} data.person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} data.person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} data.person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} data.person.name MP's full name.
    * @apiSuccess {String} data.person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} data.person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} data.person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} data.person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} data.person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} data.person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} data.person.party.name The party's name.
    * @apiSuccess {String} data.person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} data.person.id The person's Parladata id.
    * @apiSuccess {Boolean} data.person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).

    * @apiSucces {Object} data.score MP's coordinates
    * @apiSuccess {Float} data.score.vT1 First coordinate
    * @apiSuccess {Float} data.score.vT2 Second coordinate
    

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getCompass/
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getCompass/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "created_at": "21.03.2017",
        "created_for": "17.02.2017",
        "data": [{
            "person": {
            "is_active": false,
            "district": [7],
            "name": "Anja Bah \u017dibert",
            "gov_id": "P239",
            "gender": "f",
            "party": {
                "acronym": "SDS",
                "is_coalition": false,
                "id": 5,
                "name": "PS Slovenska Demokratska Stranka"
            },
            "type": "mp",
            "id": 2,
            "has_function": false
            },
            "score": {
            "vT1": 0.18281964948320664,
            "vT2": -0.05594373814997616
            }
        }, {
            "person": {
            "is_active": false,
            "district": [8],
            "name": "Ur\u0161ka Ban",
            "gov_id": "P240",
            "gender": "f",
            "party": {
                "acronym": "SMC",
                "is_coalition": true,
                "id": 1,
                "name": "PS Stranka modernega centra"
            },
            "type": "mp",
            "id": 3,
            "has_function": false
            },
            "score": {
            "vT1": -0.06505089721256502,
            "vT2": -0.1438729944923539
            }
        }]
    }
    """
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_=""
    try:
        compas = Compass.objects.filter(created_for__lte=date_of).order_by('-created_for')[0]
    except:
        raise Http404("Nismo našli kartice")
    data = compas.data
    for person in data:
        person.update({"person": getPersonData(person["person_id"], compas.created_for.strftime(API_DATE_FORMAT))})
        person.pop('person_id', None)

    return JsonResponse({"created_for": compas.created_for.strftime(API_DATE_FORMAT), 
                         "created_at": compas.created_at.strftime(API_DATE_FORMAT), 
                         "data": data}, 
                        safe=False)


def setMembershipsOfMember(request, person_id, date=None):
    if date:
        #call parladata api with date, maybe you will need to fix parladata api call
        data = tryHard(API_URL+'/getMembershipsOfMember/' + person_id + "/" + date).json()
        #date_of is date for created_for which is atribute of model (you also need to add created_for in model)
        date_of = datetime.strptime(date, API_DATE_FORMAT)
    else:
        data = tryHard(API_URL+'/getMembershipsOfMember/'+ person_id).json()
        date_of = datetime.now().date()

    person = Person.objects.get(id_parladata=int(person_id))

    memberships = saveOrAbortNew(MembershipsOfMember, created_for=date_of, person=person, data=data)

    return HttpResponse(memberships)


def getMembershipsOfMember(request, person_id, date=None): # TODO refactor keys into snake_case
    """
    * @api {get} /p/getMembershipsOfMember/{?date} MP's memberships
    * @apiName getMembershipsOfMember
    * @apiGroup MPs
    * @apiDescription This function returns an object with all the memberships the
      MP holds in various organizations. The function returns the memberships as
      they were calculated for a given date, if no date is supplied it is assumed
      the date is today.
    * @apiParam {Integer} id MP's Parladata id
    * @apiParam {date} date Optional date

    * @apiSuccess {Object} memberships MP's memberships categorised by organization type.
    
    * @apiSuccess {Object[]} memberships.kolegij MP's memberships in "kolegij"-type organizations.
    * @apiSuccess {String} memberships.kolegij.url Organization's url.
    * @apiSuccess {String} memberships.kolegij.org_type Organization type.
    * @apiSuccess {Integer} memberships.kolegij.org_id Organization's Parladata id.
    * @apiSuccess {String} memberships.kolegij.name The name of the organization.

    * @apiSuccess {Object[]} memberships.skupina_prijateljstva MP's memberships in "skupina prijateljstva"-type organizations.
    * @apiSuccess {String} memberships.skupina_prijateljstva.url Organization's url.
    * @apiSuccess {String} memberships.skupina_prijateljstva.org_type Organization type.
    * @apiSuccess {Integer} memberships.skupina_prijateljstva.org_id Organization's Parladata id.
    * @apiSuccess {String} memberships.skupina_prijateljstva.name The name of the organization.

    * @apiSuccess {Object[]} memberships.delegacija MP's memberships in "delegacija"-type organizations.
    * @apiSuccess {String} memberships.delegacija.url Organization's url.
    * @apiSuccess {String} memberships.delegacija.org_type Organization type.
    * @apiSuccess {Integer} memberships.delegacija.org_id Organization's Parladata id.
    * @apiSuccess {String} memberships.delegacija.name The name of the organization.

    * @apiSuccess {Object[]} memberships.komisija MP's memberships in "komisija"-type organizations.
    * @apiSuccess {String} memberships.komisija.url Organization's url.
    * @apiSuccess {String} memberships.komisija.org_type Organization type.
    * @apiSuccess {Integer} memberships.komisija.org_id Organization's Parladata id.
    * @apiSuccess {String} memberships.komisija.name The name of the organization.

    * @apiSuccess {Object[]} memberships.poslanska_skupina MP's memberships in "poslanska skupina"-type organizations.
    * @apiSuccess {String} memberships.poslanska_skupina.url Organization's url.
    * @apiSuccess {String} memberships.poslanska_skupina.org_type Organization type.
    * @apiSuccess {Integer} memberships.poslanska_skupina.org_id Organization's Parladata id.
    * @apiSuccess {String} memberships.poslanska_skupina.name The name of the organization.

    * @apiSuccess {Object[]} memberships.odbor MP's memberships in "odbor"-type organizations.
    * @apiSuccess {String} memberships.odbor.url Organization's url.
    * @apiSuccess {String} memberships.odbor.org_type Organization type.
    * @apiSuccess {Integer} memberships.odbor.org_id Organization's Parladata id.
    * @apiSuccess {String} memberships.odbor.name The name of the organization.

    * @apiSuccess {Object[]} memberships.preiskovalna_komisija MP's memberships in "preiskovalna komisija"-type organizations.
    * @apiSuccess {String} memberships.preiskovalna_komisija.url Organization's url.
    * @apiSuccess {String} memberships.preiskovalna_komisija.org_type Organization type.
    * @apiSuccess {Integer} memberships.preiskovalna_komisija.org_id Organization's Parladata id.
    * @apiSuccess {String} memberships.preiskovalna_komisija.name The name of the organization.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).

    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?
    

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getMembershipsOfMember/
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getMembershipsOfMember/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "created_at": "21.03.2017",
        "created_for": "17.02.2017",
        "data": [{
            "person": {
            "is_active": false,
            "district": [7],
            "name": "Anja Bah \u017dibert",
            "gov_id": "P239",
            "gender": "f",
            "party": {
                "acronym": "SDS",
                "is_coalition": false,
                "id": 5,
                "name": "PS Slovenska Demokratska Stranka"
            },
            "type": "mp",
            "id": 2,
            "has_function": false
            },
            "score": {
            "vT1": 0.18281964948320664,
            "vT2": -0.05594373814997616
            }
        }, {
            "person": {
            "is_active": false,
            "district": [8],
            "name": "Ur\u0161ka Ban",
            "gov_id": "P240",
            "gender": "f",
            "party": {
                "acronym": "SMC",
                "is_coalition": true,
                "id": 1,
                "name": "PS Stranka modernega centra"
            },
            "type": "mp",
            "id": 3,
            "has_function": false
            },
            "score": {
            "vT1": -0.06505089721256502,
            "vT2": -0.1438729944923539
            }
        }]
    }
    """
    card = getPersonCardModelNew(MembershipsOfMember, person_id, date)
    static = getPersonCardModelNew(MPStaticPL, person_id, date)

    out = {
        'person': getPersonData(person_id, date),
        'created_at': card.created_at.strftime(API_DATE_FORMAT),
        'created_for': card.created_for.strftime(API_DATE_FORMAT),
        'memberships': card.data
    }

    return JsonResponse(out, safe=False)


def getTaggedBallots(request, person_id, date_=None):
    """
    * @api {get} /p/getTaggedBallots/{id}/{?date} MP's tagged ballots
    * @apiName getTaggedBallots
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs
      ballots and their tags, ordered by date, grouped by day. The function
      returns the ballots until a given date, if no date is supplied it is
      assumed the date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object[]} results MP's tagged ballots grouped by date.
    * @apiSuccess {date} results.date The date in question.
    * @apiSuccess {Object[]} results.ballots Ballots the MP submitted on that day.
    * @apiSuccess {Integer} results.ballots.ballot_id Ballot's Parladata id.
    * @apiSuccess {String} results.ballots.option The ballot option ("za"/"proti"/"ni"/"kvorum").
    * @apiSuccess {String[]} results.ballots.tags List of tags this ballot was tagged with.
    * @apiSuccess {Integer} results.ballots.session_id Parladata id of the session where this ballot was submitted.
    * @apiSuccess {String} results.ballots.motion The text of the motion (what was the vote about).
    * @apiSuccess {Boolean} results.ballots.result Answers the question: Did the motion pass?
    * @apiSuccess {Integer} results.ballots.vote_id Parladata id of the vote this ballot belongs to.

    * @apiSuccess {String[]} all_tags List of all tags used for tagging ballots.
    

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getTaggedBallots/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getTaggedBallots/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "23. 11. 2016",
        "created_for": "4. 12. 2014",
        "results": [{
            "date": "4. 12. 2014",
            "ballots": [{
            "ballot_id": 592963,
            "option": "ni",
            "tags": ["Odbor za notranje zadeve, javno upravo in lokalno samoupravo"],
            "session_id": 5614,
            "motion": "Zakon o spremembah in dopolnitvah Zakona o dr\u017eavni upravi - Glasovanje o zakonu v celoti",
            "result": true,
            "vote_id": 6591
            }, {
            "ballot_id": 593053,
            "option": "ni",
            "tags": ["Odbor za notranje zadeve, javno upravo in lokalno samoupravo"],
            "session_id": 5614,
            "motion": "Zakon o spremembah in dopolnitvah Zakona o dr\u017eavni upravi - Amandma: K 19. \u010dlenu 4.12.2014 [ZL - Poslanska skupina Zdru\u017eena levica]",
            "result": false,
            "vote_id": 6592
            }]
        }, {
            "date": "17. 11. 2014",
            "ballots": [{
            "ballot_id": 564575,
            "option": "ni",
            "tags": ["Mandatno-volilna komisija"],
            "session_id": 6683,
            "motion": "Sklep o imenovanju \u010dlana Slovenske nacionalne komisije za UNESCO - Glasovanje",
            "result": true,
            "vote_id": 6274
            }, {
            "ballot_id": 564665,
            "option": "ni",
            "tags": ["Mandatno-volilna komisija"],
            "session_id": 6683,
            "motion": "Sklep o imenovanju predsednika in dveh \u010dlanov Upravnega odbora Sklada za financiranje razgradnje NEK in za odlaganje radioaktivnih odpadkov iz NEK - Glasovanje",
            "result": true,
            "vote_id": 6275
            }, {
            "ballot_id": 564755,
            "option": "ni",
            "tags": ["Mandatno-volilna komisija"],
            "session_id": 6683,
            "motion": "Sklep o imenovanju \u010dlanice Dr\u017eavne revizijske komisije - Glasovanje",
            "result": true,
            "vote_id": 6276
            }]
        }],
        "all_tags": ["Komisija za nadzor javnih financ", "Kolegij predsednika Dr\u017eavnega zbora", "Komisija za narodni skupnosti", "Komisija za odnose s Slovenci v zamejstvu in po svetu", "Komisija za poslovnik", "Mandatno-volilna komisija", "Odbor za delo, dru\u017eino, socialne zadeve in invalide", "Odbor za finance in monetarno politiko", "Odbor za gospodarstvo", "Odbor za infrastrukturo, okolje in prostor", "Odbor za izobra\u017eevanje, znanost, \u0161port in mladino", "Odbor za kmetijstvo, gozdarstvo in prehrano", "Odbor za kulturo", "Odbor za notranje zadeve, javno upravo in lokalno samoupravo", "Odbor za obrambo", "Odbor za pravosodje", "Odbor za zadeve Evropske unije", "Odbor za zdravstvo", "Odbor za zunanjo politiko", "Preiskovalna komisija o ugotavljanju zlorab v slovenskem ban\u010dnem sistemu ter ugotavljanju vzrokov in", "Preiskovalna komisija za ugotavljanje politi\u010dne odgovornosti nosilcev javnih funkcij pri investiciji", "Ustavna komisija", "Proceduralna glasovanja", "Zunanja imenovanja", "Poslanska vpra\u0161anja", "Komisija za nadzor obve\u0161\u010devalnih in varnostnih slu\u017eb", "Preiskovalne komisije", "Komisija za peticije ter za \u010dlovekove pravice in enake mo\u017enosti", "Interpelacija", " Preiskovalna komisija za ugotavljanje politi\u010dne odgovornosti nosilcev javnih funkcij pri investicij"]
    }
    """
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT)
    else:
        date_of = datetime.now().date()
    out = []
    ballots = Ballot.objects.filter(person__id_parladata=person_id,
                                    start_time__lte=date_of)
    if ballots:
        created_at = ballots.latest('created_at').created_at
    else:
        created_at = datetime.now()
    b_list = [[ballot for ballot in ballots.filter(start_time__range=[t_date,
                                                                      t_date+timedelta(days=1)])]
              for t_date in ballots.order_by('start_time').datetimes('start_time',
                                                                     'day')]

    lastDay = None
    for day in b_list:
        dayData = {'date': day[0].start_time.strftime(API_OUT_DATE_FORMAT),
                   'ballots': []}
        lastDay = day[0].start_time.strftime(API_OUT_DATE_FORMAT)
        for ballot in day:
            dayData['ballots'].append({
                'motion': ballot.vote.motion,
                'vote_id': ballot.vote.id_parladata,
                'result': ballot.vote.result,
                'ballot_id': ballot.id_parladata,
                'session_id': ballot.vote.session.id_parladata if ballot.vote.session else None,
                'option': ballot.option,
                'tags': ballot.vote.tags})
        out.append(dayData)

    tags = list(Tag.objects.all().values_list('name', flat=True))
    result = {
        'person': getPersonData(person_id, date_),
        'all_tags': tags,
        'created_at': created_at.strftime(API_OUT_DATE_FORMAT),
        'created_for': lastDay if lastDay else created_at.strftime(API_OUT_DATE_FORMAT),
        'results': list(reversed(out))
        }
    return JsonResponse(result, safe=False)


def setNumberOfQuestionsAll(request, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT)
    else:
        date_of = datetime.now().date()

    url = API_URL + '/getAllQuestions/' + date_of.strftime(API_DATE_FORMAT)
    data = tryHard(url).json()
    mps = tryHard(API_URL+'/getMPs/'+date_of.strftime(API_DATE_FORMAT)).json()
    mps_ids = [mp['id'] for mp in mps]
    authors = []
    for question in data:
        if question['author_id'] in mps_ids:
            authors.append(question['author_id'])

    avg = len(authors)/float(len(mps_ids))
    question_count = Counter(authors)
    max_value = 0
    max_persons = []
    for maxi in question_count.most_common(90):
        if max_value == 0:
            max_value = maxi[1]
        if maxi[1] == max_value:
            max_persons.append(maxi[0])
        else:
            break

    for person_id in mps_ids:
        person = Person.objects.get(id_parladata=person_id)
        saveOrAbortNew(model=NumberOfQuestions,
                       created_for=date_of,
                       person=person,
                       score=question_count[person_id],
                       average=avg,
                       maximum=max_value,
                       maxMPs=max_persons)

    return HttpResponse('All iz well')


def getNumberOfQuestions(request, person_id, date_=None):
    """
    * @api {get} /p/getNumberOfQuestions/{id}/{?date} MP's number of questions
    * @apiName getNumberOfQuestions
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs
      calculated number of questions (like PM's questions in the UK). The function
      returns the score as it was calculated for a given date, if no date is
      supplied the date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object} results MP's number of questions.
    * @apiSuccess {Object} results.max MP (or MPs) who has the highest number of questions and their score.
    * @apiSuccess {Integer} results.max.score Max MP's score.
    * @apiSuccess {Object[]} results.max.mps A list of MP's with the same maximum score.
    * @apiSuccess {Boolean} results.max.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} results.max.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} results.max.mps.name MP's full name.
    * @apiSuccess {String} results.max.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} results.max.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} results.max.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} results.max.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} results.max.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} results.max.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} results.max.mps.party.name The party's name.
    * @apiSuccess {String} results.max.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Boolean} results.max.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Float} results.average The average score for this metric accross the parliament.
    * @apiSuccess {Integer} results.score Score for the MP in question.

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getNumberOfQuestions/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getNumberOfQuestions/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "21.03.2017",
        "created_for": "20.03.2017",
        "results": {
            "max": {
            "score": 672449,
            "mps": [{
                "is_active": false,
                "district": [17],
                "name": "Jo\u017eef Horvat",
                "gov_id": "P020",
                "gender": "m",
                "party": {
                "acronym": "NSI",
                "is_coalition": false,
                "id": 6,
                "name": "PS Nova Slovenija"
                },
                "type": "mp",
                "id": 32,
                "has_function": false
            }]
            },
            "average": 177115,
            "score": 381389
        }
    }
    """
    card = getPersonCardModelNew(NumberOfQuestions,
                                 person_id,
                                 date_)
    card_date = card.created_for.strftime(API_DATE_FORMAT)

    out = {
        'person': getPersonData(person_id, card_date),
        'created_at': card.created_at.strftime(API_DATE_FORMAT),
        'created_for': card_date,
        'results': {
            'max': {
                'score': card.maximum,
                'mps': [getPersonData(max_p, card_date)
                        for max_p in card.maxMPs]
            },
            'average': card.average,
            'score': card.score
        }
    }

    return JsonResponse(out, safe=False)


def getQuestions(request, person_id, date_=None):
    """
    * @api {get} /p/getQuestions/{id}/{?date} MP's questions
    * @apiName getQuestions
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs
      questions, ordered by date, grouped by day. The function
      returns the ballots until a given date, if no date is supplied it is
      assumed the date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object[]} results MP's questions grouped by date.
    * @apiSuccess {date} results.date The date in question.
    * @apiSuccess {Object[]} results.questions Questions the MP submitted on that day.
    * @apiSuccess {String} results.questions.recipient_text Recipient in text form as written on www.dz-rs.si.
    * @apiSuccess {String} results.questions.url URL to the relevant question document.
    * @apiSuccess {String} results.questions.title Question title.
    * @apiSuccess {Integer} results.questions.id Parladata id of the question.
    * @apiSuccess {Integer} results.questions.session_id Parladata id of the session where this question was asked.
    * @apiSuccess {Integer} results.questions.session_name Name of the session where this question was asked.
    
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getQuestions/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getQuestions/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "11. 1. 2017",
        "created_for": "12. 12. 2014",
        "results": [{
            "date": "12. 12. 2014",
            "questions": [{
            "recipient_text": "minister za gospodarski razvoj in tehnologijo, ministrica za okolje in prostor",
            "title": "v zvezi s problematiko Cinkarne Celje in z njo povezanim okoljskim stanjem v Celju",
            "url": "http://imss.dz-rs.si/IMiS/ImisAdmin.nsf/ImisnetAgent?OpenAgent&2&DZ-MSS-01/ca20e0052d5fcd92e4bdfad7c16c7458916c91f48725827616fb01493db37336",
            "session_id": "Unknown",
            "session_name": "Unknown",
            "id": 5401
            }]
        }, {
            "date": "14. 11. 2014",
            "questions": [{
            "recipient_text": "predsednik Vlade",
            "title": "v zvezi s pripravami na privatizacijo DARS-a in strategijo upravljanja z dr\u017eavnim premo\u017eenjem",
            "url": "http://imss.dz-rs.si/IMiS/ImisAdmin.nsf/ImisnetAgent?OpenAgent&2&DZ-MSS-01/ca20e00560147f954c0d998b6c8f4da8aacddff0adf58593742b0fa62dc39b11",
            "session_id": "Unknown",
            "session_name": "Unknown",
            "id": 5232
            }, {
            "recipient_text": "minister za infrastrukturo",
            "title": "v zvezi z ohranitvijo delovnih mest v Zasavju",
            "url": "http://imss.dz-rs.si/IMiS/ImisAdmin.nsf/ImisnetAgent?OpenAgent&2&DZ-MSS-01/ca20e00544d15404319afbf78aa095c9c6cc3d29459887062737389aab9c7829",
            "session_id": "Unknown",
            "session_name": "Unknown",
            "id": 5234
            }]
        }, {
            "date": "29. 10. 2014",
            "questions": [{
            "recipient_text": "minister za finance v funkciji ministra za gospodarski razvoj in tehnologijo",
            "title": "z zvezi z vrnitvijo glasovalnih pravic RS in povezanih dru\u017eb v dru\u017ebah Telekom d.d. in Zavarovalnico Triglav d.d.",
            "url": "http://imss.dz-rs.si/IMiS/ImisAdmin.nsf/ImisnetAgent?OpenAgent&2&DZ-MSS-01/ca20e0052e4c3e7a939ddd5a2c137009af60900edcdabf8632dd7d796f2f8bcd",
            "session_id": 5615,
            "session_name": "6. izredna seja",
            "id": 5109
            }]
        }]
    }
    """

    if date_:
        fdate = datetime.strptime(date_, '%d.%m.%Y')
        questions = Question.objects.filter(person__id_parladata=person_id)
        questions = [[question
                      for question
                      in questions.filter(start_time__range=[t_date, t_date+timedelta(days=1)])]
                     for t_date
                     in questions.filter(start_time__lte=fdate).order_by('start_time').datetimes('start_time', 'day')]
    else:
        fdate = datetime.now()
        questions = Question.objects.filter(person__id_parladata=person_id)
        questions = [[question
                      for question
                      in questions.filter(start_time__range=[t_date, t_date+timedelta(days=1)])
                      ]
                     for t_date
                     in questions.order_by('start_time').datetimes('start_time', 'day')]
    out = []
    lastDay = None
    created_at = []
    for day in questions:
        dayData = {'date': day[0].start_time.strftime(API_OUT_DATE_FORMAT),
                   'questions':[]}
        lastDay = day[0].start_time.strftime(API_OUT_DATE_FORMAT)
        for question in day:
            created_at.append(question.created_at)
            persons = []
            orgs = []
            for person in question.recipient_persons.all():
                persons.append(getMinistryData(person.id_parladata, question.start_time.strftime(API_DATE_FORMAT)))
            for org in question.recipient_organizations.all():
                orgs.append(org.getOrganizationData())
            dayData['questions'].append({
                'session_name': question.session.name if question.session else 'Unknown',
                'id': question.id_parladata,
                'title': question.title,
                'recipient_text': question.recipient_text,
                'recipient_persons': persons,
                'recipient_orgs': orgs,
                'url': question.content_link,
                'session_id': question.session.id_parladata if question.session else 'Unknown'})
        out.append(dayData)

    result = {
        'person': getPersonData(person_id, date_),
        'created_at': max(created_at).strftime(API_OUT_DATE_FORMAT) if created_at else datetime.today().strftime('API_DATE_FORMAT'),
        'created_for': lastDay if lastDay else datetime.today().strftime('API_DATE_FORMAT'),
        'results': list(reversed(out))
        }
    return JsonResponse(result, safe=False)


def getListOfMembers(request, date_=None, force_render=False):
    """
    * @api {get} /p/getListOfMembers/{?date} List of MPs and their scores
    * @apiName getListOfMembers
    * @apiGroup Other
    * @apiDescription This function returns an object with all MPs and their
      scores for all analyses along with an object containing all districts
      (for filtering purposes https://parlameter.si/poslanci).
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object[]} districts List of objects representing districts.
    * @apiSuccess {String} districts.DISTRICT_ID Each object contains a single key,
      that key being the district's Parladata id and its value the district's name.
    * @apiSuccess {Object[]} data List of MPs and their scores.
    * @apiSuccess {Object} data.person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} data.person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} data.person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} data.person.name MP's full name.
    * @apiSuccess {String} data.person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} data.person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} data.person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} data.person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} data.person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} data.person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} data.person.party.name The party's name.
    * @apiSuccess {String} data.person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} data.person.id The person's Parladata id.
    * @apiSuccess {Boolean} data.person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Object} data.results Analysis results for this person.
    * @apiSuccess {Float} data.results.privzdignjeno "Elevated" language style score.
    * @apiSuccess {Float} data.speeches_per_session Average number of speeches per session.
    * @apiSuccess {Integer} data.number_of_questions Number of questions this MP has asked.
    * @apiSuccess {Float} data.presence_votes Percentage of votes this MP attended.
    * @apiSuccess {Float} data.presence_sessions Percentage of sessions this MP attended.
    * @apiSuccess {Float} data.problematicno "Problematic" language style score.
    * @apiSuccess {Float}  data.vocabulary_size MP's calculated vocabulary size.
    * @apiSuccess {Integer} data.spoken_words Number of words this MP has spoken.
    * @apiSUccess {Float} data.preprosto "Simple" language style score.
    
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getListOfMembers
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getListOfMembers/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "districts": [{
            "91": "Lendava 1"
        }, {
            "102": "Ljubljana-\u0160i\u0161ka I"
        }, {
            "101": "Ljubljana-\u0160i\u0161ka II"
        }, {
            "100": "Ljubljana-\u0160i\u0161ka III"
        }],
        "data": [{
            "person": {
            "name": "Aleksander Kav\u010di\u010d",
            "gov_id": "P259",
            "gender": "m",
            "is_active": false,
            "district": [19],
            "party": {
                "acronym": "SMC",
                "is_coalition": true,
                "name": "PS Stranka modernega centra",
                "id": 1
            },
            "type": "mp",
            "id": 39,
            "has_function": false
            },
            "results": {
            "privzdignjeno": 2.7438091511157987,
            "speeches_per_session": 1.0,
            "number_of_questions": 5.0,
            "presence_votes": 89.589905362776,
            "presence_sessions": 89.8550724637681,
            "problematicno": 2.516673651070962,
            "vocabulary_size": 135.0,
            "spoken_words": 10837,
            "preprosto": 3.377309423797745
            }
        }, {
            "person": {
            "name": "Alenka Bratu\u0161ek",
            "gov_id": "P166",
            "gender": "f",
            "is_active": false,
            "district": [62],
            "party": {
                "acronym": "PS NP",
                "is_coalition": false,
                "name": "PS nepovezanih poslancev ",
                "id": 109
            },
            "type": "mp",
            "id": 9,
            "has_function": false
            },
            "results": {
            "privzdignjeno": 0.32064092814348816,
            "speeches_per_session": 5.0,
            "number_of_questions": 49.0,
            "presence_votes": 46.6876971608833,
            "presence_sessions": 72.463768115942,
            "problematicno": 0.31498556069390254,
            "vocabulary_size": 96.0,
            "spoken_words": 282204,
            "preprosto": 0.411863764711025
            }
        }, {
            "person": {
            "name": "Andrej \u010cu\u0161",
            "gov_id": "P225",
            "gender": "m",
            "is_active": false,
            "district": [28],
            "party": {
                "acronym": "NeP - A\u010c",
                "is_coalition": false,
                "name": "Nepovezani poslanec Andrej \u010cu\u0161",
                "id": 108
            },
            "type": "mp",
            "id": 15,
            "has_function": false
            },
            "results": {
            "privzdignjeno": 0.6844781070961635,
            "speeches_per_session": 3.0,
            "number_of_questions": 284.0,
            "presence_votes": 52.944269190326,
            "presence_sessions": 69.5652173913043,
            "problematicno": 0.5026381764433223,
            "vocabulary_size": 115.0,
            "spoken_words": 122238,
            "preprosto": 0.8868782609371512
            }
        }]
    }
    """
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
        key = date_
    else:
        date_of = datetime.now().date()
        date_=date_of.strftime(API_DATE_FORMAT)
        key = date_

    c_data = cache.get("mp_list_" + key)
    if c_data and not force_render:
        data = c_data
    else:
        mps = tryHard(API_URL+'/getMPs/'+date_).json()
        data = []
        for mp in mps: 
            person_obj = {}
            person_obj["results"] = {}
            person_id = mp["id"]
            person_obj["person"] = getPersonData(person_id, date_)
            try:
                person_obj["results"]["presence_sessions"] = getPersonCardModelNew(Presence, person_id, date_).person_value_sessions
            except:
                person_obj["results"]["presence_sessions"] = None
            try:
                person_obj["results"]["presence_votes"] = getPersonCardModelNew(Presence, person_id, date_).person_value_votes
            except:
                person_obj["results"]["presence_votes"] = None
            try:
                person_obj["results"]["vocabulary_size"] = getPersonCardModelNew(VocabularySize, person_id, date_).score
            except:
                person_obj["results"]["vocabulary_size"] = None
            try:
                person_obj["results"]["spoken_words"] = getPersonCardModelNew(SpokenWords, person_id, date_).score
            except:
                person_obj["results"]["spoken_words"] = None
            try:
                person_obj["results"]["speeches_per_session"] = getPersonCardModelNew(AverageNumberOfSpeechesPerSession, person_id, date_).score
            except:
                person_obj["results"]["speeches_per_session"] = None
            try:
                person_obj["results"]["number_of_questions"] = getPersonCardModelNew(NumberOfQuestions, person_id, date_).score
            except:
                person_obj["results"]["number_of_questions"] = None
            try:
                styleScores = getPersonCardModelNew(StyleScores, int(person_id), date_)
            except:
                styleScores = None
            
            privzdignjeno = 0
            problematicno = 0
            preprosto = 0

            if styleScores.privzdignjeno != 0 and styleScores.privzdignjeno_average != 0:
                privzdignjeno = styleScores.privzdignjeno/styleScores.privzdignjeno_average
            
            if styleScores.problematicno != 0 and styleScores.problematicno_average != 0:
                problematicno = styleScores.problematicno/styleScores.problematicno_average
            
            if styleScores.preprosto != 0 and styleScores.preprosto_average != 0:
                preprosto = styleScores.preprosto/styleScores.preprosto_average
            
            person_obj["results"]["privzdignjeno"] = privzdignjeno
            person_obj["results"]["preprosto"] = preprosto
            person_obj["results"]["problematicno"] = problematicno

            data.append(person_obj)
        data = sorted(data, key=lambda k: k['person']["name"])
        data = {"districts": [{dist.id_parladata : dist.name} for dist in District.objects.all()], "data": data}
        cache.set("mp_list_" + key, data, 60 * 60 * 48)    

    return JsonResponse(data)


def getAllActiveMembers(request):
    """
    * @api {get} /p/getAllActiveMembers Get all active MPs
    * @apiName getAllActiveMembers
    * @apiGroup Other
    * @apiDescription This function returns a list of all MPs currently
      active in the parliament.

    * @apiSuccess {Object[]} / list of MPs

    * @apiSuccess {Boolean} /.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} /.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} /.name MP's full name.
    * @apiSuccess {String} /.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} /.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} /.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} /.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} /.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} /.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} /.party.name The party's name.
    * @apiSuccess {String} /.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} /.id The person's Parladata id.
    * @apiSuccess {Boolean} /.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getAllActiveMembers/

    * @apiSuccessExample {json} Example response:
    [{
        "is_active": false,
        "district": [48],
        "name": "Jasna Murgel",
        "gov_id": "P274",
        "gender": "f",
        "party": {
            "acronym": "SMC",
            "is_coalition": true,
            "id": 1,
            "name": "PS Stranka modernega centra"
        },
        "type": "mp",
        "id": 60,
        "has_function": false
        }, {
        "is_active": false,
        "district": [40],
        "name": "Ivan \u0160kodnik",
        "gov_id": "P286",
        "gender": "m",
        "party": {
            "acronym": "SMC",
            "is_coalition": true,
            "id": 1,
            "name": "PS Stranka modernega centra"
        },
        "type": "mp",
        "id": 76,
        "has_function": false
        }, {
        "is_active": false,
        "district": [46],
        "name": "Branislav Raji\u0107",
        "gov_id": "P281",
        "gender": "m",
        "party": {
            "acronym": "SMC",
            "is_coalition": true,
            "id": 1,
            "name": "PS Stranka modernega centra"
        },
        "type": "mp",
        "id": 70,
        "has_function": false
    }]
    """
    return JsonResponse([getPersonData(person.id_parladata) for person in Person.objects.filter(actived="Yes")], safe=False)


def getSlugs(request):
    """
    * @api {get} /p/getSlugs Get slugs for parlameter.si
    * @apiName getAllActiveMembers
    * @apiGroup Other
    * @apiDescription This function returns slugs for our site at parlameter.si

    * @apiSuccess {Object} partyLink Party url paths.
    * @apiSuccess {String} partyLink.govori Party speeches url.
    * @apiSuccess {String} partyLink.base Party pages base url.
    * @apiSuccess {String} partyLink.pregled Party overview url.
    * @apiSuccess {String} partyLink.glasovanja Party votes url.

    * @apiSuccess {Object} personLink Person url paths.
    * @apiSuccess {String} personLink.govori Person speeches url.
    * @apiSuccess {String} personLink.base Person pages base url.
    * @apiSuccess {String} personLink.pregled Person overview url.
    * @apiSuccess {String} personLink.glasovanja Person votes url.

    * @apiSuccess {Object} sessionLink Session url paths.
    * @apiSuccess {String} sessionLink.prisotnos Session attendance url.
    * @apiSuccess {String} sessionLink.glasovanje Session vote url.
    * @apiSuccess {String} sessionLink.transkript Session transcript url.
    * @apiSuccess {String} sessionLink.glasovanja Session votes url.

    * @apiSuccess {Object} person Slugs for people. Keys are Parladata ids.
    * @apiSuccess {Object} person.PERSON_ID Person's slugs object.
    * @apiSuccess {String} person.PERSON_ID.slug Person's url slug.

    * @apiSuccess {String} base Url base.

    * @apiSuccess {Object} party Slugs for organizations. Keys are Parladata ids.
    * @apiSuccess {Object} party.PARTY_ID Party's slug object.
    * @apiSuccess {String} party.PARTY_ID.acronym Party's acronym.
    * @apiSuccess {String} party.PARTY_ID.realAcronym Party's acronym with proper capitalisation.
    * @apiSuccess {String} party.PARTY_ID.slug Party's slug
    
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getSlugs/

    * @apiSuccessExample {json} Example response:
    {
        "partyLink": {
            "govori": "/govori/",
            "base": "/poslanska-skupina/",
            "pregled": "/pregled/",
            "glasovanja": "/glasovanja/"
        },
        "personLink": {
            "govori": "/govori/",
            "base": "/poslanec/",
            "pregled": "/pregled/",
            "glasovanja": "/glasovanja/"
        },
        "sessionLink": {
            "prisotnost": "/seja/prisotnost/",
            "glasovanje": "/seja/glasovanje/",
            "transkript": "/seja/transkript/",
            "glasovanja": "/seja/glasovanja/"
        },
        "person": {
            "2": {
            "slug": "anja-bah-zibert"
            },
            "3": {
            "slug": "urska-ban"
            },
            "4": {
            "slug": "roberto-battelli"
            }
        },
        "base": "https://parlameter.si",
        "party": {
            "1": {
            "acronym": "smc",
            "realAcronym": "SMC",
            "slug": "ps-stranka-modernega-centra"
            },
            "2": {
            "acronym": "imns",
            "realAcronym": "IMNS",
            "slug": "ps-italijanske-in-madzarske-narodne-skupnosti"
            },
            "3": {
            "acronym": "desus",
            "realAcronym": "DeSUS",
            "slug": "ps-demokratska-stranka-upokojencev-slovenije"
            },
            "4": {
            "acronym": "zaab",
            "realAcronym": "ZAAB",
            "slug": "ps-zaveznistvo-alenke-bratusek"
            }
        }
    }
    """
    obj = {"person": {person.id_parladata: {"slug": slugify(person.name)}
                      for person
                      in Person.objects.all().exclude(pg__isnull=True)},
            "personLink": {
                    "base": "/poslanec/",
                    "govori": "/govori/",
                    "glasovanja": "/glasovanja/",
                    "pregled": "/pregled/"
                },
            "party": {org.id_parladata: {"slug": slugify(org.name),
                                         "acronym": slugify(org.acronym),
                                         "realAcronym": org.acronym}
                      for org
                      in Organization.objects.all()},
            "partyLink": {
                    "base": "/poslanska-skupina/",
                    "govori": "/govori/",
                    "glasovanja": "/glasovanja/",
                    "pregled": "/pregled/"
                },

            "sessionLink": {
                    "glasovanje": "/seja/glasovanje/",
                    "glasovanja": "/seja/glasovanja/",
                    "prisotnost": "/seja/prisotnost/",
                    "transkript": "/seja/transkript/"
                },
            "base": "https://parlameter.si"
            }
    return JsonResponse(obj)


@csrf_exempt
def setAllMPsTFIDFsFromSearch(request):
    """
    API endpoint for saveing TFIDF. TFIDF is generated in parlasearch and sent
    with a POST request.

    """
    if request.method == 'POST':
        print request.body
        print type(request.body)
        post_data = json.loads(request.body)
        print type(post_data)
        if post_data:
            print post_data
            save_statuses = []
            date_of = datetime.today()
            person = Person.objects.get(id_parladata=post_data['person']['id'])
            save_statuses.append(saveOrAbortNew(Tfidf,
                                                person=person,
                                                created_for=date_of,
                                                is_visible=False,
                                                data=post_data['results']))

            return JsonResponse({'status': 'alliswell',
                                 'saved': save_statuses})
        else:
            return JsonResponse({'status': 'There is not data'})
    else:
        return JsonResponse({'status': 'It wasnt POST'})


@csrf_exempt
def setAllMPsStyleScoresFromSearch(request):
    """
    API endpoint for saveing StyleScores. StyleScores is generated in parlasearch and sent
    with a POST request.
    """
    if request.method == 'POST':
        post_data = json.loads(request.body)
        date_of = datetime.today()
        print post_data
        if post_data:
            save_statuses = []
            for score in post_data:
                print score
                status = saveOrAbortNew(StyleScores,
                                        person=Person.objects.get(id_parladata=int(score["member"])),
                                        created_for=date_of,
                                        problematicno=float(score['problematicno']),
                                        privzdignjeno=float(score['privzdignjeno']),
                                        preprosto=float(score['preprosto']),
                                        problematicno_average=float(score['problematicno_average']),
                                        privzdignjeno_average=float(score['privzdignjeno_average']),
                                        preprosto_average=float(score['preprosto_average'])
                                        )
                save_statuses.append(status)
            return JsonResponse({"status": "alliswell", "saved": save_statuses})
        else:
            return JsonResponse({"status": "There's not data"})
    else:
        return JsonResponse({"status": "It wasnt POST"})


def setPresenceThroughTime(request, person_id, date_=None):
    if date_:
        fdate = datetime.strptime(date_, '%d.%m.%Y').date()
    else:
        fdate = datetime.now().date()

    url = API_URL + '/getBallotsCounterOfPerson/' + person_id + '/' + fdate.strftime(API_DATE_FORMAT)
    data = tryHard(url).json()

    data_for_save = []

    for month in data:
        stats = month['ni'] + month['za'] + month['proti'] + month['kvorum']
        not_member = month['total'] - stats
        not_member = float(not_member) / month['total'] if not_member else 0
        presence = float(stats-month['ni']) / month['total'] if stats else 0
        data_for_save.append({'date_ts': month['date_ts'],
                              'presence': presence * 100,
                              'not_member': not_member * 100,
                              'vote_count': month['total']})

    saved = saveOrAbortNew(model=PresenceThroughTime,
                           person=Person.objects.get(id_parladata=person_id),
                           created_for=fdate,
                           data=data_for_save)

    return JsonResponse({'alliswell': True, "status": 'OK', "saved": saved})


def getPresenceThroughTime(request, person_id, date_=None):
    """
    * @api {get} /p/getPresenceThroughTime/{id}/{?date} MP's presence through time
    * @apiName getPresenceThroughTime
    * @apiGroup MPs
    * @apiDescription This function returns an object with the MPs
      calculated presence at votes through time. The function
      returns the score as it was calculated for a given date, if no date is
      supplied the date is today.
    * @apiParam {Integer} id MP's Parladata id.
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object} person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} person.name MP's full name.
    * @apiSuccess {String} person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} person.party.name The party's name.
    * @apiSuccess {String} person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} person.id The person's Parladata id.
    * @apiSuccess {Boolean} person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for What historic date does this data correspond with?

    * @apiSuccess {Object[]} results List of objects for MP's presence for every month since the beginning of the current Parliament's term.
    * @apiSuccess {Integer} results.vote_count Total number of votes that happened this month.
    * @apiSuccess {date} results.date_ts UTF-8 formatted date - first of the month.
    * @apiSuccess {Integer} results.not_member Percentage of votes where this person was not yet a MP.
    * @apiSuccess {Float} results.presence Percentage of votes this person attended.

    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getPresenceThroughTime/12
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getPresenceThroughTime/12/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "person": {
            "is_active": false,
            "district": [15],
            "name": "Luka Mesec",
            "gov_id": "P273",
            "gender": "m",
            "party": {
            "acronym": "ZL",
            "is_coalition": false,
            "id": 8,
            "name": "PS Zdru\u017eena Levica"
            },
            "type": "mp",
            "id": 58,
            "has_function": false
        },
        "created_at": "28.02.2017",
        "created_for": "28.02.2017",
        "results": [{
            "vote_count": 17,
            "date_ts": "2014-08-01T00:00:00",
            "not_member": 0,
            "presence": 70.58823529411765
        }, {
            "vote_count": 15,
            "date_ts": "2014-09-01T00:00:00",
            "not_member": 0,
            "presence": 60.0
        }, {
            "vote_count": 4,
            "date_ts": "2014-10-01T00:00:00",
            "not_member": 0,
            "presence": 100.0
        }, {
            "vote_count": 58,
            "date_ts": "2014-11-01T00:00:00",
            "not_member": 0,
            "presence": 70.6896551724138
        }, {
            "vote_count": 61,
            "date_ts": "2014-12-01T00:00:00",
            "not_member": 0,
            "presence": 27.86885245901639
        }]
    }
    """
    card = getPersonCardModelNew(PresenceThroughTime,
                                 person_id,
                                 date_)
    card_date = card.created_for.strftime(API_DATE_FORMAT)

    out = {
        'person': getPersonData(person_id, card_date),
        'created_at': card.created_at.strftime(API_DATE_FORMAT),
        'created_for': card_date,
        'results': card.data
    }

    return JsonResponse(out, safe=False)


def setListOfMembersTickers(request, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_ = date_of.strftime(API_DATE_FORMAT)

    mps = tryHard(API_URL+'/getMPs/'+date_).json()

    prevCard = getListOfMembersTickers(request, (date_of-timedelta(days=1)).strftime(API_DATE_FORMAT)).content
    prevData = json.loads(prevCard)['data']

    rank_data = {'presence_sessions': [],
                 'presence_votes': [],
                 'vocabulary_size': [],
                 'spoken_words': [],
                 'speeches_per_session': [],
                 'number_of_questions': [],
                 'privzdignjeno': [],
                 'preprosto': [],
                 'problematicno': [],
                 }

    data = []
    for mp in mps:
        person_obj = {}
        person_obj['results'] = {}
        person_id = mp['id']
        person_obj['person'] = getPersonData(person_id, date_)

        try:
            value = getPersonCardModelNew(Presence,
                                          person_id,
                                          date_).person_value_sessions
        except:
            value = 0
        person_obj['results']['presence_sessions'] = {}
        person_obj['results']['presence_sessions']['score'] = value
        rank_data['presence_sessions'].append(value)

        try:
            value = getPersonCardModelNew(Presence,
                                          person_id,
                                          date_).person_value_votes
        except:
            value = 0
        person_obj['results']['presence_votes'] = {}
        person_obj['results']['presence_votes']['score'] = value
        rank_data['presence_votes'].append(value)

        try:
            value = getPersonCardModelNew(VocabularySize,
                                          person_id,
                                          date_).score
        except:
            value = 0
        person_obj['results']['vocabulary_size'] = {}
        person_obj['results']['vocabulary_size']['score'] = value
        rank_data['vocabulary_size'].append(value)

        try:
            value = getPersonCardModelNew(SpokenWords,
                                          person_id,
                                          date_).score
        except:
            value = 0
        person_obj['results']['spoken_words'] = {}
        person_obj['results']['spoken_words']['score'] = value
        rank_data['spoken_words'].append(value)

        try:
            value = getPersonCardModelNew(AverageNumberOfSpeechesPerSession,
                                          person_id,
                                          date_).score
        except:
            value = 0
        person_obj['results']['speeches_per_session'] = {}
        person_obj['results']['speeches_per_session']['score'] = value
        rank_data['speeches_per_session'].append(value)

        try:
            value = getPersonCardModelNew(NumberOfQuestions,
                                          person_id,
                                          date_).score
        except:
            value = 0
        person_obj['results']['number_of_questions'] = {}
        person_obj['results']['number_of_questions']['score'] = value
        rank_data['number_of_questions'].append(value)

        try:
            styleScores = getPersonCardModelNew(StyleScores,
                                                int(person_id),
                                                date_)
        except:
            styleScores = None

        privzdignjeno = 0
        problematicno = 0
        preprosto = 0
        try:
            if (styleScores.privzdignjeno != 0 and
               styleScores.privzdignjeno_average != 0):
                privzdignjeno = styleScores.privzdignjeno / styleScores.privzdignjeno_average

            if (styleScores.problematicno != 0 and
               styleScores.problematicno_average != 0):
                problematicno = styleScores.problematicno / styleScores.problematicno_average

            if (styleScores.preprosto != 0 and
               styleScores.preprosto_average != 0):
                preprosto = styleScores.preprosto / styleScores.preprosto_average
        except:
            preprosto = 0
            privzdignjeno = 0
            problematicno = 0

        person_obj['results']['privzdignjeno'] = {}
        person_obj['results']['privzdignjeno']['score'] = privzdignjeno
        rank_data['privzdignjeno'].append(value)

        person_obj['results']['preprosto'] = {}
        person_obj['results']['preprosto']['score'] = preprosto
        rank_data['preprosto'].append(value)

        person_obj['results']['problematicno'] = {}
        person_obj['results']['problematicno']['score'] = problematicno
        rank_data['problematicno'].append(value)

        data.append(person_obj)

    ranking = {}
    for key in rank_data.keys():
        ranks = rank_data[key]
        inverse = len(ranks) + 1
        ranking[key] = inverse - rankdata(ranks, method='max').astype(int)

    print ranking

    # set rankings to persons data
    for idx, cPerson in enumerate(data):
        # get persons data in previous list
        is_prev = True
        if prevData:
            prevPerson = prevData[idx]
            if prevPerson['person']['id'] == cPerson['person']['id']:
                pass
            else:
                # if person isn't in the same place in the list
                prevPerson = None
                for person in prevData:
                    if person['person']['id'] == cPerson['person']['id']:
                        prevPerson = person
                        continue
                # if person isn't member in the previous list
                if not prevPerson:
                    is_prev = False
        else:
            is_prev = False
        for key in rank_data.keys():
            cPerson['results'][key]['rank'] = ranking[key][idx]
            if is_prev:
                prevSocre = prevPerson['results'][key]['score']
                currentScore = cPerson['results'][key]['score']
                diff = currentScore - prevSocre
                cPerson['results'][key]['diff'] = diff
            else:
                cPerson['results'][key]['diff'] = 0

    data = sorted(data, key=lambda k: k['person']['name'])

    MembersList(created_for=date_of,
                data=data).save()
    return JsonResponse(data, safe=False)


def getListOfMembersTickers(request, date_=None):
    """
    * @api {get} /p/getListOfMembersTickers/{?date} List of MPs and their scores with differences from last regular plenary session
    * @apiName getListOfMembersTickers
    * @apiGroup Other
    * @apiDescription This function returns an object with all MPs and their
      scores for all analyses along with an object containing all districts
      (for filtering purposes https://parlameter.si/poslanci). The score objects
      contain scores, MP's ranks as well as the difference in their scores between
      the last two regular plenary session (Redna seja).
    * @apiParam {date} date Optional date.

    * @apiSuccess {Object[]} districts List of objects representing districts.
    * @apiSuccess {String} districts.DISTRICT_ID Each object contains a single key,
      that key being the district's Parladata id and its value the district's name.
    * @apiSuccess {Object[]} data List of MPs and their scores.
    * @apiSuccess {Object} data.person MP's person object (comes with most calls).
    * @apiSuccess {Boolean} data.person.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} data.person.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} data.person.name MP's full name.
    * @apiSuccess {String} data.person.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} data.person.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} data.person.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} data.person.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} data.person.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} data.person.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} data.person.party.name The party's name.
    * @apiSuccess {String} data.person.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} data.person.id The person's Parladata id.
    * @apiSuccess {Boolean} data.person.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Object} data.results Analysis results for this person.
    
    * @apiSuccess {Object} data.results.privzdignjeno "Elevated" language style score object.
    * @apiSuccess {Float} data.results.privzdignjeno.diff "Elevated" language style score difference.
    * @apiSuccess {Float} data.results.privzdignjeno.score "Elevated" language style score.
    * @apiSuccess {Integer} data.results.privzdignjeno.rank "Elevated" language style score rank.

    * @apiSuccess {Object} data.results.speeches_per_session Average number of speeches per session object.
    * @apiSuccess {Float} data.results.speeches_per_session.diff Average number of speeches per session difference.
    * @apiSuccess {Float} data.results.speeches_per_session.score Average number of speeches per session.
    * @apiSuccess {Integer} data.results.speeches_per_session.rank Average number of speeches per session rank.

    * @apiSuccess {Object} data.results.number_of_questions Number of questions this MP has asked object.
    * @apiSuccess {Integer} data.results.number_of_questions.diff Number of questions this MP has asked difference.
    * @apiSuccess {Integer} data.results.number_of_questions.score Number of questions this MP has asked.
    * @apiSuccess {Integer} data.results.number_of_questions.rank Number of questions this MP has asked rank.

    * @apiSuccess {Object} data.results.presence_votes Percentage of votes this MP attended object.
    * @apiSuccess {Float} data.results.presence_votes.diff Percentage of votes this MP attended difference.
    * @apiSuccess {Float} data.results.presence_votes.score Percentage of votes this MP attended.
    * @apiSuccess {Integer} data.results.presence_votes.rank Percentage of votes this MP attended rank.

    * @apiSuccess {Object} data.results.presence_sessions Percentage of sessions this MP attended object.
    * @apiSuccess {Float} data.results.presence_sessions.diff Percentage of sessions this MP attended difference.
    * @apiSuccess {Float} data.results.presence_sessions.score Percentage of sessions this MP attended.
    * @apiSuccess {Integer} data.results.presence_sessions.rank Percentage of sessions this MP attended rank.

    * @apiSuccess {Object} data.results.problematicno "Problematic" language style score object.
    * @apiSuccess {Float} data.results.problematicno.diff "Problematic" language style score difference.
    * @apiSuccess {Float} data.results.problematicno.score "Problematic" language style score.
    * @apiSuccess {Integer} data.results.problematicno.rank "Problematic" language style score rank.
    
    * @apiSuccess {Object} data.results.vocabulary_size MP's calculated vocabulary size object.
    * @apiSuccess {Integer} data.results.vocabulary_size.diff MP's calculated vocabulary size difference.
    * @apiSuccess {Integer} data.results.vocabulary_size.score MP's calculated vocabulary size.
    * @apiSuccess {Integer} data.results.vocabulary_size.rank MP's calculated vocabulary size rank.

    * @apiSuccess {Object} data.results.spoken_words Number of words this MP has spoken.
    * @apiSuccess {Integer} data.results.spoken_words.diff Number of words this MP has spoken difference.
    * @apiSuccess {Integer} data.results.spoken_words.score Number of words this MP has spoken.
    * @apiSuccess {Integer} data.results.spoken_words.rank Number of words this MP has spoken rank.

    * @apiSuccess {Object} data.results.preprosto "Simple" language style score object.
    * @apiSuccess {Float} data.results.preprosto.diff "Simple" language style score difference.
    * @apiSuccess {Float} data.results.preprosto.score "Simple" language style score.
    * @apiSuccess {Integer} data.results.preprosto.rank "Simple" language style score rank.
    
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/p/getListOfMembersTickers
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/p/getListOfMembersTickers/12.12.2016

    * @apiSuccessExample {json} Example response:
    {
        "districts": [{
            "91": "Lendava 1"
        }, {
            "102": "Ljubljana-\u0160i\u0161ka I"
        }, {
            "101": "Ljubljana-\u0160i\u0161ka II"
        }, {
            "100": "Ljubljana-\u0160i\u0161ka III"
        }, {
            "99": "Ljubljana-\u0160i\u0161ka IV"
        }],
        "created_at": "2017-03-21T10:35:29.257",
        "created_for": "2017-03-21",
        "data": [{
            "person": {
            "name": "Aleksander Kav\u010di\u010d",
            "gov_id": "P259",
            "gender": "m",
            "is_active": false,
            "district": [19],
            "party": {
                "acronym": "SMC",
                "is_coalition": true,
                "name": "PS Stranka modernega centra",
                "id": 1
            },
            "type": "mp",
            "id": 39,
            "has_function": false
            },
            "results": {
            "privzdignjeno": {
                "diff": -0.07080984812327795,
                "score": 2.7438091511157987,
                "rank": 62
            },
            "speeches_per_session": {
                "diff": 0.0,
                "score": 1.0,
                "rank": 74
            },
            "number_of_questions": {
                "diff": 0.0,
                "score": 5.0,
                "rank": 62
            },
            "presence_votes": {
                "diff": 0.0681428694927888,
                "score": 89.589905362776,
                "rank": 37
            },
            "presence_sessions": {
                "diff": -1.1897036556349008,
                "score": 89.8550724637681,
                "rank": 42
            },
            "problematicno": {
                "diff": 0.04653717835381821,
                "score": 2.516673651070962,
                "rank": 62
            },
            "vocabulary_size": {
                "diff": 0.0,
                "score": 135.0,
                "rank": 14
            },
            "spoken_words": {
                "diff": 0,
                "score": 10837,
                "rank": 86
            },
            "preprosto": {
                "diff": 0.016475585916483126,
                "score": 3.377309423797745,
                "rank": 62
            }
            }
        }, {
            "person": {
            "name": "Alenka Bratu\u0161ek",
            "gov_id": "P166",
            "gender": "f",
            "is_active": false,
            "district": [62],
            "party": {
                "acronym": "PS NP",
                "is_coalition": false,
                "name": "PS nepovezanih poslancev ",
                "id": 109
            },
            "type": "mp",
            "id": 9,
            "has_function": false
            },
            "results": {
            "privzdignjeno": {
                "diff": 0.0022796756059407786,
                "score": 0.32064092814348816,
                "rank": 26
            },
            "speeches_per_session": {
                "diff": 0.0,
                "score": 5.0,
                "rank": 26
            },
            "number_of_questions": {
                "diff": 6.0,
                "score": 49.0,
                "rank": 26
            },
            "presence_votes": {
                "diff": -1.0823189594820946,
                "score": 46.6876971608833,
                "rank": 88
            },
            "presence_sessions": {
                "diff": 0.8219770711659038,
                "score": 72.463768115942,
                "rank": 87
            },
            "problematicno": {
                "diff": 0.005426527504002687,
                "score": 0.31498556069390254,
                "rank": 26
            },
            "vocabulary_size": {
                "diff": 0.0,
                "score": 96.0,
                "rank": 72
            },
            "spoken_words": {
                "diff": 2326,
                "score": 282204,
                "rank": 19
            },
            "preprosto": {
                "diff": 0.0014815186579075212,
                "score": 0.411863764711025,
                "rank": 26
            }
            }
        }]
    }
    """
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_ = date_of.strftime(API_DATE_FORMAT)
    lists = MembersList.objects.filter(created_for__lte=date_of)
    if not lists:
        return JsonResponse({'created_at': date_,
                             'created_for': date_,
                             'data': []},
                            safe=False)
    last_day = lists.latest('created_for').created_for
    cards = MembersList.objects.filter(created_for=last_day)
    card = cards.latest('created_at')
    return JsonResponse({'created_at': card.created_at,
                         'created_for': card.created_for,
                         'data': card.data,
                         'districts': [{dist.id_parladata: dist.name}
                                       for dist in District.objects.all()]},
                        safe=False)
