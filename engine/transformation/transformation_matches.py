from config import *
from .transformation_utilities import *
from config import *
class MatchTransformer:
    def transformToBatsmanVsBowlerStats(self, matchesData):

        innings = [MatchConfig.INNINGS1, MatchConfig.INNINGS2]
        stats = {}
        
        for inning in innings:
            stats[inning] = Utility().getInningsData(matchesData[inning])
        
        

            
            

        """
        Transform match data into batsman vs bowler statistics
        
        Expected schema:
        {
            "batsman_id": {
                "bowler_id": {
                    "runs": int,
                    "balls": int,
                    "dots": int,
                    "fours": int,
                    "sixes": int,
                    "dismissal": str,  # Optional, if dismissed by this bowler
                }
            }
        }
        """
        

        
        # Parse through match_data and populate stats
        # You'll need to implement the logic based on your match_data structure
        
        return stats
    
    def _processBall(self, ballData, stats):
        """Helper method to process each ball and update stats"""
        # Extract batsman_id, bowler_id, runs, etc. from ball_data
        # Update the stats dictionary accordingly
        pass

    