# coding: utf-8

from parlaseje.models import *
from sklearn.decomposition import PCA
from numpy import argpartition


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