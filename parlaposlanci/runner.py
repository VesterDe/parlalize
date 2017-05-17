import requests, json
import logging
from parlalize.settings import BASE_URL, API_URL
from parlalize.utils import update

from parlalize.utils import tryHard

logger = logging.getLogger(__name__)

setters = (
   BASE_URL+'/p/setMPStatic/',
#    BASE_URL+'/p/setMostEqualVoters/',
#     BASE_URL+'/p/setLeastEqualVoters/',
#    BASE_URL+'/p/setTFIDF/',
#    BASE_URL+'/p/setPresence/',
   BASE_URL+'/p/setAverageNumberOfSpeechesPerSession/',
#    BASE_URL+'/p/setVocabularySize/',
   BASE_URL+'/p/setLastActivity/',
    BASE_URL+'/p/setCutVotes/',
)

allsetters = (
#    BASE_URL + '/p/setAverageNumberOfWordsPerSessionALL',
    # BASE_URL + '/p/setVocabularySizeALL/',
)

# get all parliament member ID's
def getIDs():
    #create persons
    result = []

    data = tryHard(API_URL+'/getMPs/').json()

    for mp in data:
        result.append(mp['id'])

    return result


def runMPs():
    for setter in allsetters:
        print setter
        result = tryHard(setter)

        if result.status_code == 200:
           logger.info(setter + ' ALL OK')
        else:
           logger.error(setter + ' ERROR: ' + str(result.status_code))

    IDs = getIDs()
    print IDs

    for ID in IDs:
        for setter in setters:
            print setter + str(ID)
            result = tryHard(setter + str(ID))

            if result.status_code == 200:
               logger.info(setter + str(ID) + ' ALL OK')
            else:
               logger.error(setter + str(ID) + ' ERROR: ' + str(result.status_code))

#    result = tryHard(BASE_URL+'/p/setNumberOfSpokenWordsALL/',).status_code

    #if result == 200:
    #    logger.info(setter + str(ID) + ' ALL OK')
    #else:
    #    logger.error(setter + str(ID) + ' ERROR: ' + str(result))
