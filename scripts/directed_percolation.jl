using Plots; plotly()
using StatsBase
using Random, Distributions
using ProgressBars

grid = create_grid(
    linear_grid_size = 1000,
    active_site_probability = 0.68
    )

percolate!(grid)

grid

dist, exp = critical_analysis_percolation(
        active_site_probability=0.705,
        linear_grid_size=1000,
        realizations=100
        )

a = [i^(-.159464) for i in 1:1000]

piu = dist
meno = dist

Plots.plot([meno, dist, piu, a], xaxis=:log, yaxis=:log)

function critical_analysis_percolation(; active_site_probability, linear_grid_size, realizations)
    time_of_death = fill(0,linear_grid_size)
    for r in tqdm(1:realizations)
        grid = create_grid(
            linear_grid_size = linear_grid_size,
            active_site_probability = active_site_probability
            )

        time_of_death[sum(percolate!(grid))]+=1
    end

    survival_probability = [sum(time_of_death[i:linear_grid_size]) for i in 1:linear_grid_size]/sum(time_of_death)
    shifted = [survival_probability[floor(Int,1+i/8)] for i in 1:linear_grid_size]
    delta_exponent = reverse(log.(survival_probability./shifted)/log(8))

    return survival_probability, delta_exponent
end

function percolate!(grid)
    active_stpes = fill(0, length(grid))
    grid[1,1] = 2
    active_stpes[1]=1
    for n in 2:Int((length(grid)^0.5))
        if grid[1, n-1]==2
            grid[1, n]*=2
            active_stpes[n]=1
        end
        if grid[n-1, 1]==2
            grid[n, 1]*=2
            active_stpes[n]=1
        end
        for i in 2:n-1
            if grid[i-1, n-i+1]==2 || grid[i, n-i]==2
                grid[i, n-i+1]*=2
                active_stpes[n]=1
            end
        end
    end
    return active_stpes
end

function create_grid(; linear_grid_size, active_site_probability)
    grid = Matrix{Int64}(undef, linear_grid_size, linear_grid_size)
    fill!(grid, 0)
    for i in 1:linear_grid_size
        for j in 1:(linear_grid_size-i+1)
            grid[i, j] = sample([1,0], Weights([active_site_probability, 1-active_site_probability]))
        end
    end
    return grid
end
