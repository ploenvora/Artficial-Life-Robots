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

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Select()
        #self.Print()
    
    def Spawn(self):
        self.children = {}
        for key in self.parents.keys():
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID = self.nextAvailableID + 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Select(self):
        for key in self.parents.keys():
            if self.parents[key].fitness > self.children[key].fitness:
                self.parents[key] = self.children[key]

    def Print(self):
        for key in self.parents.keys():
            print("\n", self.parents[key].fitness, self.children[key].fitness, "\n")

    def Show_Best(self):
        best_fitness = 1000
        for key in self.parents.keys():
            print("\nparent fitness:", self.parents[key].fitness, "\n")
            print("\nbest fitness:", best_fitness, "\n")
            if self.parents[key].fitness < best_fitness:
                best_fitness = self.parents[key].fitness
                best_parent = self.parents[key]
        print("\nfinal best fitness:", best_fitness, "\n")
        best_parent.Start_Simulation("GUI")

    def Evaluate(self, solutions):
        for item in solutions.values():
            item.Start_Simulation("DIRECT")

        for item in solutions.values():
            item.Wait_For_Simulation_To_End("DIRECT")
