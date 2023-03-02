from helpers import *


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
        raster_array (``ndarray`` or ``list``): 2d-array (no bands) or list (bands) of 2-darrays of values to rasterize. If a list of 2d-arrays is provided, the length of the list will correspond to the number of bands added to the raster (supersedes ``bands``).
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
        new_raster = driver.Create(
            file_name, cols, rows, bands, eType=rdtype, options=options)
    except RuntimeError as e:
        logging.error("Could not create %s." % str(file_name))
        return -1

    # apply geo-origin and pixel dimensions
    if not geo_info:
        try:
            origin_x = origin[0]
            origin_y = origin[1]
        except IndexError:
            logging.error(
                "Wrong origin format (required: (INT, INT) - provided: %s)." % str(origin))
            return -1
        if rotation_angle:
            try:
                logging.info(" * rotating image by %0.2f deg" %
                             float(rotation_angle))
            except ValueError:
                logging.error(
                    "The provided rotation angle is not a number. Re-try with a numeric rotation angle (in degrees).")
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
            new_raster.SetGeoTransform(
                (origin_x, pixel_width, x_rotation, origin_y, y_rotation, -pixel_height))
        except RuntimeError as e:
            logging.error(
                "Invalid origin (must be INT) or pixel_height/pixel_width (must be INT) provided.")
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


def xy_raster_shift(file_name,x_shift, y_shift, bands=1, rdtype=gdal.GDT_Float32, nan_val=nan_value,
                    compress=True, options=['PROFILE=GeoTIFF'], compress_config=["COMPRESS=LZW", "TILED=YES"]):
    """Creates new geotiff raster with shifts in x and y direction. If enabled compresses it also compresses file.

    Args:
    file_name (string): File path of GeoTiff
    x_shift (float OR int): Shift origin in x direction. *Check that correct units are used.  Example: wgs 84 is in degrees
    y_shift (float OR int): Shift origin in y direction. *Check that correct units are used.  Example: wgs 84 is in degrees
    bands (int): Number of bands default is 1, however check raster to see how many are required. Example: RGBA=4
    rdtype: `gdal.GDALDataType <https://gdal.org/doxygen/gdal_8h.html#a22e22ce0a55036a96f652765793fb7a4>`_ raster data type (default: gdal.GDT_Float32 (32 bit floating point).
    nan_val (``int`` or ``float``): No-data value to be used in the raster. Replaces non-numeric and ``np.nan`` in the ``ndarray``. (default: ``geoconfig.nan_value``).
    compress (Bool): If True creates compressed version of the GeoTiff
    options (list): Raster creation options - default is ['PROFILE=GeoTIFF']. Add 'PHOTOMETRIC=RGB' to create an RGB image raster.
    compress_config: (list) Compress creation options - default is ["COMPRESS=LZW", "TILED=YES"] LZW=Lempel-Ziv-Welch-Algorithm  See gdal.Translate for more options

    Returns:
        int: ``0`` if successful, otherwise ``-1``.

    Hint:
    For drone rasters try
    bands=4 (rgba) rdtype=gdal.GDT_Byte nan_val=0 options=['PROFILE=GeoTIFF','PHOTOMETRIC=RGB'])

    Bugs: Issues displaying logging
    """
    # Gdal opens Tiff
    try:
        tif = gdal.Open(file_name)
    except RuntimeError:
        logging.error("Cannot open raster in Gdal.")
        return -1

    # Extracting geo_transform
    geo_transform = tif.GetGeoTransform()

    # Extracting arrays from raster to create an array list
    try:
        list_array=[]
        for n in range(bands):

            list_array.append(tif.GetRasterBand(n+1).ReadAsArray())
    except RuntimeError:
        logging.error("Cannot create array list from bands.")
        return -1

    # sets the geodata into individual types
    try:
        origin_x = geo_transform[0]
        origin_y = geo_transform[3]
        pixel_width = geo_transform[1]
        pixel_height = geo_transform[5]
        pixel_height = pixel_height * -1 # setting negative so raster is not mirrored over y-intercept, due to create_raster's "*-1 pixelheight"
        proj = osr.SpatialReference(tif.GetProjection())
        epsg = int(proj.GetAttrValue('AUTHORITY', 1))
    except ValueError:
        logging.error(
            "Problems with geodata")

    try:
        logging.info(
            "Creating raster with x shift of {0} units  and y shift of {1} units" .format(
                 float(x_shift),float(y_shift)))

    except ValueError:
        logging.error(
            "The provided x and y shifts are not numbers.")
        return -1
    # Gdal Shift
    origin = (origin_x + x_shift, origin_y + y_shift)
    file_name_new = file_name.replace(".tif", "shifted x_{0} y_{1}.tif".format(x_shift, y_shift))

    try:
        create_raster(file_name_new, list_array, bands, origin, epsg, pixel_width, pixel_height, nan_val=nan_val,
                           rdtype=rdtype, options=options)
        logging.info("Successfully created shifted raster in "+file_name_new)
    except RuntimeError:
        logging.error("Could not create raster using geotools.")
        return -1


    if compress:
        try:
            logging.info("Creating compressed raster to reduce size")
            outfn=file_name_new.replace(".tif", "_compressed.tif")
            ds = gdal.Translate(outfn, file_name_new, creationOptions=compress_config)
            ds = None
            logging.info("Successfully created compressed tiff in "+outfn)
        except RuntimeError:
            logging.error("Unable to preform compression")

    return 0

def raster2array(file_name, band_number=1):
    """Extracts a numpy ``ndarray`` from a raster.

    Args:
        file_name (str): Target file name, including directory; must end on ``".tif"``.
        band_number (int): The raster band number to open (default: ``1``).

    Returns:
        list: three-elements of [``osgeo.DataSet`` of the raster,
        ``numpy.ndarray`` of the raster ``band_numer`` (input) where no-data
        values are replaced with ``np.nan``, ``osgeo.GeoTransform`` of
         the original raster]
    """
    # open the raster and band (see above)
    raster, band = open_raster(file_name, band_number=band_number)
    try:
        # read array data from band
        band_array = band.ReadAsArray()
    except AttributeError:
        logging.error("Could not read array of raster band type=%s." %
                      str(type(band)))
        return raster, band, nan_value
    try:
        # overwrite NoDataValues with np.nan
        band_array = np.where(
            band_array == band.GetNoDataValue(), np.nan, band_array)
    except AttributeError:
        logging.error(
            "Could not get NoDataValue of raster band type=%s." % str(type(band)))
        return raster, band, nan_value
    # return the array and GeoTransformation used in the original raster
    return raster, band_array, raster.GetGeoTransform()


def remove_tif(file_name):
    """Removes a GeoTIFF and its dependent files (e.g., xml).

    Args:
        file_name (str): Directory (path) and name of a GeoTIFF

    Returns:
        None: Removes the provided ``file_name`` and all dependencies.
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
