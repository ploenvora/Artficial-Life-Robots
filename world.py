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
        p.loadSDF("world.sdf")