import pybullet as p
import time

physicsClient = p.connect(p.GUI)

#Tells pybullet to read in the world described in box.sdf
p.loadSDF("box.sdf")

#insert for-loop that iterates 1000 times
for i in range(1000):
    p.stepSimulation()
    print("Start : %s" % time.ctime())
    time.sleep(1/60)
    print("End : %s" % time.ctime())

p.disconnect()