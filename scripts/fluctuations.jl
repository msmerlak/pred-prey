using DrWatson
using ProgressBars
@quickactivate

include("../src/pred-prey.jl");
include("../scripts/plotting.jl");

n = 3000
    mean, std = [], []
    for l in tqdm(20:10:200)
        model = initialize_model(
            n_sheep = 3*l,
            n_wolves = 3*l,
            dims = (l, l),
            initial_grass = 3.,
            grass_growth_rate = 0.4,
            initial_energy_sheep = 1,
            initial_energy_wolf = 1,
            initial_metabolism_sheep = 1,
            initial_metabolism_wolf = 1,
            base_metabolic_rate = 0.,
            mutation_rate = 0.0,
            predation_efficiency = 10,
            reproduction_threshold = 40,
            wolves_immigration = true
            );

            adata = [(sheep, count), (wolves, count)]#, (:metabolism, Statistics.mean, sheep), (:metabolism, Statistics.mean, wolves)];
            mdata = [count_grass];

            @time adf, mdf = Agents.run!(model, sheepwolf_step!, grass_step!, n; adata = adata , mdata = mdata)

            append!(std, (sqrt(Statistics.mean((adf.count_wolves.^2)[1000:n])-(Statistics.mean(adf.count_wolves[1000:n]))^2))/l/l)
        end


stds[0.4] = std

Plots.plot([l for l in 20:10:200], [stds[0.2], stds[0.4], stds[0.6]], xaxis=:log, yaxis=:log , xlabel = "linear grid size", ylabel = "predator density std", linewidth = 2)

#stds = Dict{Float64, Vector{Float64}}()


function rununtil(model, s)
    wolves_counter = 0
    for val in values(model.agents)
        if wolves(val)
            wolves_counter +=1
        end
    end
    return wolves_counter == 0 ||s == n
end
