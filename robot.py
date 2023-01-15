import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random 
import constants as c
from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self):
        #Adding a robot
        self.robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robot)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
        print(self.sensors.items())
    
    def Sense(self, t):
        for sensor_name, sensor in self.sensors.items():
            sensor.Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
        print(self.motors.items())

    def Act(self, t):
        for motor_name, motor in self.motors.items():
            motor.Set_Values(t, self.robot)
            motor.Save_Values()

            





