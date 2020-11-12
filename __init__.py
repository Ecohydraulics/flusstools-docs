from helpers import *

sys.path.append(r'' + os.path.abspath(''))
sys.path.insert(0, r'' + os.path.abspath('') + '/geotools')
sys.path.insert(0, r'' + os.path.abspath('') + '/fuzzycorr')
sys.path.insert(0, r'' + os.path.abspath('') + '/lidartools')
sys.path.insert(0, r'' + os.path.abspath('') + '/what2plant')

from .fuzzycorr import *

try:
    logging.getLogger()
except:
    pass
