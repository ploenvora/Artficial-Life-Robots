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
start_x = 5
start_y = 1 
start_z = 0.5
pin_length = 0.2
pin_width = 0.2
pin_height = 1

class SOLUTION:
    def __init__(self, ID):
        self.weights = (numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2) - 1
        self.myID = ID
    
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
        print(self.fitness)
        os.system(f"rm fitness{str(self.myID)}.txt")

    def Create_World(self):
        #Tells pyrosim the name of the file where information about the world you're about to create 
        # should be stored. This world will currently be called box, because it will only contain a box.
        pyrosim.Start_SDF("world.sdf")

        pyrosim.Send_Sphere(name="BowlingBall" , pos=[2, 1.25, 0.4] , size=[0.4])

        #row 1
        pyrosim.Send_Cube(name="Pin1Base", pos=[start_x, start_y, start_z] , size = [pin_length, pin_width, pin_height])
        #row 2
        pyrosim.Send_Cube(name="Pin2Base", pos=[start_x + 0.35, start_y + 0.35, start_z] , size = [pin_length, pin_width, pin_height])
        pyrosim.Send_Cube(name="Pin3Base", pos=[start_x + 0.35, start_y - 0.35, start_z] , size = [pin_length, pin_width, pin_height])
        #row 3
        pyrosim.Send_Cube(name="Pin4Base", pos=[start_x + 0.7, start_y + 0.7, start_z] , size = [pin_length, pin_width, pin_height])
        pyrosim.Send_Cube(name="Pin5Base", pos=[start_x + 0.7, start_y, start_z] , size = [pin_length, pin_width, pin_height])
        pyrosim.Send_Cube(name="Pin6Base", pos=[start_x + 0.7, start_y - 0.7, start_z] , size = [pin_length, pin_width, pin_height])
        #row 4
        pyrosim.Send_Cube(name="Pin7Base", pos=[start_x + 1.05, start_y + 1.05, start_z] , size = [pin_length, pin_width, pin_height])
        pyrosim.Send_Cube(name="Pin8Base", pos=[start_x + 1.05, start_y + 0.35, start_z] , size = [pin_length, pin_width, pin_height])
        pyrosim.Send_Cube(name="Pin9Base", pos=[start_x + 1.05, start_y - 0.35, start_z] , size = [pin_length, pin_width, pin_height])
        pyrosim.Send_Cube(name="Pin10Base", pos=[start_x + 1.05, start_y - 1.05, start_z] , size = [pin_length, pin_width, pin_height])

        #Tells pyrosim to close the sdf file.
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        #x is length
        #y is width
        #z is height

        #torso
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.475] , size=[3, 2.5, 1.25], colorString='<color rgba="0.415 0.553 0.4 1.0"/>', materialName='<material name="Green">', mass=40)

        #leg #1 - back left  
        pyrosim.Send_Joint(name = "Torso_LegBackLeft" , parent= "Torso" , child = "LegBackLeft" , type = "revolute", position = [-1.3125, -1.0625, 1.1], jointAxis = "1 1 0")
        pyrosim.Send_Cube(name="LegBackLeft", pos=[0, 0, -0.425], size=[0.625, 0.625, 0.85])

        #leg #2 - back right 
        pyrosim.Send_Joint(name = "Torso_LegBackRight" , parent= "Torso" , child = "LegBackRight" , type = "revolute", position = [-1.3125, 1.0625, 1.1], jointAxis = "1 1 0")
        pyrosim.Send_Cube(name="LegBackRight", pos=[0, 0, -0.425], size=[0.625, 0.625, 0.85])

        #leg #3 - front left 
        pyrosim.Send_Joint(name = "Torso_LegFrontLeft" , parent= "Torso" , child = "LegFrontLeft" , type = "revolute", position = [1.3125, -1.0625, 1.1], jointAxis = "1 1 0")
        pyrosim.Send_Cube(name="LegFrontLeft", pos=[0, 0, -0.425], size=[0.625, 0.625, 0.85])

        #leg #4 - front right 
        pyrosim.Send_Joint(name = "Torso_LegFrontRight" , parent= "Torso" , child = "LegFrontRight" , type = "revolute", position = [1.3125, 1.0625, 1.1], jointAxis = "1 1 0")
        pyrosim.Send_Cube(name="LegFrontRight", pos=[0, 0, -0.425], size=[0.625, 0.625, 0.85])

        #foot #1 - back left  
        pyrosim.Send_Joint(name = "LegBackLeft_FootBackLeft" , parent= "LegBackLeft" , child = "FootBackLeft" , type = "revolute", position = [0, 0, -0.85], jointAxis = "1 1 0")
        pyrosim.Send_Cube(name="FootBackLeft", pos=[0, 0, -0.125], size=[0.7, 0.7, 0.25])

        #foot #2 - back right  
        pyrosim.Send_Joint(name = "LegBackRight_FootBackRight" , parent= "LegBackRight" , child = "FootBackRight" , type = "revolute", position = [0, 0, -0.85], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="FootBackRight", pos=[0, 0, -0.125], size=[0.7, 0.7, 0.25])

        #foot #3 - front left  
        pyrosim.Send_Joint(name = "LegFrontLeft_FootFrontLeft" , parent= "LegFrontLeft" , child = "FootFrontLeft" , type = "revolute", position = [0, 0, -0.85], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="FootFrontLeft", pos=[0, 0, -0.125], size=[0.7, 0.7, 0.25])

        #foot #4 - front right  
        pyrosim.Send_Joint(name = "LegFrontRight_FootFrontRight" , parent= "LegFrontRight" , child = "FootFrontRight" , type = "revolute", position = [0, 0, -0.85], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="FootFrontRight", pos=[0, 0, -0.125], size=[0.7, 0.7, 0.25])

        #head 
        pyrosim.Send_Joint(name = "Torso_Head" , parent= "Torso" , child = "Head" , type = "revolute", position = [1.25, 0, 1.675], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Head", pos=[0.35, 0, 0.6], size=[1, 1, 1])

        #shell #1
        pyrosim.Send_Joint(name = "Torso_Shell1" , parent= "Torso" , child = "Shell1" , type = "revolute", position = [0, 0, 2.1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Shell1", pos=[0, 0, 0.05], size=[2.75, 2.25, 0.1],colorString='<color rgba="0.415 0.553 0.4 1.0"/>', materialName='<material name="Green">')

        #shell #2
        pyrosim.Send_Joint(name = "Shell1_Shell2" , parent= "Shell1" , child = "Shell2" , type = "revolute", position = [0, 0, 0.1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Shell2", pos=[0, 0, 0.05], size=[2.5, 2, 0.1],colorString='<color rgba="0.415 0.553 0.4 1.0"/>', materialName='<material name="Green">')

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "LegBackLeft")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LegBackRight")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LegFrontLeft")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "LegFrontRight")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "FootBackLeft")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "FootBackRight")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "FootFrontLeft")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "FootFrontRight")

        pyrosim.Send_Motor_Neuron(name = 9, jointName = "Torso_LegBackLeft")
        pyrosim.Send_Motor_Neuron(name = 10, jointName = "Torso_LegBackRight")
        pyrosim.Send_Motor_Neuron(name = 11, jointName = "Torso_LegFrontLeft")
        pyrosim.Send_Motor_Neuron(name = 12, jointName = "Torso_LegFrontRight")
        pyrosim.Send_Motor_Neuron(name = 13, jointName = "LegBackLeft_FootBackLeft")
        pyrosim.Send_Motor_Neuron(name = 14, jointName = "LegBackRight_FootBackRight")
        pyrosim.Send_Motor_Neuron(name = 15, jointName = "LegFrontLeft_FootFrontLeft")
        pyrosim.Send_Motor_Neuron(name = 16, jointName = "LegFrontRight_FootFrontRight")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, len(self.weights) - 1)
        randomColumn = random.randint(0, len(self.weights[0]) - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
        self.myID = ID