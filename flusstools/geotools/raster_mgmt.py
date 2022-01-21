from ..helpers import *


def open_raster(file_name, band_number=1):
    """Opens a raster file and accesses its bands.
    
    Args:
        file_name (str): The raster file directory and name.
        band_number (int): The Raster band number to open (default: ``1``).
        
    Returns:
        osgeo.gdal.Dataset: A raster dataset a Python object.
        osgeo.gdal.Band: The defined raster band as Python object.
    """
    gdal.UseExceptions()
    # open raster file or return None if not accessible
    try:
        raster = gdal.Open(file_name)
    except RuntimeError as e:
        logging.error("Cannot open raster.")
        print(e)
        return nan_value, nan_value
    # open raster band or return None if corrupted
    try:
        raster_band = raster.GetRasterBand(band_number)
    except RuntimeError as e:
        logging.error("Cannot access raster band.")
        logging.error(e)
        return raster, nan_value
    return raster, raster_band


def create_raster(file_name, raster_array, bands=1, origin=None, epsg=4326, pixel_width=10., pixel_height=10.,
                  nan_val=nan_value, rdtype=gdal.GDT_Float32, geo_info=False, rotation_angle=None, shear_pixels=True,
                  options=["PROFILE=GeoTIFF"]):
    """Converts an ``ndarray`` (``numpy.array``) to a GeoTIFF raster.
    
    Args:
        file_name (str): Target file name, including directory; must end on ``".tif"``.
        raster_array (``ndarray`` or ``list``): Array or list of arrays of values to rasterize. If a list of arrays is provided, the length of the list will correspond to the number of bands added to the raster (supersedes ``bands``).
        bands (int): Number of bands to write to the raster (default: ``1``).
        origin (tuple): Coordinates (x, y) of the origin.
        epsg (int): EPSG:XXXX projection to use (default: ``4326``).
        pixel_height (float OR int): Pixel height as multiple of the base units defined with the EPSG number (default: ``10`` meters).
        pixel_width (float OR int): Pixel width as multiple of the base units defined with the EPSG number (default: ``10`` meters).
        nan_val (``int`` or ``float``): No-data value to be used in the raster. Replaces non-numeric and ``np.nan`` in the ``ndarray``. (default: ``geoconfig.nan_value``).
        rdtype: `gdal.GDALDataType <https://gdal.org/doxygen/gdal_8h.html#a22e22ce0a55036a96f652765793fb7a4>`_ raster data type (default: gdal.GDT_Float32 (32 bit floating point).
        geo_info (tuple): Defines a ``gdal.DataSet.GetGeoTransform`` object  and supersedes ``origin``, ``pixel_width``, ``pixel_height`` (default: ``False``).
        rotation_angle (float): Rotate (in degrees) not North-up rasters. The default value (``0``) corresponds to north-up (only modify if you know what you are doing).
        shear_pixels (bool): Use with ``rotation_angle`` to shear pixels as well (default: ``True``).
        options (list): Raster creation options - default is ['PROFILE=GeoTIFF']. Add 'PHOTOMETRIC=RGB' to create an RGB image raster.

    Returns:
        int: ``0`` if successful, otherwise ``-1``.

    Hint:
        For processing airborne imagery, the ``rotation_angle`` corresponds to the bearing angle of the aircraft with reference to true, not magnetic North.
    """
    gdal.UseExceptions()
    # check out driver
    driver = gdal.GetDriverByName("GTiff")

    # create raster dataset with number of cols and rows of the input array
    try:
        # overwrite number of bands if multiple arrays are provided in a list
        if type(raster_array) is list:
            bands = raster_array.__len__()
            cols = raster_array[0].shape[1]
            rows = raster_array[0].shape[0]
        else:
            cols = raster_array.shape[1]
            rows = raster_array.shape[0]
    except TypeError:
        logging.error("Provided array is not a numpy.ndarray.")
        return -1

    try:
        logging.info(" * creating new raster with %1i bands ..." % bands)
        new_raster = driver.Create(file_name, cols, rows, bands, eType=rdtype, options=options)
    except RuntimeError as e:
        logging.error("Could not create %s." % str(file_name))
        return -1

    # apply geo-origin and pixel dimensions
    if not geo_info:
        try:
            origin_x = origin[0]
            origin_y = origin[1]
        except IndexError:
            logging.error("Wrong origin format (required: (INT, INT) - provided: %s)." % str(origin))
            return -1
        if rotation_angle:
            try:
                logging.info(" * rotating image by %0.2f deg" % float(rotation_angle))
            except ValueError:
                logging.error("The provided rotation angle is not a number. Re-try with a numeric rotation angle (in degrees).")
                return -1
            rotation_angle = np.deg2rad(rotation_angle)
            x_rotation = -1 * pixel_width * np.sin(rotation_angle)
            y_rotation = -pixel_height * np.cos(rotation_angle)
            if shear_pixels:
                pixel_width = pixel_width * np.cos(rotation_angle)
                pixel_height = pixel_height * np.sin(rotation_angle)
        else:
            x_rotation = 0.
            y_rotation = 0.

        try:
            new_raster.SetGeoTransform((origin_x, pixel_width, x_rotation, origin_y, y_rotation, -pixel_height))
        except RuntimeError as e:
            logging.error("Invalid origin (must be INT) or pixel_height/pixel_width (must be INT) provided.")
            return -1
    else:
        try:
            new_raster.SetGeoTransform(geo_info)
        except RuntimeError as e:
            logging.error(e)
            return -1

    # write array contents to band(s)
    for b in range(bands):
        if type(raster_array) is list:
            # use array item of list if multiple arrays provided
            write_array = raster_array[b]
        else:
            write_array = raster_array
        # replace np.nan values
        write_array[np.isnan(write_array)] = nan_val
        band = new_raster.GetRasterBand(b+1)
        band.SetNoDataValue(nan_val)
        band.WriteArray(write_array)
        band.SetScale(1.0)
        # release band
        band.FlushCache()

    # create projection and assign to raster
    srs = osr.SpatialReference()
    try:
        srs.ImportFromEPSG(epsg)
    except RuntimeError as e:
        logging.error(e)
        return -1
    new_raster.SetProjection(srs.ExportToWkt())
    logging.info(" * successfully created %s" % file_name)

    return 0


def raster2array(file_name, band_number=1):
    """Extracts an ``ndarray`` from a raster.
    
    Args:
        file_name (str): Target file name, including directory; must end on ``".tif"``.
        band_number (int): The raster band number to open (default: ``1``).
        
    Returns:
        ndarray: Indicated raster band, where no-data values are replaced with ``np.nan``.
        GeoTransform: The GeoTransformation used in the original raster.
    """
    # open the raster and band (see above)
    raster, band = open_raster(file_name, band_number=band_number)
    try:
        # read array data from band
        band_array = band.ReadAsArray()
    except AttributeError:
        logging.error("Could not read array of raster band type=%s." % str(type(band)))
        return raster, band, nan_value
    try:
        # overwrite NoDataValues with np.nan
        band_array = np.where(band_array == band.GetNoDataValue(), np.nan, band_array)
    except AttributeError:
        logging.error("Could not get NoDataValue of raster band type=%s." % str(type(band)))
        return raster, band, nan_value
    # return the array and GeoTransformation used in the original raster
    return raster, band_array, raster.GetGeoTransform()


def remove_tif(file_name):
    """Removes a GeoTIFF and its dependent files (e.g., xml).

    Args:
        file_name (str): Directory (path) and name of a GeoTIFF

    Returns:
        Removes the provided ``file_name`` and all dependencies.
    """
    for file in glob.glob("%s*" % file_name.split(".tif")[0]):
        try:
            os.remove(file)
        except PermissionError:
            print("WARNING: Could not remove %s (locked by other program)." % file)
        except FileNotFoundError:
            print("WARNING: The file %s does not exist." % file)


def clip_raster(polygon, in_raster, out_raster):
    """Clips a raster to a polygon.
    
    Args:
        polygon (str): A polygon shapefile name, including directory; must end on ``".shp"``.
        in_raster (str): Name of the raster to be clipped, including its directory.
        out_raster (str): Name of the target raster, including its directory.
        
    Returns: 
        None: Creates a new, clipped raster defined with ``out_raster``.
    """
    gdal.Warp(out_raster, in_raster, cutlineDSName=polygon)
