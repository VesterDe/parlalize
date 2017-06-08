# -*- coding: utf-8 -*-
import json
import requests

from datetime import datetime, timedelta
from raven.contrib.django.raven_compat.models import client

from parlaposlanci.views import getSlugs, getListOfMembers
from parlaskupine.views import getListOfPGs, getIntraDisunionOrg
from parlaseje.views import getSessionsList
from parlaseje.models import Session
from parlaskupine.models import Organization
from parlalize.settings import API_DATE_FORMAT, BASE_URL, API_URL, slack_token
from parlalize.utils import getAllStaticData, tryHard, printProgressBar
from django.db.models import Q
from slackclient import SlackClient

FR = '?forceRender=true'


def updatePages():
    base_url = 'https://parlameter.si/'
    slugs = json.loads(getSlugs(None).content)
    for person_id, person_slug_obj in slugs['person'].items():
        url = base_url + 'poslanec/' + person_slug_obj['slug']
        print url + '/pregled/' + FR

        try:
            print requests.get(url + '/pregled/' + FR)
        except:
            print 'Timeout'
        print url + '/glasovanja' + FR

        try:
            print requests.get(url + '/glasovanja' + FR)
        except:
            print 'Timeout'
        print url + '/govori' + FR

        try:
            print requests.get(url + '/govori' + FR)
        except:
            print 'Timeout'


def updatePagesPG():
    base_url = 'https://parlameter.si/'
    slugs = json.loads(getSlugs(None).content)
    for party_id, party_slug_obj in slugs['party'].items():
        if party_slug_obj['acronym']:
            url = base_url + 'poslanska-skupina/' + party_slug_obj['slug']
            print url + '/pregled/' + FR
            try:
                print requests.get(url + '/pregled/' + FR)
            except:
                print 'Timeout'
            try:
                print requests.get(url + '/glasovanja' + FR)
            except:
                print 'Timeout'
            try:
                print requests.get(url + '/govori' + FR)
            except:
                print 'Timeout'


def updatePagesS(ses_list=None):
    base_url = 'https://parlameter.si/'
    slugs = json.loads(getSlugs(None).content)
    if ses_list:
        ses_ids = ses_list
    else:
        ses_ids = Session.objects.all().values_list('id_parladata', flat=True)
    for session_id in ses_ids:
        url = base_url + 'seja'
        print url + '/prisotnost/' + str(session_id) + FR
        try:
            print requests.get(url + '/prisotnost/' + str(session_id) + FR)
        except:
            print 'Timeout'
        try:
            print requests.get(url + '/transkript/' + str(session_id) + FR)
        except:
            print 'Timeout'
        try:
            print requests.get(url + '/glasovanja/' + str(session_id) + FR)
        except:
            print 'Timeout'


def updateCacheforList(date_=None):
    """
    Method which runs once per day (cron job)
    for recache cache with short lifetime
    """
    sc = SlackClient(slack_token)
    try:
        if not date_:
            tomorrow = datetime.now() + timedelta(days=1)
            date_ = tomorrow.strftime(API_DATE_FORMAT)
        getListOfMembers(None, date_, force_render=True)
        getListOfPGs(None, date_, force_render=True)
        getSessionsList(None, date_, force_render=True)
        updateCacheIntraDisunion()
        # store static data for search
        getAllStaticData(None, force_render=True)
    except:
        client.captureException()

    sc.api_call("chat.postMessage",
                channel="#parlalize_notif",
                text='Zgeneriru sem cache za nasledn dan.')

    return 1


def updateCacheIntraDisunion():
    organizatons = Organization.objects.filter(Q(classification='poslanska skupina') |
                                               Q(classification='stran_vlade') |
                                               Q(name='Državni zbor')).values_list('id_parladata', flat=True)
    for org in organizatons:
        getIntraDisunionOrg(None, str(org), force_render=True)

    return 1

def recacheCards(pgCards=[], mpCards=[], sessions={}, votes_of_s=[]):
    def cardRecache(card_url):
        url = card_url + '?forceRender=true'
        requests.get(url)
        url = card_url + '?forceRender=true&frame=true&altHeader=true'
        requests.get(url)
        url = card_url + '?forceRender=true&embed=true&altHeader=true'
        requests.get(url)

    mps = tryHard(API_URL + '/getMPs/').json()
    mps_ids = [mp['id'] for mp in mps]
    pg_ids = tryHard(API_URL + '/getAllPGs/').json().keys()

    base_url = 'https://glej.parlameter.si/'
    if pgCards:
        for pg in pg_ids:
            for pgCard in pgCards:
                card_url = base_url + 'ps/' + pgCard + '/' + str(pg)
                cardRecache(card_url)
            printProgressBar(pg_ids.index(pg), len(pg_ids), prefix='Orgs: ')

    if mpCards:
        for mp in mps_ids:
            for mpCard in mpCards:
                card_url = base_url + 'p/' + mpCard + '/' + str(mp)
                cardRecache(card_url)
            printProgressBar(mps_ids.index(mp),
                             len(mps_ids),
                             prefix='Members: ')

    if sessions:
        for s in sessions['sessions']:
            for sCard in sessions['cards']:
                card_url = base_url + 's/' + sCard + '/' + str(s)
                cardRecache(card_url)
            printProgressBar(mps_ids.index(mp),
                             len(mps_ids),
                             prefix='Session: ')

    if votes_of_s:
        for s in votes_of_s:
            print "recache votes of session list " + str(s)
            card_url = base_url + 's/' + 'glasovanja-seja' + '/' + str(s)
            cardRecache(card_url)
            print "recache vote graphs of session " + str(s)
            votes = Vote.objects.filter(session__id_parladata=s)
            for v in votes.values_list("id_parladata", flat=True):
                card_url = base_url + 's/' + 'glasovanje-layered-2' + '/' + str(v)
                cardRecache(card_url)
        printProgressBar(votes_of_s.index(s),
                         len(votes_of_s),
                         prefix='Session: ')
