"""
Load, analyze, and write HDF5 (h5) data files.

Hints:
    The scientific HDF5 file format is authored by hdfgroup.org
    Learn more about HDF5 files at https://portal.hdfgroup.org/display/HDF5/Learning+HDF5

Example:
     h5py.File("C:\\temp\\lidar\\191204_130110_Scanner_1_wff5.f5", "r")
"""

try:
    import h5py
except ImportError as e:
    raise ImportError("Could not h5py (try 'pip install h5py'):\n{0}".format(e))


def open_hdf(file_name, mode="r", *args, **kwargs):
    """Opens an HDF file for manipulation with any function)"""
    return h5py.File(file_name, mode)
