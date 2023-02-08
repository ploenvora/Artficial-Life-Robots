import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random 
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        #print(self.jointName)

    def Set_Values(self, desiredAngle, robot):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robot,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = desiredAngle,
            maxForce = c.forceBack)
