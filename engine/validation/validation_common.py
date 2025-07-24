from .validation_utilities import Utility
from config import *
class Common:
    def validateEntity(self, entity):
            return len(entity) > CommonConfig.ZERO_VALUE
            #return entity[CommonConfig.DATA]
    

    def validateMatchOverData(self, data):
        try:
            if not self.validateEntity(data):
                return False
            
            data = data[CommonConfig.DATA]
            
            if not (MatchConfig.INNINGS1 in data and MatchConfig.INNINGS2 in data):
                return False
            
            return True
        
        except Exception as error:
            # Log here
            print('Exception in validateMatchOverData', error)
            return False
         
         
    

    def validateStatus(self, data):
       # print(data,'inside validate status')
        try:
            message = Messages.SUCCESS if data[CommonConfig.STATUS] == True else Messages.FAILURE
            
            return Utility().createValidationResponsePacket(message, True)
        
        except Exception as error:
            # Log here
            print('Exception in validateStatus', error)
            return Utility().createValidationResponsePacket(Messages.INTERNAL_SERVER_ERROR, False)

    def validateMessage(self, data):

        try:
            message = Messages.SUCCESS if data[CommonConfig.MSG.lower()].lower() == CommonConfig.DATA_FOUND else Messages.FAILURE
            
            return Utility().createValidationResponsePacket(message, True)
        
        except Exception as error:
            return Utility().createValidationResponsePacket(Messages.INTERNAL_SERVER_ERROR, False)
            
        

        