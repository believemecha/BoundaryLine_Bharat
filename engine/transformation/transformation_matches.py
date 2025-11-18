from config import *
from .transformation_utilities import *

class MatchTransformer:
    def __init__(self, matchRawData):
        self.data = matchRawData

    def extractMatchInfo(self):
        matchInfo = self.data.get('info', {})
        city = matchInfo.get('city')
        matchType = matchInfo.get('match_type')
        gender = matchInfo.get('gender')
        outcome = matchInfo.get('outcome')
        playerOfTheMatch = matchInfo.get('player_of_match')
        venue = matchInfo.get('venue')
        matchInfo = {
            'matchInfo': matchInfo,
            'city': city,
            'matchType': matchType,
            'gender': gender,
            'outcome': outcome,
            'playerOfTheMatch': playerOfTheMatch,
            'venue': venue
        }
        return matchInfo


    @staticmethod
    def getHostName(self):
        pass


    def extractOversData(self, raw_overs_data, battingData, bowlingData):
        def updateBattingData(battingData, batsman, runs, bowler):
            battingData[batsman]['aggregate']['runsScored'] += runs
            battingData[batsman]['aggregate']['ballsFaced'] += 1
            battingData[batsman]['aggregate']['fours'] += 1 if runs == 4 else 0
            battingData[batsman]['aggregate']['sixes'] += 1 if runs == 6 else 0


        def updateBowlingData(bowlingData, bowler, batterRuns, extras, wickets):
            
            #ballerGetsWicket = wickets and wickets['kind'] not in ['run out', 'retired hurt', 'obstructing the field']
            #bowlingData[bowler]['wickets'] += 1 if ballerGetsWicket else 0
            extraRuns = extras.get('noballs', 0) + extras.get('wides', 0)
            bowlingData[bowler]['aggregate']['runsConceded'] += batterRuns + extraRuns
            bowlingData[bowler]['aggregate']['balls'] += 1 if not extras.get('noballs') and not extras.get('wides') else 0
            bowlingData[bowler]['aggregate']['foursConceded'] += 1 if batterRuns == 4 else 0
            bowlingData[bowler]['aggregate']['sixesConceded'] += 1 if batterRuns == 6 else 0

        def updateWickets(battingData, bowlingData, batter, bowler, wickets):
            if not wickets:
                return
            
            for wicketData in wickets:
                playerOut = wicketData['player_out']
                if playerOut not in battingData:
                    initiateBattingData(battingData,playerOut)
                    initialiseBatsmanVsBowlerData(playerOut, bowler, battingData, bowlingData)

                battingData[playerOut]['aggregate']['out'] = True
                ballerGetsWicket = wicketData['kind'] not in ['run out', 'retired hurt', 'obstructing the field']
                bowlingData[bowler]['aggregate']['wickets'] += 1 if ballerGetsWicket else 0
                
                if bowler not in battingData[playerOut]['vsBowlers']:
                    initialiseBatsmanVsBowlerData(playerOut, bowler, battingData, bowlingData)

                battingData[playerOut]['vsBowlers'][bowler]['out'] =  ballerGetsWicket
                bowlingData[bowler]['vsBatters'][batter]['wicket'] = ballerGetsWicket and battingData[batter]['vsBowlers'][bowler]['out']

        def initialiseBatsmanVsBowlerData(batter, bowler, battingData, bowlingData):
            if bowler not in battingData[batter]['vsBowlers']:
                battingData[batter]['vsBowlers'][bowler] = {
                                    'runsScored': 0, 
                                    'ballsFaced': 0,
                                    'fours': 0,
                                    'sixes': 0,
                                    'out': False
                                }
                
            if batter not in bowlingData[bowler]['vsBatters']:
                bowlingData[bowler]['vsBatters'][batter] = {
                                    'runsConceded': 0, 
                                    'balls': 0,
                                    'foursConceded': 0,
                                    'sixesConceded': 0,
                                    'out': False
                }
        def updateBatsmanVsBowlerData(battingData, bowlingData, batter, bowler, battersScore, extras, wickets):
            initialiseBatsmanVsBowlerData(batter, bowler, battingData, bowlingData)

            battingData[batter]['vsBowlers'][bowler]['runsScored'] += battersScore
            battingData[batter]['vsBowlers'][bowler]['ballsFaced'] += 1
            battingData[batter]['vsBowlers'][bowler]['fours'] += 1 if battersScore == 4 else 0
            battingData[batter]['vsBowlers'][bowler]['sixes'] += 1 if battersScore == 6 else 0

            
            bowlingData[bowler]['vsBatters'][batter]['runsConceded'] += battersScore
            bowlingData[bowler]['vsBatters'][batter]['balls'] += 1 if not extras.get('noballs') and not extras.get('wides') else 0
            bowlingData[bowler]['vsBatters'][batter]['foursConceded'] += 1 if battersScore == 4 else 0
            bowlingData[bowler]['vsBatters'][batter]['sixesConceded'] += 1 if battersScore == 6 else 0

            

        def initiateBattingData(battingData, batsman, matchState=None):
            battingData[batsman] = {
                "aggregate": {
                    "runsScored": 0, "ballsFaced": 0, "fours": 0, "sixes": 0, "out": False, 'state': matchState
                },
                "vsBowlers": {}
            }

        def initiateBowlingData(bowlingData, bowler, matchState=None):
            bowlingData[bowler] = {
                "aggregate": {
                    "wickets": 0, "runsConceded": 0, "balls": 0, "foursConceded": 0, "sixesConceded": 0
                },
                "vsBatters": {}
            }


        
        def getDeliveryData(ballData, battingData, bowlingData, matchState=None):
            batter, bowler = ballData['batter'], ballData['bowler']
            if batter not in battingData:
                initiateBattingData(battingData, batter, matchState)
            if bowler not in bowlingData:
                initiateBowlingData(bowlingData, bowler, matchState)

            nonStriker = ballData['non_striker']
            runs = ballData.get('runs', {})
            wickets = ballData.get('wickets')
            ifWicketFall = wickets is not None
            battersScore = runs.get('batter', 0) if runs else 0
            ## Possible extras - byes, legbyes, noballs, penalty, wides
            extras = ballData.get('extras', {})
            updateBattingData(battingData,batter,battersScore,bowler)
            updateBowlingData(bowlingData, bowler, battersScore, extras, wickets)
            updateBatsmanVsBowlerData(battingData, bowlingData, batter, bowler, battersScore, extras, wickets)
            updateWickets(battingData, bowlingData, batter, bowler, wickets)
            #matchState['runs'] = 

            return battingData, bowlingData

        totalOversPlayed = len(raw_overs_data)
        matchState = {'runsScored': 0, 'wicketsDown': 0, 'ballsPlayed': 0}
        for idx in range(totalOversPlayed):
            overs = raw_overs_data[idx]['over']
            deliveries = raw_overs_data[idx]['deliveries']
            for deliveryData in deliveries:
                #getDeliveryData(deliveryData, battingData, bowlingData,matchState)
                getDeliveryData(deliveryData, battingData, bowlingData)
        
        return battingData, bowlingData

    def extractInningsInfo(self):
        rawInningsInfo = self.data['innings']
        matchInfo = self.extractMatchInfo()
        inningsData = {'info': matchInfo}
        for idx in range(2):
            battingData, bowlingData = {}, {}
            currentInnings = rawInningsInfo[idx]
            team = currentInnings.get('team')
            overs = currentInnings.get('overs')
            powerplays = currentInnings.get('powerplays')
            battingData, bowlingData = self.extractOversData(overs, battingData, bowlingData)
            inningsData[idx] = {'battingData': battingData, 'bowlingData': bowlingData, 'oversPlayed': len(overs), 'BattingTeam': team}

        return inningsData





