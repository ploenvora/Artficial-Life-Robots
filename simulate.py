import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

#Set gravity
p.setGravity(0,0,-9.8)

#Adding a floor
planeId = p.loadURDF("plane.urdf")

#Adding a robot
robotId = p.loadURDF("body.urdf")

#Tells pybullet to read in the world described in box.sdf
p.loadSDF("world.sdf")

#insert for-loop that iterates 1000 times
pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)
for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg") # backleg sensors
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg") # frontleg sensors
    #print("Start : %s" % time.ctime())
    time.sleep(1/60)
    #print("End : %s" % time.ctime())

print(backLegSensorValues)
print(frontLegSensorValues)
numpy.save("backlegsensorvalues.npy", backLegSensorValues)
numpy.save("frontlegsensorvalues.npy", frontLegSensorValues)

p.disconnect()


