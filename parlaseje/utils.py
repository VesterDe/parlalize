# -*- coding: UTF-8 -*-
from datetime import datetime
from django.http import Http404
from parlaposlanci.models import LastActivity
from parlaseje.models import *
from parlalize.settings import API_URL, API_DATE_FORMAT
from django.http import JsonResponse
from parlalize.utils import tryHard


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


def saveOrAbortMotion(model, **kwargs):
    savedModel = model.objects.filter(**kwargs)
    tab = []
    if savedModel:
        ids = Vote.objects.values('id_parladata')
        for i in ids:
            tab.append(i['id_parladata'])
        for a in savedModel:
            if a.id_parladata in tab:
                print "Not saved"
            else:
                newModel = model(**kwargs)
                newModel.save()
                print "Saved"
    else:
        newModel = model(**kwargs)
        newModel.save()
        print "Saved"


def saveOrAbortAbsent(model, **kwargs):
    tab = []
    value = kwargs['id_parladata']
    if model:
        ids = AbsentMPs.objects.values('id_parladata')
        for i in ids:
            tab.append(i['id_parladata'])
        if int(value) in tab:
            print "Not saved"
            return False
        else:
            newModel = model(**kwargs)
            newModel.save()
            print "Saved"
            return True
    else:
        newModel = model(**kwargs)
        newModel.save()
        print "Saved"


def saveOrAbortPres(model, **kwargs):
    savedModel = kwargs['id_parladata']
    tab = []
    if savedModel:
        ids = model.objects.values('id_parladata')
        for i in ids:
            tab.append(i['id_parladata'])
        if savedModel in tab:
            print "Not saved"
        else:
            newModel = model(**kwargs)
            newModel.save()
            print "Saved"
    else:
        newModel = model(**kwargs)
        newModel.save()
        print "Saved"


def countBallots(vote):
    # count votes for, against, abstentions, misses
    votesfor = len([ballot for ballot in vote.vote.all()
                    if ballot.option == 'za'])
    votesagainst = len(
        [ballot for ballot in vote.vote.all() if ballot.option == 'proti'])
    votesabstained = len(
        [ballot for ballot in vote.vote.all() if ballot.option == 'kvorum'])
    votesmissing = len(
        [ballot for ballot in vote.vote.all() if ballot.option == 'ni'])

    return {'for': votesfor,
            'against': votesagainst,
            'abstained': votesabstained,
            'missing': votesmissing}


def updateVotes():
    for vote in Vote.objects.all():
        counts = countBallots(vote)
        votes_for = counts['for']
        against = counts['against']
        abstain = counts['abstained']
        not_present = counts['missing']
        vote.votes_for = votes_for
        vote.against = against
        vote.abstain = abstain
        vote.not_present = not_present
        vote.save()

    return 1


def getSesIDs(start_date, end_date):
    result = []
    session = Session.objects.all()
    for ids in session:
        result.append(ids.id_parladata)
    return result


def getSesDates(end_date):
    result = []
    session = Session.objects.filter(start_time__lte=end_date)
    for ids in session:
        result.append(ids.start_time)
    return result


def getSesCardModelNew(model, id, date=None):
    if date:
        modelObject = model.objects.filter(session__id_parladata=id,
                                           created_for__lte=datetime.strptime(date, '%d.%m.%Y'))
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
        return JsonResponse({
            'name': "unkonwn",
            'date': "unkonwn",
            'id': "unkonwn",
        })


def idsOfSession(model):
    mod = model.objects.all().values_list('session__id_parladata', flat=True)
    ses = tryHard(API_URL + '/getSessions/').json()
    ids = [session['id'] for session in ses]
    if len(mod) == 0:
        return ids
    else:
        return list(set(ids) - set(mod))
