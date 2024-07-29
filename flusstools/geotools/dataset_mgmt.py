from .raster_mgmt import *
from .shp_mgmt import *
gdal.UseExceptions()


def coords2offset(geo_transform, x_coord, y_coord):
    """ Returns x-y pixel offset (inverse of the ``offset2coords`` function).

    Args:
        geo_transform: osgeo.gdal.Dataset.GetGeoTransform() object
        x_coord (float): x-coordinate
        y_coord (float): y-coordinate

    Returns:
        tuple: Number of pixels ``(offset_x, offset_y)``,  both ``int`` .
    """
    try:
        origin_x = geo_transform[0]
        origin_y = geo_transform[3]
        pixel_width = geo_transform[1]
        pixel_height = geo_transform[5]
    except IndexError:
        logging.error("Invalid geo_transform object (%s)." %
                      str(geo_transform))
        return None

    try:
        offset_x = int((x_coord - origin_x) / pixel_width)
        offset_y = int((y_coord - origin_y) / pixel_height)
    except ValueError:
        logging.error(
            "geo_transform tuple contains non-numeric data: %s" % str(geo_transform))
        return None
    return offset_x, offset_y


def get_layer(dataset, band_number=1):
    """Gets a ``layer=band`` (``RasterDataSet``) or ``layer=ogr.Dataset.Layer`` of any dataset.

    Args:
        dataset (``osgeo.gdal.Dataset`` or ``osgeo.ogr.DataSource``): Either a raster or a shapefile.
        band_number (int): Only use with rasters to define a band number to open (default is ``1`` ).

    Returns:
        dict: ``{"type": raster`` or ``vector`` or ``"None", layer":`` if raster: ``raster_band``, if vector: ``GetLayer()``, else: ``None}``
    """
    if verify_dataset(dataset) == "raster":
        return {"type": "raster", "layer": dataset.GetRasterBand(band_number)}
    if verify_dataset(dataset) == "vector":
        return {"type": "vector", "layer":  dataset.GetLayer()}
    return {"type": "None", "layer": None}


def offset2coords(geo_transform, offset_x, offset_y):
    """Returns x-y coordinates from pixel offset (inverse of ``coords2offset`` function).

    Args:
        geo_transform (osgeo.gdal.Dataset.GetGeoTransform): The geo transformation to use.
        offset_x (int): x number of pixels.
        offset_y (int): y number of pixels.

    Returns:
        tuple: Two ``float`` numbers of x-y-coordinates ``(x_coord, y_coord)``.
    """
    try:
        origin_x = geo_transform[0]
        origin_y = geo_transform[3]
        pixel_width = geo_transform[1]
        pixel_height = geo_transform[5]
    except IndexError:
        logging.error("Invalid geo_transform object (%s)." %
                      str(geo_transform))
        return None

    try:
        coord_x = origin_x + pixel_width * (offset_x + 0.5)
        coord_y = origin_y + pixel_height * (offset_y + 0.5)
    except ValueError:
        logging.error(
            "geo_transform tuple contains non-numeric data: %s" % str(geo_transform))
        return None
    return coord_x, coord_y


def verify_dataset(dataset):
    """Verifies if a dataset contains raster or vector data.

    Args:
        dataset (``osgeo.gdal.Dataset`` or ``osgeo.ogr.DataSource``): Dataset to verify.

    Returns:
        str: Either "unknown", "raster", or "vector".
    """
    # Check the contents of an osgeo.gdal.Dataset
    try:
        if dataset.RasterCount > 0 and dataset.GetLayerCount() > 0:
            return "unknown"
    except AttributeError:
        pass

    try:
        if dataset.RasterCount > 0:
            return "raster"
    except AttributeError:
        pass

    try:
        if dataset.GetLayerCount() > 0:
            return "vector"
        else:
            return "empty"
    except AttributeError:
        logging.error("%s is not an osgeo.gdal.Dataset object." % str(dataset))
        return None
