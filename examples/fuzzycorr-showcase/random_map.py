import fuzzycorr.prepro as pp
from pathlib import Path
import pandas as pd

#  ------------------ INPUT -------------------------
file = 'vali_meas_2013'

# Polygon of area of interest
polyname = 'polygon_salzach'

# Characteristics of the raster
attribute = 'dz'
res = 5

# Projection
crs = 'EPSG:5684'
nodatavalue = -9999

# Corners of raster
ulc = (4571800, 5308230)
lrc = (4575200, 5302100)

current_dir = Path.cwd()

Path(current_dir / 'shapefiles').mkdir(exist_ok=True)
Path(current_dir / 'rasters').mkdir(exist_ok=True)

# Create files path
poly_path = str(current_dir / 'shapefiles') + '/' + polyname + '.shp'
path_file = str(current_dir / 'raw_data') + '/' + file + '.csv'
random_raster = str(current_dir / 'rasters') + '/' + file + '_random.tif'
clipped_random_raster = str(current_dir / 'rasters') + '/' + file + '_random_clipped.tif'
#  --------------------------------------------------------------------------------

# Instanciating object
map_file = pp.PreProFuzzy(pd.read_csv(path_file, skip_blank_lines=True), attribute=attribute, crs=crs,
                          nodatavalue=nodatavalue, res=res, ulc=ulc, lrc=lrc)

# Create random raster
map_file.random_raster(random_raster, minmax=None, save_ascii=False)

# Clip random raster
pp.clip_raster(poly_path, in_raster=random_raster, out_raster=clipped_random_raster)

