from helpers import *


def create_shp(shp_file_dir, overwrite=True, *args, **kwargs):
    """Creates a new shapefile with an optionally defined geometry type.

    Args:
        shp_file_dir (str): of the (relative) shapefile directory (ends on ``".shp"``).
        overwrite (bool): If ``True`` (default), existing files are overwritten.
        layer_name (str): The layer name to be created. If ``None``: no layer will be created.
        layer_type (str): Either ``"point"``, ``"line"``, or ``"polygon"`` of the ``layer_name``. If ``None``: no layer will be created.

    Returns:
        osgeo.ogr.DataSource: An ``ogr`` shapefile (Python object)

    Hint:
        Use the ``layer_name`` and ``layer_type`` kwargs along with each other.
        Keeping these parameters default is deprecated.
    """
    shp_driver = ogr.GetDriverByName("ESRI Shapefile")
    shp_file_dir = verify_shp_name(shp_file_dir)

    # check if output file exists if yes delete it
    if os.path.exists(shp_file_dir):
        if overwrite:
            shp_driver.DeleteDataSource(shp_file_dir)
        else:
            logging.error(
                "Shapefile already exists and overwrite=False. Delete existing shapefile and/or use overwrite=True (default).")
            return None

    # create and return new shapefile object
    new_shp = shp_driver.CreateDataSource(shp_file_dir)

    # create layer if layer_name and layer_type are provided
    if kwargs.get("layer_name") and kwargs.get("layer_type"):
        # create dictionary of ogr.SHP-TYPES
        geometry_dict = {"point": ogr.wkbPoint,
                         "points": ogr.wkbMultiPoint,
                         "line": ogr.wkbMultiLineString,
                         "polygon": ogr.wkbMultiPolygon}
        # create layer
        try:
            new_shp.CreateLayer(str(kwargs.get("layer_name")),
                                geom_type=geometry_dict[str(kwargs.get("layer_type").lower())])
        except KeyError:
            print(
                "Error: Invalid layer_type provided (must be 'point', 'line', or 'polygon').")
        except TypeError:
            print("Error: layer_name and layer_type must be string.")
        except AttributeError:
            print("Error: Cannot access layer - opened in other program?")
    return new_shp


def get_geom_description(layer):
    """Gets the WKB Geometry Type as string from a shapefile layer.

    Args:
        layer (osgeo.ogr.Layer): A shapefile layer.

    Returns:
        str:  WKB (binary) geometry type
    """
    type_dict = {0: "wkbUnknown", 1: "wkbPoint", 2: "wkbLineString", 3: "wkbPolygon",
                 4: "wkbMultiPoint", 5: "wkbMultiLineString", 6: "wkbMultiPolygon",
                 7: "wkbGeometryCollection", 8: "wkbCircularString", 9: "wkbCompoundCurve",
                 10: "wkbCurvePolygon", 11: "wkbMultiCurve", 12: "wkbMultiSurface",
                 13: "wkbCurve", 14: "wkbSurface", 15: "wkbPolyhedralSurface", 16: "wkbTIN",
                 17: "wkbTriangle", 100: "wkbNone", 101: "wkbLinearRing", 1008: "wkbCircularStringZ",
                 1009: "wkbCompoundCurveZ", 1010: "wkbCurvePolygonZ", 1011: "wkbMultiCurveZ",
                 1012: "wkbMultiSurfaceZ", 1013: "wkbCurveZ", 1014: "wkbSurfaceZ",
                 1015: "wkbPolyhedralSurfaceZ", 1016: "wkbTINZ", 1017: "wkbTriangleZ",
                 2001: "wkbPointM", 2002: "wkbLineStringM", 2003: "wkbPolygonM", 2004: "wkbMultiPointM",
                 2005: "wkbMultiLineStringM", 2006: "wkbMultiPolygonM", 2007: "wkbGeometryCollectionM",
                 2008: "wkbCircularStringM", 2009: "wkbCompoundCurveM", 2010: "wkbCurvePolygonM",
                 2011: "wkbMultiCurveM", 2012: "wkbMultiSurfaceM", 2013: "wkbCurveM", 2014: "wkbSurfaceM",
                 2015: "wkbPolyhedralSurfaceM", 2016: "wkbTINM", 2017: "wkbTriangleM", 3001: "wkbPointZM",
                 3002: "wkbLineStringZM", 3003: "wkbPolygonZM", 3004: "wkbMultiPointZM",
                 3005: "wkbMultiLineStringZM", 3006: "wkbMultiPolygonZM", 3007: "wkbGeometryCollectionZM",
                 3008: "wkbCircularStringZM", 3009: "wkbCompoundCurveZM", 3010: "wkbCurvePolygonZM",
                 3011: "wkbMultiCurveZM", 3012: "wkbMultiSurfaceZM", 3013: "wkbCurveZM",
                 3014: "wkbSurfaceZM", 3015: "wkbPolyhedralSurfaceZM", 3016: "wkbTINZM", 3017: "wkbTriangleZM",
                 -2147483647: "wkbPoint25D", -2147483646: "wkbLineString25D", -2147483645: "wkbPolygon25D",
                 -2147483644: "wkbMultiPoint25D", -2147483643: "wkbMultiLineString25D",
                 -2147483642: "wkbMultiPolygon25D", -2147483641: "wkbGeometryCollection25D"}
    try:
        geom_type = layer.GetGeom()
    except AttributeError:
        logging.error(
            "Invalid input: %s is empty or not osgeo.ogr.Layer." % str(layer))
        return type_dict[0]
    try:
        return type_dict[geom_type]
    except KeyError:
        logging.error("Unknown WKB Geometry Type.")
        return type_dict[0]


def get_geom_simplified(layer):
    """Gets a simplified geometry description (either point, line, or polygon)
     as a function of the WKB Geometry Type of a shapefile layer.

    Args:
        layer (osgeo.ogr.Layer): A shapefile layer.

    Returns:
        str: Either WKT-formatted point, line, or polygon (or unknown if invalid layer).
    """
    wkb_geom = get_geom_description(layer)
    if "point" in wkb_geom.lower():
        return "point"
    if "line" in wkb_geom.lower():
        return "line"
    if "polygon" in wkb_geom.lower():
        return "polygon"
    return "unknown"


def verify_shp_name(shp_file_name, shorten_to=13):
    """Ensure that the shapefile name does not exceed 13 characters.
    Otherwise, the function shortens the ``shp_file_name`` length to
    ``shorten_to=N`` characters.

    Args:
        shp_file_name (str): A shapefile name (with directory e.g., ``"C:/temp/poly.shp"``).
        shorten_to (int): The number of characters the shapefile name should have (default: ``13``).

    Returns:
        str: A shapefile name (including path if provided) with a length of ``shorten_to``.
    """
    pure_fn = shp_file_name.split(".shp")[0].split("/")[-1].split("\\")[-1]
    shp_dir = shp_file_name.strip(shp_file_name.split("/")[-1].split("\\")[-1])

    if pure_fn.__len__() > shorten_to:
        print("Shapefile name too long (applying auto-shortening to %s characters)." %
              str(shorten_to))
        return shp_dir + pure_fn[0: shorten_to - 1] + ".shp"
    else:
        return shp_file_name


def polygon_from_shapepoints(shapepoints, polygon, alpha=np.nan):
    """Creates a polygon around a cloud of ``shapepoints``.

    Args:
        shapepoints (str): Point shapefile name, including its directory.
        polygon (str): Target shapefile filename, including its directory.
        alpha (float): Coefficient to adjust; the lower it is, the more slim will be the polygon.

    Returns:
        None: Creates the polygon shapefile defined with ``polygon``.
    """
    gdf = geopandas.read_file(shapepoints)

    # If the user doesnt select an alpha value, the alpha will be optimized automatically.
    if np.isfinite(alpha):
        try:
            poly = alphashape.alphashape(gdf, alpha)
            poly.to_file(polygon)
        except FileNotFoundError as err:
            print(err)
    else:
        try:
            poly = alphashape.alphashape(gdf)
        except FileNotFoundError as err:
            print(err)
        else:
            poly.to_file(polygon)
