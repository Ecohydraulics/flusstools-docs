import plotter
from pathlib import Path
from matplotlib import cm

current_dir = Path.cwd()
legendx = 'Fuzzy Similarity [-]'
legendy = 'Frequency'

list_rasters = ['vali_meas_2013_res5_clipped',
                'vali_hydro_FT_manual_2013_res5_clipped']


# Bounds for colormap
bounds = [-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

list_colors = ['darkred', 'sienna', 'chocolate', 'sandybrown', 'gold', 'yellow', 'greenyellow', 'lime', 'lightseagreen','deepskyblue', 'royalblue', 'navy']

for item in list_rasters:
    rast_path = str(current_dir) + '/rasters/' + item + '.tif'
    raster = plotter.RasterDataPlotter(rast_path)
    path_fig = str(current_dir) + '/rasters/figures/' + item + '.png'
    raster.plot_continuous_w_window(output_file=path_fig, xy=(0, 0), width=170, height=270, cmap=None, list_colors=list_colors, bounds=bounds)

