import json
from ingestion.extraction import *
from validation import validation_match
from validation import validation_match
from validation import validation_common
from transformation import transformation_matches



def performMatchValidation(responseData):
   #print(len(responseData), 'Inside of performMatchValidation')
    validation_match.MatchValidator().validateRecentMatchesStatus(responseData) 
    validation_match.MatchValidator().validateRecentMatchesMessage(responseData)
    
    newMatchIds = validation_match.MatchValidator().validateRecentMatches(responseData)
   # print(newMatchIds, 'Inside of performMatchValidation')
    return newMatchIds



def getMatchOverDataById(newMatchIds):
    matchOverDataById = {}
    for matchId in newMatchIds[:10]:
        matchOverResponsePacket = fetchMatchOverData(matchId)
       # print(matchOverResponsePacket.keys(), 'Inside of getMatchOverDataById')
        validator = validation_common.Common()
        messageValidation = validator.validateMessage(matchOverResponsePacket)
        #print(matchOverResponsePacket, 'Inside of getMatchOverDataById packet data')
        statusValidation = validator.validateStatus(matchOverResponsePacket)
        dataValidation = validator.validateMatchOverData(matchOverResponsePacket)
        
        if not messageValidation[CommonConfig.STATUS] or not statusValidation[CommonConfig.STATUS] or not dataValidation:
            #print(messageValidation, statusValidation, 'Inside of getMatchOverDataById')
            continue
        
        matchOverData = matchOverResponsePacket[CommonConfig.DATA]
    
        matchOverDataById[matchId] = matchOverData

    return matchOverDataById

def transformMatchData(matchOverDataById):
    batsmanVsBowlerStats = {}
    transformer = transformation_matches.MatchTransformer()
    
    for matchId, matchData in matchOverDataById.items():
        matchStats = transformer.transformToBatsmanVsBowlerStats(matchData)
        batsmanVsBowlerStats[matchId] = matchStats

    return batsmanVsBowlerStats

# responseData = fetchRecentMatches()
# newMatchIds = performMatchValidation(responseData)
# #newMatchIds = [6963]
# matchOverData = getMatchOverDataById(newMatchIds)


with open (CommonConfig.SAMPLE_FILE) as f:
    matchOverData = json.load(f)[CommonConfig.DATA]

matchOverData = {7339: matchOverData}
batsmanVsBowlerStats = transformMatchData(matchOverData)
print(batsmanVsBowlerStats)























    



