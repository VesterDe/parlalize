
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
                                    person_value_sessions=thisSession,
                                    maxMP_sessions=[int(maxSession.voter)],
                                    average_sessions=avgSession,
                                    maximum_sessions=maxSession.attendance,
                                    person_value_votes=thisVotes,
                                    maxMP_votes=[int(maxVote.voter)],
                                    average_votes=avgVote,
                                    maximum_votes=maxVote.attendance)

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
