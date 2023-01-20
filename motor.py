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
        print(self.jointName)
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.amplitudeBack
        self.frequency = c.frequencyBack
        self.offset = c.phaseOffsetBack
        if self.jointName == b'Torso_BackLeg':
            print("worked!")
            self.frequency = c.frequencyBack / 2
        self.motorValues = (numpy.sin(numpy.linspace(0, 2 * numpy.pi, c.steps) * self.frequency + self.offset) * self.amplitude)

    def Set_Values(self, t, robot):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robot,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = self.motorValues[t],
            maxForce = c.forceBack)
    
    def Save_Values(self):
        if self.jointName == b'Torso_BackLeg':
            numpy.save("data/motorValuesBack.npy", self.motorValues)
        if self.jointName == b'Torso_FrontLeg':
            numpy.save("data/motorValuesFront.npy", self.motorValues)

