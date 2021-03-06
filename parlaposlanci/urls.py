from django.conf.urls import patterns, include, url
from parlaposlanci.views import *

urlpatterns = patterns(
    '', # TODO this is fucking crazy

    # setters
    url(r'^setMPStatic/(?P<person_id>\d+)/(?P<date_>[\w].+)', setMPStaticPL),
    url(r'^setMPStatic/(?P<person_id>\d+)/', setMPStaticPL),

    url(r'^setMinsterStatic/(?P<person_id>\d+)/(?P<date_>[\w].+)', setMinsterStatic),
    url(r'^setMinsterStatic/(?P<person_id>\d+)/', setMinsterStatic),

    url(r'^setPresence/(?P<person_id>\d+)/(?P<date_>[\w].+)', setPercentOFAttendedSession),
    url(r'^setPresence/(?P<person_id>\d+)', setPercentOFAttendedSession),

    url(r'^setAverageNumberOfSpeechesPerSession/(?P<person_id>\d+)', setAverageNumberOfSpeechesPerSession),

    url(r'^setAverageNumberOfSpeechesPerSessionALL/(?P<date_>[\w].+)', setAverageNumberOfSpeechesPerSessionAll),
    url(r'^setAverageNumberOfSpeechesPerSessionALL/', setAverageNumberOfSpeechesPerSessionAll),

    url(r'^setVocabularySize/(?P<person_id>\d+)', setVocabularySize),

    url(r'^setLastActivity/(?P<person_id>\d+)', setLastActivity),

    url(r'^setCompass/(?P<date_>[\w].+)', setCompass),
    url(r'^setCompass', setCompass),

    url(r'^setMembershipsOfMember/(?P<person_id>\d+)/(?P<date>[\w].+)', setMembershipsOfMember),
    url(r'^setMembershipsOfMember/(?P<person_id>\d+)', setMembershipsOfMember),

    url(r'^setVocabularySizeAndSpokenWords/(?P<date_>[\w].+)', setVocabularySizeAndSpokenWords),
    url(r'^setVocabularySizeAndSpokenWords/', setVocabularySizeAndSpokenWords),

    url(r'^setNumberOfQuestionsAll/(?P<date_>[\w].+)', setNumberOfQuestionsAll),
    url(r'^setNumberOfQuestionsAll/', setNumberOfQuestionsAll),

    ####################################################################################

    # getters
    url(r'^getMPStatic/(?P<person_id>\d+)/(?P<date_>[\w].+)', getMPStaticPL),
    url(r'^getMPStatic/(?P<person_id>\d+)/', getMPStaticPL),

    url(r'^getMostEqualVoters/(?P<person_id>\d+)/(?P<date_>[\w].+)', getMostEqualVoters),
    url(r'^getMostEqualVoters/(?P<person_id>\d+)/', getMostEqualVoters),

    url(r'^getLeastEqualVoters/(?P<person_id>\d+)/(?P<date_>[\w].+)', getLessEqualVoters),
    url(r'^getLeastEqualVoters/(?P<person_id>\d+)/', getLessEqualVoters),

    url(r'^getTFIDF/(?P<person_id>\d+)/(?P<date_>[\w].+)', getTFIDF),
    url(r'^getTFIDF/(?P<person_id>\d+)', getTFIDF),

    url(r'^getPresence/(?P<person_id>\d+)/(?P<date>[\w].+)', getPercentOFAttendedSession),
    url(r'^getPresence/(?P<person_id>\d+)', getPercentOFAttendedSession),

    url(r'^getStyleScores/(?P<person_id>\d+)/(?P<date_>[\w].+)', getStyleScores),
    url(r'^getStyleScores/(?P<person_id>\d+)', getStyleScores),

    url(r'^getAverageNumberOfSpeechesPerSession/(?P<person_id>\d+)/(?P<date>[\w].+)', getAverageNumberOfSpeechesPerSession),
    url(r'^getAverageNumberOfSpeechesPerSession/(?P<person_id>\d+)', getAverageNumberOfSpeechesPerSession),

    url(r'^getNumberOfSpokenWords/(?P<person_id>\d+)/(?P<date>[\w].+)', getNumberOfSpokenWords),
    url(r'^getNumberOfSpokenWords/(?P<person_id>\d+)', getNumberOfSpokenWords),

    url(r'^getLastActivity/(?P<person_id>\d+)/(?P<date_>[\w].+)', getLastActivity),
    url(r'^getLastActivity/(?P<person_id>\d+)', getLastActivity),

    url(r'^getVocabularySize/(?P<person_id>\d+)/(?P<date_>[\w].+)', getVocabularySize),
    url(r'^getVocabularySize/(?P<person_id>\d+)', getVocabularySize),
    url(r'^getVocabularySizeLanding/(?P<date_>[\w].+)', getVocabolarySizeLanding),
    url(r'^getVocabularySizeLanding', getVocabolarySizeLanding),
    url(r'^getUniqueWordsLanding/(?P<date_>[\w].+)', getVocabolarySizeUniqueWordsLanding),
    url(r'^getUniqueWordsLanding/', getVocabolarySizeUniqueWordsLanding),

    url(r'^getAllSpeeches/(?P<person_id>\d+)/(?P<date_>[\w].+)', getAllSpeeches),
    url(r'^getAllSpeeches/(?P<person_id>\d+)', getAllSpeeches),

    url(r'^getQuestions/(?P<person_id>\d+)/(?P<date_>[\w].+)', getQuestions),
    url(r'^getQuestions/(?P<person_id>\d+)', getQuestions),

    url(r'^setPresenceThroughTime/(?P<person_id>\d+)/(?P<date_>[\w].+)', setPresenceThroughTime),
    url(r'^setPresenceThroughTime/(?P<person_id>\d+)', setPresenceThroughTime),

    url(r'^getPresenceThroughTime/(?P<person_id>\d+)/(?P<date_>[\w].+)', getPresenceThroughTime),
    url(r'^getPresenceThroughTime/(?P<person_id>\d+)', getPresenceThroughTime),

    url(r'^getListOfMembersTickers/(?P<date_>[\w].+)', getListOfMembersTickers),
    url(r'^getListOfMembersTickers/', getListOfMembersTickers),

    url(r'^getMPsIDs', getMPsIDs),

    url(r'^getCompass/(?P<date_>[\w].+)', getCompass),
    url(r'^getCompass', getCompass),

    url(r'^getTaggedBallots/(?P<person_id>\d+)/(?P<date_>[\w].+)', getTaggedBallots),
    url(r'^getTaggedBallots/(?P<person_id>\d+)', getTaggedBallots),

    url(r'^getMembershipsOfMember/(?P<person_id>\d+)/(?P<date>[\w].+)', getMembershipsOfMember),
    url(r'^getMembershipsOfMember/(?P<person_id>\d+)', getMembershipsOfMember),

    url(r'^getNumberOfQuestions/(?P<person_id>\d+)/(?P<date_>[\w].+)', getNumberOfQuestions),
    url(r'^getNumberOfQuestions/(?P<person_id>\d+)/', getNumberOfQuestions),

    url(r'^getListOfMembers/(?P<date_>[\w].+)', getListOfMembers),
    url(r'^getListOfMembers/', getListOfMembers),

    url(r'^getAllActiveMembers/', getAllActiveMembers),

    url(r'^getSlugs/', getSlugs),

    ###########################################################################
    # POST setters
    url(r'^setAllMPsTFIDFsFromSearch/', setAllMPsTFIDFsFromSearch),
    url(r'^setAllMPsStyleScoresFromSearch/', setAllMPsStyleScoresFromSearch),

    ###########################################################################

    #runer
    #url(r'^runSetters/(?P<date_to>[\w].+)', runSetters),
)
