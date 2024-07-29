from pathlib import Path
import fuzzycorr.plotter as fuzplt

list_files = ['salzach_sim_versus_obs_n8hd4']

legendx = 'Fuzzy Similarity [-]'
legendy = 'Frequency'

current_dir = Path.cwd()
Path(current_dir / 'analysis').mkdir(exist_ok=True)

for file in list_files:
    path_raster = str(current_dir / 'results/fuzzy_numerical') + '/' + file + '.tif'
    outputpath = str(current_dir / 'analysis') + '/' + file + '_hist.png'
    raster = fuzplt.RasterDataPlotter(path_raster)
    raster.make_hist(legendx, legendy, fontsize=15, output_file=outputpath, figsize=(10, 4), set_ylim=(0, 1000), set_xlim=(-0.2, 1.0))

