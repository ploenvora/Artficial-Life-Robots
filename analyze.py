import numpy as numpy
import matplotlib.pyplot

backLegSensorValues = numpy.load("data/backlegsensorvalues.npy")
frontLegSensorValues = numpy.load("data/frontlegsensorvalues.npy")
targetAngles = numpy.load("data/targetAngles.npy")
motorCommand = numpy.load("data/motorCommand.npy")
motorCommandBack = numpy.load("data/motorCommandBack.npy")
motorCommandFront = numpy.load("data/motorCommandFront.npy")

# matplotlib.pyplot.plot(backLegSensorValues, label = 'Back Leg', linewidth = 2)
# matplotlib.pyplot.plot(frontLegSensorValues, label = 'Front Leg')
# matplotlib.pyplot.legend()
matplotlib.pyplot.plot(motorCommandBack, label = 'Back Leg')
matplotlib.pyplot.plot(motorCommandFront, label = 'Front Leg')
matplotlib.pyplot.legend()
matplotlib.pyplot.show()
