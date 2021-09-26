using Plots, CairoMakie

function plot_population_timeseries(adf, mdf)
    figure = InteractiveDynamics.Figure(resolution = (600, 400))
    ax = figure[1, 1] = InteractiveDynamics.Axis(figure; xlabel = "Step", ylabel = "Population")
    sheepl = InteractiveDynamics.lines!(ax, adf.step, adf.count_sheep, color = :blue)
    wolfl = InteractiveDynamics.lines!(ax, adf.step, adf.count_wolves, color = :orange)
    # grassl = InteractiveDynamics.lines!(ax, mdf.step, mdf.count_grass, color = :green)
    figure[1, 2] =
        InteractiveDynamics.Legend(figure, [sheepl, wolfl], ["Sheep", "Wolves"])
    figure
end


function plot_metabolism_timeseries(adf, mdf)
    figure = InteractiveDynamics.Figure(resolution = (600, 400))
    ax = figure[1, 1] = InteractiveDynamics.Axis(figure; xlabel = "Step", ylabel = "Metabolism")
    sheepl = InteractiveDynamics.lines!(ax, adf.step, adf.mean_metabolism_sheep, color = :blue)
    wolfl = InteractiveDynamics.lines!(ax, adf.step, adf.mean_metabolism_wolves, color = :orange)
    # grassl = InteractiveDynamics.lines!(ax, mdf.step, mdf.count_grass, color = :green)
    figure[1, 2] =
        InteractiveDynamics.Legend(figure, [sheepl, wolfl], ["Sheep", "Wolves"])
    figure
end
