# -*- coding: UTF-8 -*-
from utils.speech import WordAnalysis
from parlalize.utils import *
import requests
import json
from django.http import JsonResponse
from parlaskupine.models import *
from parlaseje.models import Activity, Session, Vote, Speech, Question
from collections import Counter
from parlalize.settings import API_URL, API_DATE_FORMAT, BASE_URL, API_OUT_DATE_FORMAT
import numpy as np
from scipy.stats.stats import pearsonr
from scipy.spatial.distance import euclidean
from parlaposlanci.models import Person
from parlaposlanci.views import getMPsList
import math
from kvalifikatorji.scripts import countWords, getCountListPG, getScores, problematicno, privzdignjeno, preprosto
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from parlalize.utils import tryHard

# Create your views here.

def setBasicInfOfPG(request, pg_id, date_):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
        data = tryHard(API_URL+'/getBasicInfOfPG/'+str(pg_id)+'/'+date_).json()
    else:
        date_of = datetime.now().date()
        data = tryHard(API_URL+'/getBasicInfOfPG/'+str(pg_id)+'/'+date_of).json()

    headOfPG = 0
    viceOfPG = []
    if data['HeadOfPG'] != None:
        headOfPG = Person.objects.get(id_parladata=int(data['HeadOfPG']))
    else:
        headOfPG = None

    if data['ViceOfPG']:
        for vice in data['ViceOfPG']:
            if vice != None:
                viceOfPG.append(vice)
            else:
                viceOfPG.append(None)
    else:
                viceOfPG.append(None)

    result = saveOrAbortNew(model=PGStatic,
                            created_for=date_of,
                            organization=Organization.objects.get(id_parladata=int(pg_id)),
                            headOfPG=headOfPG,
                            viceOfPG=viceOfPG,
                            numberOfSeats=data['NumberOfSeats'],
                            allVoters=data['AllVoters'],
                            facebook=data['Facebook'],
                            twitter=data['Twitter'],
                            email=data['Mail']
                            )

    return JsonResponse({'alliswell': True})


def getBasicInfOfPG(request, pg_id, date=None):
    card = getPGCardModel(PGStatic, pg_id, date)
    headOfPG = 0
    viceOfPG = []
    if card.headOfPG:
        headOfPG = getPersonData(card.headOfPG.id_parladata, date)
    else:
        headOfPG = 0
    for vice in card.viceOfPG:
        if vice:
            viceOfPG.append(getPersonData(vice, date))
        # else:
            # viceOfPG.append(0)

    data = {
           'party':card.organization.getOrganizationData(),
           'created_at': card.created_at.strftime(API_DATE_FORMAT),
           'created_for': card.created_for.strftime(API_DATE_FORMAT),
           'headOfPG':headOfPG,
           'viceOfPG':viceOfPG,
           'numberOfSeats':card.numberOfSeats,
           'allVoters':card.allVoters,
           'social':{
           'facebook':card.facebook,
           'twitter':card.twitter,
           'email':card.email
           }
           }

    return JsonResponse(data)


def setPercentOFAttendedSessionPG(request, pg_id, date_=None):
    if date_:
        isNewVote = tryHard(API_URL +'/isVoteOnDay/'+date_).json()["isVote"]
        print isNewVote
        if not isNewVote:
            return JsonResponse({'alliswell': True, "status":'Ni glasovanja na ta dan', "saved": False})
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = findDatesFromLastCard(PercentOFAttendedSession, pg_id, datetime.now().date())[0]

    allSum = {}
    data = {}

    membersOfPG = tryHard(API_URL+'/getMembersOfPGsOnDate/'+date_).json()
    data = tryHard(API_URL+'/getNumberOfAllMPAttendedSessions/'+date_).json()

    sessions = {pg:[] for pg in membersOfPG if membersOfPG[pg]}
    votes = {pg:[] for pg in membersOfPG if membersOfPG[pg]}
    for pg in membersOfPG:
        if not membersOfPG[pg]:
            continue
        for member in membersOfPG[pg]:
            if str(member) in data["sessions"].keys():
                sessions[pg].append(data["sessions"][str(member)])
                votes[pg].append(data["votes"][str(member)])
        sessions[pg] = sum(sessions[pg])/len(sessions[pg])
        votes[pg] = sum(votes[pg])/len(votes[pg])

    thisMPSessions = sessions[pg_id]
    maximumSessions = max(sessions.values())
    maximumPGSessions = [pgId for pgId in sessions if sessions[pgId]==maximumSessions]
    averageSessions = sum(data["sessions"].values()) / len(data["sessions"])

    thisMPVotes = votes[pg_id]
    maximumVotes = max(votes.values())
    maximumPGVotes = [pgId for pgId in votes if votes[pgId]==maximumVotes]
    averageVotes = sum(data["votes"].values()) / len(data["votes"])

    #kaksen bo interfejs ko bo imela prav ta PG maksimum
    result = saveOrAbortNew(model=PercentOFAttendedSession,
                         created_for=date_of,
                         organization=Organization.objects.get(id_parladata=int(pg_id)),
                         organization_value_sessions = thisMPSessions,
                         maxPG_sessions=maximumPGSessions,
                         average_sessions=averageSessions,
                         maximum_sessions=maximumSessions,
                         organization_value_votes = thisMPVotes,
                         maxPG_votes=maximumPGVotes,
                         average_votes=averageVotes,
                         maximum_votes=maximumVotes)

    return JsonResponse({'alliswell': True})

def getPercentOFAttendedSessionPG(request, pg_id, date_=None):

    card = getPGCardModelNew(PercentOFAttendedSession, pg_id, date_)

    # uprasi ce isto kot pri personu razdelimo
    data = {
           'organization': card.organization.getOrganizationData(),
           'created_at': card.created_at.strftime(API_DATE_FORMAT),
           'created_for': card.created_for.strftime(API_DATE_FORMAT),
           "sessions":{
                'organization_value': card.organization_value_sessions,
                'maxPG': [Organization.objects.get(id_parladata=pg).getOrganizationData() for pg in card.maxPG_sessions],
                'average': card.average_sessions,
                'maximum': card.maximum_sessions,
                },
            "votes":{
                'organization_value': card.organization_value_votes,
                'maxPG': [Organization.objects.get(id_parladata=pg).getOrganizationData() for pg in card.maxPG_votes],
                'average': card.average_votes,
                'maximum': card.maximum_votes,
                }
           }

    return JsonResponse(data)


def setMPsOfPG(request, pg_id, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_ = datetime.now().date()

    membersOfPG = tryHard(API_URL+'/getMembersOfPGsOnDate/'+ date_).json()

    result = saveOrAbortNew(model=MPOfPg,
                        organization=Organization.objects.get(id_parladata=pg_id),
                        id_parladata=pg_id,
                        MPs =  membersOfPG[pg_id],
                        created_for=date_of
                        )

    return JsonResponse({'alliswell': True})

def getMPsOfPG(request, pg_id, date_=None):

    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_ = ""

    card = getPGCardModelNew(MPOfPg, pg_id, date_)
    ids = card.MPs
    result = sorted([getPersonData(MP, date_) for MP in ids], key=lambda k: k['name'])
    return JsonResponse({"results": result,
                         "party": card.organization.getOrganizationData(),
                         "created_at": card.created_at.strftime(API_DATE_FORMAT),
                         "created_for": card.created_for.strftime(API_DATE_FORMAT)})


def getSpeechesOfPG(request, pg_id, date_=False):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_ = date_of.strftime(API_DATE_FORMAT)

    speeches_q = Speech.getValidSpeeches(date_of + timedelta(days=1))

    membersOfPGRanges = reversed(tryHard(API_URL+'/getMembersOfPGsRanges' + ("/"+date_ if date_ else "")).json())
    out = []
    for pgMembersRange in membersOfPGRanges:
        startTime = datetime.strptime(pgMembersRange["start_date"],
                                      API_DATE_FORMAT)
        endTime = datetime.strptime(pgMembersRange["end_date"],
                                    API_DATE_FORMAT) + timedelta(hours=23,
                                                                 minutes=59)
        speeches = [[speech
                    for speech
                    in speeches_q.filter(person__id_parladata__in=pgMembersRange["members"][pg_id],
                                         start_time__range=[t_date, t_date+timedelta(days=1)]).order_by("-id_parladata")]
                    for t_date
                    in speeches_q.filter(start_time__lte=endTime,
                                         start_time__gte=startTime,
                                         person__id_parladata__in=pgMembersRange["members"][pg_id]).datetimes('start_time', 'day')]
        for day in reversed(speeches):
            #dayData = {"date": day[0].start_time.strftime(API_OUT_DATE_FORMAT), "sessions":[]}
            dayDataDict = {"date": day[0].start_time.strftime(API_OUT_DATE_FORMAT), "sessions":{}}
            addedPersons = []
            addedSessions = []
            for speech in day:
                #debug
                #print addedPersons, addedSessions
                #print dayData
                #print "add", speech.person.id_parladata, speech.session.id_parladata
                #print speech.id_parladata, speech.start_time
                #print "index", addedPersons.index(speech.person.id_parladata), addedSessions.index(speech.session.id_parladata)
                
                #if speech.session.id_parladata in addedSessions:
                if speech.session.id_parladata in dayDataDict["sessions"].keys():
                    if speech.person.id_parladata in dayDataDict["sessions"][speech.session.id_parladata]["speakers"].keys():
                        #session = dayData["sessions"][addedSessions.index(speech.session.id_parladata)]
                        #speaker = session["speakers"][addedPersons.index(speech.person.id_parladata)]
                        #speaker = ["speeches"].append(speech.id_parladata)

                        session = dayDataDict["sessions"][speech.session.id_parladata]
                        speaker = session["speakers"][speech.person.id_parladata]
                        speaker["speeches"].append(speech.id_parladata)
                    else:
                        #addedPersons.append(speech.person.id_parladata)
                        #dayData["sessions"][addedSessions.index(speech.session.id_parladata)]["speakers"].append({"speeches":[speech.id_parladata],
                        #                        "person":getPersonData(speech.person.id_parladata, startTime.strftime(API_DATE_FORMAT))})
                        session = dayDataDict["sessions"][speech.session.id_parladata]
                        session["speakers"][speech.person.id_parladata] = {
                            "speeches":[speech.id_parladata],
                            "person":getPersonData(speech.person.id_parladata, startTime.strftime(API_DATE_FORMAT))
                        }
                else:
                    #reset persons for each session on date
                    #addedPersons = []
                    #addedSessions.append(speech.session.id_parladata)
                    #addedPersons.append(speech.person.id_parladata)

                    dayDataDict["sessions"][speech.session.id_parladata]={
                        "session_name": speech.session.name,
                        "session_org": speech.session.organization.name,
                        "session_id": speech.session.id_parladata, 
                        "speakers":{ 
                            speech.person.id_parladata:{
                                "speeches":[speech.id_parladata],
                                "person":getPersonData(speech.person.id_parladata, startTime.strftime(API_DATE_FORMAT))
                            }
                        }
                    }

                    #dayData["sessions"].append({"session_name": speech.session.name,"session_id": speech.session.id_parladata, "speakers":[{"speeches":[speech.id_parladata],
                    #                            "person":getPersonData(speech.person.id_parladata, startTime.strftime(API_DATE_FORMAT))}]})
            #out.append(dayData)
            out.append(dayDataDict)
            if len(out)>14:
                break
        if len(out)>14:
            break

    #dict to list for sorting in front
    for day in out:
        ses_ids = day["sessions"].keys()
        for session in ses_ids:
            day["sessions"][session]["speakers"] = sorted(day["sessions"][session]["speakers"].values(), key=lambda k,: k["person"]["name"], reverse=False)
        ses_order_ids = Session.objects.filter(id_parladata__in=ses_ids).order_by("-start_time").values_list("id_parladata", flat=True)
        temp_day_order = [day["sessions"][s_id] for s_id in ses_order_ids]
        day["sessions"] = temp_day_order

    # WORKAROUND: created_at is today.
    result = {
        'results': out,
        "created_for": out[-1]["date"],
        "created_at": date_,
        "party": Organization.objects.get(id_parladata=pg_id).getOrganizationData()
        }
    return JsonResponse(result, safe=False)


def howMatchingThem(request, pg_id, type_of, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_ = date_of.strftime(API_DATE_FORMAT)

    pg_score, membersInPGs, votes, all_votes = getRangeVotes([pg_id],
                                                             date_,
                                                             'logic')

    # most match them
    if type_of == 'match':
        for voter in membersInPGs[str(pg_id)]:
            votes.pop(str(voter))

    # deviation in PG
    if type_of == 'deviation':
        del membersInPGs[str(pg_id)]
        for pgs in membersInPGs.keys():
            for voter in membersInPGs[str(pgs)]:
                # WORKAROUND: if one person is in more then one PG
                if str(voter) in votes:
                    votes.pop(str(voter))

    members = getMPsList(request, date_)
    membersDict = {str(mp['id']): mp for mp in json.loads(members.content)}

    # calculate euclidean
    out = {person: (euclidean(list(pg_score), [votes[str(person)][str(val)]
                    for val in all_votes]))
           for person in sorted(votes.keys())}

    for person in out.keys():
        if math.isnan(out[person]):
            out.pop(person, None)

    keys = sorted(out, key=out.get)
    key4remove = []
    for key in keys:
        # if members isn't member in this time skip him
        if key not in membersDict.keys():
            key4remove.append(key)
            continue
        membersDict[str(key)].update({'ratio': out[str(key)]})
        person = Person.objects.get(id_parladata=int(key))
        membersDict[key].update({'person': person, 'id': key})

    # remove keys of members which isn't member in this time
    for key in key4remove:
        keys.remove(key)
    return membersDict, keys, date_of


def setMostMatchingThem(request, pg_id, date_=None):
    if date_:
        isNewVote = tryHard(API_URL + '/isVoteOnDay/'+date_).json()['isVote']
        print isNewVote
        if not isNewVote:
            return JsonResponse({'alliswell': True,
                                 'status': 'Ni glasovanja na ta dan',
                                 'saved': False})
        members, keys, date_of = howMatchingThem(request, pg_id,
                                                 date_=date_,
                                                 type_of='match')
    else:
        members, keys, date_of = howMatchingThem(request,
                                                 pg_id,
                                                 type_of='match')

    out = {index: members[key]
           for key, index in zip(keys[:5], [1, 2, 3, 4, 5])}

    try:
        org = Organization.objects.get(id_parladata=int(pg_id))
        result = saveOrAbortNew(model=MostMatchingThem,
                                created_for=date_of,
                                organization=org,
                                person1=out[1]['person'],
                                votes1=out[1]['ratio'],
                                person2=out[2]['person'],
                                votes2=out[2]['ratio'],
                                person3=out[3]['person'],
                                votes3=out[3]['ratio'],
                                person4=out[4]['person'],
                                votes4=out[4]['ratio'],
                                person5=out[5]['person'],
                                votes5=out[5]['ratio'])
        return JsonResponse({'alliswell': True})
    except:
        return JsonResponse({'alliswell': False})


def setLessMatchingThem(request, pg_id, date_=None):
    if date_:
        isNewVote = tryHard(API_URL + '/isVoteOnDay/' + date_).json()['isVote']
        print isNewVote
        if not isNewVote:
            return JsonResponse({'alliswell': True,
                                 'status': 'Ni glasovanja na ta dan',
                                 'saved': False})
        members, keys, date_of = howMatchingThem(request,
                                                 pg_id,
                                                 date_=date_,
                                                 type_of='match')
    else:
        members, keys, date_of = howMatchingThem(request,
                                                 pg_id,
                                                 type_of='match')

    out = {index: members[key]
           for key, index in zip(keys[-6:-1], [5, 4, 3, 2, 1])}
    org = Organization.objects.get(id_parladata=int(pg_id))
    try:
        result = saveOrAbortNew(model=LessMatchingThem,
                                created_for=date_of,
                                organization=org,
                                person1=out[1]['person'],
                                votes1=out[1]['ratio'],
                                person2=out[2]['person'],
                                votes2=out[2]['ratio'],
                                person3=out[3]['person'],
                                votes3=out[3]['ratio'],
                                person4=out[4]['person'],
                                votes4=out[4]['ratio'],
                                person5=out[5]['person'],
                                votes5=out[5]['ratio'])
        return JsonResponse({'alliswell': True})
    except:
        return JsonResponse({'alliswell': False})


def setDeviationInOrg(request, pg_id, date_=None):
    if date_:
        isNewVote = tryHard(API_URL + '/isVoteOnDay/'+date_).json()['isVote']
        print isNewVote
        if not isNewVote:
            return JsonResponse({'alliswell': True,
                                 'status': 'Ni glasovanja na ta dan',
                                 'saved': False})
        members, keys, date_of = howMatchingThem(request,
                                                 pg_id,
                                                 date_=date_,
                                                 type_of='deviation')
    else:
        members, keys, date_of = howMatchingThem(request,
                                                 pg_id,
                                                 type_of='deviation')

    numOfKeys = len(keys)

    out = []
    for member, data in members.items():
        if member in keys:
            print member, data
            data.pop('person')
            out.append(data)
    out = sorted(out, key=lambda k, : k['ratio'], reverse=True)
    print 'out', out
    try:
        org_data = Organization.objects.get(id_parladata=int(pg_id))
        result = saveOrAbortNew(model=DeviationInOrganization,
                                created_for=date_of,
                                organization=org_data,
                                data=json.dumps(out)
                                )

        return JsonResponse({'alliswell': True,
                             'status': 'OK',
                             'saved': result})
    except:
        return JsonResponse({'alliswell': False})


def getMPStaticPersonData(id_, date_):
    try:
        url = BASE_URL + '/p/getMPStatic/' + str(id_) + '/' + date_
        return tryHard(url).json()['person']
    except:
        return {'id': id_}


def getMostMatchingThem(request, pg_id, date_=None):
    mostMatching = getPGCardModelNew(MostMatchingThem, pg_id, date_)
    if not date_:
        date_ = ''
    org = Organization.objects.get(id_parladata=int(pg_id))
    out = {
        'organization': org.getOrganizationData(),
        'created_at': mostMatching.created_at.strftime(API_DATE_FORMAT),
        'created_for': mostMatching.created_for.strftime(API_DATE_FORMAT),
        'results': [
            {
                'ratio': mostMatching.votes1,
                'person': getPersonData(mostMatching.person1.id_parladata,
                                        date_)
            },
            {
                'ratio': mostMatching.votes2,
                'person': getPersonData(mostMatching.person2.id_parladata,
                                        date_)
            },
            {
                'ratio': mostMatching.votes3,
                'person': getPersonData(mostMatching.person3.id_parladata,
                                        date_)
            },
            {
                'ratio': mostMatching.votes4,
                'person': getPersonData(mostMatching.person4.id_parladata,
                                        date_)
            },
            {
                'ratio': mostMatching.votes5,
                'person': getPersonData(mostMatching.person5.id_parladata,
                                        date_)
            }
        ]
    }

    return JsonResponse(out, safe=False)


def getLessMatchingThem(request, pg_id, date_=None):
    mostMatching = getPGCardModelNew(LessMatchingThem, pg_id, date_)
    if not date_:
        date_ = ''

    org = Organization.objects.get(id_parladata=int(pg_id))
    out = {
        'organization': org.getOrganizationData(),
        'created_at': mostMatching.created_at.strftime(API_DATE_FORMAT),
        'created_for': mostMatching.created_for.strftime(API_DATE_FORMAT),
        'results': [
            {
                'ratio': mostMatching.votes1,
                'person': getPersonData(mostMatching.person1.id_parladata,
                                        date_)
            },
            {
                'ratio': mostMatching.votes2,
                'person': getPersonData(mostMatching.person2.id_parladata,
                                        date_)
            },
            {
                'ratio': mostMatching.votes3,
                'person': getPersonData(mostMatching.person3.id_parladata,
                                        date_)
            },
            {
                'ratio': mostMatching.votes4,
                'person': getPersonData(mostMatching.person4.id_parladata,
                                        date_)
            },
            {
                'ratio': mostMatching.votes5,
                'person': getPersonData(mostMatching.person5.id_parladata,
                                        date_)
            }
        ]
    }
    return JsonResponse(out, safe=False)


def getDeviationInOrg(request, pg_id, date_=None):
    mostMatching = getPGCardModelNew(DeviationInOrganization, pg_id, date_)
    if not date_:
        date_ = ''
    out_r = []
    for result in mostMatching.data:
        out_r.append({
            'ratio': result['ratio'],
            'person': getMPStaticPersonData(int(result['id']), date_)})
    org = Organization.objects.get(id_parladata=int(pg_id))
    out = {
        'organization': org.getOrganizationData(),
        'created_at': mostMatching.created_at.strftime(API_DATE_FORMAT),
        'created_for': mostMatching.created_for.strftime(API_DATE_FORMAT),
        'results': out_r
    }
    # remove None from list. If PG dont have 6 members.
    out['results'] = filter(lambda a: a is not None, out['results'])
    return JsonResponse(out, safe=False)


def setCutVotes(request, pg_id, date_=None):
    def getMaxOrgData(data, ids):
        d = {str(pg): data[pg] for pg in ids}
        keys =  ','.join([key for key,val in d.iteritems() if val == max(d.values())])
        return keys, max(d.values())
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_ = date_of.strftime(API_DATE_FORMAT)

    isNewVote = tryHard(API_URL +'/isVoteOnDay/'+date_).json()['isVote']
    print isNewVote
    if not isNewVote:
        return JsonResponse({'alliswell': True, 'status':'Ni glasovanja na ta dan', 'saved': False})

    r = tryHard(API_URL+'/getCoalitionPGs/')
    coalition = r.json()

    pgs_for = {}
    pgs_against = {}
    pgs_abstain = {}
    pgs_absent = {}
    pgs_abstain = {}
    pgs_absent = {}

    coal_avg = {}
    oppo_avg = {}

    coal_pgs = [str(pg) for pg in coalition["coalition"]]
    oppo_pgs = [str(pg) for pg in coalition["opposition"]]

    pg_score_C, membersInPGs, votes, all_votes = getRangeVotes(coal_pgs, date_, "plain")
    pg_score_O, membersInPGs, votes, all_votes = getRangeVotes(oppo_pgs, date_, "plain")


    # Calculate coalition and opposition average
    coal_avg["for"] = (float(sum(map(voteFor, pg_score_C)))/float(len(pg_score_C)))*100
    oppo_avg["for"] = (float(sum(map(voteFor, pg_score_O)))/float(len(pg_score_O)))*100
    coal_avg["against"] = (float(sum(map(voteAgainst, pg_score_C)))/float(len(pg_score_C)))*100
    oppo_avg["against"] = (float(sum(map(voteAgainst, pg_score_O)))/float(len(pg_score_O)))*100
    coal_avg["abstain"] = (float(sum(map(voteAbstain, pg_score_C)))/float(len(pg_score_C)))*100
    oppo_avg["abstain"] = (float(sum(map(voteAbstain, pg_score_O)))/float(len(pg_score_O)))*100
    coal_avg["absent"] = (float(sum(map(voteAbsent, pg_score_C)))/float(len(pg_score_C)))*100
    oppo_avg["absent"] = (float(sum(map(voteAbsent, pg_score_O)))/float(len(pg_score_O)))*100

    # get votes against
    for pg in membersInPGs:
        votesOfPG = [votes[str(member)][b] for member in membersInPGs[str(pg)] for b in sorted(votes[str(member)])]
        # get votes for of PGs
        try:
            pgs_for[str(pg)] = (float(sum(map(voteFor, votesOfPG)))/float(len(votesOfPG)))*100
        except:
            pgs_for[str(pg)] = 0
        # get votes against of PGs
        try:                 
            pgs_against[str(pg)] = (float(sum(map(voteAgainst, votesOfPG)))/float(len(votesOfPG)))*100
        except:
            pgs_against[str(pg)] = 0

        # get votes abstain of PGs
        try:
            pgs_abstain[str(pg)] = (float(sum(map(voteAbstain, votesOfPG)))/float(len(votesOfPG)))*100
        except:
            pgs_abstain[str(pg)] = 0

        # get votes obsent of PGs
        try:
            pgs_absent[str(pg)] = (float(sum(map(voteAbsent, votesOfPG)))/float(len(votesOfPG)))*100
        except:
            pgs_absent[str(pg)] = 0

    final_response = saveOrAbortNew(
        CutVotes,
        created_for=date_of,
        organization=Organization.objects.get(id_parladata=pg_id),
        this_for=pgs_for[pg_id],
        this_against=pgs_against[pg_id],
        this_abstain=pgs_abstain[pg_id],
        this_absent=pgs_absent[pg_id],
        coalition_for=coal_avg["for"],
        coalition_against=coal_avg["against"],
        coalition_abstain=coal_avg["abstain"],
        coalition_absent=coal_avg["absent"],
        coalition_for_max=getMaxOrgData(pgs_for, coal_pgs)[1],
        coalition_against_max=getMaxOrgData(pgs_against, coal_pgs)[1],
        coalition_abstain_max=getMaxOrgData(pgs_abstain, coal_pgs)[1],
        coalition_absent_max=getMaxOrgData(pgs_absent, coal_pgs)[1],
        coalition_for_max_org=getMaxOrgData(pgs_for, coal_pgs)[0],
        coalition_against_max_org=getMaxOrgData(pgs_against, coal_pgs)[0],
        coalition_abstain_max_org=getMaxOrgData(pgs_abstain, coal_pgs)[0],
        coalition_absent_max_org=getMaxOrgData(pgs_absent, coal_pgs)[0],
        opposition_for=oppo_avg["for"],
        opposition_against=oppo_avg["against"],
        opposition_abstain=oppo_avg["abstain"],
        opposition_absent=oppo_avg["absent"],
        opposition_for_max=getMaxOrgData(pgs_for, oppo_pgs)[1],
        opposition_against_max=getMaxOrgData(pgs_against, oppo_pgs)[1],
        opposition_abstain_max=getMaxOrgData(pgs_abstain, oppo_pgs)[1],
        opposition_absent_max=getMaxOrgData(pgs_absent, oppo_pgs)[1],
        opposition_for_max_org=getMaxOrgData(pgs_for, oppo_pgs)[0],
        opposition_against_max_org=getMaxOrgData(pgs_against, oppo_pgs)[0],
        opposition_abstain_max_org=getMaxOrgData(pgs_abstain, oppo_pgs)[0],
        opposition_absent_max_org=getMaxOrgData(pgs_absent, oppo_pgs)[0]
    )

    return JsonResponse({'alliswell': True, "status":'OK', "saved": final_response})


def getCutVotes(request, pg_id, date=None):
    cutVotes = getPGCardModelNew(CutVotes, pg_id, date)
    this_org = Organization.objects.get(id_parladata=int(pg_id))
    out = {
        'organization': this_org.getOrganizationData(),
        'created_at': cutVotes.created_at.strftime(API_DATE_FORMAT),
        'created_for': cutVotes.created_for.strftime(API_DATE_FORMAT),
        'results': {
            'abstain': {
                'score': cutVotes.this_abstain,
                'maxCoalition': {
                    'parties': [org.getOrganizationData() for org in Organization.objects.filter(id_parladata__in=[int(textid) for textid in cutVotes.coalition_abstain_max_org.split(',')])],
                    'score': cutVotes.coalition_abstain_max
                },
                'maxOpposition': {
                    'parties': [org.getOrganizationData() for org in Organization.objects.filter(id_parladata__in=[int(textid) for textid in cutVotes.opposition_abstain_max_org.split(',')])],
                    'score': cutVotes.opposition_abstain_max
                },
                "avgOpposition": {'score': cutVotes.opposition_abstain},
                "avgCoalition": {'score': cutVotes.coalition_abstain},
            },
            "against": {
                'score': cutVotes.this_against,
                'maxCoalition': {
                    'parties': [org.getOrganizationData()for org in Organization.objects.filter(id_parladata__in=[int(textid) for textid in cutVotes.coalition_against_max_org.split(',')])],
                    'score': cutVotes.coalition_against_max
                },
                'maxOpposition': {
                    'parties': [org.getOrganizationData() for org in Organization.objects.filter(id_parladata__in=[int(textid) for textid in cutVotes.opposition_against_max_org.split(',')])],
                    'score': cutVotes.opposition_against_max
                },
                "avgOpposition": {'score': cutVotes.opposition_against},
                "avgCoalition": {'score': cutVotes.coalition_against},
            },
            "absent": {
                'score': cutVotes.this_absent,
                'maxCoalition': {
                    'parties': [org.getOrganizationData() for org in Organization.objects.filter(id_parladata__in=[int(textid) for textid in cutVotes.coalition_absent_max_org.split(',')])],
                    'score': cutVotes.coalition_absent_max
                },
                'maxOpposition': {
                    'parties': [org.getOrganizationData() for org in Organization.objects.filter(id_parladata__in=[int(textid) for textid in cutVotes.opposition_absent_max_org.split(',')])],
                    'score': cutVotes.opposition_absent_max
                },
                "avgOpposition": {'score': cutVotes.opposition_absent},
                "avgCoalition": {'score': cutVotes.coalition_absent},
            },
            'for': {
                'score': cutVotes.this_for,
                'maxCoalition': {
                    'parties': [org.getOrganizationData() for org in Organization.objects.filter(id_parladata__in=[int(textid) for textid in cutVotes.coalition_for_max_org.split(',')])],
                    'score': cutVotes.coalition_for_max
                },
                'maxOpposition': {
                    'parties': [org.getOrganizationData() for org in Organization.objects.filter(id_parladata__in=[int(textid) for textid in cutVotes.opposition_for_max_org.split(',')])],
                    'score': cutVotes.opposition_for_max
                },
                "avgOpposition": {'score': cutVotes.opposition_for},
                "avgCoalition": {'score': cutVotes.coalition_for},
            },
        }
    }
    return JsonResponse(out)


def setWorkingBodies(request, org_id, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
    print "set "+org_id+" "+date_
    members = tryHard(API_URL+"/getOrganizationRolesAndMembers/"+org_id+(("/"+date_) if date_ else "")).json()
    if not len(members["president"]) or not len(members["members"]) or not len(members["vice_president"]):
        return JsonResponse({'alliswell': False, "status": {"president_count": len(members["president"]),
                                                            "vice_president": len(members["vice_president"]),
                                                            "members": len(members["members"]),
                                                            "viceMember": len(members['viceMember'])
                                                            }})
    out = {}
    name = members.pop("name")
    all_members = [member for role in members.values() for member in role]
    coalitionPGs = tryHard(API_URL+'/getCoalitionPGs/').json()
    membersOfPG = tryHard(API_URL+'/getMembersOfPGsOnDate/'+date_).json()
    sessions = tryHard(API_URL+'/getSessionsOfOrg/'+org_id+(("/"+date_) if date_ else "")).json()
    coal_pgs = {str(pg):[member for member in membersOfPG[str(pg)] if member in all_members] for pg in coalitionPGs["coalition"]}
    oppo_pgs = {str(pg):[member for member in membersOfPG[str(pg)] if member in all_members] for pg in coalitionPGs["opposition"]}

    coal_members = sum([len(member) for member in coal_pgs.values()])
    oppo_members = sum([len(member) for member in oppo_pgs.values()])

    kol = 100.0/float(coal_members+oppo_members)
    
    seats = [{"party":Organization.objects.get(id_parladata=pg_id).getOrganizationData(), "seats": len(members_list), "coalition": "coalition"}for pg_id, members_list in coal_pgs.items() if len(members_list)>0]+[{"party":Organization.objects.get(id_parladata=pg_id).getOrganizationData(), "seats": len(members_list), "coalition": "opposition"}for pg_id, members_list in oppo_pgs.items() if len(members_list)>0]
    out["info"] = {role: [member for member in members_list] for role, members_list in members.items()}
    out["ratio"] = {"coalition": coal_members*kol, "opposition": oppo_members*kol}
    out["seats_per_pg"] = list(reversed(sorted(seats, key=lambda s: s["seats"])))
    out["sessions"] = [{"id": session["id"], "name": session["name"], "date": session["start_time"]} for session in sessions]
    out["name"] = name
    final_response = saveOrAbortNew(
        WorkingBodies,
        created_for=date_of,
        organization=Organization.objects.get(id_parladata=org_id),
        president = Person.objects.get(id_parladata=out["info"]["president"][0]),
        vice_president = out["info"]["vice_president"],
        members = out["info"]["members"],
        viceMember = out["info"]["viceMember"],
        coal_ratio = coal_members*kol,
        oppo_ratio = oppo_members*kol,
        seats = list(reversed(sorted(seats, key=lambda s: s["seats"]))),
        sessions = [session["id"] for session in sessions],
    )
    return JsonResponse(out)


def getWorkingBodies(request, org_id, date_=None):
    workingBodies = getPGCardModelNew(WorkingBodies, org_id, date_)
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
    sessions = [session.getSessionData()
                for session
                in Session.objects.filter(organizations__id_parladata=org_id,
                                          start_time__lte=date_of).order_by("-start_time")]

    for session in sessions:
        session.update({"votes": True if Vote.objects.filter(session__id_parladata=session["id"]) else False, 
                        "speeches": True if Speech.objects.filter(session__id_parladata=session["id"]) else False})

    return JsonResponse({"organization": workingBodies.organization.getOrganizationData(),
                         'created_at': workingBodies.created_at.strftime(API_DATE_FORMAT),
                         'created_for': workingBodies.created_for.strftime(API_DATE_FORMAT),
                         "info": {"president": getPersonData(workingBodies.president.id_parladata),
                                  "vice_president": sorted([getPersonData(person) for person in workingBodies.vice_president], key=lambda k: k['name']),
                                  "members": sorted([getPersonData(person) for person in workingBodies.members], key=lambda k: k['name']),
                                  "viceMember": sorted([getPersonData(person) for person in workingBodies.viceMember], key=lambda k: k['name'])},
                         "ratio":{"coalition": workingBodies.coal_ratio,
                                  "opposition": workingBodies.oppo_ratio},
                         "seats_per_pg": workingBodies.seats,
                         "sessions": sessions})


def getWorkingBodies_live(request, org_id, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
    members = tryHard(API_URL+"/getOrganizationRolesAndMembers/"+org_id+(("/"+date_) if date_ else "")).json()
    out = {}
    name = members.pop("name")
    all_members = [member for role in members.values() for member in role]
    coalitionPGs = tryHard(API_URL+'/getCoalitionPGs/').json()
    membersOfPG = tryHard(API_URL+'/getMembersOfPGsOnDate/'+date_).json()
    sessions = tryHard(API_URL+'/getSessionsOfOrg/'+org_id+(("/"+date_) if date_ else "")).json()
    coal_pgs = {str(pg):[member for member in membersOfPG[str(pg)] if member in all_members] for pg in coalitionPGs["coalition"]}
    oppo_pgs = {str(pg):[member for member in membersOfPG[str(pg)] if member in all_members] for pg in coalitionPGs["opposition"]}

    coal_members = sum([len(member) for member in coal_pgs.values()])
    oppo_members = sum([len(member) for member in oppo_pgs.values()])

    kol = 100.0/float(coal_members+oppo_members)
    seats = [{"party":Organization.objects.get(id_parladata=pg_id).getOrganizationData(), "seats": len(members_list), "coalition": "coalition"}for pg_id, members_list in coal_pgs.items() if len(members_list)>0]+[{"party":Organization.objects.get(id_parladata=pg_id).getOrganizationData(), "seats": len(members_list), "coalition": "opposition"}for pg_id, members_list in oppo_pgs.items() if len(members_list)>0]
    out["info"] = {role: [getPersonData(member) for member in members_list] for role, members_list in members.items()}
    out["ratio"] = {"coalition": coal_members*kol, "opposition": oppo_members*kol}
    out["seats_per_pg"] = list(reversed(sorted(seats, key=lambda s: s["seats"])))
    out["sessions"] = [{"id": session["id"], "name": session["name"], "date": session["start_time"]} for session in sessions]
    out["name"] = name
    return JsonResponse(out)


def getTaggedBallots(request, pg_id, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT)
    else:
        date_of = datetime.now().date()
        date_ = ''
    url = API_URL + '/getMembersOfPGRanges/' + pg_id + '/' + date_
    membersOfPGRanges = tryHard(url).json()
    out = []
    latest = []
    for pgMembersRange in membersOfPGRanges:
        ballots = Ballot.objects.filter(person__id_parladata__in=pgMembersRange['members'],
                                        start_time__lte=datetime.strptime(pgMembersRange['end_date'],
                                                                          API_DATE_FORMAT),
                                        start_time__gte=datetime.strptime(pgMembersRange['start_date'],
                                                                          API_DATE_FORMAT))
        if ballots:
            latest.append(ballots.latest('created_at').created_at)
        ballots = [ballots.filter(start_time__range=[t_date,
                                                     t_date+timedelta(days=1)])
                   for t_date
                   in ballots.order_by('start_time').datetimes('start_time',
                                                               'day')]

        for day in ballots:
            dayData = {'date': day[0].start_time.strftime(API_OUT_DATE_FORMAT),
                       'ballots': []}
            votes = list(set(day.order_by('start_time').values_list('vote_id',
                                                                    flat=True)))
            for vote in votes:
                vote_balots = day.filter(vote_id=vote)
                counter = Counter(vote_balots.values_list('option', flat=True))
                dayData['ballots'].append({
                    'motion': vote_balots[0].vote.motion,
                    'vote_id': vote_balots[0].vote.id_parladata,
                    'result': vote_balots[0].vote.result,
                    'session_id': vote_balots[0].vote.session.id_parladata if vote_balots[0].vote.session else None,
                    'option': max(counter, key=counter.get),
                    'tags': vote_balots[0].vote.tags})
            out.append(dayData)

    tags = list(Tag.objects.all().values_list('name', flat=True))
    result = {
        'party': Organization.objects.get(id_parladata=pg_id).getOrganizationData(),
        'created_at': max(latest).strftime(API_DATE_FORMAT) if latest else None,
        'created_for': out[-1]['date'] if out else None,
        'all_tags': tags,
        'results': list(reversed(out))
        }
    return JsonResponse(result, safe=False)


#Depricated
def setVocabularySizeALL_(request, date_):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_=""

#    thisperson = Person.objects.get(id_parladata=int(person_id))

    mps = tryHard(API_URL+'/getMPs/'+date_).json()
    membersOfPGsRanges = tryHard(API_URL+'/getMembersOfPGsRanges' + ("/"+date_ if date_ else "/")).json()
    print "setVocabularySizeALL " + date_
    text = {}
    vocabulary_sizes = []
    result = {}
    for pgMembersRange in membersOfPGsRanges:
        print "___" + pgMembersRange["start_date"]
        for pg in pgMembersRange["members"].keys():
            for member in pgMembersRange["members"][pg]: 
                speeches = tryHard(API_URL+'/getSpeechesInRange/' + str(member) + "/" + pgMembersRange["start_date"] + "/" + pgMembersRange["end_date"]).json()
                if pg in text.keys():
                    text[pg] += ''.join([speech['content'] for speech in speeches])
                else:
                    text[pg] = ''.join([speech['content'] for speech in speeches])
                    
    for pg, words in text.items():
        vocabulary_sizes.append({'pg': pg, 'vocabulary_size': len(countWords(words, Counter()))})

#        if int(mp['id']) == int(person_id):
#            result['person'] = len(countWords(text, Counter()))

    vocabularies_sorted = sorted(vocabulary_sizes, key=lambda k: k['vocabulary_size'])

    scores = [org['vocabulary_size'] for org in vocabulary_sizes]

    result['average'] = float(sum(scores))/float(len(scores))

    result['max'] = vocabularies_sorted[-1]['vocabulary_size']
    maxOrg = Organization.objects.get(id_parladata=vocabularies_sorted[-1]['pg'])

#    result.append({'person_id': vocabularies_sorted[-1]['person_id'], 'vocabulary_size': vocabularies_sorted[-1]['vocabulary_size']})

    for p in vocabularies_sorted:
        saveOrAbortNew(
            VocabularySize,
            organization=Organization.objects.get(id_parladata=int(p['pg'])),
            created_for=date_of,
            score=[v['vocabulary_size'] for v in vocabularies_sorted if v['pg'] == p['pg']][0],
            maxOrg=maxOrg,
            average=result['average'],
            maximum=result['max'])

    return JsonResponse({'alliswell': True})


def setVocabularySizeALL(request, date_=None):
    sw = WordAnalysis(count_of="groups", date_=date_)

    if not sw.isNewSpeech:
        return JsonResponse({'alliswell': True, 'msg': 'Na ta dan ni bilo govorov'})

    #Vocabolary size
    all_score = sw.getVocabularySize()
    max_score, maxPGid = sw.getMaxVocabularySize()
    avg_score = sw.getAvgVocabularySize()
    date_of = sw.getDate()
    maxPG = Organization.objects.get(id_parladata=maxPGid)

    print "[INFO] saving vocabulary size"
    for p in all_score:
        saveOrAbortNew(model=VocabularySize,
                       organization=Organization.objects.get(id_parladata=int(p['counter_id'])),
                       created_for=date_of,
                       score=int(p['coef']),
                       maxOrg=maxPG,
                       average=avg_score,
                       maximum=max_score)


    return JsonResponse({'alliswell': True, 'msg': 'shranjeno'})


def getVocabularySize(request, pg_id, date_=None):

    card = getPGCardModelNew(VocabularySize, pg_id, date_)

    out = {
        'party': card.organization.getOrganizationData(),
        'created_at': card.created_at.strftime(API_DATE_FORMAT),
        'created_for': card.created_for.strftime(API_DATE_FORMAT),
        'results': {
            'max': {
                'score': card.maximum,
                'parties': [card.maxOrg.getOrganizationData()]
            },
            'average': card.average,
            'score': card.score
        }
    }

    return JsonResponse(out, safe=False)

# get PGs IDs
def getPGsIDs(request):
    output = []
    data = tryHard(API_URL+'/getAllPGs/')
    data = data.json()

    output = {"list": [i for i in data], "lastDate": Session.objects.all().order_by("-start_time")[0].start_time.strftime(API_DATE_FORMAT)}

    return JsonResponse(output, safe=False)


def setStyleScoresPGsALL(request, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_=date_of.strftime(API_DATE_FORMAT)

    membersOfPGsRanges = tryHard(API_URL+'/getMembersOfPGsRanges' + ("/"+date_ if date_ else "/")).json()
    pgs = membersOfPGsRanges[-1]["members"].keys()

    print 'Starting PGs'
    scores = {}
    for pg in pgs:
        print 'PG id: ' + str(pg)

        # get word counts with solr
        counter = Counter(getCountListPG(int(pg), date_))
        total = sum(counter.values())

        scores_local = getScores([problematicno, privzdignjeno, preprosto], counter, total)

        #average = average_scores

        print scores_local, #average
        scores[pg] = scores_local


    print scores
    average = {"problematicno": sum([score['problematicno'] for score in scores.values()])/len(scores), "privzdignjeno": sum([score['privzdignjeno'] for score in scores.values()])/len(scores), "preprosto": sum([score['preprosto'] for score in scores.values()])/len(scores)}
    for pg, score in scores.items():
        saveOrAbortNew(
            model=StyleScores,
            created_for=date_of,
            organization=Organization.objects.get(id_parladata=int(pg)),
            problematicno=score['problematicno'],
            privzdignjeno=score['privzdignjeno'],
            preprosto=score['preprosto'],
            problematicno_average=average['problematicno'],
            privzdignjeno_average=average['privzdignjeno'],
            preprosto_average=average['preprosto']
        )

    return JsonResponse({'alliswell': True})


@csrf_exempt
def setAllPGsStyleScoresFromSearch(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        print post_data
        if post_data:
            save_statuses = []
            for score in post_data:
                print score
                #print score["date_of"]
                date_of = datetime.today()
                save_statuses.append(saveOrAbortNew(model=StyleScores,
                                                    created_for=date_of,
                                                    organization=Organization.objects.get(id_parladata=int(score["party"])),
                                                    problematicno=float(score['problematicno']),
                                                    privzdignjeno=float(score['privzdignjeno']),
                                                    preprosto=float(score['preprosto']),
                                                    problematicno_average=float(score['problematicno_average']),
                                                    privzdignjeno_average=float(score['privzdignjeno_average']),
                                                    preprosto_average=float(score['preprosto_average'])
                                                ))
            return JsonResponse({"status": "alliswell", "saved": save_statuses})
        else:
            return JsonResponse({"status": "There's not data"})
    else:
        return JsonResponse({"status": "It wasnt POST"})

def getStyleScoresPG(request, pg_id, date_=None):
    card = getPGCardModelNew(StyleScores, int(pg_id), date_)

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
        'party': card.organization.getOrganizationData(),
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

    # out = {
    #     'party': card.organization.getOrganizationData(),
    #     'created_at': card.created_at.strftime(API_DATE_FORMAT),
    #     'created_for': card.created_for.strftime(API_DATE_FORMAT),
    #     'results': {
    #         'privzdignjeno': card.privzdignjeno*10000,
    #         'problematicno': card.problematicno*10000,
    #         'preprosto': card.preprosto*10000,
    #         'average': {
    #             'privzdignjeno': card.privzdignjeno_average*10000,
    #             'problematicno': card.problematicno_average*10000,
    #             'preprosto': card.preprosto_average*10000
    #         }
    #     }
    # }
    return JsonResponse(out, safe=False)


@csrf_exempt
def setAllPGsTFIDFsFromSearch(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        if post_data:
            save_statuses = []
            for score in post_data:
                date_of = datetime.today()
                save_statuses.append(saveOrAbortNew(Tfidf, 
                                                    organization=Organization.objects.get(id_parladata=score["party"]["id"]), 
                                                    created_for=date_of,
                                                    is_visible=False,
                                                    data=score["results"]))

            return JsonResponse({"status": "alliswell", "saved": save_statuses})
        else:
            return JsonResponse({"status": "There's not data"})
    else:
        return JsonResponse({"status": "It wasnt POST"})

def setTFIDF(request, party_id, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT)
    else:
        date_of = datetime.now().date()
        date_ = date_of.strftime(API_DATE_FORMAT)
    print "TFIDF", party_id
    data = tryHard("https://isci.parlameter.si/tfidf/ps/"+party_id).json()
    is_saved = saveOrAbortNew(Tfidf,
                              organization=Organization.objects.get(id_parladata=party_id),
                              created_for=date_of,
                              data=data["results"])

    return JsonResponse({"alliswell": True,
                         "saved": is_saved})


def getTFIDF(request, party_id, date_=None):

    card = getPGCardModelNew(Tfidf, int(party_id), is_visible=True, date=date_)

    out = {
        'party': card.organization.getOrganizationData(),
        'results': card.data,
        "created_for": card.created_for.strftime(API_DATE_FORMAT), 
        "created_at": card.created_at.strftime(API_DATE_FORMAT)
    }

    return JsonResponse(out)


def setNumberOfQuestionsAll(request, date_=None):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT)
    else:
        date_of = datetime.now().date()

    date_s = date_of.strftime(API_DATE_FORMAT)

    url = API_URL + '/getAllQuestions/' + date_s
    data = tryHard(url).json()
    url_pgs = API_URL + '/getAllPGs/' + date_s
    pgs_on_date = tryHard(url_pgs).json()
    url = API_URL + '/getMPs/' + date_s
    mps = tryHard(url).json()

    mpStatic = {}
    for mp in mps:
        mpStatic[str(mp['id'])] = getPersonData(str(mp['id']), date_s)

    allPGs = tryHard(API_URL+'/getAllPGsExt/').json().keys()

    pg_ids = [int(pg_id) for pg_id in pgs_on_date.keys()]
    authors = []
    for question in data:
        qDate = datetime.strptime(question['date'], "%Y-%m-%dT%X")
        qDate = qDate.strftime(API_DATE_FORMAT)
        try:
            person_data = mpStatic[str(question['author_id'])]
        except KeyError as e:
            person_data = getPersonData(str(question['author_id']), date_s)
            mpStatic[str(question['author_id'])] = person_data
        if person_data and person_data['party'] and person_data['party']['id']:
            #if person_data['party']['id'] in pg_ids:
            authors.append(person_data['party']['id'])
            #else:
            #    print "ta pg ne obstaja zdj: ", person_data['party']['name']
        else:
            print "person nima mpstatic: ", question['author_id']

    avg = len(authors)/float(len(pg_ids))
    question_count = Counter(authors)
    max_value = 0
    max_orgs = []
    for maxi in question_count.most_common(90):
        if max_value == 0:
            max_value = maxi[1]
        if maxi[1] == max_value:
            max_orgs.append(maxi[0])
        else:
            break
    is_saved = []
    for pg_id in pg_ids:
        org = Organization.objects.get(id_parladata=pg_id)
        is_saved.append(saveOrAbortNew(model=NumberOfQuestions,
                                       created_for=date_of,
                                       organization=org,
                                       score=question_count[pg_id],
                                       average=avg,
                                       maximum=max_value,
                                       maxOrgs=max_orgs))

    return JsonResponse({"alliswell": True,
                         "saved": is_saved})


def getNumberOfQuestions(request, pg_id, date_=None):
    card = getPGCardModelNew(NumberOfQuestions,
                             pg_id,
                             date_)
    card_date = card.created_for.strftime(API_DATE_FORMAT)

    max_orgs = []
    for m_org in card.maxOrgs:
        org = Organization.objects.get(id_parladata=m_org)
        max_orgs.append(org.getOrganizationData())

    out = {
        'party': card.organization.getOrganizationData(),
        'created_at': card.created_at.strftime(API_DATE_FORMAT),
        'created_for': card_date,
        'results': {
            'max': {
                'score': card.maximum,
                'parties': max_orgs
            },
            'average': card.average,
            'score': card.score
        }
    }

    return JsonResponse(out, safe=False)


def getQuestions(request, person_id, date_=None):
    if date_:
        fdate = datetime.strptime(date_, '%d.%m.%Y')
        questions = Question.objects.objects.filter(person__id_parladata=person_id)
        questions = [[question for question in questions.filter(start_time__range=[t_date, t_date+timedelta(days=1)])] for t_date in questions.filter(start_time__lte=fdate).order_by('start_time').datetimes('start_time', 'day')]
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
            dayData['questions'].append({
                'session_name': question.session.name if question.session else 'Unknown',
                'question_id': question.id_parladata,
                'title': question.title,
                'recipient_text': question.recipient_text,
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


def getQuestionsOfPG1(request, pg_id, date_=False):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_ = date_of.strftime(API_DATE_FORMAT)

    end_of_day = date_of + timedelta(days=1)
    questions = Question.objects.filter(start_time__lt=end_of_day)

    membersOfPGRanges = reversed(tryHard(API_URL+'/getMembersOfPGsRanges' + ("/"+date_ if date_ else "")).json())
    out = []
    personsData = {}
    for pgMembersRange in membersOfPGRanges:
        startTime = datetime.strptime(pgMembersRange["start_date"], API_DATE_FORMAT)
        endTime = datetime.strptime(pgMembersRange["end_date"], API_DATE_FORMAT)+timedelta(hours=23, minutes=59)
        questionz = [[question
                      for question
                      in questions.filter(person__id_parladata__in=pgMembersRange["members"][pg_id],
                                          start_time__range=[t_date, t_date+timedelta(hours=23, minutes=59)]).order_by("-id_parladata")
                      ]
                     for t_date
                     in questions.filter(start_time__lt=endTime,
                                         start_time__gt=startTime,
                                         person__id_parladata__in=pgMembersRange["members"][pg_id]).datetimes('start_time', 'day')]
        for day in reversed(questionz):
            #dayData = {"date": day[0].start_time.strftime(API_OUT_DATE_FORMAT), "sessions":[]}
            dayDataDict = {"date": day[0].start_time.strftime(API_OUT_DATE_FORMAT), "questions": []}
            addedPersons = []
            addedSessions = []
            for question in day:
                person_id = question.person.id_parladata
                try:
                    personData = personsData[person_id]
                except KeyError as e:
                    personData = getPersonData(person_id, date_)
                    personsData[person_id] = personData
                questionData = question.getQuestionData()
                questionData.update({'person': personData})
                dayDataDict["questions"].append(questionData)

            out.append(dayDataDict)

    # WORKAROUND: created_at is today.
    result = {
        'results': out,
        'created_for': out[-1]["date"] if out else date_,
        'created_at': date_,
        'party': Organization.objects.get(id_parladata=pg_id).getOrganizationData(),
        }
    return JsonResponse(result, safe=False)


def getQuestionsOfPG(request, pg_id, date_=False):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        date_of = datetime.now().date()
        date_ = date_of.strftime(API_DATE_FORMAT)

    end_of_day = date_of + timedelta(days=1)
    questions = Question.objects.filter(start_time__lt=end_of_day)

    personsData = {}

    all_recipients = []

    membersOfPGRanges = reversed(tryHard(API_URL+'/getMembersOfPGsRanges' + ("/"+date_ if date_ else "")).json())
    i = 0
    out = []
    for pgMembersRange in membersOfPGRanges:
        startTime = datetime.strptime(pgMembersRange["start_date"], API_DATE_FORMAT)
        endTime = datetime.strptime(pgMembersRange["end_date"], API_DATE_FORMAT) + timedelta(hours=23, minutes=59)

        rangeQuestions = questions.filter(start_time__lt=endTime,
                                          start_time__gt=startTime,
                                          person__id_parladata__in=pgMembersRange["members"][pg_id])
        all_recipients += list(rangeQuestions.values_list('recipient_text',
                                                          flat=True))

        for t_date in rangeQuestions.datetimes('start_time', 'day').order_by("-start_time"):
            thisRangeQ = rangeQuestions.filter(start_time__range=[t_date, t_date+timedelta(hours=23, minutes=59)]).order_by('-start_time')
            questionsOnDate = []
            for question in thisRangeQ:
                i += 1
                persons_id = question.person.id_parladata
                try:
                    personData = personsData[persons_id]
                except KeyError as e:
                    personData = getPersonData(persons_id, date_)
                    personsData[persons_id] = personData
                questionData = question.getQuestionData()
                questionData.update({'person': personData})
                questionsOnDate.append(questionData)

            dayDataDict = {"date": t_date.strftime(API_OUT_DATE_FORMAT),
                           "questions": questionsOnDate}
            out.append(dayDataDict)
    print i
    # WORKAROUND: created_at is today.
    result = {
        'results': out,
        'created_for': out[-1]["date"] if out else date_,
        'created_at': date_,
        'party': Organization.objects.get(id_parladata=pg_id).getOrganizationData(),
        'all_authors': [pData for pData in personsData.values()],
        'all_recipients': list(set(all_recipients)),
        }
    return JsonResponse(result, safe=False)


def getListOfPGs(request, date_=None, force_render=False):
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
        key = date_
    else:
        date_of = datetime.now().date()
        date_=date_of.strftime(API_DATE_FORMAT)
        key = date_

    c_data = cache.get("pg_list_" + key)
    if c_data and not force_render:
        data = c_data
    else:
        allPGs = tryHard(API_URL+'/getAllPGsExt/').json().keys()
        pgs = tryHard(API_URL+'/getMembersOfPGsRanges/'+date_).json()[-1]["members"]
        data = []
        for pg, members in pgs.items():
            if pg in allPGs and members:
                pg_obj = {}
                pg_obj["results"] = {}
                pg_id = pg
                pg_obj["party"] = Organization.objects.get(id_parladata=pg).getOrganizationData()
                try:
                    pg_obj["results"]["presence_sessions"] = json.loads(getPercentOFAttendedSessionPG(None, pg_id, date_).content)["sessions"]["organization_value"]
                    pg_obj["results"]["presence_votes"] = json.loads(getPercentOFAttendedSessionPG(None, pg_id, date_).content)["votes"]["organization_value"]
                except:
                    pg_obj["results"]["presence_sessions"] = None
                    pg_obj["results"]["presence_votes"] = None

                try:
                    pg_obj["results"]["vocabulary_size"] = json.loads(getVocabularySize(None, pg_id, date_).content)["results"]["score"]
                except:
                    pg_obj["results"]["vocabulary_size"] = None
                try:
                    pg_obj["results"]["number_of_questions"] = json.loads(getNumberOfQuestions(None, pg_id, date_).content)["results"]["score"]
                except:
                    pg_obj["results"]["number_of_questions"] = None

                try:
                    styleScores = json.loads(getStyleScoresPG(None, pg_id, date_).content)
                except:
                    styleScores = None
                pg_obj["results"]["privzdignjeno"] = styleScores["results"]["privzdignjeno"] if styleScores else None
                pg_obj["results"]["preprosto"] = styleScores["results"]["preprosto"] if styleScores else None
                pg_obj["results"]["problematicno"] = styleScores["results"]["problematicno"] if styleScores else None
                pg_obj["results"]["seat_count"] = len(members)
                


                data.append(pg_obj)
        data = sorted(data, key=lambda k: k['results']["seat_count"], reverse=True)
        cache.set("pg_list_" + key, data, 60 * 60 * 48) 

    return JsonResponse({"data": data})


def setPresenceThroughTime(request, party_id, date_=None):
    if date_:
        fdate = datetime.strptime(date_, '%d.%m.%Y').date()
    else:
        fdate = datetime.now().date()

    url = API_URL + '/getBallotsCounterOfParty/' + party_id + '/' + fdate.strftime(API_DATE_FORMAT)
    data = tryHard(url).json()

    data_for_save = []

    for month in data:
        stats = month['ni'] + month['za'] + month['proti'] + month['kvorum']
        not_member = month['total'] - stats
        presence = float(stats-month['ni']) / stats if stats else 0
        data_for_save.append({'date_ts': month['date_ts'],
                              'presence': presence * 100,
                              })

    org = Organization.objects.get(id_parladata=party_id)
    saved = saveOrAbortNew(model=PresenceThroughTime,
                           organization=org,
                           created_for=fdate,
                           data=data_for_save)

    return JsonResponse({'alliswell': True, "status": 'OK', "saved": saved})


def getPresenceThroughTime(request, party_id, date_=None):
    card = getPGCardModelNew(PresenceThroughTime,
                             party_id,
                             date_)
    card_date = card.created_for.strftime(API_DATE_FORMAT)

    out = {
        'party': card.organization.getOrganizationData(),
        'created_at': card.created_at.strftime(API_DATE_FORMAT),
        'created_for': card_date,
        'results': card.data
    }

    return JsonResponse(out, safe=False)


def getIntraDisunion(request):
    out = {}
    votesData = {}
    tab = []
    ob =  {}
    obs =  {}
    dataOut =  {}
    paginator = Paginator(Vote.objects.all().order_by('start_time'), 50)                                                          
    page = request.GET.get('page', 1)
    try:
        votespag = paginator.page(page)
    except PageNotAnInteger:
        votespag = paginator.page(1)
    except EmptyPage:
        votespag = paginator.page(paginator.num_pages)
    
    for vote in votespag:
        votesData[vote.id_parladata] = {'text':vote.motion,
                                        'result':vote.result,
                                        'date':vote.start_time,
                                        'tag':vote.tags,
                                        'id_parladata':vote.id_parladata}
    
    for vote in votespag:
        intraD = vote.vote_intradisunion.all()
        for intra in intraD:
            if intra.organization.acronym in out.keys():
                obs = votesData[vote.id_parladata].copy()
                obs['maximum'] = intra.maximum
                out[intra.organization.acronym]['votes'].append(obs)
            else:
                obj = votesData[vote.id_parladata].copy()
                obj['maximum'] = intra.maximum
                ob['organization'] = intra.organization.getOrganizationData()
                ob['votes'] = []
                ob['votes'].append(obj)
                out[intra.organization.acronym] = ob
                ob = {}
        tab.append({'text':vote.motion,
                    'result':vote.result,
                    'date':vote.start_time,
                    'tag':vote.tags,
                    'maximum':vote.intra_disunion,
                    'id_parladata':vote.id_parladata})

    out['DZ'] = {'organization': 'dz',
                 'votes': tab}
    dataOut['results'] = out
    dataOut['all_tags'] = list(Tag.objects.all().values_list('name', flat=True))
    return JsonResponse(dataOut, safe=False)


def getIntraDisunionOrg(request, org_id, force_render=False):
    out = {}
    votesData = {}
    ob = {}
    obj = {}
    ob['votes'] = []
    tab = []
    votes = Vote.objects.all().order_by('start_time')                               
    for vote in votes:
        votesData[vote.id_parladata] = {'text':vote.motion,
                                        'result':vote.result,
                                        'date':vote.start_time,
                                        'tag':vote.tags,
                                        'id_parladata':vote.id_parladata}

    c_data = cache.get("pg_disunion" + org_id)
    if c_data and not force_render:
        out = c_data
    else:
        if int(org_id) == 95:
            for vote in votes:
                tab.append({'text':vote.motion,
                             'result':vote.result,
                             'date':vote.start_time,
                             'tag':vote.tags,
                             'maximum':vote.intra_disunion})
                out['DZ'] = {'organization': 'dz',
                             'votes': tab}
            out['all_tags'] = list(Tag.objects.all().values_list('name', flat=True))
            cache.set("pg_disunion" + org_id, out, 60 * 60 * 48) 
        else:
            for vote in votes:
                intraD = IntraDisunion.objects.filter(vote=vote,
                                                      organization__id_parladata=org_id)
                for intra in intraD:
                    obj = votesData[vote.id_parladata].copy()
                    obj['maximum'] = intra.maximum
                    ob['votes'].append(obj)
                    ob['organization'] = Organization.objects.get(id_parladata=org_id).getOrganizationData()
                out[Organization.objects.get(id_parladata=org_id).acronym] = ob
            out['all_tags'] = list(Tag.objects.all().values_list('name', flat=True))
            cache.set("pg_disunion" + org_id, out, 60 * 60 * 48) 
    
    return JsonResponse(out, safe=False)
