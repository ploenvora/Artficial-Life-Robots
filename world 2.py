import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random 
import constants as c

class WORLD:
    def __init__(self):
        # #Adding a floor
        self.planeId = p.loadURDF("plane.urdf")
        #Tells pybullet to read in the world described in box.sdf
        #p.loadSDF("world.sdf")
        self.objects = p.loadSDF("world.sdf")

    def getPositions(self):
        positions = list()
        for obj in range(c.ball + c.pins):
            positions.append(p.getBasePositionAndOrientation(self.objects[obj])[0])
        return positions


