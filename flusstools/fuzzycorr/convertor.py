"""
Descriptions will be updated by Bea
"""
from osgeo import gdal
from pathlib import Path

current_dir = Path.cwd()
list_of_files = ['vali_meas_2013_clipped', 'vali_hydro_FT_manual_2013_clipped']

for file in list_of_files:
    map_asc = str(current_dir / 'salzach_case/rasters') + '/' + file + '.asc'
    map_in = str(current_dir / 'salzach_case/rasters') + '/' + file + '.tif'
    gdal.Translate(map_asc, map_in, format='AAIGrid')
