import json
from ingestion.extraction import *
from validation import validation_match
from validation import validation_match
from validation import validation_common



def performMatchValidation(responseData):
    validation_match.MatchValidator().validateRecentMatchesStatus(responseData) 
    validation_match.MatchValidator().validateRecentMatchesMessage(responseData)
    newMatchIds = validation_match.MatchValidator().validateRecentMatches(responseData)
    return newMatchIds



def getMatchOverDataById(newMatchIds):
    matchOverDataById = {}
    for matchId in newMatchIds[:1]:
        matchOverResponsePacket = fetchMatchOverData(matchId)
        validator = validation_common.Common()
        validator.validateMessage(matchOverResponsePacket)
        validator.validateStatus(matchOverResponsePacket)
        matchOverData = validator.validateEntity(matchOverResponsePacket)
        matchOverDataById[matchId] = matchOverData

    return matchOverDataById

responseData = fetchRecentMatches()
newMatchIds = performMatchValidation(responseData)
matchOverData = getMatchOverDataById(newMatchIds)











    



