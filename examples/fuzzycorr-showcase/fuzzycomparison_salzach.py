from pathlib import Path
import timeit
import fuzzycorr.fuzzycomp as fuzz
import fuzzycorr.plotter as fuzplt

# ------------------------INPUT--------------------------------------
# Neighborhood definition
n = 8  # 'radius' of neighborhood
halving_distance = 4

# Output map and textfile
current_dir = Path.cwd()
Path(current_dir / "results").mkdir(exist_ok=True)  # create dir if not existent
save_dir = str(current_dir / "results")

comparison_name = "salzach_sim_versus_obs_n8hd4"  # filename for the results (.txt) and comparison map (
# .tif)

# Maps to compare
map_A_in = str(current_dir / "rasters/vali_hydro_FT_manual_2013_res5_clipped.tif")
map_B_in = str(current_dir / "rasters/vali_meas_2013_res5_clipped.tif")
# ------------------------------------------------------------------

# Start run time count
start = timeit.default_timer()

# Perform fuzzy comparison
compareAB = fuzz.FuzzyComparison(map_A_in, map_B_in, n, halving_distance)
global_simil = compareAB.fuzzy_numerical(comparison_name, save_dir=save_dir)

# Print global similarity
print('Average fuzzy similarity:', global_simil)

# Stops run time count
stop = timeit.default_timer()

# Print run time:
print('Enlapsed time: ', stop - start, 's')

# Plotting comparison map
cmap = 'inferno'
raster = fuzplt.RasterDataPlotter(str(current_dir / "results/salzach_sim_versus_obs_n8hd4.tif"))
path_fig = str(current_dir) + '/results/' + comparison_name + '.png'
raster.plot_continuous_raster(path_fig, cmap)

