from config import *
from storage.storage_operations import *
class Utility:
    def getMatchIds(self, entities):
        matchIds, match_id = [], MatchConfig.MATCH_ID
        for entity in entities:
            currentMatchId = entity[match_id]
            matchIds.append(currentMatchId)

        return matchIds
        


    def createResponsePacket(self, message, data):
        return {CommonConfig.MESSAGE: message, CommonConfig.DATA: data}
    
    def filterOutProcessedMatches(self, matchIds):
        newMatches = []
        for id in matchIds:
            print(id, '***')
            if id not in processedMatches:
                newMatches.append(id)

        return newMatches
    
    