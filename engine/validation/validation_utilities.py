from config import *
# from storage.storage_operations import *
class Utility:
    def getUnfinishedMatchIds(self, entities):
        matchIds, match_id = [], MatchConfig.MATCH_ID

        for entity in entities:
            currentMatchId = entity[match_id]
            if entity[MatchConfig.MATCH_STATUS].lower() != CommonConfig.FINISHED:
               # print(entity[MatchConfig.MATCH_STATUS])
                continue
            matchIds.append(currentMatchId)

        return matchIds

    def generateApiResponse(self, url, headers):
        pass
        


    def createResponsePacket(self, message, data):
        return {CommonConfig.MESSAGE: message, CommonConfig.DATA: data}
    
    def createValidationResponsePacket(self, message, status):
        return {CommonConfig.MESSAGE: message, CommonConfig.STATUS: status}
    
    def filterOutProcessedMatches(self, matchIds):
        newMatches = []
        for id in matchIds:
          #  print(id, '***')
            if id not in processedMatches:
                newMatches.append(id)

        return newMatches
    
    