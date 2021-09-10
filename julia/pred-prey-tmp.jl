import Random, Distributions, Statistics
import Agents, InteractiveDynamics

mutable struct SheepWolf <: Agents.AbstractAgent
    id::Int
    pos::Dims{2}
    type::Symbol # :sheep or :wolf
    energy::Float64
    metabolism::Float64
end

# Simple helper functions
Sheep(id, pos, energy, metabolism) = SheepWolf(id, pos, :sheep, energy, metabolism)
Wolf(id, pos, energy, metabolism) = SheepWolf(id, pos, :wolf, energy, metabolism)

sheep(a) = a.type == :sheep
wolves(a) = a.type == :wolf
count_grass(model) = sum(model.grass)

function initialize_model(;
    n_sheep = 100,
    n_wolves = 50,
    dims = (100, 100),
    initial_grass = 1.,
    grass_growth_rate = 1,
    initial_energy_sheep = 1,
    initial_energy_wolf = 1,
    initial_metabolism_sheep = 1,
    initial_metabolism_wolf = 1,
    mutation_rate = .05,
    predation_efficiency = 10,
    reproduction_threshold = 50,
    seed = nothing,
)

    space = Agents.GridSpace(dims, periodic = true)
    properties = (
        grass = fill(initial_grass, dims),
        mutation_rate = mutation_rate,
        min_metabolism = 0.002,
        grass_growth_rate = grass_growth_rate,
        predation_efficiency = predation_efficiency,
        reproduction_threshold = reproduction_threshold
        # rng = rng
    )
    model = Agents.ABM(SheepWolf, space; properties, scheduler = Agents.Schedulers.randomly)
    id = 0
    for _ = 1:n_sheep
        id += 1
        Agents.add_agent!(Sheep(id, (0, 0), initial_energy_sheep, initial_metabolism_sheep), model)
    end
    for _ = 1:n_wolves
        id += 1
        Agents.add_agent!(Wolf(id, (0, 0), initial_energy_wolf, initial_metabolism_wolf), model)
    end
    return model
end

using Memoize
@memoize function collect_sheep_here_memo(position, model)
    agents_here = collect(Agents.agents_in_position(position, model))
    sheep_here = filter!(x -> x.type == :sheep, agents_here)
    return sheep_here
end


function collect_sheep_here(position, model)
    return filter!(x -> x.type == :sheep, collect(Agents.agents_in_position(position, model)))
end



function sheepwolf_step!(agent::SheepWolf, model)

    Agents.walk!(agent, rand, model)
    agent.energy -= 1 + agent.metabolism

    sheep_here = collect_sheep_here(agent.pos, model)


    if agent.type == :sheep
        sheep_eat!(agent, sheep_here, model)
    else # then `agent.type == :wolf`
        wolf_eat!(agent, sheep_here, model)
    end

    if agent.energy < 0
        Agents.kill_agent!(agent, model)
        return
    elseif agent.energy >= model.reproduction_threshold
        reproduce!(agent, model)
        return
    end
end


function sheep_eat!(sheep, sheep_here, model)
    if model.grass[sheep.pos...] > 0
        sheep.energy += model.grass[sheep.pos...]/length(sheep_here)
        model.grass[sheep.pos...] -= model.grass[sheep.pos...]/length(sheep_here)
    end
end

function wolf_eat!(wolf, sheep_here, model)
    if !isempty(sheep_here)
        prey = rand(model.rng, sheep_here)
        if Random.rand(model.rng) < wolf.metabolism/prey.metabolism
            Agents.kill_agent!(prey, model)
            wolf.energy += model.predation_efficiency
        end
    end
end


function reproduce!(agent, model)
    agent.energy /= 2
    Agents.add_agent_pos!(SheepWolf(
        Agents.nextid(model),
        agent.pos,
        agent.type,
        agent.energy,
        max(model.min_metabolism, Random.rand(model.rng, Distributions.Normal(agent.metabolism, model.mutation_rate)))
    ), model)
    return
end

function grass_step!(model)
    @inbounds for p in Agents.positions(model) # we don't have to enable bound checking
        model.grass[p...] += model.grass_growth_rate
    end
end


model = initialize_model(
    n_sheep = 100,
    n_wolves = 100,
    dims = (50, 50),
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

n = 100

adata = [(sheep, count), (wolves, count), (:metabolism, Statistics.mean, sheep), (:metabolism, Statistics.mean, wolves)];
mdata = [count_grass];

@time adf, mdf = Agents.run!(model, sheepwolf_step!, grass_step!, n; adata = adata , mdata = mdata);
