import numpy
import pyrosim.pyrosim as pyrosim
import os
import random as random
import time
import constants as c
import copy

height = 1
width = 1
length = 1
x = 0
y = 0
z = 0.5

class SOLUTION:
    def __init__(self, ID, links = [], joints = [], sensors = [], jointaxis = [], counter = 0):
        self.myID = ID
        self.links = links
        self.joints = joints
        self.sensors = sensors
        self.jointaxis = jointaxis
        self.weights = []
        self.counter = counter
        self.links_cubic = []
        self.joints_cubic = []

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Initialize_Body()
        self.Send_Brain()
        fitness = self.Run_Simulation(directOrGUI)
        return fitness

    def Wait_For_Simulation_To_End(self, directOrGUI):
        fileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fileName):
            time.sleep(0.01)
        f = open(fileName, "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm " + fileName)
        return self.fitness

    def Run_Simulation(self, directOrGUI):
        os.system(f"python3.9 simulate.py {directOrGUI} {str(self.myID)} &")
        fitness = self.Wait_For_Simulation_To_End(directOrGUI)
        return fitness

    def Create_World(self):
        #Tells pyrosim the name of the file where information about the world you're about to create 
        # should be stored. This world will currently be called box, because it will only contain a box.
        pyrosim.Start_SDF("world.sdf")
        
        pyrosim.Send_Cube(name="Box", pos=[x + 5,y + 5,z] , size=[width, length, height])
        #Tells pyrosim to close the sdf file.
        pyrosim.End()

    def Initialize_Body(self):
        pyrosim.Start_URDF(f"body{self.myID}.nndf")

        #Find the number of initial links
        numLinks = random.randint(c.linksMin, c.linksMax)

        #Create the starting link
        width = 1 #random.uniform(c.sizeMin, c.sizeMax)
        length = 1 #random.uniform(c.sizeMin, c.sizeMax)
        height = 1 #random.uniform(c.sizeMin, c.sizeMax)

        #Store the first link in self.links
        self.links = [self.Link("Link0", (width, length, height), faces_chosen=[])]
        #Set the absolute position and relative position of the first link
        self.links[0].position = (0, 0, 3)
        self.links[0].relative = (0, 0, 3)

        #Reinitialize everything!
        self.sensors = []
        self.jointaxis = []
        self.joints = []

        #Determine the link type and joint type by random
        self.sensors.append(random.choice([True, False]))
        self.jointaxis.append(random.randint(1, 3))

        #Intialize a counter that counts the number of successful links added
        self.counter = 1

        #Generate links and joints to complete the structure
        while len(self.links) != numLinks:
            self.Add_Link()

        #Function that puts everything in pyrosim
        self.Send_Links()

        pyrosim.End()

    def Add_Link(self):
        #Find a random link to connect it to 
        parentLink = random.choice(self.links)

        #Set link vars
        width = random.uniform(c.sizeMin, parentLink.size[0])
        length = random.uniform(c.sizeMin, parentLink.size[1])
        height = random.uniform(c.sizeMin, parentLink.size[2])

        px, py, pz = parentLink.position[0], parentLink.position[1],parentLink.position[2]
        pw, pl, ph = parentLink.size[0], parentLink.size[1], parentLink.size[2]

        #Create the new link
        newLink = self.Link("Link" + str(self.counter), (width, length, height), parent=parentLink)

        # Chose a face, if face does not exist, return
        face, sx, sy, sz = parentLink.choseFace()
        if not face:
            # print("\n\n\n\n cannot chose face")
            return
        
        #Use the face to determine the joint positions, if there are no joints it starts from the origin
        if parentLink.name == "Link0":
            jx, jy, jz = px + sx*pw/2, py + sy*pl/2, pz + sz*ph/2
            absolute = (jx, jy, jz)
        else: 
            parentJoint = [joint for joint in self.joints if joint.child == parentLink.name][0]
            absolute = (px + sx*pw/2, py + sy*pl/2, pz + sz*ph/2)
            jx, jy, jz = tuple(x - y for x, y in zip(absolute, parentJoint.position))
        
        #Create new joint
        newJoint = self.Joint(f"{parentLink.name}_{newLink.name}", parentLink.name, newLink.name, absolute, (jx, jy, jz))
        
        #Input the absolute and relative position of the links
        newLink.relative = (width * sx/2, length * sy/2, height * sz/2)
        newLink.position = (px + sx*(pw+width)/2, py + sy*(pl+length)/2, pz + sz*(ph+height)/2)
        newLink.faces_chosen = []

        #Check if it intersects with the floor, if it does, return
        if newLink.position[2] - newLink.size[2] < 0:
            # print("\n\n\n\n intersects w floor")
            return
        
        #Check for intersections with other links
        intersects = False
        for otherLink in self.links:
            if newLink.intersects(otherLink):
                intersects = True
        
        if intersects:
            # print("\n\n\n\n intersects with other links")
            return
        
        #If new link and joint is a successful addition
        #Append the new link to self.links
        self.links.append(newLink)
        #Append face to face chosen for parent and new link
        parentLink.faces_chosen.append(face)
        oppositeFace = face.replace("+", "_").replace("-", "+").replace("_", "-")
        newLink.faces_chosen.append(oppositeFace)
        #Append the new joint to self.joints
        self.joints.append(newJoint)
        #Add 1 to the counter number
        self.counter += 1

        #Determine the link type and joint type by random
        self.sensors.append(random.choice([True, False]))
        self.jointaxis.append(random.randint(1, 3))

    def Send_Links(self):
        for link in range(len(self.links)):
            if self.sensors[link]:
                pyrosim.Send_Cube(name = "Link" + str(link), pos=self.links[link].relative, size=self.links[link].size, colorString='<color rgba="0.164 0.776 0.478 1.0"/>', materialName='<material name="Green">')
            else:
                pyrosim.Send_Cube(name = "Link" + str(link), pos=self.links[link].relative, size=self.links[link].size, colorString='<color rgba="0.164 0.776 0.95 1.0"/>', materialName='<material name="Blue">')

        for joint in range(len(self.joints)):
            if self.jointaxis[joint] == 1:
                pyrosim.Send_Joint(name = self.joints[joint].name, parent = self.joints[joint].parent, child = self.joints[joint].child, type = "revolute", position = self.joints[joint].relative, jointAxis = "0 1 0")
            elif self.jointaxis[joint] == 2:
                pyrosim.Send_Joint(name = self.joints[joint].name, parent = self.joints[joint].parent, child = self.joints[joint].child, type = "revolute", position = self.joints[joint].relative, jointAxis = "1 0 0")
            else:
                pyrosim.Send_Joint(name = self.joints[joint].name, parent = self.joints[joint].parent, child = self.joints[joint].child, type = "revolute", position = self.joints[joint].relative, jointAxis = "0 0 1")

    def Send_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        self.weights = (numpy.random.rand(len(self.links), len(self.links) - 1) * 2) - 1

        sensorCounter = 0
        for index in range(len(self.links)):
            if self.sensors[index]:
                pyrosim.Send_Sensor_Neuron(name = str(sensorCounter), linkName = "Link" + str(index))
                sensorCounter += 1

        for joint in range(len(self.joints)):
            pyrosim.Send_Motor_Neuron(name = str(joint + sum(self.sensors)), jointName = self.joints[joint].name)

        for currentRow in range(sum(self.sensors)):
            for currentColumn in range(len(self.joints)):
                pyrosim.Send_Synapse(sourceNeuronName = str(currentRow), targetNeuronName = str(currentColumn + sum(self.sensors)), weight = self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        self.Create_World()

        #Choice 1: Add, remove or change sensor/joint type
        choice1 = random.choice(["add", "remove", "change"])

        #If there is only one link left, you cannot remove
        if len(self.links) <= 2:
            choice1 = random.choice(["add", "change"])

        if choice1 == 'add':
            self.Add_Link()
        elif choice1 == 'remove':
            self.Remove_Link()
        else:
            choice2 = random.choice(["type", "size"])
            if choice2 == "type":
                self.Change_Type()
            else:
                self.Change_Size()

        #Start a new body file
        pyrosim.Start_URDF(f"body{self.myID}.nndf")
        self.Send_Links()
        pyrosim.End()

        #Start a new brain file
        self.Send_Brain()

        #Start the baby's simulation
        fitness = self.Run_Simulation("DIRECT")
        return fitness
        # for link in self.links:
        #     print(link.position, link.relative)

        # for joint in self.joints:
        #     print(joint.position, joint.relative)

    def Change_Type(self):
        #Choose if we are changing link or joint
        linkOrjoint = random.choice(["link", "joint"])
        #Change link from sensored/unsensored to the opposite
        if linkOrjoint == "link":
            changedLink = random.choice(range(len(self.links)))
            self.sensors[changedLink] = not self.sensors[changedLink]
        #Change joint to a new type
        else:
            changedJoint = random.choice(range(len(self.joints)))
            axes = [1, 2, 3]
            leftoverAxes = [axis for axis in axes if axis != self.jointaxis[changedJoint]]
            self.jointaxis[changedJoint] = random.choice(leftoverAxes)

    def Change_Size(self):

        #If we are in cubic world just make Change_Size(return) :)
        return
    
        #Choose a random link, make sure that the link is connected to one thing
        intersects = True
        while intersects:
            found = False
            while not found:
                changeLink = random.choice(range(len(self.links)))
                # print("\n\n\n\n cannot find it yet")
                if len(self.links[changeLink].faces_chosen) == 1 and changeLink != 0:
                    found = True
            
            parentLink = self.links[changeLink].parent

            #Set link vars
            width = random.uniform(c.sizeMin, parentLink.size[0])
            length = random.uniform(c.sizeMin, parentLink.size[1])
            height = random.uniform(c.sizeMin, parentLink.size[2])

            # #Set link vars
            # width = random.uniform(c.sizeMin, c.sizeMax)
            # length = random.uniform(c.sizeMin, c.sizeMax)
            # height = random.uniform(c.sizeMin, c.sizeMax)

            #Change the size of the links
            self.links[changeLink].size = (width, length, height)
            oldRelPosition = self.links[changeLink].relative
            oldAbsPosition = self.links[changeLink].position
            newRelPosition = ()
            newAbsPosition = ()
            for idx, pos in enumerate(oldRelPosition):
                if pos > 0:
                    newRelPosition += (self.links[changeLink].size[idx]/2,)
                    newAbsPosition += (self.links[changeLink].size[idx]/2 - oldAbsPosition[idx],)
                elif pos < 0:
                    newRelPosition += (-self.links[changeLink].size[idx]/2,)
                    newAbsPosition += (-self.links[changeLink].size[idx]/2 - oldAbsPosition[idx],)
                else:
                    newRelPosition += (oldRelPosition[idx],)
                    newAbsPosition += (oldAbsPosition[idx],)
            self.links[changeLink].relative = newRelPosition
            self.links[changeLink].position = newAbsPosition

            #Give a list of other links
            otherLinks = self.links[:changeLink] + self.links[changeLink + 1:]

            for otherLink in otherLinks:
                if self.links[changeLink].intersects(otherLink):
                    intersects = False

    def Remove_Link(self):
        #Choose a random link, make sure that the link is connected to one thing
        found = False
        while not found:
            delLink = random.choice(range(len(self.links)))
            if len(self.links[delLink].faces_chosen) == 1 and delLink != 0:
                found = True
                self.counter -= 1

        #Remove it from the faces chosen of the parent joint
        for link in self.links:
            for joint in self.joints:
                if joint.child == self.links[delLink].name:
                    if joint.parent == link.name:
                        link.faces_chosen.pop(-1)

        #Delete that link from self.links and self.joints
        for idx, joint in enumerate(self.joints):
            if joint.child == self.links[delLink].name:
                del self.joints[idx]
                del self.links[delLink]
                del self.sensors[delLink]
                del self.jointaxis[idx]

        #Change the link names
        for idx in range(delLink, len(self.links)):
            oldName = self.links[idx].name
            newName = "Link" + str(idx)
            self.links[idx].name = newName
            #Change the joint names
            for idx, joint in enumerate(self.joints):
                if joint.parent == oldName:
                    joint.parent = f"{newName}"
                    joint.name = f"{newName}_{joint.child}"
                if joint.child == oldName:
                    joint.child = f"{newName}"
                    joint.name = f"{joint.parent}_{newName}"
        
    def Set_ID(self, ID):
        self.myID = ID

    # Declaring new classes
    class Link:
        def __init__(self, name, size, position = None, relative = None, faces_chosen = [], parent = None):
            self.name = name
            self.size = size
            self.position = position
            self.relative = relative
            self.faces_chosen = faces_chosen
            self.parent = parent
        
        # def __str__(self):
        #     return "{}: position={}, relative={}, size={} \n".format(self.name, self.position, self.relative, self.size)
        
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
                # print("\n\n\n\n faces chosen is 6")
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


        

    