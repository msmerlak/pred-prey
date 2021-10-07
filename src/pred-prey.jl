using DrWatson
@quickactivate

import Random, Distributions, Statistics
import Agents, InteractiveDynamics
import ProgressBars

mutable struct SheepWolf <: Agents.AbstractAgent
    id::Int
    pos::Dims{2}
    type::Symbol # :sheep or :wolf
    energy::Float64
    metabolism::Float64
end

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
    base_metabolic_rate = 1,
    initial_metabolism_sheep = 1,
    initial_metabolism_wolf = 1,
    mutation_rate = .05,
    predation_efficiency = 10,
    reproduction_threshold = 40,
    wolves_immigration = false,
    seed = nothing,
)

    space = Agents.GridSpace(dims, periodic = true)
    properties = (
        grass = fill(initial_grass, dims),
        time_from_last_immigration = [0],
        extinction_statistics = Dict([(1, 0)]),
        mutation_rate = mutation_rate,
        min_metabolism = 0.002,
        grass_growth_rate = grass_growth_rate,
        predation_efficiency = predation_efficiency,
        reproduction_threshold = reproduction_threshold,
        base_metabolic_rate = base_metabolic_rate,
        wolves_immigration = wolves_immigration,
        initial_metabolism_wolf = initial_metabolism_wolf,
        initial_energy_wolf = initial_energy_wolf
        sheeps_immigration = sheeps_immigration,
        initial_metabolism_sheep = initial_metabolism_sheep,
        initial_energy_sheep = initial_energy_sheep
    )
    model = Agents.ABM(SheepWolf, space; properties, scheduler = Agents.Schedulers.randomly)
    id = 0
    for _ = 1:n_sheep
        id += 1
        Agents.add_agent!(SheepWolf(id, (0, 0), :sheep, initial_energy_sheep, initial_metabolism_sheep), model)
    end
    for _ = 1:n_wolves
        id += 1
        Agents.add_agent!(SheepWolf(id, (0, 0), :wolf, initial_energy_wolf, initial_metabolism_wolf), model)
    end
    return model
end

function collect_sheep_here(position, model)
    return filter!(sheep, collect(Agents.agents_in_position(position, model)))
end

function sheepwolf_step!(agent::SheepWolf, model)

    Agents.walk!(agent, rand, model)
    agent.energy -= model.base_metabolic_rate + agent.metabolism

    sheep_here = collect_sheep_here(agent.pos, model)

    if agent.type == :sheep
        sheep_eat!(agent, sheep_here, model)
    else
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

function model_step!(model)
    @inbounds for p in Agents.positions(model) # we don't have to enable bound checking
        model.grass[p...] += model.grass_growth_rate
    end
    # wolves immigration
    if model.wolves_immigration && length(filter(wolves, [agents for agents in Agents.allagents(model)])) == 0
        Agents.add_agent!(SheepWolf(Agents.nextid(model), (0, 0), :wolf, model.initial_energy_wolf, model.initial_metabolism_wolf), model)
        # extinctions counting
        if haskey(model.extinction_statistics, model.time_from_last_immigration[1])
            model.extinction_statistics[model.time_from_last_immigration[1]] += 1
        else
            model.extinction_statistics[model.time_from_last_immigration[1]] = 1
        end
        model.time_from_last_immigration[1] = 1
    else
        model.time_from_last_immigration[1] += 1
    end
    # sheeps immigration
    if model.sheeps_immigration && length(filter(sheep, [agents for agents in Agents.allagents(model)])) == 0
        Agents.add_agent!(SheepWolf(Agents.nextid(model), (0, 0), :sheep, model.initial_energy_sheep, model.initial_metabolism_sheep), model)
    end
end
