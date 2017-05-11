# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from parlaposlanci.models import *
from parlaseje.models import *
from jsonfield import JSONField
from behaviors.models import Timestampable

# converting datetime to popolo
class PopoloDateTimeField(models.DateTimeField):

    def get_popolo_value(self, value):
        return str(datetime.strftime(value, '%Y-%m-%d'))

# Create your models here.
@python_2_unicode_compatible
class Organization(Timestampable, models.Model):
    """
    A group with a common purpose or reason for existence that goes beyond the set of people belonging to it
    """

    name = models.TextField(_('name'),
                            help_text=_('A primary name, e.g. a legally recognized name'))

    id_parladata = models.IntegerField(_('parladata id'),
                                       blank=True,
                                       null=True,
                                       help_text=_('id parladata'))

    classification = models.TextField(_('Classification'),
                                      blank=True,
                                      null=True,
                                      help_text=_('Organization calssification.'))

    acronym = models.CharField(_('acronym'),
                               blank = True,
                               null = True,
                               max_length = 128,
                               help_text=_('Organization acronym'))

    is_coalition = models.BooleanField(_('coalition'),
                                      default=False)

    def __str__(self):
        return unicode(self.name) + " " + str(self.id_parladata)

    def getOrganizationData(self):
        return {
                  'id': self.id_parladata,
                  'name': self.name,
                  'acronym': self.acronym,
                  'is_coalition': self.is_coalition,
               }


class PGStatic(Timestampable, models.Model):
    organization = models.ForeignKey('Organization', 
                                     help_text=_('Organization foreign key relationship'))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    headOfPG = models.ForeignKey('parlaposlanci.Person',
                                 null = True,
                                 related_name='PGStaticH', help_text=_('Head of MP'))

    viceOfPG = JSONField(blank=True, null=True)

    numberOfSeats = models.IntegerField(blank = True, 
                                        null = True, 
                                        help_text = _('Number of seats in parlament of PG'))

    allVoters = models.IntegerField(blank=True, 
                                    null=True, 
                                    help_text=_('Number of voters'))

    facebook = models.TextField(blank=True, 
                                null=True, 
                                default=None, 
                                help_text=_('Facebook profile URL'))

    twitter = models.TextField(blank=True, 
                               null=True, 
                               default=None, 
                               help_text=_('Twitter profile URL'))

    email = models.TextField(blank=True, 
                             null=True, 
                             default=None, 
                             help_text=_('email profile URL'))

class PercentOFAttendedSession(Timestampable, models.Model): #Model for presence of PG on sessions

    organization = models.ForeignKey('Organization',
                               blank=True, null=True,
                               related_name='childrenPG',
                               help_text=_('PG'))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    organization_value_sessions = models.FloatField(_('Presence of this PG'),
                                   blank=True, null=True,
                                   help_text=_('Presence of this PG'))


    maxPG_sessions = JSONField(blank=True, null=True,
                               help_text=_('PG who has max prfesence of sessions'))


    average_sessions = models.FloatField(_('average'),
                                   blank=True, null=True,
                                   help_text=_('Average of PG attended sessions'))

    maximum_sessions = models.FloatField(_('max'),
                                   blank=True, null=True,
                                   help_text=_('Max of PG attended sessions'))

    organization_value_votes = models.FloatField(_('Presence of this PG'),
                                   blank=True, null=True,
                                   help_text=_('Presence of this PG'))


    maxPG_votes = JSONField(blank=True, null=True,
                            help_text=_('PG who has max prfesence of sessions'))


    average_votes = models.FloatField(_('average'),
                                   blank=True, null=True,
                                   help_text=_('Average of PG attended sessions'))

    maximum_votes = models.FloatField(_('max'),
                                   blank=True, null=True,
                                   help_text=_('Max of PG attended sessions'))


class MPOfPg(Timestampable, models.Model):

    organization = models.ForeignKey('Organization',
                           blank=True, null=True,
                           related_name='MPOfPg_',
                           help_text=_('PG'))

    id_parladata = models.IntegerField(_('parladata id'),
                            blank=True, null=True,help_text=_('id parladata'))

    MPs = JSONField(blank=True, null=True)

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))


class MostMatchingThem(Timestampable, models.Model):

    organization = models.ForeignKey('Organization',
                           blank=True, null=True,
                           related_name='childrenMMT',
                           help_text=_('PG'))

    created_for = models.DateField(_('date of analize'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    person1 = models.ForeignKey('parlaposlanci.Person',
                                blank=True, null=True,
                                related_name='childrenMMT1',
                                help_text=_('MP1'))

    votes1 = models.FloatField(_('MatchingThem1'),
                               blank=True, null=True,
                               help_text=_('MatchingThem'))

    person2 = models.ForeignKey('parlaposlanci.Person',
                                blank=True, null=True,
                                related_name='childrenMMT2',
                                help_text=_('MP2'))

    votes2 = models.FloatField(_('MatchingThem2'),
                               blank=True, null=True,
                               help_text=_('MatchingThem'))

    person3 = models.ForeignKey('parlaposlanci.Person',
                                blank=True, null=True,
                                related_name='childrenMMT3',
                                help_text=_('MP3'))

    votes3 = models.FloatField(_('MatchingThem3'),
                               blank=True, null=True,
                               help_text=_('MatchingThem'))

    person4 = models.ForeignKey('parlaposlanci.Person',
                                blank=True, null=True,
                                related_name='childrenMMT4',
                                help_text=_('MP4'))

    votes4 = models.FloatField(_('MatchingThem4'),
                               blank=True, null=True,
                               help_text=_('MatchingThem'))

    person5 = models.ForeignKey('parlaposlanci.Person',
                                blank=True, null=True,
                                related_name='childrenMMT5',
                                help_text=_('MP5'))

    votes5 = models.FloatField(_('MatchingThem5'),
                               blank=True, null=True,
                               help_text=_('MatchingThem'))


class LessMatchingThem(Timestampable, models.Model):

    organization = models.ForeignKey('Organization',
                                     blank=True, null=True,
                                     related_name='childrenLMT',
                                     help_text=_('PG'))

    created_for = models.DateField(_('date of analize'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of activity'))

    person1 = models.ForeignKey('parlaposlanci.Person',
                                blank=True, null=True,
                                related_name='childrenLMT1',
                                help_text=_('MP1'))

    votes1 = models.FloatField(_('MatchingThem1'),
                               blank=True, null=True,
                               help_text=_('MatchingThem'))

    person2 = models.ForeignKey('parlaposlanci.Person',
                                blank=True, null=True,
                                related_name='childrenLMT2',
                                help_text=_('MP2'))

    votes2 = models.FloatField(_('MatchingThem2'),
                               blank=True, null=True,
                               help_text=_('MatchingThem'))

    person3 = models.ForeignKey('parlaposlanci.Person',
                                blank=True, null=True,
                                related_name='childrenLMT3',
                                help_text=_('MP3'))

    votes3 = models.FloatField(_('MatchingThem3'),
                               blank=True, null=True,
                               help_text=_('MatchingThem'))

    person4 = models.ForeignKey('parlaposlanci.Person',
                                blank=True, null=True,
                                related_name='childrenLMT4',
                                help_text=_('MP4'))

    votes4 = models.FloatField(_('MatchingThem4'),
                               blank=True, null=True,
                               help_text=_('MatchingThem'))

    person5 = models.ForeignKey('parlaposlanci.Person',
                                blank=True, null=True,
                                related_name='childrenLMT5',
                                help_text=_('MP5'))

    votes5 = models.FloatField(_('MatchingThem5'),
                               blank=True, null=True,
                               help_text=_('MatchingThem'))


class DeviationInOrganization(Timestampable, models.Model):

    organization = models.ForeignKey('Organization',
                                     blank=True, null=True,
                                     related_name='childrenD',
                                     help_text=_('PG'))

    data = JSONField(blank=True, null=True)

    created_for = models.DateField(_('date of analize'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of activity'))


class CutVotes(Timestampable, models.Model):
    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))
    organization = models.ForeignKey("Organization")
    this_for = models.FloatField(default=0.0)
    this_against = models.FloatField(default=0.0)
    this_abstain = models.FloatField(default=0.0)
    this_absent = models.FloatField(default=0.0)
    coalition_for = models.FloatField(default=0.0)
    coalition_against = models.FloatField(default=0.0)
    coalition_abstain = models.FloatField(default=0.0)
    coalition_absent = models.FloatField(default=0.0)
    coalition_for_max = models.FloatField(default=0.0)
    coalition_against_max = models.FloatField(default=0.0)
    coalition_abstain_max = models.FloatField(default=0.0)
    coalition_absent_max = models.FloatField(default=0.0)
    coalition_for_max_org = models.CharField(max_length=500)
    coalition_against_max_org = models.CharField(max_length=500)
    coalition_abstain_max_org = models.CharField(max_length=500)
    coalition_absent_max_org = models.CharField(max_length=500)
    opposition_for = models.FloatField(default=0.0)
    opposition_against = models.FloatField(default=0.0)
    opposition_abstain = models.FloatField(default=0.0)
    opposition_absent = models.FloatField(default=0.0)
    opposition_for_max =models.FloatField(default=0.0)
    opposition_against_max = models.FloatField(default=0.0)
    opposition_abstain_max = models.FloatField(default=0.0)
    opposition_absent_max = models.FloatField(default=0.0)
    opposition_for_max_org = models.CharField(max_length=500)
    opposition_against_max_org = models.CharField(max_length=500)
    opposition_abstain_max_org = models.CharField(max_length=500)
    opposition_absent_max_org = models.CharField(max_length=500)


class WorkingBodies(Timestampable, models.Model):
    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    organization = models.ForeignKey("Organization")

    president = models.ForeignKey('parlaposlanci.Person',
                                  blank=True, null=True,
                                  help_text=_('President'))

    vice_president = JSONField()

    members = JSONField()

    viceMember = JSONField()

    coal_ratio = models.FloatField()

    oppo_ratio = models.FloatField()

    seats = JSONField()

    sessions = JSONField()


class VocabularySize(Timestampable, models.Model): #Card for Vacabularty size of Org
    organization = models.ForeignKey('Organization',
                                     blank=True, null=True,
                                     related_name='vocabularySizes',
                                     help_text=_('Org'))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    score = models.FloatField(_('Vacabularty size of this Org'),
                                   blank=True, null=True,
                                   help_text=_('Vacabularty size of this Org'))

    maxOrg = models.ForeignKey('Organization',
                               blank=True, null=True,
                               related_name='childrenVacSiz',
                               help_text=_('Organization which has max vacabularty size'))

    average = models.FloatField(_('average'),
                                   blank=True, null=True,
                                   help_text=_('Vacabularty size of Org'))

    maximum = models.FloatField(_('max'),
                                   blank=True, null=True,
                                   help_text=_('Max of Org vacabularty size '))


class StyleScores(Timestampable, models.Model): #Card for Style Scores of MP
    organization = models.ForeignKey('Organization',
                                     blank=True, null=True,
                                     related_name='styleScores',
                                     help_text=_('Org'))
    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))
    problematicno = models.FloatField(_('Problematicno style score of this PG'),
                                   blank=True, null=True,
                                   help_text=_('Problematicno score of this PG'))
    privzdignjeno = models.FloatField(_('Privzdignjeno style score of this PG'),
                                   blank=True, null=True,
                                   help_text=_('Privzdignjeno style score of this PG'))
    preprosto = models.FloatField(_('Preprosto style score of this PG'),
                                   blank=True, null=True,
                                   help_text=_('Preprosto style score of this PG'))
    problematicno_average = models.FloatField(_('Problematicno average style score'),
                                   blank=True, null=True,
                                   help_text=_('Problematicno average style score'))
    privzdignjeno_average = models.FloatField(_('Privzdignjeno average style score'),
                                   blank=True, null=True,
                                   help_text=_('Privzdignjeno average style score'))
    preprosto_average = models.FloatField(_('Preprosto average style score'),
                                   blank=True, null=True,
                                   help_text=_('Preprosto average style score'))


class Tfidf(Timestampable, models.Model):
    organization = models.ForeignKey('Organization',
                                     blank=True, null=True,
                                     related_name='tfidf',
                                     help_text=_('Org'))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    is_visible = models.BooleanField(_('is visible'),
                                     default=True)

    data = JSONField(blank=True, null=True)

    def __str__(self):
        return unicode(self.organization.name) + " --> " + unicode(self.created_for)


class NumberOfQuestions(Timestampable, models.Model):
    organization = models.ForeignKey('Organization',
                                     blank=True, null=True,
                                     related_name='numOfQuestions',
                                     help_text=_('Org'))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    score = models.FloatField(blank=True,
                              null=True,
                              help_text=_('MP score'))

    average = models.FloatField(blank=True,
                                null=True,
                                help_text=_('Average score'))

    maximum = models.FloatField(blank=True,
                                null=True,
                                help_text=_('Maximum score'))

    maxOrgs = JSONField(blank=True, null=True)


class PresenceThroughTime(Timestampable, models.Model):
    organization = models.ForeignKey('Organization',
                                     blank=True, null=True,
                                     related_name='presenceThroughTime',
                                     help_text=_('Org'))
    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))
    data = JSONField(blank=True, null=True)


class IntraDisunion(Timestampable, models.Model):
    organization = models.ForeignKey('Organization',
                                     blank=True, null=True,
                                     related_name='intraDisunion',
                                     help_text=_('Org'))

    vote = models.ForeignKey('parlaseje.Vote',
                             blank=True, null=True,
                             related_name='VoteintraDisunion',
                             help_text=_('Vote'))

    maximum = models.CharField(_('Maximum'),
                               blank = True,
                               null = True,
                               max_length = 128,
                               help_text=_('Maximum of organization disunion.'))