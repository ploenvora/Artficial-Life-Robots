import pyrosim.pyrosim as pyrosim

#Stores a box with initial position x=0, y=0, z=0.5, and height, length and width all
# equal to 1 meter, in box.sdf.
height = 1
width = 1
length = 1
x = 0
y = 0
z = 0.5
x2 = 1
y2 = 0
z2 = 1.5

def Create_World():
    #Tells pyrosim the name of the file where information about the world you're about to create 
    # should be stored. This world will currently be called box, because it will only contain a box.
    pyrosim.Start_SDF("world.sdf")
    
    pyrosim.Send_Cube(name="Box", pos=[x + 10,y + 10,z] , size=[width, length, height])
    #pyrosim.Send_Cube(name="Box2", pos=[x2,y2,z2] , size=[width, length, height])

    #Tells pyrosim to close the sdf file.
    pyrosim.End()

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5] , size=[width, length, height])
    pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1,0,1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5] , size=[width, length, height])
    pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2,0,1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5] , size=[width, length, height])
    pyrosim.End()

Create_World()
Create_Robot()