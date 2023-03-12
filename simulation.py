import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random 
import constants as c

from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self, directOrGUI, solutionID):

        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)

        #self.physicsClient = p.connect(p.GUI)
        #self.physicsClient = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        #Set gravity
        p.setGravity(0,0,-9.8)
        
        self.myID = solutionID
        self.world = WORLD()
        self.robot = ROBOT(self.myID)
    
    def Run(self):
        for i in range(1000):
            #print(i)
            p.stepSimulation()

            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            time.sleep(1/600)

    def __del__(self):
        p.disconnect()

    def Get_Fitness(self):
        self.robot.Get_Fitness(self.myID)
