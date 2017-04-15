# coding: utf-8

from parlaseje.models import *
from sklearn.decomposition import PCA
from numpy import argpartition

all_votes = Vote.objects.all()
all_votes_as_list = list(all_votes)
all_votes_as_vectors = [(vote.votes_for, vote.against, vote.abstain, vote.not_present) for vote in all_votes_as_list]

pca = PCA(n_components=1)
pca.fit(all_votes_as_vectors)
distances = pca.score_samples(all_votes_as_vectors)

number_of_samples = len(all_votes_as_list)/4

ind = argpartition(distances, number_of_samples)[:number_of_samples]

for i in ind: print all_votes_as_vectors[i], all_votes[i].motion
