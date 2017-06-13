# -*- coding: UTF-8 -*-
from datetime import datetime
from parlalize.utils import *
import json
from django.http import JsonResponse, HttpResponse
from parlaseje.models import *
from parlalize.settings import API_URL, API_DATE_FORMAT, BASE_URL, SETTER_KEY, ISCI_URL
from parlaseje.utils import *
from collections import defaultdict, Counter
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
import re
from django.db.models import Q, F
from django.core.cache import cache
from parlalize.utils import tryHard, lockSetter


def getSpeech(request, speech_id):
    """
    * @api {get} /getSpeech/{speech_id} Requests information of speech.
    * @apiName GetSpeech
    * @apiGroup Session
    * @apiParam {speech_id} speech id is parameter which returns exactly specified speech
    * @@apiSuccess {Json} This function returns detiled data of specific speech.
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
    *
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for For when was this data created?
    *
    * @apiSuccess {Object} results
    * @apiSuccess {Integer} results.quote_id Id of quote if exists.
    * @apiSuccess {String} results.content Content of speech.
    *
    * @apiSuccess {Object} results.session object
    * @apiSuccess {String} results.session.name Name of session.
    * @apiSuccess {Date} results.session.date_ts Date and time of session.
    * @apiSuccess {Date} results.session.date Date of session.
    * @apiSuccess {Integer} results.session.id Id of session.
    * @apiSuccess {Boolean} results.session.in_review Return true or false if session is in review.
    * @apiSuccess {Object[]} results.session.orgs Organization object
    * @apiSuccess {String} results.session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} results.session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} results.session.orgs.id Id of organization
    * @apiSuccess {Integer} results.session.orgs.name Name of organization
    *
    * @apiSuccess {String} results.quoted_text Content of quoted text.
    * @apiSuccess {String} results.speech_id Id of speech.
    * @apiSuccess {String} results.end_idx End intex of quoted text.
    * @apiSuccess {String} results.start_idx End intex of quoted text.
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
    * @apiParam {session_id} session id is parameter which returns specific session
    * @apiSuccess {Json} returns detiled data of all speeches on session.
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for For when was this data created?
    * @apiSuccess {Object} session object
    * @apiSuccess {String} session.name Name of session.
    * @apiSuccess {Date} session.date_ts Date and time of session.
    * @apiSuccess {Date} session.date Date of session.
    * @apiSuccess {Integer} session.id Id of session.
    * @apiSuccess {Boolean} session.in_review Return true or false if session is in review.
    * @apiSuccess {Object[]} session.orgs Organization object
    * @apiSuccess {String} session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} session.orgs.id Id of organization
    * @apiSuccess {Integer} session.orgs.name Name of organization
    *
    * @apiSuccess {Object[]} results Array of persons and speeches of session.
    * @apiSuccess {Object} results.person person MP's person object (comes with most calls).
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
    * @apiSuccess {Object} results.results
    * @apiSuccess {Integer} results.results.quote_id Id of quote if exists.
    * @apiSuccess {String} results.results.content Content of speech.
    *
    * @apiSuccess {Object} results.results.session object
    * @apiSuccess {String} results.results.session.name Name of session.
    * @apiSuccess {Date} results.results.session.date_ts Date and time of session.
    * @apiSuccess {Date} results.results.session.date Date of session.
    * @apiSuccess {Integer} results.results.session.id Id of session.
    * @apiSuccess {Boolean} results.results.session.in_review Return true or false if session is in review.
    * @apiSuccess {Object[]} results.results.session.orgs Organization object
    * @apiSuccess {String} results.results.session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} results.results.session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} results.results.session.orgs.id Id of organization
    * @apiSuccess {Integer} results.results.session.orgs.name Name of organization
    *
    * @apiSuccess {String} results.results.quoted_text Content of quoted text.
    * @apiSuccess {String} results.results.speech_id Id of speech.
    * @apiSuccess {String} results.results.end_idx End intex of quoted text.
    * @apiSuccess {String} results.results.start_idx End intex of quoted text.
    *
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

    sessionData = session.getSessionData()
    session_time = session.start_time.strftime(API_DATE_FORMAT)

    personsStatic = tryHard(BASE_URL + "/utils/getAllStaticData/").json()

    data = []
    for speech in speeches:
        out = {"speech_id": speech.id_parladata,
               "content": speech.content,
               "session": sessionData,
               "quoted_text": None,
               "end_idx": None,
               "start_idx": None,
               "quote_id": None}
        try:
            personData = personsStatic['persons'][str(speech.person.id_parladata)]
        except:
            personData = getPersonData(speech.person.id_parladata,
                                       session_time)
        result = {
            'person': personData,
            'results': out
        }
        data.append(result)

    return JsonResponse({"session": sessionData,
                         "created_for": session_time,
                         "created_at": datetime.today().strftime(API_DATE_FORMAT),
                         "results": data})


def getSpeechesIDsOfSession(request, session_id):
    """
    * @api {get} /getSpeechesIDsOfSession/{session_id} Requests IDs of all speeches on specific session.
    * @apiName getSpeechesIDsOfSession
    * @apiGroup Session
    * @apiParam {session_id} session id is parameter which returns specific session
    * @apiSuccess {Json} returns IDs of speeches on specific session
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for For when was this data created?
    * @apiSuccess {Object} session object
    * @apiSuccess {String} session.name Name of session.
    * @apiSuccess {Date} session.date_ts Date and time of session.
    * @apiSuccess {Date} session.date Date of session.
    * @apiSuccess {Integer} session.id Id of session.
    * @apiSuccess {Boolean} session.in_review Return true or false if session is in review.
    * @apiSuccess {Object[]} session.orgs Organization object
    * @apiSuccess {String} session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} session.orgs.id Id of organization
    * @apiSuccess {Integer} session.orgs.name Name of organization
    * @apiSuccess {Integer[]} results IDs of all speeches on session.
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


@lockSetter
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
        url = API_URL + '/getBallotsOfMotion/' + str(mot['vote_id']) + '/'
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

        if Vote.objects.filter(id_parladata=mot['vote_id']):
            vote = Vote.objects.filter(id_parladata=mot['vote_id'])
            vote.update(created_for=session.start_time,
                        start_time=mot['start_time'],
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
                                    start_time=mot['start_time'],
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


@lockSetter
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
        url = API_URL + '/getBallotsOfMotion/' + str(mot['vote_id']) + '/'
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
    * @apiParam {speech_id} session id is parameter which returns exactly specified session
    * @apiSuccess {Json} returns detiled data of all motions on specific session
    * @apiParam {date} date Optional date.
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for For when was this data created?
    * @apiSuccess {Object} session object
    * @apiSuccess {String} session.name Name of session.
    * @apiSuccess {Date} session.date_ts Date and time of session.
    * @apiSuccess {Date} session.date Date of session.
    * @apiSuccess {Integer} session.id Id of session.
    * @apiSuccess {Boolean} session.in_review Return true or false if session is in review.
    * @apiSuccess {Object[]} session.orgs Organization object
    * @apiSuccess {String} session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} session.orgs.id Id of organization
    * @apiSuccess {Integer} session.orgs.name Name of organization
    * @apiSuccess {Integer} results IDs of all speeches on session.
    * @apiSuccess {Object} results object
    * @apiSuccess {Object} results.session object
    * @apiSuccess {String} results.session.name Name of session.
    * @apiSuccess {Date} results.session.date_ts Date and time of session.
    * @apiSuccess {Date} results.session.date Date of session.
    * @apiSuccess {Integer} results.session.id Id of session.
    * @apiSuccess {Boolean} results.session.in_review Return true or false if session is in review.
    * @apiSuccess {Object[]} results.session.orgs Organization object
    * @apiSuccess {String} results.session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} results.session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} results.session.orgs.id Id of organization
    * @apiSuccess {Integer} results.session.orgs.name Name of organization
    * @apiSuccess {Integer} results.results IDs of all speeches on session.
    * @apiSuccess {Object} results.results object
    * @apiSuccess {Integer} results.abstain Number of MPs that abstain on voting.
    * @apiSuccess {Integer} results.against Number of MPs that are against on voting.
    * @apiSuccess {Integer} results.motion_id ID of motion.
    * @apiSuccess {String} results.text Text of motion
    * @apiSuccess {String[]} results.tags Array of tags of motion.
    * @apiSuccess {Boolean} results.is_outlier Analaysis if person is outlier.
    * @apiSuccess {Integer} results.not_present Number of MPs that were not present.
    * @apiSuccess {Integer} results.votes_for Number of MPs that voted with yes.
    * @apiSuccess {Boolean} results.result True or False if the motion was successful.
    * @apiSuccess {String[]} results.tags Array of tags of motion.
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getMotionOfSession/9427
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/s/getMotionOfSession/9427/21.12.2016
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
                                        'is_outlier': card.is_outlier,
                                        'tags': card.tags,
                                        'has_outliers': card.has_outlier_voters
                                        }
                            })
                dates.append(card.created_at)
            created_at = max(dates).strftime(API_DATE_FORMAT)
        else:
            out = []
        ses_date = session.start_time.strftime(API_DATE_FORMAT)
        tags = list(Tag.objects.all().values_list('name', flat=True))
        return JsonResponse({"results": out,
                             "session": session.getSessionData(),
                             "tags": tags,
                             "created_for": ses_date,
                             "created_at": created_at}, safe=False)
    else:
        return JsonResponse({'result': 'No session'})


def getMotionGraph(request, id_mo, date=False):
    """
    * @api {get} /getMotionGraph/{id_mo}/{?date} Requests information of specific motion.
    * @apiName getMotionGraph
    * @apiGroup Session
    * @apiParam {id_mo} session id is parameter which returns exactly specified motion
    * @apiParam {date} date Optional date.
    * @apiSuccess {Json} returns detiled data of motion
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for For when was this data created?
    * @apiSuccess {Object} session object
    * @apiSuccess {String} session.name Name of session.
    * @apiSuccess {Date} session.date_ts Date and time of session.
    * @apiSuccess {Date} session.date Date of session.
    * @apiSuccess {Integer} session.id Id of session.
    * @apiSuccess {Boolean} session.in_review Return true or false if session is in review.
    * @apiSuccess {Object[]} session.orgs Organization object
    * @apiSuccess {String} session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} session.orgs.id Id of organization
    * @apiSuccess {Integer} session.orgs.name Name of organization
    * @apiSuccess {String} name Name of motion
    * @apiSuccess {String} id Motions id
    * @apiSuccess {String} required Number of required votes to pass the motion.
    * @apiSuccess {Boolean} result Result of motion.
    * @apiSuccess {String[]} documents Links to the documents of motion.
    * @apiSuccess {Object} all object
    * @apiSuccess {Object} all.kvorum object
    * @apiSuccess {String} all.kvorum.option Name of option
    * @apiSuccess {Integer} all.kvorum.total_votes Total votes for this option
    * @apiSuccess {Object[]} all.kvorum.breakdown   
    * @apiSuccess {Object} all.kvorum.breakdown.pg
    * @apiSuccess {String} rall.kvorum.breakdown.pg.acronym Organization acronym
    * @apiSuccess {Boolean} rall.kvorum.breakdown.pg.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} all.kvorum.breakdown.pg.id Id of organization
    * @apiSuccess {Integer} all.kvorum.breakdown.pg.name Name of organization
    * @apiSuccess {Object[]} all.kvorum.breakdown.mps MP's person object 
    * @apiSuccess {Boolean} all.kvorum.breakdown.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} all.kvorum.breakdown.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} all.kvorum.breakdown.mps.name MP's full name.
    * @apiSuccess {String} all.kvorum.breakdown.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} all.kvorum.breakdown.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} all.kvorum.breakdown.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} all.kvorum.breakdown.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} all.kvorum.breakdown.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} all.kvorum.breakdown.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} all.kvorum.breakdown.mps.party.name The party's name.
    * @apiSuccess {String} all.kvorum.breakdown.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} all.kvorum.breakdown.mps.id The person's Parladata id.
    * @apiSuccess {Boolean} all.kvorum.breakdown.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Object} all.not_present object
    * @apiSuccess {String} all.not_present.option Name of option
    * @apiSuccess {Integer} all.not_present.total_votes Total votes for this option
    * @apiSuccess {Object[]} all.not_present.breakdown   
    * @apiSuccess {Object} all.not_present.breakdown.pg
    * @apiSuccess {String} rall.not_present.breakdown.pg.acronym Organization acronym
    * @apiSuccess {Boolean} rall.not_present.breakdown.pg.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} all.not_present.breakdown.pg.id Id of organization
    * @apiSuccess {Integer} all.not_present.breakdown.pg.name Name of organization
    * @apiSuccess {Object[]} all.not_present.breakdown.mps MP's person object 
    * @apiSuccess {Boolean} all.not_present.breakdown.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} all.not_present.breakdown.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} all.not_present.breakdown.mps.name MP's full name.
    * @apiSuccess {String} all.not_present.breakdown.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} all.not_present.breakdown.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} all.not_present.breakdown.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} all.not_present.breakdown.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} all.not_present.breakdown.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} all.not_present.breakdown.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} all.not_present.breakdown.mps.party.name The party's name.
    * @apiSuccess {String} all.not_present.breakdown.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} all.not_present.breakdown.mps.id The person's Parladata id.
    * @apiSuccess {Boolean} all.not_present.breakdown.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Object} all.against object
    * @apiSuccess {String} all.against.option Name of option
    * @apiSuccess {Integer} all.against.total_votes Total votes for this option
    * @apiSuccess {Object[]} all.against.breakdown   
    * @apiSuccess {Object} all.against.breakdown.pg
    * @apiSuccess {String} rall.against.breakdown.pg.acronym Organization acronym
    * @apiSuccess {Boolean} rall.against.breakdown.pg.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} all.against.breakdown.pg.id Id of organization
    * @apiSuccess {Integer} all.against.breakdown.pg.name Name of organization
    * @apiSuccess {Object[]} all.against.breakdown.mps MP's person object 
    * @apiSuccess {Boolean} all.against.breakdown.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} all.against.breakdown.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} all.against.breakdown.mps.name MP's full name.
    * @apiSuccess {String} all.against.breakdown.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} all.against.breakdown.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} all.against.breakdown.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} all.against.breakdown.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} all.against.breakdown.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} all.against.breakdown.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} all.against.breakdown.mps.party.name The party's name.
    * @apiSuccess {String} all.against.breakdown.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} all.against.breakdown.mps.id The person's Parladata id.
    * @apiSuccess {Boolean} all.against.breakdown.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
    * @apiSuccess {Object} all.for object
    * @apiSuccess {String} all.for.option Name of option
    * @apiSuccess {Integer} all.for.total_votes Total votes for this option
    * @apiSuccess {Object[]} all.for.breakdown   
    * @apiSuccess {Object} all.for.breakdown.pg
    * @apiSuccess {String} rall.for.breakdown.pg.acronym Organization acronym
    * @apiSuccess {Boolean} rall.for.breakdown.pg.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} all.for.breakdown.pg.id Id of organization
    * @apiSuccess {Integer} all.for.breakdown.pg.name Name of organization
    * @apiSuccess {Object[]} all.for.breakdown.mps MP's person object 
    * @apiSuccess {Boolean} all.for.breakdown.mps.is_active Answer the question: Is this MP currently active?
    * @apiSuccess {Integer[]} all.for.breakdown.mps.district List of Parladata ids for districts this person was elected in.
    * @apiSuccess {String} all.for.breakdown.mps.name MP's full name.
    * @apiSuccess {String} all.for.breakdown.mps.gov_id MP's id on www.dz-rs.si
    * @apiSuccess {String} all.for.breakdown.mps.gender MP's gender (f/m) used for grammar
    * @apiSuccess {Object} all.for.breakdown.mps.party This MP's standard party objects (comes with most calls).
    * @apiSuccess {String} all.for.breakdown.mps.party.acronym The MP's party's acronym.
    * @apiSuccess {Boolean} all.for.breakdown.mps.party.is_coalition Answers the question: Is this party in coalition with the government?
    * @apiSuccess {Integer} all.for.breakdown.mps.party.id This party's Parladata (organization) id.
    * @apiSuccess {String} all.for.breakdown.mps.party.name The party's name.
    * @apiSuccess {String} all.for.breakdown.mps.type The person's parlalize type. Always "mp" for MPs.
    * @apiSuccess {Integer} all.for.breakdown.mps.id The person's Parladata id.
    * @apiSuccess {Boolean} all.for.breakdown.mps.has_function Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).
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

        docs = model[0].vote.document_url
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


def getMotionAnalize(request, motion_id):
    model = get_object_or_404(Vote_analysis, vote__id_parladata=motion_id)
    vote = model.vote
    docs = vote.document_url

    options = {'for': model.votes_for,
               'against': model.against,
               'abstain': model.abstain,
               'not_present': model.not_present}
    stats = {'for': model.votes_for,
             'against': model.against,
             'abstain': model.abstain,
             'not_present': model.not_present}
    max_vote_opt = max(stats, key=stats.get)
    if stats[max_vote_opt] == 0:
        max_vote_percent_opt = 0
        max_vote_opt = '/'
    else:
        max_vote_percent_opt = float(stats[max_vote_opt])/(stats['abstain']+stats['against']+stats['for']+stats['not_present'])*100

    tmp_data = model.pgs_data
    orgs_data = {}
    pg_outliers = {}
    for org in tmp_data:
        org_obj = Organization.objects.get(id_parladata=int(org))
        if org_obj.classification == 'poslanska skupina':
            orgs_data[org] = json.loads(tmp_data[org])
            orgs_data[org]['party'] = org_obj.getOrganizationData()
            if orgs_data[org]['outliers']:
                pg_outliers[int(org)] = orgs_data[org]['outliers']

    orgs_data = sorted(orgs_data.values(), key=lambda party: sum(party['votes'].values()), reverse=True)

    members = []
    for option, members_ids in [('for', json.loads(model.mp_yes)),
                            ('against', json.loads(model.mp_no)),
                            ('not_present', json.loads(model.mp_np)),
                            ('abstain', json.loads(model.mp_kvor))]:
        for mp in members_ids:
            personData = getPersonData(mp)
            # set if person is outlier
            outlier = False
            if personData['party']['id'] in pg_outliers.keys():
                if option in pg_outliers[personData['party']['id']]:
                    outlier = True
            members.append({'person': personData,
                            'option': option,
                            'is_outlier': outlier})

    out = {'id': motion_id,
           'session': model.session.getSessionData(),
           'created_for': vote.created_for.strftime(API_DATE_FORMAT),
           'created_at': model.created_at.strftime(API_DATE_FORMAT),
           'name': vote.motion,
           'result': {'accepted': vote.result,
                      'value': max_vote_percent_opt,
                      'max_opt': max_vote_opt,
                      'is_outlier': vote.is_outlier},
           'documents': docs if docs else [],
           'members': members,
           'parties': orgs_data,
           'gov_side': {'coalition': json.loads(model.coal_opts),
                        'opposition': json.loads(model.oppo_opts)},
           'all': options}
    return JsonResponse(out, safe=False)


@lockSetter
def setPresenceOfPG(request, session_id):
    """ Stores presence of PGs on specific session
    """
    votes = tryHard(API_URL + '/getBallotsOfSession/' + str(session_id) + '/').json()
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
    * @api {get} /getPresenceOfPG/{session_id}/{?date} Requests information of presence of PGs on specific session.
    * @apiName getPresenceOfPG
    * @apiGroup Session
    * @apiParam {session_id} session id is parameter which returns exactly specified session
    * @apiParam {date} date Optional date.
    * @apiSuccess {Json} returns data presence of PGs on specific session
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for For when was this data created?
    * @apiSuccess {Object} session object
    * @apiSuccess {String} session.name Name of session.
    * @apiSuccess {Date} session.date_ts Date and time of session.
    * @apiSuccess {Date} session.date Date of session.
    * @apiSuccess {Integer} session.id Id of session.
    * @apiSuccess {Boolean} session.in_review Return true or false if session is in review.
    * @apiSuccess {Object[]} session.orgs Organization object
    * @apiSuccess {String} session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} session.orgs.id Id of organization
    * @apiSuccess {Integer} session.orgs.name Name of organization
    * @apiSuccess {Object[]} results 
    * @apiSuccess {Integer} results.percent Percent of presence on session for each PG.
    * @apiSuccess {Object} results.organization
    * @apiSuccess {String} results.organization.acronym Organization acronym
    * @apiSuccess {Boolean} results.organization.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} results.organization.id Id of organization
    * @apiSuccess {Integer} results.organization.name Name of organization
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


@lockSetter
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
    * @apiParam {quote_id} quote id is parameter which returns exactly specified quote
    * @apiSuccess {Json} returns specific quote of speech.
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
    *
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for For when was this data created?
    *
    * @apiSuccess {Object} results
    * @apiSuccess {Integer} results.quote_id Id of quote if exists.
    * @apiSuccess {String} results.content Content of speech.
    *
    * @apiSuccess {Object} results.session object
    * @apiSuccess {String} results.session.name Name of session.
    * @apiSuccess {Date} results.session.date_ts Date and time of session.
    * @apiSuccess {Date} results.session.date Date of session.
    * @apiSuccess {Integer} results.session.id Id of session.
    * @apiSuccess {Boolean} results.session.in_review Return true or false if session is in review.
    * @apiSuccess {Object[]} results.session.orgs Organization object
    * @apiSuccess {String} results.session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} results.session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} results.session.orgs.id Id of organization
    * @apiSuccess {Integer} results.session.orgs.name Name of organization
    *
    * @apiSuccess {String} results.quoted_text Content of quoted text.
    * @apiSuccess {String} results.speech_id Id of speech.
    * @apiSuccess {String} results.end_idx End intex of quoted text.
    * @apiSuccess {String} results.start_idx End intex of quoted text.
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
    * @apiSuccess {Json} returns data like presence, tfidf and all motions of last session.
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for For when was this data created?
    * @apiSuccess {Object} presence
    * @apiSuccess {Integer} presence.percent Percent of presence on session for each PG.
    * @apiSuccess {Object} presence.org
    * @apiSuccess {String} presence.org.acronym Organization acronym
    * @apiSuccess {Boolean} presence.org.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} presence.org.id Id of organization
    * @apiSuccess {Integer} presence.org.name Name of organization
    * @apiSuccess {Object} tfidf
    * @apiSuccess {date} tfidf.created_at When was this data created?
    * @apiSuccess {date} tfidf.created_for For when was this data created?
    * @apiSuccess {Object} tfidf.session object
    * @apiSuccess {String} tfidf.session.name Name of session.
    * @apiSuccess {Date} tfidf.session.date_ts Date and time of session.
    * @apiSuccess {Date} tfidf.session.date Date of session.
    * @apiSuccess {Integer} tfidf.session.id Id of session.
    * @apiSuccess {Boolean} tfidf.session.in_review Return true or false if session is in review.
    * @apiSuccess {Object[]} tfidf.session.orgs Organization object
    * @apiSuccess {String} tfidf.session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} tfidf.session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} tfidf.session.orgs.id Id of organization
    * @apiSuccess {Integer} tfidf.session.orgs.name Name of organization
    * @apiSuccess {Object[]} tfidf.results
    * @apiSuccess {String} tfidf.results.term Term that is analyzed.
    * @apiSuccess {Object} tfidf.results.scores Scores of TFIDF
    * @apiSuccess {Integer} tfidf.results.scores.tf Term frequency
    * @apiSuccess {Integer} tfidf.results.scores.df Document frequency
    * @apiSuccess {Integer} tfidf.results.scores.tf-idf Term frequency / Document frequency
    * @apiSuccess {Object} session object
    * @apiSuccess {String} session.name Name of session.
    * @apiSuccess {Date} session.date_ts Date and time of session.
    * @apiSuccess {Date} session.date Date of session.
    * @apiSuccess {Integer} session.id Id of session.
    * @apiSuccess {Boolean} session.in_review Return true or false if session is in review.
    * @apiSuccess {Object[]} session.orgs Organization object
    * @apiSuccess {String} session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} session.orgs.id Id of organization
    * @apiSuccess {String} session.orgs.name Name of organization
    * @apiSuccess {Object[]} motion
    * @apiSuccess {Object} motion.results.session object
    * @apiSuccess {String} motion.results.session.name Name of session.
    * @apiSuccess {Date} motion.results.session.date_ts Date and time of session.
    * @apiSuccess {Date} motion.results.session.date Date of session.
    * @apiSuccess {Integer} motion.results.session.id Id of session.
    * @apiSuccess {Boolean} motion.results.session.in_review Return true or false if session is in review.
    * @apiSuccess {Object[]} motion.results.session.orgs Organization object
    * @apiSuccess {String} motion.results.session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} motion.results.session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} motion.results.session.orgs.id Id of organization
    * @apiSuccess {Integer} motion.results.session.orgs.name Name of organization
    * @apiSuccess {Integer} motion.results.results IDs of all speeches on session.
    * @apiSuccess {Object} motion.results.results object
    * @apiSuccess {Integer} motion.results.abstain Number of MPs that abstain on voting.
    * @apiSuccess {Integer} motion.results.against Number of MPs that are against on voting.
    * @apiSuccess {Integer} motion.results.motion_id ID of motion.
    * @apiSuccess {String} motion.results.text Text of motion
    * @apiSuccess {String[]} motion.results.tags Array of tags of motion.
    * @apiSuccess {Boolean} motion.results.is_outlier Analaysis if person is outlier.
    * @apiSuccess {Integer} motion.results.not_present Number of MPs that were not present.
    * @apiSuccess {Integer} motion.results.votes_for Number of MPs that voted with yes.
    * @apiSuccess {Boolean} motion.results.result True or False if the motion was successful.
    * @apiSuccess {String[]} motion.results.tags Array of tags of motion.
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
    * @api {get} /getSessionsByClassification/ Requests data of all sessions by classification.
    * @apiName getSessionsByClassification
    * @apiGroup Session
    * @apiSuccess {Json} returns data of all session by classification.
    * @apiSuccess {Object[]} kolegij Classification of session
    * @apiSuccess {String} kolegij.name Name of session.
    * @apiSuccess {Date} kolegij.date_ts Date and time of session.
    * @apiSuccess {Date} kolegij.date Date of session.
    * @apiSuccess {Integer} kolegij.id Id of session.
    * @apiSuccess {Boolean} kolegij.in_review Returns true or false if session is in review.
    * @apiSuccess {Boolean} kolegij.votes Returns true or false if session has votes.
    * @apiSuccess {Boolean} kolegij.speeches Returns true or false if session has speeches.
    * @apiSuccess {Object[]} kolegij.orgs Organization object
    * @apiSuccess {String} kolegij.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} kolegij.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} kolegij.orgs.id Id of organization
    * @apiSuccess {Integer} kolegij.orgs.name Name of organization
    * @apiSuccess {Object[]} dt Classification of session
    * @apiSuccess {String} dt.name Name of session.
    * @apiSuccess {Date} dt.date_ts Date and time of session.
    * @apiSuccess {Date} dt.date Date of session.
    * @apiSuccess {Integer} dt.id Id of session.
    * @apiSuccess {Boolean} dt.in_review Returns true or false if session is in review.
    * @apiSuccess {Boolean} dt.votes Returns true or false f session has votes.
    * @apiSuccess {Boolean} dt.speeches Returns true or false if session has speeches.
    * @apiSuccess {Object[]} dt.orgs Organization object
    * @apiSuccess {String} dt.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} dt.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} dt.orgs.id Id of organization
    * @apiSuccess {Integer} dt.orgs.name Name of organization
    * @apiSuccess {Object[]} dz Classification of session
    * @apiSuccess {String} dz.name Name of session.
    * @apiSuccess {Date} dz.date_ts Date and time of session.
    * @apiSuccess {Date} dz.date Date of session.
    * @apiSuccess {Integer} dz.id Id of session.
    * @apiSuccess {Boolean} dz.in_review Returns true or false if session is in review.
    * @apiSuccess {Boolean} dz.votes Returns true or false f session has votes.
    * @apiSuccess {Boolean} dz.speeches Returns true or false if session has speeches.
    * @apiSuccess {Object[]} dz.orgs Organization object
    * @apiSuccess {String} dz.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} dz.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} dz.orgs.id Id of organization
    * @apiSuccess {Integer} dz.orgs.name Name of organization
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
    """
    * @api {get} /getSessionsList/ Requests data of all sessions.
    * @apiName getSessionsList
    * @apiGroup Session
    * @apiParam {date} date Optional date.
    * @apiParam {Boolean} force_render Optional force render.
    * @apiSuccess {Json} returns data of all sessions.
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for For when was this data created?
    * @apiSuccess {Object} session object
    * @apiSuccess {String} session.name Name of session.
    * @apiSuccess {Date} session.date_ts Date and time of session.
    * @apiSuccess {Date} session.date Date of session.
    * @apiSuccess {Date} session.updated_at_ts Last update of session.
    * @apiSuccess {Integer} session.id Id of session.
    * @apiSuccess {Boolean} session.in_review Return true or false if session is in review.
    * @apiSuccess {Boolean} session.speeches Return true or false if session has speeches.
    * @apiSuccess {Boolean} session.votes Return true or false if session has votes_for.
    * @apiSuccess {Object[]} session.orgs Organization object
    * @apiSuccess {String} session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} session.orgs.id Id of organization
    * @apiSuccess {Integer} session.orgs.name Name of organization
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getSessionsList/
    * @apiExample {curl} Example with date:
        curl -i https://analize.parlameter.si/v1/s/getSessionsList/21.12.2016
    * @apiExample {curl} Example with force_render:
        curl -i https://analize.parlameter.si/v1/s/getSessionsList/True
    * @apiSuccessExample {json} Example response:
    {
    "created_at": "24.04.2017",
    "created_for": "24.04.2017",
    "sessions": [
    {
    "updated_at_ts": "2017-04-24T20:39:11.782",
    "speeches": true,
    "name": "29. redna seja",
    "date_ts": "2017-04-20T02:00:00",
    "votes": true,
    "updated_at": "24.04.2017",
    "org": {
    "acronym": "DZ",
    "is_coalition": false,
    "name": "Državni zbor",
    "id": 95
    },
    "date": "20. 4. 2017",
    "orgs": [
    {
    "acronym": "DZ",
    "is_coalition": false,
    "name": "Državni zbor",
    "id": 95
    }
    ],
    "id": 9427,
    "in_review": true
    },
    {
    "updated_at_ts": "2017-04-20T01:26:40.675",
    "speeches": true,
    "name": "93. redna seja",
    "date_ts": "2017-04-19T02:00:00",
    "votes": false,
    "updated_at": "20.04.2017",
    "org": {
    "acronym": "",
    "is_coalition": false,
    "name": "Kolegij predsednika državnega zbora",
    "id": 9
    },
    "date": "19. 4. 2017",
    "orgs": [
    {
    "acronym": "",
    "is_coalition": false,
    "name": "Kolegij predsednika državnega zbora",
    "id": 9
    }
    ],
    "id": 9424,
    "in_review": true
    }
    }
    """
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
                # continue
            session.update({"updated_at": last_day.strftime(API_DATE_FORMAT)})
            session.update({"updated_at_ts": last_day})
            if Vote.objects.filter(session__id_parladata=session["id"]):
                is_vote = True
            else:
                is_vote = False
            if Speech.objects.filter(session__id_parladata=session["id"]):
                is_speech = True
            else:
                is_speech = False
            session.update({"votes": is_vote,
                            "speeches": is_speech})
            # joint sessions fix
            if session['id'] not in sessionsIds:
                # TODO zbrisi ta umazn fix ko se dodajo empty state-si
                newList.append(session)
                sessionsIds.append(session['id'])
        # TODO zbrisi ta umazn fix ko se dodajo empty state-si
        out["sessions"] = newList
        cache.set("sessions_list_" + key, out, 60 * 60 * 48)

    return JsonResponse(out)


@lockSetter
def setTFIDF(request, session_id):
    """Stores TFIDF analysis.
    """
    date_of = datetime.now().date()
    url = ISCI_URL + "/tfidf/s/" + str(session_id)
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
    * @api {get} /getTFIDF/{session_id} Requests data of TFIDF analysis.
    * @apiName getTFIDF
    * @apiGroup Session
    * @apiParam {date} date Optional date.
    * @apiSuccess {Json} returns data of TFIDF analysis.
    * @apiSuccess {date} created_at When was this data created?
    * @apiSuccess {date} created_for For when was this data created?
    * @apiSuccess {Object} session object
    * @apiSuccess {String} session.name Name of session.
    * @apiSuccess {Date} session.date_ts Date and time of session.
    * @apiSuccess {Date} session.date Date of session.
    * @apiSuccess {Integer} session.id Id of session.
    * @apiSuccess {Boolean} session.in_review Return true or false if session is in review.
    * @apiSuccess {Object[]} session.orgs Organization object
    * @apiSuccess {String} session.orgs.acronym Organization acronym
    * @apiSuccess {Boolean} session.orgs.is_coalition True of False if organization is in coalition
    * @apiSuccess {Integer} session.orgs.id Id of organization
    * @apiSuccess {Integer} session.orgs.name Name of organization
    * @apiSuccess {Object[]} results
    * @apiSuccess {String} results.term Term that is analyzed.
    * @apiSuccess {Object} results.scores Scores of TFIDF
    * @apiSuccess {Integer} results.scores.tf Term frequency
    * @apiSuccess {Integer} results.scores.df Document frequency
    * @apiSuccess {Integer} results.scores.tf-idf Term frequency / Document frequency
    * @apiExample {curl} Example:
        curl -i https://analize.parlameter.si/v1/s/getTFIDF/9379
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
    * @apiSuccess {Json} returns data of all working bodies.
    * @apiSuccess {Integer} id Id of working bodie.
    * @apiSuccess {String} name Name of working bodie.
    * @apiExample {curl} Example:
        curl -i     
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


def getComparedVotes(request):
    people_same = request.GET.get('people_same')
    parties_same = request.GET.get('parties_same')
    people_different = request.GET.get('people_different')
    parties_different = request.GET.get('parties_different')

    if people_same != '':
        people_same_list = people_same.split(',')
    else:
        people_same_list = []
    if parties_same != '':
        parties_same_list = parties_same.split(',')
    else:
        parties_same_list = []
    
    if people_different != '':
        people_different_list = people_different.split(',')
    else:
        people_different_list = []
    if parties_different != '':
        parties_different_list = parties_different.split(',')
    else:
        parties_different_list = []
    
    if len(people_same_list) + len(parties_same_list) == 0:
        return HttpResponse('Need at least one same to compare.')
    if len(people_same_list) + len(parties_same_list) < 2 and len(people_different_list) + len(parties_different_list) < 1:
        return HttpResponse('Not enough to compare.')

    beginning = 'SELECT * FROM '
    select_same_people = ''
    select_same_parties = ''
    
    match_same_people_ballots = ''
    match_same_people_persons = ''
    match_same_people_options = ''

    match_same_parties_ballots = ''
    match_same_parties_organizations = ''
    match_same_parties_options = ''

    select_different_people = ''
    select_different_parties = ''
    
    match_different_people_ballots = ''
    match_different_people_persons = ''
    match_different_people_options = ''

    match_different_parties_ballots = ''
    match_different_parties_organizations = ''
    match_different_parties_options = ''

    # select for same people DONE
    for i, e in enumerate(people_same_list):
        if i < len(people_same_list) - 1:
            select_same_people = '%s parlaseje_ballot b%s, parlaseje_activity a%s, parlaposlanci_person p%s, ' % (select_same_people, str(i), str(i), str(i))
        else:
            select_same_people = '%s parlaseje_ballot b%s, parlaseje_activity a%s, parlaposlanci_person p%s' % (select_same_people, str(i), str(i), str(i))
    
    # select for same parties DONE
    for i, e in enumerate(parties_same_list):
        if i < len(parties_same_list) - 1:
            select_same_parties = '%s parlaseje_ballot pb%s, parlaskupine_organization o%s, ' % (select_same_parties, str(i), str(i))
        else:
            select_same_parties = '%s parlaseje_ballot pb%s, parlaskupine_organization o%s' % (select_same_parties, str(i), str(i))

    # select for different people DONE
    for i, e in enumerate(people_different_list):
        if i < len(people_different_list) - 1:
            select_different_people = '%s parlaseje_ballot db%s, parlaseje_activity da%s, parlaposlanci_person dp%s, ' % (select_different_people, str(i), str(i), str(i))
        else:
            select_different_people = '%s parlaseje_ballot db%s, parlaseje_activity da%s, parlaposlanci_person dp%s' % (select_different_people, str(i), str(i), str(i))
    
    # select for different parties DONE
    for i, e in enumerate(parties_different_list):
        if i < len(parties_different_list) - 1:
            select_different_parties = '%s parlaseje_ballot dpb%s, parlaskupine_organization do%s, ' % (select_different_parties, str(i), str(i))
        else:
            select_different_parties = '%s parlaseje_ballot dpb%s, parlaskupine_organization do%s' % (select_different_parties, str(i), str(i))

    # match same people ballots by vote id DONE
    # if only one person was passed, match_same_people_ballots will remain an empty string
    for i, e in enumerate(people_same_list):
        if i != 0:
            if i < len(people_same_list) - 1:
                match_same_people_ballots = '%s b0.vote_id = b%s.vote_id AND ' % (match_same_people_ballots, str(i))
            else:
                match_same_people_ballots = '%s b0.vote_id = b%s.vote_id' % (match_same_people_ballots, str(i))
    
    # match same parties ballots by vote id DONE
    # if only one same party was passed match_same_parties_ballots will remain an empty string
    if len(people_same_list) == 0:
        # no same people were passed to the API
        pass
        if len(parties_same_list) == 0:
            # no same parties were passed
            return HttpResponse('You need to pass at least one "same" person or party.')
        elif len(parties_same_list) == 1:
            # only one same party was passed, there is nothing to match yet
            match_same_parties_ballots = ''
        else:
            # more than one same party was passed
            for i, e in enumerate(parties_same_list):
                if i != 0:
                    # ignore the first one, because all others will be compared with it
                    if i < len(parties_same_list) - 1:
                        # not last
                        match_same_parties_ballots = '%s pb0.vote_id = pb%s.vote_id AND ' % (match_same_parties_ballots, str(i))
                    else:
                        # last
                        match_same_parties_ballots = '%s pb0.vote_id = pb%s.vote_id' % (match_same_parties_ballots, str(i))
    elif len(people_same_list) > 0:
        # one or more same people were passed
        for i, e in enumerate(parties_same_list):
            # do not ignore the first one, because all will be compared to the first person ballot
            if i < len(parties_same_list) - 1:
                # not last
                match_same_parties_ballots = '%s b0.vote_id = pb%s.vote_id AND ' % (match_same_parties_ballots, str(i))
            else:
                # last
                match_same_parties_ballots = '%s b0.vote_id = pb%s.vote_id' % (match_same_parties_ballots, str(i))
    
    

    # match same people with persons DONE
    for i, e in enumerate(people_same_list):
        if i < len(people_same_list) - 1:
            match_same_people_persons = '%s b%s.activity_ptr_id = a%s.id AND a%s.person_id = p%s.id AND p%s.id_parladata = %s AND ' % (match_same_people_persons, str(i), str(i), str(i), str(i), str(i), e)
        else:
            match_same_people_persons = '%s b%s.activity_ptr_id = a%s.id AND a%s.person_id = p%s.id AND p%s.id_parladata = %s' % (match_same_people_persons, str(i), str(i), str(i), str(i), str(i), e)
    
    # match same parties with organizations DONE
    for i, e in enumerate(parties_same_list):
        if i < len(parties_same_list) -1:
            match_same_parties_organizations = '%s pb%s.org_voter_id = o%s.id AND o%s.id_parladata = %s AND ' % (match_same_parties_organizations, str(i), str(i), str(i), e)
        else:
            match_same_parties_organizations = '%s pb%s.org_voter_id = o%s.id AND o%s.id_parladata = %s' % (match_same_parties_organizations, str(i), str(i), str(i), e)

    # match same people based on options DONE
    for i, e in enumerate(people_same_list):
        if i != 0:
            if i != len(people_same_list) - 1:
                match_same_people_options = '%s b0.option = b%s.option AND ' % (match_same_people_options, str(i))
            else:
                match_same_people_options = '%s b0.option = b%s.option' % (match_same_people_options, str(i))
    
    # match same parties based on options
    for i, e in enumerate(parties_same_list):
        if i == 0:
            if select_same_people != '':
                if len(parties_same_list) > 1:
                    match_same_parties_options = '%s b0.option = pb0.option AND ' % (match_same_parties_options)
                else: 
                    match_same_parties_options = '%s b0.option = pb0.option ' % (match_same_parties_options)
        else:
            if i != len(parties_same_list) - 1:
                match_same_parties_options = '%s pb0.option = pb%s.option AND ' % (match_same_parties_options, str(i))
            else:
                match_same_parties_options = '%s pb0.option = pb%s.option' % (match_same_parties_options, str(i))
    
    # compare different people and parties
    if len(people_same_list) > 0:
        # we compare with same people

        # match different people ballots by vote id
        for i, e in enumerate(people_different_list):
            if i < len(people_different_list) - 1:
                match_different_people_ballots = '%s b0.vote_id = db%s.vote_id AND ' % (match_different_people_ballots, str(i))
            else:
                match_different_people_ballots = '%s b0.vote_id = db%s.vote_id' % (match_different_people_ballots, str(i))
        
        # match different parties ballots by vote id
        for i, e in enumerate(parties_different_list):
            if i < len(parties_different_list) - 1:
                match_different_parties_ballots = '%s b0.vote_id = dpb%s.vote_id AND ' % (match_different_parties_ballots, str(i))
            else:
                match_different_parties_ballots = '%s b0.vote_id = dpb%s.vote_id' % (match_different_parties_ballots, str(i))

        # match different people based on options
        for i, e in enumerate(people_different_list):
            if i != len(people_different_list) - 1:
                match_different_people_options = '%s b0.option != db%s.option AND ' % (match_different_people_options, str(i))
            else:
                match_different_people_options = '%s b0.option != db%s.option' % (match_different_people_options, str(i))
        
        # match different parties based on options
        for i, e in enumerate(parties_different_list):
                if i < len(parties_different_list) - 1:
                    match_different_parties_options = '%s b0.option != dpb%s.option AND ' % (match_different_parties_options, str(i))
                else: 
                    match_different_parties_options = '%s b0.option != dpb%s.option ' % (match_different_parties_options, str(i))
    
    else:
        # we compare with same parties

        # match different people ballots by vote id
        for i, e in enumerate(people_different_list):
            if i < len(people_different_list) - 1:
                match_different_people_ballots = '%s pb0.vote_id = db%s.vote_id AND ' % (match_different_people_ballots, str(i))
            else:
                match_different_people_ballots = '%s pb0.vote_id = db%s.vote_id' % (match_different_people_ballots, str(i))
        
        # match different parties ballots by vote id
        for i, e in enumerate(parties_different_list):
            if i < len(parties_different_list) - 1:
                match_different_parties_ballots = '%s pb0.vote_id = dpb%s.vote_id AND ' % (match_different_parties_ballots, str(i))
            else:
                match_different_parties_ballots = '%s pb0.vote_id = dpb%s.vote_id' % (match_different_parties_ballots, str(i))

        # match different people based on options
        for i, e in enumerate(people_different_list):
            if i != len(people_different_list) - 1:
                match_different_people_options = '%s pb0.option != db%s.option AND ' % (match_different_people_options, str(i))
            else:
                match_different_people_options = '%s pb0.option != db%s.option' % (match_different_people_options, str(i))
        
        # match different parties based on options
        for i, e in enumerate(parties_different_list):
                if i < len(parties_different_list) - 1:
                    match_different_parties_options = '%s pb0.option != dpb%s.option AND ' % (match_different_parties_options, str(i))
                else: 
                    match_different_parties_options = '%s pb0.option != dpb%s.option ' % (match_different_parties_options, str(i))
    
    # match different people with person
    for i, e in enumerate(people_different_list):
        if i < len(people_different_list) - 1:
            match_different_people_persons = '%s db%s.activity_ptr_id = da%s.id AND da%s.person_id = dp%s.id AND dp%s.id_parladata = %s AND ' % (match_different_people_persons, str(i), str(i), str(i), str(i), str(i), e)
        else:
            match_different_people_persons = '%s db%s.activity_ptr_id = da%s.id AND da%s.person_id = dp%s.id AND dp%s.id_parladata = %s' % (match_different_people_persons, str(i), str(i), str(i), str(i), str(i), e)

    # match different parties with organizations
    for i, e in enumerate(parties_different_list):
        if i < len(parties_different_list) - 1:
            match_different_parties_organizations = '%s dpb%s.org_voter_id = do%s.id AND do%s.id_parladata = %s AND ' % (match_different_parties_organizations, str(i), str(i), str(i), e)
        else:
            match_different_parties_organizations = '%s dpb%s.org_voter_id = do%s.id AND do%s.id_parladata = %s' % (match_different_parties_organizations, str(i), str(i), str(i), e)
    
    
    query = beginning
    
    q_selectors_list = [select_same_people, select_same_parties, select_different_people, select_different_parties]
    q_selectors_list_clean = [s for s in q_selectors_list if s != '']
    q_selectors = ', '.join(q_selectors_list_clean)
    print 'q_selectors ' + q_selectors
    
    query = query + ' ' + q_selectors + ' WHERE'

    q_match_ballots_list = [match_same_people_ballots, match_same_parties_ballots, match_different_people_ballots, match_different_parties_ballots]
    q_match_ballots_list_clean = [s for s in q_match_ballots_list if s != '']
    q_match_ballots = ' AND '.join(q_match_ballots_list_clean)
    print 'q_match_ballots ' + q_match_ballots

    # query = query + ' ' + q_match_ballots + ' AND'

    q_match_options_list = [match_same_people_options, match_same_parties_options, match_different_people_options, match_different_parties_options]
    q_match_options_list_clean = [s for s in q_match_options_list if s != '']
    q_match_options = ' AND '.join(q_match_options_list_clean)

    print 'q_match_options ' + q_match_options

    # query = query + ' ' + q_match_options + ' AND'

    q_match_persons_list = [match_same_people_persons, match_different_people_persons]
    q_match_persons_list_clean = [s for s in q_match_persons_list if s != '']
    q_match_persons = ' AND '.join(q_match_persons_list_clean)

    print 'q_match_persons ' + q_match_persons

    # query = query + ' ' + q_match_persons + ' AND'

    q_match_organizations_list = [match_same_parties_organizations, match_different_parties_organizations]
    q_match_organizations_list_clean = [s for s in q_match_organizations_list if s != '']
    q_match_organizations = ' AND '.join(q_match_organizations_list_clean)

    print 'q_match_organizations ' + q_match_organizations

    # query = query + ' ' + q_match_organizations

    after_where_list = [q_match_ballots, q_match_options, q_match_persons, q_match_organizations]
    after_where_list_clean = [s for s in after_where_list if s != '']
    after_where = ' AND '.join(after_where_list_clean)

    query = query + after_where
    
    if request.GET.get('special'):
        # exclude 'ni'
        exclude_ni_people_same = ''
        exclude_ni_parties_same = ''
        exclude_ni_people_different = ''
        exclude_ni_parties_different = ''

        for i, e in enumerate(people_same_list):
            if i < len(people_same_list) - 1:
                exclude_ni_people_same = '%s b%s.option != \'ni\' AND ' % (exclude_ni_people_same, i)
            else:
                exclude_ni_people_same = '%s b%s.option != \'ni\'' % (exclude_ni_people_same, i)
        
        for i, e in enumerate(parties_same_list):
            if i < len(parties_same_list) - 1:
                exclude_ni_parties_same = '%s pb%s.option != \'ni\' AND ' % (exclude_ni_parties_same, i)
            else:
                exclude_ni_parties_same = '%s pb%s.option != \'ni\'' % (exclude_ni_parties_same, i)
        
        for i, e in enumerate(people_different_list):
            if i < len(people_different_list) - 1:
                exclude_ni_people_different = '%s db%s.option != \'ni\' AND ' % (exclude_ni_people_different, i)
            else:
                exclude_ni_people_different = '%s db%s.option != \'ni\'' % (exclude_ni_people_different, i)
        
        for i, e in enumerate(parties_different_list):
            if i < len(parties_different_list) - 1:
                exclude_ni_parties_different = '%s dpb%s.option != \'ni\' AND ' % (exclude_ni_parties_different, i)
            else:
                exclude_ni_parties_different = '%s dpb%s.option != \'ni\'' % (exclude_ni_parties_different, i)

        exclude_ni_list = [exclude_ni_people_same, exclude_ni_parties_same, exclude_ni_people_different, exclude_ni_parties_different]
        exclude_ni_list_clean = [s for s in exclude_ni_list if s != '']
        exclude_ni = ' AND '.join(exclude_ni_list_clean)

        query = query + ' AND ' + exclude_ni
    # return HttpResponse(query)
    print query

    print 'STATEMENT PARTS:'
    print 'select_same_people ' + select_same_people
    print 'select_same_parties ' + select_same_parties
    print 'match_same_people_ballots ' + match_same_people_ballots
    print 'match_same_people_persons ' + match_same_people_persons
    print 'match_same_people_options ' + match_same_people_options
    print 'match_same_parties_ballots ' + match_same_parties_ballots
    print 'match_same_parties_organizations ' + match_same_parties_organizations
    print 'match_same_parties_options ' + match_same_parties_options
    print 'select_different_people ' + select_different_people
    print 'select_different_parties ' + select_different_parties
    print 'match_different_people_ballots ' + match_different_people_ballots
    print 'match_different_people_persons ' + match_different_people_persons
    print 'match_different_people_options ' + match_different_people_options
    print 'match_different_parties_ballots ' + match_different_parties_ballots
    print 'match_different_parties_organizations ' + match_different_parties_organizations
    print 'match_different_parties_options ' + match_different_parties_options

    ballots = Ballot.objects.raw(query)
    session_ids = set([b.vote.session.id for b in ballots])
    sessions = {}
    for s in session_ids:
        sessions[s] = Session.objects.get(id=s).getSessionData()

    print '[SESSION IDS:]'
    print set(session_ids)
    out = {
        'total': Vote.objects.all().count(),
        'results': []
    }

    for ballot in ballots:
        out['results'].append({
            'session': sessions[ballot.vote.session.id],
            'results': {
                'motion_id': ballot.vote.id_parladata,
                'text': ballot.vote.motion,
                'votes_for': ballot.vote.votes_for,
                'against': ballot.vote.against,
                'abstain': ballot.vote.abstain,
                'not_present': ballot.vote.not_present,
                'result': ballot.vote.result,
                'is_outlier': ballot.vote.is_outlier,
                'tags': ballot.vote.tags,
                'date': ballot.start_time.strftime(API_DATE_FORMAT)
            }
        })

    return JsonResponse(out, safe=False)


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
                        'not_present': vot.not_present,
                        'result': vot.result}
                })
        else:
            out.append({'Error': "No vote"})
            return JsonResponse(out, safe=False)
    return JsonResponse(out, safe=False)
