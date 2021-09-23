from defs_diagnostics import *
import multiprocess as mp
import matplotlib.pyplot as plt
%matplotlib inline
from numpy import arange

sim = run(
    grid_size=25,
    FC=False,
    nb_steps=5000,
    counts_dict={
        'hare': 100,
        'wolf': 100,
        'human': 0
    },
    energy_dict={
        'hare': 100,
        'wolf': 100,
        'human': 100
    },
    metabolism_dict={
        'hare': 5,
        'wolf': 5,
        'human': 1
    },
    reproduction_threshold = 60,
    predation_efficiency = 10,
    grass_growth_rate=50,
    immigration=False,
    mutation_rate=0.1
)

sim.plot()

plt.figure(figsize=(20,5))
plt.plot(sim.density['hare'])
plt.plot(sim.density['wolf'])
plt.plot(sim.density['human'])
plt.ylabel('density')
plt.savefig('density.png')


x_lifetime, y_lifetime = zip(*sorted(normalized_dictionary(dict(sim.lifetime['wolf'])).items()))
plt.plot(x_lifetime, y_lifetime)
plt.xscale('log')
plt.show()

np.mean(sim.metabolism['hare'][10000:])
np.mean(sim.metabolism['wolf'][10000:])





'''
if __name__ == '__main__':

    with mp.Pool(mp.cpu_count()) as pool:
        averages = pool.map(lambda l: run(
            grid_size=30,
            FC=False,
            nb_steps=10000,
            counts_dict={
                'hare': 100,
                'wolf': 100,
                'human': 0
            },
            energy_dict={
                'hare': 100,
                'wolf': 100,
                'human': 100
            },
            metabolism_dict={
                'hare': 1,
                'wolf': 1,
                'human': 1
            },
            reproduction_threshold = 50,
            predation_efficiency = 10,
            grass_growth_rate=l,
            immigration=False,
            mutation_rate=0.05
        ).time_avg(), arange(1, 100, 100/mp.cpu_count()))

        wolf_to_hare = [avg['wolf'] / avg['hare'] for avg in averages]
        human_to_wolfs = [avg['human'] / avg['wolf'] for avg in averages]
    plt.plot(wolf_to_hare)
    plt.plot(human_to_wolfs)
    averages
    plt.loglog(wolf_to_hare)
'''
