from solution import SOLUTION
import constants as c
import copy as copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.parents = {}
        self.nextAvailableID = 0
        for item in range(c.populationSize):
            self.parents[item] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
        #     # if currentGeneration == 0:
        #     #     self.parent.Evaluate("GUI")

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()
    
    def Spawn(self):
        self.children = {}
        for key in self.parents.keys():
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1
        # self.child = copy.deepcopy(self.parent)
        # self.child.Set_ID(self.nextAvailableID)
        # self.nextAvailableID = self.nextAvailableID + 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Select(self):
        #print(self.parent.fitness, self.child.fitness)
        for key in self.parents.keys():
            if self.parents[key].fitness > self.children[key].fitness:
                self.parents[key] = self.children[key]

    def Print(self):
        # Modify Print() to iterate through the keys in self.parents, and print the fitness of self.parents[key] and then the fitness of self.children[key] on the same line.
        # Right at the start and right at the end of Print(), print an empty line. This will separate the two rows of parent/child fitnesses from the next two rows of parent/child fitness values in the next generation.
        for key in self.parents.keys():
            print("\n", self.parents[key].fitness, self.children[key].fitness, "\n")
        #print("\n", self.parent.fitness, self.child.fitness)

    def Show_Best(self):
        for key in self.parents.keys():
            best_fitness = 200
            if self.parents[key].fitness < best_fitness:
                best_fitness = self.parents[key].fitness
                best_parent = self.parents[key]
        best_parent.Start_Simulation("GUI")
        #self.parent.Evaluate("GUI")

    def Evaluate(self, solutions):
        for item in solutions.values():
            item.Start_Simulation("DIRECT")

        for item in solutions.values():
            item.Wait_For_Simulation_To_End("DIRECT")
            #print(item.fitness)
