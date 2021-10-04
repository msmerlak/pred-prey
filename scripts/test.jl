using DrWatson
@quickactivate

include("../src/pred-prey.jl");
include("../scripts/plotting.jl");

model = initialize_model(
    n_sheep = 100,
    n_wolves = 100,
    dims = (100, 100),
    initial_grass = 1.5,
    grass_growth_rate = λ,
    initial_energy_sheep = 50,
    initial_energy_wolf = 50,
    initial_metabolism_sheep = 1,
    initial_metabolism_wolf = 1,
    base_metabolic_rate = 0.,
    mutation_rate = 0.0,
    predation_efficiency = 10,
    reproduction_threshold = 40
    );

    n = 1000

    adata = [(sheep, count), (wolves, count)]#, (:metabolism, Statistics.mean, sheep), (:metabolism, Statistics.mean, wolves)];
    mdata = [count_grass];

    @time adf, mdf = Agents.run!(model, sheepwolf_step!, grass_step!, n; adata = adata , mdata = mdata)

plot_population_timeseries(adf, mdf)
