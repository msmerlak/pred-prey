using DrWatson
@quickactivate

include("../src/pred-prey.jl");
include("../scripts/plotting.jl");

s_counts , w_counts = [], []
    for λ in ProgressBars.tqdm(0.14:0.002:0.17)
        model = initialize_model(
            n_sheep = 6000,
            n_wolves = 60,
            dims = (200, 200),
            initial_grass = 3.,
            grass_growth_rate = λ,
            initial_energy_sheep = 1.,
            initial_energy_wolf = 1.,
            initial_metabolism_sheep = 1.,
            initial_metabolism_wolf = 1.,
            base_metabolic_rate = 0.,
            mutation_rate = 0.0,
            predation_efficiency = 10,
            reproduction_threshold = 40,
            wolves_immigration = false
            );

            n = 2000

            adata = [(sheep, count), (wolves, count)]#, (:metabolism, Statistics.mean, sheep), (:metabolism, Statistics.mean, wolves)];
            mdata = [count_grass];

            @time adf, mdf = Agents.run!(model, sheepwolf_step!, grass_step!, n; adata = adata , mdata = mdata)
            append!(s_counts, [adf.count_sheep])
            append!(w_counts, [adf.count_wolves])
        end

s_counts
x = [i for i in 0.14:0.002:0.17]
y_s = [Statistics.mean(s_counts[i][1000:2001]) for i in 1:16]
y_w = [Statistics.mean(w_counts[i][1000:2001]) for i in 1:16]
Plots.plot(x, [y_s, y_w])
