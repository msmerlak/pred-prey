using DrWatson
@quickactivate

include("../src/pred-prey.jl");
include("../scripts/plotting.jl");

realizations = 10
n = 100

for r in 1:realizations
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

    adata = [(sheep, count), (wolves, count), (:metabolism, Statistics.mean, sheep), (:metabolism, Statistics.mean, wolves)];
    mdata = [count_grass];

    @time adf, mdf = Agents.run!(model, sheepwolf_step!, grass_step!, rununtil; adata = adata , mdata = mdata)
    #plot_population_timeseries(adf, mdf)

    println(last(adf.step))
    print(model.agents.count)
end

# function to feed to run!(), when true the sim stops
function rununtil(model, s)
    return model.agents.count >= 2000 || s == n # NOW I ONLY NEED TO UNDERSTAND HOW TO COUNT ONLY WOLFS
end
