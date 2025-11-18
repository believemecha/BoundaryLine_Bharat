import os
import json
odiFolderPath = '/Users/ramit/Downloads/odis_json'

def getJsonFiles(filePath):
    files = os.listdir(filePath)
    return files


def loadJsonFiles(jsonFiles):
    jsonData = []
    for fileName in jsonFiles:
        filePath = os.path.join(odiFolderPath, fileName)
        with open(filePath, "r") as outFile:
            try:
                rawJsonData = json.load(outFile)
            except Exception as e:
                ## Log Exception
                print(f'Error occured while loading file {fileName}: ', e)
            jsonData.append(rawJsonData)

    return jsonData

def ingestion_batch_main():
    odiJsonFiles = getJsonFiles(odiFolderPath)
    jsonData = loadJsonFiles(odiJsonFiles)
    return jsonData



