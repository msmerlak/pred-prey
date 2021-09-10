"""
Predator Prey - Agent Based Code (PredPrey-ABC)
"""
from random import choice
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

class Agent:

    def __init__(self, species, energy, metabolism):
        self.energy = energy
        self.species = species
        self.metabolism = metabolism
        self.energy = energy

class Ecosystem:

    def __init__(self, area, grass, counts_dict, energy_dict, metabolism_dict):
        self.species = counts_dict.keys()
        self.grass = grass
        self.population = {}

        for s in self.species:
            self.population[s] = [Agent(species = s, energy = energy_dict[s], metabolism = metabolism_dict[s]) for i in range(counts_dict[s])]
        self.counts = {s: [counts_dict[s]] for s in self.species}
        self.counts['grass'] = [grass]
        self.mean_energy = {s: [energy_dict[s]] for s in self.species}
        self.mean_metabolism = {s: [metabolism_dict[s]] for s in self.species}

    def agents_starve(self):
        for s in self.species:
            agents_to_starve = (agent for agent in self.population[s] if agent.energy <= 0)
            for agent in agents_to_starve:
                self.population[s].remove(agent)

    def grass_grows(self, grass_growth_rate):
        self.grass += grass_growth_rate

    def agents_reproduce(self, reproduction_threshold, mutation_rate):
        for s in self.species:

            agents_to_reproduce = [agent for agent in self.population[s] if agent.energy >= reproduction_threshold]

            mutations = np.random.normal(scale=mutation_rate, size=len(agents_to_reproduce))

            for i in range(len(agents_to_reproduce)):
                parent = agents_to_reproduce[i]
                offspring = Agent(species=s, energy=parent.energy / 2,
                                  metabolism=max(0.002,parent.metabolism + mutations[i]))
                self.population[s].append(offspring)
                parent.energy = parent.energy / 2

    def herbivores_graze(self):
        herbivores = self.population[0]
        for herbivore in herbivores:
            if self.grass > 0:
                herbivore.energy += self.grass / len(herbivores)
                herbivore.energy -= 1 + herbivore.metabolism
                self.grass -= 1

    def predators_eat(self, area, predation_efficiency):
        for p in (s for s in self.species if s > 0):

            for pred in self.population[p]:
                pred.energy -= 1 + pred.metabolism

            predators = np.random.choice(self.population[p], size = min(len(self.population[p]), round(len(self.population[p])*len(self.population[p-1])/area)), replace=False)
            
            coin_flips = np.random.random(size=len(predators))

            for i in range(len(predators)):
                pred = predators[i]


                if len(self.population[p - 1]) == 0:
                    break

                prey = choice(self.population[p - 1])

                if coin_flips[i] < pred.metabolism / prey.metabolism:
                    self.population[p - 1].remove(prey)
                    pred.energy += predation_efficiency

    def immigration(self, energy_dict, metabolism_dict):
        for s in self.species:
            if len(self.population[s]) == 0:
                immigrant = Agent(species = s, energy=energy_dict[s], metabolism=metabolism_dict[s])
                self.population[s].append(immigrant)

    def evolve(self, area, energy_dict, metabolism_dict, reproduction_threshold, grass_growth_rate, immigration, mutation_rate, predation_efficiency):
        if immigration:
            self.immigration(energy_dict, metabolism_dict)
        self.agents_starve()
        self.grass_grows(grass_growth_rate)
        self.herbivores_graze()
        self.agents_reproduce(reproduction_threshold, mutation_rate)
        self.predators_eat(area, predation_efficiency)

    def save_counts(self):
        for s in self.species:
            self.counts[s].append(len(self.population[s]))
        self.counts['grass'].append(self.grass)

    def save_mean_energy(self):
        for s in self.species:
            self.mean_energy[s].append(np.mean([agent.energy for agent in self.population[s]]))

    def save_mean_metabolism(self):
        for s in self.species:
            self.mean_metabolism[s].append(np.mean([agent.metabolism for agent in self.population[s]]))

    def time_avg(self):
        self.time_avg = {}

        for s in self.species:
            total_duration = len(self.counts[s])
            self.time_avg[s] = np.mean(self.density[s][round(total_duration/2):])
        return self.time_avg

    def plot(self):
            plt.figure(figsize=(10,10))
            plt.subplot(311)
            plt.plot(self.counts[0])
            plt.plot(self.counts[1])
            plt.plot(self.counts[2])
            plt.ylabel('density')


            plt.subplot(312)
            plt.plot(self.mean_metabolism[0])
            plt.plot(self.mean_metabolism[1])
            plt.plot(self.mean_metabolism[2])
            plt.ylabel('metabolism')

            plt.subplot(313)
            plt.plot(self.counts['grass'])
            plt.ylabel('grass')
            plt.show()

def run(nb_steps, area, grass, counts_dict, energy_dict, metabolism_dict, reproduction_threshold, grass_growth_rate, immigration, mutation_rate, predation_efficiency):

    # create grid
    ecosystem = Ecosystem(area, grass, counts_dict, energy_dict, metabolism_dict)

    # evolve
    for step in tqdm(range(nb_steps)):
        ecosystem.evolve(area, energy_dict, metabolism_dict, reproduction_threshold,
                        grass_growth_rate, immigration, mutation_rate, predation_efficiency)
        ecosystem.save_counts()
        ecosystem.save_mean_energy()
        ecosystem.save_mean_metabolism()
        if immigration:
            ecosystem.immigration(energy_dict, metabolism_dict)
        elif min(ecosystem.counts.values()) == 0:
            break

    return ecosystem

if __name__ == '__main__':
    sim = run(
        area = 500,
        nb_steps=10000,
        grass = 500,
        counts_dict={
            0: 100,
            1: 20,
            2: 0
        },
        energy_dict={
            0: 50,
            1: 50,
            2: 50
        },
        metabolism_dict={
            0: 5,
            1: 1,
            2: 1
        },
        reproduction_threshold = 30,
        predation_efficiency = 10,
        grass_growth_rate=50,
        immigration=False,
        mutation_rate=.05
    )

    sim.plot()
