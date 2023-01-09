import pyrosim.pyrosim as pyrosim

#Tells pyrosim the name of the file where information about the world you're about to create 
# should be stored. This world will currently be called box, because it will only contain a box.
pyrosim.Start_SDF("box.sdf")

#Stores a box with initial position x=0, y=0, z=0.5, and height, length and width all 
# equal to 1 meter, in box.sdf.
height = 3
width = 2
length = 1
pyrosim.Send_Cube(name="Box", pos=[0,0,0.5] , size=[length,width,height])

#Tells pyrosim to close the sdf file.
pyrosim.End()