from parlalize.utils import tryHard
from parlalize.settings import API_URL, API_DATE_FORMAT
from parlaposlanci.models import Person, District
from parlaskupine.models import Organization
from parlaseje.models import Session, Speech, Question, Ballot, Vote, Question
# parlalize initial runner methods #

DZ = 95


def updatePeople():
    data = tryHard(API_URL + '/getAllPeople/').json()
    mps = tryHard(API_URL + '/getMPs/').json()
    mps_ids = [mp['id'] for mp in mps]
    for mp in data:
        if Person.objects.filter(id_parladata=mp['id']):
            person = Person.objects.get(id_parladata=mp['id'])
            person.name = mp['name']
            person.pg = mp['membership']
            person.id_parladata = int(mp['id'])
            person.image = mp['image']
            person.actived = True if int(mp['id']) in mps_ids else False
            person.gov_id = mp['gov_id']
            person.save()
        else:
            is_active = True if int(mp['id']) in mps_ids else False
            person = Person(name=mp['name'],
                            pg=mp['membership'],
                            id_parladata=int(mp['id']),
                            image=mp['image'],
                            actived=is_active,
                            gov_id=mp['gov_id'])
            person.save()

    return 1


def updateOrganizations():
    data = tryHard(API_URL + '/getAllOrganizations').json()
    for pg in data:
        if Organization.objects.filter(id_parladata=pg):
            org = Organization.objects.get(id_parladata=pg)
            org.name = data[pg]['name']
            org.classification = data[pg]['classification']
            org.acronym = data[pg]['acronym']
            org.is_coalition = data[pg]['is_coalition']
            print data[pg]['acronym']
            org.save()
        else:
            org = Organization(name=data[pg]['name'],
                               classification=data[pg]['classification'],
                               id_parladata=pg,
                               acronym=data[pg]['acronym'],
                               is_coalition=data[pg]['is_coalition'])
            org.save()
    return 1


def deleteUnconnectedSpeeches():
    data = tryHard(API_URL + '/getAllSpeeches').json()
    idsInData = [speech['id'] for speech in data]
    blindSpeeches = Speech.objects.all().exclude(id_parladata__in=idsInData)
    blindSpeeches.delete()


def updateSpeeches():
    data = tryHard(API_URL + '/getAllAllSpeeches').json()
    existingISs = list(Speech.objects.all().values_list('id_parladata',
                                                        flat=True))
    for dic in data:
        if int(dic['id']) not in existingISs:
            print 'adding speech'
            print dic['valid_to']
            person = Person.objects.get(id_parladata=int(dic['speaker']))
            speech = Speech(person=person,
                            organization=Organization.objects.get(
                                id_parladata=int(dic['party'])),
                            content=dic['content'], order=dic['order'],
                            session=Session.objects.get(
                                id_parladata=int(dic['session'])),
                            start_time=dic['start_time'],
                            end_time=dic['end_time'],
                            valid_from=dic['valid_from'],
                            valid_to=dic['valid_to'],
                            id_parladata=dic['id'])
            speech.save()
        else:
            print 'update speech'
            speech = Speech.objects.filter(id_parladata=dic['id'])
            speech.update(valid_from=dic['valid_from'],
                          valid_to=dic['valid_to'])

    # delete speeches which was deleted in parladata @dirty fix
    deleteUnconnectedSpeeches()
    return 1


def updateQuestions():
    data = tryHard(API_URL + '/getAllQuestions').json()
    existingISs = list(Question.objects.all().values_list("id_parladata",
                                                          flat=True))
    for dic in data:
        if int(dic["id"]) not in existingISs:
            print "adding question"
            if dic['session_id']:
                session = Session.objects.get(id_parladata=int(dic['session_id']))
            else:
                session = None
            link = dic['link'] if dic['link'] else None
            person = Person.objects.get(id_parladata=int(dic['author_id']))
            if dic['recipient_id']:
                rec_p = list(Person.objects.filter(id_parladata__in=dic['recipient_id']))
            else:
                rec_p = []
            if dic['recipient_org_id']:
                rec_org = list(Organization.objects.filter(id_parladata__in=dic['recipient_org_id']))
            else:
                rec_org = []
            question = Question(person=person,
                                session=session,
                                start_time=dic['date'],
                                id_parladata=dic['id'],
                                recipient_text=dic['recipient_text'],
                                title=dic['title'],
                                content_link=link,
                                )
            question.save()
            question.recipient_persons.add(*rec_p)
            question.recipient_organizations.add(*rec_org)
        else:
            print "update question"
            if dic['recipient_id']:
                rec_p = list(Person.objects.filter(id_parladata__in=dic['recipient_id']))
            else:
                rec_p = []
            if dic['recipient_org_id']:
                rec_org = list(Organization.objects.filter(id_parladata__in=dic['recipient_org_id']))
            else:
                rec_org = []
            question = Question.objects.get(id_parladata=dic["id"])
            question.recipient_persons.add(*rec_p)
            question.recipient_organizations.add(*rec_org)

    return 1

# treba pofixsat


def updateMotionOfSession():
    ses = Session.objects.all()
    for s in ses:
        print s.id_parladata
        tryHard(BASE_URL + '/s/setMotionOfSession/' + str(s.id_parladata))

# treba pofixsat


def updateBallots():
    data = tryHard(API_URL + '/getAllBallots').json()
    existingISs = Ballot.objects.all().values_list('id_parladata', flat=True)
    for dic in data:
        # Ballot.objects.filter(id_parladata=dic['id']):
        if int(dic['id']) not in existingISs:
            print 'adding ballot ' + str(dic['vote'])
            vote = Vote.objects.get(id_parladata=dic['vote'])
            person = Person.objects.get(id_parladata=int(dic['voter']))
            ballots = Ballot(person=person,
                             option=dic['option'],
                             vote=vote,
                             start_time=vote.start_time,
                             end_time=None,
                             id_parladata=dic['id'])
            ballots.save()
    return 1


def setAllSessions():
    data = tryHard(API_URL + '/getSessions/').json()
    session_ids = list(Session.objects.all().values_list('id_parladata',
                                                         flat=True))
    for session in data:
        print session['id']
        orgs = Organization.objects.filter(id_parladata__in=session['organizations_id'])
        if not orgs:
            orgs = Organization.objects.filter(id_parladata=session['organization_id'])
        if session['id'] not in session_ids:
            result = Session(name=session['name'],
                             gov_id=session['gov_id'],
                             start_time=session['start_time'],
                             end_time=session['end_time'],
                             classification=session['classification'],
                             id_parladata=session['id'],
                             in_review=session['is_in_review'],
                             organization=orgs[0]
                             )
            result.save()
            orgs = list(orgs)
            result.organizations.add(*orgs)
            if session['id'] == DZ:
                if 'redna seja' in session['name'].lower():
                    # call method for create new list of members
                    # setListOfMembers(session['start_time'])
                    pass
        else:
            ses = Session.objects.filter(name=session['name'],
                                         gov_id=session['gov_id'],
                                         start_time=session['start_time'],
                                         end_time=session['end_time'],
                                         classification=session['classification'],
                                         id_parladata=session['id'],
                                         in_review=session['is_in_review'],
                                         organization=orgs[0])
            ses = ses.exclude(organizations=None)
            if not session:
                # save changes
                session2 = Session.objects.get(id_parladata=session['id'])
                session2.name = session['name']
                session2.gov_id = session['gov_id']
                session2.start_time = session['start_time']
                session2.end_time = session['end_time']
                session2.classification = session['classification']
                session2.in_review = session['is_in_review']
                session2.organization = orgs[0]
                session2.save()
                orgs = list(orgs)
                session2.organizations.add(*orgs)

    return 1


def updateMinistrers():
    start_date = datetime(day=2, month=8, year=2014)
    days = range((datetime.now()-start_date).days)
    prev_ministers = []
    for day in days:
        today = start_date + timedelta(days=day)
        print today
        ministers = tryHard(API_URL + '/getIDsOfAllMinisters/' + today.strftime(API_DATE_FORMAT)).json()['ministers_ids']
        diff = list(set(ministers) - set(prev_ministers))
        if diff:
            for person in diff:
                print person
                setMinsterStatic(None, str(person), today.strftime(API_DATE_FORMAT))
            prev_ministers = ministers


def updateDistricts():
    districts = tryHard(API_URL + '/getDistricts').json()
    existing_districts = District.objects.all().values_list('id_parladata',
                                                            flat=True)
    for district in districts:
        if district['id'] not in existing_districts:
            District(name=district['name'], id_parladata=district['id']).save()
        else:
            dist = District.objects.get(id_parladata=district['id'])
            if dist.name != district['name']:
                dist.name = district['name']
                dist.save()
    return 1


def updateTags():
    tags = tryHard(API_URL+'/getTags').json()
    existing_tags = Tag.objects.all().values_list('id_parladata', flat=True)
    count = 0
    for tag in tags:
        if tag['id'] not in existing_tags:
            Tag(name=tag['name'], id_parladata=tag['id']).save()
            count += 1
    return 1


def updatePersonStatus():
    mps = tryHard(API_URL + '/getMPs').json()
    mps_ids = [mp['id'] for mp in mps]
    for person in Person.objects.all():
        if person.actived == 'Yes':
            if person.id_parladata not in mps_ids:
                person.actived = 'No'
                person.save()
        else:
            if person.id_parladata in mps_ids:
                person.actived = 'Yes'
                person.save()


def updatePersonFunctions():
    mps = tryHard(API_URL + '/getMembersWithFuction').json()

    for person in Person.objects.all():
        if person.has_function:
            if person.id_parladata not in mps['members_with_function']:
                person.has_function = False
                person.save()
        else:
            if person.id_parladata in mps['members_with_function']:
                person.has_function = True
                person.save()


def update():
    updateOrganizations()
    print 'org'

    updatePeople()
    print 'pep'

    updateMinistrers()
    print 'ministers'

    setAllSessions()
    print 'Sessions'

    updateSpeeches()
    print 'speeches'

    updateMotionOfSession()
    print 'votes'

    updateBallots()
    print 'ballots'

    updateDistricts()

    updateTags()

    print 'update person status'
    updatePersonStatus()

    print 'update person has_function'
    updatePersonFunctions()

    return 1
