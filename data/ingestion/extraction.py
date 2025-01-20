import requests
import sys
# from validation.validation_match import *
# from validation.validation_player import *

from utilities.ingestion_utilities import *


def generateApiResponse(url, headers):
    config = CommonConfig()
    SUCCESS, FAILURE = config.SUCCESS, config.FAILURE
    try:
        response = requests.get(url, headers=headers)
        if succesfulResponse(response):
            # Successful Api Response
            responseData = response.json()
            print('This is response data', responseData)
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



data = fetchRecentMatches()
print(data, 'This is the data')











