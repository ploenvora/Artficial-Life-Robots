import pybullet as p
import time

physicsClient = p.connect(p.GUI)

#insert for-loop that iterates 1000 times
for i in range(1000):
    p.stepSimulation()
    print("Start : %s" % time.ctime())
    time.sleep(5)
    print("End : %s" % time.ctime())

p.disconnect()