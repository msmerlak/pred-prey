from defs_diagnostics import *
import multiprocess as mp
import matplotlib.pyplot as plt
%matplotlib inline
from numpy import arange

# single λ
sim = run(
    grid_size=25,
    FC=False,
    nb_steps=1000,
    levels=2,
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
    reproduction_threshold=60,
    predation_efficiency=10,
    grass_growth_rate=10,
    immigration=False,
    mutation_rate=0.1
)

sim.plot(levels=2)

sim.autopsy['hare']['killed']/(sim.autopsy['hare']['starved']+sim.autopsy['hare']['killed'])


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

np.mean(sim.metabolism['hare'][500:])
np.mean(sim.metabolism['wolf'][500:])


# varying λ
with mp.Pool(mp.cpu_count()) as pool:
    metabolisms = pool.map(lambda l: run(
        grid_size=30,
        FC=False,
        nb_steps=3000,
        levels=2,
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
        reproduction_threshold=50,
        predation_efficiency=10,
        grass_growth_rate=l,
        immigration=False,
        mutation_rate=0.05
    ).metabolism, arange(1, 20, 20/mp.cpu_count()))

x_axis = arange(1, 50, 50./mp.cpu_count())
y_axis = [np.mean(metabolisms[i]['hare'][50:]) for i in range(8)]

plt.figure(figsize=(20,5))
plt.loglog(x_axis, [np.mean(metabolisms[i]['hare'][2000:]) for i in range(8)])
plt.loglog(x_axis, [np.mean(metabolisms[i]['wolf'][2000:]) for i in range(8)])
plt.loglog(x_axis, [np.mean(metabolisms[i]['hare'][2000:])/np.mean(metabolisms[i]['wolf'][500:]) for i in range(8)])
plt.loglog(x_axis,x_axis)
plt.ylabel('metabolism')
plt.show()

plt.plot(x_axis,y_axis)
