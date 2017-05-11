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


def setMotionAnalize(session_id):
    session = get_object_or_404(Session, id_parladata=session_id)
    url = API_URL + '/getVotesOfSessionTable/' + str(session_id) + '/'
    data = pd.read_json(url)
    coalition = requests.get(API_URL + '/getCoalitionPGs').json()['coalition']
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

    parties = data.groupby(['vote_id', 'voterparty']).sum().apply(lambda row: getOptions(row, 'ps'), axis=1)

    for vote_id in all_votes.index.values:
        vote = Vote.objects.get(id_parladata=vote_id)
        vote_a = Vote_analysis.objects.filter(vote__id_parladata=vote_id)
        party_data = {}
        for party in parties[vote_id].keys():
            party_data[party] = parties[vote_id][party]
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
        return json.dumps([])


def getPGsList(row, proti):
    try:
        pgs = [str(pg) for pg in list(proti[row.name].reset_index()['voterparty'])]
        return json.dumps(dict(Counter(pgs)))
    except:
        return json.dumps({})


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
    if side == 'oppo':
        outliers = [opt for opt in ['for', 'against'] if stats[opt]]
    else:
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
