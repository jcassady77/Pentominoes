
import json

#Class for one specific pentomino object
class Pentomino:
    #Parse JSON for object data (static)
    pentominoFile = open("./pentominoData.json")
    pentominoData = json.load(pentominoFile)
    def __init__(self, objectId):
        #set 3d object matrix
        self.objectId = objectId
        self.objectMatrix = Pentomino.pentominoData.get("pentominoObjectMatrixData").get(objectId)
        self.orientation = [0,0,1]
    
