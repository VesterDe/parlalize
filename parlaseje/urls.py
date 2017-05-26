from django.conf.urls import patterns, include, url
from parlaseje.views import *


urlpatterns = patterns(
    #wtf fix (first url was ignored)
    (),
    url(r'^getSpeech/(?P<speech_id>\d+)', getSpeech),
    url(r'^getSpeechesOfSession/(?P<session_id>\d+)', getSpeechesOfSession),
    url(r'^getSpeechesIDsOfSession/(?P<session_id>\d+)', getSpeechesIDsOfSession),
    #url(r'^setAllSessions/', setAllSessions),

    
    url(r'^setMotionOfSession/(?P<id_se>\d+)', setMotionOfSession),
    url(r'^setMotionOfSession/(?P<id_se>\d+)/(?P<date_>[\w].+)', setMotionOfSession),
    url(r'^getMotionOfSessionVotes/(?P<votes>[\w,]+)$', getMotionOfSessionVotes),

    url(r'^setMotionOfSessionGraph/(?P<id_se>\d+)/(?P<date_>[\w].+)', setMotionOfSessionGraph),
    url(r'^setMotionOfSessionGraph/(?P<id_se>\d+)', setMotionOfSessionGraph),

    url(r'^getMotionAnalize/(?P<motion_id>\d+)', getMotionAnalize),
    
    url(r'^getMotionOfSession/(?P<id_se>\d+)', getMotionOfSession),
    url(r'^getMotionOfSession/(?P<id_se>\d+)/(?P<date>[\w].+)', getMotionOfSession),
    
    url(r'^getMotionGraph/(?P<id_mo>\d+)', getMotionGraph),
    url(r'^getMotionGraph/(?P<id_mo>\d+)/(?P<date>[\w].+)', getMotionGraph),

    url(r'^setAbsentMPs/(?P<id_se>\d+)', setAbsentMPs),
    
    url(r'^getAbsentMPs/(?P<id_se>\d+)', getAbsentMPs),
    url(r'^getAbsentMPs/(?P<id_se>\d+)/(?P<date>[\w].+)', getAbsentMPs),

    url(r'^setPresenceOfPG/(?P<id_se>\d+)/(?P<date_>[\w].+)', setPresenceOfPG),
    url(r'^setPresenceOfPG/(?P<id_se>\d+)', setPresenceOfPG),
    
    url(r'^getPresenceOfPG/(?P<id_se>\d+)', getPresenceOfPG),
    url(r'^getPresenceOfPG/(?P<id_se>\d+)/(?P<date>[\w].+)', getPresenceOfPG),

    url(r'^setSpeechesOnSession/(?P<date>[\w].+)', setSpeechesOnSession),
    url(r'^getMaxSpeechesOnSession/(?P<date>[\w].+)', getMaxSpeechesOnSession),
    url(r'^getMinSpeechesOnSession/(?P<date>[\w].+)', getMinSpeechesOnSession),

    url(r'^getMinSpeechesOnSession/', getMinSpeechesOnSession),
    url(r'^getMaxSpeechesOnSession/', getMaxSpeechesOnSession),

    url(r'^setQuote/(?P<speech_id>\d+)/(?P<start_pos>\d+)/(?P<end_pos>\d+)', setQuote),
    url(r'^getQuote/(?P<quote_id>\d+)', getQuote),

    url(r'^setTFIDF/(?P<session_id>\d+)', setTFIDF),
    url(r'^getTFIDF/(?P<session_id>\d+)', getTFIDF),

    url(r'^getLastSessionLanding(/(?P<date_>[\w].+))?', getLastSessionLanding),

    url(r'^getSessionsByClassification/', getSessionsByClassification),

    url(r'^getSessionsList/', getSessionsList),

    url(r'^getWorkingBodies/', getWorkingBodies),

    url(r'^getComparedVotes/', getComparedVotes),
)
