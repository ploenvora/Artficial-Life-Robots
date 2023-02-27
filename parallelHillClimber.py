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
        
        # print("\n\npopulation size:", c.populationSize)
        for item in range(self.population):
            # print("\ninitialized once\n")
            # Creates a solution for each parent for the population size
            self.parents[item] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        # print("\nend of phc initialization\n")

    def Evolve(self):
        # print("\nstart of evolve\n")
        self.Evaluate(self.parents)
        #For each generations, it evolves for one generation
        for currentGeneration in range(self.generation):
            self.Evolve_For_One_Generation(currentGeneration)
        # print("\nend of evolved\n")

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
            #MUTATE IS RUNNING
            # print("\n\nmutate is running\n\n")
            child.Mutate()

    def Select(self):
        #print(self.parent.fitness, self.child.fitness)
        # print("\nselection function starts")
        for key in self.parents.keys():
            # print("\nkey:", key, "\nparent solutionID:", self.parents[key].myID, "\nchild solutionID:", self.children[key].myID)
            # print("\nparent fitness:", self.parents[key].fitness, "\nchild fitness:", self.children[key].fitness)
            if self.parents[key].fitness > self.children[key].fitness:
                self.parents[key] = self.children[key]

    def Print(self):
        # Modify Print() to iterate through the keys in self.parents, and print the fitness of self.parents[key] and then the fitness of self.children[key] on the same line.
        # Right at the start and right at the end of Print(), print an empty line. This will separate the two rows of parent/child fitnesses from the next two rows of parent/child fitness values in the next generation.
        for key in self.parents.keys():
            print("\n", self.parents[key].fitness, self.children[key].fitness, "\n")
        #print("\n", self.parent.fitness, self.child.fitness)

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
            item.Start_Simulation("DIRECT")
    
    def Save_Best(self, currentGeneration):
        best_fitness = float('inf')
        for key in self.parents.keys():
            if self.parents[key].fitness < best_fitness:
                best_fitness = self.parents[key].fitness
        self.results.append((currentGeneration, best_fitness))
        with open(f"results_{self.population}_{self.generation}_{self.run}.csv", mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.results)

        

