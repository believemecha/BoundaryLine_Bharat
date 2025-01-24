from .validation_common import Common
from .validation_utilities import Utility
from config import *

class MatchValidator(Common):
    def __init__(self):
        pass

    
    def validateRecentMatches(self, data):
        utility = Utility()
        matchIds = utility.getMatchIds(data[CommonConfig.DATA])
        print(matchIds)
        filteredIds = utility.filterOutProcessedMatches(matchIds)
        return filteredIds

    def validateRecentMatchesStatus(self, data):
        try:
            message = Messages.SUCCESS if data[CommonConfig.STATUS] == True else Messages.FAILURE
            
            return Utility().createResponsePacket(message, data)
        
        except Exception as error:
            # Log here
            return Utility().createResponsePacket(Messages.INTERNAL_SERVER_ERROR, data)

    def validateRecentMatchesMessage(self, data):
        try:
            message = Messages.SUCCESS if data[CommonConfig.MSG].lower() == CommonConfig.DATA_FOUND else Messages.FAILURE
            
            return Utility().createResponsePacket(message, data)
        
        except Exception as error:
            # Log here
            return Utility().createResponsePacket(Messages.INTERNAL_SERVER_ERROR, data)

        


    


