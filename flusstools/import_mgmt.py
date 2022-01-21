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
    print("Could not import standard libraries:\n{0}".format(e))

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
    print(
        "Could not import numpy/matplotlib (is it installed?). {0}".format(e))
try:
    import pandas as pd
except ImportError as e:
    print(
        "Could not import pandas (is it installed?). {0}".format(e))

from osgeo import gdal

# append own directories
sys.path.append(r'' + os.path.abspath('.'))
sys.path.append(r'' + os.path.abspath('..'))
sys.path.insert(0, r'' + os.path.abspath('') + '/geotools')
sys.path.insert(0, r'' + os.path.abspath('') + '/fuzzycorr')
sys.path.insert(0, r'' + os.path.abspath('') + '/lidartools')
