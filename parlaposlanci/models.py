# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from parlaposlanci.models import *
from parlaseje.models import *

from behaviors.models import Timestampable

from jsonfield import JSONField

# Create your models here.

# converting datetime to popolo
class PopoloDateTimeField(models.DateTimeField):

    def get_popolo_value(self, value):
        return str(datetime.strftime(value, '%Y-%m-%d'))

@python_2_unicode_compatible
class Person(Timestampable, models.Model): # poslanec, minister, predsednik dz etc.


    name = models.CharField(_('name'),
                            blank=True, null=True,
                            max_length=128,
                            help_text=_('A person\'s preferred full name'))

    pg = models.CharField(_('parlament group'),
                            null=True, max_length=128,
                            help_text=_('Parlament group of MP'))

    id_parladata = models.IntegerField(_('parladata id'),
                            blank=True, null=True,help_text=_('id parladata'))

    image = models.URLField(_('image'),
                            blank=True, null=True,
                            help_text=_('A URL of a head shot'))

    actived = models.CharField(_('actived'),
                            null=True,
                            max_length=128,
                            help_text=_('Yes if MP is actived or no if it is not'))

    gov_id = models.CharField(_('gov id'),
                            null=True,
                            max_length=128,
                            help_text=_('The ID of the official on the government website.')
                            )

    has_function = models.BooleanField(default=False,
                                       help_text=_('True if is president or something special.'))



    def __str__(self):
        return self.name

class Presence(Timestampable, models.Model): #Card for presence of MP on sessions

    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='children',
                               help_text=_('MP'))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    person_value_sessions = models.FloatField(_('Presence of this MP'),
                                                blank=True, null=True,
                                                help_text=_('Presence of this MP'))


    maxMP_sessions = JSONField(blank=True, null=True,
                                      help_text=_('Person who has max presence of sessions'))


    average_sessions = models.FloatField(_('average'),
                                           blank=True, null=True,
                                           help_text=_('Average of MP attended sessions'))

    maximum_sessions = models.FloatField(_('max'),
                                           blank=True, null=True,
                                           help_text=_('Max of MP attended sessions'))


    person_value_votes = models.FloatField(_('Presence of this MP'),
                                             blank=True, null=True,
                                             help_text=_('Presence of this MP'))


    maxMP_votes = JSONField(blank=True, null=True,
                                   help_text=_('Person who has max presence of sessions'))


    average_votes = models.FloatField(_('average'),
                                        blank=True, null=True,
                                        help_text=_('Average of MP attended sessions'))

    maximum_votes = models.FloatField(_('max'),
                                        blank=True, null=True,
                                        help_text=_('Max of MP attended sessions'))



class SpokenWords(Timestampable, models.Model): #Card for spoken words of MP on sessions

    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenSW',
                               help_text=_('MP'))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    score = models.IntegerField(_('SW of this MP'),
                                   blank=True, null=True,
                                   help_text=_('SW of this MP'))

    maxMP = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenSW_',
                               help_text=_('Person who has max spoken words'))

    average = models.IntegerField(_('average'),
                                   blank=True, null=True,
                                   help_text=_('Average of MP attended sessions'))

    maximum = models.IntegerField(_('max'),
                                   blank=True, null=True,
                                   help_text=_('Max of MP attended sessions'))

class SpeakingStyle(Timestampable, models.Model): #card for privzdignjeno besedje
    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               help_text=_('MP'))

    problematicno_score = models.IntegerField(help_text=_('Problematicno besedje score.'))
    privzdignjeno_score = models.IntegerField(help_text=_('Privzdignjeno besedje score.'))
    preprosto_score = models.IntegerField(help_text=_('Preprosto besedje score.'))

    problematicno_avg = models.IntegerField(help_text=_('Problematicno besedje average score.'))
    privzdignjeno_avg = models.IntegerField(help_text=_('Privzdignjeno besedje average score.'))
    preprosto_avg = models.IntegerField(help_text=_('Preprosto besedje average score.'))

class CutVotes(Timestampable, models.Model):
    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))
    person = models.ForeignKey("Person")
    this_for = models.FloatField()
    this_against = models.FloatField()
    this_abstain = models.FloatField()
    this_absent = models.FloatField()
    coalition_for = models.FloatField()
    coalition_against = models.FloatField()
    coalition_abstain = models.FloatField()
    coalition_absent = models.FloatField()
    coalition_for_max = models.FloatField()
    coalition_against_max = models.FloatField()
    coalition_abstain_max = models.FloatField()
    coalition_absent_max = models.FloatField()
    coalition_for_max_person = models.CharField(max_length = 500)
    coalition_against_max_person = models.CharField(max_length = 500)
    coalition_abstain_max_person = models.CharField(max_length = 500)
    coalition_absent_max_person = models.CharField(max_length = 500)
    opposition_for = models.FloatField()
    opposition_against = models.FloatField()
    opposition_abstain = models.FloatField()
    opposition_absent = models.FloatField()
    opposition_for_max =models.FloatField()
    opposition_against_max = models.FloatField()
    opposition_abstain_max = models.FloatField()
    opposition_absent_max = models.FloatField()
    opposition_for_max_person = models.CharField(max_length = 500)
    opposition_against_max_person = models.CharField(max_length = 500)
    opposition_abstain_max_person = models.CharField(max_length = 500)
    opposition_absent_max_person = models.CharField(max_length = 500)


class LastActivity(Timestampable, models.Model): #TODO

    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenLA',
                               help_text=_('MP'))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    """session_id = models.ForeignKey('Session',
                               blank=True, null=True,
                               related_name='session',
                               help_text=_('Session of activity'))"""


    session_id = models.TextField(_('type of activity'),
                                 blank=True, null=True,
                                 help_text=_('type of activity'))

    vote_name = models.TextField(_('type of activity'),
                                 blank=True, null=True,
                                 help_text=_('type of activity'))

    typee = models.TextField(_('type of activity'),
                                 blank=True, null=True,
                                 help_text=_('type of activity'))

    activity_id = models.TextField(_('type of activity'),
                                 blank=True, null=True,
                                 help_text=_('type of activity'))

    option = models.TextField(_('type of activity'),
                                 blank=True, null=True,
                                 help_text=_('type of activity'))

    result = models.TextField(_('type of activity'),
                                 blank=True, null=True,
                                 help_text=_('type of activity'))


class EqualVoters(Timestampable, models.Model):

    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenEWT',
                               help_text=_('MP'))

    created_for = models.DateField(_('date of actanalizeivity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of activity'))

    person1 = models.ForeignKey('Person',
                                blank=True, null=True,
                                related_name='childrenEW1',
                                help_text=_('MP1'))

    votes1 = models.FloatField(_('EqualVoters1'),
                               blank=True, null=True,
                               help_text=_('EqualVoters'))

    person2 = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenEW2',
                               help_text=_('MP2'))

    votes2 = models.FloatField(_('EqualVoters2'),
                                 blank=True, null=True,
                                 help_text=_('EqualVoters'))

    person3 = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenEW3',
                               help_text=_('MP3'))

    votes3 = models.FloatField(_('EqualVoters3'),
                                 blank=True, null=True,
                                 help_text=_('EqualVoters'))

    person4 = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenEW4',
                               help_text=_('MP4'))

    votes4 = models.FloatField(_('EqualVoters4'),
                                 blank=True, null=True,
                                 help_text=_('EqualVoters'))

    person5 = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenEW5',
                               help_text=_('MP5'))

    votes5 = models.FloatField(_('EqualVoters5'),
                                 blank=True, null=True,
                                 help_text=_('EqualVoters'))

class LessEqualVoters(Timestampable, models.Model):

    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenLEWT',
                               help_text=_('MP'))

    created_for = models.DateField(_('date of analize'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of activity'))

    person1 = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenLEW1',
                               help_text=_('MP1'))

    votes1 = models.FloatField(_('EqualVoters1'),
                                 blank=True, null=True,
                                 help_text=_('EqualVoters'))

    person2 = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenLEW2',
                               help_text=_('MP2'))

    votes2 = models.FloatField(_('EqualVoters2'),
                                 blank=True, null=True,
                                 help_text=_('EqualVoters'))

    person3 = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenLEW3',
                               help_text=_('MP3'))

    votes3 = models.FloatField(_('EqualVoters3'),
                                 blank=True, null=True,
                                 help_text=_('EqualVoters'))

    person4 = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenLEW4',
                               help_text=_('MP4'))

    votes4 = models.FloatField(_('EqualVoters4'),
                                 blank=True, null=True,
                                 help_text=_('EqualVoters'))

    person5 = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenLEW5',
                               help_text=_('MP5'))

    votes5 = models.FloatField(_('EqualVoters5'),
                                 blank=True, null=True,
                                 help_text=_('EqualVoters'))

class MPsWhichFitsToPG(Timestampable, models.Model):

    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenMPWPG',
                               help_text=_('MP1'))

class MPStaticPL(Timestampable, models.Model):
    person = models.ForeignKey('Person', help_text=_('Person foreign key relationship'))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    voters = models.IntegerField(blank=True, null=True, help_text=_('Number of voters'))

    age = models.IntegerField(blank=True, null=True, help_text=_('Person\'s age.'))

    mandates = models.IntegerField(blank=True, null=True, help_text=_('Number of mandates'))

    party_id = models.IntegerField(blank=True, null=True, help_text=_('Parladata party id'))

    acronym = models.TextField(blank=True, null=True, help_text=_('Parliament group\'s acronym'))

    education = models.TextField(blank=True, null=True, help_text=_('Person\'s education'))

    previous_occupation = models.TextField(blank=True, null=True, help_text=_('Person\'s previous occupation'))

    name = models.TextField(blank=True, null=True, help_text=_('Name'))

    district = JSONField(blank=True, null=True, help_text=_('Voting district name.'))

    facebook = models.TextField(blank=True, null=True, default=None, help_text=_('Facebook profile URL'))
    twitter = models.TextField(blank=True, null=True, default=None, help_text=_('Twitter profile URL'))
    linkedin = models.TextField(blank=True, null=True, default=None, help_text=_('Linkedin profile URL'))

    party_name = models.TextField(blank=True, null=True, help_text=_('Party name'))

    gov_id = models.CharField(_('gov id'),
                            null=True,
                            max_length=128,
                            help_text=_('The ID of the official on the government website.')
                            )

    gender = models.CharField(max_length=1, 
                              default="f",
                              help_text=_('Gender'))

    working_bodies_functions = JSONField(blank=True, null=True)

class MPStaticGroup(Timestampable, models.Model):

    person = models.ForeignKey('MPStaticPL', help_text=_('Person foreign key to MPStaticPL'))

    groupid = models.IntegerField()
    groupname = models.TextField()


class NumberOfSpeechesPerSession(Timestampable, models.Model): #Card for Average number Of Speeches Per Session

    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='speaker',
                               help_text=_('MP'))

    created_for = models.DateField(_('date of activity'),
                               blank=True,
                               null=True,
                               help_text=_('date of analize'))

    person_value = models.FloatField(_('Number of speeches of this MP'),
                                   blank=True, null=True,
                                   help_text=_('Number of speeches of this MP'))

    maxMP = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenNOSPS',
                               help_text=_('Person who has max speeches per session'))

    average = models.FloatField(_('average'),
                                   blank=True, null=True,
                                   help_text=_('Average of MP speeches per session'))

    maximum = models.FloatField(_('max'),
                                   blank=True, null=True,
                                   help_text=_('Max of MP speeches per session'))

class VocabularySize(Timestampable, models.Model): #Card for Vacabularty size of MP
    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='VocabularySizes',
                               help_text=_('MP'))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    score = models.FloatField(_('Vacabularty size of this MP'),
                                   blank=True, null=True,
                                   help_text=_('Vacabularty size of this MP'))

    maxMP = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='maxVocabulary',
                               help_text=_('Person who has max vacabularty size'))

    average = models.FloatField(_('average'),
                                   blank=True, null=True,
                                   help_text=_('Vacabularty size of MP'))

    maximum = models.FloatField(_('max'),
                                   blank=True, null=True,
                                   help_text=_('Max of MP vacabularty size '))


class VocabularySizeUniqueWords(Timestampable, models.Model): #Card for Vacabularty size of MP
    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='uniqueWords',
                               help_text=_('MP'))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    score = models.FloatField(_('Vacabularty size of this MP'),
                                   blank=True, null=True,
                                   help_text=_('Vacabularty size of this MP'))

    maxMP = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='maxUniqueWords',
                               help_text=_('Person who has max vacabularty size'))

    average = models.FloatField(_('average'),
                                   blank=True, null=True,
                                   help_text=_('Vacabularty size of MP'))

    maximum = models.FloatField(_('max'),
                                   blank=True, null=True,
                                   help_text=_('Max of MP vacabularty size '))



class StyleScores(Timestampable, models.Model): #Card for Style Scores of MP
    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               related_name='childrenStSc',
                               help_text=_('MP'))
    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))
    problematicno = models.FloatField(_('Problematicno style score of this MP'),
                                   blank=True, null=True,
                                   help_text=_('Problematicno score of this MP'))
    privzdignjeno = models.FloatField(_('Privzdignjeno style score of this MP'),
                                   blank=True, null=True,
                                   help_text=_('Privzdignjeno style score of this MP'))
    preprosto = models.FloatField(_('Preprosto style score of this MP'),
                                   blank=True, null=True,
                                   help_text=_('Preprosto style score of this MP'))
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
    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               help_text=_('MP'))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    is_visible = models.BooleanField(_('is visible'),
                                     default=True)

    data = JSONField(blank=True, null=True)


    def __str__(self):
        return unicode(self.person.name) + " --> " + unicode(self.created_for)
#class StyleScores(Timestampable, models.Model):
#    person = models.ForeignKey('Person',
#                               blank=True, null=True,
#                               help_text=_('MP'))


class AverageNumberOfSpeechesPerSession(Timestampable, models.Model):

    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               help_text=_('MP'))

    created_for = models.DateField(_('date of analize'),
                               blank=True,
                               null=True,
                               help_text=_('date of activity'))

    score = models.FloatField(blank=True, null=True, help_text=_('MP score'))

    average = models.FloatField(blank=True, null=True, help_text=_('Average score'))

    maximum = models.FloatField(blank=True, null=True, help_text=_('Maximum score'))

    maxMP = models.ForeignKey('Person', blank=True, null=True, help_text=_('Maximum MP'), related_name='max_person')

class Compass(Timestampable, models.Model):

    calculated_from = models.DateField(
                                _('date of first ballot entered'),
                                blank=True,
                                null=True,
                                help_text=_('date of first ballot entered'))

    created_for = models.DateField(_('date of analize'),
                               blank=True,
                               null=True,
                               help_text=_('date of activity'))

    data = JSONField(blank=True, null=True)

class TaggedBallots(Timestampable, models.Model):

    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               help_text=_('MP'))

    data = JSONField(blank=True, null=True)

class MembershipsOfMember(Timestampable, models.Model):
    person = models.ForeignKey('Person',
                               blank=True, null=True,
                               help_text=_('MP'))

    created_for = models.DateField(_('date of activity'),
                                   blank=True,
                                   null=True,
                                   help_text=_('date of analize'))

    data = JSONField(blank=True, null=True)


class District(models.Model):
    id_parladata = models.IntegerField(_('parladata id'),
                                       blank=True,
                                       null=True,
                                       help_text=_('id parladata'))

    name =  models.CharField(_('name of district'),
                            null=True, max_length=128,
                            help_text=_('District name'))
