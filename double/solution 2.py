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
        self.weights = []
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

        linksMin = 5
        linksMax = 10
        sizeMin = 0.5
        sizeMax = 1

        #generate random number of links between 5 - 10
        global linksNumber
        linksNumber = linksMin + int((linksMax - linksMin + 1) * random.random())

        #generate an array of link sizes
        global linksSizes
        linksSizes = numpy.empty((0, 3))
        global maxHeight
        maxHeight = 0.5

        for link in range(linksNumber):
            width = sizeMin + (sizeMax - sizeMin) * random.random()
            length = sizeMin + (sizeMax - sizeMin) * random.random()
            height = sizeMin + (sizeMax - sizeMin) * random.random()
            if height > maxHeight:
                maxHeight = height
                #link with the tallest Z
                maxLink = link
            tup = (width, length, height)
            linksSizes = numpy.vstack((linksSizes, tup))
        
        xPos = 0
        yPos = 0
        zPos = maxHeight/2

        for link in range(1, linksNumber):
            pyrosim.Send_Cube(name = "Link" + str(link - 1), pos = [xPos,yPos,zPos], size=linksSizes[link - 1])
            xPos = (linksSizes[link][0])/2
        
        global jointNames
        jointNames = []
        for joint in range(linksNumber - 2):
            pyrosim.Send_Joint(name = f"Link{joint}_Link{joint+1}", parent = "Link" + str(joint), child = "Link" + str(joint+1), type = "revolute", position = [(linksSizes[joint][0]),yPos,zPos], jointAxis = "0 1 0")
            jointNames = numpy.append(jointNames, f"Link{joint}_Link{joint+1}")

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        for link in range(linksNumber - 1):
            pyrosim.Send_Sensor_Neuron(name = str(link), linkName = "Link" + str(link))

        for joint in range(linksNumber - 2):
            pyrosim.Send_Motor_Neuron(name = str(joint), jointName = str(jointNames[joint]))
        
        self.weights = (numpy.random.rand(linksNumber, linksNumber - 1) * 2) - 1

        for currentRow in range(linksNumber):
            for currentColumn in range(linksNumber - 2):
                pyrosim.Send_Synapse(sourceNeuronName = str(currentRow), targetNeuronName = str(currentColumn + linksNumber), weight = self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, len(self.weights) - 1)
        randomColumn = random.randint(0, len(self.weights[0]) - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
        self.myID = ID