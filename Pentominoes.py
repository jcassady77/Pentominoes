from math import pi, sin, cos

import numpy as np
import math
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *
from panda3d.core import LVecBase3


from Pentomino import Pentomino


class Pentominoes(ShowBase):
    def moveSelectedObjectYpos(self):
        self.selectedNodePos.addY(1)
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
        
    def cycleSelectedObject(self):
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

    def __init__(self):
        ShowBase.__init__(self)

        base.setBackgroundColor(0.0, 0.0, 0.0, 0.0)

        self.renderedObjects = {}
        
        Pentominoes.initLighting(self)
        self.renderOrigin()

        #x y z i j k
        self.selectedNodePos = LVecBase3()
        self.selectedNodeOrient = LVecBase3()

        self.cameraPos = LVecBase3(5,50,20)
        self.cameraOrient = LVecBase3(180,-10,0)
 
        Pentomino0 = Pentomino("0")
        self.selectedNode = Pentomino0.renderPentomino(self)

        self.accept('w', self.moveSelectedObjectYpos)
        self.accept('s', self.moveSelectedObjectYneg)
        self.accept('a', self.moveSelectedObjectXpos)
        self.accept('d', self.moveSelectedObjectXneg)
        self.accept('e', self.moveSelectedObjectZpos)
        self.accept('q', self.moveSelectedObjectZneg)

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
        self.selectedNode.setPosHpr(self.selectedNodePos, self.selectedNodeOrient)
        return Task.cont


pentominoesInstance = Pentominoes()
# pentominoesInstance.test()
pentominoesInstance.run()