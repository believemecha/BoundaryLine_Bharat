from ingestion.ingestion_batch import *
from validation.validation_match import *
from transformation.transformation_matches import *
from storage.storage_operations import *
from datetime import datetime
INVALID = False

def performValidations(matchJsonData):
    matchValidator = MatchValidator(matchJsonData)
    ifDataProperlyLoaded = matchValidator.ifDataLoadedProperly()
    ## Log here
    matchAlreadyHandled = matchValidator.ifMatchAlreadyProcessed()
    ## Log if match is completed

    noMatchResult = matchValidator.ifNoOutcomeOfMatch()
    return ifDataProperlyLoaded and (not matchAlreadyHandled) and (not noMatchResult)

def performTransformation(matchJsonData):
    transformer = MatchTransformer(matchJsonData)
    data = transformer.extractInningsInfo()
    return data

def performStorageOperations(matchJsonData):
    playersInMatch = matchJsonData['info']['matchInfo']['registry']['people']
    playersTeamWise = matchJsonData['info']['matchInfo']['players']
    teamA, teamB = list(playersTeamWise.keys())
    playersTeamA, playersTeamB = playersTeamWise[teamA], playersTeamWise[teamB]
    playerIdMapping = {}
    for player in playersInMatch:
        playerIdAtSource = playersInMatch[player]
        playerTeam = teamA if player in playersTeamA else teamB
        playerObj = Player(player, playerTeam)
        playerId = playerObj.ifPlayerExistsInDatabase()
        if not playerId:
            playerId = playerObj.addPlayer(player, playerTeam, playerIdAtSource)
        playerIdMapping[player] = playerId
    matchInfo = matchJsonData['info']['matchInfo']
    try:
        venue, date, teamA, teamB, format = matchInfo.get('venue'),matchInfo.get('dates')[0],\
                                            matchInfo.get('teams')[0],matchInfo.get('teams')[1], \
                                            matchInfo.get('match_info')
        date = datetime.strptime(date, "%Y-%m-%d")
        matchObj = Match(venue, date, teamA, teamB, format)
        matchId = matchObj.addMatchInfo()
    except Exception as e:
        #TODO Log here
        #TODO There must be return statement
        print(f'Error in fetching match info: {e}')



    tossData = matchJsonData['info']['matchInfo']['toss']
    format = matchJsonData['info']['matchInfo']['match_type']
    formatId = Format().getFormatId(format)
    if not formatId:
        formatId = Format().addFormat(format)

    if tossData['decision'] == 'field':
        teamBowling = tossData['winner']
        teamBatting = teamA if teamBowling == teamB else teamB
    else:
        teamBatting = teamA if tossData['winner'] == teamA else teamB
        teamBowling = teamB if teamBatting == teamA else teamA
    ## Update Batsman stats
    for inningIdx in range(2):
        ## Update innings table
        inningObj = Innings(matchId)
        inningId = inningObj.addInningsInfo()

        ## Update batting data
        inningData = matchJsonData[inningIdx]
        battingData = inningData['battingData']

        for batsman in battingData:
            playerId = playerIdMapping.get(batsman)
            if not playerId:
                continue
            battingObj = BatsmanStats(playerId=playerId)
            battingObj.main(battingData[batsman], playerId, playerIdMapping, formatId)
            batsmanVsBowlerObj = BatsmanVsBowlerStats(playerId=playerId)
            batsmanVsBowlerObj.updateBatsmanVsBowlerStats(battingData[batsman], playerIdMapping)
            
        ## Update bowling data
        bowlingData = inningData['bowlingData']
        for bowler in bowlingData:
            playerId = playerIdMapping.get(bowler)
            if not playerId:
                continue
            bowlingObj = BowlerStats(playerId=playerId)
            bowlingObj.main(bowlingData[bowler], playerId, playerIdMapping, formatId)

        
        # updateBatsmanVsBowlerStats()


odiJsonData = ingestion_batch_main()
result = []
size = len(odiJsonData)
for idx in range(size):
    matchJsonData = odiJsonData[idx]
    validationStatus = performValidations(matchJsonData)
    ## Log validation status
    if validationStatus is INVALID:
        ## Log the invalid with proper reason
        continue

    transformedMatchData = performTransformation(matchJsonData)
    result.append(transformedMatchData)


for matchData in result:
    performStorageOperations(matchData)


# data = getExistingPlayers()
# matchStats = getMatchDetails()
batsmanStats = BatsmanStats().getAllBatsmanStats()
batsmenFormatStats = BatsmanStats().getFormatwiseStatsAllBatsman()
batsmenVsBowlerStats = BatsmanVsBowlerStats().getAllBatsmanVsBowlerStats()
opponentwiseBatsmanStatsTable = BatsmanStats().getOpponentwiseBatsmanStats()
print("Completed Successfully")

'''
runs, balls, fours, sixes, out, state, metadata

runs, matches, innings, strike rate, average, 50s, 100s, 30s, 40s, notout, batting position, overs remaining
when came to bat, runsToChase, defendingOrChasing,

\
format wise
opponent team wise
opponent bolwers wise
home/away condition wise
result wise - winning cause

'''