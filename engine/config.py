import os

class CommonConfig:
    API_JSON_FILE = '/Users/ramit/Desktop/BoundryLine/BoundaryLine/engine/ingestion/Api.json'
    SAMPLE_FILE = '/Users/ramit/Desktop/BoundryLine/BoundaryLine/engine/matchOverDataSample.json'
    SUCCESS_STATUS = 200
    TO_MANY_REQUESTS = 429
    SUCCESS, FAILURE = 0, 1
    ZERO_VALUE = 0
    MESSAGE = 'Message'
    DATA= "data"
    STATUS = 'status'
    DATA_FOUND = "data found."
    MSG = 'MSG'
    MATCH_ID = 'MATCH_ID'
    FINISHED = 'finished'
    STATUS = 'status'



class Messages:
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
    NOT_FOUND = 'NOT_FOUND'
    CREATED = 'CREATED'
    OK = 'OK'
    TO_MANY_REQUESTS = 'TO_MANY_REQUESTS'

    

class GetClientMEssage:
    pass


class MatchConfig:
    MATCH_ID = 'match_id'
    MATCH_STATUS = 'match_status'
    INNINGS1 = '1 Inning'
    INNINGS2 = '2 Inning'
    TITLE = 'title'
    WICKET = 'wicket'
    OVERS = 'overs'
    RUNS = 'runs'
    WIDES = 'wides'
    BALLS = 'balls'
    DESCRIPTION = 'description'
    NOBALLS = 'noballs'
    LEGBYES = 'legbyes'
    BYES = 'byes'
    SEPERATOR = ' to '


class IngestionConfig:
    RECENT_MATCHES = 'RECENT_MATCHES'
    OVER_HISTORY = 'OVER_HISTORY'

class MatchColumns:
    MATCH_ID = 'match_id'



class RequestHeaders:
    HEADER = 0
    VALUE = 1
    ACCEPT = ['Accept', 'application/json']
    CONTENT_TYPE = ['Content-Type', 'null']
    X_RAPIDAPI_UA = ['x-rapidapi-ua', 'RapidAPI-Playground']
    X_RAPIDAPI_KEY = ['x-rapidapi-key', '313daaa998msh26aeaccc0d02b7bp1cebc6jsna45fbb6defef']
    X_RAPIDAPI_HOST = ['x-rapidapi-host', 'cricket-live-line1.p.rapidapi.com']
    CONTENT_TYPE_APPLICATION_JSON = ['Content-Type', 'application/json']

class Overs:
    INNING_ONE = 1
    INNING_TWO = 2

class ApiKeys:
    KEYS = ['313daaa998msh26aeaccc0d02b7bp1cebc6jsna45fbb6defef', '3f9f123a29msh2beaa37d0cddd46p1b57bejsn762407515581']
