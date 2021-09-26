from with_space import *
import multiprocess as mp
import matplotlib.pyplot as plt
%matplotlib inline
from numpy import arange

sim = run(
    grid_size=100,
    FC=False,
    nb_steps=1000,
    counts_dict={
        'hare': 100,
        'wolf': 100,
        'human': 0
    },
    energy_dict={
        'hare': 50,
        'wolf': 50,
        'human': 50
    },
    metabolism_dict={
        'hare': 5,
        'wolf': 1,
        'human': 1
    },
    reproduction_threshold = 30,
    predation_efficiency = 10,
    grass_growth_rate=20,
    immigration=False,
    mutation_rate=.1
)

sim.plot()

if __name__ == '__main__':

    #without evolution
    with mp.Pool(mp.cpu_count()) as pool:
        no_ev = pool.map(lambda l: [l, run(
            grid_size=20,
            FC=False,
            nb_steps=5000,
            counts_dict={
                'hare': 100,
                'wolf': 100,
                'human': 0
            },
            energy_dict={
                'hare': 50,
                'wolf': 50,
                'human': 50
            },
            metabolism_dict={
                'hare': 5,
                'wolf': 1,
                'human': 1
            },
            reproduction_threshold = 30,
            predation_efficiency = 10,
            grass_growth_rate=l,
            immigration=False,
            mutation_rate=0.0
        ).time_avg()], arange(1, 200, 200/mp.cpu_count()))
    plt.plot([av[0] for av in no_ev],[av[1]['wolf']/av[1]['hare'] for av in no_ev])
    #with evolution
    with mp.Pool(mp.cpu_count()) as pool:
        ev = pool.map(lambda l: [l, run(
            grid_size=20,
            FC=False,
            nb_steps=5000,
            counts_dict={
                'hare': 100,
                'wolf': 100,
                'human': 0
            },
            energy_dict={
                'hare': 50,
                'wolf': 50,
                'human': 50
            },
            metabolism_dict={
                'hare': 5,
                'wolf': 1,
                'human': 1
            },
            reproduction_threshold = 30,
            predation_efficiency = 10,
            grass_growth_rate=l,
            immigration=False,
            mutation_rate=0.05
        ).time_avg()], arange(1, 200, 200/mp.cpu_count()))
    plt.plot([av[0] for av in ev],[av[1]['wolf']/av[1]['hare'] for av in ev])

plt.scatter([av[1]['hare'] for av in ev], [av[1]['wolf'] for av in ev])
