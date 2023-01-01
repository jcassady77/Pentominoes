from math import pi, sin, cos

import numpy as np
import math
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *
from panda3d.core import LVecBase3


from Pentomino import Pentomino


class Pentominoes(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        base.setBackgroundColor(0.0, 0.0, 0.0, 0.0)

        #self.renderedCubes = {}
        self.pentominoes = []
        
        Pentominoes.initLighting(self)
        self.renderOrigin()

        #x y z i j k
        self.cameraPos = LVecBase3(5,50,20)
        self.cameraOrient = LVecBase3(180,-10,0)

        self.selectedPentomino = None
 
        Pentomino0 = Pentomino("1", self)
        Pentomino1 = Pentomino("2", self)
        Pentomino2 = Pentomino("3", self)

        Pentomino1.position.x = 2
        Pentomino1.position.y = 2
        Pentomino1.position.z = 2

        Pentomino2.position.x = 4
        Pentomino2.position.y = 4
        Pentomino2.position.z = 4

        Pentomino0.renderPentomino(self)
        Pentomino1.renderPentomino(self)
        Pentomino2.renderPentomino(self)

        self.updateAllPentominoPos()

        #init selected pentominoes
        self.selectedPentomino = self.pentominoes[0]
        self.selectedPentomino.node.setColorScale(100, 1, 1, 1)

        #Object movement
            #Translation
        self.accept('w', self.moveSelectedObjectYneg)
        self.accept('s', self.moveSelectedObjectYpos)
        self.accept('a', self.moveSelectedObjectXpos)
        self.accept('d', self.moveSelectedObjectXneg)
        self.accept('e', self.moveSelectedObjectZpos)
        self.accept('q', self.moveSelectedObjectZneg)
            #Rotation
        self.accept('shift-w', self.rotSelectedObjectYneg)
        self.accept('shift-s', self.rotSelectedObjectYpos)
        self.accept('shift-a', self.rotSelectedObjectXpos)
        self.accept('shift-d', self.rotSelectedObjectXneg)
        self.accept('shift-e', self.rotSelectedObjectZpos)
        self.accept('shift-q', self.rotSelectedObjectZneg)

        #Camera Movement
            #Pan
        self.accept('arrow_up', self.moveCameraPanUp)
        self.accept('arrow_down', self.moveCameraPanDown)
        self.accept('arrow_left', self.moveCameraPanLeft)
        self.accept('arrow_right', self.moveCameraPanRight)
        self.accept('arrow_up-repeat', self.moveCameraPanUp)
        self.accept('arrow_down-repeat', self.moveCameraPanDown)
        self.accept('arrow_left-repeat', self.moveCameraPanLeft)
        self.accept('arrow_right-repeat', self.moveCameraPanRight)
            #Rotate
        self.accept('shift-arrow_up', self.moveCameraRotateUp)
        self.accept('shift-arrow_down', self.moveCameraRotateDown)
        self.accept('shift-arrow_left', self.moveCameraRotateLeft)
        self.accept('shift-arrow_right', self.moveCameraRotateRight)
        self.accept('shift-arrow_up-repeat', self.moveCameraRotateUp)
        self.accept('shift-arrow_down-repeat', self.moveCameraRotateDown)
        self.accept('shift-arrow_left-repeat', self.moveCameraRotateLeft)
        self.accept('shift-arrow_right-repeat', self.moveCameraRotateRight)


        self.accept('t', self.cycleSelectedObject)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.updateCameraTask, "updateCameraTask")
        self.taskMgr.add(self.updateSelectedObjectPosTask, "updateSelectedObjectPosTask")

    def moveSelectedObjectXpos(self):
        self.checkCollisionHandler("position.addX", 2)
    def moveSelectedObjectXneg(self):
        self.checkCollisionHandler("position.addX", -2)
    def moveSelectedObjectYpos(self):
        self.checkCollisionHandler("position.addY", 2)
    def moveSelectedObjectYneg(self):
        self.checkCollisionHandler("position.addY", -2)
    def moveSelectedObjectZpos(self):
        self.checkCollisionHandler("position.addZ", 2)
    def moveSelectedObjectZneg(self):
        self.checkCollisionHandler("position.addZ", -2)

    def rotSelectedObjectXpos(self):
        self.checkCollisionHandler("orientation.addX", 90)
    def rotSelectedObjectXneg(self):
        self.checkCollisionHandler("orientation.addX", -90)
    def rotSelectedObjectYpos(self):
        self.checkCollisionHandler("orientation.addY", 90)
    def rotSelectedObjectYneg(self):
        self.checkCollisionHandler("orientation.addY", -90)
    def rotSelectedObjectZpos(self):
        self.checkCollisionHandler("orientation.addZ", 90)
    def rotSelectedObjectZneg(self):
        self.checkCollisionHandler("orientation.addZ", -90)

    def checkCollisionHandler(self, movementType, delta):
        proposedSelectedPentomino = Pentomino(self.selectedPentomino.objectId, self, False)
        proposedSelectedPentomino.position = LVecBase3(self.selectedPentomino.position)
        proposedSelectedPentomino.orientation = LVecBase3(self.selectedPentomino.orientation)
        self.movePentominoHandler(proposedSelectedPentomino, movementType, delta)
        proposedSelectedPentomino.renderPentomino(self)
        proposedSelectedPentomino.node.setPosHpr(proposedSelectedPentomino.position, proposedSelectedPentomino.orientation)
        if (self.checkCollision(proposedSelectedPentomino)):
            self.movePentominoHandler(self.selectedPentomino, movementType, delta)
        else:
            #do something to show the user there is a collision
            pass
        proposedSelectedPentomino.delPentomino(self)

    def movePentominoHandler(self, pentomino, movementType, delta):
        match movementType:
            case "position.addX":
                pentomino.position.addX(delta)
            case "position.addY":
                pentomino.position.addY(delta)
            case "position.addZ":
                pentomino.position.addZ(delta)
            case "orientation.addX":
                pentomino.orientation.addX(delta)
            case "orientation.addY":
                pentomino.orientation.addY(delta)
            case "orientation.addZ":
                pentomino.orientation.addZ(delta)

    def checkCollision(self, proposedSelectedPentomino):
        #Should return True if there are NO collisions
        absolutePositions = set()
        for pentomino in self.pentominoes:
            if (pentomino == self.selectedPentomino): #If "node" is the selected node
                continue
            for cube in pentomino.node.getChildren():
                absolutePositions.add((\
                    round(cube.getPos(self.render).x), \
                    round(cube.getPos(self.render).y), \
                    round(cube.getPos(self.render).z)))
        for cube in proposedSelectedPentomino.node.getChildren():
            absolutePositions.add((\
                    round(cube.getPos(self.render).x), \
                    round(cube.getPos(self.render).y), \
                    round(cube.getPos(self.render).z)))
        if (len(absolutePositions) < len(self.pentominoes)*5):
            return False
        return True

    def getAbsolutePositionOfCube(self, parentNodePos, parentNodeOrient, cubePos):
        # if (getHpr().x == -90 or 270):
        #             PentominoTrans = LPoint3f().y 
        return

    def cycleSelectedObject(self): #currently can cycle through unrendered pentomimoes
        selectedPentominoArrayIndex = self.pentominoes.index(self.selectedPentomino)
        self.selectedPentomino.node.clearColorScale()
        if (len(self.pentominoes) <= (selectedPentominoArrayIndex+1)):
            selectedPentominoArrayIndex = 0
        else:
            selectedPentominoArrayIndex = selectedPentominoArrayIndex + 1
        self.selectedPentomino = self.pentominoes[selectedPentominoArrayIndex]
        self.selectedPentomino.node.setColorScale(100, 1, 1, 1)


    def moveCameraRotateUp(self):
        self.cameraOrient.setY(self.cameraOrient.y + 2)
    def moveCameraRotateDown(self):
        self.cameraOrient.setY(self.cameraOrient.y - 2)
    def moveCameraRotateLeft(self):
        self.cameraOrient.setX(self.cameraOrient.x + 2)
    def moveCameraRotateRight(self):
        self.cameraOrient.setX(self.cameraOrient.x - 2)
    def moveCameraPanUp(self):
        self.cameraPos.setX(self.cameraPos.x - sin(math.radians(self.cameraOrient.x))*cos(math.radians(self.cameraOrient.y+90)))
        self.cameraPos.setY(self.cameraPos.y + cos(math.radians(self.cameraOrient.x))*cos(math.radians(self.cameraOrient.y+90)))
        self.cameraPos.setZ(self.cameraPos.z + sin(math.radians(self.cameraOrient.y+90)))
    def moveCameraPanDown(self):
        self.cameraPos.setX(self.cameraPos.x + sin(math.radians(self.cameraOrient.x))*cos(math.radians(self.cameraOrient.y+90)))
        self.cameraPos.setY(self.cameraPos.y - cos(math.radians(self.cameraOrient.x))*cos(math.radians(self.cameraOrient.y+90)))
        self.cameraPos.setZ(self.cameraPos.z - sin(math.radians(self.cameraOrient.y+90)))
    def moveCameraPanLeft(self):
        self.cameraPos.setX(self.cameraPos.x - cos(math.radians(self.cameraOrient.x)))
        self.cameraPos.setY(self.cameraPos.y - sin(math.radians(self.cameraOrient.x)))
    def moveCameraPanRight(self):
        self.cameraPos.setX(self.cameraPos.x + cos(math.radians(self.cameraOrient.x)))
        self.cameraPos.setY(self.cameraPos.y + sin(math.radians(self.cameraOrient.x)))

    

    def initLighting(self):
        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor((0.1, 0.1, 0.1, 1))
        ambientLightNP = self.render.attachNewNode(ambientLight)
        self.render.setLight(ambientLightNP)

        plight1 = PointLight('plight')
        plight1.setColor((1, 1, 1, 1))
        plnp1 = self.render.attachNewNode(plight1)
        plnp1.setPos(100, 100, 100)
        self.render.setLight(plnp1)

        plight2 = PointLight('plight')
        plight2.setColor((1, 1, 1, 1))
        plnp2 = self.render.attachNewNode(plight2)
        plnp2.setPos(100, -50, 100)
        self.render.setLight(plnp2)

    def renderOrigin(self):
        self.origin = self.loader.loadModel("./eggFiles/Axes")
        self.origin.reparentTo(self.render)
        self.origin.setScale(1, 1, 1)
        self.origin.setPos(0, 0, 0)

    # Define a procedure to move the camera.
    def updateCameraTask(self, task):
        self.camera.setPos(self.cameraPos)
        self.camera.setHpr(self.cameraOrient)
        return Task.cont

    def updateSelectedObjectPosTask(self, task):
        if None != self.selectedPentomino:
            self.selectedPentomino.position.x = round(self.selectedPentomino.position.x)
            self.selectedPentomino.position.y = round(self.selectedPentomino.position.y)
            self.selectedPentomino.position.z = round(self.selectedPentomino.position.z)

            self.selectedPentomino.orientation.x = round(self.selectedPentomino.orientation.x)
            self.selectedPentomino.orientation.y = round(self.selectedPentomino.orientation.y)
            self.selectedPentomino.orientation.z = round(self.selectedPentomino.orientation.z)

            self.selectedPentomino.node.setPosHpr(self.selectedPentomino.position, self.selectedPentomino.orientation)
        return Task.cont

    def updateAllPentominoPos(self):
        for pentomino in self.pentominoes:
            pentomino.node.setPosHpr(pentomino.position, pentomino.orientation)


pentominoesInstance = Pentominoes()
# pentominoesInstance.test()
pentominoesInstance.run()