
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
    
    def renderCube(self, pentominoesInstance, pos, cubeArray, parentNode):
        # Load the environment model.
        distanceScale = 2
        distanceOffset = 1
        newCube = pentominoesInstance.loader.loadModel("./eggFiles/cube")
        # Reparent the model to render.
        newCube.reparentTo(parentNode)
        # Apply scale and position transforms on the model.
        newCube.setScale(1, 1, 1)
        newCube.setPos(\
            distanceScale*pos[0]+distanceOffset, \
            distanceScale*pos[1]+distanceOffset, \
            distanceScale*pos[2]+distanceOffset)
        cubeArray.append(newCube)

    def renderPentomino(self, pentominoesInstance):
        #Render a specific pentomino Object
        objectNode = pentominoesInstance.render.attachNewNode(self.objectId)
        cubeArray = []
        for cubeLocation in self.objectMatrix:
            Pentomino.renderCube(self, pentominoesInstance, cubeLocation, cubeArray, objectNode)
        pentominoesInstance.renderedObjects[self.objectId] = cubeArray
        return objectNode
