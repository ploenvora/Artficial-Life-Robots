from simulation import SIMULATION
import sys
directOrGUI = sys.argv[1]

simulation = SIMULATION(directOrGUI)
simulation.Run()
simulation.Get_Fitness()
#python3 simulate.py DIRECT
#python3 simulate.py GUI
