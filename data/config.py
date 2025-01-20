import os


class CommonConfig:
    API_JSON_FILE = '/home/ramit/Desktop/Boundry Line/data/ingestion/Api.json'
    SUCCESS_STATUS = 200
    SUCCESS, FAILURE = 0, 1

class IngestionConfig:
    RECENT_MATCHES = 'RECENT_MATCHES'


class RequestHeaders:
    HEADER = 0
    VALUE = 1
    ACCEPT = ['Accept', 'application/json']
    CONTENT_TYPE = ['Content-Type', 'null']
    X_RAPIDAPI_UA = ['x-rapidapi-ua', 'RapidAPI-Playground']
    X_RAPIDAPI_KEY = ['x-rapidapi-key', '313daaa998msh26aeaccc0d02b7bp1cebc6jsna45fbb6defef']
    X_RAPIDAPI_HOST = ['x-rapidapi-host', 'cricket-live-line1.p.rapidapi.com']

