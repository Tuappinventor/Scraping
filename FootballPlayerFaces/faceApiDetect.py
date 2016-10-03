#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import cognitive_face as CF

# Create new list
def createNewFacesList(idList, nameList):
    CF.face_list.create(idList, nameList)

# ---MAIN---

KEY = "YOUR_KEY"
CF.Key.set(KEY)

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
                 csvWriter.writerow([row[0], row[1], row[2], ret[u'persistedFaceId']])

def getComparationFaces(urlFace):
    ret = CF.face.detect(urlFace)
    ret = CF.face.find_similars(ret[0][u'faceId'], 1, None, 1000, 'matchFace')
    if (len(ret) == 0):
        print "No faces in the list"
        return

    print str(ret[0][u'persistedFaceId']) + "----" + str(ret[0][u'confidence'])

getComparationFaces("http://www.fichajes.net/files/simeone_1_1.jpeg")
