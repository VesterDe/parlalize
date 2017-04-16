# -*- coding: UTF-8 -*-
from datetime import datetime
from parlalize.utils import *
import json
from django.http import JsonResponse
from parlaseje.models import *
from parlalize.settings import API_URL, API_DATE_FORMAT
from parlaseje.utils import *
from collections import defaultdict, Counter
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
import re
from django.db.models import Q
from django.core.cache import cache
from parlalize.utils import tryHard


def getSpeech(request, speech_id):
    """
    * @api {get} /getSpeech/{speech_id} Requests information of Speech
    * @apiName GetSpeech
    * @apiGroup Session
    *
    * @apiParam {speech_id} speech id is parameter which returns
    *exactly specified speech
    * @apiSuccess {Json} returns detiled data of specific speech
    * 
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getSpeech/1118139
    * @apiSuccessExample {json} Example response:
    {
    "person": {
    "is_active": false,
    "district": [
    103
    ],
    "name": "Violeta Tomić",
    "gov_id": "P289",
    "gender": "f",
    "party": {
    "acronym": "ZL",
    "is_coalition": false,
    "id": 8,
    "name": "PS Združena Levica"
    },
    "type": "mp",
    "id": 80,
    "has_function": false
    },
    "created_at": "20.02.2017",
    "created_for": "09.02.2017",
    "results": {
    "quote_id": null,
    "content": "Spoštovani predsednik, hvala za besedo. Kolegice in kolegi! ...
    "session": {
    "name": "42. izredna seja",
    "date_ts": "2017-02-02T01:00:00",
    "orgs": [
    {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    }
    ],
    "date": "2. 2. 2017",
    "org": {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    },
    "id": 8972,
    "in_review": false
    },
    "quoted_text": null,
    "speech_id": 1118139,
    "end_idx": null,
    "start_idx": null
    }
    }
    """
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
    """
    * @api {get} /getSpeechesOfSession/{session_id} Requests information of speeches on session.
    * @apiName getSpeechesOfSession
    * @apiGroup Session
    *
    * @apiParam {session_id} session id is parameter which returns
    *specific session
    * @apiSuccess {Json} returns detiled data of all speeches on session.
    * 
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getSpeechesOfSession/9408
    * @apiSuccessExample {json} Example response:
    {
    "created_for": "05.04.2017",
    "session": {
    "name": "33. redna seja",
    "date_ts": "2017-04-05T02:00:00",
    "orgs": [
    {
    "acronym": "",
    "is_coalition": false,
    "id": 25,
    "name": "Odbor za pravosodje"
    }
    ],
    "date": "5. 4. 2017",
    "org": {
    "acronym": "",
    "is_coalition": false,
    "id": 25,
    "name": "Odbor za pravosodje"
    },
    "id": 9408,
    "in_review": true
    },
    "created_at": "16.04.2017",
    "results": [
    {
    "person": {
    "is_active": false,
    "district": [
    36
    ],
    "name": "Jan Škoberne",
    "gov_id": "P301",
    "gender": "m",
    "party": {
    "acronym": "SD",
    "is_coalition": true,
    "id": 7,
    "name": "PS Socialni Demokrati"
    },
    "type": "mp",
    "id": 1356,
    "has_function": false
    },
    "results": {
    "quote_id": null,
    "content": "Spoštovane kolegice in kolegi, dragi in cenjeni gostje, dobro jutro, dobrodošli! ...
    "session": {
    "name": "33. redna seja",
    "date_ts": "2017-04-05T02:00:00",
    "orgs": [
    {
    "acronym": "",
    "is_coalition": false,
    "id": 25,
    "name": "Odbor za pravosodje"
    }
    ],
    "date": "5. 4. 2017",
    "org": {
    "acronym": "",
    "is_coalition": false,
    "id": 25,
    "name": "Odbor za pravosodje"
    },
    "id": 9408,
    "in_review": true
    },
    "quoted_text": null,
    "speech_id": 1176731,
    "end_idx": null,
    "start_idx": null
    }
    },
    {
    "person": {
    "is_active": null,
    "district": null,
    "name": "Tina Brecelj",
    "gov_id": "G1373",
    "gender": null,
    "party": {
    "acronym": null,
    "is_coalition": null,
    "id": null,
    "name": null
    },
    "type": "visitor",
    "id": 1373,
    "has_function": false
    },
    "results": {
    "quote_id": null,
    "content": "Najlepša hvala gospod predsednik za besedo. Spoštovane poslanke, poslanci, spoštovani gostje,...
    "session": {
    "name": "33. redna seja",
    "date_ts": "2017-04-05T02:00:00",
    "orgs": [
    {
    "acronym": "",
    "is_coalition": false,
    "id": 25,
    "name": "Odbor za pravosodje"
    }
    ],
    "date": "5. 4. 2017",
    "org": {
    "acronym": "",
    "is_coalition": false,
    "id": 25,
    "name": "Odbor za pravosodje"
    },
    "id": 9408,
    "in_review": true
    },
    "quoted_text": null,
    "speech_id": 1176732,
    "end_idx": null,
    "start_idx": null
    }
    }
    }
    """
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
    """
    * @api {get} /getSpeechesIDsOfSession/{session_id} Requests IDs of all speeches on specific session.
    * @apiName getSpeechesIDsOfSession
    * @apiGroup Session
    *
    * @apiParam {session_id} session id is parameter which returns
    *specific session
    * @apiSuccess {Json} returns IDs of speeches on specific session
    * 
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getSpeechesIDsOfSession/9408
    * @apiSuccessExample {json} Example response:
    {
    "created_for": "05.04.2017",
    "session": {
    "name": "33. redna seja",
    "date_ts": "2017-04-05T02:00:00",
    "orgs": [
    {
    "acronym": "",
    "is_coalition": false,
    "id": 25,
    "name": "Odbor za pravosodje"
    }
    ],
    "date": "5. 4. 2017",
    "org": {
    "acronym": "",
    "is_coalition": false,
    "id": 25,
    "name": "Odbor za pravosodje"
    },
    "id": 9408,
    "in_review": true
    },
    "created_at": "16.04.2017",
    "results": [
    1176731,
    1176732,
    1176733,
    1176734,
    ...
    ]}
    """
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
    # pomoje se lahk zbrise
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


def setMotionOfSession(request, session_id):
    """Stores all motions with detiled data of specific sesison.
    """
    motion = tryHard(API_URL + '/motionOfSession/' + str(session_id) + '/').json()
    session = Session.objects.get(id_parladata=session_id)
    yes = 0
    no = 0
    kvorum = 0
    not_present = 0
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
        result = mot['result']
        if not str(result).strip().isdigit():
            result = resultOfMotion(yes,
                                    no,
                                    kvorum,
                                    not_present,
                                    mot['id'],
                                    session.start_time)

        if Vote.objects.filter(id_parladata=mot['vote_id']):
            vote = Vote.objects.filter(id_parladata=mot['vote_id'])
            vote.update(created_for=session.start_time,
                        session=session,
                        motion=mot['text'],
                        tags=mot['tags'],
                        votes_for=yes,
                        against=no,
                        abstain=kvorum,
                        not_present=not_present,
                        result=result,
                        id_parladata=mot['vote_id'],
                        document_url=mot['doc_url'],
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
                                    result=result,
                                    id_parladata=mot['vote_id'],
                                    document_url=mot['doc_url']
                                    )

        yes = 0
        no = 0
        kvorum = 0
        not_present = 0
    return JsonResponse({'alliswell': True})


def setMotionOfSessionGraph(request, session_id):
    """Stores all motions with detiled data of specific sesison.
    """
    motion = tryHard(API_URL + '/motionOfSession/' + str(session_id) + '/').json()
    session = Session.objects.get(id_parladata=session_id)
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
    for mot in motion:
        url = API_URL + '/getVotesOfMotion/' + str(mot['vote_id']) + '/'
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

        result = mot['result']
        if not str(result).strip().isdigit():
            result = resultOfMotion(yes,
                                    no,
                                    kvorum,
                                    not_present,
                                    mot['id'],
                                    session.start_time)
        vote = Vote.objects.get(id_parladata=mot['vote_id'])
        if VoteDetailed.objects.filter(vote__id_parladata=mot['vote_id']):
            voteDetailed = VoteDetailed.objects.filter(vote__id_parladata=mot['vote_id'])
            voteDetailed.update(session=session,
                                vote=vote,
                                created_for=session.start_time,
                                motion=mot['text'],
                                otes_for=yes,
                                against=no,
                                abstain=kvorum,
                                not_present=not_present,
                                result=result,
                                pgs_yes=yesdic,
                                pgs_no=nodic,
                                pgs_np=npdic,
                                pgs_kvor=kvordic,
                                mp_yes=tabyes,
                                mp_no=tabno,
                                mp_np=tabnp,
                                mp_kvor=tabkvo)
        else:
            vg = saveOrAbortNew(model=VoteDetailed,
                                session=session,
                                vote=vote,
                                created_for=session.start_time,
                                motion=mot['text'],
                                votes_for=yes,
                                against=no,
                                abstain=kvorum,
                                not_present=not_present,
                                result=result,
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


def getMotionOfSession(request, session_id, date=False):
    """
    * @api {get} /getMotionOfSession/{session_id}/{?date} Requests information of all motions on specific session.
    * @apiName getMotionOfSession
    * @apiGroup Session
    *
    * @apiParam {speech_id} session id is parameter which returns
    *exactly specified session
    * @apiSuccess {Json} returns detiled data of all motions on specific session
    * @apiParam {date} date Optional date.
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getMotionOfSession/9408
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/s/getMotionOfSession/9408/21.12.2016
    * @apiSuccessExample {json} Example response:
    {
    "created_at": null,
    "created_for": "05.04.2017",
    "session": {
    "name": "33. redna seja",
    "date_ts": "2017-04-05T02:00:00",
    "orgs": [
    {
    "acronym": "",
    "is_coalition": false,
    "id": 25,
    "name": "Odbor za pravosodje"
    }
    ],
    "date": "5. 4. 2017",
    "org": {
    "acronym": "",
    "is_coalition": false,
    "id": 25,
    "name": "Odbor za pravosodje"
    },
    "id": 9408,
    "in_review": true
    },
    "results": [],
    "tags": [
    "Komisija za nadzor javnih financ",
    "Kolegij predsednika Državnega zbora",
    "Komisija za narodni skupnosti",
    "Komisija za odnose s Slovenci v zamejstvu in po svetu",
    "Komisija za poslovnik",
    "Mandatno-volilna komisija",
    "Odbor za delo, družino, socialne zadeve in invalide",
    "Odbor za finance in monetarno politiko",
    "Odbor za gospodarstvo",
    "Odbor za infrastrukturo, okolje in prostor",
    "Odbor za izobraževanje, znanost, šport in mladino",
    "Odbor za kmetijstvo, gozdarstvo in prehrano",
    "Odbor za kulturo",
    "Odbor za notranje zadeve, javno upravo in lokalno samoupravo",
    "Odbor za obrambo",
    "Odbor za pravosodje",
    "Odbor za zadeve Evropske unije",
    "Odbor za zdravstvo",
    "Odbor za zunanjo politiko",
    "Preiskovalna komisija o ugotavljanju zlorab v slovenskem bančnem sistemu ter ugotavljanju vzrokov in",
    "Preiskovalna komisija za ugotavljanje politične odgovornosti nosilcev javnih funkcij pri investiciji",
    "Ustavna komisija",
    "Proceduralna glasovanja",
    "Zunanja imenovanja",
    "Poslanska vprašanja",
    "Komisija za nadzor obveščevalnih in varnostnih služb",
    "Preiskovalne komisije",
    "Komisija za peticije ter za človekove pravice in enake možnosti",
    "Interpelacija",
    " Preiskovalna komisija za ugotavljanje politične odgovornosti nosilcev javnih funkcij pri investicij"
    ]
    }
    """
    out = []
    created_at = None
    if Session.objects.filter(id_parladata=int(session_id)):
        session = Session.objects.get(id_parladata=int(session_id))
        if Vote.objects.filter(session__id_parladata=session_id):
            model = Vote.objects.filter(session__id_parladata=session_id)
            dates = []
            for card in model:
                print card
                out.append({'session': session.getSessionData(),
                            'results': {'motion_id': card.id_parladata,
                                        'text': card.motion,
                                        'votes_for': card.votes_for,
                                        'against': card.against,
                                        'abstain': card.abstain,
                                        'not_present': card.not_present,
                                        'result': card.result,
                                        }
                            })
                dates.append(card.created_at)
            created_at = max(dates).strftime(API_DATE_FORMAT)
        else:
            out = []
        ses_date = session.start_time.strftime(API_DATE_FORMAT)
        return JsonResponse({"results": out,
                             "session": session.getSessionData(),
                             "created_for": ses_date,
                             "created_at": created_at}, safe=False)
    else:
        return JsonResponse({'result': 'No session'})


def getMotionOfSessionVotes(request, votes):
    # pomoje se lahk izbrise
    out = []
    votes = votes.split(',')
    for vote in votes:
        if Vote.objects.filter(id_parladata=vote):
            vot = Vote.objects.get(id_parladata=vote)
            out.append({
                'created_for': vot.created_for,
                'session': vot.session.getSessionData(),
                'results': {'motion_id': vot.id_parladata,
                            'text': vot.motion,
                            'votes_for': vot.votes_for,
                            'against': vot.against,
                            'abstain': vot.abstain,
                            'not_present': vot.not_present,
                            'result': vot.result}
            })
        else:
            out.append({'Error': "No vote"})
            return JsonResponse(out, safe=False)
    return JsonResponse(out, safe=False)


def getMotionGraph(request, id_mo, date=False):
    """
    * @api {get} /getMotionGraph/{id_mo}/{?date} Requests information of specific motion.
    * @apiName getMotionGraph
    * @apiGroup Session
    *
    * @apiParam {id_mo} session id is parameter which returns
    *exactly specified motion
    * @apiParam {date} date Optional date.
    * @apiSuccess {Json} returns detiled data of motion
    * 
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getMotionGraph/6900
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/s/getMotionGraph/6900/21.12.2016
    * @apiSuccessExample {json} Example response:
    {
    "session": {
    "name": "28. redna seja",
    "date_ts": "2017-03-20T01:00:00",
    "orgs": [
    {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    }
    ],
    "date": "20. 3. 2017",
    "org": {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    },
    "id": 9379,
    "in_review": true
    },
    "all": {
    "kvorum": {
    "breakdown": [],
    "option": "kvorum",
    "total_votes": 0
    },
    "not_present": {},
    "against": {},
    "for": {}
    },
    "created_for": "20.03.2017",
    "name": "Dnevni red v celoti",
    "documents": [],
    "created_at": "21.03.2017",
    "required": "62",
    "id": "6900",
    "result": true
    }
    """
    out = []
    if VoteDetailed.objects.filter(vote__id_parladata=id_mo):
        if date:
            model = VoteDetailed.objects.filter(vote__id_parladata=id_mo,
                                                start_time__lte=datetime.strptime(date, '%d.%m.%Y'))
        else:
            model = VoteDetailed.objects.filter(vote__id_parladata=id_mo)

        option_for = []
        option_kvor = []
        option_against = []
        option_np = []
        mps = []

        for pg in model[0].pgs_kvor:
            party = Organization.objects.get(id_parladata=pg).getOrganizationData()

            for mp in model[0].mp_kvor:
                persondata = getPersonData(mp, date)

                if persondata['party']['acronym'] == party['acronym']:
                    mps.append(persondata)
            if mps:
                option_kvor.append({'pg': party, 'mps': mps})

            mps = []

        out_kvor = {'option': 'kvorum',
                    'total_votes': model[0].abstain,
                    'breakdown': option_kvor}

        for pg in model[0].pgs_yes:
            party = Organization.objects.get(id_parladata=pg).getOrganizationData()

            for mp in model[0].mp_yes:
                persondata = getPersonData(mp, date)

                if persondata['party']['acronym'] == party['acronym']:
                    mps.append(persondata)
            if mps:
                option_for.append({'pg': party, 'mps': mps})

            mps = []

        out_for = {'option': 'for',
                   'total_votes': model[0].votes_for,
                   'breakdown': option_for}

        for pg in model[0].pgs_no:
            party = Organization.objects.get(id_parladata=pg).getOrganizationData()
            for mp in model[0].mp_no:
                persondata = getPersonData(mp, date)

                if persondata['party']['acronym'] == party['acronym']:
                    mps.append(persondata)
            if mps:
                option_against.append({'pg': party, 'mps': mps})

            mps = []

        out_against = {'option': 'against',
                       'total_votes': model[0].against,
                       'breakdown': option_against}

        for pg in model[0].pgs_np:
            party = Organization.objects.get(id_parladata=pg).getOrganizationData()
            for mp in model[0].mp_np:
                persondata = getPersonData(mp, date)

                if persondata['party']['acronym'] == party['acronym']:
                    mps.append(persondata)
            if mps:
                option_np.append({'pg': party, 'mps': mps})

            mps = []

        out_np = {'option': 'not_present',
                  'total_votes': model[0].not_present,
                  'breakdown': option_np}

        out = {'id': id_mo,
               'created_for': model[0].vote.created_for.strftime(API_DATE_FORMAT),
               'created_at': model[0].created_at.strftime(API_DATE_FORMAT),
               'name': model[0].motion,
               'result': model[0].result,
               'documents': model[0].vote.document_url,
               'required': '62',
               'all': {'kvorum': out_kvor,
                       'for': out_for,
                       'against': out_against,
                       'not_present': out_np},
               'session': model[0].session.getSessionData()}
        return JsonResponse(out, safe=False)
    else:
        raise Http404("Nismo našli kartice")


def setAbsentMPs(request, session_id):
    """Stores absent MPs of specific session
    """
    votes = tryHard(API_URL + '/getVotesOfSession/' + str(session_id) + '/').json()
    session = Session.objects.get(id_parladata=session_id)
    mps = tryHard(API_URL + '/getMembersOfPGsOnDate/' + session.start_time.strftime(API_DATE_FORMAT)).json()

    mpsID = []
    if len(votes) != 0:
        mpsID = reduce(lambda x, y: x + y, mps.values())
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


def getAbsentMPs(request, session_id, date=False):
    # Ne uporabljamo damo ven?
    """
    * @api {get} /getAbsentMPs/{session_id}/{?date} Requests information of all absent MPs on specific sesion.
    * @apiName getAbsentMPs
    * @apiGroup Session
    *
    * @apiParam {session_id} session id is parameter which returns
    *exactly specified session
    * @apiParam {date} date Optional date.
    * @apiSuccess {Json} returns data of all absent MPs on specific session.
    * 
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getAbsentMPs/9408
    * @apiExample {curl} Example with date:
        curl -i hhttps://analize.parlameter.si/v1/s/getAbsentMPs/9408/21.12.2016
    * @apiSuccessExample {json} Example response:

    """
    session = get_object_or_404(Session, id_parladata=session_id)
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
            result = {"person": getPersonData(abMP, date)}
            results.append(result)

    except ObjectDoesNotExist:
        raise Http404("Nismo našli kartice")
    return JsonResponse({"results": results,
                         "session": session.getSessionData(),
                         "created_at": absentMembers.created_at.strftime(API_DATE_FORMAT),
                         "created_for": absentMembers.created_for.strftime(API_DATE_FORMAT)}, safe=False)


def setPresenceOfPG(request, session_id):
    """ Stores presence of PGs on specific session
    """
    votes = tryHard(API_URL + '/getVotesOfSession/' + str(session_id) + '/').json()
    motions = tryHard(API_URL + '/motionOfSession/' + str(session_id) + '/').json()
    session = Session.objects.get(id_parladata=session_id)
    membersOfPG = tryHard(API_URL + '/getMembersOfPGsOnDate/' + session.start_time.strftime(API_DATE_FORMAT)).json()

    allTimePGs = tryHard(API_URL + '/getAllPGsExt/').json().keys()

    onSession = {}
    final = {}
    allPgs = {}

    if len(votes) != 0:
        for vote in votes:
            if vote['option'] != 'ni':
                if vote['mo_id'] in onSession.keys():
                    onSession[vote['mo_id']].append(vote['pg_id'])
                else:
                    onSession.update({vote['mo_id']: [vote['pg_id']]})
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

    result = saveOrAbortNew(model=PresenceOfPG,
                            created_for=session.start_time,
                            presence=[final],
                            session=session)

    return JsonResponse({'alliswell': True})


def getPresenceOfPG(request, session_id, date=False):
    """
    * @api {get} /getPresenceOfPG/{session_id}/{?date} Requests information of presence of PGs on specific session
    * @apiName getPresenceOfPG
    * @apiGroup Session
    *
    * @apiParam {session_id} session id is parameter which returns
    *exactly specified session
    * @apiParam {date} date Optional date.
    * @apiSuccess {Json} returns data presence of PGs on specific session
    * 
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getPresenceOfPG/9379
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/s/getPresenceOfPG/9379/21.12.2016
    * @apiSuccessExample {json} Example response:
    {
    "session": {
    "name": "28. redna seja",
    "date_ts": "2017-03-20T01:00:00",
    "orgs": [
    {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    }
    ],
    "date": "20. 3. 2017",
    "org": {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    },
    "id": 9379,
    "in_review": true
    },
    "created_at": "12.04.2017",
    "created_for": "20.03.2017",
    "results": [
    {
    "organization": {
    "acronym": "IMNS",
    "is_coalition": false,
    "id": 2,
    "name": "PS italijanske in madžarske narodne skupnosti"
    },
    "percent": 96
    },
    ...
    ]
    }
    """
    results = []
    try:
        if date:
            presence = PresenceOfPG.objects.get(session__id_parladata=session_id,
                                                start_time__lte=datetime.strptime(date, '%d.%m.%Y'))
        else:
            presence = PresenceOfPG.objects.filter(session__id_parladata=session_id)
            presence = presence.latest("created_at")

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
    """ Stores all speeches of all MPs.
    """
    if date:
        numberOfSessions = len(Session.objects.filter(start_time__lte=datetime.strptime(date, '%d.%m.%Y')))
        mps = tryHard(API_URL + '/getMPs/' + date).json()
    else:
        numberOfSessions = len(Session.objects.filter(start_time__lte=datetime.now().date()).json())
        mps = tryHard(API_URL + '/getMPs/' + str(datetime.now().date().strftime(API_DATE_FORMAT))).json()
        date = datetime.now().date()

    mpsID = {}
    for mp in mps:
        url = API_URL + '/getSpeechesOfMP/' + str(mp['id']) + '/' + date
        speech = len(tryHard(url).json())
        if numberOfSessions != 0:
            mpsID.update({mp['id']: float(float(speech) / float(numberOfSessions))})
    date = datetime.strptime(date, '%d.%m.%Y')
    result = saveOrAbortNew(model=AverageSpeeches,
                            created_for=date,
                            speechesOnSession=mpsID)
    return JsonResponse({'alliswell': True})


def getMinSpeechesOnSession(request, date=False):
    """
    * @api {get} /getMinSpeechesOnSession/{?date} Requests data who has the less speeches on sessions.
    * @apiName getMinSpeechesOnSession
    * @apiGroup Session
    * @apiParam {date} date Optional date.
    * @apiSuccess {Json} returns data who has the less speeches on sessions.
    * 
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getMinSpeechesOnSession
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/s/getMinSpeechesOnSession/21.12.2016
    * @apiSuccessExample {json} Example response:
    [
    {
    "person": {
    "is_active": false,
    "district": [
    84
    ],
    "name": "Vlasta Počkaj",
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
    "speeches": 0.0007552870090634441
    },
    {
    "person": {
    "is_active": false,
    "district": [
    85
    ],
    "name": "Teja Ljubič",
    "gov_id": "P304",
    "gender": "f",
    "party": {
    "acronym": "SMC",
    "is_coalition": true,
    "id": 1,
    "name": "PS Stranka modernega centra"
    },
    ...
    ]
    """
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
    """
    * @api {get} /getMaxSpeechesOnSession/{?date} Requests data who has the most speeches on sessions.
    * @apiName getMaxSpeechesOnSession
    * @apiGroup Session
    * @apiParam {date} date Optional date.
    * @apiSuccess {Json} returns data who has the most speeches on sessions.
    * 
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getMaxSpeechesOnSession
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/s/getMaxSpeechesOnSession/21.12.2016
    * @apiSuccessExample {json} Example response:
    [
    {
    "person": {
    "is_active": false,
    "district": [
    76
    ],
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
    },
    "speeches": 6.601963746223565
    },
    {
    "person": {
    "is_active": false,
    "district": [
    93
    ],
    "name": "Primož Hainz",
    "gov_id": "P255",
    "gender": "m",
    "party": {
    "acronym": "DeSUS",
    "is_coalition": true,
    "id": 3,
    "name": "PS Demokratska Stranka Upokojencev Slovenije"
    },
    "type": "mp",
    "id": 29,
    "has_function": true
    },
    "speeches": 3.270392749244713
    },
    ...
    ]
    """
    results = []
    try:
        if date:
            date_ = datetime.strptime(date, API_DATE_FORMAT)
            averageSpeeches = AverageSpeeches.objects.filter(created_for__lte=date_).latest("created_for").speechesOnSession
        else:
            averageSpeeches = AverageSpeeches.objects.latest("created_for").speechesOnSession
            date_ = datetime.now().date()
            date = date_.strftime(API_DATE_FORMAT)

        sort = sorted(averageSpeeches.items(), key=lambda x: x[1], reverse=True)
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
    """Stores quotes of specific speech.
    """
    speech = get_object_or_404(Speech, id_parladata=speech_id)
    quote = Quote(speech=speech,
                  first_char=start_pos,
                  last_char=end_pos,
                  quoted_text=re.sub(r"\n+", " ", speech.content.strip())[int(start_pos):int(end_pos)].strip())
    quote.save()

    return JsonResponse({"status": "alliswell", "id": quote.id})


def getQuote(request, quote_id):
    """
    * @api {get} /getQuote/{quote_id} Requests specific quote of speech.
    * @apiName getQuote
    * @apiGroup Session
    *
    * @apiParam {quote_id} quote id is parameter which returns
    *exactly specified quote
    * @apiSuccess {Json} returns specific quote of speech.
    * 
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getQuote/354
    * @apiSuccessExample {json} Example response:
    {
    "person": {
    "is_active": false,
    "district": [
    76
    ],
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
    },
    "created_at": "16.04.2017",
    "created_for": "16.04.2017",
    "results": {
    "quote_id": 354,
    "content": "Spoštovane kolegice poslanke in kolegi poslanci, gospe in gospodje! ...
    "session": {
    "name": "28. redna seja",
    "date_ts": "2017-03-20T01:00:00",
    "orgs": [
    {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    }
    ],
    "date": "20. 3. 2017",
    "org": {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    },
    "id": 9379,
    "in_review": true
    },
    "quoted_text": "pozdravljam. Prehajamo na določitev dnevnega reda 28. seje Državnega zbora....
    "speech_id": 1178191,
    "end_idx": 1947,
    "start_idx": 898
    }
    }
    """
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
    """
    * @api {get} /getLastSessionLanding/{?date} Requests data of last session.
    * @apiName getLastSessionLanding
    * @apiGroup Session
    * @apiParam {date} date Optional date.
    * @apiSuccess {Json} returns data of last session.
    * 
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getLastSessionLanding
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/s/getLastSessionLanding/21.12.2016
    * @apiSuccessExample {json} Example response:
    {
    "created_for": "20.03.2017",
    "presence": [
    {
    "org": {
    "acronym": "PS NP",
    "is_coalition": false,
    "id": 109,
    "name": "PS nepovezanih poslancev "
    },
    "percent": 100
    },
    {
    "org": {
    "acronym": "SMC",
    "is_coalition": true,
    "id": 1,
    "name": "PS Stranka modernega centra"
    },
    "percent": 99
    },
    ...
    "created_at": "16.04.2017",
    "tfidf": {
    "session": {
    "name": "28. redna seja",
    "date_ts": "2017-03-20T01:00:00",
    "org": {
    "acronym": "DZ",
    "is_coalition": false,
    "name": "Državni zbor",
    "id": 95
    },
    "date": "20. 3. 2017",
    "orgs": [
    {
    "acronym": "DZ",
    "is_coalition": false,
    "name": "Državni zbor",
    "id": 95
    }
    ],
    "id": 9379,
    "in_review": true
    },
    "session": {
    "name": "28. redna seja",
    "date_ts": "2017-03-20T01:00:00",
    "orgs": [
    {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    }
    ],
    "date": "20. 3. 2017",
    "org": {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    },
    "id": 9379,
    "in_review": true
    },
    "motions": [
    {
    "session": {
    "name": "28. redna seja",
    "date_ts": "2017-03-20T01:00:00",
    "org": {
    "acronym": "DZ",
    "is_coalition": false,
    "name": "Državni zbor",
    "id": 95
    },
    "date": "20. 3. 2017",
    "orgs": [
    {
    "acronym": "DZ",
    "is_coalition": false,
    "name": "Državni zbor",
    "id": 95
    }
    ],
    "id": 9379,
    "in_review": true
    },
    "results": {
    "abstain": 0,
    "tags": [
    "Proceduralna glasovanja"
    ],
    "text": "Dnevni red v celoti",
    "motion_id": 6900,
    "against": 1,
    "votes_for": 83,
    "is_outlier": true,
    "not_present": 6,
    "result": true
    }
    }
    }
    """
    if date_:
        fdate = datetime.strptime(date_, API_DATE_FORMAT).date()
    else:
        fdate = datetime.now().today()
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
                tfidf = json.loads(getTFIDF(None, presence.session.id_parladata).content)
                if tfidf["results"]:
                    ready = True
                else:
                    presence_index += 1
        else:
            presence_index += 1

    results = [{"org": Organization.objects.get(id_parladata=p).getOrganizationData(),
                                "percent": presence.presence[0][p]} for p in presence.presence[0]]
    result = sorted(results, key=lambda k: k['percent'], reverse=True)
    session = Session.objects.get(id_parladata=int(presence.session.id_parladata))
    return JsonResponse({"session": session.getSessionData(),
                         "created_for": session.start_time.strftime(API_DATE_FORMAT),
                         "created_at": datetime.today().strftime(API_DATE_FORMAT),
                         "presence": result,
                         "motions": motions["results"],
                         "tfidf": tfidf}, safe=False)


def getSessionsByClassification(request):
    """
    * @api {get} /getSessionsByClassification/ Requests data of all session by classification.
    * @apiName getSessionsByClassification
    * @apiGroup Session
    * @apiSuccess {Json} returns data of all session by classification.
    * 
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getSessionsByClassification
    * @apiSuccessExample {json} Example response:
    {
    "kolegij": [
    {
    "votes": false,
    "name": "91. redna seja",
    "date_ts": "2017-04-13T02:00:00",
    "speeches": true,
    "orgs": [
    {
    "acronym": "",
    "is_coalition": false,
    "id": 9,
    "name": "Kolegij predsednika državnega zbora"
    }
    ],
    "date": "13. 4. 2017",
    "org": {
    "acronym": "",
    "is_coalition": false,
    "id": 9,
    "name": "Kolegij predsednika državnega zbora"
    },
    "id": 9419,
    "in_review": true
    },
    "dt": [
    {
    "acronym": "",
    "sessions": [
    {
    "votes": false,
    "name": "39. redna seja",
    "date_ts": "2017-03-31T02:00:00",
    "speeches": false,
    "orgs": [
    {
    "acronym": "",
    "is_coalition": false,
    "id": 101,
    "name": "Preiskovalna komisija za ugotavljanje politične odgovornosti nosilcev javnih funkcij pri investiciji v blok 6 Termoelektrarne Šoštanj"
    }
    ],
    "date": "31. 3. 2017",
    "org": {
    "acronym": "",
    "is_coalition": false,
    "id": 101,
    "name": "Preiskovalna komisija za ugotavljanje politične odgovornosti nosilcev javnih funkcij pri investiciji v blok 6 Termoelektrarne Šoštanj"
    },
    "id": 9397,
    "in_review": false
    },
    "dz": [
    {
    "votes": true,
    "name": "28. redna seja",
    "date_ts": "2017-03-20T01:00:00",
    "speeches": true,
    "orgs": [
    {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    }
    ],
    "date": "20. 3. 2017",
    "org": {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    },
    "id": 9379,
    "in_review": true
    }
    }
    """
    COUNCIL_ID = 9
    DZ = 95
    working_bodies = ["odbor", "komisija", "preiskovalna komisija"]
    out = {"kolegij": [session.getSessionData() for session in Session.objects.filter(organizations__id_parladata=COUNCIL_ID).order_by("-start_time")],
           "dz": [session.getSessionData() for session in Session.objects.filter(organizations__id_parladata=DZ).order_by("-start_time")],
           "dt": [org.getOrganizationData() for org in Organization.objects.filter(classification__in=working_bodies)]}

    for dt in out["dt"]:
        dt["sessions"] = [session.getSessionData() for session in Session.objects.filter(organizations__id_parladata=dt["id"]).order_by("-start_time")]
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
        orgs = Organization.objects.filter(Q(id_parladata=COUNCIL_ID) |
                                           Q(id_parladata=DZ) |
                                           Q(classification__in=working_bodies))
        sessions = Session.objects.filter(organizations__in=orgs)
        sessions = sessions.order_by("-start_time")
        out = {'sessions': [session.getSessionData() for session in sessions],
               'created_for': datetime.now().strftime(API_DATE_FORMAT),
               'created_at': datetime.now().strftime(API_DATE_FORMAT)}

        newList = []
        sessionsIds = []
        for session in out["sessions"]:
            activity = Activity.objects.filter(session__id_parladata=session['id'])
            if activity:
                last_day = activity.latest('updated_at').updated_at
            else:
                last_day = session['date_ts']
                # TODO zbrisi ta umazn fix ko se dodajo empty state-si
                continue
            session.update({"updated_at": last_day.strftime(API_DATE_FORMAT)})
            session.update({"updated_at_ts": last_day})
            # joint sessions fix
            if session['id'] not in sessionsIds:
                # TODO zbrisi ta umazn fix ko se dodajo empty state-si
                newList.append(session)
                sessionsIds.append(session['id'])
        # TODO zbrisi ta umazn fix ko se dodajo empty state-si
        out["sessions"] = newList
        cache.set("sessions_list_" + key, out, 60 * 60 * 48)

    return JsonResponse(out)


def setTFIDF(request, session_id):
    """Stores TFIDF analysis.
    """
    date_of = datetime.now().date()
    url = "https://isci.parlameter.si/tfidf/s/" + str(session_id)
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
    """
    * @api {get} /getTFIDF/{session_id} Requests data of TFIDF analysis..
    * @apiName getTFIDF
    * @apiGroup Session
    * @apiParam {date} date Optional date.
    * @apiSuccess {Json} returns data of TFIDF analysis.
    * 
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getTFIDF/
    * @apiSuccessExample {json} Example response:
    {
    "created_at": "22.03.2017",
    "created_for": "22.03.2017",
    "session": {
    "name": "28. redna seja",
    "date_ts": "2017-03-20T01:00:00",
    "orgs": [
    {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    }
    ],
    "date": "20. 3. 2017",
    "org": {
    "acronym": "DZ",
    "is_coalition": false,
    "id": 95,
    "name": "Državni zbor"
    },
    "id": 9379,
    "in_review": true
    },
    "results": [
    {
    "term": "filharmonija",
    "scores": {
    "tf": 18,
    "df": 28,
    "tf-idf": 0.6428571428571429
    }
    },
    {
    "term": "Plečnikov",
    "scores": {
    "tf": 15,
    "df": 55,
    "tf-idf": 0.2727272727272727
    }
    }
    ]
    }
    """
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


def getWorkingBodies(request):
    """
    * @api {get} /getWorkingBodies/ Requests data of all working bodies.
    * @apiName getWorkingBodies
    * @apiGroup Session
    * 
    * @apiSuccess {Json} returns data of all working bodies.
    * 
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getWorkingBodies
    * @apiSuccessExample {json} Example response:
    [
    {
    "id": 101,
    "name": "Preiskovalna komisija za ugotavljanje politične odgovornosti nosilcev javnih funkcij pri investiciji v blok 6 Termoelektrarne Šoštanj"
    },
    {
    "id": 106,
    "name": "Preiskovalna komisija o ugotavljanju zlorab v slovenskem zdravstvenem sistemu na področju prodaje in nakupa žilnih opornic"
    },
    {
    "id": 105,
    "name": "Komisija za nadzor obveščevalnih in varnostnih služb"
    }
    ]
    """
    working_bodies = ['odbor', 'komisija', 'preiskovalna komisija']
    orgs = Organization.objects.filter(classification__in=working_bodies)
    data = []
    for org in orgs:
        data.append({'id': org.id_parladata, 'name': org.name})
    return JsonResponse(data, safe=False)
