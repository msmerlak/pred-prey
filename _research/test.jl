using DrWatson
@quickactivate

include("../src/pred-prey.jl");
include("../src/plotting.jl");

model = initialize_model(
    n_sheep = 100,
    n_wolves = 100,
    dims = (100, 100),
    initial_grass = 1.,
    grass_growth_rate = 20,
    initial_energy_sheep = 50,
    initial_energy_wolf = 50,
    initial_metabolism_sheep = 5,
    initial_metabolism_wolf = 1,
    mutation_rate = 0.1,
    predation_efficiency = 10,
    reproduction_threshold = 30
);

n = 10

adata = [(sheep, count), (wolves, count), (:metabolism, Statistics.mean, sheep), (:metabolism, Statistics.mean, wolves)];
mdata = [count_grass];


adf, mdf = Agents.run!(model, sheepwolf_step!, grass_step!, n; adata = adata , mdata = mdata)


@time adf, mdf = Agents.run!(model, sheepwolf_step!, grass_step!, 1; adata = adata , mdata = mdata)
