import pybullet as p
import time
import pybullet_data

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

#Set gravity
p.setGravity(0,0,-9.8)

#Adding a floor
planeId = p.loadURDF("plane.urdf")

#Tells pybullet to read in the world described in box.sdf
p.loadSDF("box.sdf")

#insert for-loop that iterates 1000 times
for i in range(1000):
    p.stepSimulation()
    print("Start : %s" % time.ctime())
    time.sleep(1/60)
    print("End : %s" % time.ctime())

p.disconnect()