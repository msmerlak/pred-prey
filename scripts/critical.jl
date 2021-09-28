using DrWatson
@quickactivate

include("../src/pred-prey.jl");
include("../scripts/plotting.jl");

function rununtil(model, s)
    wolves_counter = 0
    for val in values(model.agents)
        if wolves(val)
            wolves_counter +=1
        end
    end
    return wolves_counter == 0 ||s == n
end


realizations = 100
n = 1000

time_of_death = Dict{Int64,Int64}()

for r in 1:realizations
    model = initialize_model(
        n_sheep = 100,
        n_wolves = 100,
        dims = (100, 100),
        initial_grass = 1.,
        grass_growth_rate = .5,
        initial_energy_sheep = 50,
        initial_energy_wolf = 50,
        initial_metabolism_sheep = 1,
        initial_metabolism_wolf = 1,
        mutation_rate = 0.1,
        predation_efficiency = 10,
        reproduction_threshold = 30
    );

    adata = [(sheep, count), (wolves, count)];
    mdata = [count_grass];

    @time adf, mdf = Agents.run!(model, sheepwolf_step!, grass_step!, rununtil; adata = adata , mdata = mdata)

    println("steps : ", last(adf.step))
    if haskey(time_of_death, last(adf.step))
        time_of_death[last(adf.step)] += 1
    else
        time_of_death[last(adf.step)] = 1
    end
end

plot_population_timeseries(adf, mdf)

delete!(time_of_death, n)
plot_time_of_death_histogram(time_of_death)
