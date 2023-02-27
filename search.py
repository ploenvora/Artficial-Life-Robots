import os
import time
from hillclimber import HILL_CLIMBER
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c
import random

# for i in range(4):``
#     os.system("python3.9 generate.py")
#     os.system("python3.9 simulate.py")

# for idx in range(10, 20):
#     random.seed(idx + 1)
#     phc = PARALLEL_HILL_CLIMBER(run = idx + 1)
#     phc.population = c.populationSize
#     phc.Evolve()
#     phc.Show_Best()
#     time.sleep(12)
#     # os.system("rm *brain*.nndf")
#     # os.system("rm *body*.nndf")
#     if not os.path.exists(f"Run{(idx + 1)}"):
#         os.makedirs(f"NewRun{(idx + 1)}")
#     for file in os.listdir("."):
#         if "nndf" in file:
#             os.system(f"mv {file} NewRun{(idx + 1)}/")

# for file in os.listdir("."):
#     if "nndf" in file:
#         os.system(f"mv {file} Run6/")

phc = PARALLEL_HILL_CLIMBER(run = 101)
phc.population = c.populationSize
phc.Evolve()
phc.Show_Best()


