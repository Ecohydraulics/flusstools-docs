"""An example application for projecting non-georeferenced TIF files on a spatial reference system.
The TIF files in this example have a prefix and suffix name, which are separated by a 4-digits number.
The origin of the new GeoTIFF files is derived from a KML file.
"""
# append geo_utils script directory to interpreter path
import os, sys
sys.path.append(os.path.abspath(".."))

# import geo_utils - and this script also requires pyproj (install with pyshp)
from geo_utils.geo_utils import *
import pyproj


@cache
def project_tiffs(kml_dir, src_tiff_dir, epsg_tar, epsg_src=4326, tiff_prefix="", tiff_suffix=".tif",
                  tar_tiff_dir="/", pixel_width=1.0):
    """Project non-georeferenced GeoTIFFs from a source EPSG on to a target EPSG
    and use KML placemarks as origins for the new projections.

    Args:
        kml_dir (str): Directory of a KML (or KMZ) file
        src_tiff_dir (str): Directory for source (non-georeferenced) TIFFs - must end on ``'/'```
        epsg_src (int): Authority code of the source spatial reference system (KML files usually use ``EPSG=4326``)
        epsg_tar (int): Authority code of the target spatial reference system
        tar_tiff_dir (str): Directory (path) where projected GeoTIFFs will be saved
        pixel_width (``float`` or ``int``): Defines the size of one pixel relative to the base unit system (e.g., if 1 and the base unit system is metric, then the ``pixel_size`` is 1 m)
        tiff_prefix (str): An optional prefix to narrow down source TIFF file names to use - do not include a directory
        tiff_suffix (str): An optional suffix to narrow down source TIFF file names to use - must end on ``'.tif'``
    """

    # check if the target directory exists
    if not os.path.isdir(tar_tiff_dir):
        os.mkdir(tar_tiff_dir)

    # read kml file as geopandas dataframe
    gdf_kml = kmx2other(kml_dir, output="gpd")

    # define source and target coordinate systems
    kml_crs = pyproj.CRS("EPSG:%s" % str(epsg_src))
    tar_crs = pyproj.CRS("EPSG:%s" % str(epsg_tar))
    transformer = pyproj.Transformer.from_crs(kml_crs, tar_crs)

    # retrieve prefix name of tiff files
    tiff_prefix_dir = "{0}{1}".format(src_tiff_dir, tiff_prefix)

    for i in range(gdf_kml["coordinates"].__len__()):
        img_no = int(gdf_kml["description"][i].split("Image Number=<td><b>")[-1].split("</b>")[0])
        tiff_name = tiff_prefix_dir + "%0004i" % img_no + tiff_suffix
        print(" * identified raster name %s ..." % tiff_name)

        print("   - retrieving origin coordinates from kml")
        long, lat, alt = (float(coord) for coord in gdf_kml["coordinates"][i].split(","))
        x, y = transformer.transform(lat, long)

        print("   - opening R, G, and B arrays of the source raster ... ")
        src_ras, red_array, none_ref = raster2array(tiff_name, band_number=1)
        src_ras, blue_array, none_ref = raster2array(tiff_name, band_number=2)
        src_ras, green_array, none_ref = raster2array(tiff_name, band_number=3)
        # release source raster
        src_ras = None
        # summarize RGB array in  list
        rgb = [red_array, blue_array, green_array]

        print("   - creating new projected raster ... ")
        create_raster(file_name=tar_tiff_dir + tiff_prefix + "%0004i" % img_no + "_georef.tif",
                      raster_array=rgb,
                      epsg=epsg_tar,
                      origin=(x, y),
                      nan_val=0,
                      pixel_width=0.1,
                      pixel_height=0.1,
                      rdtype=gdal.GDT_UInt16,
                      rotation_angle=178.,
                      shear_pixels=False,
                      options=["PHOTOMETRIC=RGB", "PROFILE=GeoTIFF"])


if __name__ == "__main__":
    # get source file names as list
    src_tiff_dir = "/dir/to/tifs/"
    src_tiff_prefix = "tif_prefix"
    src_tiff_suffix = "tif_suffix.tif"
    tar_tiff_dir = os.path.abspath("") + "/output/"

    # read image anchors (origins) from kml file (always has source epsg=4326 - google maps uses 3857)
    src_kml = "/dir/to/and/of/a/google-earth-file.kml"

    project_tiffs(kml_dir=src_kml, src_tiff_dir=src_tiff_dir,
                  tar_tiff_dir=tar_tiff_dir,
                  tiff_prefix=src_tiff_prefix,
                  tiff_suffix=src_tiff_suffix,
                  epsg_src=4326,
                  epsg_tar=3857)
