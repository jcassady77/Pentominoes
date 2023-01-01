
import json
from panda3d.core import LVecBase3

#Class for one specific pentomino object
class Pentomino:
    #Parse JSON for object data (static)
    pentominoFile = open("./pentominoData.json")
    pentominoData = json.load(pentominoFile)
    def __init__(self, objectId, pentominoesInstance, addToPentominoesList=True):
        #set 3d object matrix
        self.objectId = objectId
        self.objectMatrix = Pentomino.pentominoData.get("pentominoObjectMatrixData").get(objectId)
        self.position = LVecBase3()
        self.orientation = LVecBase3()
        if (addToPentominoesList):
            pentominoesInstance.pentominoes.append(self)

    def delPentomino(self, pentominoesInstance):
        if (self in pentominoesInstance.pentominoes):
            pentominoesInstance.pentominoes.remove(self)
        for cube in self.node.getChildren():
            cube.removeNode()
        self.node.removeNode()
        del self.objectId
        del self.objectMatrix
        del self.position
        del self.orientation
    
    def renderCube(self, pentominoesInstance, pos, parentNode):
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

    def renderPentomino(self, pentominoesInstance):
        #Render a specific pentomino Object
        self.node = pentominoesInstance.render.attachNewNode(self.objectId)
        for cubeLocation in self.objectMatrix:
            Pentomino.renderCube(self, pentominoesInstance, cubeLocation, self.node)
    
