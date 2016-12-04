# -*- coding: utf-8 -*-

import requests
from parlaposlanci.views import setMPStaticPL
from parlalize.settings import API_URL, API_DATE_FORMAT, BASE_URL
from parlalize.utils import getPGIDs, findDatesFromLastCard
from datetime import datetime, timedelta
from django.apps import apps
from parlaposlanci.models import District
from raven.contrib.django.raven_compat.models import client


from parlaposlanci.views import setCutVotes, setStyleScoresALL, setMPStaticPL, setMembershipsOfMember, setLessEqualVoters, setMostEqualVoters, setPercentOFAttendedSession, setLastActivity, setAverageNumberOfSpeechesPerSessionAll, setVocabularySizeAndSpokenWords, setCompass, getListOfMembers, setTFIDF
from parlaposlanci.models import Person, StyleScores, CutVotes, VocabularySize, MPStaticPL, MembershipsOfMember, LessEqualVoters, EqualVoters, Presence, AverageNumberOfSpeechesPerSession, VocabularySize, Compass

from parlaskupine.views import setCutVotes as setCutVotesPG, setDeviationInOrg, setLessMatchingThem, setMostMatchingThem, setPercentOFAttendedSessionPG, setMPsOfPG, setBasicInfOfPG, setWorkingBodies, setVocabularySizeALL, setStyleScoresPGsALL, setTFIDF as setTFIDFpg, getListOfPGs
from parlaskupine.models import Organization, WorkingBodies, CutVotes as CutVotesPG, DeviationInOrganization, LessMatchingThem, MostMatchingThem, PercentOFAttendedSession, MPOfPg, PGStatic, VocabularySize as VocabularySizePG, StyleScores as StyleScoresPG

from parlaseje.models import Session, Vote, Ballot, Speech, Tag, PresenceOfPG, AbsentMPs, AverageSpeeches, Vote_graph
from parlaseje.views import setPresenceOfPG, setAbsentMPs, setSpeechesOnSession, setMotionOfSessionGraph
from parlaseje.utils import idsOfSession, getSesDates

from multiprocessing import Pool

from parlalize.utils import tryHard, datesGenerator

## parlalize initial runner methods ##

def updatePeople():
    data = tryHard(API_URL + '/getAllPeople/').json()
    mps = tryHard(API_URL + '/getMPs/').json()
    mps_ids = [mp['id'] for mp in mps]
    for mp in data:
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
            person = Person(name=mp['name'], pg=mp['membership'], id_parladata=int(mp['id']), image=mp[
                            'image'], actived=True if int(mp['id']) in mps_ids else False, gov_id=mp['gov_id'])
            person.save()

    return 1


def updateOrganizations():
    data = tryHard(API_URL + '/getAllOrganizations').json()
    for pg in data:
        if Organization.objects.filter(id_parladata=pg):
            org = Organization.objects.get(id_parladata=pg)
            org.name = data[pg]['name']
            org.classification = data[pg]['classification']
            org.acronym = data[pg]['acronym']
            org.is_coalition = data[pg]['is_coalition']
            print data[pg]['acronym']
            org.save()
        else:
            org = Organization(name=data[pg]['name'],
                               classification=data[pg]['classification'],
                               id_parladata=pg,
                               acronym=data[pg]['acronym'],
                               is_coalition=data[pg]['is_coalition'])
            org.save()
    return 1


def updateSpeeches():
    data = tryHard(API_URL + '/getAllSpeeches').json()
    for dic in data:
        if Speech.objects.filter(id_parladata=dic['id']):
            print "updating speech"
            Speech.objects.filter(id_parladata=dic['id']).update(person=Person.objects.get(
                                id_parladata=int(dic['speaker'])),
                            organization=Organization.objects.get(
                                id_parladata=int(dic['party'])),
                            content=dic['content'], order=dic['order'],
                            session=Session.objects.get(
                                id_parladata=int(dic['session'])),
                            start_time=dic['start_time'],
                            end_time=dic['end_time'],
                            id_parladata=dic['id'])
        else:
            print "adding speech"
            speech = Speech(person=Person.objects.get(id_parladata=int(dic['speaker'])),
                            organization=Organization.bjects.get(
                                id_parladata=int(dic['party'])),
                            content=dic['content'], order=dic['order'],
                            session=Session.objects.get(
                                id_parladata=int(dic['session'])),
                            start_time=dic['start_time'],
                            end_time=dic['end_time'],
                            id_parladata=dic['id'])
            speech.save()
    return 1

# treba pofixsat


def updateMotionOfSession():
    ses = Session.objects.all()
    for s in ses:
        print s.id_parladata
        tryHard(BASE_URL + '/s/setMotionOfSession/' + str(s.id_parladata))

# treba pofixsat


def updateBallots():
    data = tryHard(API_URL + '/getAllBallots').json()
    existingISs = Ballot.objects.all().values_list("id_parladata", flat=True)
    for dic in data:
        # Ballot.objects.filter(id_parladata=dic['id']):
        if int(dic["id"]) not in existingISs:
            print "adding ballot " + str(dic['vote'])
            vote = Vote.objects.get(id_parladata=dic['vote'])
            ballots = Ballot(person=Person.objects.get(id_parladata=int(dic['voter'])),
                             option=dic['option'],
                             vote=vote,
                             start_time=vote.session.start_time,
                             end_time=None,
                             id_parladata=dic['id'])
            ballots.save()
    return 1


def setAllSessions():
    data  = tryHard(API_URL + '/getSessions/').json()
    session_ids = list(Session.objects.all().values_list("id_parladata", flat=True))
    for sessions in data:
        if sessions['id'] not in session_ids:
            result = Session(name=sessions['name'],
                             gov_id=sessions['gov_id'],
                             start_time=sessions['start_time'],
                             end_time=sessions['end_time'],
                             classification=sessions['classification'],
                             id_parladata=sessions['id'],
                             organization=Organization.objects.get(id_parladata=sessions['organization_id']),
                             in_review=sessions['is_in_review']
                             ).save()
        else:
            if not Session.objects.filter(name=sessions['name'],
                                          gov_id=sessions['gov_id'],
                                          start_time=sessions['start_time'],
                                          end_time=sessions['end_time'],
                                          classification=sessions['classification'],
                                          id_parladata=sessions['id'],
                                          organization=Organization.objects.get(id_parladata=sessions['organization_id']),
                                          in_review=sessions['is_in_review']):
                #save changes
                session = Session.objects.get(id_parladata=sessions['id'])
                session.name = sessions['name']
                session.gov_id = sessions['gov_id']
                session.start_time = sessions['start_time']
                session.end_time = sessions['end_time']
                session.classification = sessions['classification']
                session.id_parladata = sessions['id']
                session.organization = Organization.objects.get(id_parladata=sessions['organization_id'])
                session.in_review = sessions['is_in_review']
                session.save()

    return 1

## parlaposlanci runner methods ##


def updateMPStatic():
    memberships = tryHard(API_URL + '/getMembersOfPGsRanges/').json()
    lastObject = {"members": {}}
    print "[info] update MP static"
    for change in memberships:
        # call setters for new pg
        for pg in list(set(change["members"].keys()) - set(lastObject["members"].keys())):
            for member in change["members"][pg]:
                setMPStaticPL(None, str(member), change["start_date"])

        # call setters for members which have change in memberships
        for pg in change["members"].keys():
            if pg in lastObject["members"].keys():
                for member in list(set(change["members"][pg]) - set(lastObject["members"][pg])):
                    setMPStaticPL(None, str(member), change["start_date"])
        lastObject = change


def runSettersMP(date_to):
    toDate = (datetime.strptime(date_to, API_DATE_FORMAT) - timedelta(days=1)).date()
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
        if membership["end_time"]:
            end_time = datetime.strptime(
                membership["end_time"].split("T")[0], "%Y-%m-%d").date()
            if end_time > toDate:
                end_time = toDate
        else:
            end_time = toDate

        for model, setter in setters_models.items():
            print setter, date_to
            if membership["start_time"]:
                print "START", membership["start_time"]
                start_time = datetime.strptime(
                    membership["start_time"].split("T")[0], "%Y-%m-%d")
                dates = findDatesFromLastCard(model, membership["id"], end_time.strftime(
                    API_DATE_FORMAT), start_time.strftime(API_DATE_FORMAT))
            else:
                dates = findDatesFromLastCard(
                    model, membership["id"], end_time.strftime(API_DATE_FORMAT))
            for date in dates:
                print date.strftime('%d.%m.%Y')
                print str(membership["id"]) + "/" + date.strftime('%d.%m.%Y')
                try:
                    setter(None, str(membership["id"]), date.strftime('%d.%m.%Y'))
                except:
                    client.captureException()
        # setLastActivity allways runs without date
        setLastActivity(request, str(membership["id"]))

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

    return JsonResponse({"status": "all is fine :D"}, safe=False)


# using for multiprocess runner
def doMembersRunner(data):
    temp_data = data.copy()
    membership = temp_data["membership"]
    toDate = temp_data["toDate"]
    stDate = temp_data["stDate"]
    setters_models = temp_data["setters_models"]
    print "start Date", stDate
    print "todate", toDate
    print "mems_start_time", membership["start_time"]
    print "mems_end_time", membership["end_time"]
    if membership["end_time"]:
        end_time = datetime.strptime(membership["end_time"].split("T")[0], "%Y-%m-%d").date()
        if end_time > toDate:
            end_time = toDate
    else:
        if membership["start_time"]:
            if datetime.strptime(membership["start_time"].split("T")[0], "%Y-%m-%d").date() > toDate:
                return
        end_time = toDate

    for model, setter in setters_models.items():
        print setter, toDate
        if membership["start_time"]:
            #print "START", membership["start_time"]
            start_time = datetime.strptime(
                membership["start_time"].split("T")[0], "%Y-%m-%d")
            if stDate == None:
                dates = findDatesFromLastCard(model, membership["id"], end_time.strftime(
                    API_DATE_FORMAT), start_time.strftime(API_DATE_FORMAT))
            else:
                dates = datesGenerator(stDate, toDate)
        else:
            if stDate == None:
                dates = findDatesFromLastCard(
                    model, membership["id"], end_time.strftime(API_DATE_FORMAT))
            else:
                dates = datesGenerator(stDate, toDate)
        for date in dates:
            #print date.strftime('%d.%m.%Y')
            #print str(membership["id"]) + "/" + date.strftime('%d.%m.%Y')
            try:
                setter(None, str(membership["id"]), date.strftime('%d.%m.%Y'))
            except:
                client.captureException()
    # setLastActivity allways runs without date
        setLastActivity(None, str(membership["id"]))


# using for multiprocess runner
def doAllMembersRunner(data):
    temp_data = data.copy()
    setter = temp_data["setters"]
    model = temp_data["model"]
    toDate = temp_data["toDate"]
    zero = temp_data["zero"]
    #print(toDate - datetime(day=2, month=8, year=2014).date()).days

    members = tryHard(API_URL + '/getMPs/' + toDate.strftime(API_DATE_FORMAT)).json()
    dates = []
    if model == Compass:
        cards = model.objects.all().order_by("created_for")
        if cards:
            dates.append(list(cards)[-1].created_for)
    else:
        for member in members:
            members_cards = model.objects.filter(person__id_parladata=member["id"]).order_by("created_for")
            if members_cards:
                dates.append(list(members_cards)[-1].created_for)
    print dates
    if dates:
        zero = min(dates)
    print zero
    print "start all members"+str(setter)
    for i in range((toDate - zero).days):
        print(zero + timedelta(days=i)).strftime('%d.%m.%Y')
        try:
            setter(None, (zero + timedelta(days=i)).strftime('%d.%m.%Y'))
        except:
            client.captureException()

#stDate uporabljamo takrat ko hocemo pofixati luknje v analizah
def runSettersMPMultiprocess(date_to): 
    toDate = datetime.strptime(date_to, API_DATE_FORMAT).date()
    zero = datetime(day=2, month=8, year=2014).date()
    setters_models = {
        # model: setter,

        CutVotes: setCutVotes,
        MembershipsOfMember: setMembershipsOfMember,
        LessEqualVoters: setLessEqualVoters,
        EqualVoters: setMostEqualVoters,
        Presence: setPercentOFAttendedSession,

    }

    # Runner for setters ALL
    all_in_one_setters_models = {
        AverageNumberOfSpeechesPerSession: setAverageNumberOfSpeechesPerSessionAll,
        VocabularySize: setVocabularySizeAndSpokenWords,
        Compass: setCompass,
        StyleScores: setStyleScoresALL,
    }

    memberships = tryHard(API_URL + '/getAllTimeMemberships').json()



    pool = Pool(processes=1)
    pool.map(doMembersRunner, [{"membership": membership, "stDate": None, "toDate": toDate, "setters_models": setters_models} for membership in memberships])

    #pool = Pool(processes=16)
    #pool.map(doAllMembersRunner, [{"setters": setter, "model": model, "toDate": toDate, "zero": zero} for model, setter in all_in_one_setters_models.items()])


    return "all is fine :D"

def runMembersSetterOnDates(setter, stDate, toDate):
    stDate = datetime.strptime(stDate, API_DATE_FORMAT).date()
    toDate = datetime.strptime(toDate, API_DATE_FORMAT).date()

    setters_models = {
    None: setter
    }

    memberships = tryHard(API_URL + '/getAllTimeMemberships').json()

    pool = Pool(processes=1)
    pool.map(doMembersRunner, [{"membership": membership, "stDate": stDate, "toDate": toDate, "setters_models": setters_models} for membership in memberships])

    return "all is fine :D"


def runSetterOnDates(setter, stDate, toDate):
    stDate = datetime.strptime(stDate, API_DATE_FORMAT).date()
    toDate = datetime.strptime(toDate, API_DATE_FORMAT).date()

    dates = datesGenerator(stDate, toDate)

    for date in dates:
        print "Setting", date, setter
        setter(None, date.strftime(API_DATE_FORMAT))

    print "END ", setter

    return 1    


def runSettersMPSinglePerson(date_to=None):
    if not date_to:
        date_to=datetime.today().strftime(API_DATE_FORMAT)

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
        doMembersRunner({"membership": membership, "toDate": toDate, "setters_models": setters_models})

    return 1

def runSettersMPAllPerson(date_to=None):
    if not date_to:
        date_to=datetime.today().strftime(API_DATE_FORMAT)

    toDate = datetime.strptime(date_to, API_DATE_FORMAT).date()
    zero = datetime(day=2, month=8, year=2014).date()
    all_in_one_setters_models = {
        AverageNumberOfSpeechesPerSession: setAverageNumberOfSpeechesPerSessionAll,
        VocabularySize: setVocabularySizeAndSpokenWords,
        Compass: setCompass,
        StyleScores: setStyleScoresALL,
    }
    for model, setter in all_in_one_setters_models.items():
        doAllMembersRunner({"setters": setter, "model": model, "toDate": toDate, "zero": zero})

    return 1

# Create all cards for data_ date. If date_ is None set for run setters
# for today.
def onDateMPCardRunner(date_=None):
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    if date_:
        date_of = (datetime.strptime(date_, API_DATE_FORMAT) - timedelta(days=1)).date()
    else:
        date_of = (datetime.now()-timedelta(days=1)).date()
        date_ = date_of.strftime(API_DATE_FORMAT)
    setters = [
        #setCutVotes,
        #setMembershipsOfMember,
        #setLessEqualVoters,
        #setMostEqualVoters,
        #setPercentOFAttendedSession,
        #setTFIDF
    ]

    memberships = tryHard(API_URL + '/getMPs/' + date_).json()

    for membership in memberships:
        for setter in setters:
            print "running:" + str(setter)
            try:
                setter(None, str(membership["id"]), date_)
            except:
                print FAIL + "FAIL on: " + str(setter) + " and with id: " + str(membership["id"]) + ENDC
        setLastActivity(None, str(membership["id"]))

    # Runner for setters ALL
    all_in_one_setters = [
        #setAverageNumberOfSpeechesPerSessionAll,
        #setVocabularySizeAndSpokenWords,
        #setCompass,
    ]

    zero = datetime(day=2, month=8, year=2014).date()
    for setter in all_in_one_setters:
        print "running:" + str(setter)
        try:
            setter(None, date_)
        except:
            print "FAIL on: " + str(setter)


## parlaseje runners methods ##

def runSettersPG(date_to=None):
    if not date_to:
        date_to=datetime.today().strftime(API_DATE_FORMAT)

    toDate = (datetime.strptime(date_to, '%d.%m.%Y') - timedelta(days=1)).date()
    setters_models = {
        CutVotesPG: setCutVotesPG,#BASE_URL+'/p/setCutVotes/',
        DeviationInOrganization: setDeviationInOrg,
        LessMatchingThem: setLessMatchingThem,
        MostMatchingThem: setMostMatchingThem,
        PercentOFAttendedSession: setPercentOFAttendedSessionPG,
        MPOfPg: setMPsOfPG,
        PGStatic: setBasicInfOfPG,
    }

    IDs = getPGIDs()
    #IDs = [1, 2]
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
            membersOfPGsRanges = tryHard(
                API_URL + '/getMembersOfPGRanges/' + str(ID) + ("/" + date_to if date_to else "/")).json()

            #find if pg exist
            for pgRange in membersOfPGsRanges:
                if not pgRange["members"]:
                    continue
                else:
                    if not start_time:
                        start_time = datetime.strptime(
                            pgRange["start_date"], '%d.%m.%Y').date()

                    end_time = datetime.strptime(
                        pgRange["end_date"], '%d.%m.%Y').date()

            if not start_time:
                continue

            dates = findDatesFromLastCard(model, ID, end_time.strftime(API_DATE_FORMAT), start_time.strftime(API_DATE_FORMAT))
            print dates
            for date in dates:
                if date < start_time or date > end_time:
                    break
                print date.strftime(API_DATE_FORMAT)
                # print setter + str(ID) + "/" + date.strftime(API_DATE_FORMAT)
                try:
                    setter(None, str(ID), date.strftime(API_DATE_FORMAT))
                except:
                    client.captureException()
        curentId += 1
        # result = tryHard(setter + str(ID) + "/" + date.strftime(API_DATE_FORMAT)).status_code

    # Runner for setters ALL
    all_in_one_setters_models = {
        VocabularySizePG: setVocabularySizeALL,
        StyleScoresPG: setStyleScoresPGsALL,
    }

    zero = datetime(day=2, month=8, year=2014).date()
    for model, setter in all_in_one_setters_models.items():
        if model.objects.all():
            zero = model.objects.all().latest("created_for").created_for
        print(toDate - datetime(day=2, month=8, year=2014).date()).days
        for i in range((toDate - zero.date()).days):
            print(zero + timedelta(days=i)).strftime('%d.%m.%Y')
            print setter
            try:
                setter(None, (zero + timedelta(days=i)).strftime('%d.%m.%Y'))
            except:
                client.captureException()

    organizations = tryHard(API_URL + "/getOrganizatonByClassification").json()
    print organizations
    for org in organizations["working_bodies"] + organizations["council"]:
        print org
        dates = findDatesFromLastCard(WorkingBodies, org["id"], date_to)
        for date in dates:
            try:
                print setWorkingBodies(None, str(org["id"]), date.strftime(API_DATE_FORMAT)).content
            except:
                client.captureException()

    return "all is fine :D PG ji so settani"


def onDatePGCardRunner(date_=None):
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    if date_:
        date_of = (datetime.strptime(date_, API_DATE_FORMAT) - timedelta(days=1)).date()
    else:
        date_of = (datetime.now()-timedelta(days=1)).date()
        date_ = date_of.strftime(API_DATE_FORMAT)
    print date_
    setters = [
        #setCutVotesPG,
        setDeviationInOrg,
        #setLessMatchingThem,
        #setMostMatchingThem,
        #setPercentOFAttendedSessionPG,
        #setMPsOfPG,
        #setBasicInfOfPG,
    ]

    membersOfPGsRanges = tryHard(
        API_URL + '/getMembersOfPGsRanges/' + date_).json()
    IDs = [key for key, value in membersOfPGsRanges[-1]["members"].items()
           if value]
    curentId = 0

    for setter in setters:
        for ID in IDs:
            print setter
            try:
                setter(None, str(ID), date_)
            except:
                print FAIL + "FAIL on: " + str(setter) + " and with id: " + str(ID) + ENDC

    # Runner for setters ALL
    all_in_one_setters = [
        #setVocabularySizeALL,
    ]

    for setter in all_in_one_setters:
        try:
            setter(None, date_)
        except:
            print FAIL + "FAIL on: " + str(setter) + ENDC

    #updateWB()

def runSettersSessions(date_to=None):
    if not date_to:
        date_to=datetime.today().strftime(API_DATE_FORMAT)
 
    setters_models = {
        #PresenceOfPG: setPresenceOfPG,
        #AbsentMPs: setAbsentMPs,
        #AverageSpeeches: setSpeechesOnSession,
        Vote_graph: setMotionOfSessionGraph
    }
    for model, setter in setters_models.items():
        if model != AverageSpeeches:
            #IDs = getSesIDs(dates[1],dates[-1])
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
            if dates==[]:
                continue
            datesSes = getSesDates(dates[-1])
            for date in datesSes:
                print date
                try:
                    setter(None, date.strftime(API_DATE_FORMAT))
                except:
                    client.captureException()
    return "all is fine :D"


def update():
    updateOrganizations()
    print "org"

    updatePeople()
    print "pep"

    setAllSessions()
    print "Sessions"

    updateSpeeches()
    print "speeches"

    updateMotionOfSession()
    print "votes"

    updateBallots()
    print "ballots"

    updateDistricts()

    updateTags()

    print "mp static"
    updateMPStatic()

    print "update person status"
    updatePersonStatus()

    print "update person has_function"
    updatePersonFunctions()

    #print "start update cards"
    #updateLastDay()

    return 1

def updateCacheforList(date_=None):
    #refresh cache
    try:
        if not date_:
            date_ = (datetime.now() + timedelta(days=1)).strftime(API_DATE_FORMAT)
        getListOfMembers(None, date_, force_render=True)
        getListOfPGs(None, date_, force_render=True)
    except:
        client.captureException()

    client.captureMessage('Zgeneriru sem cache za nasledn dan')

    return 1

def updateLastDay():
    lastVoteDay = Vote.objects.latest("created_for").created_for
    onDateMPCardRunner(lastVoteDay.strftime(API_DATE_FORMAT))
    onDatePGCardRunner(lastVoteDay.strftime(API_DATE_FORMAT))
    return 1


def deleteAppModels(appName):
    my_app = apps.get_app_config(appName)
    my_models = my_app.get_models()
    for model in my_models:
        print "delete model: ", model
        model.objects.all().delete()


def updateDistricts():
    districts = tryHard(API_URL + "/getDistricts").json()
    existing_districts = District.objects.all().values_list("id_parladata", flat=True)
    for district in districts:
        if district["id"] not in existing_districts:
            District(name=district["name"], id_parladata=district["id"]).save()
        else:
            dist = District.objects.get(id_parladata=district["id"])
            if dist.name != district["name"]:
                dist.name = district["name"]
                dist.save()
    return 1


def updateTags():
    tags = tryHard(API_URL+'/getTags').json()
    existing_tags = Tag.objects.all().values_list("id_parladata", flat=True)
    count = 0
    for tag in tags:
        if tag["id"] not in existing_tags:
            Tag(name=tag["name"], id_parladata=tag["id"]).save()
            count += 1
    return 1

def updatePersonStatus():
    mps = tryHard(API_URL + '/getMPs').json()
    mps_ids = [mp["id"] for mp in mps]
    for person in Person.objects.all():
        if person.actived == "Yes":
            if person.id_parladata not in mps_ids:
                person.actived = "No"
                person.save()
        else:
            if person.id_parladata in mps_ids:
                person.actived = "Yes"
                person.save()


def updatePersonFunctions():
    mps = tryHard(API_URL + '/getMembersWithFuction').json()

    for person in Person.objects.all():
        if person.has_function:
            if person.id_parladata not in mps["members_with_function"]:
                person.has_function = False
                person.save()
        else:
            if person.id_parladata in mps["members_with_function"]:
                person.has_function = True
                person.save()

def updateWB():
    organizations = tryHard(API_URL + "/getOrganizatonByClassification").json()
    for wb in organizations["working_bodies"] + organizations["council"]:
        #pg = tryHard(API_URL + '/getMembersOfPGRanges/'+ str(wb['id']) +'/' + datetime.now().date().strftime(API_DATE_FORMAT)).json()
        #for mem in pg:
        print "setting working_bodie: ",wb['name']
        try:
            setWorkingBodies(None, str(wb["id"]), datetime.now().date().strftime(API_DATE_FORMAT))  
        except:
            client.captureException()
            
    return "all is fine :D WB so settani"


def morningCash():

    allUrls = [
        {
            "group":"s",
            "method":"seznam-odsotnih-poslancev",
            "class": "DZ"
        },{
            "group":"p",
            "method":"osnovne-informacije",
            "class": "all"
        },{
            "group":"p",
            "method":"razrez-glasovanj",
            "class": "all"
        },{
            "group":"p",
            "method":"stilne-analize",
            "class": "all"
        },{
            "group":"s",
            "method":"glasovanje-layered",
            "class": "all"
        },{
            "group":"p",
            "method":"najmanjkrat-enako",
            "class": "all"
        },{
            "group":"p",
            "method":"najveckrat-enako",
            "class": "all"
        },{
            "group":"s",
            "method":"glasovanja-seja",
            "class": "DZ"
        },{
            "group":"pg",
            "method":"razrez-glasovanj",
            "class": "all"
        },{
            "group":"p",
            "method":"izracunana-prisotnost-glasovanja",
            "class": "all"
        },{
            "group":"pg",
            "method":"izracunana-prisotnost-seje",
            "class": "all"
        },{
            "group":"p",
            "method":"glasovanja",
            "class": "all"
        },{
            "group":"p",
            "method":"izracunana-prisotnost-seje",
            "class": "all"
        },{
            "group":"p",
            "method":"besedni-zaklad",
            "class": "all"
        },{
            "group":"p",
            "method":"stevilo-izgovorjenih-besed",
            "class": "all"
        },{
            "group":"p",
            "method":"clanstva",
            "class": "all"
        },{
            "group":"p",
            "method":"povezave-do-govorov",
            "class": "all"
        },{
            "group":"ps",
            "method":"besedni-zaklad",
            "class": "all"
        },{
            "group":"ps",
            "method":"vsi-govori-poslanske-skupine",
            "class": "all"
        },{
            "group":"c",
            "method":"kompas",
            "class": "none"
        },{
            "group":"pg",
            "method":"glasovanja",
            "class": "all"
        },{
            "group":"c",
            "method":"zadnja-seja",
            "class": "none"
        },{
            "group":"p",
            "method":"tfidf",
            "class": "all"
        },{
            "group":"ps",
            "method":"stilne-analize",
            "class": "all"
        },{
            "group":"c",
            "method":"besedni-zaklad-vsi",
            "class": "none"
        },{
            "group":"p",
            "method":"povprecno-stevilo-govorov-na-sejo",
            "class": "all"
        },{
            "group":"p",
            "method":"zadnje-aktivnosti",
            "class": "all"
        },{
            "group" : "ps",
            "method" : "osnovne-informacije-poslanska-skupina",
            "class": "all"
        },
        {
            "group" : "ps",
            "method" : "izracunana-prisotnost-glasovanja",
            "class": "all"
        },
        {
            "group" : "ps",
            "method" : "tfidf",
            "class": "all"
        },
        {
            "group" : "wb",
            "method" : "getWorkingBodies",
            "class" : "all"
        },
        {
            "group" : "ps",
            "method" : "clanice-in-clani-poslanske-skupine",
            "class" : "all"
        },
        { 
            "group" : "pg",
            "method" : "najlazje-pridruzili",
            "class" : "all"
        },
        { 
            "group" : "pg",
            "method" : "najtezje-pridruzili",
            "class" : "all"
        },
        { 
            "group" : "pg",
            "method" : "odstopanje-od-poslanske-skupine",
            "class" : "all"
        },
        { 
            "group" : "s",
            "method" : "prisotnost-po-poslanskih-skupinah",
            "class" : "DZ"
        },
        {
            "group" : "p",
            "method" : "seznam-poslancev",
            "class" : "none"
        },
        {
            "group" : "ps",
            "method" : "seznam-poslanskih-skupin",
            "class": "all"
        }    
    ]

    # allUrls = tryHard("https://glej.parlameter.si/api/cards/getUrls").json()
    theUrl = 'https://glej.parlameter.si/'
    mps = tryHard('https://data.parlameter.si/v1/getMPs').json()
    session = tryHard('https://data.parlameter.si/v1/getSessions/').json()
    wb = tryHard('https://data.parlameter.si/v1/getOrganizatonByClassification').json()['working_bodies']
    sessionDZ = []
    for ses in session:
        if ses['organization_id'] == 95:
            sessionDZ.append(ses['id'])

    for url in allUrls:
        if url['group'] == 's':
            if url['class'] == 'DZ':
                #seje DZ
                for ses in sessionDZ:
                    method = url['group'] + '/' + url['method'] + '/'
                    print theUrl + method + str(ses) + '?forceRender=true'
                    requests.get(theUrl + method + str(ses) + '?forceRender=true')
                    requests.get(theUrl + method + str(ses) + '?forceRender=true&frame=true&altHeader=true')
                    requests.get(theUrl + method + str(ses) + '?forceRender=true&embed=true&altHeader=true')
            else:
                #VSE SEJE
                print url['method']
                for ses in Session.objects.values_list("id_parladata", flat=True):
                    method = url['group'] + '/' + url['method'] + '/'
                    print theUrl + method + str(ses) + '?forceRender=true'
                    requests.get(theUrl + method + str(ses) + '?forceRender=true')
                    requests.get(theUrl + method + str(ses) + '?forceRender=true&frame=true&altHeader=true')
                    requests.get(theUrl + method + str(ses) + '?forceRender=true&embed=true&altHeader=true')
        if url['group'] == 'p':
            if url['class'] == "none":
                #kličeš brez IDja s končnim slashem
                method = url['group'] + '/' + url['method'] + '/'
                print theUrl + method + str(ses) + '?forceRender=true'
                requests.get(theUrl + method + '?forceRender=true')
                requests.get(theUrl + method + '?forceRender=true&frame=true&altHeader=true')
                requests.get(theUrl + method + '?forceRender=true&embed=true&altHeader=true')
            else:
                #vsi poslanci
                for mp in mps:
                    method = url['group'] + '/' + url['method'] + '/'
                    print theUrl + method + str(mp['id']) + '?forceRender=true'
                    requests.get(theUrl + method + str(mp['id']) + '?forceRender=true')
                    requests.get(theUrl + method + str(mp['id']) + '?forceRender=true&frame=true&altHeader=true')
                    requests.get(theUrl + method + str(mp['id']) + '?forceRender=true&embed=true&altHeader=true')
        if (url['group'] == 'pg') or (url['group'] == 'ps'):
                for pg in Organization.objects.values_list("id_parladata", flat=True):
                    method = url['group'] + '/' + url['method'] + '/'
                    print theUrl + method + str(pg) + '?forceRender=true'
                    requests.get(theUrl + method + str(pg) + '?forceRender=true')
                    requests.get(theUrl + method + str(pg) + '?forceRender=true&frame=true&altHeader=true')
                    requests.get(theUrl + method + str(pg) + '?forceRender=true&embed=true&altHeader=true')
        if (url['group'] == 'c'):
            # kličeš brez IDja s končnim slashem
            method = url['group'] + '/' + url['method'] + '/'
            requests.get(theUrl + method + '?forceRender=true')
            requests.get(theUrl + method + '?forceRender=true&frame=true&altHeader=true')
            requests.get(theUrl + method + '?forceRender=true&embed=true&altHeader=true')
            print 'yay!'
        if (url['group'] == 'wb'):
            # kličeš vsa delovna telesa
            print 'yay!'

            for w in wb['id']:
                method = url['group'] + '/' + url['method'] + '/'
                print theUrl + method + str(w) + '?forceRender=true'
                requests.get(theUrl + method + str(w) + '?forceRender=true')
                requests.get(theUrl + method + str(w) + '?forceRender=true&frame=true&altHeader=true')
                requests.get(theUrl + method + str(w) + '?forceRender=true&embed=true&altHeader=true')
            print 'yay!'
