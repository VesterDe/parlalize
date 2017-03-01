import json
import requests

from datetime import datetime, timedelta
from raven.contrib.django.raven_compat.models import client

from parlaposlanci.views import getSlugs, getListOfMembers
from parlaskupine.views import getListOfPGs
from parlaseje.views import getSessionsList
from parlaseje.models import Session
from parlalize.settings import API_DATE_FORMAT, BASE_URL
from parlalize.utils import getAllStaticData

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
    try:
        if not date_:
            tomorrow = datetime.now() + timedelta(days=1)
            date_ = tomorrow.strftime(API_DATE_FORMAT)
        getListOfMembers(None, date_, force_render=True)
        getListOfPGs(None, date_, force_render=True)
        getSessionsList(None, date_, force_render=True)

        # store static data for search
        getAllStaticData(None, force_render=True)
    except:
        client.captureException()

    client.captureMessage('Zgeneriru sem cache za nasledn dan')

    return 1
