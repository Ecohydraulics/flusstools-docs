from pathlib import Path
import fuzzycorr.prepro as pp
import pandas as pd


# ---------------Data Pre-processing---------------------------------
# ------------------------INPUT--------------------------------------
#  Raw data input path
list_files = ['vali_hydro_FT_manual_2013',
              'vali_meas_2013']

# Parameters
attribute = 'dz'
interpol_method = 'cubic'

# Polygon of area of interest
polyname = 'polygon_salzach'

#  Raster Resolution: Change as appropriate
#  NOTE: Fuzzy Analysis has unique resolution
res = 5

# Projection
crs = 'EPSG:5684'
nodatavalue = -9999

# Corners of raster
ulc = (4571800, 5308230)
lrc = (4575200, 5302100)

# Create directories if not existent
current_dir = Path.cwd()
Path(current_dir / 'shapefiles').mkdir(exist_ok=True)
Path(current_dir / 'rasters').mkdir(exist_ok=True)

poly_path = str(current_dir / 'shapefiles') + '/' + polyname + '.shp'

# -----------------------------------------------------------------------

for file in list_files:
    # Path management
    path_file = str(current_dir / 'raw_data') + '/' + file + '.csv'
    raster_out = str(current_dir / 'rasters') + '/' + file + '_res5.tif'

    # Instantiate object of class PreProFuzzy
    map_file = pp.PreProFuzzy(pd.read_csv(path_file, skip_blank_lines=True), attribute=attribute, crs=crs, nodatavalue=nodatavalue, res=res, ulc=ulc, lrc=lrc)

    # Normalize points to a grid-ed array
    array_ = map_file.norm_array(method=interpol_method)

    # Write raster
    map_file.array2raster(array_, raster_out, save_ascii=False)

    # Clip raster and save it
    clip_raster = str(current_dir / 'rasters') + '/' + file + '_res5_clipped' + '.tif'
    map_file.create_polygon(poly_path, alpha=0.01)
    pp.clip_raster(poly_path, raster_out, clip_raster)
