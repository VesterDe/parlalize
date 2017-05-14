# -*- coding: UTF-8 -*-
from datetime import datetime
from django.http import Http404
from parlaposlanci.models import LastActivity
from parlaseje.models import *
from parlalize.settings import API_URL, API_DATE_FORMAT
from django.http import JsonResponse
from parlalize.utils import tryHard


def getGraphCardModel(model, id, date=None):
    if date:
        dateObj = datetime.strptime(date, '%d.%m.%Y')
        modelObject = model.objects.filter(id_parladata=id,
                                           created_at__lte=dateObj)
    else:
        modelObject = model.objects.filter(id_parladata=id,
                                           created_at__lte=datetime.now())
    if not modelObject:
        raise Http404('Nismo našli kartice')
    else:
        newModel = model(**kwargs)
        newModel.save()
        return True
    return False


def getSesIDs(start_date, end_date):
    result = []
    data = tryHard(API_URL + '/getSessions/').json()
    session = Session.objects.all()
    for ids in session:
        result.append(ids.id_parladata)
    return result


def getSesDates(end_date):
    result = []
    data = tryHard(API_URL + '/getSessions/').json()
    session = Session.objects.filter(start_time__lte=end_date)
    for ids in session:
        result.append(ids.start_time)
    return result


def getSesCardModelNew(model, id, date=None):
    if date:
        dateObj = datetime.strptime(date, '%d.%m.%Y')
        modelObject = model.objects.filter(session__id_parladata=id,
                                           created_for__lte=dateObj)
    else:
        modelObject = model.objects.filter(session__id_parladata=id,
                                           created_for__lte=datetime.now())

    if not modelObject:
        raise Http404("Nismo našli kartice")
    else:
        modelObject = modelObject.latest('created_for')
        print "get object ", modelObject.created_for
    return modelObject


def resultOfMotion(yes, no, kvorum, not_present, vote_id, date_=None):
    result = tryHard(API_URL + '/getResultOfMotion/' + str(vote_id)).json()
    allMPs = (int(len(tryHard(API_URL + '/getMPs/' +
                              date_.strftime(API_DATE_FORMAT)).json())) * 2) / 3
    if result['result'] == "1" or result['result'] == "1 ":
        return True
    elif result['result'] == "0" or result['result'] == "0 ":
        return False
    else:
        if yes >= allMPs:
            allMPs = 0
            return True
        else:
            allMPs = 0
            return False


def getSessionDataAPI(requests, session_id):
    session = Session.objects.filter(id_parladata=session_id)

    if session:
        return JsonResponse(session[0].getSessionData())
    else:
        return JsonResponse({'name': 'unkonwn',
                             'date': 'unkonwn',
                             'id': 'unkonwn',
                             })


def idsOfSession(model):
    mod = model.objects.all().values_list('session__id_parladata', flat=True)
    ses = tryHard(API_URL + '/getSessions/').json()
    ids = [session['id'] for session in ses]
    if len(mod) == 0:
        return ids
    else:
        return list(set(ids) - set(mod))
