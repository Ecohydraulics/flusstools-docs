from flusstools.lidartools import hylas
import os


las_file_name = os.path.abspath("") + "/data/my-las-file.las"
shp_file_name = os.path.abspath("") + "/data/las-pts.shp"
epsg = 25832
methods = ["las2shp", "las2dem", "las2tif"]
attribs = "aci"
px_size = 2
tif_prefix = os.path.abspath("") + "/data/full"

hylas.process_file(las_file_name,
                   epsg=epsg,
                   methods=methods,
                   extract_attributes=attribs,
                   pixel_size=px_size,
                   shapefile_name=shp_file_name,
                   tif_prefix=tif_prefix,
                   smoothing=10.0,
                   power=2.0)
