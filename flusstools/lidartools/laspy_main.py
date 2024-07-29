"""Main script for las file processing. Use as:

``process_file(source_file_name, epsg, **opts)`` (more about arguments in the function doc below)
"""

from .laspy_processor import *
import webbrowser


def lookup_epsg(file_name):
    """Starts a google search to retrieve information from a file name (or other ``str``)
    with information such as *UTM32*.

    Args:
        file_name (str): file name  or other string with words separated by "-" or "_"

    Notes:
        * This function opens a google search in the default web browser.
        * More information about projections, spatial reference systems, and coordinate systems
         can be obtained with the `geo_utils <https://geo-utils.readthedocs.io>`_ package.

    """
    search_string = file_name.replace(
        "_", "+").replace(".", "+").replace("-", "+")
    google_qry = "https://www.google.com/?#q=projection+crs+epsg+"
    webbrowser.open(google_qry + search_string)


@cache
def process_file(source_file_name, epsg, **opts):
    """Loads a las-file and convert it to another geospatial file format (keyword arguments ``**opts``).

    Args:
        source_file_name (str): Full directory of the source file to use with methods
                             * if method="las2*" > provide a las-file name
                             * if method="shp2*" > provide a shapefile name
        epsg (int): Authority code to use (try ``hylas.lookup_epsg(las_file_name)`` to look up the epsg online).

    Keyword Args:
        create_dem (bool): default: False - set to True for creating a digital elevation model (DEM)
        extract_attributes (str): Attributes to extract from the las-file available in pattr (config.py)
        methods(`list` [`str`]): Enabled list strings are las2shp, las2tif, shp2tif, las2dem
        overwrite (bool): Overwrite existing shapefiles and/or GeoTIFFs (default: ``True``).
        pixel_size (float): Use with *2tif  to set the size of pixels relative to base units (pixel_size=5 > 5-m pixels)
        shapefile_name (str): Name of the point shapefile to produce with las2*
        tif_prefix (str): Prefix include folder path to use for GeoTiFFs (defined extract_attributes are appended to file name)
        interpolate_gap_pixels (bool): Fill empty pixels that are not touched by a shapefile point with interpolated values (default: ``True``)
        radius1 (float): Define the x-radius for interpolating pixels (default: ``-1``, corresponding to infinity). Only applicable ``with interpolate_gap_pixels``.
        radius2 (float): Define the y-radius for interpolating pixels (default: ``-1``, corresponding to infinity). Only applicable ``with interpolate_gap_pixels``.
        power (float): Power of the function for interpolating pixel values (default: ``1.0``, corresponding to linear).
        smoothing (float): Smoothing parameter for interpolating pixel values (default: ``0.0``).
        min_points (int): Minimum number of points to use for interpolation. If the interpolator cannot find at least ``min_points`` for a pixel, it assigns a ``no_data`` value to that pixel  (default: ``0``).
        max_points (int): Maximum number of points to use for interpolation. The interpolator will not use more than ``max_points`` closest points to interpolate a pixel value (default: ``0``).

    Returns:
        bool: ``True`` if successful, ``False`` otherwise
    """

    default_keys = {
        "extract_attributes": "aci",
        "interpolate_gap_pixels": True,
        "methods": ["las2shp"],
        "shapefile_name": os.path.abspath("") + "/{0}.shp".format(source_file_name.split(".")[0]),
        "tif_prefix": os.path.abspath("") + "/{0}_".format(source_file_name.split(".")[0]),
        "overwrite": True,
        "create_dem": False,
        "pixel_size": 1.0,
        "radius1": -1,
        "radius2": -1,
        "power": 1.0,
        "smoothing": 0.0,
        "min_points": 0,
        "max_points": 0,
    }

    for k in default_keys.keys():
        if opts.get(k):
            default_keys[k] = opts.get(k)

    las_object = LasPoint(las_file_name=source_file_name,
                          epsg=epsg,
                          use_attributes=default_keys["extract_attributes"],
                          overwrite=default_keys["overwrite"])

    if "las2shp" in default_keys["methods"] or not os.path.isfile(default_keys["shapefile_name"]):
        logging.info(" * Need to create a point shapefile first (%s does not exist) ..." %
                     default_keys["shapefile_name"])
        las_object.export2shp(shapefile_name=default_keys["shapefile_name"])

    if "las2dem" in "".join(default_keys["methods"]):
        logging.info(" * Generating DEM from %s." %
                     default_keys["shapefile_name"])
        las_object.create_dem(target_file_name=default_keys["tif_prefix"] + "_dem.tif",
                              src_shp_file_name=default_keys["shapefile_name"],
                              pixel_size=default_keys["pixel_size"],
                              interpolate_gap_pixels=default_keys["interpolate_gap_pixels"],
                              power=default_keys["power"],
                              radius1=default_keys["radius1"],
                              radius2=default_keys["radius2"],
                              smoothing=default_keys["smoothing"],
                              min_points=default_keys["min_points"],
                              max_points=default_keys["max_points"]
                              )

    if "2tif" in "".join(default_keys["methods"]):
        logging.info(" * Creating GeoTIFFs ...")
        for attr in default_keys["extract_attributes"]:
            tif_name = "{0}{1}.tif".format(
                default_keys["tif_prefix"], wattr[attr])
            logging.info("   -- Creating %s ..." % tif_name)
            geo_utils.rasterize(in_shp_file_name=default_keys["shapefile_name"],
                                out_raster_file_name=tif_name,
                                interpolate_gap_pixels=False,
                                pixel_size=default_keys["pixel_size"],
                                field_name=wattr[attr],
                                overwrite=default_keys["overwrite"])
        logging.info("   -- Done.")
    return True
