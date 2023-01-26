import os
from hillclimber import HILL_CLIMBER

# for i in range(4):
#     os.system("python3.9 generate.py")
#     os.system("python3.9 simulate.py")

hc = HILL_CLIMBER()
hc.Evolve()
hc.Show_Best()
