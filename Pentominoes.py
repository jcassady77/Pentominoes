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
        self.renderedPentominoNodes = []
        
        Pentominoes.initLighting(self)
        self.renderOrigin()

        #x y z i j k
        self.selectedNodeArrayIndex = 0
        self.selectedNodePos = LVecBase3()
        self.selectedNodeOrient = LVecBase3()

        self.cameraPos = LVecBase3(5,50,20)
        self.cameraOrient = LVecBase3(180,-10,0)
 
        Pentomino0 = Pentomino("26")
        print(Pentomino0.objectMatrix)
        Pentomino1 = Pentomino("27")
        self.renderPentominoWrapper(Pentomino0)
        self.renderPentominoWrapper(Pentomino1)

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

    def moveSelectedObjectYpos(self):
        self.selectedNodePos.addY(1)
        self.checkCollision(self.selectedNodePos)
    def moveSelectedObjectYneg(self):
        self.selectedNodePos.addY(-1)
    def moveSelectedObjectXpos(self):
        self.selectedNodePos.addX(1)
    def moveSelectedObjectXneg(self):
        self.selectedNodePos.addX(-1)
    def moveSelectedObjectZpos(self):
        self.selectedNodePos.addZ(1)
    def moveSelectedObjectZneg(self):
        self.selectedNodePos.addZ(-1)

    def rotSelectedObjectYpos(self):
        self.selectedNodeOrient.addY(90)
    def rotSelectedObjectYneg(self):
        self.selectedNodeOrient.addY(-90)
    def rotSelectedObjectXpos(self):
        self.selectedNodeOrient.addX(90)
    def rotSelectedObjectXneg(self):
        self.selectedNodeOrient.addX(-90)
    def rotSelectedObjectZpos(self):
        self.selectedNodeOrient.addZ(90)
    def rotSelectedObjectZneg(self):
        self.selectedNodeOrient.addZ(-90)

    def checkCollision(self, proposedSelectedNodePos):
        for node in self.renderedPentominoNodes:
            if (node == self.selectedNode):
                print("found selected node")
            print("nodePos")
            print(node.getPos())
            print("nodeOrient")
            print(node.getHpr())
            print()
            for cube in node.getChildren():
                print(cube.getPos())
        # print()
        # for pentominoCubeArray in self.renderedCubes:
        #     for cube in self.renderedCubes[pentominoCubeArray]:
        #         print(cube.getPos())
        print()
        print()
        print()

    def cycleSelectedObject(self):
        self.selectedNode.clearColorScale()
        if (len(self.renderedPentominoNodes) <= (self.selectedNodeArrayIndex+1)):
            self.selectedNodeArrayIndex = 0
        else:
            self.selectedNodeArrayIndex = self.selectedNodeArrayIndex + 1
        self.selectedNode = self.renderedPentominoNodes[self.selectedNodeArrayIndex]
        self.selectedNodePos = self.selectedNode.getPos()
        self.selectedNode.setColorScale(100, 1, 1, 1)

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

    def renderPentominoWrapper(self, pentomino):
        renderedPentominoNode = pentomino.renderPentomino(self)
        self.selectedNode = renderedPentominoNode
        self.renderedPentominoNodes.append(renderedPentominoNode)

    # Define a procedure to move the camera.
    def updateCameraTask(self, task):
        self.camera.setPos(self.cameraPos)
        self.camera.setHpr(self.cameraOrient)
        return Task.cont

    def updateSelectedObjectPosTask(self, task):
        self.selectedNode.setPosHpr(self.selectedNodePos, self.selectedNodeOrient)
        return Task.cont


pentominoesInstance = Pentominoes()
# pentominoesInstance.test()
pentominoesInstance.run()