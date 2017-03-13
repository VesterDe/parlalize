import csv
import pandas as pd
import json

from datetime import datetime

from parlalize.settings import API_URL, API_DATE_FORMAT
from parlalize.utils import tryHard, saveOrAbortNew

from parlaseje.models import Session
from parlaposlanci.models import Person, EqualVoters, LessEqualVoters, Presence
from parlaskupine.models import Organization, MostMatchingThem, LessMatchingThem, DeviationInOrganization, PercentOFAttendedSession


VOTE_MAP = {'za': 1,
            'proti': -1,
            'kvorum': 0,
            'ni': 0,
            'ni_poslanec': 0
            }


class VotesAnalysis(object):
    def __init__(self, date_=None):
        self.debug = False
        if date_:
            self.date_ = date_.strftime(API_DATE_FORMAT)
            self.date_of = date_
        else:
            self.date_ = ''
            self.date_of = datetime.now()
        self.api_url = None
        self.members = None
        self.data = None

        self.presenceOfPGsSignleSessions = None
        self.presenceMP_S = None
        self.presenceMP_V = None
        self.equalVotersData = None
        self.equalVotersPGData = None
        self.memsOfPGs = None
        self.presencePGs = None
        self.pgs = None

        print 'getData'
        self.prepareData()

        # analyse
        print 'analyse'
        self.presenceMPsSessions()
        self.presenceMPsVotes()
        self.presencePGsTogether()
        self.equalVoters()
        self.equalVotersPG()

    def prepareData(self):
        if self.debug:
            self.data = pd.read_pickle('backup_baze.pkl')
        else:
            url = API_URL + '/getVotesTable/' + self.date_
            print url
            self.data = pd.read_json(url)
            # before debug load data to backup_baze.pkl file (uncoment next line)
            # self.data.to_pickle('backup_baze.pkl')
        url = API_URL + '/getMPs/' + self.date_
        print url
        mps = tryHard(url).json()
        self.members = [mp['id'] for mp in mps]
        url = API_URL + '/getMembersOfPGsOnDate/' + self.date_
        print url
        self.memsOfPGs = tryHard(url).json()
        url = API_URL + '/getAllPGs/' + self.date_
        print url
        self.pgs = tryHard(url).json()
        self.pgs = self.pgs.keys()

        def toLogic(row):
            """
            voter option to logic value
            """
            return VOTE_MAP[row['option']]

        # prepere helper columns (logic, option_ni, voter_unit)
        self.data['logic'] = self.data.apply(lambda row: toLogic(row), axis=1)
        self.data['option_x'] = 0
        self.data.loc[self.data['option'] == 'ni', 'option_x'] = 1
        self.data['voter_unit'] = 1

    # analyses
    def presencePGsSingleSessions(self):
        """
        Analyse presence of partys on single sessions
        """
        data2 = self.data.groupby(['voterparty',
                                   'session_id'],).sum().reset_index()
        data2['attendance'] = 100 * (1 - data2.option_x / data2.voter_unit)
        self.presenceOfPGsSignleSessions = data2

    def presenceMPsSessions(self):
        """
        Analyse members presence on sessions
        """
        data2 = self.data.groupby(['voter', 'session_id']).sum().reset_index()
        data2['attendance'] = 1 - data2.option_x / data2.voter_unit
        nonAttendanceCount = data2[data2.attendance == 0.0].groupby(['voter'])
        nonAttendanceCount = nonAttendanceCount.count().id.reset_index()
        allSessionsCount = data2.groupby(['voter']).count().id.reset_index()
        out = pd.merge(nonAttendanceCount,
                       allSessionsCount,
                       on='voter',
                       how='right')
        out['attendance'] = 100 * (1 - out.id_x / out.id_y)
        self.presenceMP_S = out

    def presenceMPsVotes(self):
        """
        Analyse members presence on votes
        """
        data2 = self.data.groupby(['voter']).sum().reset_index()
        data2['attendance'] = 100 * (1 - data2.option_x / data2.voter_unit)
        out = data2[['voter', 'attendance']]
        self.presenceMP_V = out

    def presencePGsTogether(self):
        """
        Analyse partys presence on sessions and votes
        get average score of members in party
        """
        pSes = self.presenceMP_S
        pVote = self.presenceMP_V
        pg_mps = self.memsOfPGs
        pgs = [key for key, value in pg_mps.items() if value]
        sessions = [pSes[pSes.voter.isin(pg_mps[pg])].mean().attendance
                    for pg
                    in pgs]

        votes = [pVote[pVote.voter.isin(pg_mps[pg])].mean().attendance
                 for pg
                 in pgs]
        d = {'pg': pd.Series(pgs, index=pgs),
             'votes': pd.Series(votes, index=pgs),
             'sessions': pd.Series(sessions, index=pgs)}
        self.presencePGs = pd.DataFrame(d)

    def equalVoters(self):
        """
        Analyse how equal are voters
        """
        data2 = self.data[['voter',
                           'vote_id',
                           'logic']].pivot('voter', 'vote_id')
        data2 = data2.transpose().reset_index().iloc[:, 2:]
        zero_data = data2.fillna(0)
        distance = lambda column1, column2: pd.np.linalg.norm(column1 - column2)
        result = zero_data.apply(lambda col1: zero_data.apply(lambda col2: distance(col1, col2)))
        self.equalVotersData = result

    def equalVotersPG(self):
        """
        Analyse how equal are voters to partys and deviation in party
        """
        averagePGs = self.data[['voterparty',
                                'vote_id',
                                'logic']].groupby(['voterparty',
                                                   'vote_id']).mean()
        averagePGs = averagePGs.reset_index().pivot('voterparty',
                                                    'vote_id').transpose()
        membersLogis = self.data[['voter',
                                  'vote_id',
                                  'logic']].pivot('voter',
                                                  'vote_id').transpose()

        zero_data_pg = averagePGs.fillna(0)
        zero_data_mp = membersLogis.fillna(0)
        distance = lambda column1, column2: pd.np.linalg.norm(column1 - column2)
        result = zero_data_pg.apply(lambda col1: zero_data_mp.apply(lambda col2: distance(col1, col2)))
        self.equalVotersPGData = result

    # setters
    def setEqualVoters(self):
        """
        set cards how equal are voters
        """
        for mp in self.members:
            print '.:' + str(mp) + ':.'
            person = Person.objects.get(id_parladata=int(mp))
            r = self.equalVotersData[mp]
            mps_data = r.reset_index().sort_values(mp, ascending=False)

            # most equal
            most_data = []
            data = mps_data[-6:-1]
            for idx in range(5):
                member_id = int(data.iloc[idx]['voter'])
                member = Person.objects.get(id_parladata=member_id)
                most_data.append({'member': member,
                                  'score': data.iloc[idx][mp]})
            most_data = list(reversed(most_data))

            result = saveOrAbortNew(model=EqualVoters,
                                    created_for=self.date_of,
                                    person=person,
                                    person1=most_data[0]['member'],
                                    votes1=most_data[0]['score'],
                                    person2=most_data[1]['member'],
                                    votes2=most_data[1]['score'],
                                    person3=most_data[2]['member'],
                                    votes3=most_data[2]['score'],
                                    person4=most_data[3]['member'],
                                    votes4=most_data[3]['score'],
                                    person5=most_data[4]['member'],
                                    votes5=most_data[4]['score'])

            # less equal
            less_data = []
            data = mps_data[:5]
            for idx in range(5):
                member_id = int(data.iloc[idx]['voter'])
                member = Person.objects.get(id_parladata=member_id)
                less_data.append({'member': member,
                                  'score': data.iloc[idx][mp]})

            result = saveOrAbortNew(model=LessEqualVoters,
                                    created_for=self.date_of,
                                    person=person,
                                    person1=less_data[0]['member'],
                                    votes1=less_data[0]['score'],
                                    person2=less_data[1]['member'],
                                    votes2=less_data[1]['score'],
                                    person3=less_data[2]['member'],
                                    votes3=less_data[2]['score'],
                                    person4=less_data[3]['member'],
                                    votes4=less_data[3]['score'],
                                    person5=less_data[4]['member'],
                                    votes5=less_data[4]['score'])

    def setEqualVotesPG(self):
        """
        set cards how equal are voters to Partys
        """
        results = self.equalVotersPGData
        for pg in results.keys():
            org = Organization.objects.get(id_parladata=int(pg))
            r = results[pg]
            r = r.reset_index().sort_values(pg, ascending=False)
            thisPG = r[r.voter.isin(self.memsOfPGs[str(pg)])]
            otherMembers = [m
                            for pg_key
                            in self.memsOfPGs.keys()
                            if pg_key != str(pg)
                            for m
                            in self.memsOfPGs[pg_key]
                            ]
            print 'pg', pg, len(self.memsOfPGs[str(pg)]), len(otherMembers)
            otherMems = r[r.voter.isin(otherMembers)]

            # most equal
            most_data = []
            data = otherMems[-6:-1]
            for idx in range(5):
                member_id = int(data.iloc[idx]['voter'])
                member = Person.objects.get(id_parladata=member_id)
                most_data.append({'member': member,
                                  'score': data.iloc[idx][pg]})
            most_data = list(reversed(most_data))

            result = saveOrAbortNew(model=MostMatchingThem,
                                    created_for=self.date_of,
                                    organization=org,
                                    person1=most_data[0]['member'],
                                    votes1=most_data[0]['score'],
                                    person2=most_data[1]['member'],
                                    votes2=most_data[1]['score'],
                                    person3=most_data[2]['member'],
                                    votes3=most_data[2]['score'],
                                    person4=most_data[3]['member'],
                                    votes4=most_data[3]['score'],
                                    person5=most_data[4]['member'],
                                    votes5=most_data[4]['score'])
            # less equal
            print otherMems[:5]
            less_data = []
            data = otherMems[:5]
            for idx in range(5):
                member_id = int(data.iloc[idx]['voter'])
                member = Person.objects.get(id_parladata=member_id)
                less_data.append({'member': member,
                                  'score': data.iloc[idx][pg]})

            result = saveOrAbortNew(model=LessMatchingThem,
                                    created_for=self.date_of,
                                    organization=org,
                                    person1=less_data[0]['member'],
                                    votes1=less_data[0]['score'],
                                    person2=less_data[1]['member'],
                                    votes2=less_data[1]['score'],
                                    person3=less_data[2]['member'],
                                    votes3=less_data[2]['score'],
                                    person4=less_data[3]['member'],
                                    votes4=less_data[3]['score'],
                                    person5=less_data[4]['member'],
                                    votes5=less_data[4]['score'])
            # deviation
            print thisPG
            dev_data = []
            for idx in range(thisPG.count()['voter']):
                dev_data.append({'id': thisPG.iloc[idx]['voter'],
                                 'ratio': thisPG.iloc[idx][pg]})
            result = saveOrAbortNew(model=DeviationInOrganization,
                                    created_for=self.date_of,
                                    organization=org,
                                    data=dev_data
                                    )

    def setPresenceMPs(self):
        """
        set presence for all Members
        """
        votes = self.presenceMP_V
        sessions = self.presenceMP_S

        self.members
        actualVotes = votes[votes.voter.isin(self.members)]
        avgVote = actualVotes[['attendance']].mean().attendance
        maxVote = actualVotes.max()

        actualSession = sessions[sessions.voter.isin(self.members)]
        avgSession = actualSession[['attendance']].mean().attendance
        maxSession = actualSession.max()

        for mp in self.members:
            person = Person.objects.get(id_parladata=int(mp))
            thisVotes = votes[votes.voter == mp].reset_index().at[0, 'attendance']
            tempS = sessions[sessions.voter == mp].reset_index()
            thisSession = tempS.at[0, 'attendance']
            print mp

            result = saveOrAbortNew(model=Presence,
                                    created_for=self.date_of,
                                    person=person,
                                    person_value_sessions=thisSession*100,
                                    maxMP_sessions=[int(maxSession.voter)],
                                    average_sessions=avgSession*100,
                                    maximum_sessions=maxSession.attendance*100,
                                    person_value_votes=thisVotes*100,
                                    maxMP_votes=[int(maxVote.voter)],
                                    average_votes=avgVote*100,
                                    maximum_votes=maxVote.attendance*100)

    def setPresenceOfPGs(self):
        """
        set presence for all Partys
        """
        table = self.presencePGs

        averageSessions = table['sessions'].mean()
        averageVotes = table['votes'].mean()

        maxVotes = table['votes'].max()
        maxVotesOrgIdx = table['votes'].idxmax()

        maxSessions = table['sessions'].max()
        maxSessionOrgIdx = table['sessions'].idxmax()

        for pg in self.pgs:
            thisSessions = table[table.pg == pg].sessions[pg]
            thisVotes = table[table.pg == pg].votes[pg]
            thisOrg = Organization.objects.get(id_parladata=pg)
            result = saveOrAbortNew(model=PercentOFAttendedSession,
                                    created_for=self.date_of,
                                    organization=thisOrg,
                                    organization_value_sessions=thisSessions,
                                    maxPG_sessions=[maxSessionOrgIdx],
                                    average_sessions=averageSessions,
                                    maximum_sessions=maxSessions,
                                    organization_value_votes=thisVotes,
                                    maxPG_votes=[maxVotesOrgIdx],
                                    average_votes=averageVotes,
                                    maximum_votes=maxVotes)

    def setAll(self):
        """
        set all vote cards
        """
        self.setPresenceMPs()
        self.setPresenceOfPGs()
        self.setEqualVoters()
        self.setEqualVotesPG()
