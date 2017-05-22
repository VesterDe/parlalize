from django.conf.urls import patterns, url
from parlaseje.views import *


urlpatterns = patterns(
    #fix (first url was ignored)
    (),

    #All setters
    url(r'^setMotionOfSession/(?P<session_id>\d+)', setMotionOfSession),
    url(r'^setMotionOfSession/(?P<session_id>\d+)/(?P<date_>[\w].+)', setMotionOfSession),

    url(r'^setPresenceOfPG/(?P<session_id>\d+)', setPresenceOfPG),
    url(r'^setPresenceOfPG/(?P<session_id>\d+)/(?P<date_>[\w].+)', setPresenceOfPG),

    url(r'^setTFIDF/(?P<session_id>\d+)', setTFIDF),

    url(r'^setMotionOfSessionGraph/(?P<session_id>\d+)', setMotionOfSessionGraph),
    url(r'^setMotionOfSessionGraph/(?P<session_id>\d+)/(?P<date_>[\w].+)', setMotionOfSessionGraph),

    url(r'^setQuote/(?P<speech_id>\d+)/(?P<start_pos>\d+)/(?P<end_pos>\d+)', setQuote),

    #All getters 
    url(r'^getSpeech/(?P<speech_id>\d+)', getSpeech),
    url(r'^getSpeechesOfSession/(?P<session_id>\d+)', getSpeechesOfSession),
    url(r'^getSpeechesIDsOfSession/(?P<session_id>\d+)', getSpeechesIDsOfSession),

    url(r'^getMotionAnalize/(?P<motion_id>\d+)', getMotionAnalize),

    url(r'^getPresenceOfPG/(?P<session_id>\d+)', getPresenceOfPG),
    url(r'^getPresenceOfPG/(?P<session_id>\d+)/(?P<date>[\w].+)', getPresenceOfPG),

    url(r'^getQuote/(?P<quote_id>\d+)', getQuote),

    url(r'^getTFIDF/(?P<session_id>\d+)', getTFIDF),

    url(r'^getLastSessionLanding(/(?P<date_>[\w].+))?', getLastSessionLanding),

    url(r'^getSessionsByClassification/', getSessionsByClassification),

    url(r'^getSessionsList/', getSessionsList),

    url(r'^getWorkingBodies/', getWorkingBodies),

    url(r'^getMotionOfSession/(?P<session_id>\d+)', getMotionOfSession),
    url(r'^getMotionOfSession/(?P<session_id>\d+)/(?P<date>[\w].+)', getMotionOfSession),

    url(r'^getMotionGraph/(?P<id_mo>\d+)', getMotionGraph),
    url(r'^getMotionGraph/(?P<id_mo>\d+)/(?P<date>[\w].+)', getMotionGraph),
)
