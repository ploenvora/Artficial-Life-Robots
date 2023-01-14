import numpy as numpy
import matplotlib.pyplot

backLegSensorValues = numpy.load("data/backlegsensorvalues.npy")
frontLegSensorValues = numpy.load("data/frontlegsensorvalues.npy")

matplotlib.pyplot.plot(backLegSensorValues, label = 'Back Leg', linewidth = 2)
matplotlib.pyplot.plot(frontLegSensorValues, label = 'Front Leg')
matplotlib.pyplot.legend()
matplotlib.pyplot.show()
