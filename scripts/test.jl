using DrWatson
@quickactivate

include("../src/pred-prey.jl");
include("../scripts/plotting.jl");

model = initialize_model(
    n_sheep = 30,
    n_wolves = 30,
    dims = (20, 20),
    initial_grass = 3.,
    grass_growth_rate = 0.5,
    initial_energy_sheep = 1,
    initial_energy_wolf = 1,
    initial_metabolism_sheep = 1,
    initial_metabolism_wolf = 1,
    base_metabolic_rate = 0.,
    mutation_rate = 0.0,
    predation_efficiency = 10,
    reproduction_threshold = 40,
    wolves_immigration = true,
    );

    n = 1000

    adata = [(sheep, count), (wolves, count)]#, (:metabolism, Statistics.mean, sheep), (:metabolism, Statistics.mean, wolves)];
    mdata = [count_grass];

    @time adf, mdf = Agents.run!(model, sheepwolf_step!, model_step!, n; adata = adata , mdata = mdata)

model.time_from_last_immigration

mdf
Plots.plot(adf.step, [adf.count_sheep, adf.count_wolves])

(sqrt(Statistics.mean((adf.count_wolves.^2)[1000:n])-(Statistics.mean(adf.count_wolves[1000:n]))^2))/l/l
