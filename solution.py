import numpy
import pyrosim.pyrosim as pyrosim
import os
import random as random
import time
import constants as c

height = 1
width = 1
length = 1
x = 0
y = 0
z = 0.5

class SOLUTION:
    def __init__(self, ID):
        self.weights = (numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2) - 1
        self.myID = ID

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        #os.system("python3 simulate.py " + directOrGUI)
        os.system(f"python3.9 simulate.py {directOrGUI} {str(self.myID)} &")
        while not os.path.exists(f"fitness{str(self.myID)}.txt"):
            time.sleep(0.01)
        with open(f"fitness{str(self.myID)}.txt", "r") as file:
            fitnessFile = file.read()
        file.close()
        self.fitness = float(fitnessFile)
        print(self.fitness)
    
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        #os.system("python3 simulate.py " + directOrGUI)
        os.system(f"python3.9 simulate.py {directOrGUI} {str(self.myID)} &")
    
    def Wait_For_Simulation_To_End(self, directOrGUI):
        while not os.path.exists(f"fitness{str(self.myID)}.txt"):
            time.sleep(0.01)
        with open(f"fitness{str(self.myID)}.txt", "r") as file:
            fitnessFile = file.read()
        file.close()
        self.fitness = float(fitnessFile)
        #print(self.fitness)
        os.system(f"rm fitness{str(self.myID)}.txt")

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
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1] , size=[width, length, height])
        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0,-0.5,1], jointAxis = "1 0 0")
        # back leg
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2,1,0.2])
        # front leg
        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0,0.5,1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0] , size=[0.2,1,0.2])
        # left leg
        pyrosim.Send_Joint(name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5, 0, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0] , size=[1, 0.2, 0.2])
        # right leg
        pyrosim.Send_Joint(name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5, 0, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0] , size=[1, 0.2, 0.2])
        # front lower leg
        pyrosim.Send_Joint(name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg" , child = "FrontLowerLeg" , type = "revolute", position = [0, 1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        # back lower leg
        pyrosim.Send_Joint(name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", position = [0, -1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        # left lower leg
        pyrosim.Send_Joint(name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg" , child = "LeftLowerLeg" , type = "revolute", position = [-1, 0, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        # right lower leg
        pyrosim.Send_Joint(name = "RightLeg_RightLowerLeg" , parent= "RightLeg" , child = "RightLowerLeg" , type = "revolute", position = [1, 0, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        # pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        # pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        # pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        # pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg")
        # pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "RightLowerLeg")

        pyrosim.Send_Motor_Neuron(name = 4, jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 5, jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name = 6, jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name = 7, jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name = 8, jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 9, jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 10, jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 11, jointName = "RightLeg_RightLowerLeg")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])
        # pyrosim.Send_Synapse(sourceNeuronName = 0 , targetNeuronName = 3 , weight = -5.0)
        # pyrosim.Send_Synapse(sourceNeuronName = 1 , targetNeuronName = 3 , weight = -5.0)
        # pyrosim.Send_Synapse(sourceNeuronName = 0, targetNeuronName = 4, weight = -5.0)
        # pyrosim.Send_Synapse(sourceNeuronName = 1, targetNeuronName =  4, weight = -5.0)

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, len(self.weights) - 1)
        randomColumn = random.randint(0, len(self.weights[0]) - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
        self.myID = ID