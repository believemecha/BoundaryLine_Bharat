from .validation_utilities import Utility
from config import *
class Common:
    def validateEntity(self, entity):
            #return len(entity) > CommonConfig.ZERO_VALUE
            return entity[CommonConfig.DATA]
    

    def validateStatus(self, data):
        try:
            message = Messages.SUCCESS if data[CommonConfig.STATUS] == True else Messages.FAILURE
            
            return Utility().createResponsePacket(message, data)
        
        except Exception as error:
            # Log here
            return Utility().createResponsePacket(Messages.INTERNAL_SERVER_ERROR, data)

    def validateMessage(self, data):
        try:
            message = Messages.SUCCESS if data[CommonConfig.MSG].lower() == CommonConfig.DATA_FOUND else Messages.FAILURE
            
            return Utility().createResponsePacket(message, data)
        
        except Exception as error:
            # Log here
            return Utility().createResponsePacket(Messages.INTERNAL_SERVER_ERROR, data)

        