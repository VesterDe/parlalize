# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from behaviors.models import Timestampable, Versionable
from parlalize.settings import API_OUT_DATE_FORMAT
from datetime import datetime


class PopoloDateTimeField(models.DateTimeField):
    """Converting datetime to popolo."""

    def get_popolo_value(self, value):
        return str(datetime.strftime(value, '%Y-%m-%d'))


class Session(Timestampable, models.Model):
    """Model of all sessions that happened in parliament, copied from parladata."""

    name = models.CharField(_('name'),
                            blank=True, null=True,
                            max_length=128,
                            help_text=_('Session name'))

    date = PopoloDateTimeField(_('date of session'),
                               blank=True, null=True,
                               help_text=_('date of session'))

    id_parladata = models.IntegerField(_('parladata id'),
                                       blank=True, null=True,
                                       help_text=_('id parladata'))

    mandate = models.CharField(_('mandate name'),
                               blank=True, null=True,
                               max_length=128,
                               help_text=_('Mandate name'))

    start_time = PopoloDateTimeField(_('start time of session'),
                                     blank=True, null=True,
                                     help_text='Start time')

    end_time = PopoloDateTimeField(_('end time of session'),
                                   blank=True, null=True,
                                   help_text='End time')

    organization = models.ForeignKey('parlaskupine.Organization',
                                     blank=True, null=True,
                                     related_name='session',
                                     help_text='The organization in session')

    organizations = models.ManyToManyField('parlaskupine.Organization',
                                           related_name='sessions',
                                           help_text='The organizations in session')

    classification = models.CharField(_('classification'),
                                      max_length=128,
                                      blank=True, null=True,
                                      help_text='Session classification')

    actived = models.CharField(_('actived'),
                               null=True, blank=True,
                               max_length=128,
                               help_text=_('Yes if PG is actived or no if it is not'))

    classification = models.CharField(_('classification'),
                                      max_length=128,
                                      blank=True, null=True,
                                      help_text=_('An organization category, e.g. committee'))

    gov_id = models.TextField(blank=True, null=True,
                              help_text='Gov website ID.')

    in_review = models.BooleanField(default=False,
                                    help_text='Is session in review?')

    def __str__(self):
        return self.name

    def getSessionDataMultipleOrgs(self):
        orgs_data = [org.getOrganizationData()
                     for org
                     in self.organizations.all()]
        return {'name': self.name,
                'date': self.start_time.strftime(API_OUT_DATE_FORMAT),
                'date_ts': self.start_time,
                'id': self.id_parladata,
                'orgs': orgs_data,
                'in_review': self.in_review}

    def getSessionData(self):
        orgs_data = [org.getOrganizationData()
                     for org
                     in self.organizations.all()]
        return {'name': self.name,
                'date': self.start_time.strftime(API_OUT_DATE_FORMAT),
                'date_ts': self.start_time,
                'id': self.id_parladata,
                'org': self.organization.getOrganizationData(),
                'orgs': orgs_data,
                'in_review': self.in_review}


class Activity(Timestampable, models.Model):
    """All activities of MP."""

    id_parladata = models.IntegerField(_('parladata id'),
                                       blank=True, null=True,
                                       help_text=_('id parladata'))

    session = models.ForeignKey('Session',
                                blank=True, null=True,
                                related_name="%(app_label)s_%(class)s_related",
                                help_text=_('Session '))

    person = models.ForeignKey('parlaposlanci.Person',
                               blank=True, null=True,
                               help_text=_('MP'))

    start_time = PopoloDateTimeField(blank=True, null=True,
                                     help_text='Start time')

    end_time = PopoloDateTimeField(blank=True, null=True,
                                   help_text='End time')

    def get_child(self):
        if Speech.objects.filter(activity_ptr=self.id):
            return Speech.objects.get(activity_ptr=self.id)
        elif Ballot.objects.filter(activity_ptr=self.id):
            return Ballot.objects.get(activity_ptr=self.id)
        else:
            return Question.objects.get(activity_ptr=self.id)


class Speech(Versionable, Activity):
    """Model of all speeches in parlament."""

    content = models.TextField(blank=True, null=True,
                               help_text='Words spoken')

    order = models.IntegerField(blank=True, null=True,
                                help_text='Order of speech')

    organization = models.ForeignKey('parlaskupine.Organization',
                                     blank=True, null=True,
                                     help_text='Organization')

    def __init__(self, *args, **kwargs):
        super(Activity, self).__init__(*args, **kwargs)

    @staticmethod
    def getValidSpeeches(date_):
        return Speech.objects.filter(valid_from__lt=date_, valid_to__gt=date_)


class Question(Activity):
    """Model of MP questions to the government."""

    content_link = models.URLField(help_text='Words spoken',
                                   max_length=350,
                                   blank=True, null=True)

    title = models.TextField(blank=True, null=True,
                             help_text='Words spoken')

    recipient_persons = models.ManyToManyField('parlaposlanci.Person',
                                               blank=True,
                                               null=True,
                                               help_text='Recipient persons (if it\'s a person).',
                                               related_name='questions')
    recipient_organizations = models.ManyToManyField('parlaskupine.Organization',
                                                     blank=True,
                                                     null=True,
                                                     help_text='Recipient organizations (if it\'s an organization).',
                                                     related_name='questions_org')
    recipient_text = models.TextField(blank=True,
                                      null=True,
                                      help_text='Recipient name as written on dz-rs.si')

    def getQuestionData(self):
        # fix import issue
        from parlalize.utils import getMinistryData
        persons = []
        orgs = []
        for person in self.recipient_persons.all():
            persons.append(getMinistryData(person.id_parladata, self.start_time.strftime(API_DATE_FORMAT)))
        for org in self.recipient_organizations.all():
            orgs.append(org.getOrganizationData())
        return {'title': self.title,
                'recipient_text': self.recipient_text,
                'recipient_persons': persons,
                'recipient_orgs': orgs,
                'url': self.content_link,
                'id': self.id_parladata}


class Ballot(Activity):
    """Model of all ballots"""

    vote = models.ForeignKey('Vote',
                             blank=True, null=True,
                             related_name='vote',
                             help_text=_('Vote'))

    option = models.CharField(max_length=128,
                              blank=True, null=True,
                              help_text='Yes, no, abstain')

    org_voter = models.ForeignKey('parlaskupine.Organization',
                                  blank=True, null=True,
                                  related_name='OrganizationVoter',
                                  help_text=_('Organization voter'))

    def __init__(self, *args, **kwargs):
        super(Activity, self).__init__(*args, **kwargs)


class Vote(Timestampable, models.Model):
    """Model of all votes that happend on specific sessions,
       with number of votes for, against, abstain and not present.
    """

    created_for = models.DateField(_('date of vote'),
                                   blank=True, null=True,
                                   help_text=_('date of vote'))

    session = models.ForeignKey('Session',
                                blank=True, null=True,
                                related_name='in_session',
                                help_text=_('Session '))

    motion = models.TextField(blank=True, null=True,
                              help_text='The motion for which the vote took place')


    tags = JSONField(blank=True, null=True)

    votes_for = models.IntegerField(blank=True, null=True,
                                    help_text='Number of votes for')

    against = models.IntegerField(blank=True, null=True,
                                  help_text='Number votes againt')

    abstain = models.IntegerField(blank=True, null=True,
                                  help_text='Number votes abstain')

    not_present = models.IntegerField(blank=True, null=True,
                                      help_text='Number of MPs that warent on the session')

    result = models.NullBooleanField(blank=True, null=True,
                                     default=False,
                                     help_text='The result of the vote')

    id_parladata = models.IntegerField(_('parladata id'),
                                       blank=True, null=True,
                                       help_text=_('id parladata'))

    document_url = JSONField(blank=True,
                             null=True)

    start_time = PopoloDateTimeField(blank=True,
                                     null=True,
                                     help_text='Start time')

    is_outlier = models.NullBooleanField(default=False,
                                         help_text='is outlier')

    has_outlier_voters = models.NullBooleanField(default=False,
                                                 help_text='has outlier voters')

    intra_disunion = models.FloatField(default=0.0,
                                       help_text='intra disunion for all members')


class VoteDetailed(Timestampable, models.Model):
    """Model of votes with data, how each MP and PG voted."""

    motion = models.TextField(blank=True, null=True,
                              help_text='The motion for which the vote took place')

    session = models.ForeignKey('Session',
                                blank=True, null=True,
                                related_name='in_session_for_VG',
                                help_text=_('Session '))

    vote = models.ForeignKey('Vote',
                             blank=True, null=True,
                             related_name='vote_of_graph',
                             help_text=_('Vote'))

    created_for = models.DateField(_('date of vote'),
                                   blank=True, null=True,
                                   help_text=_('date of vote'))

    votes_for = models.IntegerField(blank=True, null=True,
                                    help_text='Number of votes for')

    against = models.IntegerField(blank=True, null=True,
                                  help_text='Number votes againt')

    abstain = models.IntegerField(blank=True, null=True,
                                  help_text='Number votes abstain')

    not_present = models.IntegerField(blank=True, null=True,
                                      help_text='Number of MPs that warent on the session')

    result = models.NullBooleanField(blank=True, null=True,
                                     default=False,
                                     help_text='The result of the vote')

    pgs_yes = JSONField(blank=True, null=True)
    pgs_no = JSONField(blank=True, null=True)
    pgs_np = JSONField(blank=True, null=True)
    pgs_kvor = JSONField(blank=True, null=True)

    mp_yes = JSONField(blank=True, null=True)
    mp_no = JSONField(blank=True, null=True)
    mp_np = JSONField(blank=True, null=True)
    mp_kvor = JSONField(blank=True, null=True)


class Vote_analysis(Timestampable, models.Model):

    session = models.ForeignKey('Session',
                               blank=True, null=True,
                               related_name='in_session_for_VA',
                               help_text=_('Session '))

    vote = models.ForeignKey('Vote',
                               blank=True, null=True,
                               related_name='analysis',
                               help_text=_('Vote'))

    created_for = models.DateField(_('date of vote'),
                                    blank=True,
                                    null=True,
                                    help_text=_('date of vote'))

    votes_for = models.IntegerField(blank=True, null=True,
                                   help_text='Number of votes for')

    against = models.IntegerField(blank=True, null=True,
                                   help_text='Number votes againt')

    abstain = models.IntegerField(blank=True, null=True,
                                   help_text='Number votes abstain')

    not_present = models.IntegerField(blank=True, null=True,
                                   help_text='Number of MPs that warent on the session')
    pgs_data = JSONField(blank=True, null=True)

    mp_yes = JSONField(blank=True, null=True)
    mp_no = JSONField(blank=True, null=True)
    mp_np = JSONField(blank=True, null=True)
    mp_kvor = JSONField(blank=True, null=True)

    coal_opts = JSONField(blank=True, null=True)

    oppo_opts = JSONField(blank=True, null=True)


class AbsentMPs(Timestampable, models.Model):
    """Model for analysis absent MPs on session."""

    session = models.ForeignKey('Session',
                                blank=True, null=True,
                                related_name='session_absent',
                                help_text=_('Session '))

    absentMPs = JSONField(blank=True, null=True)

    created_for = models.DateField(_('date of vote'),
                                   blank=True, null=True,
                                   help_text=_('date of vote'))


class Quote(Timestampable, models.Model):
    """Model for quoted text from speeches."""

    quoted_text = models.TextField(_('quoted text'),
                                   blank=True, null=True,
                                   help_text=_('text quoted in a speech'))

    speech = models.ForeignKey('Speech',
                               help_text=_('the speech that is being quoted'))

    first_char = models.IntegerField(blank=True, null=True,
                                     help_text=_('index of first character of quote string'))

    last_char = models.IntegerField(blank=True, null=True,
                                    help_text=_('index of last character of quote string'))


class PresenceOfPG(Timestampable, models.Model):
    """Model for analysis presence of PG on session."""

    session = models.ForeignKey('Session',
                                blank=True, null=True,
                                related_name='session_presence',
                                help_text=_('Session '))

    presence = JSONField(blank=True, null=True)

    created_for = models.DateField(_('date of activity'),
                                   blank=True, null=True,
                                   help_text=_('date of analize'))


class Tfidf(Timestampable, models.Model):
    """Model for analysis TFIDF."""

    session = models.ForeignKey('Session',
                                blank=True, null=True,
                                related_name='tfidf',
                                help_text=_('Session '))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    is_visible = models.BooleanField(_('is visible'),
                                     default=True)

    data = JSONField(blank=True, null=True)

    def __str__(self):
        return unicode(self.session.name) + " --> " + unicode(self.session.organization.name)


class Tag(models.Model):
    """All tags of votes."""

    id_parladata = models.IntegerField(_('parladata id'),
                                       blank=True,
                                       null=True,
                                       help_text=_('id parladata'))

    name = models.TextField(blank=True,
                            null=True,
                            help_text=_('tag name'))