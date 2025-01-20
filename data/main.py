from ingestion.extraction import *
import json

data = fetchRecentMatches()
with open('result.json', 'w') as outFile:
    json.dump(data, outFile)
print('Inside main')
print(data, 'This is the data')