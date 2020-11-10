"""Global variables"""
from import_mgmt import *


cache_folder = os.path.abspath("") + "/__cache__/"
nan_value = -9999.0

gdal_dtype_dict = {
    0: "gdal.GDT_Unknown",
    1: "gdal.GDT_Byte",
    2: "gdal.GDT_UInt16",
    3: "gdal.GDT_Int16",
    4: "gdal.GDT_UInt32",
    5: "gdal.GDT_Int32",
    6: "gdal.GDT_Float32",
    7: "gdal.GDT_Float64",
    8: "gdal.GDT_CInt16",
    9: "gdal.GDT_CInt32",
    10: "gdal.GDT_CFloat32",
    11: "gdal.GDT_CFloat64",
}
