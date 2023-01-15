import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random as random

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
targetAngles = numpy.sin(numpy.arange(1000) * (numpy.pi/499.5)) * numpy.pi/4

# back leg
amplitudeBack = numpy.pi
frequencyBack = 100
phaseOffsetBack = 0
motorCommandBack = amplitudeBack * numpy.sin(frequencyBack * numpy.arange(1000) * (numpy.pi/499.5) + phaseOffsetBack)

# front leg
amplitudeFront = numpy.pi
frequencyFront = 100
phaseOffsetFront = numpy.pi/4
motorCommandFront = amplitudeFront * numpy.sin(frequencyFront * numpy.arange(1000) * (numpy.pi/499.5) + phaseOffsetFront)

#numpy.save("data/motorCommandBack.npy", motorCommandBack)
#numpy.save("data/motorCommandFront.npy", motorCommandFront)
#numpy.save("data/targetAngles.npy", targetAngles)
#exit()
for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg") # backleg sensors
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg") # frontleg sensors
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_BackLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = motorCommandBack[i],
        maxForce = 500)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_FrontLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = motorCommandFront[i],
        maxForce = 500)

    #print("Start : %s" % time.ctime())
    time.sleep(1/60)
    #print("End : %s" % time.ctime())

print(backLegSensorValues)
print(frontLegSensorValues)
numpy.save("backlegsensorvalues.npy", backLegSensorValues)
numpy.save("frontlegsensorvalues.npy", frontLegSensorValues)

p.disconnect()


