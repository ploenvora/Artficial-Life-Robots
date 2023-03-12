import os
import time
from hillclimber import HILL_CLIMBER
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c
import random

# for i in range(4):``
#     os.system("python3.9 generate.py")
#     os.system("python3.9 simulate.py")

#### UNCOMMENT THIS
for idx in range(1):
    random.seed(idx + 1)
    phc = PARALLEL_HILL_CLIMBER(run = idx + 1)
    phc.population = c.populationSize
    phc.Evolve()
    # phc.Show_Best()
    time.sleep(12)
    # os.system("rm *brain*.nndf")
    # os.system("rm *body*.nndf")
    if not os.path.exists(f"FINALRUNHIER{(idx + 1)}"):
        os.makedirs(f"FINALRUNHIER{(idx + 1)}")
    for file in os.listdir("."):
        if "nndf" in file:
            os.system(f"mv {file} FINALRUNHIER{(idx + 1)}/")
#### UNCOMMENT THIS

# for file in os.listdir("."):
#     if "nndf" in file:
#         os.system(f"mv {file} Run6/")

# random.seed(3)
# phc = PARALLEL_HILL_CLIMBER(run = 2)
# phc.population = c.populationSize
# phc.Evolve()
# phc.Show_Best()
# time.sleep(12)

# os.system(f"python3.9 simulate.py GUI {str(0)} &")