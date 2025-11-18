from .models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("postgresql://bharat:yourpassword@69.164.242.182:5432/bharatdb")  # or your DB URL
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
class Player:
    def __init__(self, name, country, idAtSource=None):
        self.name = name
        self.country = country

    def ifPlayerExistsInDatabase(self):
        playerData = session.query(PlayerTable).filter_by(name=self.name,country=self.country).first()
        return playerData.id if playerData else None

    def addPlayer(self, playerName, country, sourceId):
        currentPlayer = PlayerTable(name=playerName, country=country)
        session.add(currentPlayer)
        session.flush()  # Ensures the currentPlayer.id is populated
        playerStats = BatsmanStatsTable(player_id=currentPlayer.id)  # Add default values
        session.add(playerStats)
        session.commit()

        return currentPlayer.id
    
    def updatePlayerStats(self, stats):
        pass

    def getExistingPlayers(self):
        data = session.query(PlayerTable).all()
        statsData = session.query(BatsmanStatsTable).all()
        result = []
        stats = []
        for playerData in data:
            playerId = playerData.id
            result.append([playerData.name, playerData.country])
            statsData = session.query(BatsmanStatsTable).filter_by(player_id=playerId).first()
            stats.append(statsData)

        # session.query(PlayerTable).delete()
        session.commit()

        return result, stats


class Match:
    def __init__(self, venue, date, teamA, teamB, format):
        self.venue = venue
        self.date = date
        self.teamA = teamA
        self.teamB = teamB
        self.format = format

    def addMatchInfo(self):
        match = MatchTable(venue=self.venue, date=self.date, teamA = self.teamA, teamB=self.teamB, format=self.format)
        session.add(match)
        session.commit()
        return match.id


class Innings:
    def __init__(self, matchId):
        self.matchId = matchId

    def addInningsInfo(self):
        inning = InningsTable(match_id=self.matchId)
        session.add(inning)
        session.commit()
        return inning.id

class BatsmanStats:
    def __init__(self, playerId=None, totalRuns=0, ballsFaced=0, fours=0, sixes=0, strikeRate=0.0, average=0.0):
        self.playerId = playerId
        self.totalRuns = totalRuns
        self.ballsFaced = ballsFaced
        self.fours = fours
        self.sixes = sixes
        self.strikeRate = strikeRate
        self.average = average

    def addBatsmanStats(self):
        batsmanStats = BatsmanStatsTable(
            player_id=self.playerId,
            total_runs=self.totalRuns,
            balls_faced=self.ballsFaced,
            fours=self.fours,
            sixes=self.sixes,
            strike_rate=self.strikeRate,
            average=self.average
        )
        session.add(batsmanStats)
        session.commit()

    def updateBatsmanStats(self, playerId, batsmanStats):
        existingStats = session.query(BatsmanStatsTable).filter_by(player_id=playerId).first()
        if existingStats:
            existingStats.total_runs = batsmanStats['total_runs']
            existingStats.balls_faced = batsmanStats['balls_faced']
            existingStats.fours = batsmanStats['fours']
            existingStats.sixes = batsmanStats['sixes']
            existingStats.strike_rate = batsmanStats['strike_rate']
            existingStats.average = batsmanStats['average']
            existingStats.total_dismissals = batsmanStats['total_dismissals']
            existingStats.innings_played = batsmanStats['innings_played']
            session.commit()
        else:
            newStats = BatsmanStatsTable(
                player_id=playerId,
                total_runs=batsmanStats['total_runs'],
                balls_faced=batsmanStats['balls_faced'],
                fours=batsmanStats['fours'],
                sixes=batsmanStats['sixes'],
                strike_rate=batsmanStats['strike_rate'],
                average=batsmanStats['average'],
                total_dismissals=batsmanStats['total_dismissals'],
                innings_played=batsmanStats['innings_played']
            )
            session.add(newStats)
            session.commit()

    def getBatsmanStats(self, playerId):
        batsmanStats = session.query(BatsmanStatsTable).filter_by(player_id=playerId).first()
        return batsmanStats
    
    def getAllBatsmanStats(self):
        batsmanStatsList = session.query(BatsmanStatsTable).all()
        result = {}
        for idx, batsmanStats in enumerate(batsmanStatsList):
            player = session.query(PlayerTable).filter_by(id=batsmanStats.player_id).first()
            result[player.name] = batsmanStats
        return batsmanStatsList
    
    def getBatsmanStatsInFormat(self, formatId, batsmanId):
        FormatwiseBatsmanStatsTableObj = session.query(FormatwiseBatsmanStatsTable).filter_by(format_id=formatId, batsman_id=batsmanId).first()
        return FormatwiseBatsmanStatsTableObj

    def updateBatsmanFormatStats(self, formatId, runs, balls, fours, sixes, outState):
        formatStats = self.getBatsmanStatsInFormat(formatId, self.playerId)
        if formatStats:
            formatStats.runs += runs
            formatStats.balls += balls
            formatStats.fours += fours
            formatStats.sixes += sixes
            formatStats.matches += 1
            formatStats.innings += 1
            formatStats.not_out += 0 if outState else 1
            formatStats.strike_rate = (formatStats.runs / formatStats.balls) * 100 if formatStats.balls > 0 else 0.0
            formatStats.average = (formatStats.runs / (formatStats.innings - formatStats.not_out)) if (formatStats.innings - formatStats.not_out) > 0 else 0.0
            formatStats.half_centuries += 1 if runs >=50 and runs <100 else 0
            formatStats.centuries += 1 if runs >=100 else 0
            formatStats.ducks += 1 if runs ==0 else 0
            formatStats.double_centuries += 1 if runs >=200 else 0
            formatStats.triple_centuries += 1 if runs >=300 else 0
            formatStats.four_hundreds += 1 if runs >=400 else 0
            session.commit()
        else:
            newFormatStats = FormatwiseBatsmanStatsTable(
                format_id=formatId,
                batsman_id=self.playerId,
                runs=runs,
                balls=balls,
                fours=fours,
                sixes=sixes,
                matches=1,
                innings=1,
                not_out=0 if outState else 1,
                strike_rate=(runs / balls) * 100 if balls > 0 else 0.0,
                average=(runs / (1 - (0 if outState else 1))) if (1 - (0 if outState else 1)) > 0 else 0.0,
                half_centuries=1 if runs >=50 and runs <100 else 0,
                centuries=1 if runs >=100 else 0,
                ducks=1 if runs ==0 else 0,
                double_centuries=1 if runs >=200 else 0,
                triple_centuries=1 if runs >=300 else 0,
                four_hundreds=1 if runs >=400 else 0
            )
            session.add(newFormatStats)
            session.commit()

    def getFormatwiseStatsAllBatsman(self):
        formatwiseStats = session.query(FormatwiseBatsmanStatsTable).all()
        return formatwiseStats
    
    
    def main(self, battingData, playerId, playerIdMapping, formatId):
        # self.addBatsmanVsBowlerStats(battingData, playerId, playerIdMapping)


        aggregateBattingData = battingData['aggregate']
        runs, balls, fours, sixes, outState = aggregateBattingData['runsScored'], \
                                                    aggregateBattingData['ballsFaced'], \
                                                    aggregateBattingData['fours'], \
                                                    aggregateBattingData['sixes'], \
                                                    aggregateBattingData['out']
        batsmanStats = self.getBatsmanStats(playerId)
        previousRuns = batsmanStats.total_runs if batsmanStats else 0
        previousBalls = batsmanStats.balls_faced if batsmanStats else 0
        totalDismisals = (batsmanStats.total_dismissals if batsmanStats else 0) + (1 if outState else 0)
        inningsPlayed = (batsmanStats.innings_played if batsmanStats else 0) + 1

        newTotalRuns = previousRuns + runs
        newBallsFaced = previousBalls + balls
        newFours = (batsmanStats.fours if batsmanStats else 0) + fours
        newSixes = (batsmanStats.sixes if batsmanStats else 0) + sixes
        newStrikeRate = (newTotalRuns / newBallsFaced) * 100 if newBallsFaced > 0 else 0.0
        newAverage = newTotalRuns / totalDismisals if totalDismisals > 0 else 0.0
        newBatsmanStats = {
            'total_runs': newTotalRuns,
            'balls_faced': newBallsFaced,
            'fours': newFours,
            'sixes': newSixes,
            'strike_rate': newStrikeRate,
            'average': newAverage,
            'total_dismissals': totalDismisals,
            'innings_played': inningsPlayed
        }



        self.updateBatsmanStats(playerId, newBatsmanStats)
        self.updateBatsmanFormatStats(formatId, runs, balls, fours, sixes, outState)

class BowlerStats:
    def __init__(self, playerId=None):
        self.playerId = playerId

    def main(self, bowlingData, playerId, playerIdMapping, formatId):
        aggregateBowlingData = bowlingData['aggregate']
        runsConceded, ballsBowled, wickets = aggregateBowlingData['runsConceded'], \
                                             aggregateBowlingData['balls'], \
                                             aggregateBowlingData.get('wickets', 0)
        existingStats = session.query(BowlerStatsTable).filter_by(player_id=playerId).first()
        if existingStats:
            existingStats.runs_conceded += runsConceded
            existingStats.balls_bowled += ballsBowled
            existingStats.wickets += wickets
            existingStats.strike_rate = (existingStats.balls_bowled / existingStats.wickets) if existingStats.wickets > 0 else 0.0
            existingStats.average = (existingStats.runs_conceded / existingStats.wickets) if existingStats.wickets > 0 else 0.0
            session.commit()
        else:
            strikeRate = (ballsBowled / wickets) if wickets > 0 else 0.0
            average = (runsConceded / wickets) if wickets > 0 else 0.0
            newStats = BowlerStatsTable(
                player_id=playerId,
                runs_conceded=runsConceded,
                balls_bowled=ballsBowled,
                wickets=wickets,
                strike_rate=strikeRate,
                average=average
            )
            session.add(newStats)
            session.commit()


class BatsmanVsBowlerStats:
    def __init__(self, playerId=None):
        self.batsmanId = playerId

    def updateBatsmanVsBowlerStats(self, battingInfo, playerIdMapping):
        vsBowlersData = battingInfo.get('vsBowlers', {})
        for bowlerName, bowlerStats in vsBowlersData.items():
            bowlerId = playerIdMapping.get(bowlerName)
            opponentBowlerWiseBatsmanStatsObj = OpponentBowlerWiseBatsmanStats(self.batsmanId, bowlerId)
            runs, balls, fours, sixes, isDissmissed = bowlerStats.get('runsScored', 0), \
                                                    bowlerStats.get('ballsFaced', 0), \
                                                    bowlerStats.get('fours', 0), \
                                                    bowlerStats.get('sixes', 0), \
                                                    bowlerStats.get('out', False)
            existingStats = session.query(BatsmanVsBowlerStatsTable).filter_by(batsman_id=self.batsmanId, bowler_id=bowlerId).first()
            if existingStats:
                existingStats.runs += runs
                existingStats.balls += balls
                existingStats.fours += fours
                existingStats.sixes += sixes
                existingStats.dismissals += 1 if isDissmissed else 0
                session.commit()
            else:
                newStats = BatsmanVsBowlerStatsTable(
                    batsman_id=self.batsmanId,
                    bowler_id=bowlerId,
                    runs=runs,
                    balls=balls,
                    fours=fours,
                    sixes=sixes,
                    dismissals=1 if isDissmissed else 0
                )
                session.add(newStats)
                session.commit()
            
            opponentBowlerWiseBatsmanStatsObj = OpponentBowlerWiseBatsmanStats(self.batsmanId, bowlerId)
            opponentBowlerWiseBatsmanStatsObj.updateBattingStats(bowlerStats)
    def getAllBatsmanVsBowlerStats(self):
        stats = session.query(BatsmanVsBowlerStatsTable).all()
        return stats

class Format:
    def addFormat(self, formatName):
        formatObj = FormatTable(name=formatName)
        session.add(formatObj)
        session.commit()
        return formatObj.id
    
    def getFormatId(self, formatName):
        formatObj = session.query(FormatTable).filter_by(name=formatName).first()
        return formatObj.id if formatObj else None

class FormatwiseBatsmanStats:
    pass

class OpponentwiseBatsmanStats:
    pass

class OpponentBowlerWiseBatsmanStats:
    def __init__(self, batsmanId, bowlerId):
        self.batsmanId = batsmanId
        self.bowlerId = bowlerId

    def updateBattingStats(self, battingData):
        pass






# Create a player

