import json
import inspect
from config import CommonConfig, IngestionConfig, RequestHeaders

def loadApiJson(jsonFile):
   # print(f"Current function name: {inspect.currentframe().f_code.co_name}")
    with open(jsonFile, 'r') as file:

        fileData = json.load(file)
    return fileData


def loadApiJsonFile():
   # print(f"Current function name: {inspect.currentframe().f_code.co_name}")
    config = CommonConfig()
    filePath = config.API_JSON_FILE
    return loadApiJson(filePath)


def getRecentMatchUrl(allApis):
   # print(f"Current function name: {inspect.currentframe().f_code.co_name}")
    config = IngestionConfig()
    url = allApis[config.RECENT_MATCHES]
    return url

def getRecentMatchHeaders():
   # print(f"Current function name: {inspect.currentframe().f_code.co_name}")
    config = RequestHeaders()
    header, value = config.HEADER, config.VALUE
    headers = {
        config.ACCEPT[header]: config.ACCEPT[value],
        config.CONTENT_TYPE[header]: config.CONTENT_TYPE[value],
        config.X_RAPIDAPI_HOST[header]: config.X_RAPIDAPI_HOST[value],
        config.X_RAPIDAPI_KEY[header]: config.X_RAPIDAPI_KEY[value],
        config.X_RAPIDAPI_UA[header]: config.X_RAPIDAPI_UA[value]

    }

    return headers

def succesfulResponse(response):
    #print(f"Current function name: {inspect.currentframe().f_code.co_name}")
    config = CommonConfig()
    SUCCESS = config.SUCCESS_STATUS
    return response.status_code == SUCCESS



