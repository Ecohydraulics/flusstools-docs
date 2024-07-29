from .dataset_mgmt import *


def get_esriwkt(epsg):
    """Gets esriwkt-formatted spatial references with epsg code online.

    Args:
        epsg (int): EPSG Authority Code

    Returns:
        str: An esriwkt string (if an error occur, the default epsg=``4326`` is used).

    Example:
        Call this function with ``get_esriwkt(4326)`` to get a return, such as
        ``'GEOGCS["GCS_WGS_1984",DATUM[...],...]``.

    Hint:
        This function requires an internet connection:
        Loads spatial reference codes as ``"https://spatialreference.org/ref/sr-org/{0}/esriwkt/".format(epsg)``
        For instance, ``epsg=3857`` yields ``"https://spatialreference.org/ref/sr-org/3857/esriwkt/"``
    """
    try:
        with urllib.request.urlopen("http://spatialreference.org/ref/epsg/{0}/esriwkt/".format(epsg)) as response:
            return str(response.read()).strip("b").strip("'")
    except Exception:
        pass
    try:
        with urllib.request.urlopen(
                "http://spatialreference.org/ref/sr-org/epsg{0}-wgs84-web-mercator-auxiliary-sphere/esriwkt/".format(
                    epsg)) as response:
            return str(response.read()).strip("b").strip("'")

    except Exception as e:
        logging.error(
            "Could not find epsg code on spatialreference.org. Returning default WKT(epsg=4326).")
        print(e)
        return 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295],UNIT["Meter",1]]'


def get_srs(dataset):
    """Gets the spatial reference of any ``gdal.Dataset``.

    Args:
        dataset (gdal.Dataset): A shapefile or raster.

    Returns:
        osr.SpatialReference: A spatial reference object.
    """
    gdal.UseExceptions()

    if verify_dataset(dataset) == "raster":
        sr = osr.SpatialReference()
        sr.ImportFromWkt(dataset.GetProjection())
    else:
        try:
            sr = osr.SpatialReference(str(dataset.GetLayer().GetSpatialRef()))
        except AttributeError:
            logging.error("Invalid source data (%s)." % str(dataset))
            return osr.SpatialReference()
    # auto-detect epsg
    try:
        auto_detect = sr.AutoIdentifyEPSG()
        if auto_detect != 0:
            # Find matches returns list of tuple of SpatialReferences
            sr = sr.FindMatches()[0][0]
            sr.AutoIdentifyEPSG()
    except TypeError:
        logging.error("Empty spatial reference.")
        return osr.SpatialReference()
    # assign input SpatialReference
    try:
        sr.ImportFromEPSG(int(sr.GetAuthorityCode(None)))
    except TypeError:
        logging.error(
            "Could not retrieve authority code (EPSG import failed).")
    return sr


def get_wkt(epsg, wkt_format="esriwkt"):
    """Gets WKT-formatted projection information for an epsg code using the ``osr`` library.

    Args:
        epsg (int): epsg Authority code
        wkt_format (str): of wkt format (default is esriwkt for shapefile projections)

    Returns:
        str: WKT (if error: returns default corresponding to ``epsg=4326``).
    """
    default = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295],UNIT["Meter",1]]'
    spatial_ref = osr.SpatialReference()
    try:
        spatial_ref.ImportFromEPSG(epsg)
    except TypeError:
        logging.error(
            "epsg must be integer. Returning default WKT(epsg=4326).")
        return default
    except Exception:
        logging.error(
            "epsg number does not exist. Returning default WKT(epsg=4326).")
        return default
    if wkt_format == "esriwkt":
        spatial_ref.MorphToESRI()
    return spatial_ref.ExportToPrettyWkt()


def make_prj(shp_file_name, epsg):
    """Generates a projection file for a shapefile.

    Args:
        shp_file_name (str): of a shapefile name (with directory e.g., ``"C:/temp/poly.shp"``).
        epsg (int): EPSG Authority Code

    Returns:
        None: Creates a projection file (``.prj``) in the same directory and
        with the same name of ``shp_file_name``.
    """
    shp_dir = shp_file_name.strip(shp_file_name.split("/")[-1].split("\\")[-1])
    shp_name = shp_file_name.split(".shp")[0].split("/")[-1].split("\\")[-1]
    with open(r"" + shp_dir + shp_name + ".prj", "w+") as prj:
        prj.write(get_wkt(epsg))


def reproject(source_dataset, new_projection_dataset):
    """Re-projects a dataset (raster or shapefile) onto the spatial reference system
    of a (shapefile or raster) layer.

    Args:
        source_dataset (gdal.Dataset): Shapefile or raster.
        new_projection_dataset (gdal.Dataset): Shapefile or raster with new projection info.

    Returns:
        None: **If the source is a raster**, the function creates a GeoTIFF in same directory as ``source_dataset`` with a ``"_reprojected"`` suffix in the file name.
        **If the source is a shapefile**, the function creates a shapefile in same directory as ``source_dataset`` with a ``"_reprojected"`` suffix in the file name.
    """

    # get source and target spatial reference systems
    srs_src = get_srs(source_dataset)
    srs_tar = get_srs(new_projection_dataset)

    # get dictionary of layer type and layer (or band=layer)
    layer_dict = get_layer(source_dataset)

    if layer_dict["type"] == "raster":
        reproject_raster(source_dataset, srs_src, srs_tar)

    if layer_dict["type"] == "vector":
        reproject_shapefile(
            source_dataset, layer_dict["layer"], srs_src, srs_tar)


def reproject_raster(source_dataset, source_srs, target_srs):
    """Re-projects a raster dataset. This function is called by the ``reproject`` function.

    Args:
        source_dataset (osgeo.ogr.DataSource): Instantiates with an ``ogr.Open(SHP-FILE)``.
        source_srs (osgeo.osr.SpatialReference): Instantiates with ``get_srs(source_dataset)``
        target_srs (osgeo.osr.SpatialReference): Instantiates with ``get_srs(DATASET-WITH-TARGET-PROJECTION)``.

    Returns:
        None: Creates a new GeoTIFF raster in the same directory where ``source_dataset`` lives.
    """
    # READ THE SOURCE GEO TRANSFORMATION (ORIGIN_X, PIXEL_WIDTH, 0, ORIGIN_Y, 0, PIXEL_HEIGHT)
    src_geo_transform = source_dataset.GetGeoTransform()

    # DERIVE PIXEL AND RASTER SIZE
    pixel_width = src_geo_transform[1]
    x_size = source_dataset.RasterXSize
    y_size = source_dataset.RasterYSize

    # ensure that TransformPoint (later) uses (x, y) instead of (y, x) with gdal version >= 3.0
    source_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    target_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

    # get CoordinateTransformation
    coord_trans = osr.CoordinateTransformation(source_srs, target_srs)

    # get boundaries of reprojected (new) dataset
    (org_x, org_y, org_z) = coord_trans.TransformPoint(
        src_geo_transform[0], src_geo_transform[3])
    (max_x, min_y, new_z) = coord_trans.TransformPoint(src_geo_transform[0] + src_geo_transform[1] * x_size,
                                                       src_geo_transform[3] + src_geo_transform[5] * y_size, )

    # INSTANTIATE NEW (REPROJECTED) IN-MEMORY DATASET AS A FUNCTION OF THE RASTER SIZE
    mem_driver = gdal.GetDriverByName('MEM')
    tar_dataset = mem_driver.Create("",
                                    int((max_x - org_x) / pixel_width),
                                    int((org_y - min_y) / pixel_width),
                                    1, gdal.GDT_Float32)
    # create new GeoTransformation
    new_geo_transformation = (org_x, pixel_width, src_geo_transform[2],
                              org_y, src_geo_transform[4], -pixel_width)

    # assign the new GeoTransformation to the target dataset
    tar_dataset.SetGeoTransform(new_geo_transformation)
    tar_dataset.SetProjection(target_srs.ExportToWkt())

    # PROJECT THE SOURCE RASTER ONTO THE NEW REPROJECTED RASTER
    rep = gdal.ReprojectImage(source_dataset, tar_dataset,
                              source_srs.ExportToWkt(), target_srs.ExportToWkt(),
                              gdal.GRA_Bilinear)

    # SAVE REPROJECTED DATASET AS GEOTIFF
    src_file_name = source_dataset.GetFileList()[0]
    tar_file_name = src_file_name.split(
        ".tif")[0] + "_epsg" + target_srs.GetAuthorityCode(None) + ".tif"
    create_raster(tar_file_name, raster_array=tar_dataset.ReadAsArray(),
                  epsg=int(target_srs.GetAuthorityCode(None)),
                  geo_info=tar_dataset.GetGeoTransform())
    logging.info("Saved reprojected raster as %s" % tar_file_name)


def reproject_shapefile(source_dataset, source_layer, source_srs, target_srs):
    """Re-projects a shapefile dataset. This function is called by the ``reproject`` function.

    Args:
        source_dataset (osgeo.ogr.DataSource): Instantiates with ``ogr.Open(SHP-FILE)``.
        source_layer (osgeo.ogr.Layer ): Instantiates with ``source_dataset.GetLayer()``.
        source_srs (osgeo.osr.SpatialReference): Instantiates with ``get_srs(source_dataset)``.
        target_srs (osgeo.osr.SpatialReference): Instantiates with ``get_srs(DATASET-WITH-TARGET-PROJECTION)``.

    Returns:
        None: Creates a new shapefile in the same directory where ``source_dataset`` lives.
    """
    # make GeoTransformation
    coord_trans = osr.CoordinateTransformation(source_srs, target_srs)

    # make target shapefile
    tar_file_name = verify_shp_name(source_dataset.GetName(), shorten_to=4).split(".shp")[
                        0] + "_epsg" + target_srs.GetAuthorityCode(None) + ".shp"
    tar_shp = create_shp(
        tar_file_name, layer_type=get_geom_simplified(source_layer))
    tar_lyr = tar_shp.GetLayer()

    # look up layer (features) definitions in input shapefile
    src_lyr_def = source_layer.GetLayerDefn()
    # copy field names of input layer attribute table to output layer
    for i in range(0, src_lyr_def.GetFieldCount()):
        tar_lyr.CreateField(src_lyr_def.GetFieldDefn(i))

    # instantiate feature definitions object for output layer (currently empty)
    tar_lyr_def = tar_lyr.GetLayerDefn()

    try:
        feature = source_layer.GetNextFeature()
    except AttributeError:
        logging.error("Invalid or empty vector dataset.")
        return None
    while feature:
        # get the input geometry
        geometry = feature.GetGeometryRef()
        # re-project (transform) geometry to new system
        geometry.Transform(coord_trans)
        # create new output feature
        out_feature = ogr.Feature(tar_lyr_def)
        # assign in-geometry to output feature and copy field values
        out_feature.SetGeometry(geometry)
        for i in range(0, tar_lyr_def.GetFieldCount()):
            out_feature.SetField(tar_lyr_def.GetFieldDefn(
                i).GetNameRef(), feature.GetField(i))
        # add the feature to the shapefile
        tar_lyr.CreateFeature(out_feature)
        # prepare next iteration
        feature = source_layer.GetNextFeature()

    # add projection file
    make_prj(tar_file_name, int(source_srs.GetAuthorityCode(None)))
