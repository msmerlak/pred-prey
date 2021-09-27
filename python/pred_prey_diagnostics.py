from defs_diagnostics import *
import multiprocess as mp
import matplotlib.pyplot as plt
%matplotlib inline
from numpy import arange

# single λ
sim = run(
    grid_size=50,
    FC=False,
    nb_steps=5000,
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
    reproduction_threshold=40,
    predation_efficiency=10,
    grass_growth_rate=50,
    immigration=False,
    mutation_rate=0.1
)

sim.plot(levels=2)


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
    sims = pool.map(lambda l: run(
        grid_size=30,
        FC=False,
        nb_steps=5000,
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
    ), np.logspace(0, np.log10(50), mp.cpu_count()))


# plot metabolisms
plt.figure(figsize=(20,5))
x_axis = np.logspace(0, np.log10(30), mp.cpu_count())
plt.plot(x_axis, [np.mean(sims[i].metabolism['hare'][2000:]) for i in range(mp.cpu_count())])
plt.plot(x_axis, [np.mean(sims[i].metabolism['wolf'][2000:]) for i in range(mp.cpu_count())])
#plt.plot(x_axis, [np.mean(sims[i].metabolism['hare'][1500:])/np.mean(sims[i].metabolism['wolf'][1500:]) for i in range(mp.cpu_count())])
plt.plot(x_axis,np.log(x_axis), '--k')
plt.ylabel('metabolism')
plt.show()

# plot densities
plt.figure(figsize=(20,5))
x_axis = np.logspace(0, np.log10(30), mp.cpu_count())
plt.plot(x_axis, [np.mean(sims[i].density['hare'][2000:]) for i in range(mp.cpu_count())])
plt.plot(x_axis, [np.mean(sims[i].density['wolf'][2000:]) for i in range(mp.cpu_count())])
plt.ylabel('density')
plt.show()

plt.figure(figsize=(20,5))
plt.plot([np.mean(sims[i].density['hare'][2000:]) for i in range(mp.cpu_count())], [np.mean(sims[i].density['wolf'][2000:]) for i in range(mp.cpu_count())])
plt.plot([np.mean(sims[i].density['hare'][2000:]) for i in range(mp.cpu_count())],[np.mean(sims[i].density['hare'][2000:]) for i in range(mp.cpu_count())], '--k')
plt.ylabel('density')
plt.show()

# plot fraction of killed over the total
plt.figure(figsize=(20,5))
x_axis = np.logspace(0, np.log10(50), mp.cpu_count())
y_axis = [sims[i].autopsy['hare']['killed']/(sims[i].autopsy['hare']['killed']+sims[i].autopsy['hare']['starved']) for i in range(mp.cpu_count())]
plt.plot(x_axis, y_axis, 'k')
plt.ylabel('fraction of killed')
plt.show()
