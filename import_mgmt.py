"""Basic imports and functions for geo_utils"""
try:
    import logging
    import glob
    import os
    import urllib
    import subprocess
    import itertools
    import shutil
    import platform
except ImportError as e:
    raise ImportError("Could not import standard libraries:\n{0}".format(e))

# import scientific python packages
try:
    import numpy as np
    # import matplotlib  # for future use
except ImportError as e:
    raise ImportError("Could not import numpy/matplotlib (is it installed?). {0}".format(e))
try:
    import pandas as pd
except ImportError as e:
    raise ImportError("Could not import pandas (is it installed?). {0}".format(e))

# import osgeo python packages
try:
    import gdal
    import osr
    from gdal import ogr
except ImportError as e:
    raise ImportError("Could not import gdal and dependent packages (is it installed?). {0}".format(e))

# import other geospatial python packages
try:
    import geopandas
except ImportError as e:
    raise ImportError("Could not import geopandas (is it installed?). {0}".format(e))
try:
    import alphashape
except ImportError as e:
    raise ImportError("Could not import alphashape (is it installed?). {0}".format(e))
try:
    import shapely
    from shapely.geometry import Polygon, LineString, Point
except ImportError as e:
    raise ImportError("Could not import shapely (is it installed?). {0}".format(e))
try:
    import fiona
except ImportError as e:
    raise ImportError("Could not import fiona (is it installed?). {0}".format(e))
try:
    # install pyshp to enable shapefile import
    import shapefile
except ImportError as e:
    raise ImportError("Could not import pyshp (shapefile - is it installed?). {0}".format(e))
try:
    import geojson
except ImportError as e:
    raise ImportError("Could not import fiona (is it installed?). {0}".format(e))
