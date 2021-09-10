"""
Predator Prey - Agent Based Code (PredPrey-ABC)
"""
from random import choice# randint, uniform, choice, random, gauss
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import log
import numpy as np
from tqdm import tqdm

# Parameters and functions ---

#from parameters import *

############------------------------------------#
# SETTINGS #------------------------------------#
############------------------------------------#

SAVE = False
PLOT = True
# number of levels
LEVELS = 2 # !!! IMPORTANT !!! IT CAN ONLY BE 2 OR 3

# Classes and functions definitions ---

class Agent:

    def __init__(self, species, energy, metabolism, i, j):
        self.energy = energy
        self.species = species
        self.metabolism = metabolism
        self.i, self.j = i, j

    # def move(self, grid_size):
    #     if FC:
    #         new_i, new_j = np.random.randint(grid_size, size = 2)
    #     else:
    #         i, j = self.i, self.j
    #         ic, jc = np.random.randint(low = -1, high = 2, size = 2)
    #         new_i = (ic + i) % grid_size
    #         new_j = (jc + j) % grid_size
    #     self.i, self.j = new_i, new_j

class Cell:

    def __init__(self, grass=1):
        self.resources = grass
        self.local_population = {'hare' : [], 'wolf' : [], 'human' : []}

class Grid:

    def __init__(self, size, FC):
        self.size = size
        self.FC = FC
        self.levels = LEVELS
        self.population = {'hare' : [], 'wolf' : [], 'human' : []}

        self.density = {'hare' : [], 'wolf' : [], 'human' : []}
        self.energy = {'hare' : [], 'wolf' : [], 'human' : []}
        self.metabolism = {'hare' : [], 'wolf' : [], 'human' : []}
        self.grass = []
        # 2D grid
        self.grid = [[Cell() for i in range(self.size)] for j in range(self.size)]


    def place_agents(self, counts_dict, energy_dict, metabolism_dict):

        for species in ['hare', 'wolf', 'human']:

            positions = np.random.randint(self.size, size = (counts_dict[species], 2))

            for i in range(counts_dict[species]):
                agent = Agent(species, energy_dict[species], metabolism_dict[species], positions[i,0], positions[i,1])
                self.population[species].append(agent)
                self.grid[agent.i][agent.j].local_population[species].append(agent)

    def agents_starve(self):
        for species in ['hare', 'wolf', 'human']:
            #self.population[species] = [agent for agent in self.population[species] if agent.energy > 0]
            agents_to_starve = (agent for agent in self.population[species] if agent.energy <= 0)
            for agent in agents_to_starve:
                self.population[species].remove(agent)
                self.grid[agent.i][agent.j].local_population[species].remove(agent)

    def grass_grows(self, grass_growth_rate):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j].resources += grass_growth_rate

    def agents_move(self):
        for species in ['hare', 'wolf', 'human']:
            pop_size = len(self.population[species])
            if self.FC:
                delta = np.random.randint(grid_size, size = (pop_size, 2))
            else:
                delta = np.random.randint(low = -1, high = 2, size = (pop_size, 2))

            for k in range(pop_size):
                agent = self.population[species][k]
                self.grid[agent.i][agent.j].local_population[species].remove(agent)
                agent.i, agent.j = (agent.i + delta[k,0]) % self.size, (agent.j + delta[k,1]) % self.size
                self.grid[agent.i][agent.j].local_population[species].append(agent)

    def immigration(self, energy_dict, metabolism_dict):
        active_species = ['hare', 'wolf', 'human'] if self.levels == 3 else ['hare', 'wolf']
        for species in active_species:
            if len(self.population[species]) == 0:

                immigrant = Agent(species, energy_dict[species], metabolism_dict[species], np.random.randint(self.size), np.random.randint(self.size))
                self.population[species].append(immigrant)
                self.grid[immigrant.i][immigrant.j].local_population[species].append(immigrant)

    def agents_reproduce(self, reproduction_threshold, mutation_rate):
        for species in ['hare', 'wolf', 'human']:
            agents_to_reproduce = (agent for agent in self.population[species] if agent.energy >= reproduction_threshold)
            for parent in agents_to_reproduce:
                i,j = parent.i, parent.j
                offspring = Agent(species = parent.species, energy = parent.energy/2, metabolism = mutate(parent.metabolism, mutation_rate), i = parent.i, j = parent.j)
                self.grid[i][j].local_population[species].append(offspring)
                self.population[species].append(offspring)
                parent.energy = parent.energy/2
                #print('reproduction', parent.species)

    def hares_graze(self):
        for hare in self.population['hare']:
            i, j = hare.i, hare.j
            #hares_here = [h for h in self.population['hare'] if h.i == i and h.j == j]
            hares_here = self.grid[i][j].local_population['hare']
            tmp_eat = self.grid[i][j].resources /len(hares_here)
            hare.energy += tmp_eat
            self.grid[i][j].resources -= tmp_eat
            hare.energy -= 1 + hare.metabolism

    def wolves_eat(self, predation_efficiency):
        for wolf in self.population['wolf']:
            i, j = wolf.i, wolf.j
            hares_here = self.grid[i][j].local_population['hare']
            if len(hares_here) > 0:
                tmp_hare = choice(hares_here)
                if np.random.random() < wolf.metabolism/tmp_hare.metabolism:
                    wolf.energy += predation_efficiency # tmp_hare.energy
                    self.grid[i][j].local_population['hare'].remove(tmp_hare)
                    self.population['hare'].remove(tmp_hare)
            wolf.energy -= 1 + wolf.metabolism

    def humans_eat(self, predation_efficiency):
        for human in self.population['human']:
            i, j = human.i, human.j
            #wolves_here = [w for w in self.population['wolf'] if w.i == i and w.j == j]
            wolves_here = self.grid[i][j].local_population['wolf']
            if len(wolves_here) > 0:
                tmp_wolf = choice(wolves_here)
                if np.random.random() < human.metabolism/tmp_wolf.metabolism:
                    human.energy += predation_efficiency #tmp_wolf.energy #
                    self.grid[i][j].local_population['wolf'].remove(tmp_wolf)
                    self.population['wolf'].remove(tmp_wolf)

            human.energy -= 1 + human.metabolism

    def evolve(self, energy_dict, metabolism_dict, reproduction_threshold, grass_growth_rate, immigration, mutation_rate, predation_efficiency):
        if immigration:
            self.immigration(energy_dict, metabolism_dict)
        self.agents_starve()
        self.grass_grows(grass_growth_rate)
        self.hares_graze()
        self.agents_reproduce(reproduction_threshold, mutation_rate)
        self.wolves_eat(predation_efficiency)
        self.humans_eat(predation_efficiency)
        self.agents_move()

    def save_density(self):
        area = self.size**2
        for species in ['hare', 'wolf', 'human']:
            self.density[species].append(len(self.population[species])/area)

    def save_energy(self):
        for species in ['hare', 'wolf', 'human']:
            self.energy[species].append(np.mean([agent.energy for agent in self.population[species]]))

    def save_metabolism(self):
        for species in ['hare', 'wolf', 'human']:
            self.metabolism[species].append(np.mean([agent.metabolism for agent in self.population[species]]))

    def save_grass_density(self):
        area = self.size**2
        tmp_grass = 0
        for i in range(self.size):
            for j in range(self.size):
                tmp_grass += self.grid[i][j].resources
        self.grass.append(tmp_grass/area)

    def time_avg(self):
        self.time_avg = {}

        for species in ['hare', 'wolf', 'human']:
            total_duration = len(self.density[species])
            self.time_avg[species] = np.mean(self.density[species][round(total_duration/2):])
        return self.time_avg

    def plot(self):
            plt.figure(figsize=(15,15))
            plt.subplot(311)
            plt.plot(self.density['hare'])
            plt.plot(self.density['wolf'])
            plt.plot(self.density['human'])
            plt.ylabel('density')

            # plt.subplot(311)
            # plt.plot(self.energy['hare'])
            # plt.plot(self.energy['wolf'])
            # plt.plot(self.energy['human'])
            # plt.ylabel('energy')

            plt.subplot(312)
            plt.plot(self.metabolism['hare'])
            plt.plot(self.metabolism['wolf'])
            plt.plot(self.metabolism['human'])
            plt.ylabel('metabolism')

            plt.subplot(313)
            plt.plot(self.grass)
            plt.ylabel('grass')
            plt.show()

def mutate(parent_metabolism, mutation_rate):
    new_metabolism = np.random.normal(loc = parent_metabolism, scale = mutation_rate)
    if new_metabolism > 0:
        return new_metabolism
    else:
        return 0.0002*1



def run(grid_size, FC, nb_steps, counts_dict, energy_dict, metabolism_dict, reproduction_threshold, grass_growth_rate, immigration, mutation_rate, predation_efficiency):
    # initializations

    # create grid
    sim_grid = Grid(grid_size, FC)

    # put the guys
    sim_grid.place_agents(counts_dict, energy_dict, metabolism_dict)

    # evolve
    for step in tqdm(range(nb_steps)):
        sim_grid.evolve(energy_dict, metabolism_dict, reproduction_threshold, grass_growth_rate, immigration, mutation_rate, predation_efficiency)
        sim_grid.save_density()
        sim_grid.save_energy()
        sim_grid.save_metabolism()
        sim_grid.save_grass_density()

        if min([len(pop) for pop in sim_grid.population]) == 0:
            break

    return sim_grid
