from solution import SOLUTION
import constants as c
import copy as copy
import os
import csv

class PARALLEL_HILL_CLIMBER:
    def __init__(self, run):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.parents = {}
        self.nextAvailableID = 0
        self.results = []
        self.population = c.populationSize
        self.generation = c.numberOfGenerations
        self.run = run
        self.fitness = []
        
        for item in range(self.population):
            # Creates a solution for each parent for the population size
            self.parents[item] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        #For each generations, it evolves for one generation
        for currentGeneration in range(self.generation):
            self.Evolve_For_One_Generation(currentGeneration)

    def Evolve_For_One_Generation(self, currentGeneration):
        # Each parent spawns, mutates
        self.Spawn()
        self.Mutate()
        #self.Evaluate(self.children)
        #self.Print()
        self.Select()
        self.Save_Best(currentGeneration)
    
    def Spawn(self):
        self.children = {}
        for key in self.parents.keys():
            #deep copy doesn't copy the exact version
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    # We need to edit this function
    # For each child solution, mutate is called
    def Mutate(self):
        for child in self.children.values():
            fitness = child.Mutate()
            self.fitness.append((child.myID, fitness))

    def Select(self):
        for key in self.parents.keys():
            if self.parents[key].fitness > self.children[key].fitness:
                self.parents[key] = self.children[key]

    def Print(self):
        # Modify Print() to iterate through the keys in self.parents, and print the fitness of self.parents[key] and then the fitness of self.children[key] on the same line.
        # Right at the start and right at the end of Print(), print an empty line. This will separate the two rows of parent/child fitnesses from the next two rows of parent/child fitness values in the next generation.
        for key in self.parents.keys():
            print("\n", self.parents[key].fitness, self.children[key].fitness, "\n")

    def Show_Best(self):
        best_fitness = float('inf')
        for key in self.parents.keys():
            if self.parents[key].fitness < best_fitness:
                best_fitness = self.parents[key].fitness
                best_parent = self.parents[key]
        print("\nstarting show best\n\nthe best fitness:", best_fitness)
        best_parent.Run_Simulation("GUI")

    def Evaluate(self, solutions):
        for item in solutions.values():
            fitness = item.Start_Simulation("DIRECT")
            self.fitness.append((item.myID, fitness))

    def Save_Best(self, currentGeneration):
        best_fitness = float('inf')
        for key in self.parents.keys():
            if self.parents[key].fitness < best_fitness:
                best_fitness = self.parents[key].fitness
                best_parent = self.parents[key]
        self.results.append((best_parent.myID, currentGeneration, best_fitness))
        with open(f"hier_results_{self.population}_{self.generation}_{self.run}.csv", mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.results)
        with open(f"hier_compiled_results_{self.population}_{self.generation}_{self.run}.csv", mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.fitness)

        

