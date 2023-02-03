import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random 

# number of steps
steps = 1000

# back leg
forceBack = 100000
amplitudeBack = numpy.pi
frequencyBack = 20
phaseOffsetBack = 0
motorCommandBack = amplitudeBack * numpy.sin(frequencyBack * numpy.arange(1000) * (numpy.pi/499.5) + phaseOffsetBack)

# front leg
forceFront = 500
amplitudeFront = numpy.pi
frequencyFront = 20
phaseOffsetFront = numpy.pi/4
motorCommandFront = amplitudeFront * numpy.sin(frequencyFront * numpy.arange(1000) * (numpy.pi/499.5) + phaseOffsetFront)

numberOfGenerations  = 10
populationSize = 10

numSensorNeurons = 9
numMotorNeurons = 8
motorJointRange = 0.3

ball = 1
pins = 10
