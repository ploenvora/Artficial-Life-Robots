import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random 
import constants as c
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
from world import WORLD
import os


class ROBOT:
    def __init__(self, solutionID):
        #Adding a robot
        self.world = WORLD()
        self.robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robot)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")
        os.system(f"rm brain{solutionID}.nndf")

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
    
    def Sense(self, t):
        index = 0
        for sensor_name, sensor in self.sensors.items():
            sensor.Get_Value(t)
            # Marching to the beat
            # if index == 0:
            #     sensor.values[t] = numpy.sin(15*t)
            # index += 1

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
        #print(self.motors)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[bytes(jointName, 'utf-8')].Set_Values(desiredAngle * c.motorJointRange, self.robot)

    def Think(self):
        self.nn.Update()
        #self.nn.Print()

    def Get_Fitness(self, myID):
        # stateOfLinkZero = p.getLinkState(self.robot,0)
        # positionOfLinkZero = stateOfLinkZero[0]
        # xCoordinateOfLinkZero = positionOfLinkZero[0]
        positions = self.world.getPositions()
        zPinPositionSum = sum([tuple[2] for tuple in positions[1:]])
        # basePositionAndOrientation = p.getBasePositionAndOrientation(self.robot)
        # basePosition = basePositionAndOrientation[0]
        # xPosition = basePosition[0]
        # zPosition = basePosition[2]
        #print("\n\n\n", basePositionAndOrientation, "\n\n\n")

        #Floating on air
        # sum = 0
        # for sensor_name, sensor in self.sensors.items():
        #     sum = sum + numpy.mean(sensor.values)
        # meanSensorValues = sum/4
        #print("\n\n\n", meanSensorValues, "\n\n\n")

        with open(f"tmp{str(myID)}.txt", "w") as file:
            file.write(str(zPinPositionSum))
        file.close()
        os.system(f"mv 'tmp{myID}.txt' 'fitness{myID}.txt'")            
