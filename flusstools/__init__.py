import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from helpers import *
    import lidartools
    import fuzzycorr
    import geotools
    import bedanalyst
except ModuleNotFoundError:
    print("Failed to initialize FlussTools - consider re-installation")

try:
    logging.getLogger()
except NameError:
    pass
