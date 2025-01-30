from ingestion.extraction import *
from validation import validation_match
from validation import validation_match

import json

# fetch over by over, eventually ball by ball details for each match

responseData = fetchRecentMatches()
## Logs and handling needs to be done here after validations

#validation_match.MatchValidator.validateEntity(responseData)
validation_match.MatchValidator().validateRecentMatchesStatus(responseData)
validation_match.MatchValidator().validateRecentMatchesMessage(responseData)
newMatchIds = validation_match.MatchValidator().validateRecentMatches(responseData)

for matchId in newMatchIds:
    pass