import pyrosim.pyrosim as pyrosim

#Tells pyrosim the name of the file where information about the world you're about to create 
# should be stored. This world will currently be called box, because it will only contain a box.
pyrosim.Start_SDF("boxes.sdf")

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
#pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[width, length, height])
#pyrosim.Send_Cube(name="Box2", pos=[x2,y2,z2] , size=[width, length, height])

x_change = 0

for i in range(5):
    y_change = 0
    for i in range(5):
        z_change = 0.5
        size_change = 1
        for i in range(10):
            pyrosim.Send_Cube(name="Box", pos=[x_change,y_change,z_change] , size=[size_change, size_change, size_change])
            z_change = z_change + 1
            size_change = size_change * 0.9
        y_change = y_change + 1
    x_change = x_change + 1

#Tells pyrosim to close the sdf file.
pyrosim.End()