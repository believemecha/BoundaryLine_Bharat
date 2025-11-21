import logging
from ingestion.ingestion_batch import *
from validation.validation_match import *
from transformation.transformation_matches import *
from storage.storage_operations import *
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor




# Configure logging
logging.basicConfig(

    
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("application.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

INVALID = False


def performValidations(matchJsonData):
    """
    Perform validations on the match JSON data.
    """
    logging.info("Starting validations for match data.")
    try:
        matchValidator = MatchValidator(matchJsonData)
        ifDataProperlyLoaded = matchValidator.ifDataLoadedProperly()
        logging.info("Validation: Data properly loaded - %s", ifDataProperlyLoaded)

        matchAlreadyHandled = matchValidator.ifMatchAlreadyProcessed()
        logging.info("Validation: Match already processed - %s", matchAlreadyHandled)

        noMatchResult = matchValidator.ifNoOutcomeOfMatch()
        logging.info("Validation: No outcome of match - %s", noMatchResult)

        result = ifDataProperlyLoaded and (not matchAlreadyHandled) and (not noMatchResult)
        logging.info("Validation result: %s", result)
        return result
    except Exception as e:
        logging.error("Error during validations: %s", e)
        return False


def performTransformation(matchJsonData):
    """
    Perform transformations on the match JSON data.
    """
    logging.info("Starting transformation for match data.")
    try:
        transformer = MatchTransformer(matchJsonData)
        data = transformer.extractInningsInfo()
        logging.info("Transformation completed successfully.")
        return data
    except Exception as e:
        logging.error("Error during transformation: %s", e)
        return None

def batting_worker(args):
    batsman, data, playerIdMapping, formatId = args
    session = SessionLocal()
    try:
        playerId = playerIdMapping[batsman]

        battingObj = BatsmanStats(playerId=playerId, session=session)
        battingObj.main(data, playerId, playerIdMapping, formatId)

        session.commit()
    except Exception as e:
        session.rollback()
        print("Batting worker error for", batsman, ":", e)
    finally:
        session.close()

def bowling_worker(args):
    bowler, data, playerIdMapping, formatId = args
    session = SessionLocal()
    try:
        playerId = playerIdMapping[bowler]

        bowlingObj = BowlerStats(playerId=playerId, session=session)
        bowlingObj.main(data, playerId, playerIdMapping, formatId)

        session.commit()
    except Exception as e:
        session.rollback()
        print("Bowling worker error for", bowler, ":", e)
    finally:
        session.close()




def performStorageOperations(matchJsonData):
    logging.info("Starting storage operations for match data.")

    try:
        # ------------------------- PLAYER MAPPING -------------------------
        def getPlayerIdMapping(playersInMatch, playersTeamA, playersTeamB, teamA, teamB):
            mapping = {}
            for player in playersInMatch:
                sourceId = playersInMatch[player]
                team = teamA if player in playersTeamA else teamB
                playerObj = Player(player, team)
                playerId = playerObj.ifPlayerExistsInDatabase()
                if not playerId:
                    playerId = playerObj.addPlayer(player, team, sourceId)
                mapping[player] = playerId
            logging.info("Player ID mapping completed.")
            return mapping

        playersInMatch = matchJsonData['info']['matchInfo']['registry']['people']
        playersTeamWise = matchJsonData['info']['matchInfo']['players']
        teamA, teamB = list(playersTeamWise.keys())

        playerIdMapping = getPlayerIdMapping(
            playersInMatch,
            playersTeamWise[teamA],
            playersTeamWise[teamB],
            teamA,
            teamB
        )

        # ------------------------- MATCH INFO -------------------------
        matchInfo = matchJsonData['info']['matchInfo']
        venue = matchInfo.get('venue')
        date = datetime.strptime(matchInfo.get('dates')[0], "%Y-%m-%d")
        teamA, teamB = matchInfo.get('teams')
        format = matchInfo.get('match_info')

        matchObj = Match(venue, date, teamA, teamB, format)
        matchId = matchObj.addMatchInfo()
        logging.info(f"Match added with ID: {matchId}")

        # ------------------------- FORMAT -------------------------
        formatType = matchJsonData['info']['matchInfo']['match_type']
        formatId = Format().getFormatId(formatType)
        if not formatId:
            formatId = Format().addFormat(formatType)
            logging.info(f"Format inserted: {formatId}")

        # ------------------------- TOSS -------------------------
        tossData = matchJsonData['info']['matchInfo']['toss']
        winner = tossData['winner']

        if tossData['decision'] == 'field':
            teamBowling = winner
            teamBatting = teamA if winner == teamB else teamB
        else:
            teamBatting = teamA if winner == teamA else teamB
            teamBowling = teamB if teamBatting == teamA else teamA

        # ------------------------- INNINGS -------------------------
        for inningIdx in range(2):

            inningObj = Innings(matchId)
            inningId = inningObj.addInningsInfo()
            logging.info(f"Inning {inningIdx+1} added with ID: {inningId}")

            inningData = matchJsonData[inningIdx]

            battingData = inningData['battingData']
            bowlingData = inningData['bowlingData']

            # ------- Prepare thread jobs -------
            batting_jobs = [
                (batsman, battingData[batsman], playerIdMapping, formatId)
                for batsman in battingData if batsman in playerIdMapping
            ]

            bowling_jobs = [
                (bowler, bowlingData[bowler], playerIdMapping, formatId)
                for bowler in bowlingData if bowler in playerIdMapping
            ]

            # ------- Run batting + bowling in parallel -------
            logging.info("Launching threads for batting & bowling updates...")

            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(batting_worker, batting_jobs)
                executor.map(bowling_worker, bowling_jobs)

            # ------------------ Batsman vs Bowler Stats ------------------
            try:
                session = SessionLocal()
                bvb = BatsmanVsBowlerStats(session=session)

                bvb.updateBatsmanVsBowlerStats(battingData, playerIdMapping)


                session.commit()
                session.close()

                logging.info("Batsman vs Bowler stats updated.")
            except Exception as e:
                logging.error("Error in BVB stats: %s", e)

    except Exception as e:
        logging.error("Unexpected error in performStorageOperations:", e)


odiJsonData = ingestion_batch_main()
result = []
size = len(odiJsonData)
logging.info("Processing %d matches.", size)

for idx in range(size):
    matchJsonData = odiJsonData[idx]
    validationStatus = performValidations(matchJsonData)
    logging.info("Validation status for match %d: %s", idx + 1, validationStatus)
    if validationStatus is INVALID:
        logging.warning("Match %d is invalid. Skipping.", idx + 1)
        continue

    transformedMatchData = performTransformation(matchJsonData)
    result.append(transformedMatchData)

for matchData in result:
    performStorageOperations(matchData)

batsmanStats = BatsmanStats().getAllBatsmanStats()
batsmenFormatStats = BatsmanStats().getFormatwiseStatsAllBatsman()
batsmenVsBowlerStats = BatsmanVsBowlerStats().getAllBatsmanVsBowlerStats()
# opponentwiseBatsmanStatsTable = BatsmanStats().getOpponentwiseBatsmanStats()
logging.info("Completed Successfully")
print("Completed Successfully")