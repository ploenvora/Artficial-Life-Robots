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

        linksMin = 10
        linksMax = 20
        sizeMin = 0.2
        sizeMax = 1

        global numLinks
        numLinks = random.randint(linksMin, linksMax)

        # Starting link
        width = random.uniform(sizeMin, sizeMax)
        length = random.uniform(sizeMin, sizeMax)
        height = random.uniform(sizeMin, sizeMax)
        global links
        links = [self.Link("Link0", (width, length, height))]
        links[0].position = (0, 0, height/2 + 2)
        links[0].relative = (0, 0, height/2 + 2)
        links[0].faces_chosen = []
        global joints
        joints = []
        counter = 1

        # Generate links and joints to complete the structure
        while len(links) != numLinks:
            # Create a new link
            width = random.uniform(sizeMin, sizeMax)
            length = random.uniform(sizeMin, sizeMax)
            height = random.uniform(sizeMin, sizeMax)
            newLink = self.Link("Link" + str(counter), (width, length, height))

            # Find a random link to connect it to 
            parentLink = random.choice(links)
            px, py, pz = parentLink.position[0], parentLink.position[1],parentLink.position[2]
            pw, pl, ph = parentLink.size[0], parentLink.size[1], parentLink.size[2]
            
            # Chose a face
            face, sx, sy, sz = parentLink.choseFace()
            if not face:
                continue
            
            # Use the face to determine the joint positions, if there are no joints it starts from the origin
            if parentLink.name == "Link0":
                jx, jy, jz = px + sx*pw/2, py + sy*pl/2, pz + sz*ph/2
                absolute = (jx, jy, jz)
            else: 
                parentJoint = [joint for joint in joints if joint.child == parentLink.name][0]
                absolute = (px + sx*pw/2, py + sy*pl/2, pz + sz*ph/2)
                jx, jy, jz = tuple(x - y for x, y in zip(absolute, parentJoint.position))  
            
            newJoint = self.Joint(f"{parentLink.name}_{newLink.name}", parentLink.name, newLink.name, absolute, (jx, jy, jz))
            
            # Input the absolute and relative position of the links
            newLink.relative = (width * sx/2, length * sy/2, height * sz/2)
            newLink.position = (px + sx*(pw+width)/2, py + sy*(pl+length)/2, pz + sz*(ph+height)/2)
            newLink.faces_chosen = []
            
            # Check for intersections with other links
            intersects = False
            for otherLink in links:
                if newLink.intersects(otherLink):
                    intersects = True
            
            if intersects:
                continue
            else:
                links.append(newLink)
                parentLink.faces_chosen.append(face)
                oppositeFace = face.replace("+", "_").replace("-", "+").replace("_", "-")
                newLink.faces_chosen.append(oppositeFace)
                joints.append(newJoint)
                counter += 1
        
        print("Links:")
        for link in links:
            print(link)
        print("Joints:")
        for joint in joints:
            print(joint)

        #Generate links
        global unsensoredLinks
        global sensoredLinks
        unsensoredLinks = []
        sensoredLinks = []
        for link in range(numLinks):
            randomBool = random.choice([True, False])
            if randomBool:
                sensoredLinks.append(("Link"+str(link), link))
                pyrosim.Send_Cube(name = "Link" + str(link), pos = (links[link].relative[0], links[link].relative[1], links[link].relative[2]), size=links[link].size, colorString='<color rgba="0.164 0.776 0.478 1.0"/>', materialName='<material name="Green">')
            else:
                unsensoredLinks.append(("Link"+str(link), link))
                pyrosim.Send_Cube(name = "Link" + str(link), pos = (links[link].relative[0], links[link].relative[1], links[link].relative[2]), size=links[link].size, colorString='<color rgba="0.164 0.776 0.95 1.0"/>', materialName='<material name="Blue">')

        for joint in joints:
            randomBool2 = random.choice([1, 2, 3])
            if randomBool2 == 1:
                pyrosim.Send_Joint(name = joint.name, parent = joint.parent, child = joint.child, type = "revolute", position = (joint.relative[0], joint.relative[1], joint.relative[2]), jointAxis = "0 1 0")
            elif randomBool2 == 2:
                pyrosim.Send_Joint(name = joint.name, parent = joint.parent, child = joint.child, type = "revolute", position = (joint.relative[0], joint.relative[1], joint.relative[2]), jointAxis = "1 0 0")
            else:
                pyrosim.Send_Joint(name = joint.name, parent = joint.parent, child = joint.child, type = "fixed", position = (joint.relative[0], joint.relative[1], joint.relative[2]), jointAxis = "0 1 0")

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        for link in range(len(sensoredLinks)):
            pyrosim.Send_Sensor_Neuron(name = str(link), linkName = "Link" + str(sensoredLinks[link][1]))

        for joint in range(len(joints)):
            pyrosim.Send_Motor_Neuron(name = str(joint + link + 1), jointName = joints[joint].name)
        
        self.weights = (numpy.random.rand(numLinks, numLinks - 1) * 2) - 1
        # print(self.weights)

        for currentRow in range(len(sensoredLinks)):
            for currentColumn in range(len(joints)):
                pyrosim.Send_Synapse(sourceNeuronName = str(currentRow), targetNeuronName = str(currentColumn + len(sensoredLinks)), weight = self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, len(self.weights) - 1)
        randomColumn = random.randint(0, len(self.weights[0]) - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
        self.myID = ID

    # Declaring new classes
    class Link:
        def __init__(self, name, size, position = None, relative = None, faces_chosen = []):
            self.name = name
            self.size = size
            self.position = position
            self.relative = relative
            self.faces_chosen = faces_chosen
        
        def __str__(self):
            return "{}: position={}, relative={}, size={} \n".format(self.name, self.position, self.relative, self.size)
        
        def intersects(self, other_link):
            dx = abs(self.position[0] - other_link.position[0])
            dy = abs(self.position[1] - other_link.position[1])
            dz = abs(self.position[2] - other_link.position[2])
            if dx < (self.size[0] + other_link.size[0])/2 and dy < (self.size[1] + other_link.size[1])/2 and dz < (self.size[2] + other_link.size[2])/2:
                return True
            return False
        
        def choseFace(self):
            # If the list is full (all faces have joints)
            if len(self.faces_chosen) == 6:
                return False, None, None, None
            
            while True:
                # Choose a random face
                face, sx, sy, sz = random.choice([("x+", 1, 0, 0), 
                                                ("x-", -1, 0, 0), 
                                                ("y+", 0, 1, 0), 
                                                ("y-", 0, -1, 0), 
                                                ("z+", 0, 0, 1), 
                                                ("z-", 0, 0, -1)])
                # If face is not in list, return
                if face not in self.faces_chosen:
                    return face, sx, sy, sz

    class Joint:
        def __init__(self, name, parent, child, position, relative):
            self.name = name
            self.parent = parent
            self.child = child
            self.position = position
            self.relative = relative
        
        def __str__(self):
            return "{}: parent={}, child={}, position={}, relative={}".format(self.name, self.parent, self.child, self.position, self.relative)