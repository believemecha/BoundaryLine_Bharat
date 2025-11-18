from config import *

class Utility:
    def __init__(self):
        pass

    @staticmethod
    def isWicket(wicketData):
        return wicketData != ''
    
    @staticmethod
    def parseRuns(runs):
        """Parses run string like '4', '1wd', '2b'."""
        if 'wd' in runs:
            return int(runs[:-2]) if len(runs) > 2 else 1, True
        elif 'b' in runs:
            return int(runs[:-1]), True
        else:
            return int(runs), False

    def getBatsmanAndBowler(self, data):
        array = data.split(MatchConfig.SEPERATOR)
        batsman = array[1].split(',')[0].strip()
        bowler = array[0].strip()
        return batsman, bowler

    def initialiseBattingData(self, batsman, battingData):
        if batsman not in battingData:
            battingData[batsman] = {
                MatchConfig.RUNS: 0,
                MatchConfig.BALLS: 0,
                MatchConfig.WICKET: False,
                MatchConfig.FOURS: 0,
                MatchConfig.SIXES: 0
            }

    def initialiseBowlingData(self, bowler, bowlingData):
        if bowler not in bowlingData:
            bowlingData[bowler] = {
                MatchConfig.RUNS_CONCEDED: 0,
                MatchConfig.WICKETS: 0,
                MatchConfig.BALLS_BOWLED: 0
            }

    def updateBatsmanVsBowlerStats(self, batsman, bowler, batsmanRun, isFour, isSix, isLegal, battingData):
        if bowler not in battingData[batsman]:
            battingData[batsman][bowler] = [0, 0, 0, 0]  # balls, runs, 4s, 6s
        stats = battingData[batsman][bowler]
        stats[0] += 1 if isLegal else 0
        stats[1] += batsmanRun
        stats[2] += 1 if isFour else 0
        stats[3] += 1 if isSix else 0

    def updateBattingStats(self, batsman, bowler, batsmanRun, isFour, isSix, isWicket, isLegal, battingData):
        if isWicket:
            battingData[batsman][MatchConfig.WICKET] = bowler
        else:
            battingData[batsman][MatchConfig.RUNS] += batsmanRun
            battingData[batsman][MatchConfig.BALLS] += 1 if isLegal else 0
            battingData[batsman][MatchConfig.FOURS] += 1 if isFour else 0
            battingData[batsman][MatchConfig.SIXES] += 1 if isSix else 0

    def updateBowlingStats(self, bowler, runsConceded, isWicket, isLegal, bowlingData):
        bowlingData[bowler][MatchConfig.RUNS_CONCEDED] += runsConceded
        bowlingData[bowler][MatchConfig.BALLS_BOWLED] += 1 if isLegal else 0
        bowlingData[bowler][MatchConfig.WICKETS] += 1 if isWicket else 0

    def getOverData(self, overData, battingData, bowlingData):
        for ballWrapper in overData[1:]:
            ballData = ballWrapper.get(CommonConfig.DATA, {})
            if not ballData:
                continue

            batsman, bowler = self.getBatsmanAndBowler(ballData[MatchConfig.TITLE])
            self.initialiseBattingData(batsman, battingData)
            self.initialiseBowlingData(bowler, bowlingData)

            isWicket = self.isWicket(ballData[MatchConfig.WICKET])
            runsRaw = ballData[MatchConfig.RUNS]
            runsConceded, isExtra = self.parseRuns(runsRaw)
            isFour = 'FOUR' in ballData[MatchConfig.TITLE]
            isSix = 'SIX' in ballData[MatchConfig.TITLE]

            # Bat involvement
            batsmanRun = 0 if isExtra else runsConceded
            isLegalDelivery = not isExtra

            # Player vs Player stats
            self.updateBatsmanVsBowlerStats(batsman, bowler, batsmanRun, isFour, isSix, isLegalDelivery, battingData)

            # Batsman stats
            self.updateBattingStats(batsman, bowler, batsmanRun, isFour, isSix, isWicket, isLegalDelivery, battingData)

            # Bowler stats
            self.updateBowlingStats(bowler, runsConceded, isWicket, isLegalDelivery, bowlingData)

        return battingData, bowlingData

    def getInningsData(self, matchData):
        battingData = {}
        bowlingData = {}
        for over in matchData:
            self.getOverData(matchData[over], battingData, bowlingData)
        return battingData, bowlingData