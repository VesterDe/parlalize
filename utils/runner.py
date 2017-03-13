# -*- coding: utf-8 -*-

import requests
from parlaposlanci.views import setMPStaticPL
from parlalize.settings import API_URL, API_DATE_FORMAT, BASE_URL
from parlalize.utils import getPGIDs, findDatesFromLastCard
from datetime import datetime, timedelta
from django.apps import apps
from parlaposlanci.models import District
from raven.contrib.django.raven_compat.models import client


from parlaposlanci.views import setCutVotes, setStyleScoresALL, setMPStaticPL, setMembershipsOfMember, setLessEqualVoters, setMostEqualVoters, setPercentOFAttendedSession, setLastActivity, setAverageNumberOfSpeechesPerSessionAll, setVocabularySizeAndSpokenWords, setCompass, getListOfMembers, setTFIDF, getSlugs, setListOfMembersTickers, setPresenceThroughTime
from parlaposlanci.models import Person, StyleScores, CutVotes, VocabularySize, MPStaticPL, MembershipsOfMember, LessEqualVoters, EqualVoters, Presence, AverageNumberOfSpeechesPerSession, VocabularySize, Compass

from parlaskupine.views import setCutVotes as setCutVotesPG, setDeviationInOrg, setLessMatchingThem, setMostMatchingThem, setPercentOFAttendedSessionPG, setMPsOfPG, setBasicInfOfPG, setWorkingBodies, setVocabularySizeALL, setStyleScoresPGsALL, setTFIDF as setTFIDFpg, getListOfPGs, setPresenceThroughTime as setPresenceThroughTimePG
from parlaskupine.models import Organization, WorkingBodies, CutVotes as CutVotesPG, DeviationInOrganization, LessMatchingThem, MostMatchingThem, PercentOFAttendedSession, MPOfPg, PGStatic, VocabularySize as VocabularySizePG, StyleScores as StyleScoresPG

from parlaseje.models import Session, Vote, Ballot, Speech, Question, Tag, PresenceOfPG, AbsentMPs, AverageSpeeches, Vote_graph
from parlaseje.views import setPresenceOfPG, setAbsentMPs, setSpeechesOnSession, setMotionOfSessionGraph, getSessionsList, setMotionOfSession
from parlaseje.utils import idsOfSession, getSesDates
from utils.recache import updatePagesS
from utils.imports import update
from multiprocessing import Pool

from parlalize.utils import tryHard, datesGenerator, printProgressBar
import json

from time import time

DZ = 95


# parlaposlanci runner methods #


def updateMPStatic():
    memberships = tryHard(API_URL + '/getMembersOfPGsRanges/').json()
    lastObject = {'members': {}}
    print '[info] update MP static'
    for change in memberships:
        # call setters for new pg
        for pg in list(set(change['members'].keys()) - set(lastObject['members'].keys())):
            for member in change['members'][pg]:
                setMPStaticPL(None, str(member), change['start_date'])

        # call setters for members which have change in memberships
        for pg in change['members'].keys():
            if pg in lastObject['members'].keys():
                personsForUpdate = list(set(change['members'][pg]) - set(lastObject['members'][pg]))
                for member in personsForUpdate:
                    setMPStaticPL(None, str(member), change['start_date'])
        lastObject = change


def runSettersMP(date_to):
    thisDay = datetime.strptime(date_to, API_DATE_FORMAT)
    toDate = (thisDay - timedelta(days=1)).date()
    setters_models = {
        # model: setter,
        CutVotes: setCutVotes,
        MembershipsOfMember: setMembershipsOfMember,
        LessEqualVoters: setLessEqualVoters,
        EqualVoters: setMostEqualVoters,
        Presence: setPercentOFAttendedSession,

    }
    memberships = tryHard(API_URL + '/getAllTimeMemberships').json()

    for membership in memberships:
        if membership['end_time']:
            end_time = datetime.strptime(
                membership['end_time'].split('T')[0], '%Y-%m-%d').date()
            if end_time > toDate:
                end_time = toDate
        else:
            end_time = toDate

        for model, setter in setters_models.items():
            print setter, date_to
            if membership['start_time']:
                print 'START', membership['start_time']
                start_time = datetime.strptime(
                    membership['start_time'].split('T')[0], '%Y-%m-%d')
                dates = findDatesFromLastCard(model,
                                              membership['id'],
                                              end_time.strftime(API_DATE_FORMAT),
                                              start_time.strftime(API_DATE_FORMAT))
            else:
                dates = findDatesFromLastCard(
                    model, membership['id'],
                    end_time.strftime(API_DATE_FORMAT))
            for date in dates:
                print date.strftime('%d.%m.%Y')
                print str(membership['id']) + '/' + date.strftime('%d.%m.%Y')
                try:
                    setter(None,
                           str(membership['id']),
                           date.strftime('%d.%m.%Y'))
                except:
                    client.captureException()
        # setLastActivity allways runs without date
        setLastActivity(request, str(membership['id']))

    # Runner for setters ALL
    all_in_one_setters_models = {
        AverageNumberOfSpeechesPerSession: setAverageNumberOfSpeechesPerSessionAll,
        VocabularySize: setVocabularySizeAndSpokenWords,
        Compass: setCompass,
    }

    zero = datetime(day=2, month=8, year=2014).date()
    for model, setter in all_in_one_setters_models.items():
        print(toDate - datetime(day=2, month=8, year=2014).date()).days
        for i in range((toDate - datetime(day=2, month=8, year=2014).date()).days):
            print(zero + timedelta(days=i)).strftime('%d.%m.%Y')
            try:
                setter(None, (zero + timedelta(days=i)).strftime('%d.%m.%Y'))
            except:
                client.captureException()

    return JsonResponse({'status': 'all is fine :D'}, safe=False)


def runMembersSetterOnDates(setter, stDate, toDate):
    stDate = datetime.strptime(stDate, API_DATE_FORMAT).date()
    toDate = datetime.strptime(toDate, API_DATE_FORMAT).date()

    setters_models = {None: setter}

    memberships = tryHard(API_URL + '/getAllTimeMemberships').json()

    pool = Pool(processes=1)
    pool.map(doMembersRunner, [{'membership': membership,
                                'stDate': stDate,
                                'toDate': toDate,
                                'setters_models': setters_models}
                               for membership in memberships])

    return 'all is fine :D'


def runSetterOnDates(setter, stDate, toDate):
    stDate = datetime.strptime(stDate, API_DATE_FORMAT).date()
    toDate = datetime.strptime(toDate, API_DATE_FORMAT).date()

    dates = datesGenerator(stDate, toDate)

    for date in dates:
        print 'Setting', date, setter
        setter(None, date.strftime(API_DATE_FORMAT))

    print 'END ', setter

    return 1


def runSettersMPSinglePerson(date_to=None):
    if not date_to:
        date_to = datetime.today().strftime(API_DATE_FORMAT)

    toDate = datetime.strptime(date_to, API_DATE_FORMAT).date()
    zero = datetime(day=2, month=8, year=2014).date()
    memberships = tryHard(API_URL + '/getAllTimeMemberships').json()

    setters_models = {
        # model: setter,
        CutVotes: setCutVotes,
        MembershipsOfMember: setMembershipsOfMember,
        LessEqualVoters: setLessEqualVoters,
        EqualVoters: setMostEqualVoters,
        Presence: setPercentOFAttendedSession,
    }
    for membership in memberships:
        doMembersRunner({'membership': membership,
                         'toDate': toDate,
                         'setters_models': setters_models})

    return 1


def runSettersMPAllPerson(date_to=None):
    if not date_to:
        date_to = datetime.today().strftime(API_DATE_FORMAT)

    toDate = datetime.strptime(date_to, API_DATE_FORMAT).date()
    zero = datetime(day=2, month=8, year=2014).date()
    all_in_one_setters_models = {
        AverageNumberOfSpeechesPerSession: setAverageNumberOfSpeechesPerSessionAll,
        VocabularySize: setVocabularySizeAndSpokenWords,
        Compass: setCompass,
        StyleScores: setStyleScoresALL,
    }
    for model, setter in all_in_one_setters_models.items():
        doAllMembersRunner({'setters': setter,
                            'model': model,
                            'toDate': toDate,
                            'zero': zero})

    return 1


def onDateMPCardRunner(date_=None):
    """
    Create all cards for data_ date. If date_ is None set for run setters
    for today.
    """
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    if date_:
        dateObj = datetime.strptime(date_, API_DATE_FORMAT)
        date_of = (dateObj - timedelta(days=1)).date()
    else:
        date_of = (datetime.now() - timedelta(days=1)).date()
        date_ = date_of.strftime(API_DATE_FORMAT)
    setters = [
        setCutVotes,
        setMembershipsOfMember,
        setLessEqualVoters,
        setMostEqualVoters,
        setPercentOFAttendedSession,
        setPresenceThroughTime,
        # setTFIDF
    ]

    memberships = tryHard(API_URL + '/getMPs/' + date_).json()

    for membership in memberships:
        for setter in setters:
            print 'running:' + str(setter)
            try:
                setter(None, str(membership['id']), date_)
            except:
                msg = ('' + FAIL + ''
                       'FAIL on: '
                       '' + str(setter) + ''
                       ' and with id: '
                       '' + str(membership['id']) + ''
                       '' + ENDC + '')
                print msg
        setLastActivity(None, str(membership['id']))

    # Runner for setters ALL
    all_in_one_setters = [
        setAverageNumberOfSpeechesPerSessionAll,
        setVocabularySizeAndSpokenWords,
        setCompass,
    ]

    zero = datetime(day=2, month=8, year=2014).date()
    for setter in all_in_one_setters:
        print 'running:' + str(setter)
        try:
            setter(None, date_)
        except:
            print 'FAIL on: ' + str(setter)


# parlaseje runners methods #

def runSettersPG(date_to=None):
    if not date_to:
        date_to = datetime.today().strftime(API_DATE_FORMAT)
    dateObj = datetime.strptime(date_to, API_DATE_FORMAT)
    toDate = (dateObj - timedelta(days=1)).date()
    setters_models = {
        CutVotesPG: setCutVotesPG,
        DeviationInOrganization: setDeviationInOrg,
        LessMatchingThem: setLessMatchingThem,
        MostMatchingThem: setMostMatchingThem,
        PercentOFAttendedSession: setPercentOFAttendedSessionPG,
        MPOfPg: setMPsOfPG,
        PGStatic: setBasicInfOfPG,
    }

    IDs = getPGIDs()
    # IDs = [1, 2]
    # print IDs
    allIds = len(IDs)
    curentId = 0
    start_time = None
    end_time = None
    for model, setter in setters_models.items():
        for ID in IDs:
            print setter
            start_time = None
            end_time = None
            url_date = ('/' + date_to if date_to else '/')
            url = API_URL + '/getMembersOfPGRanges/' + str(ID) + url_date
            membersOfPGsRanges = tryHard(url).json()

            # find if pg exist
            for pgRange in membersOfPGsRanges:
                if not pgRange['members']:
                    continue
                else:
                    if not start_time:
                        start_time = datetime.strptime(
                            pgRange['start_date'], '%d.%m.%Y').date()

                    end_time = datetime.strptime(
                        pgRange['end_date'], '%d.%m.%Y').date()

            if not start_time:
                continue

            dates = findDatesFromLastCard(model,
                                          ID,
                                          end_time.strftime(API_DATE_FORMAT),
                                          start_time.strftime(API_DATE_FORMAT))
            print dates
            for date in dates:
                if date < start_time or date > end_time:
                    break
                print date.strftime(API_DATE_FORMAT)
                # print setter + str(ID) + '/' + date.strftime(API_DATE_FORMAT)
                try:
                    setter(None, str(ID), date.strftime(API_DATE_FORMAT))
                except:
                    client.captureException()
        curentId += 1

    # Runner for setters ALL
    all_in_one_setters_models = {
        VocabularySizePG: setVocabularySizeALL,
        StyleScoresPG: setStyleScoresPGsALL,
    }

    zero = datetime(day=2, month=8, year=2014).date()
    for model, setter in all_in_one_setters_models.items():
        if model.objects.all():
            zero = model.objects.all().latest('created_for').created_for
        print(toDate - datetime(day=2, month=8, year=2014).date()).days
        for i in range((toDate - zero.date()).days):
            print(zero + timedelta(days=i)).strftime('%d.%m.%Y')
            print setter
            try:
                setter(None, (zero + timedelta(days=i)).strftime('%d.%m.%Y'))
            except:
                client.captureException()

    organizations = tryHard(API_URL + '/getOrganizatonByClassification').json()
    print organizations
    for org in organizations['working_bodies'] + organizations['council']:
        print org
        dates = findDatesFromLastCard(WorkingBodies, org['id'], date_to)
        for date in dates:
            try:
                print setWorkingBodies(None,
                                       str(org['id']),
                                       date.strftime(API_DATE_FORMAT)).content
            except:
                client.captureException()

    return 'all is fine :D PG ji so settani'


def onDatePGCardRunner(date_=None):
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    if date_:
        dateObj = datetime.strptime(date_, API_DATE_FORMAT)
        date_of = (dateObj - timedelta(days=1)).date()
    else:
        date_of = (datetime.now() - timedelta(days=1)).date()
        date_ = date_of.strftime(API_DATE_FORMAT)
    print date_
    setters = [
        setCutVotesPG,
        setDeviationInOrg,
        setLessMatchingThem,
        setMostMatchingThem,
        setPercentOFAttendedSessionPG,
        setMPsOfPG,
        setBasicInfOfPG,
        setPresenceThroughTimePG,
    ]

    membersOfPGsRanges = tryHard(
        API_URL + '/getMembersOfPGsRanges/' + date_).json()
    IDs = [key for key, value in membersOfPGsRanges[-1]['members'].items()
           if value]
    curentId = 0

    for setter in setters:
        for ID in IDs:
            print setter
            try:
                setter(None, str(ID), date_)
            except:
                text = ('' + FAIL + 'FAIL on: ' + str(setter) + ''
                        ' and with id: ' + str(ID) + ENDC + '')
                print text

    # Runner for setters ALL
    all_in_one_setters = [
        # setVocabularySizeALL,
    ]

    for setter in all_in_one_setters:
        try:
            setter(None, date_)
        except:
            print FAIL + 'FAIL on: ' + str(setter) + ENDC

    # updateWB()


def runSettersSessions(date_to=None, sessions_ids=None):
    if not date_to:
        date_to = datetime.today().strftime(API_DATE_FORMAT)

    setters_models = {
        PresenceOfPG: setPresenceOfPG,
        # AverageSpeeches: setSpeechesOnSession,
        Vote_graph: setMotionOfSessionGraph
    }
    for model, setter in setters_models.items():
        if model != AverageSpeeches:
            # IDs = getSesIDs(dates[1],dates[-1])
            if sessions_ids:
                last = sessions_ids
            else:
                last = idsOfSession(model)
            print last
            print model
            for ID in last:
                print ID
                try:
                    setter(None, str(ID))
                except:
                    client.captureException()
        else:
            dates = findDatesFromLastCard(model, None, date_to)
            print model
            if dates == []:
                continue
            datesSes = getSesDates(dates[-1])
            for date in datesSes:
                print date
                try:
                    setter(None, date.strftime(API_DATE_FORMAT))
                except:
                    client.captureException()
    return 'all is fine :D'


def updateAll():
    update()

    print 'mp static'
    updateMPStatic()

    print 'start update cards'
    updateLastDay()

    return 1


def updateLastDay(date_=None):
    if not date_:
        to_date = datetime.now()
    else:
        to_date = date_
    try:
        print 'sessions'
        runSettersSessions()
    except:
        client.captureException()

    votes = Vote.objects.filter(session_date__lte=to_date)
    lastVoteDay = votes.latest('created_for').created_for
    speeches = Speech.objects.filter(session_date__lte=to_date)
    lastSpeechDay = speeches.latest('start_time').start_time

    votez = VotesAnalysis(to_date)
    votez.setAll()

    runForTwoDays = True

    if lastVoteDay.date() == lastSpeechDay.date():
        runForTwoDays = False

    try:
        onDateMPCardRunner(lastVoteDay.strftime(API_DATE_FORMAT))
    except:
        client.captureException()
    try:
        onDatePGCardRunner(lastVoteDay.strftime(API_DATE_FORMAT))
    except:
        client.captureException()

    # if last vote and speech isn't in the same day
    if runForTwoDays:
        try:
            onDateMPCardRunner(lastSpeechDay.strftime(API_DATE_FORMAT))
        except:
            client.captureException()
        try:
            onDatePGCardRunner(lastSpeechDay.strftime(API_DATE_FORMAT))
        except:
            client.captureException()

    return 1


def deleteAppModels(appName):
    my_app = apps.get_app_config(appName)
    my_models = my_app.get_models()
    for model in my_models:
        print 'delete model: ', model
        model.objects.all().delete()


def updateWB():
    organizations = tryHard(API_URL + '/getOrganizatonByClassification').json()
    for wb in organizations['working_bodies'] + organizations['council']:
        print 'setting working_bodie: ', wb['name']
        try:
            setWorkingBodies(None,
                             str(wb['id']),
                             datetime.now().date().strftime(API_DATE_FORMAT))
        except:
            client.captureException()

    return 'all is fine :D WB so settani'


def deleteUnconnectedSpeeches():
    data = tryHard(API_URL + '/getAllSpeeches').json()
    idsInData = [speech['id'] for speech in data]
    blindSpeeches = Speech.objects.all().exclude(id_parladata__in=idsInData)
    blindSpeeches.delete()


def fastUpdate(date_=None):
    start_time = time()
    new_redna_seja = []
    lockFile = open('parser.lock', 'w+')
    lockFile.write('LOCKED')
    lockFile.close()
    client.captureMessage('Start fast update at: ' + str(datetime.now()))

    dates = []

    lastBallotTime = Ballot.objects.latest('updated_at').updated_at
    lastVoteTime = Vote.objects.latest('updated_at').updated_at
    lastSpeechTime = Speech.objects.latest('updated_at').updated_at

    if date_:
        dates = [date_ + '_00:00' for i in range(5)]
    else:
        # get dates of last update
        dates.append(Person.objects.latest('updated_at').updated_at)
        dates.append(Session.objects.latest('updated_at').updated_at)
        dates.append(lastSpeechTime)
        dates.append(lastBallotTime)
        dates.append(Question.objects.latest('updated_at').updated_at)

    # prepare url
    url = API_URL + '/getAllChangesAfter/'
    for sDate in dates:
        url += sDate.strftime(API_DATE_FORMAT + '_%H:%M') + '/'

    print url

    data = tryHard(url[:-1]).json()

    print 'Speeches: ', len(data['speeches'])
    print 'Sessions: ', len(data['sessions'])
    print 'Persons: ', len(data['persons'])
    print 'Questions: ', len(data['questions'])

    sdate = datetime.now().strftime(API_DATE_FORMAT)

    # Persons
    mps = tryHard(API_URL + '/getMPs/' + sdate).json()
    mps_ids = [mp['id'] for mp in mps]
    for mp in data['persons']:
        if Person.objects.filter(id_parladata=mp['id']):
            person = Person.objects.get(id_parladata=mp['id'])
            person.name = mp['name']
            person.pg = mp['membership']
            person.id_parladata = int(mp['id'])
            person.image = mp['image']
            person.actived = True if int(mp['id']) in mps_ids else False
            person.gov_id = mp['gov_id']
            person.save()
        else:
            actived = True if int(mp['id']) in mps_ids else False
            person = Person(name=mp['name'],
                            pg=mp['membership'],
                            id_parladata=int(mp['id']),
                            image=mp['image'],
                            actived=actived,
                            gov_id=mp['gov_id'])
            person.save()

    session_ids = list(Session.objects.all().values_list('id_parladata',
                                                         flat=True))

    # sessions
    for sessions in data['sessions']:
        orgs = Organization.objects.filter(id_parladata__in=sessions['organizations_id'])
        if not orgs:
            orgs = Organization.objects.filter(id_parladata=sessions['organization_id'])
        if sessions['id'] not in session_ids:
            result = Session(name=sessions['name'],
                             gov_id=sessions['gov_id'],
                             start_time=sessions['start_time'],
                             end_time=sessions['end_time'],
                             classification=sessions['classification'],
                             id_parladata=sessions['id'],
                             organization=orgs[0],
                             in_review=sessions['is_in_review']
                             )
            result.save()
            orgs = list(orgs)
            result.organizations.add(*orgs)
            if sessions['id'] == DZ:
                if 'redna seja' in sessions['name'].lower():
                    # call method for create new list of members
                    #new_redna_seja.append(sessions)
                    pass
        else:
            if not Session.objects.filter(name=sessions['name'],
                                          gov_id=sessions['gov_id'],
                                          start_time=sessions['start_time'],
                                          end_time=sessions['end_time'],
                                          classification=sessions['classification'],
                                          id_parladata=sessions['id'],
                                          organization=orgs[0],
                                          in_review=sessions['is_in_review']):
                # save changes
                session = Session.objects.get(id_parladata=sessions['id'])
                session.name = sessions['name']
                session.gov_id = sessions['gov_id']
                session.start_time = sessions['start_time']
                session.end_time = sessions['end_time']
                session.classification = sessions['classification']
                session.in_review = sessions['is_in_review']
                session.save()
                orgs = list(orgs)
                session.organizations.add(*orgs)

    # update speeches
    existingIDs = list(Speech.objects.all().values_list('id_parladata',
                                                        flat=True))
    for dic in data['speeches']:
        if int(dic['id']) not in existingIDs:
            print 'adding speech'
            person = Person.objects.get(id_parladata=int(dic['speaker']))
            speech = Speech(person=person,
                            organization=Organization.objects.get(
                                id_parladata=int(dic['party'])),
                            content=dic['content'], order=dic['order'],
                            session=Session.objects.get(
                                id_parladata=int(dic['session'])),
                            start_time=dic['start_time'],
                            end_time=dic['end_time'],
                            valid_from=dic['valid_from'],
                            valid_to=dic['valid_to'],
                            id_parladata=dic['id'])
            speech.save()
        else:
            print 'update speech'
            speech = Speech.objects.filter(id_parladata=dic['id'])
            speech.update(content=dic['content'],
                          valid_from=dic['valid_from'],
                          valid_to=dic['valid_to'])

    # update Votes
    for session_id in data['sessions_of_updated_votes']:
        setMotionOfSession(None, str(session_id))

    # update ballots
    existingISs = Ballot.objects.all().values_list('id_parladata', flat=True)
    for dic in data['ballots']:
        if int(dic['id']) not in existingISs:
            print 'adding ballot ' + str(dic['vote'])
            vote = Vote.objects.get(id_parladata=dic['vote'])
            person = Person.objects.get(id_parladata=int(dic['voter']))
            ballots = Ballot(person=person,
                             option=dic['option'],
                             vote=vote,
                             start_time=vote.session.start_time,
                             end_time=None,
                             id_parladata=dic['id'])
            ballots.save()

    # update questions
    existingISs = list(Question.objects.all().values_list('id_parladata',
                                                          flat=True))
    for dic in data['questions']:
        if int(dic['id']) not in existingISs:
            print 'adding question'
            if dic['session_id']:
                session = Session.objects.get(id_parladata=int(dic['session_id']))
            else:
                session = None
            link = dic['link'] if dic['link'] else None
            person = Person.objects.get(id_parladata=int(dic['author_id']))
            if dic['recipient_id']:
                rec_p = Person.objects.get(id_parladata=int(dic['recipient_id']))
            else:
                rec_p = None
            if dic['recipient_org_id']:
                rec_org = Organization.objects.get(id_parladata=int(dic['recipient_org_id']))
            else:
                rec_org = None
            question = Question(person=person,
                                session=session,
                                start_time=dic['date'],
                                id_parladata=dic['id'],
                                recipient_text=dic['recipient_text'],
                                title=dic['title'],
                                content_link=link,
                                recipient_organization=rec_org,
                                recipient_person=rec_p,
                                )
            question.save()

    updateDistricts()

    updateTags()

    if data['persons']:
        print 'mp static'
        updateMPStatic()
        print 'update person status'
        updatePersonStatus()

    t_delta = time() - start_time
    msg = ('End fast update ('
           '' + str(t_delta) + ''
           ' s) and start update sessions cards at: '
           '' + str(datetime.now()) + '')
    client.captureMessage(msg)

    print 'sessions'
    s_update = []
    # sessions = Session.objects.filter(updated_at__gte=datetime.now().date)
    # s_update += list(sessions.values_list('id_parladata', flat=True))
    votes = Vote.objects.filter(updated_at__gt=lastVoteTime)
    s_update += list(votes.values_list('session__id_parladata', flat=True))
    ballots = Ballot.objects.filter(updated_at__gt=lastBallotTime)
    s_update += list(ballots.values_list('vote__session__id_parladata',
                                         flat=True))

    if s_update:
        runSettersSessions(sessions_ids=list(set(s_update)))

    t_delta = time() - start_time
    msg = ('End creating cards ('
           '' + str(t_delta) + ''
           ' s) and start creating recache: '
           '' + str(datetime.now()) + '')
    client.captureMessage(msg)

    lockFile = open('parser.lock', 'w+')
    lockFile.write('UNLOCKED')
    lockFile.close()

    # recache

    # add sesessions of updated speeches to recache
    speeches = Speech.objects.filter(updated_at__gt=lastSpeechTime)
    s_update += list(speeches.values_list('session__id_parladata', flat=True))

    date_ = (datetime.now() + timedelta(days=1)).strftime(API_DATE_FORMAT)
    getSessionsList(None, date_, force_render=True)
    print s_update
    if s_update:
        print 'recache'
        updatePagesS(list(set(s_update)))

    t_delta = time() - start_time
    msg = ('End fastUpdate everything ('
           '' + str(t_delta) + ' s): '
           '' + str(datetime.now()) + '')
    client.captureMessage(msg)

    for session in new_redna_seja:
        # run cards
        msg = ('New redna seja: '
               '' + session.name + ''
               ' Start creating cards')
        client.captureMessage(msg)
        updateLastDay(session.date)
        setListOfMembers(sessions['start_time'])
        client.captureMessage('New P and PG cards was created.')


def setListOfMembers(date_time):
    """
    TODO: naredi da se posle mejl ko se doda nova redna seja.
    Ker je potrebno pognat se style score na searchu.
    """
    start_date = datetime.strptime(date_time, '%Y-%m-%dT%X')
    start_date = start_date - timedelta(days=1)
    setListOfMembersTickers(None, start_time.strftime(API_DATE_FORMAT))
