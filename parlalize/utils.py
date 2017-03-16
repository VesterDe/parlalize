# -*- coding: UTF-8 -*-
import numpy
from datetime import datetime, timedelta
from django.http import Http404, JsonResponse, HttpResponse
import requests
from parlaposlanci.models import Person, StyleScores, CutVotes, MPStaticPL, MembershipsOfMember, LessEqualVoters, EqualVoters, Presence, AverageNumberOfSpeechesPerSession, VocabularySize, Compass, SpokenWords, LastActivity
from parlaskupine.models import Organization, WorkingBodies, CutVotes as CutVotesPG, DeviationInOrganization, LessMatchingThem, MostMatchingThem, PercentOFAttendedSession, MPOfPg, PGStatic, VocabularySize as VocabularySizePG, StyleScores as StyleScoresPG
from parlaseje.models import Session, Vote, Ballot, Speech, Tag, PresenceOfPG, AbsentMPs, AverageSpeeches, Vote_graph
from parlalize.settings import VOTE_MAP, API_URL, BASE_URL, API_DATE_FORMAT, DEBUG
from django.contrib.contenttypes.models import ContentType
import requests
import json
import numpy as np
import time
import csv
from django.core.cache import cache


def tryHard(url):
    data = None
    counter = 0
    while data is None:
        try:
            if counter > 10:
                client.captureMessage(url+' je zahinavu več ko 10x.')
                return
            data = requests.get(url)
        except:
            counter += 1
            time.sleep(30)
            pass
    return data


def voteToLogical(vote):
    if vote == 'za':
        return 1
    elif vote == 'proti':
        return 0
    else:
        return -1


# Return dictionary of votes results by user ids.
def getLogicVotes(date_=None):
    if date_:
        r = tryHard(API_URL+'/getVotes/'+date_)
        v = tryHard(API_URL+'/getAllVotes/'+date_)
    else:
        r = tryHard(API_URL+'/getVotes/')
        v = tryHard(API_URL+'/getAllVotes/')
    pl_votes = v.json()
    votes = r.json()

    niPoslanec = VOTE_MAP['ni_poslanec']

    for person_id in votes.keys():
        for vote in pl_votes:
            try:
                logic_vote = VOTE_MAP[str(votes[str(person_id)][str(vote['id'])])]
                votes[str(person_id)][str(vote['id'])] = logic_vote
            except:
                if type(votes[str(person_id)]) == list:
                    votes[str(person_id)] = {}
                votes[str(person_id)][str(vote['id'])] = niPoslanec

    return votes


def getVotes():
    r = tryHard(API_URL + '/getVotes/')
    pl_votes = Vote.objects.all()
    votes = r.json()
    for person_id in votes.keys():
        for vote in pl_votes:
            try:
                if not votes[str(person_id)][str(vote.id_parladata)]:
                    print 'bu'
            except:
                if type(votes[str(person_id)]) == list:
                    votes[str(person_id)] = {}
                votes[str(person_id)][str(vote.id_parladata)] = 'ni_poslanec'
    return votes


def votesToLogical(votes, length):
    maxVotes = length
    for key in votes.keys():
        votes[key] = map(voteToLogical, votes[key])
        if (len(votes[key]) < length):
            votes[key].extend(numpy.zeros(maxVotes-int(len(votes[key]))))
        else:

            votes[key] = [votes[key][i] for i in range(length)]


def voteFor(vote):
    if vote == 'za':
        return 1
    else:
        return 0


def voteAgainst(vote):
    if vote == 'proti':
        return 1
    else:
        return 0


def voteAbstain(vote):
    if vote == 'kvorum':
        return 1
    else:
        return 0


def voteAbsent(vote):
    if vote == 'ni':
        return 1
    else:
        return 0


def normalize(val, max_):
    try:
        return round((float(val)*100)/float(max_))
    except:
        return val


# checks if cards with the data exists or not
def saveOrAbort(model, **kwargs):
    savedModel = model.objects.filter(**kwargs)
    if savedModel:
        # Add cards which has always uninqe data
        if model != LastActivity:
            lastModel = model.objects.latest('created_at')
            if savedModel.latest('created_at').id != lastModel.id:
                newModel = model(**kwargs)
                newModel.save()
                return True
        else:
            return False
    else:
        newModel = model(**kwargs)
        newModel.save()
        return True
    return False


def saveOrAbortNew(model, **kwargs):
    # checks if cards with the data exists or not NEW
    """
    usage:
        watch parlaposlanci/views.py:setMembershipsOfMember

        if you use saveOrAbortNew in setter you need to use
        getPersonCardModelNew in getter
    """
    def save_it(model, created_for, **kwargs):
        kwargs.update({'created_for': created_for})
        newModel = model(**kwargs)
        newModel.save()
        return True
    if model != LastActivity:
        created_for = kwargs.pop('created_for')
    # print kwargs
    savedModel = model.objects.filter(**kwargs)

    if savedModel:
        if 'person' in kwargs:
            if model != LastActivity:
                person_id = kwargs['person'].id_parladata
                cards = model.objects.filter(person__id_parladata=person_id,
                                             created_for__lte=created_for)
                lastDate = cards.latest('created_for').created_for
                if savedModel.latest('created_for').created_for != lastDate:
                    save_it(model, created_for, **kwargs)

        elif 'organization' in kwargs:
            party_id = kwargs['organization'].id_parladata
            models = model.objects.filter(organization__id_parladata=party_id,
                                          created_for__lte=created_for)
            if models:
                # if allready exist write in DB for thiw PG
                lastDate = models.latest('created_for').created_for
                if savedModel.latest('created_for').created_for != lastDate:
                    save_it(model, created_for, **kwargs)
            else:
                save_it(model, created_for, **kwargs)

        elif 'session' in kwargs:
            ses_id = kwargs['session'].id_parladata
            models = model.objects.filter(session__id_parladata=ses_id)
            lastDate = models.latest('created_at').created_for
            if savedModel.latest('created_for').created_for != lastDate:
                save_it(model, created_for, **kwargs)
    else:
        if model != LastActivity:
            kwargs.update({'created_for': created_for})
        newModel = model(**kwargs)
        newModel.save()
        return True
    return False


def findDatesFromLastCard(model, id, lastParsedDate, minDate=None):
    toDate = datetime.strptime(lastParsedDate, '%d.%m.%Y').date()

    print model._meta.app_label
    try:
        if model._meta.app_label == 'parlaposlanci':
            models = model.objects.filter(person__id_parladata=id)
            lastCardDate = models.order_by('-created_for')[0].created_for
        elif model._meta.app_label == 'parlaskupine':
            models = model.objects.filter(organization__id_parladata=id)
            lastCardDate = models.order_by('-created_for')[0].created_for
        elif model._meta.app_label == 'parlaseje':
            models = model.objects.all()
            lastCardDate = models.order_by('-created_for')[0].created_for
    except:
        lastCardDate = datetime.strptime('02.08.2014', '%d.%m.%Y').date()
    # lastCardDate = lastCardDate.replace(tzinfo=None)
    if minDate:
        od = datetime.strptime(minDate, '%d.%m.%Y').date()
        lastCardDate = datetime.strptime(minDate, '%d.%m.%Y').date()
        if od > lastCardDate:
            lastCardDate = od

    return [(lastCardDate+timedelta(days=days))
            for days
            in range((toDate-lastCardDate).days)]


def datesGenerator(stDate, toDate):
    dates = [(stDate + timedelta(days=x))
             for x
             in range(0, (toDate - stDate).days)]
    return dates


def getPersonCardModelNew(model, id, date=None, is_visible=None):
    if date:
        dateObj = datetime.strptime(date, '%d.%m.%Y')
        modelObject = model.objects.filter(person__id_parladata=id,
                                           created_for__lte=dateObj)
    else:
        modelObject = model.objects.filter(person__id_parladata=id,
                                           created_for__lte=datetime.now())
    if is_visible:
        modelObject = modelObject.filter(is_visible=True)

    if not modelObject:
        # if model == LastActivity:
            # return None
        if DEBUG:
            raise Http404('Nismo našli kartice' + str(model)+str(id))
        else:
            raise Http404('Nismo našli kartice')
    else:
        if model == LastActivity:
            latest_day = modelObject.latest('created_for').created_for
            print latest_day
            if len(modelObject.filter(created_for=latest_day)) > 1:
                models = modelObject.filter(created_for=latest_day)
                modelObject = models.latest('created_at')
            else:
                modelObject = modelObject.latest('created_for')
        else:
            date = modelObject.latest('created_for').created_for
            models = modelObject.filter(created_for=date)
            modelObject = models.latest('created_at')
            # modelObject = modelObject.latest('created_for')
    return modelObject


def getPersonCardModel(model, id, date=None):
    if date:
        dateObj = datetime.strptime(date, '%d.%m.%Y')
        if model == LastActivity:
            modelObject = model.objects.filter(person__id_parladata=id,
                                               date__lte=dateObj)
        else:
            dateObj
            modelObject = model.objects.filter(person__id_parladata=id,
                                               created_at__lte=dateObj)
    else:
        if model == LastActivity:
            modelObject = model.objects.filter(person__id_parladata=id,
                                               date__lte=datetime.now())
        else:
            modelObject = model.objects.filter(person__id_parladata=id,
                                               created_at__lte=datetime.now())
    if not modelObject:
        if model == LastActivity:
            return None
        raise Http404('Nismo našli kartice')
    else:
        if model == LastActivity:
            modelObject = modelObject.latest('date')
        else:
            modelObject = modelObject.latest('created_at')
    return modelObject


def getPGCardModel(model, id, date=None):
    if date:
        dateObj = datetime.strptime(date, '%d.%m.%Y')
        modelObject = model.objects.filter(organization__id_parladata=id,
                                           created_at__lte=dateObj)
    else:
        modelObject = model.objects.filter(organization__id_parladata=id,
                                           created_at__lte=datetime.now())
    if not modelObject:
        raise Http404('Nismo našli kartice')
    else:
        modelObject = modelObject.latest('created_at')
    return modelObject


def getPGCardModelNew(model, id, date=None, is_visible=None):
    if date:
        dateObj = datetime.strptime(date, '%d.%m.%Y')
        modelObject = model.objects.filter(organization__id_parladata=id,
                                           created_for__lte=dateObj)
    else:
        modelObject = model.objects.filter(organization__id_parladata=id,
                                           created_for__lte=datetime.now())

    if is_visible:
        modelObject = modelObject.filter(is_visible=True)

    if not modelObject:
        # if model == LastActivity:
            # return None
        raise Http404('Nismo našli kartice')
    else:
        date = modelObject.latest('created_for').created_for
        modelObject = modelObject.filter(created_for=date).latest('created_at')
    return modelObject


def getSCardModel(model, id_se, date=None):
    if date:
        dateObj = datetime.strptime(date, '%d.%m.%Y')
        modelObject = model.objects.filter(id_parladata=id_se,
                                           created_at__lte=dateObj)
    else:
        modelObject = model.objects.filter(id_parladata=id_se,
                                           created_at__lte=datetime.now())
    if not modelObject:
        raise Http404('Nismo našli kartice')
    else:
        modelObject = modelObject.latest('created_at')
    return modelObject


# get all parliament member ID's
def getIDs():
    # create persons
    result = []
    # getAllPeople
    data = tryHard(API_URL+'/getAllPeople').json()
    # data = tryHard(API_URL+'/getMPs').json()

    for mp in data:
        result.append(mp['id'])

    return result


# get all PG ID's
def getPGIDs():
    data = tryHard(API_URL+'/getAllPGsExt/').json()

    return [pg for pg in data]


def getRangeVotes(pgs, date_, votes_type='logic'):
    def getVotesOnDay(votesPerDay_, day):
        # tempList = sorted(votesPerDay_, key=lambda k: k['time'])
        if day in votesPerDay_.keys():
            votesPerDay_[day].sort(key=lambda r: r['time'])
        else:
            return []
        try:
            out = [a['id'] for a in votesPerDay_[day]]
            return out
        except:
            return []

    # get data
    r = tryHard(API_URL+'/getMembersOfPGsOnDate/'+date_)
    membersInPGs = r.json()

    r = tryHard(API_URL+'/getMembersOfPGsRanges/'+date_)
    membersInPGsRanges = r.json()

    # create dict votesPerDay
    r = tryHard(API_URL+'/getAllVotes/'+date_)
    allVotesData = r.json()

    if date_:
        if votes_type == 'logic':
            votes = getLogicVotes(date_)
        else:
            r = tryHard(API_URL+'/getVotes/'+date_)
            votes = r.json()

        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        if votes_type == 'logic':
            votes = getLogicVotes()
        else:
            r = tryHard(API_URL+'/getVotes/'+date_)
            votes = r.json()
        date_of = datetime.now().date()

    # print votes
    # prepare votes in 'windows'
    votesPerDay = {}
    for vote in allVotesData:
        vote_date = vote['start_time'].split('T')[0]
        if vote_date in votesPerDay.keys():
            dateObj = datetime.strptime(vote['start_time'], '%Y-%m-%dT%X')
            votesPerDay[vote_date].append({'id': vote['id'],
                                           'time': dateObj})
        else:
            dateObj = datetime.strptime(vote['start_time'], '%Y-%m-%dT%X')
            votesPerDay[vote_date] = [{'id': vote['id'],
                                       'time': dateObj}]

    # get average score of PG
    if votes_type == 'logic':
        pg_score = np.array([])
    else:
        pg_score = []
    counter = 0
    all_votes = []
    for membersInRange in membersInPGsRanges:
        if len(pgs) == 1 and not membersInRange['members'][str(pgs[0])]:
            continue
        start_date = datetime.strptime(membersInRange['start_date'],
                                       API_DATE_FORMAT).date()
        end_date = datetime.strptime(membersInRange['end_date'],
                                     API_DATE_FORMAT).date()
        days = (end_date - start_date).days
        votes_ids = [vote_id
                     for i
                     in range(days+1)
                     for vote_id
                     in getVotesOnDay(votesPerDay,
                                      (start_date+timedelta(days=i)).strftime('%Y-%m-%d'))]
        if votes_ids == []:
            continue
        all_votes = all_votes + votes_ids
        counter += len(votes_ids)
        if votes_type == 'logic':
            pg_score_temp = np.mean([[votes[str(member)][str(b)]
                                      for b
                                      in votes_ids
                                      ]
                                     for pg_id
                                     in pgs
                                     for member
                                     in membersInRange['members'][pg_id]],
                                    axis=0)
        else:
            members = [member
                       for pg_id
                       in pgs
                       for member
                       in membersInRange['members'][pg_id]]

            # print member, votes[str(member)].keys()
            # Print member and vote id where is fail in data for cutVotes
            for member in members:
                for b in votes_ids:
                    if str(b) not in votes[str(member)].keys():
                        print member, b, 'FAIL'
                        # fix for cutVotes for members which isn't member for a half of day
                        if votes_type == 'plain':
                            votes[str(member)][str(b)] = 'X'
            pg_score_temp = [votes[str(member)][str(b)]
                             for member
                             in members
                             for b
                             in votes_ids if votes[str(member)][str(b)] != 'X']

        if votes_type == 'logic':
            pg_score = np.concatenate((pg_score,
                                       pg_score_temp),
                                      axis=0)
        else:
            pg_score = pg_score+pg_score_temp

    return pg_score, membersInPGs, votes, all_votes


def getMPGovId(id_parladata):
    person = Person.objects.filter(id_parladata=id_parladata)[0]
    out = {'id': person.id_parladata,
           'gov_id': person.gov_id}
    return out


def getPersonData(id_parladata, date_=None):
    if not date_:
        date_ = datetime.now().strftime(API_DATE_FORMAT)
    try:
        data = getPersonCardModelNew(MPStaticPL, id_parladata, date_)
    except:
        url = API_URL + '/getPersonData/' + str(id_parladata) + '/'
        guest = tryHard(url).json()
        gov_id = None
        if guest and guest['gov_id']:
            return {
                'type': 'visitor' if guest else 'unknown',
                'party': {'acronym': None,
                          'id': None,
                          'name': None,
                          'is_coalition': None},
                'name': guest['name'] if guest else None,
                'gov_id': guest['gov_id'],
                'id': id_parladata,
                'district': None,
                'gender': None,
                'is_active': None,
                'has_function': False,
                }
        else:
            return {'type': 'visitor' if guest else 'unknown',
                    'party': {'acronym': None,
                              'id': None,
                              'name': None,
                              'is_coalition': None},
                    'name': guest['name'] if guest else None,
                    'gov_id': None,
                    'id': id_parladata,
                    'district': None,
                    'gender': None,
                    'is_active': None,
                    'has_function': False,
                    }
    party = Organization.objects.get(id_parladata=data.party_id)
    partyData = party.getOrganizationData()
    return {
            'type': 'mp',
            'name': data.person.name,
            'id': int(data.person.id_parladata),
            'gov_id': data.gov_id,
            'party': partyData,
            'gender': data.gender,
            'district': data.district,
            'is_active': True if data.person.actived == 'True' else False,
            'has_function': data.person.has_function,
        }


def getPersonDataAPI(request, id_parladata, date_=None):
    data = getPersonData(id_parladata, date_)
    return JsonResponse(data)


def modelsData(request):
    out = []
    for ct in ContentType.objects.all():
        m = ct.model_class()

        out.append({'model': m.__module__,
                    'Ime modela': m.__name__,
                    'st:': m._default_manager.count()})
    return JsonResponse(out, safe=False)


def getAllStaticData(request, force_render=False):

    date_of = datetime.now().date()
    date_ = date_of.strftime(API_DATE_FORMAT)

    c_data = cache.get('all_statics')
    if c_data and not force_render:
        out = c_data
    else:

        PS_NP = ['poslanska skupina', 'nepovezani poslanec']
        date_ = datetime.now().strftime(API_DATE_FORMAT)

        out = {'persons': {}, 'partys': {}, 'wbs': {}}
        for person in Person.objects.all():
            personData = getPersonData(person.id_parladata,
                                       date_)
            out['persons'][person.id_parladata] = personData

        parliamentary_group = Organization.objects.filter(classification__in=PS_NP)
        for party in parliamentary_group:
            out['partys'][party.id_parladata] = party.getOrganizationData()

        working_bodies = ['odbor', 'komisija', 'preiskovalna komisija']
        orgs = Organization.objects.filter(classification__in=working_bodies)
        out['wbs'] = [{'id': org.id_parladata,
                       'name': org.name} for org in orgs]

        cache.set('all_statics', out, 60 * 60 * 48)

    return JsonResponse(out)


def checkSessions():
    ses = tryHard(API_URL + '/getSessions/').json()
    sessions = [s['id'] for s in ses]
    ballots = [s.vote.id_parladata for s in Ballot.objects.all()]
    motionIDs = []
    for id_se in sessions:
        url = API_URL + '/motionOfSession/' + str(id_se) + '/'
        if len(tryHard(url).json()) > 0:
            motionIDs.append(id_se)
    print 'Vsa glasovanja: ', len(motionIDs)

    if len(Session.objects.all()) > 0:
        print 'Seje katerih ni v parlalizah: ', list(set(sessions) - set(Session.objects.values_list('id_parladata', flat=True)))
    else:
        print 'ni sej sploh'

    if len(Vote.objects.all()) > 0:
        print 'Vote katerih ni v parlalizah: ', list(set(motionIDs) - set(Vote.objects.values_list('id_parladata', flat=True)))
    else:
        print 'ni votov sploh'

    if len(Vote_graph.objects.all()) > 0:
        print 'Vote graph katerih ni v parlalizah: ', list(set(motionIDs) - set(Vote_graph.objects.all().values_list('vote__id_parladata', flat=True)))
    else:
        print 'ni votov grafov sploh'

    if len(PresenceOfPG.objects.all()) > 0:
        print 'stevilo PresenceOfPG: ', len(PresenceOfPG.objects.all())
    else:
        print 'ni PresenceOfPG sploh'

    if len(AverageSpeeches.objects.all()) > 0:
        print 'stevilo AverageSpeeches: ', len(AverageSpeeches.objects.all())
    else:
        print 'ni AverageSpeeches sploh'

    if len(AbsentMPs.objects.all()) > 0:
        print 'stevilo AbsentMPs: ', len(AbsentMPs.objects.all())
    else:
        print 'ni AbsentMPs sploh'


def checkPG():
    org = [int(i) for i in (tryHard(API_URL+'/getAllOrganizations').json()).keys()]
    pg = [int(i) for i in (tryHard(API_URL+'/getAllPGs').json()).keys()]

    if len(Organization.objects.all()) > 0:
        print 'Organizacij katerih ni v parlalizah: ', list(set(org) - set(Organization.objects.values_list('id_parladata', flat=True)))
    else:
        print 'ni sej sploh'

    if len(PGStatic.objects.all()) > 0:
        print 'PGStatic: za te PG ni kartice: ', list(set(pg) - set(PGStatic.objects.values_list('organization__id_parladata', flat=True)))
    else:
        print 'ni PGStatic sploh'

    if len(PercentOFAttendedSession.objects.all()) > 0:
        print 'PercentOFAttendedSession: za te PG ni kartice: ', list(set(pg) - set(PercentOFAttendedSession.objects.values_list('organization__id_parladata', flat=True)))
    else:
        print 'ni PercentOFAttendedSession sploh'

    if len(MPOfPg.objects.all()) > 0:
        print 'MPOfPg: za te PG ni kartice: ', list(set(pg) - set(MPOfPg.objects.values_list('organization__id_parladata', flat=True)))
    else:
        print 'ni MPOfPg sploh'

    if len(MostMatchingThem.objects.all()) > 0:
        print 'MostMatchingThem: za te PG ni kartice: ', list(set(pg) - set(MostMatchingThem.objects.values_list('organization__id_parladata', flat=True)))
    else:
        print 'ni MostMatchingThem sploh'

    if len(LessMatchingThem.objects.all()) > 0:
        print 'LessMatchingThem: za te PG ni kartice: ', list(set(pg) - set(LessMatchingThem.objects.values_list('organization__id_parladata', flat=True)))
    else:
        print 'ni LessMatchingThem sploh'

    if len(DeviationInOrganization.objects.all()) > 0:
        print 'DeviationInOrganization: za te PG ni kartice: ', list(set(pg) - set(DeviationInOrganization.objects.values_list('organization__id_parladata', flat=True)))
    else:
        print 'ni DeviationInOrganization sploh'

    if len(CutVotes.objects.all()) > 0:
        print 'CutVotes: za te PG ni kartice: ', list(set(pg) - set(CutVotes.objects.values_list('organization__id_parladata', flat=True)))
    else:
        print 'ni CutVotes sploh'

    if len(VocabularySize.objects.all()) > 0:
        print 'VocabularySize: za te PG ni kartice: ', list(set(pg) - set(VocabularySize.objects.values_list('organization__id_parladata', flat=True)))
    else:
        print 'ni VocabularySize sploh'

def checkMP():
    mps = [i['id'] for i in tryHard(API_URL+'/getMPs').json()]

    print mps

    if len(Person.objects.all()) > 0:
        print 'Poslancev katerih ni v parlalizah: ', list(set(mps) - set(Person.objects.values_list('id_parladata', flat=True)))
    else:
        print 'ni sej sploh'
    
    if len(Presence.objects.all()) > 0:
        print 'Presence: za te MP ni kartice: ', list(set(mps) - set(Presence.objects.values_list('person__id_parladata', flat=True)))
    else:
        print 'ni Presence sploh'

    if len(SpokenWords.objects.all()) > 0:
        print 'SpokenWords: za te MP ni kartice: ', list(set(mps) - set(SpokenWords.objects.values_list('person__id_parladata', flat=True)))
    else:
        print 'ni SpokenWords sploh'

    if len(SpeakingStyle.objects.all()) > 0:
        print 'SpeakingStyle: za te MP ni kartice: ', list(set(mps) - set(SpeakingStyle.objects.values_list('person__id_parladata', flat=True)))
    else:
        print 'ni SpeakingStyle sploh'

    #if len(CutVotes.objects.all()) > 0:
    #    print 'CutVotes: za te MP ni kartice: ', list(set(mps) - set(CutVotes.objects.values_list('person__id_parladata', flat=True)))
    #else:
    #    print 'ni CutVotes sploh'

    if len(LastActivity.objects.all()) > 0:
        print 'LastActivity: za te MP ni kartice: ', list(set(mps) - set(LastActivity.objects.values_list('person__id_parladata', flat=True)))
    else:
        print 'ni LastActivity sploh'

    if len(EqualVoters.objects.all()) > 0:
        print 'EqualVoters: za te MP ni kartice: ', list(set(mps) - set(EqualVoters.objects.values_list('person__id_parladata', flat=True)))
    else:
        print 'ni EqualVoters sploh'

    if len(LessEqualVoters.objects.all()) > 0:
        print 'LessEqualVoters: za te MP ni kartice: ', list(set(mps) - set(LessEqualVoters.objects.values_list('person__id_parladata', flat=True)))
    else:
        print 'ni LessEqualVoters sploh'

    if len(MPsWhichFitsToPG.objects.all()) > 0:
        print 'MPsWhichFitsToPG: za te MP ni kartice: ', list(set(mps) - set(MPsWhichFitsToPG.objects.values_list('person__id_parladata', flat=True)))
    else:
        print 'ni MPsWhichFitsToPG sploh'

    if len(MPStaticPL.objects.all()) > 0:
        print 'MPStaticPL: za te MP ni kartice: ', list(set(mps) - set(MPStaticPL.objects.values_list('person__id_parladata', flat=True)))
    else:
        print 'ni MPStaticPL sploh'
    #if len(MPStaticGroup.objects.all()) > 0:
    #    print 'MPStaticGroup: za te MP ni kartice: ', list(set(mps) - set(MPStaticGroup.objects.values_list('person__id_parladata', flat=True)))
    #else:
    #    print 'ni MPStaticGroup sploh'

    if len(NumberOfSpeechesPerSession.objects.all()) > 0:
        print 'NumberOfSpeechesPerSession: za te MP ni kartice: ', list(set(mps) - set(NumberOfSpeechesPerSession.objects.values_list('person__id_parladata', flat=True)))
    else:
        print 'ni NumberOfSpeechesPerSession sploh'

    #if len(VocabularySize.objects.all()) > 0:
    #    print 'VocabularySize: za te MP ni kartice: ', list(set(mps) - set(VocabularySize.objects.values_list('person__id_parladata', flat=True)))
    #else:
    #    print 'ni VocabularySize sploh'

    if len(AverageNumberOfSpeechesPerSession.objects.all()) > 0:
        print 'AverageNumberOfSpeechesPerSession: za te MP ni kartice: ', list(set(mps) - set(AverageNumberOfSpeechesPerSession.objects.values_list('person__id_parladata', flat=True)))
    else:
        print 'ni AverageNumberOfSpeechesPerSession sploh'

    #if len(Compass.objects.all()) > 0:
    #    print 'Compass: za te MP ni kartice: ', list(set(mps) - set(Compass.objects.values_list('person__id_parladata', flat=True)))
    #else:
    #    print 'ni Compass sploh'

    if len(TaggedBallots.objects.all()) > 0:
        print 'TaggedBallots: za te MP ni kartice: ', list(set(mps) - set(TaggedBallots.objects.values_list('person__id_parladata', flat=True)))
    else:
        print 'ni TaggedBallots sploh'

    if len(MembershipsOfMember.objects.all()) > 0:
        print 'MembershipsOfMember: za te MP ni kartice: ', list(set(mps) - set(MembershipsOfMember.objects.values_list('person__id_parladata', flat=True)))
    else:
        print 'ni MembershipsOfMember sploh'


def getPersonsCardDates(request, person_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = ('attachment; filename="'
                                       '' + str(person_id) + ''
                                       '.csv"')

    mems = tryHard(API_URL + '/getAllTimeMemberships').json()
    member_dates = [mem for mem in mems if str(mem['id']) == person_id]

    dates = {}
    dates['is_member'] = []
    for d in member_dates:
        if d['start_time']:
            start = datetime.strptime(d['start_time'].split('T')[0],
                                      '%Y-%m-%d')
        else:
            start = datetime(day=1, month=8, year=2014)
        if d['end_time']:
            end = datetime.strptime(d['end_time'].split('T')[0],
                                    '%Y-%m-%d')
        else:
            end = datetime.today()
        while end > start:
            dates['is_member'].append(start.strftime(API_DATE_FORMAT))
            start = start+timedelta(days=1)

    models = {'spoken': SpokenWords,
              'presence': Presence,
              'style': StyleScores,
              'equal': EqualVoters,
              'less_equal': LessEqualVoters,
              'static': MPStaticPL,
              'number_of_speeches': AverageNumberOfSpeechesPerSession,
              'memberships': MembershipsOfMember,
              'last_activity': LastActivity,
              'vocabolary_size': VocabularySize,
              }

    for key, model in models:
        modelz = model.objects.filter(person__id_parladata=person_id)
        datez = modelz.order_by('created_for').values_list('created_for',
                                                           flat=True)
        dates[key] = [day.strftime(API_DATE_FORMAT) for day in datez]

    writer = csv.writer(response)
    keys = dates.keys()
    writer.writerow(['Date']+keys)
    date = datetime(day=1, month=8, year=2014)
    while date < datetime.today():
        print date
        strDate = date.strftime(API_DATE_FORMAT)
        writer.writerow([strDate]+['Yes' if strDate in dates[key] else ''
                                   for key in keys])
        date = date + timedelta(days=1)

    return response


def getOrgsCardDates(request, org_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = ('attachment; filename="'
                                       '' + str(org_id) + ''
                                       '.csv"')

    dates = {}

    models = {'PGStatic': PGStatic,
              'PercentOFAttendedSession': PercentOFAttendedSession,
              'MPOfPg': MPOfPg,
              'MostMatchingThem': MostMatchingThem,
              'LessMatchingThem': LessMatchingThem,
              'DeviationInOrganization': DeviationInOrganization,
              'vocabulary_size': VocabularySizePG,
              'style_scores': StyleScoresPG,
              }
    for key, model in models:
        modelz = model.objects.filter(organization__id_parladata=org_id)
        datez = modelz.order_by('created_for').values_list('created_for',
                                                           flat=True)
        dates[key] = [day.strftime(API_DATE_FORMAT) for day in datez]

    datez = static.order_by('created_for').values_list('created_for',
                                                       flat=True)

    writer = csv.writer(response)
    keys = dates.keys()
    writer.writerow(['Date']+keys)
    date = datetime(day=1, month=8, year=2014)
    while date < datetime.today():
        print date
        strDate = date.strftime(API_DATE_FORMAT)
        writer.writerow([strDate]+['Yes' if strDate in dates[key] else ''
                                   for key in keys])
        date = date + timedelta(days=1)

    return response


def monitorMe(request):

    r = requests.get('https://analize.parlameter.si/v1/p/getMPStatic/2/')
    if r.status_code == 200:
        return HttpResponse('All iz well.')
    else:
        return HttpResponse('PANIC!')


def printProgressBar(iteration,
                     total,
                     prefix='',
                     suffix='',
                     decimals=1,
                     length=100,
                     fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r' + prefix + '|' + bar + '|' + percent + suffix + '\r')
    # Print New Line on Complete
    if iteration == total:
        print()
