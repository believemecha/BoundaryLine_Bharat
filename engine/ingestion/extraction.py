import requests
import sys
from utilities.ingestion_utilities import *

def generateApiResponse(url, headers):
    config = CommonConfig()
    SUCCESS, FAILURE = config.SUCCESS, config.FAILURE
    try:
        response = requests.get(url, headers=headers)
        if succesfulResponse(response):
            # Successful Api Response
            responseData = response.json()
            return responseData
        
        else:
            # Log failure
            statusCode = response.status_code
            sys.exit(response.status_code)

    except requests.exceptions.RequestException as e:
        # Log Exception
        print('Failure', e)
        sys.exit(FAILURE)



def fetchRecentMatches():
    allApis = loadApiJsonFile()
    url = getRecentMatchUrl(allApis)
    headers = getRecentMatchHeaders()
    apiResonse = generateApiResponse(url, headers)
    return apiResonse


def fetchMatchOverData(matchId):    
    allApis = loadApiJsonFile()
    url = getOverDataUrl(allApis, matchId)
    #print(url)
    headers = getOverDataHeader()
   # print(url, headers, 'Inside of fetchMatchOverData')
    apiResponse = generateApiResponse(url, headers)
    #print(apiResponse, 'Inside of fetchMatchOverData')
    return apiResponse



# data = fetchRecentMatches()
# print(data, 'This is the data')











