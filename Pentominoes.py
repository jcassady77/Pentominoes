from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import *

from Pentomino import Pentomino

class Pentominoes(ShowBase):

    def test(self):
        Pentomino0 = Pentomino("1")

        Pentominoes.renderObject(self, Pentomino0, [0, 0, 0, 0], [0, 0, 0])

        print("hi")


    def __init__(self):
        ShowBase.__init__(self)

        base.setBackgroundColor(0.0, 0.0, 0.0, 0.0)

        self.renderedObjects = {}
        
        Pentominoes.initLighting(self)
        self.renderOrigin()

        self.accept('arrow_up-up', self.test)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

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

    def renderCube(self, pos, cubeArray):
        # Load the environment model.
        distanceScale = 2
        distanceOffset = 1
        newCube = self.loader.loadModel("./eggFiles/cube")
        # Reparent the model to render.
        newCube.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        newCube.setScale(1, 1, 1)
        newCube.setPos(\
            distanceScale*pos[0]+distanceOffset, \
            distanceScale*pos[1]+distanceOffset, \
            distanceScale*pos[2]+distanceOffset)
        cubeArray.append(newCube)

    def renderObject(self, pentominoObject, orientation, position):
        #Render a specific pentomino Object
        cubeArray = []
        for cubeLocation in pentominoObject.objectMatrix:
            Pentominoes.renderCube(self, cubeLocation, cubeArray)
        self.renderedObjects[pentominoObject.objectId] = cubeArray

    def renderOrigin(self):
        self.origin = self.loader.loadModel("./eggFiles/Axes")
        self.origin.reparentTo(self.render)
        self.origin.setScale(1, 1, 1)
        self.origin.setPos(0, 0, 0)

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 20.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

pentominoesInstance = Pentominoes()
# pentominoesInstance.test()
pentominoesInstance.run()