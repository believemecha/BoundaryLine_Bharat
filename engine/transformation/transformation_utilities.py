from config import *
class Utility:
    def __init__(self):
        pass

    def getInningsData(self, matchData):
        overs = list(matchData.keys())
        inningsBattingData = {}
        for over in overs:
            self.getOverData(matchData[over],inningsBattingData)
        return inningsBattingData


    def getBatsmanAndBowler(self, data):
        array = data.split(MatchConfig.SEPERATOR)
        batsman = array[1].split(',')[0]
        baller = array[0]
        return batsman, baller
    
    def isWicket(self, wicketData):
        return wicketData != ''
    
    def initialiseBattingData(self, batsman, inningsBattingData):
        if batsman not in inningsBattingData:
            inningsBattingData[batsman] = {
                MatchConfig.RUNS: 0,
                MatchConfig.BALLS: 0,
                MatchConfig.WICKET: False
            }
        

    def getOverData(self, overData, inningsBattingData):
        runsConceded, wickets = 0, 0
        wides, nos, extras = 0, 0, 0

        for ballWrapperData in overData[1:]:
            ballData = ballWrapperData[CommonConfig.DATA]
            print(ballData)
            batsman, baller = self.getBatsmanAndBowler(ballData[MatchConfig.TITLE])
            self.initialiseBattingData(batsman, inningsBattingData)
            isWicket = self.isWicket(ballData[MatchConfig.WICKET])
            
            runs = ballData[MatchConfig.RUNS]
            #extras = ballData[MatchConfig.WIDES] + ballData[MatchConfig.NOBALLS] + ballData[MatchConfig.LEGBYES] + ballData[MatchConfig.BYES]
            runsConceded += int(runs) 
            if isWicket:
                wickets += 1
                inningsBattingData[batsman][MatchConfig.WICKET] = True
            else:
                inningsBattingData[batsman][MatchConfig.RUNS] += int(runs)
                inningsBattingData[batsman][MatchConfig.BALLS] += 1

        return inningsBattingData

        

