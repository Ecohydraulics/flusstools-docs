"""``geotools`` is a package for creating, modifying, and transforming geospatial datasets."""


from .kml import *
from .srs_mgmt import *
gdal.UseExceptions()


def float2int(raster_file_name, band_number=1):
    """Converts a float number raster to an integer raster (required for converting a raster to a polygon shapefile).

    Args:
        raster_file_name (str): Target file name, including directory; must end on ``".tif"``.
        band_number (int): The raster band number to open (default: ``1``).

    Returns:
        str: ``"path/to/ew_raster_file.tif"``
    """

    raster, array, geo_transform = raster2array(
        raster_file_name, band_number=band_number)
    try:
        array = array.astype(int)
    except ValueError:
        logging.error("! Invalid raster pixel values.")
        return raster_file_name
    new_name = raster_file_name.split(".tif")[0] + "_int.tif"

    # get source coordinate system and exit function if not possible
    src_srs = get_srs(raster)
    if not src_srs:
        # ensure consistency
        return raster_file_name

    # create integer raster
    print(" * info: creating integer raster to Polygonize:\n   >> %s" % new_name)
    create_raster(new_name, array, epsg=int(src_srs.GetAuthorityCode(None)),
                  rdtype=gdal.GDT_Int32, geo_info=geo_transform)
    return new_name


def raster2line(raster_file_name, out_shp_fn, pixel_value, max_distance_method="simplified"):
    """Converts a raster to a line shapefile, where ``pixel_value`` determines line start and end points.

    Args:
        raster_file_name (str): of input raster file name, including directory; must end on ``".tif"``.
        out_shp_fn (str): of target shapefile name, including directory; must end on ``".shp"``.
        pixel_value (``int`` or ``float``): Pixel values to connect.
        max_distance_method (str): change to (pixel) ``"width"`` or ``"height"`` to force lines to exactly follow pixels (no triangulation).

     Returns:
        None: Writes a new shapefile to disk.
    """

    # calculate max. distance between points
    # ensures correct neighbourhoods for start and end pts of lines
    raster, array, geo_transform = raster2array(raster_file_name)
    pixel_width = geo_transform[1]

    # verify if user provided max_distance_method argument
    if not max_distance_method == "simplified":
        if "height" in max_distance_method:
            max_distance = geo_transform[1]
        else:
            # assume that user want pixel width
            max_distance = pixel_width
    else:
        max_distance = np.ceil(np.sqrt(2 * pixel_width**2))

    # extract pixels with the user-defined pixel value from the raster array
    trajectory = np.where(array == pixel_value)
    if np.count_nonzero(trajectory) == 0:
        logging.error(
            "! The defined pixel_value (%s) does not occur in the raster band." % str(pixel_value))
        return None

    # convert pixel offset to coordinates and append to nested list of points
    points = []
    count = 0
    for offset_y in trajectory[0]:
        offset_x = trajectory[1][count]
        points.append(offset2coords(geo_transform, offset_x, offset_y))
        count += 1

    # create multiline (write points dictionary to line geometry (wkbMultiLineString)
    multi_line = ogr.Geometry(ogr.wkbMultiLineString)
    for i in itertools.combinations(points, 2):
        point1 = ogr.Geometry(ogr.wkbPoint)
        point1.AddPoint(i[0][0], i[0][1])
        point2 = ogr.Geometry(ogr.wkbPoint)
        point2.AddPoint(i[1][0], i[1][1])

        distance = point1.Distance(point2)
        if distance < max_distance:
            line = ogr.Geometry(ogr.wkbLineString)
            line.AddPoint(i[0][0], i[0][1])
            line.AddPoint(i[1][0], i[1][1])
            multi_line.AddGeometry(line)

    # write multiline (wkbMultiLineString2shp) to shapefile
    new_shp = create_shp(
        out_shp_fn, layer_name="raster_pts", layer_type="line")
    lyr = new_shp.GetLayer()
    feature_def = lyr.GetLayerDefn()
    new_line_feat = ogr.Feature(feature_def)
    new_line_feat.SetGeometry(multi_line)
    lyr.CreateFeature(new_line_feat)

    # create projection file
    srs = get_srs(raster)
    make_prj(out_shp_fn, int(srs.GetAuthorityCode(None)))
    print(" * success (raster2line): wrote %s" % str(out_shp_fn))


def raster2polygon(file_name, out_shp_fn, band_number=1, field_name="values"):
    """Converts a raster to a polygon shapefile.

    Args:
        file_name (str): Target file name, including directory; must end on ``".tif"``
        out_shp_fn (str): Shapefile name (with directory e.g., ``"C:/temp/poly.shp"``)
        band_number (int): Raster band number to open (default: ``1``)
        field_name (str): Field name where raster pixel values will be stored (default: ``"values"``)
        add_area (bool): If ``True``, an "area" field will be added, where the area in the shapefiles unit system is calculated (default: ``False``)

     Returns:
        osgeo.ogr.DataSource: Python object of the provided ``out_shp_fn``.
    """
    logging.info(" * Polygonizing %s ..." % str(file_name))
    # ensure that the input raster contains integer values only and open the input raster
    file_name = float2int(file_name)
    raster, raster_band = open_raster(file_name, band_number=band_number)

    # create new shapefile with the create_shp function
    new_shp = create_shp(
        out_shp_fn, layer_name="raster_data", layer_type="polygon")
    dst_layer = new_shp.GetLayer()

    # create new field to define values
    new_field = ogr.FieldDefn(field_name, ogr.OFTInteger)
    dst_layer.CreateField(new_field)

    # Polygonize(band, hMaskBand[optional]=None, destination lyr, field ID, papszOptions=[], callback=None)
    gdal.Polygonize(raster_band, None, dst_layer, 0, [], callback=None)

    # create projection file
    srs = get_srs(raster)
    make_prj(out_shp_fn, int(srs.GetAuthorityCode(None)))
    logging.info(" * success (Polygonize): wrote %s" % str(out_shp_fn))
    return new_shp


def rasterize(in_shp_file_name, out_raster_file_name, pixel_size=10, no_data_value=-9999,
              rdtype=gdal.GDT_Float32, overwrite=True, interpolate_gap_pixels=False, **kwargs):
    """Converts any ESRI shapefile to a raster.

    Args:
        in_shp_file_name (str): A shapefile name (with directory e.g., ``"C:/temp/poly.shp"``)
        out_raster_file_name (str): Target file name, including directory; must end on ``".tif"``
        pixel_size (float): Pixel size as multiple of length units defined in the spatial reference (default: ``10``)
        no_data_value (int OR float): Numeric value for no-data pixels (default: ``-9999``)
        rdtype (gdal.GDALDataType): The raster data type (default: ``gdal.GDT_Float32`` (32 bit floating point)
        overwrite (bool): Overwrite existing files (default: ``True``)
        interpolate_gap_pixels (bool): Fill empty pixels that are not touched by a shapefile element with interpolated values (default: ``False``)

    Keyword Args:
        field_name (str): Name of the shapefile's field with values to burn to raster pixel values.
        radius1 (float): Define the x-radius for interpolating pixels (default: ``-1``, corresponding to infinity). Only applicable ``with interpolate_gap_pixels``.
        radius2 (float): Define the y-radius for interpolating pixels (default: ``-1``, corresponding to infinity). Only applicable ``with interpolate_gap_pixels``.
        power (float): Power of the function for interpolating pixel values (default: ``1.0``, corresponding to linear).
        smoothing (float): Smoothing parameter for interpolating pixel values (default: ``0.0``).
        min_points (int): Minimum number of points to use for interpolation. If the interpolator cannot find at least ``min_points`` for a pixel, it assigns a ``no_data`` value to that pixel  (default: ``0``).
        max_points (int): Maximum number of points to use for interpolation. The interpolator will not use more than ``max_points`` closest points to interpolate a pixel value (default: ``0``).


    Hints:
        More information on pixel value interpolation:
        ``interpolate_gap_pixels=True`` interpolates values at pixels that are not touched by any las point.
        The pixel value interpolation uses ``gdal_grid`` (i.e., its Python bindings through ``gdal.Grid()``).
        Control the interpolation parameters with the keyword arguments ``radius1``, ``radius2``, ``power``, ``max_points``, ``min_points``,  and ``smoothing``..

    Returns:
        int: Creates the GeoTIFF raster defined with ``out_raster_file_name`` (success: ``0``, otherwise ``None``).
    """

    default_keys = {"radius1": -1,
                    "radius2": -1,
                    "power": 1.0,
                    "smoothing": 0.0,
                    "min_points": 0,
                    "max_points": 0,
                    }

    for k in default_keys.keys():
        if kwargs.get(k):
            default_keys[k] = str(kwargs.get(k))

    # check if any action is required
    if os.path.isfile(out_raster_file_name) and not overwrite:
        logging.info(" * %s already exists. Nothing to do." %
                     out_raster_file_name)
        return None

    # open data source
    try:
        source_ds = ogr.Open(in_shp_file_name)
    except RuntimeError as err:
        logging.error("! Could not open %s." % str(in_shp_file_name))
        return None
    source_lyr = source_ds.GetLayer()

    # read extent
    x_min, x_max, y_min, y_max = source_lyr.GetExtent()

    # get x and y resolution in number of pixel
    x_res = int((x_max - x_min) / pixel_size)
    y_res = int((y_max - y_min) / pixel_size)

    # get spatial reference system and assign to raster
    srs = get_srs(source_ds)
    try:
        srs.ImportFromEPSG(int(srs.GetAuthorityCode(None)))
    except RuntimeError as err:
        logging.error(e)
        return None

    if float(pixel_size) < 1.0:
        logging.info(
            "   -- Yeek! This will be a high resolution raster. Be prepared that your system resources will be occupied for a while.")

    # use gdal.Grid if gap interpolation (fill void pixels) is True
    if interpolate_gap_pixels:
        logging.info(
            " * Creating gridded raster with interpolated values for empty pixels from neighbouring pixels ...")
        logging.info(
            "   -- Note: to deactivate pixel value interpolation option use interpolate_gap_pixels=False")

        try:
            algorithm = "invdist:power={0}:radius1={1}:radius2={2}:smoothing={3}:min_points={4}:max_points={5}".format(
                str(default_keys["power"]), str(
                    default_keys["radius1"]), str(default_keys["radius2"]),
                str(default_keys["smoothing"]), str(
                    default_keys["min_points"]), str(default_keys["max_points"])
            )

            gdal.Grid(out_raster_file_name, in_shp_file_name,
                      algorithm=algorithm,
                      zfield=kwargs.get("field_name"),
                      outputType=rdtype,
                      outputSRS=srs,
                      width=x_res,
                      height=y_res,
                      outputBounds=[x_min, y_min, x_max, y_max])
            return 0

        except KeyError:
            logging.error("! Invalid gdal.Grid options provided.")
            return None
        except RuntimeError as err:
            logging.error("! %s." % str(err))

    # create destination data source (GeoTIff raster)
    try:
        target_ds = gdal.GetDriverByName('GTiff').Create(
            out_raster_file_name, x_res, y_res, 1, eType=rdtype)
    except RuntimeError as err:
        logging.error("! Could not create %s." % str(out_raster_file_name))
        return None
    target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
    band = target_ds.GetRasterBand(1)
    band.Fill(no_data_value)
    band.SetNoDataValue(no_data_value)

    # assign spatial reference
    target_ds.SetProjection(srs.ExportToWkt())

    # RasterizeLayer(Dataset dataset, int bands, Layer layer, pfnTransformer=None, pTransformArg=None,
    # int burn_values=0, options=None, GDALProgressFunc callback=0, callback_data=None)
    try:
        if kwargs.get("field_name"):
            gdal.RasterizeLayer(target_ds, [1], source_lyr, None, None, burn_values=[0],
                                options=["ALL_TOUCHED=TRUE", "ATTRIBUTE=" + str(kwargs.get("field_name"))])
        else:
            gdal.RasterizeLayer(target_ds, [1], source_lyr, None, None, burn_values=[0],
                                options=["ALL_TOUCHED=TRUE"])
    except RuntimeError as err:
        logging.error("! Could not rasterize (burn values from %s)." %
                      str(in_shp_file_name))
        return None

    # release raster band
    band.FlushCache()
