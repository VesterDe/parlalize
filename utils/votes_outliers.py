# coding: utf-8
from django.shortcuts import get_object_or_404

from parlaseje.models import *
from sklearn.decomposition import PCA
from numpy import argpartition

import pandas as pd
import requests
import json
from collections import Counter

from parlaseje.models import Vote_analysis
from parlalize.settings import API_URL
from parlaskupine.models import Organization, IntraDisunion

from parlalize.utils import printProgressBar


def setOutliers():

    all_votes = Vote.objects.all()
    all_votes.update(is_outlier=False)
    all_votes_as_list = list(all_votes)
    all_votes_as_vectors = [(vote.votes_for, vote.against, vote.abstain, vote.not_present) for vote in all_votes_as_list]

    pca = PCA(n_components=1)
    pca.fit(all_votes_as_vectors)
    distances = pca.score_samples(all_votes_as_vectors)

    number_of_samples = len(all_votes_as_list)/4

    idx = argpartition(distances, number_of_samples)[:number_of_samples]

    vote_ids = [all_votes[i].id for i in idx]

    outlierVotes = Vote.objects.filter(id__in=vote_ids)
    outlierVotes.update(is_outlier=True)

    return 'finished'


def setMotionAnalize(request, session_id):
    """
    request argument is here just because runner put 2 arguments in setter
    setMotionAnalyze
    setIntraDisunion
    """
    session = get_object_or_404(Session, id_parladata=session_id)
    url = API_URL + '/getVotesOfSessionTable/' + str(session_id) + '/'
    data = pd.read_json(url)
    if data.empty:
        return
    coalition = requests.get(API_URL + '/getCoalitionPGs').json()['coalition']
    partys = Organization.objects.filter(classification='poslanska skupina')
    paries_ids = partys.values_list('id_parladata', flat=True)
    orgs = requests.get(API_URL + '/getAllPGsExt/')
    data['option_ni'] = 0
    data['option_za'] = 0
    data['option_proti'] = 0
    data['option_kvorum'] = 0
    data.loc[data['option'] == 'ni', 'option_ni'] = 1
    data.loc[data['option'] == 'za', 'option_za'] = 1
    data.loc[data['option'] == 'proti', 'option_proti'] = 1
    data.loc[data['option'] == 'kvorum', 'option_kvorum'] = 1
    data['voter_unit'] = 1
    data['is_coalition'] = 0
    data.loc[data['voterparty'].isin(coalition), 'is_coalition'] = 1

    #za proti ni kvorum
    all_votes = data.groupby('vote_id').sum()

    all_votes['max_option_percent'] = all_votes.apply(lambda row: getPercent(row['option_za'], row['option_proti'], row['option_kvorum'], row['option_ni']), axis=1)

    m_proti = data[data.option_proti == 1].groupby(['vote_id']).apply(lambda x: x["voter"])
    m_za = data[data.option_za == 1].groupby(['vote_id']).apply(lambda x: x["voter"])
    m_ni = data[data.option_ni == 1].groupby(['vote_id']).apply(lambda x: x["voter"])
    m_kvorum = data[data.option_kvorum == 1].groupby(['vote_id']).apply(lambda x: x["voter"])

    pg_proti = data[data.option_proti == 1].groupby(['vote_id']).apply(lambda x: x["voterparty"])
    pg_za = data[data.option_za == 1].groupby(['vote_id']).apply(lambda x: x["voterparty"])
    pg_ni = data[data.option_ni == 1].groupby(['vote_id']).apply(lambda x: x["voterparty"])
    pg_kvorum = data[data.option_kvorum == 1].groupby(['vote_id']).apply(lambda x: x["voterparty"])

    all_votes['m_proti'] = all_votes.apply(lambda row: getMPsList(row, m_proti), axis=1)
    all_votes['m_za'] = all_votes.apply(lambda row: getMPsList(row, m_za), axis=1)
    all_votes['m_ni'] = all_votes.apply(lambda row: getMPsList(row, m_ni), axis=1)
    all_votes['m_kvorum'] = all_votes.apply(lambda row: getMPsList(row, m_kvorum), axis=1)

    all_votes['pg_proti'] = all_votes.apply(lambda row: getPGsList(row, pg_proti), axis=1)
    all_votes['pg_za'] = all_votes.apply(lambda row: getPGsList(row, pg_za), axis=1)
    all_votes['pg_ni'] = all_votes.apply(lambda row: getPGsList(row, pg_ni), axis=1)
    all_votes['pg_kvorum'] = all_votes.apply(lambda row: getPGsList(row, pg_kvorum), axis=1)

    all_votes['coal'] = data[data.is_coalition == 1].groupby(['vote_id']).sum().apply(lambda row: getOptions(row, 'coal'), axis=1)
    all_votes['oppo'] = data[data.is_coalition == 0].groupby(['vote_id']).sum().apply(lambda row: getOptions(row, 'oppo'), axis=1)

    parties = data.groupby(['vote_id',
                            'voterparty']).sum().apply(lambda row: getOptions(row,
                                                                              'ps'), axis=1)

    partyBallots = data.groupby(['vote_id',
                                 'voterparty']).sum().apply(lambda row: getPartyBallot(row), axis=1)

    partyIntryDisunion = data.groupby(['vote_id', 'voterparty']).sum().apply(lambda row: getIntraDisunion(row), axis=1)
    # TODO: create save-ing for coalInter, oppoInter
    coalInterCalc = data[data.is_coalition == 1].groupby(['vote_id']).sum().apply(lambda row: getIntraDisunion(row), axis=1)
    oppoInterCalc = data[data.is_coalition == 0].groupby(['vote_id']).sum().apply(lambda row: getIntraDisunion(row), axis=1)
    allInter = data.groupby(['vote_id']).sum().apply(lambda row: getIntraDisunion(row), axis=1)

    opozition = Organization.objects.get(name="Opozicija")
    coalition = Organization.objects.get(name="Koalicija")

    for vote_id in all_votes.index.values:
        vote = Vote.objects.get(id_parladata=vote_id)
        vote_a = Vote_analysis.objects.filter(vote__id_parladata=vote_id)

        party_data = {}
        has_outliers = False
        for party in parties[vote_id].keys():
            # save just parlimetary groups
            if party in paries_ids:
                party_data[party] = parties[vote_id][party]
                if json.loads(party_data[party])['outliers']:
                    has_outliers = True
                # update/add IntraDisunion
                intra = IntraDisunion.objects.filter(organization__id_parladata=party,
                                                     vote=vote)
                if intra:
                    intra.update(maximum=partyIntryDisunion[vote_id][party])
                else:
                    org = Organization.objects.get(id_parladata=party)
                    IntraDisunion(organization=org,
                                  vote=vote,
                                  maximum=partyIntryDisunion[vote_id][party]
                                  ).save()
                # save org Ballot
                options = json.loads(partyBallots[vote_id][party])
                for option in options:
                    # if ballot doesn't exist then create it
                    if not Ballot.objects.filter(org_voter__id_parladata=party,
                                                 vote__id_parladata=vote_id,
                                                 option=option):
                        org = Organization.objects.get(id_parladata=party)
                        Ballot(vote=vote,
                               org_voter=org,
                               option=option,
                               start_time=vote.start_time,
                               session=vote.session).save()

        opoIntra = IntraDisunion.objects.filter(organization=opozition,
                                                vote=vote)
        coalIntra = IntraDisunion.objects.filter(organization=coalition,
                                                 vote=vote)

        if opoIntra:
            opoIntra.update(maximum=oppoInterCalc[vote_id])
        else:
            IntraDisunion(organization=opozition,
                          vote=vote,
                          maximum=oppoInterCalc[vote_id]
                          ).save()

        if coalIntra:
            coalIntra.update(maximum=coalInterCalc[vote_id])
        else:
            IntraDisunion(organization=coalition,
                          vote=vote,
                          maximum=coalInterCalc[vote_id]
                          ).save()

        vote.has_outlier_voters = has_outliers
        vote.intra_disunion = allInter[vote_id]
        vote.save()
        print all_votes.loc[vote_id, 'pg_za']
        if vote_a:
            vote_a.update(votes_for=all_votes.loc[vote_id, 'option_za'],
                          against=all_votes.loc[vote_id, 'option_proti'],
                          abstain=all_votes.loc[vote_id, 'option_kvorum'],
                          not_present=all_votes.loc[vote_id, 'option_ni'],
                          pgs_data=party_data,
                          mp_yes=all_votes.loc[vote_id, 'm_za'],
                          mp_no=all_votes.loc[vote_id, 'm_proti'],
                          mp_np=all_votes.loc[vote_id, 'm_ni'],
                          mp_kvor=all_votes.loc[vote_id, 'm_kvorum'],
                          coal_opts=all_votes.loc[vote_id, 'coal'],
                          oppo_opts=all_votes.loc[vote_id, 'oppo'])
        else:
            Vote_analysis(session=session,
                          vote=vote,
                          created_for=vote.start_time,
                          votes_for=all_votes.loc[vote_id, 'option_za'],
                          against=all_votes.loc[vote_id, 'option_proti'],
                          abstain=all_votes.loc[vote_id, 'option_kvorum'],
                          not_present=all_votes.loc[vote_id, 'option_ni'],
                          pgs_data=party_data,
                          mp_yes=all_votes.loc[vote_id, 'm_za'],
                          mp_no=all_votes.loc[vote_id, 'm_proti'],
                          mp_np=all_votes.loc[vote_id, 'm_ni'],
                          mp_kvor=all_votes.loc[vote_id, 'm_kvorum'],
                          coal_opts=all_votes.loc[vote_id, 'coal'],
                          oppo_opts=all_votes.loc[vote_id, 'oppo']).save()


def getPercent(a, b, c, d=None):
    a = 0 if pd.isnull(a) else a
    b = 0 if pd.isnull(b) else b
    c = 0 if pd.isnull(c) else c
    if d:
        d = 0 if pd.isnull(d) else d
        devizer = float(sum([a, b, c, d]))
        if devizer:
            return max(a, b, c, d) / devizer * 100
        else:
            return 0
    else:
        devizer = float(sum([a, b, c]))
        if devizer:
            return max(a, b, c) / devizer * 100
        else:
            return 0


def getMPsList(row, proti):
    try:
        return json.dumps(list(proti[row.name].reset_index()['voter']))
    except:
        try:
            # fix if session has one vote
            return json.dumps(list(proti.values[0]))
        except:
            return json.dumps([])


def getPGsList(row, proti):
    try:
        pgs = [str(pg) for pg in list(proti[row.name].reset_index()['voterparty'])]
        return json.dumps(dict(Counter(pgs)))
    except:
        return json.dumps({})


def getPartyBallot(row):
    """
    using for set ballot of party:

    methodology: ignore not_present
    """
    stats = {'za': row['option_za'],
             'proti': row['option_proti'],
             'kvorum': row['option_kvorum'],
             'ni': row['option_ni']}
    if max(stats.values()) == 0:
        return '[]'
    max_ids = [key for key, val in stats.iteritems() if val == max(stats.values())]
    return json.dumps(max_ids)


def getIntraDisunion(row):
    maxOptionPercent = getPercent(row['option_za'],
                                  row['option_proti'],
                                  row['option_kvorum'])
    if maxOptionPercent == 0:
        return 0
    return 100 - maxOptionPercent


def getOptions(row, side):
    maxOptionPercent = getPercent(row['option_za'],
                                  row['option_proti'],
                                  row['option_kvorum'],
                                  row['option_ni'])
    stats = {'for': row['option_za'],
             'against': row['option_proti'],
             'abstain': row['option_kvorum'],
             'not_present': row['option_ni']}
    max_opt = max(stats, key=stats.get)
    max_ids = [key for key, val in stats.iteritems() if val == max(stats.values())]

    if len(max_ids) > 1:
        if 'not_present' in max_ids:
            max_ids.remove('not_present')
            if len(max_ids) > 1:
                max_vote = 'cant_compute'
            else:
                max_vote = max_ids[0]
        else:
            max_vote = 'cant_compute'
    else:
        max_vote = max_ids[0]

    outliers = []
    if side == 'oppo':
        # if side is oppozition don't show outliers
        pass
        #if max_vote != 'not_present':
        #    outliers = [opt for opt in ['for', 'against'] if stats[opt]]
    else:
        if max_vote != 'not_present':
            outliers = [opt for opt in ['abstain', 'for', 'against'] if stats[opt]]
    for opt in max_ids:
        if opt in outliers:
            outliers.remove(opt)

    return json.dumps({'votes': {
                                 'for': row['option_za'],
                                 'against': row['option_proti'],
                                 'abstain': row['option_kvorum'],
                                 'not_present': row['option_ni'],
                                 },
                       'max': {
                               'max_opt': max_vote,
                               'maxOptPerc': maxOptionPercent
                               },
                       'outliers': outliers})


def updateMotionAnalizeOfAllSessions():
    dz_sessions = Session.objects.filter(organization__id_parladata=95)
    session_ids = list(dz_sessions.values_list("id_parladata", flat=True))

    for session_id in session_ids:
        printProgressBar(session_ids.index(session_id), len(session_ids), prefix='Sessions: ')
        setMotionAnalize(None, str(session_id))

