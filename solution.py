import numpy
import pyrosim.pyrosim as pyrosim
import os
import random as random

height = 1
width = 1
length = 1
x = 0
y = 0
z = 0.5

class SOLUTION:
    def __init__(self):
        self.weights = (numpy.random.rand(3, 2) * 2) - 1

    def Evaluate(self, str):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3.9 simulate.py {str}")
        with open("fitness.txt", "r") as file:
            fitnessFile = file.read()
        file.close()
        self.fitness = float(fitnessFile)

    def Create_World(self):
        #Tells pyrosim the name of the file where information about the world you're about to create 
        # should be stored. This world will currently be called box, because it will only contain a box.
        pyrosim.Start_SDF("world.sdf")
        
        pyrosim.Send_Cube(name="Box", pos=[x + 5,y + 5,z] , size=[width, length, height])

        #Tells pyrosim to close the sdf file.
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        #pyrosim.Send_Cube(name="Box", pos=[x + 5,y + 5,z] , size=[width, length, height])
        # torso
        pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5] , size=[width, length, height])
        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1,0,1])
        # back leg
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5] , size=[width, length, height])
        # front leg
        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2,0,1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5] , size=[width, length, height])
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Motor_Neuron(name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_FrontLeg")

        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + 3, weight = self.weights[currentRow][currentColumn])
                
        # pyrosim.Send_Synapse(sourceNeuronName = 0 , targetNeuronName = 3 , weight = -5.0)
        # pyrosim.Send_Synapse(sourceNeuronName = 1 , targetNeuronName = 3 , weight = -5.0)
        # pyrosim.Send_Synapse(sourceNeuronName = 0, targetNeuronName = 4, weight = -5.0)
        # pyrosim.Send_Synapse(sourceNeuronName = 1, targetNeuronName =  4, weight = -5.0)

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, len(self.weights) - 1)
        randomColumn = random.randint(0, len(self.weights[0]) - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1