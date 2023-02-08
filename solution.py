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

        linksMin = 8
        linksMax = 15
        sizeMin = 0.3
        sizeMax = 1

        #generate random number of links between 5 - 10
        global linksNumber
        linksNumber = linksMin + int((linksMax - linksMin + 1) * random.random())

        linksSensorMin = int(linksNumber/2) - 2
        linksSensorMax = int((linksNumber + 1)/2) + 2

        global linksSensorNumber
        linksSensorNumber = linksSensorMin + int((linksSensorMax - linksSensorMin + 1) * random.random())

        #choose links that have sensors
        global linksSensor
        linksSensor = numpy.random.choice(numpy.arange(linksNumber), size=linksSensorNumber, replace=False)
        print("links number:", linksNumber, "links sensor", linksSensorNumber, "links with sensor:", linksSensor)

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

        for link in range(linksNumber):
            if link in linksSensor:
                pyrosim.Send_Cube(name = "Link" + str(link), pos = [xPos,yPos, zPos], size=linksSizes[link], colorString='<color rgba="0.164 0.776 0.478 1.0"/>', materialName='<material name="Green">')
            else: 
                pyrosim.Send_Cube(name = "Link" + str(link), pos = [xPos,yPos, zPos], size=linksSizes[link], colorString='<color rgba="0.164 0.776 0.95 1.0"/>', materialName='<material name="Blue">')
            if link < linksNumber - 1:
                xPos = (linksSizes[link + 1][0])/2
                zPos = 0
        
        global jointNames
        jointNames = []
        zPos = maxHeight/2
        for joint in range(linksNumber - 1):
            if joint == 0:
                xPos = (linksSizes[joint][0])/2
            else:
                xPos = (linksSizes[joint][0])
            pyrosim.Send_Joint(name = f"Link{joint}_Link{joint+1}", parent = "Link" + str(joint), child = "Link" + str(joint+1), type = "revolute", position = [xPos,yPos,zPos], jointAxis = "0 1 0")
            zPos = 0
            jointNames = numpy.append(jointNames, f"Link{joint}_Link{joint+1}")

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        for link in range(linksSensorNumber):
            pyrosim.Send_Sensor_Neuron(name = str(link), linkName = "Link" + str(linksSensor[link]))

        for joint in range(linksNumber - 1):
            pyrosim.Send_Motor_Neuron(name = str(joint + link + 1), jointName = str(jointNames[joint]))
        
        self.weights = (numpy.random.rand(linksSensorNumber, linksNumber - 1) * 2) - 1
        print(self.weights)

        for currentRow in range(linksSensorNumber):
            for currentColumn in range(linksNumber - 1):
                pyrosim.Send_Synapse(sourceNeuronName = str(currentRow), targetNeuronName = str(currentColumn + linksSensorNumber), weight = self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, len(self.weights) - 1)
        randomColumn = random.randint(0, len(self.weights[0]) - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
        self.myID = ID