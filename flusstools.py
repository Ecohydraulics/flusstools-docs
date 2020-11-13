import os, sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('..') + '/geotools')
sys.path.insert(0, os.path.abspath('..') + '/fuzzycorr')
sys.path.insert(0, os.path.abspath('..') + '/what2plant')
sys.path.insert(0, os.path.abspath('..') + '/lidartools')
sys.path.insert(0, os.path.abspath('..') + '/examples/fuzzycorr-showcase')
sys.path.insert(0, os.path.abspath('..') + '/examples/geotools-showcase')

from geotools import *
from fuzzycorr import *
from lidartools import *
from what2plant import *
