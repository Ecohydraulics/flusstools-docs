"""Basic imports and functions for geo_utils"""
try:
    import logging
    import csv
    import glob
    import os
    import sys
    import urllib
    import subprocess
    import itertools
    import shutil
    import subprocess
    from pathlib import Path
    import platform
    from tabulate import tabulate
except ImportError as e:
    raise ImportError("Could not import standard libraries:\n{0}".format(e))

# import scientific python packages
try:
    import numpy as np
    import matplotlib.pyplot as plt  # for fuzzycor
    import matplotlib.patches as patches
    from matplotlib import colors
    import matplotlib.transforms
    from scipy import interpolate
    import scipy.stats as stats
except ImportError as e:
    raise ImportError("Could not import numpy/matplotlib (is it installed?). {0}".format(e))
try:
    import pandas as pd
except ImportError as e:
    raise ImportError("Could not import pandas (is it installed?). {0}".format(e))

# import osgeo python packages
try:
    from osgeo import gdal
    from osgeo import osr
    from osgeo import ogr
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
# try:
#     import fiona
# except ImportError as e:
#     raise ImportError("Could not import fiona (is it installed?). {0}".format(e))
try:
    # install pyshp to enable shapefile import
    import shapefile
except ImportError as e:
    raise ImportError("Could not import shapefile (included in pyshp - is it installed?). {0}".format(e))
try:
    import geojson
except ImportError as e:
    raise ImportError("Could not import fiona (is it installed?). {0}".format(e))
try:
    import earthpy.plot as ep
except ImportError as e:
    raise ImportError("Could not import earthpy (is it installed?). {0}".format(e))
try:
    import rasterio as rio
except ImportError as e:
    raise ImportError("Could not import rasterio (is it installed?). {0}".format(e))
try:
    import rasterstats
except ImportError as e:
    raise ImportError("Could not import rasterstats (is it installed?). {0}".format(e))
try:
    import laspy
except ImportError as e:
    raise ImportError("Could not import laspy (is it installed?). {0}".format(e))
try:
    import mapclassify.classifiers as mc
except ImportError as e:
    raise ImportError("Could not import mapclassify (is it installed?). {0}".format(e))
try:
    import pyproj
except ImportError as e:
    raise ImportError("Could not import pyproj (is it installed?). {0}".format(e))

# import database packages
try:
    import sqlite3
except ImportError as e:
    raise ImportError("Could not import sqlite3 (is it installed?). {0}".format(e))

# GUI mgmt
try:
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import filedialog
except ImportError as e:
    raise ImportError("Could not import tkinter (is it installed?). {0}".format(e))

# append own directories

sys.path.append(r'' + os.path.abspath(''))
sys.path.insert(0, r'' + os.path.abspath('') + '/geotools')
sys.path.insert(0, r'' + os.path.abspath('') + '/fuzzycorr')
sys.path.insert(0, r'' + os.path.abspath('') + '/lidartools')
sys.path.insert(0, r'' + os.path.abspath('') + '/what2plant')
