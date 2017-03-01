# using for multiprocess runner
def doMembersRunner(data):
    temp_data = data.copy()
    membership = temp_data["membership"]
    toDate = temp_data["toDate"]
    stDate = temp_data["stDate"]
    setters_models = temp_data["setters_models"]
    print "start Date", stDate
    print "todate", toDate
    print "mems_start_time", membership["start_time"]
    print "mems_end_time", membership["end_time"]
    if membership["end_time"]:
        end_time = datetime.strptime(membership["end_time"].split("T")[0],
                                     "%Y-%m-%d").date()
        if end_time > toDate:
            end_time = toDate
    else:
        if membership["start_time"]:
            if datetime.strptime(membership["start_time"].split("T")[0],
                                 "%Y-%m-%d").date() > toDate:
                return
        end_time = toDate

    for model, setter in setters_models.items():
        print setter, toDate
        if membership["start_time"]:
            # print "START", membership["start_time"]
            start_time = datetime.strptime(
                membership["start_time"].split("T")[0], "%Y-%m-%d")
            if stDate is None:
                dates = findDatesFromLastCard(model,
                                              membership["id"],
                                              end_time.strftime(API_DATE_FORMAT),
                                              start_time.strftime(API_DATE_FORMAT))
            else:
                dates = datesGenerator(stDate, toDate)
        else:
            if stDate is None:
                dates = findDatesFromLastCard(model,
                                              membership["id"],
                                              end_time.strftime(API_DATE_FORMAT))
            else:
                dates = datesGenerator(stDate, toDate)
        for date in dates:
            # print date.strftime('%d.%m.%Y')
            # print str(membership["id"]) + "/" + date.strftime('%d.%m.%Y')
            try:
                setter(None, str(membership["id"]), date.strftime('%d.%m.%Y'))
            except:
                client.captureException()
    # setLastActivity allways runs without date
        setLastActivity(None, str(membership["id"]))


# using for multiprocess runner
def doAllMembersRunner(data):
    temp_data = data.copy()
    setter = temp_data["setters"]
    model = temp_data["model"]
    toDate = temp_data["toDate"]
    zero = temp_data["zero"]
    # print(toDate - datetime(day=2, month=8, year=2014).date()).days

    members = tryHard(API_URL + '/getMPs/' + toDate.strftime(API_DATE_FORMAT))
    members = members.json()
    dates = []
    if model == Compass:
        cards = model.objects.all().order_by("created_for")
        if cards:
            dates.append(list(cards)[-1].created_for)
    else:
        for member in members:
            members_cards = model.objects.filter(person__id_parladata=member["id"])
            members_cards = members_cards.order_by("created_for")
            if members_cards:
                dates.append(list(members_cards)[-1].created_for)
    print dates
    if dates:
        zero = min(dates)
    print zero
    print "start all members"+str(setter)
    for i in range((toDate - zero).days):
        print(zero + timedelta(days=i)).strftime('%d.%m.%Y')
        try:
            setter(None, (zero + timedelta(days=i)).strftime('%d.%m.%Y'))
        except:
            client.captureException()


def runSettersMPMultiprocess(date_to):
    """
    stDate uporabljamo takrat ko hocemo pofixati luknje v analizah
    """
    toDate = datetime.strptime(date_to, API_DATE_FORMAT).date()
    zero = datetime(day=2, month=8, year=2014).date()
    setters_models = {
        # model: setter,

        CutVotes: setCutVotes,
        MembershipsOfMember: setMembershipsOfMember,
        LessEqualVoters: setLessEqualVoters,
        EqualVoters: setMostEqualVoters,
        Presence: setPercentOFAttendedSession,

    }

    # Runner for setters ALL
    all_in_one_setters_models = {
        AverageNumberOfSpeechesPerSession: setAverageNumberOfSpeechesPerSessionAll,
        VocabularySize: setVocabularySizeAndSpokenWords,
        Compass: setCompass,
        StyleScores: setStyleScoresALL,
    }

    memberships = tryHard(API_URL + '/getAllTimeMemberships').json()

    pool = Pool(processes=1)
    pool.map(doMembersRunner, [{"membership": membership,
                                "stDate": None,
                                "toDate": toDate,
                                "setters_models": setters_models}
                               for membership in memberships])

    return "all is fine :D"


def morningCash():

    allUrls = [
        # {
        #     "group":"s",
        #     "method":"seznam-odsotnih-poslancev",
        #     "class": "DZ"
        # },{
        #     "group":"p",
        #     "method":"osnovne-informacije",
        #     "class": "all"
        # },{
        #     "group":"p",
        #     "method":"razrez-glasovanj",
        #     "class": "all"
        # },{
        #     "group":"p",
        #     "method":"stilne-analize",
        #     "class": "all"
        # },
        {
             "group":"s",
             "method":"glasovanje-layered",
             "class": "all"
        }
        # {
        #     "group":"p",
        #     "method":"najmanjkrat-enako",
        #     "class": "all"
        # },{
        #     "group":"p",
        #     "method":"najveckrat-enako",
        #     "class": "all"
        # },{
        #     "group":"s",
        #     "method":"glasovanja-seja",
        #     "class": "DZ"
        # },{
        #     "group":"pg",
        #     "method":"razrez-glasovanj",
        #     "class": "all"
        # },{
        #     "group":"p",
        #     "method":"izracunana-prisotnost-glasovanja",
        #     "class": "all"
        # },{
        #     "group":"pg",
        #     "method":"izracunana-prisotnost-seje",
        #     "class": "all"
        # },{
        #     "group":"p",
        #     "method":"glasovanja",
        #     "class": "all"
        # },{
        #     "group":"p",
        #     "method":"izracunana-prisotnost-seje",
        #     "class": "all"
        # },{
        #     "group":"p",
        #     "method":"besedni-zaklad",
        #     "class": "all"
        # },{
        #     "group":"p",
        #     "method":"stevilo-izgovorjenih-besed",
        #     "class": "all"
        # },{
        #     "group":"p",
        #     "method":"clanstva",
        #     "class": "all"
        # },{
        #     "group":"p",
        #     "method":"povezave-do-govorov",
        #     "class": "all"
        # },{
        #     "group":"ps",
        #     "method":"besedni-zaklad",
        #     "class": "all"
        # },{
        #     "group":"ps",
        #     "method":"vsi-govori-poslanske-skupine",
        #     "class": "all"
        # },{
        #     "group":"c",
        #     "method":"kompas",
        #     "class": "none"
        # },{
        #     "group":"pg",
        #     "method":"glasovanja",
        #     "class": "all"
        # },{
        #     "group":"c",
        #     "method":"zadnja-seja",
        #     "class": "none"
        # },{
        #     "group":"p",
        #     "method":"tfidf",
        #     "class": "all"
        # },{
        #     "group":"ps",
        #     "method":"stilne-analize",
        #     "class": "all"
        # },{
        #     "group":"c",
        #     "method":"besedni-zaklad-vsi",
        #     "class": "none"
        # },{
        #     "group":"p",
        #     "method":"povprecno-stevilo-govorov-na-sejo",
        #     "class": "all"
        # },{
        #     "group":"p",
        #     "method":"zadnje-aktivnosti",
        #     "class": "all"
        # },{
        #     "group" : "ps",
        #     "method" : "osnovne-informacije-poslanska-skupina",
        #     "class": "all"
        # },
        # {
        #     "group" : "ps",
        #     "method" : "izracunana-prisotnost-glasovanja",
        #     "class": "all"
        # },
        # {
        #     "group" : "ps",
        #     "method" : "tfidf",
        #     "class": "all"
        # },
        # {
        #     "group" : "wb",
        #     "method" : "getWorkingBodies",
        #     "class" : "all"
        # },
        # {
        #     "group" : "ps",
        #     "method" : "clanice-in-clani-poslanske-skupine",
        #     "class" : "all"
        # },
        # { 
        #     "group" : "pg",
        #     "method" : "najlazje-pridruzili",
        #     "class" : "all"
        # },
        # { 
        #     "group" : "pg",
        #     "method" : "najtezje-pridruzili",
        #     "class" : "all"
        # },
        # { 
        #     "group" : "pg",
        #     "method" : "odstopanje-od-poslanske-skupine",
        #     "class" : "all"
        # },
        # { 
        #     "group" : "s",
        #     "method" : "prisotnost-po-poslanskih-skupinah",
        #     "class" : "DZ"
        # },
        # {
        #     "group" : "p",
        #     "method" : "seznam-poslancev",
        #     "class" : "none"
        # },
        # {
        #     "group" : "ps",
        #     "method" : "seznam-poslanskih-skupin",
        #     "class": "all"
        # }    
    ]

    # allUrls = tryHard("https://glej.parlameter.si/api/cards/getUrls").json()
    theUrl = 'https://glej.parlameter.si/'
    mps = tryHard('https://data.parlameter.si/v1/getMPs').json()
    session = tryHard('https://data.parlameter.si/v1/getSessions/').json()
    wb = tryHard('https://data.parlameter.si/v1/getOrganizatonByClassification')
    wb = wb.json()['working_bodies']
    vote_ids = Vote.objects.all().values_list("id_parladata", flat=True)
    sessionDZ = []
    for ses in session:
        if ses['organization_id'] == DZ:
            sessionDZ.append(ses['id'])

    for url in allUrls:
        if url['group'] == 's':
            if url['method'] == "lasovanje-layered":
                # glasovanja
                method = url['group'] + '/' + url['method'] + '/'
                for vote in vote_ids:
                    requests.get(theUrl + method + str(vote) + '?forceRender=true')
                    requests.get(theUrl + method + str(vote) + '?forceRender=true&frame=true&altHeader=true')
                    requests.get(theUrl + method + str(vote) + '?forceRender=true&embed=true&altHeader=true')
            elif url['class'] == 'DZ':
                #seje DZ
                for ses in sessionDZ:
                    method = url['group'] + '/' + url['method'] + '/'
                    print theUrl + method + str(ses) + '?forceRender=true'
                    requests.get(theUrl + method + str(ses) + '?forceRender=true')
                    requests.get(theUrl + method + str(ses) + '?forceRender=true&frame=true&altHeader=true')
                    requests.get(theUrl + method + str(ses) + '?forceRender=true&embed=true&altHeader=true')
            else:
                #VSE SEJE
                print url['method']
                for ses in Session.objects.values_list("id_parladata", flat=True):
                    method = url['group'] + '/' + url['method'] + '/'
                    print theUrl + method + str(ses) + '?forceRender=true'
                    requests.get(theUrl + method + str(ses) + '?forceRender=true')
                    requests.get(theUrl + method + str(ses) + '?forceRender=true&frame=true&altHeader=true')
                    requests.get(theUrl + method + str(ses) + '?forceRender=true&embed=true&altHeader=true')
        if url['group'] == 'p':
            if url['class'] == "none":
                #kličeš brez IDja s končnim slashem
                method = url['group'] + '/' + url['method'] + '/'
                print theUrl + method + str(ses) + '?forceRender=true'
                requests.get(theUrl + method + '?forceRender=true')
                requests.get(theUrl + method + '?forceRender=true&frame=true&altHeader=true')
                requests.get(theUrl + method + '?forceRender=true&embed=true&altHeader=true')
            else:
                #vsi poslanci
                for mp in mps:
                    method = url['group'] + '/' + url['method'] + '/'
                    print theUrl + method + str(mp['id']) + '?forceRender=true'
                    requests.get(theUrl + method + str(mp['id']) + '?forceRender=true')
                    requests.get(theUrl + method + str(mp['id']) + '?forceRender=true&frame=true&altHeader=true')
                    requests.get(theUrl + method + str(mp['id']) + '?forceRender=true&embed=true&altHeader=true')
        if (url['group'] == 'pg') or (url['group'] == 'ps'):
                for pg in Organization.objects.values_list("id_parladata", flat=True):
                    method = url['group'] + '/' + url['method'] + '/'
                    print theUrl + method + str(pg) + '?forceRender=true'
                    requests.get(theUrl + method + str(pg) + '?forceRender=true')
                    requests.get(theUrl + method + str(pg) + '?forceRender=true&frame=true&altHeader=true')
                    requests.get(theUrl + method + str(pg) + '?forceRender=true&embed=true&altHeader=true')
        if (url['group'] == 'c'):
            # kličeš brez IDja s končnim slashem
            method = url['group'] + '/' + url['method'] + '/'
            requests.get(theUrl + method + '?forceRender=true')
            requests.get(theUrl + method + '?forceRender=true&frame=true&altHeader=true')
            requests.get(theUrl + method + '?forceRender=true&embed=true&altHeader=true')
            print 'yay!'
        if (url['group'] == 'wb'):
            for w in wb:
                method = url['group'] + '/' + url['method'] + '/'
                print theUrl + method + str(w['id']) + '?forceRender=true'
                requests.get(theUrl + method + str(w['id']) + '?forceRender=true')
                requests.get(theUrl + method + str(w['id']) + '?forceRender=true&frame=true&altHeader=true')
                requests.get(theUrl + method + str(w['id']) + '?forceRender=true&embed=true&altHeader=true')
            print 'yay!'