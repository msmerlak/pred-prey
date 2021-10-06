using DrWatson
using ProgressBars
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

function critical_analysis(; grass_growth_rate, n, realizations)
    n, realizations = n, realizations
    time_of_death = fill(0,n)
    for r in tqdm(1:realizations)
        model = initialize_model(
            n_sheep = 6000,
            n_wolves = 60,
            dims = (200, 200),
            initial_grass = 3.,
            grass_growth_rate = grass_growth_rate,
            initial_energy_sheep = 1,
            initial_energy_wolf = 1,
            initial_metabolism_sheep = 1,
            initial_metabolism_wolf = 1,
            base_metabolic_rate = 0.,
            mutation_rate = 0.0,
            predation_efficiency = 10,
            reproduction_threshold = 40
        );

        adata = [(sheep, count), (wolves, count)];
        mdata = [count_grass];
        adf, mdf = Agents.run!(model, sheepwolf_step!, grass_step!, rununtil; adata = adata , mdata = mdata)
        time_of_death[last(adf.step)]+=1
    end

    survival_probability = fill(0., n)
    survival_probability[n] = time_of_death[n]
    for i in tqdm(1:n-1)
        survival_probability[n-i] = survival_probability[n-i+1] + time_of_death[n-i]
    end
    survival_probability = survival_probability/sum(survival_probability)
    #shifted = [survival_probability[floor(Int,1+i/2)] for i in 1:n]
    #delta_exponent = reverse(log.(survival_probability./shifted)/log(2))

    return survival_probability #, delta_exponent
end

dists = Dict{Float64, Vector{Float64}}()

n=1000
dist = critical_analysis(
        grass_growth_rate=0.16,
        n=n,
        realizations=100
)

dists[0.16] = dist

Plots.plot([0.0005*power_law1, dists[0.16]], xaxis=:log, yaxis=:log)

# multi λ
#exps = Dict{Float64, Vector{Float64}}()
for λ in tqdm(0.162:0.002:0.168)
    dists[λ] = critical_analysis(
            grass_growth_rate=λ,
            n=10000,
            realizations=100
    )
end

dists[0.165] = dist

Plots.plot([dists[λ] for λ in 0.162:0.002:0.168], xaxis=:log, yaxis=:log)

power_law1 = [i^(-.159) for i in 1:n]
power_law2 = [i^(-.45) for i in 1:n]
power_lawMF = [i^(-2) for i in 1:100000]
dyn_perc = [i^(-.025) for i in 1:n]
exp =  [Base.exp(-i/10000) for i in 1:n]
Plots.plot([0.1*power_law2, dists[0.184], dists[0.182], dists[0.186]], xaxis=:log, yaxis=:log)
