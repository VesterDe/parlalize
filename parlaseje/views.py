# -*- coding: UTF-8 -*-
from datetime import datetime

from parlalize.utils import *
import requests
import json
from django.http import JsonResponse
from parlaseje.models import *
from parlalize.settings import API_URL, API_DATE_FORMAT
from parlaseje.utils import *
from collections import defaultdict, Counter
from math import fabs
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
import re
from django.db.models import Q
from django.core.cache import cache

from parlalize.utils import tryHard

# Create your views here.


def getSpeech(request, speech_id):
    speech = get_object_or_404(Speech, id_parladata=speech_id)
    out = {"speech_id": speech.id_parladata,
           "content": speech.content,
           "session": speech.session.getSessionData(),
           "quoted_text": None,
           "end_idx": None,
           "start_idx": None,
           'quote_id': None}

    result = {
        'person': getPersonData(speech.person.id_parladata,
                                speech.session.start_time.strftime(API_DATE_FORMAT)),
        'created_for': speech.start_time.strftime(API_DATE_FORMAT),
        'created_at': speech.created_at.strftime(API_DATE_FORMAT),
        'results': out
    }
    return JsonResponse(result)


def getSpeechesOfSession(request, session_id):
    session = get_object_or_404(Session, id_parladata=session_id)
    speeches_queryset = Speech.getValidSpeeches(datetime.now())
    speeches = speeches_queryset.filter(session=session).order_by("start_time",
                                                                  "order")

    data = []
    for speech in speeches:
        out = {"speech_id": speech.id_parladata,
               "content": speech.content,
               "session": speech.session.getSessionData(),
               "quoted_text": None,
               "end_idx": None,
               "start_idx": None}

        result = {
            'person': getPersonData(speech.person.id_parladata,
                                    speech.session.start_time.strftime(API_DATE_FORMAT)),
            'results': out
        }
        data.append(result)

    return JsonResponse({"session": session.getSessionData(),
                         "created_for": session.start_time.strftime(API_DATE_FORMAT),
                         "created_at": datetime.today().strftime(API_DATE_FORMAT),
                         "results": data})


def getSpeechesIDsOfSession(request, session_id):
    session = get_object_or_404(Session, id_parladata=session_id)

    speeches = Speech.getValidSpeeches(datetime.now())
    speeches = speeches.filter(session=session).order_by("start_time",
                                                         "order")
    speeches_ids = list(speeches.values_list("id_parladata", flat=True))

    created_for = session.start_time.strftime(API_DATE_FORMAT)
    created_at = datetime.today().strftime(API_DATE_FORMAT)

    return JsonResponse({"session": session.getSessionData(),
                         "created_for": created_for,
                         "created_at": created_at,
                         "results": speeches_ids})


def getSessionSpeeches(request, session_id):
    out = []
    session = Session.objects.get(id_parladata=session_id)
    speeches = Speech.getValidSpeeches(datetime.now())
    for speech in speeches.filter(session=session).order_by("start_time",
                                                            "order"):
        out.append({"speech_id": speech.id_parladata,
                    "content": speech.content,
                    "person_id": speech.person.id_parladata})
    result = {
        'session': session.getSessionData(),
        'created_for': session.start_time.strftime(API_DATE_FORMAT),
        'created_at': datetime.today().strftime(API_DATE_FORMAT),
        'results': out
    }
    return JsonResponse(result, safe=False)


def setMotionOfSession(request, id_se):
    motion = tryHard(API_URL + '/motionOfSession/'+str(id_se)+'/').json()
    session = Session.objects.get(id_parladata=id_se)
    tab = []
    yes = 0
    no = 0
    kvorum = 0
    not_present = 0
    option = ""
    tyes = []
    for mot in motion:
        url = API_URL + '/getVotesOfMotion/' + str(mot['vote_id']) + '/'
        votes = tryHard(url).json()
        for vote in votes:
            if vote['option'] == str('za'):
                yes = yes + 1
            if vote['option'] == str('proti'):
                no = no + 1
            if vote['option'] == str('kvorum'):
                kvorum = kvorum + 1
            if vote['option'] == str('ni'):
                not_present = not_present + 1

        if Vote.objects.filter(id_parladata=mot['vote_id']):
            Vote.objects.filter(id_parladata=mot['vote_id']).update(created_for=session.start_time,
                                                                    session=session,
                                                                    motion=mot['text'],
                                                                    tags=mot['tags'],
                                                                    votes_for=yes,
                                                                    against=no,
                                                                    abstain=kvorum,
                                                                    not_present=not_present,
                                                                    result=resultOfMotion(yes, no, kvorum, not_present, mot['id'], session.start_time),
                                                                    id_parladata=mot['vote_id'],
                                                                    )
        else:
            result = saveOrAbortNew(model=Vote,
                                       created_for=session.start_time,
                                       session=session,
                                       motion=mot['text'],
                                       tags=mot['tags'],
                                       votes_for=yes,
                                       against=no,
                                       abstain=kvorum,
                                       not_present=not_present,
                                       result=resultOfMotion(yes, no, kvorum, not_present, mot['id'], session.start_time),
                                       id_parladata=mot['vote_id'],
                                       )

        yes = 0
        no = 0
        kvorum = 0
        not_present = 0
    return JsonResponse({'alliswell': True})


def setMotionOfSessionGraph(request, id_se):
    motion = tryHard(API_URL + '/motionOfSession/'+str(id_se)+'/').json()
    session = Session.objects.get(id_parladata=id_se)
    tab = []
    yes = 0
    no = 0
    kvorum = 0
    not_present = 0
    option = ""
    tabyes = []
    tabno = []
    tabkvo = []
    tabnp = []
    yesdic = defaultdict(int)
    nodic = defaultdict(int)
    kvordic = defaultdict(int)
    npdic = defaultdict(int)
    tyes = []
    for mot in motion:
        url = API_URL + '/getVotesOfMotion/'+str(mot['vote_id'])+'/'
        votes = tryHard(url).json()
        for vote in votes:
            if vote['option'] == str('za'):
                yes = yes + 1
                yesdic[vote['pg_id']] += 1
                tabyes.append(vote['mp_id'])
            if vote['option'] == str('proti'):
                no = no + 1
                nodic[vote['pg_id']] += 1
                tabno.append(vote['mp_id'])

            if vote['option'] == str('kvorum'):
                kvorum = kvorum + 1
                kvordic[vote['pg_id']] += 1
                tabkvo.append(vote['mp_id'])
            if vote['option'] == str('ni'):
                not_present = not_present + 1
                npdic[vote['pg_id']] += 1
                tabnp.append(vote['mp_id'])

        if Vote_graph.objects.filter(vote__id_parladata=mot['vote_id']):
            Vote_graph.objects.filter(vote__id_parladata=mot['vote_id']).update(
                        session=session,
                        vote=Vote.objects.get(id_parladata=mot['vote_id']),
                        created_for=session.start_time,
                        motion=mot['text'],
                        votes_for=yes,
                        against=no,
                        abstain=kvorum,
                        not_present=not_present,
                        result=resultOfMotion(yes, no, kvorum, not_present, mot['id'], session.start_time),
                        pgs_yes=yesdic,
                        pgs_no=nodic,
                        pgs_np=npdic,
                        pgs_kvor=kvordic,
                        mp_yes=tabyes,
                        mp_no=tabno,
                        mp_np=tabnp,
                        mp_kvor=tabkvo,
                        )
        else:
            vg = saveOrAbortNew(model=Vote_graph,
                         session=session,
                         vote=Vote.objects.get(id_parladata=mot['vote_id']),
                         created_for=session.start_time,
                         motion=mot['text'],
                         votes_for=yes,
                         against=no,
                         abstain=kvorum,
                         not_present=not_present,
                         result=resultOfMotion(yes, no, kvorum, not_present, mot['id'], session.start_time),
                         pgs_yes=yesdic,
                         pgs_no=nodic,
                         pgs_np=npdic,
                         pgs_kvor=kvordic,
                         mp_yes=tabyes,
                         mp_no=tabno,
                         mp_np=tabnp,
                         mp_kvor=tabkvo
                         )

        yes = 0
        no = 0
        kvorum = 0
        not_present = 0
        tabyes = []
        tabno = []
        tabkvo = []
        tabnp = []
        yesdic = defaultdict(int)
        nodic = defaultdict(int)
        kvordic = defaultdict(int)
        npdic = defaultdict(int)
    return JsonResponse({'alliswell': True})

def getMotionOfSession(request, id_se, date=False):
    out = []
    created_at = None
    if Session.objects.filter(id_parladata=int(id_se)):
        session = Session.objects.get(id_parladata=int(id_se))
        if Vote.objects.filter(session__id_parladata=id_se):
            if date:
                model = Vote.objects.filter(session__id_parladata=id_se, start_time__lte=datetime.strptime(date, '%d.%m.%Y'))
            else:
                model = Vote.objects.filter(session__id_parladata=id_se)
            dates = []
            for card in model:
                print card
                out.append({
                'session': session.getSessionData(),
                'results': {

                        'motion_id': card.id_parladata,
                        'text': card.motion,
                        'votes_for': card.votes_for,
                        'against': card.against,
                        'abstain': card.abstain,
                        'not_present':card.not_present,
                        'result':card.result}
                })
                dates.append(card.created_at)
            created_at = max(dates).strftime(API_DATE_FORMAT)
        else:
            out = []
        return JsonResponse({"results": out,
                             "session": session.getSessionData(),
                             "created_for": session.start_time.strftime(API_DATE_FORMAT),
                             "created_at": created_at}, safe=False)
    else:
        return JsonResponse({'result':'No session'})

def getMotionOfSessionVotes(request, votes):
    out = []
    votes = votes.split(',')
    for vote in votes:
        if Vote.objects.filter(id_parladata=vote):
            vot = Vote.objects.get(id_parladata=vote)
            out.append({
                'created_for': vot.created_for,
                'session': vot.session.getSessionData(),
                'results': {

                        'motion_id': vot.id_parladata,
                        'text': vot.motion,
                        'votes_for': vot.votes_for,
                        'against': vot.against,
                        'abstain': vot.abstain,
                        'not_present':vot.not_present,
                        'result':vot.result}
                })
        else:
            out.append({'Error': "No vote"})
            return JsonResponse(out, safe=False)
    return JsonResponse(out, safe=False)

def getMotionGraph(request, id_mo, date=False):
    out = []
    if Vote_graph.objects.filter(vote__id_parladata=id_mo):
        if date:
            model = Vote_graph.objects.filter(vote__id_parladata=id_mo, start_time__lte=datetime.strptime(date, '%d.%m.%Y'))
        else:
            model = Vote_graph.objects.filter(vote__id_parladata=id_mo)


        option_for = []
        option_kvor = []
        option_against = []
        option_np = []
        breakdown = []
        mps =[]


        for pg in model[0].pgs_kvor:
            party = Organization.objects.get(id_parladata=pg).getOrganizationData()

            for mp in model[0].mp_kvor:
                persondata = getPersonData(mp, date)

                if persondata['party']['acronym'] == party['acronym']:
                    mps.append(persondata)
            if mps:
                option_kvor.append({'pg': party, 'mps': mps})

            mps = []

        out_kvor = {'option':'kvorum','total_votes': model[0].abstain, 'breakdown':option_kvor}

        for pg in model[0].pgs_yes:
            party = Organization.objects.get(id_parladata=pg).getOrganizationData()

            for mp in model[0].mp_yes:
                persondata = getPersonData(mp, date)

                if persondata['party']['acronym'] == party['acronym']:
                    mps.append(persondata)
            if mps:
                option_for.append({'pg': party, 'mps': mps})

            mps = []

        out_for = {'option':'for','total_votes': model[0].votes_for, 'breakdown':option_for}

        for pg in model[0].pgs_no:
            party = Organization.objects.get(id_parladata=pg).getOrganizationData()
            for mp in model[0].mp_no:
                persondata = getPersonData(mp, date)

                if persondata['party']['acronym'] == party['acronym']:
                    mps.append(persondata)
            if mps:
                option_against.append({'pg': party, 'mps': mps})

            mps = []

        out_against = {'option':'against','total_votes': model[0].against, 'breakdown':option_against}

        for pg in model[0].pgs_np:
            party = Organization.objects.get(id_parladata=pg).getOrganizationData()
            for mp in model[0].mp_np:
                persondata = getPersonData(mp, date)

                if persondata['party']['acronym'] == party['acronym']:
                    mps.append(persondata)
            if mps:
                option_np.append({'pg': party, 'mps': mps})

            mps = []

        out_np = {'option':'not_present','total_votes': model[0].not_present, 'breakdown':option_np}

        out = {'id':id_mo,
               'created_for': model[0].vote.created_for.strftime(API_DATE_FORMAT),
               'created_at': model[0].created_at.strftime(API_DATE_FORMAT),
               'name': model[0].motion, 
               'result':model[0].result, 
               'required':'62', #TODO: naji pravo stvar za ta 62 :D
               'all': {'kvorum': out_kvor, 
                       'for': out_for, 
                       'against': out_against, 
                       'not_present': out_np}}
        return JsonResponse(out, safe=False)
    else:
        raise Http404("Nismo našli kartice")

def setAbsentMPs(request, id_se):
    votes = tryHard(API_URL + '/getVotesOfSession/'+str(id_se)+'/').json()
    session = Session.objects.get(id_parladata=id_se)
    mps = tryHard(API_URL+'/getMembersOfPGsOnDate/'+ session.start_time.strftime(API_DATE_FORMAT)).json()


    mpsID = []
    if len(votes) != 0:
        mpsID = reduce(lambda x,y: x+y,mps.values())
        for vote in votes:
            if vote['option'] != 'ni':
                if vote['mp_id'] in mpsID:
                    mpsID.remove(vote['mp_id'])

        result = saveOrAbortNew(model=AbsentMPs,
                                session=session,
                                absentMPs=mpsID,
                                created_for=session.start_time
                                )

        mpsID = []
    return JsonResponse({'alliswell': True})


def getAbsentMPs(request, id_se, date=False):
    session = get_object_or_404(Session, id_parladata=id_se)
    try:
        if date:
            date_ = datetime.strptime(date, API_DATE_FORMAT)
            absentMembers = AbsentMPs.objects.get(session=session, start_time__lte=data_)
        else:
            absentMembers = AbsentMPs.objects.get(session=session)
            date_ = datetime.now().date()
            date = date_.strftime(API_DATE_FORMAT)
        results = []

        for abMP in absentMembers.absentMPs:
            result = {
            "person": getPersonData(abMP, date)
            }
            results.append(result)

    except ObjectDoesNotExist:
        raise Http404("Nismo našli kartice")
    return JsonResponse({"results": results,
                         "session": session.getSessionData(),
                         "created_at": absentMembers.created_at.strftime(API_DATE_FORMAT),
                         "created_for": absentMembers.created_for.strftime(API_DATE_FORMAT)}, safe=False)

def setPresenceOfPG(request, id_se):
    votes = tryHard(API_URL+'/getVotesOfSession/'+str(id_se)+'/').json()
    motions = tryHard(API_URL+'/motionOfSession/'+str(id_se)+'/').json()
    session = Session.objects.get(id_parladata=id_se)
    membersOfPG = tryHard(API_URL+'/getMembersOfPGsOnDate/'+ session.start_time.strftime(API_DATE_FORMAT)).json()

    allTimePGs = tryHard(API_URL+'/getAllPGsExt/').json().keys()

    onSession = {}
    yesdic = defaultdict(int)
    allsessionsinone = defaultdict(list)
    final = {}
    numOfMPs = {}
    results = {}
    allPgs = {}

    if len(votes) != 0:
        for vote in votes:
            if vote['option'] != 'ni':
                if vote['mo_id'] in onSession.keys():
                    onSession[vote['mo_id']].append(vote['pg_id'])
                else:
                    onSession.update({vote['mo_id'] : [vote['pg_id']]})
    else:
        return JsonResponse({'alliswell': True, "status": "nothin to add"})

    counters = dict(Counter([item for sublist in onSession.values() for item in sublist]))

    for i in membersOfPG:
        allPgs[i] = len(membersOfPG[i]) * len(motions)
        print type(i), type(allTimePGs[1])
        if allPgs[i] == 0 or i not in allTimePGs:
            continue
        if int(i) in counters.keys():
            final[i] = int((float(counters[int(i)]) / float(allPgs[str(i)])) * 100)
        else:
            final[i] = 0



    """for b in onSession:
        for i in onSession[b]:
            yesdic[i] += 1
        results[b] = yesdic

    if len(results)>0:
        temp = dict(results[results.keys()[0]])
        for i in temp:
            if allPgs[str(i)] != 0:
                final[i] = int((float(temp[i]) / float(allPgs[str(i)])) * 100)
            else:
                final[i] = 0

        for pg in allPgs.keys():
            for result in results:"""





    result = saveOrAbortNew(model=PresenceOfPG,
                            created_for=session.start_time,
                            presence=[final],
                            session = session
                            )

    return JsonResponse({'alliswell': True})

def getPresenceOfPG(request, id_se, date=False):
    results = []
    try:
        if date:
            presence = PresenceOfPG.objects.get(session__id_parladata=id_se, start_time__lte=datetime.strptime(date, '%d.%m.%Y'))
        else:
            presence = PresenceOfPG.objects.get(session__id_parladata=id_se)

            for p in presence.presence[0]:
                results.append({"organization": Organization.objects.get(id_parladata=p).getOrganizationData(), "percent": presence.presence[0][p]})
            results = sorted(results, key=lambda k: k['percent'], reverse=True)
    except ObjectDoesNotExist:
        raise Http404("Nismo našli kartice")
    return JsonResponse({"results": results,
                         "created_for": presence.created_for.strftime(API_DATE_FORMAT),
                         "created_at": presence.created_at.strftime(API_DATE_FORMAT),
                         "session": presence.session.getSessionData()}, 
                        safe=False)


def setSpeechesOnSession(request, date=False):
    if date:
        numberOfSessions = len(Session.objects.filter(start_time__lte=datetime.strptime(date, '%d.%m.%Y')))
        mps = tryHard(API_URL+'/getMPs/'+ date).json()
    else:
        numberOfSessions = len(Session.objects.filter(start_time__lte=datetime.now().date()).json())
        mps = tryHard(API_URL+'/getMPs/'+  str(datetime.now().date().strftime(API_DATE_FORMAT))).json()
        date = datetime.now().date()

    mpsID = {}
    for mp in mps:
        url = API_URL + '/getSpeechesOfMP/' + str(mp['id'])+'/' + date
        speech = len(tryHard(url).json())
        if numberOfSessions != 0:
            mpsID.update({mp['id']: float(float(speech)/float(numberOfSessions))})
    date = datetime.strptime(date, '%d.%m.%Y')
    result = saveOrAbortNew(model=AverageSpeeches,
                            created_for=date,
                            speechesOnSession=mpsID)
    return JsonResponse({'alliswell': True})


def getMinSpeechesOnSession(request, date=False):
    results = []
    try:
        if date:
            date_ = datetime.strptime(date, API_DATE_FORMAT)
            averageSpeeches = AverageSpeeches.objects.filter(created_for__lte=date_).latest("created_for").speechesOnSession
        else:
            averageSpeeches = AverageSpeeches.objects.latest("created_for").speechesOnSession
            date_ = datetime.now().date()
            date = date_.strftime(API_DATE_FORMAT)
        sort = sorted(averageSpeeches.items(), key=lambda x:x[1])

        for s in sort:
            result = {
                "person": getPersonData(s[0], date),
                'speeches': s[1]
            }
            results.append(result)
    except ObjectDoesNotExist:
        return JsonResponse({"status": "No card MOFO"}, safe=False)
    return JsonResponse(results[:5], safe=False)


def getMaxSpeechesOnSession(request, date=False):
    results = []
    try:
        if date:
            date_ = datetime.strptime(date, API_DATE_FORMAT)
            averageSpeeches = AverageSpeeches.objects.filter(created_for__lte=date_).latest("created_for").speechesOnSession
        else:
            averageSpeeches = AverageSpeeches.objects.latest("created_for").speechesOnSession
            date_ = datetime.now().date()
            date = date_.strftime(API_DATE_FORMAT)


        sort = sorted(averageSpeeches.items(), key=lambda x:x[1], reverse=True)
        for s in sort:
            result = {
                "person": getPersonData(s[0], date),
                'speeches': s[1]
            }
            results.append(result)

    except ObjectDoesNotExist:
        return JsonResponse({"status": "No card MOFO"}, safe=False)
    return JsonResponse(results[:5], safe=False)


def setQuote(request, speech_id, start_pos, end_pos):
    speech = get_object_or_404(Speech, id_parladata=speech_id)
    quote = Quote(speech=speech, first_char=start_pos, last_char=end_pos, quoted_text=re.sub(r"\n+", " ", speech.content.strip())[int(start_pos):int(end_pos)].strip())
    quote.save()

    return JsonResponse({"status": "alliswell", "id": quote.id})


def getQuote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    return JsonResponse({"person": getPersonData(quote.speech.person.id_parladata, quote.speech.session.start_time.strftime(API_DATE_FORMAT)),
                         "created_for": quote.created_at.strftime(API_DATE_FORMAT),
                         "created_at": quote.created_at.strftime(API_DATE_FORMAT),
                         "results": {"quoted_text": quote.quoted_text,
                                     "start_idx": quote.first_char,
                                     "end_idx": quote.last_char,
                                     "speech_id": quote.speech.id_parladata,
                                     "content": quote.speech.content,
                                     'session': quote.speech.session.getSessionData(),
                                     'quote_id': quote.id}})


def getLastSessionLanding(request, date_=None):
    if date_:
        fdate = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        fdate=datetime.now().today()
    ready = False
    presences = PresenceOfPG.objects.filter(created_for__lte=fdate).order_by("-created_for")
    if not presences:
        raise Http404("Nismo našli kartice")
    presence_index = 0
    motions = None
    presence = None

    while not ready:
        print presence_index
        presence = presences[presence_index]
        motions = json.loads(getMotionOfSession(None, presence.session.id_parladata).content)
        if type(motions) == dict:
            if "results" in motions.keys():
                # tfidf = tryHard("https://isci.parlameter.si/tfidf/s/"+str(presence.session.id_parladata))
                # if tfidf.status_code == 200:
                tfidf = json.loads(getTFIDF(None, presence.session.id_parladata).content)
                if tfidf["results"]:
                    ready = True
                else:
                    presence_index += 1
        else:
            presence_index += 1

    results = [{"org":Organization.objects.get(id_parladata=p).getOrganizationData(),
                                "percent":presence.presence[0][p],} for p in presence.presence[0]]
    result = sorted(results, key=lambda k: k['percent'], reverse=True)
    session = Session.objects.get(id_parladata=int(presence.session.id_parladata))
    return JsonResponse({"session": session.getSessionData(),
                         "created_for": session.start_time.strftime(API_DATE_FORMAT),
                         "created_at": datetime.today().strftime(API_DATE_FORMAT),
                         "presence": result,
                         "motions": motions["results"],
                         "tfidf": tfidf}, safe=False)


def getSessionsByClassification(request):
    COUNCIL_ID = 9
    DZ = 95
    working_bodies = ["odbor", "komisija", "preiskovalna komisija"]
    out = {"kolegij": [session.getSessionData() for session in Session.objects.filter(organization__id_parladata=COUNCIL_ID).order_by("-start_time")],
           "dz": [session.getSessionData() for session in Session.objects.filter(organization__id_parladata=DZ).order_by("-start_time")],
           "dt": [org.getOrganizationData() for org in Organization.objects.filter(classification__in=working_bodies)],}

    for dt in out["dt"]:
        dt["sessions"] = [session.getSessionData() for session in Session.objects.filter(organization__id_parladata=dt["id"]).order_by("-start_time")]
        for session in dt["sessions"]:
            session.update({"votes": True if Vote.objects.filter(session__id_parladata=session["id"]) else False, 
                            "speeches": True if Speech.objects.filter(session__id_parladata=session["id"]) else False})

    for session in out["kolegij"]:
        session.update({"votes": True if Vote.objects.filter(session__id_parladata=session["id"]) else False, 
                        "speeches": True if Speech.objects.filter(session__id_parladata=session["id"]) else False})

    for session in out["dz"]:
        session.update({"votes": True if Vote.objects.filter(session__id_parladata=session["id"]) else False, 
                        "speeches": True if Speech.objects.filter(session__id_parladata=session["id"]) else False})

    return JsonResponse(out)


def getSessionsList(request, date_=None, force_render=False):
    COUNCIL_ID = 9
    DZ = 95
    working_bodies = ['odbor', 'komisija', 'preiskovalna komisija']
    if date_:
        date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
        key = date_
    else:
        date_of = datetime.now().date()
        date_ = date_of.strftime(API_DATE_FORMAT)
        key = date_

    out = cache.get("sessions_list_" + key)
    if out and not force_render:
        data = out
    else:
        orgs = Organization.objects.filter(Q(organization__id_parladata=COUNCIL_ID) |
                                           Q(organization__id_parladata=DZ) |
                                           Q(classification__in=working_bodies))
        sessions = Session.objects.filter(organization__in=orgs)
        sessions = sessions.order_by("-start_time")
        out = {'sessions': [session.getSessionData() for session in sessions],
               'created_for': datetime.now().strftime(API_DATE_FORMAT),
               'created_at': datetime.now().strftime(API_DATE_FORMAT)}

        for session in out["sessions"]:
            act = Activity.objects.filter(session__id_parladata=session['id'])
            if act:
                last_day = act.latest('updated_at').updated_at.strftime(API_DATE_FORMAT)
            else:
                last_day = session['date']
            session.update({"updated_at": last_day})
        cache.set("sessions_list_" + key, out, 60 * 60 * 48)

    return JsonResponse(out)


def setTFIDF(request, session_id):
    date_of = datetime.now().date()
    url = "https://isci.parlameter.si/tfidf/s/"+str(session_id)
    data = tryHard(url).json()
    session = Session.objects.get(id_parladata=session_id)
    is_saved = saveOrAbortNew(Tfidf,
                              session=session,
                              created_for=date_of,
                              is_visible=False,
                              data=data["results"])

    return JsonResponse({"alliswell": True,
                         "saved": is_saved})


def getTFIDF(request, session_id):
    card = Tfidf.objects.filter(session__id_parladata=session_id,
                                is_visible=True)
    if card:
        card = card.latest("created_at")
        out = {
            'session': card.session.getSessionData(),
            'results': card.data,
            "created_for": card.created_for.strftime(API_DATE_FORMAT),
            "created_at": card.created_at.strftime(API_DATE_FORMAT)
        }
    else:
        date_of = datetime.now().date()
        if Session.objects.filter(id_parladata=session_id):
            out = {
                'session': Session.objects.get(id_parladata=session_id).getSessionData(),
                'results': [],
                "created_for": date_of.strftime(API_DATE_FORMAT),
                "created_at": date_of.strftime(API_DATE_FORMAT)
            }
        else:
            out = {
                'session': None,
                'results': [],
                "created_for": date_of.strftime(API_DATE_FORMAT),
                "created_at": date_of.strftime(API_DATE_FORMAT)
            }

    return JsonResponse(out)
