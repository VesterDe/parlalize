import requests
from datetime import datetime, timedelta
from parlalize.utils import getLogicVotes
from parlalize.settings import API_URL, API_DATE_FORMAT
import numpy as np

from parlalize.utils import tryHard


class RangeVotes(object):

    membersInPGs = None
    allVotesData = None
    membersInPGsRanges = None
    api_url = None
    date_of = None
    votesLogic = None
    votesPlain = None
    votesPerDay = {}
    all_votes = []
    date_ = None

    pg_score_logic = None
    pg_score_plain = None

    def __init__(self, api_url, date_):
        self.api_url = api_url
        self.date_ = date_
        self.loadData(date_)
        self.setVotesPerDay()

    def loadData(self, date_):
        #get data
        r = tryHard(self.api_url+'/getMembersOfPGsOnDate/'+date_)
        self.membersInPGs = r.json()

        r = tryHard(self.api_url+'/getMembersOfPGsRanges/'+date_)
        self.membersInPGsRanges = r.json()

        #create dict votesPerDay
        r = tryHard(self.api_url+'/getAllVotes/'+date_)
        self.allVotesData = r.json()

        if date_:
            self.votesLogic = getLogicVotes(date_)
            r = tryHard(self.api_url+'/getVotes/'+date_)
            self.votesPlain = r.json()
            self.date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
        else:
            self.votesLogic = getLogicVotes()
            r = tryHard(self.api_url+'/getVotes/'+date_)
            self.votesPlain = r.json()
            self.date_of = datetime.now().date()


    def setVotesPerDay(self):
        for vote in self.allVotesData:
            vote_date = vote["start_time"].split("T")[0]
            if vote_date in self.votesPerDay.keys():
                self.votesPerDay[vote_date].append({"id": vote["id"], "time": datetime.strptime(vote["start_time"], "%Y-%m-%dT%X")})
            else:
                self.votesPerDay[vote_date] = [{"id": vote["id"], "time": datetime.strptime(vote["start_time"], "%Y-%m-%dT%X")}]

    def getAverageSocreOfPGs(self, pgs, votes_type=None):
        # get average score of PG
        counter = 0
        for membersInRange in self.membersInPGsRanges:
            start_date = datetime.strptime(membersInRange["start_date"], API_DATE_FORMAT).date()
            end_date = datetime.strptime(membersInRange["end_date"], API_DATE_FORMAT).date()
            days = (end_date - start_date).days
            votes_ids = [vote_id for i in range(days+1) for vote_id in self.getVotesOnDay(self.votesPerDay, (start_date+timedelta(days=i)).strftime("%Y-%m-%d"))]
            if votes_ids==[]:
                continue
            self.all_votes = self.all_votes + votes_ids
            counter+=len(votes_ids)
            if votes_type=="logic":
                print "orvi", [[self.votesLogic[str(member)][str(b)]
                                        for b in votes_ids]
                                        for pg_id in pgs for member in membersInRange["members"][pg_id]]
                pg_score_temp = np.mean([[self.votesLogic[str(member)][str(b)]
                                        for b in votes_ids]
                                        for pg_id in pgs for member in membersInRange["members"][pg_id]],
                                        axis=0)
            else:
                members = [member for pg_id in pgs for member in membersInRange["members"][pg_id]]
            
                pg_score_temp =[self.votesPlain[str(member)][str(b)] for member in members for b in votes_ids]

            if votes_type=="logic":
                self.pg_score_logic = np.concatenate((self.pg_score_logic, pg_score_temp), axis=0)
            else:
                self.pg_score_plain = self.pg_score_plain+pg_score_temp


    def logicCalculations(self, pgs, date_):
        self.pg_score_logic=np.array([])
        self.getAverageSocreOfPGs(pgs, "logic")

        #needs for deviation
        votes_of_pg = {str(voter): votesLogic[str(voter)] for voter in self.membersInPGs[str(pg_id)]}

        #needs for how others matching this group
        votes_of_others = {str(voter): votesLogic[str(voter)] for pg in self.membersInPGs.keys() if pg != str(pg_id) for voter in self.membersInPGs[str(pg)]}



    def plainCalculations(self, pgs, date_):
        self.pg_score_plain=[]
        self.getAverageSocreOfPGs(pgs)




    @staticmethod
    def getVotesOnDay(votesPerDay_, day):
        #tempList = sorted(votesPerDay_, key=lambda k: k['time'])
        if day in votesPerDay_.keys():
            votesPerDay_[day].sort(key=lambda r: r["time"])
        else:
            return []
        try:
            out = [a["id"] for a in votesPerDay_[day]]
            return out
        except:
            return []


range_ = RangeVotes(API_URL)
#range_.logicCalculations(["4"], "17.09.2015")

class Compare():
    def __init__(self):

    def howMatchingThem(request, pg_id, type_of, date_=None):
        if date_:
            date_of = datetime.strptime(date_, API_DATE_FORMAT).date()
        else:
            date_of = datetime.now().date()

        pg_score, membersInPGs, votes, all_votes = getRangeVotes([pg_id], date_, "logic")

        # most match them
        if type_of == "match":
            for voter in membersInPGs[str(pg_id)]:
                votes.pop(str(voter))

        # deviation in PG
        if type_of == "deviation":
            del membersInPGs[str(pg_id)]
            for pgs in membersInPGs.keys():
                for voter in membersInPGs[str(pgs)]:
                    #WORKAROUND: if one person is in more then one PG
                    if voter in votes:
                        votes.pop(str(voter))


        members = getMPsList(request, date_)
        membersDict = {str(mp['id']): mp for mp in json.loads(members.content)}

        #calculate parsonr
        out = {person: (pearsonr(list(pg_score), [votes[str(person)][str(val)] for val in all_votes])[0]+1)*50 for person in sorted(votes.keys())}

        for person in out.keys():
            if math.isnan(out[person]):
                out.pop(person, None)

        keys = sorted(out, key=out.get)
        key4remove = []
        for key in keys:
            # if members isn't member in this time skip him
            if key not in membersDict.keys():
                key4remove.append(key)
                continue
            membersDict[str(key)].update({'ratio': out[str(key)]})
            membersDict[key].update({'id': key})

        #remove keys of members which isn't member in this time
        for key in key4remove:
            keys.remove(key)
        return membersDict, keys, date_of