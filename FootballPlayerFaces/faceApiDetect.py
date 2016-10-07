#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import cognitive_face as CF
import json

class PlayerInfo(object):
    name = ""
    photoUrl = ""
    faceId = ""

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def loadPlayersInfo(playersInfoList, file):
    with open(file, 'rb') as csvReadFile:
        csvReader = csv.reader(csvReadFile, delimiter=',', quotechar='|')
        for row in csvReader:
            player = PlayerInfo()
            player.name = row[1]
            player.photoUrl = row[2]
            player.faceId = row[3]
            playersInfoList.append(player)

def getPlayerNameByFaceId(playersInfoList, faceId):
    for playerInfo in playersInfoList:
        if playerInfo.faceId == faceId:
            return playerInfo
    return None

def createNewFacesList(idList, nameList):
    CF.face_list.create(idList, nameList)

def createFaceList():
    idList = 2
    #createNewFacesList(2, "atletiFaces")
    with open('atletiCaras.csv', 'rb') as csvReadFile:
        with open('atletiCarasOut.csv', 'wb') as csvWriteFile:
             csvReader = csv.reader(csvReadFile, delimiter=',', quotechar='|')
             csvWriter = csv.writer(csvWriteFile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
             for row in csvReader:
                 # Add face to the list
                 ret = CF.face_list.add_face(row[2], idList)
                 print "Face " + str(ret[u'persistedFaceId']) + " added to list " + str(idList)
                 csvWriter.writerow([row[0], row[1], row[2], ret[u'persistedFaceId']])

def getComparationFaces(urlFace, faceListId, playersInfoList):
    ret = CF.face.detect(urlFace)
    ret = CF.face.find_similars(ret[0][u'faceId'], faceListId, None, 1000, 'matchFace')
    if (len(ret) == 0):
        print "No faces in the list"
        return

    resultObj = "["
    cont = 0
    for cont in range(3):
        faceId = str(ret[cont][u'persistedFaceId'])
        confidence = str(ret[cont][u'confidence'])
        player = getPlayerNameByFaceId(playersInfoList, faceId)
        if player == None:
            return
        #print "#" + str((cont + 1)) + ") " + str(player.name) + " --- " + confidence + " --- " + player.photoUrl
        resultObj += player.toJSON() + ","
    resultObj = resultObj[:-1]
    resultObj += "]"
    resultObj = resultObj.replace("\n","")
    resultObj = resultObj.replace("\"",'"')
    return resultObj

# ---MAIN---

def lambda_handler(event, context):
    KEY = 'your_key'
    CF.Key.set(KEY)

    idList = 2
    #createFaceList(idList)

    file = "atletiCarasOut.csv"
    playersInfoList = []
    loadPlayersInfo(playersInfoList, file)

    urlFace = "http://img.estaticos-atleticodemadrid.com/system/fotos/603/showlarge/moya_web.jpg?1413539984"
    resultObj = getComparationFaces(event.key1, idList, playersInfoList)
    return resultObj

#lambda_handler("","")
