from math import pi, sin, cos

import numpy as np
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import *
from panda3d.core import LVecBase3

from Pentomino import Pentomino


class Pentominoes(ShowBase):
    def moveSelectedObjectUp(self):
        self.selectedNodePos.addY(1)

    def moveSelectedObjectDown(self):
        self.selectedNodePos.addY(-1)

    def moveSelectedObjectLeft(self):
        self.selectedNodePos.addX(-1)

    def moveSelectedObjectRight(self):
        self.selectedNodePos.addX(1)

    def cycleSelectedObject(self):
        self.selectedNode.setColorScale(100, 1, 1, 1)

    def __init__(self):
        ShowBase.__init__(self)

        base.setBackgroundColor(0.0, 0.0, 0.0, 0.0)

        self.renderedObjects = {}
        
        Pentominoes.initLighting(self)
        self.renderOrigin()

        #x y z i j k
        self.selectedNodePos = LVecBase3()
        self.selectedNodeOrient = LVecBase3()

        Pentomino0 = Pentomino("0")
        self.selectedNode = Pentomino0.renderPentomino(self)

        self.accept('arrow_up', self.moveSelectedObjectUp)
        self.accept('arrow_down', self.moveSelectedObjectDown)
        self.accept('arrow_left', self.moveSelectedObjectLeft)
        self.accept('arrow_right', self.moveSelectedObjectRight)

        self.accept('t', self.cycleSelectedObject)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
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
    def spinCameraTask(self, task):
        angleDegrees = task.time * 20.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(40 * sin(angleRadians), -40 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def updateSelectedObjectPosTask(self, task):
        self.selectedNode.setPosHpr(self.selectedNodePos, self.selectedNodeOrient)
        return Task.cont


pentominoesInstance = Pentominoes()
# pentominoesInstance.test()
pentominoesInstance.run()