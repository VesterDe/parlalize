import requests
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.manifold import MDS as sklearnMDS
from parlalize.settings import API_URL, API_DATE_FORMAT, BASE_URL
from parlalize.utils import tryHard


def showCompass():
    """
    Plot compass data
    """
    fig, ax = plt.subplots()
    ax.scatter(ideology, zeros)
    for i, txt in enumerate(people):
        ax.annotate(str(txt), (ideology[i], zeros[i]))
    plt.show()

    return false


def assignValueToOption(option):
    """
    get numeric class for vote option
    """
    if option == 'ni':
        return 0
    if option == 'za':
        return 1
    if option == 'proti':
        return 2
    if option == 'kvorum':
        return 3
    if option == 'ni obstajal':
        return 4


def makeSimilarities(people_ballots_sorted_list):
    """
    make Matrix similarity of ballots for all persons
    """

    similarities = []

    # iterate through people
    for i, personA in enumerate(people_ballots_sorted_list):
        similarities.append([])

        # iterate through people for a second time
        for j, personB in enumerate(people_ballots_sorted_list):

            # start counting similar ballots
            ballot_similarity = 0
            for k, ballot in enumerate(personA):
                if ballot == personB[k]:
                    ballot_similarity = ballot_similarity + 1

            # done comparing with person
            similarities[i].append(ballot_similarity)

    return np.array(similarities)


def enrichData(vT1, vT2, people, date_of):
    """
    prepare output data
    """
    enriched = [{'person_id': str(speaker),
                 'score': {'vT1': vT1[i],
                           'vT2': vT2[i]}} for i, speaker in enumerate(people)]

    return enriched


def getData(date_of):
    """
    group balots for each person and calculate SVD
    """
    # getting all the necessary data
    allballots = tryHard(API_URL+'/getAllBallots/'+date_of.strftime(API_DATE_FORMAT)).json()
    people = tryHard(API_URL+'/getMPs/'+date_of.strftime(API_DATE_FORMAT)).json()

    # sort people's ids
    people_ids = sorted([person['id'] for person in people])

    people_without_ballots = []

    # group ballots by people
    people_ballots = []
    for voter in people_ids:
        people_ballots.append([ballot for ballot in allballots if ballot['voter'] == voter])
        if people_ballots[-1]==[]:
            people_without_ballots.append(voter)
    lengths = [len(person) for person in people_ballots]

    # get ids of all votes
    all_vote_ids = []
    for person in people_ballots:
        for ballot in person:
            all_vote_ids.append(ballot['vote'])
    all_vote_ids = set(all_vote_ids)

    # pad votes and write in "ni obstajal" for people who didn't exist yet
    for person in people_ballots:
        if len(person) < max(lengths):
            for vote_id in all_vote_ids:
                if len(person) == 0:
                    if vote_id not in [ballot['vote'] for ballot in person]:
                        person.append({'vote': vote_id, 'voter': people_without_ballots[0], 'option': 'ni obstajal', 'id': -1})
                        people_without_ballots.remove(people_without_ballots[0])
                else:
                    if vote_id not in [ballot['vote'] for ballot in person]:
                        person.append({'vote': vote_id, 'voter': person[0]['id'], 'option': 'ni obstajal', 'id': -1})

    # sort ballots
    people_ballots_sorted = sorted([sorted(person, key=lambda k: k['vote']) for person in people_ballots], key=lambda j: j[0]['voter'])
    people_ballots_sorted_list = [person for person in people_ballots_sorted]

    hijene = []
    # assign numerical values to ballots
    for i, person in enumerate(people_ballots_sorted_list):
        # print person
        for j, ballot in enumerate(person):
            people_ballots_sorted_list[i][j] = assignValueToOption(ballot['option'])
        if (len(people_ballots_sorted_list[i]) - people_ballots_sorted_list[i].count(4)) < 5:
            hijene.append(i)
            print "brisem", i
    print i
    print people_ids
    hijene.sort()
    for i in reversed(hijene):
        print "delete ", people_ids[i], i
        del people_ballots_sorted_list[i]
        del people_ids[i]
    # transform numerical ballot values to numpy array
    thearray = np.array(people_ballots_sorted_list)

    # generate similarity matrix by adding +1 each time two people's ballots match
    similarities = makeSimilarities(people_ballots_sorted_list)
    u, s, vT = np.linalg.svd(similarities)

    return enrichData(vT[1,:], vT[0,:], people_ids, date_of)
