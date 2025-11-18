from .validation_utilities import Utility
from config import *

class MatchValidator():
    def __init__(self, jsonData):
        self.rawData = jsonData

    def ifMatchAlreadyProcessed(self):
        infoData = self.rawData['info']
        date = '&'.join(infoData['dates'])
        teams = '&'.join(infoData['dates'])
        ## Perform database lookup
        return False
    
    def ifDataLoadedProperly(self):
        metaKeys = ['meta', 'info', 'innings']
        for key in metaKeys:
            if key not in self.rawData:
                return False
            
        return True
    
    def ifNoOutcomeOfMatch(self):
        matchResult = self.rawData['info']['outcome'].get('result')
        return matchResult and matchResult.lower() == 'no result'



    
    # def validateMatchCompletion(self, entity):
    #     return  entity[MatchConfig.MATCH_STATUS] == CommonConfig.FINISHED
    

    # def validateMatchDataPacket(self, data):
    #     return MatchConfig.INNINGS1 in data and MatchConfig.INNINGS2 in data
        

    # def validateRecentMatches(self, data):
    #     utility = Utility()
    #     matchIds = utility.getUnfinishedMatchIds(data[CommonConfig.DATA])
    #     filteredIds = utility.filterOutProcessedMatches(matchIds)
    #     return filteredIds

    # def validateRecentMatchesStatus(self, data):
    #     try:
    #         message = Messages.SUCCESS if data[CommonConfig.STATUS] == CommonConfig.OK_MESSAGE else Messages.FAILURE
            
    #         return Utility().createResponsePacket(message, data)
        
    #     except Exception as error:
    #         # Log here
    #         return Utility().createResponsePacket(Messages.INTERNAL_SERVER_ERROR, data)

    # def validateRecentMatchesMessage(self, data):
    #     try:
    #         message = Messages.SUCCESS if data[CommonConfig.MSG].lower() == CommonConfig.DATA_FOUND else Messages.FAILURE
            
    #         return Utility().createResponsePacket(message, data)
        
    #     except Exception as error:
    #         # Log here
    #         return Utility().createResponsePacket(Messages.INTERNAL_SERVER_ERROR, data)



        


    


