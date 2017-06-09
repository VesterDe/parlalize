from django.conf.urls import patterns, include, url
from parlaskupine.views import *


urlpatterns = patterns('',

#	url(r'^getMPsList/', getMPsList),
    # setters
    url(r'^setBasicInfOfPG/(?P<pg_id>\d+)/(?P<date_>[\w].+)', setBasicInfOfPG),
    url(r'^setBasicInfOfPG/(?P<pg_id>\d+)', setBasicInfOfPG),

    url(r'^setPercentOFAttendedSessionPG/(?P<pg_id>\d+)/(?P<date_>[\w].+)', setPercentOFAttendedSessionPG),
    url(r'^setPercentOFAttendedSessionPG/(?P<pg_id>\d+)', setPercentOFAttendedSessionPG),
    url(r'^setBasicInfOfPG/(?P<pg_id>\d+)', setBasicInfOfPG),
    url(r'^setPercentOFAttendedSessionPG/(?P<pg_id>\d+)', setPercentOFAttendedSessionPG),

    url(r'^setMPsOfPG/(?P<pg_id>\d+)/(?P<date_>[\w].+)', setMPsOfPG),
    url(r'^setMPsOfPG/(?P<pg_id>\d+)', setMPsOfPG),

    url(r'^setWorkingBodies/(?P<org_id>\d+)/(?P<date_>[\w].+)', setWorkingBodies),
    url(r'^setWorkingBodies/(?P<org_id>\d+)', setWorkingBodies),

    url(r'^setVocabularySizeALL/(?P<date_>[\w].+)', setVocabularySizeALL),
    url(r'^setVocabularySizeALL', setVocabularySizeALL),

    url(r'^setTFIDF/(?P<party_id>\d+)/(?P<date_>[\w].+)', setTFIDF),
    url(r'^setTFIDF/(?P<party_id>\d+)', setTFIDF),

    url(r'^setNumberOfQuestionsAll/(?P<date_>[\w].+)', setNumberOfQuestionsAll),
    url(r'^setNumberOfQuestionsAll/', setNumberOfQuestionsAll),

    url(r'^setPresenceThroughTime/(?P<party_id>\d+)/(?P<date_>[\w].+)', setPresenceThroughTime),
    url(r'^setPresenceThroughTime/(?P<party_id>\d+)', setPresenceThroughTime),

    # getters
    url(r'^getBasicInfOfPG/(?P<pg_id>\d+)', getBasicInfOfPG),

    url(r'^getPercentOFAttendedSessionPG/(?P<pg_id>\d+)/(?P<date_>[\w].+)', getPercentOFAttendedSessionPG),
    url(r'^getPercentOFAttendedSessionPG/(?P<pg_id>\d+)', getPercentOFAttendedSessionPG),

    url(r'^getSpeechesOfPG/(?P<pg_id>\d+)/(?P<date_>[\w].+)', getSpeechesOfPG),
    url(r'^getSpeechesOfPG/(?P<pg_id>\d+)', getSpeechesOfPG),
    
    url(r'^getBasicInfOfPG/(?P<pg_id>\d+)', getBasicInfOfPG),
    url(r'^getPercentOFAttendedSessionPG/(?P<pg_id>\d+)', getPercentOFAttendedSessionPG),

    url(r'^getMPsOfPG/(?P<pg_id>\d+)/(?P<date_>[\w].+)', getMPsOfPG),
    url(r'^getMPsOfPG/(?P<pg_id>\d+)', getMPsOfPG),
    
    url(r'^getMostMatchingThem/(?P<pg_id>\d+)/(?P<date_>[\w].+)', getMostMatchingThem),
    url(r'^getMostMatchingThem/(?P<pg_id>\d+)/', getMostMatchingThem),

    url(r'^getLessMatchingThem/(?P<pg_id>\d+)/(?P<date_>[\w].+)', getLessMatchingThem),
    url(r'^getLessMatchingThem/(?P<pg_id>\d+)/', getLessMatchingThem),

    url(r'^getDeviationInOrg/(?P<pg_id>\d+)/(?P<date_>[\w].+)', getDeviationInOrg),
    url(r'^getDeviationInOrg/(?P<pg_id>\d+)/', getDeviationInOrg),

    url(r'^getTaggedBallots/(?P<pg_id>\d+)/(?P<date_>[\w].+)', getTaggedBallots),
    url(r'^getTaggedBallots/(?P<pg_id>\d+)', getTaggedBallots),

    url(r'^getVocabularySize/(?P<pg_id>\d+)/(?P<date_>[\w].+)', getVocabularySize),
    url(r'^getVocabularySize/(?P<pg_id>\d+)', getVocabularySize),

    url(r'^getWorkingBodies/(?P<org_id>\d+)/(?P<date_>[\w].+)', getWorkingBodies),
    url(r'^getWorkingBodies/(?P<org_id>\d+)', getWorkingBodies),

    url(r'^getStyleScores/(?P<pg_id>\d+)/(?P<date_>[\w].+)', getStyleScoresPG),
    url(r'^getStyleScores/(?P<pg_id>\d+)', getStyleScoresPG),

    url(r'^getTFIDF/(?P<party_id>\d+)/(?P<date_>[\w].+)', getTFIDF),
    url(r'^getTFIDF/(?P<party_id>\d+)', getTFIDF),

    url(r'^getNumberOfQuestions/(?P<pg_id>\d+)/(?P<date_>[\w].+)', getNumberOfQuestions),
    url(r'^getNumberOfQuestions/(?P<pg_id>\d+)/', getNumberOfQuestions),

    url(r'^getQuestionsOfPG/(?P<pg_id>\d+)/(?P<date_>[\w].+)', getQuestionsOfPG),
    url(r'^getQuestionsOfPG/(?P<pg_id>\d+)/', getQuestionsOfPG),

    url(r'^getPresenceThroughTime/(?P<party_id>\d+)/(?P<date_>[\w].+)', getPresenceThroughTime),
    url(r'^getPresenceThroughTime/(?P<party_id>\d+)', getPresenceThroughTime),

    url(r'^getIntraDisunionOrg/(?P<org_id>\d+)', getIntraDisunionOrg),
    url(r'^getIntraDisunion/', getIntraDisunion),

    url(r'^getPGsIDs', getPGsIDs),

    ####################################################################################
    #POST setters
    url(r'^setAllPGsStyleScoresFromSearch/', setAllPGsStyleScoresFromSearch),
    url(r'^setAllPGsTFIDFsFromSearch/', setAllPGsTFIDFsFromSearch),

    ####################################################################################

    # runenr
    #url(r'^runSetters/(?P<date_to>[\w].+)', runSetters),

    url(r'^getListOfPGs/(?P<date_>[\w].+)/', getListOfPGs),
    url(r'^getListOfPGs/', getListOfPGs),

    url(r'^getWorkingBodiesLive/(?P<org_id>\d+)/(?P<date_>[\w].+)', getWorkingBodies_live),
)
