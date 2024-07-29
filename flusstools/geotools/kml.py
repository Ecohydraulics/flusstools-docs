"""Modified script (original: Linwood Creekmore III)

Examples:

    output to geopandas dataframe (gdf):
    ``gdf = kmx2other("my-places.kmz", output="gpd")``

    plot the new gdf (use %matplotlib inline in notebooks)
    ``gdf.plot()``

    convert a kml-file to a shapefile
    ``success = kmx2other("my-places.kml", output="shp")``
"""

# from io import BytesIO, StringIO
from zipfile import ZipFile
import re
from .kmx_parser import *


def kmx2other(file, output="df"):
    """Converts a Keyhole Markup Language Zipped (KMZ) or KML file to a pandas dataframe, geopandas geodataframe,
    csv, geojson, or ESRI shapefile.

    Parameters:
        file (str): The  path to a KMZ or KML file.
        output (str): Defines the output type. Valid options are: ``"shapefile"``, ``"shp"``, ``"shapefile"``, or ``"ESRI Shapefile"``.

    Hint:
            The core function is taken from http://programmingadvent.blogspot.com/2013/06/kmzkml-file-parsing-with-python.html

    Returns:
        str: Success message (use ``print(kmx2other(...))`` to see what the function did.)
    """
    r = re.compile(r"(?<=\.)km+[lz]?", re.I)
    try:
        # alternatively, try (re.findall(r"(?<=\.)[\w]+",file))[-1]
        extension = r.search(file).group(0)
    except IOError as e:
        logging.error("I/O error {0}".format(e))
        return -1

    # create buffer file
    if "kml" in extension.lower():
        buffer = file
    elif "kmz" in extension.lower():
        kmz = ZipFile(file, "r")
        v_match = np.vectorize(lambda x: bool(r.search(x)))
        name_array = np.array(kmz.namelist())
        sel = v_match(name_array)
        buffer = kmz.open(name_array[sel][0], "r")
    else:
        raise ValueError(
            "Incorrect file format provided. Retry with a valid KML or KMZ file.")

    # instantiate file parser and handler
    parser = xml.sax.make_parser()
    handler = PlacemarkHandler()
    parser.setContentHandler(handler)
    parser.parse(buffer)

    try:
        # close kmz file (if kmz)
        kmz.close()
    except AttributeError:
        pass
    except NameError:
        pass

    # create pandas dataframe of file handler
    df = pd.DataFrame(handler.mapping).T
    names = list(map(lambda x: x.lower(), df.columns))

    if "description" in names:
        extra_data = df.apply(PlacemarkHandler.htmlizer, axis=1)
        df = df.join(extra_data)

    output = output.lower()

    if (output == "df") or (output == "dataframe") or not output:
        result = df

    elif output == "csv":
        out_filename = file[:-3] + "csv"
        df.to_csv(out_filename, encoding="utf-8", sep="\t")
        result = ("Successfully converted {0} to CSV (written to disk: {1}".format(
            file, out_filename))

    elif (output == "gpd") or (output == "gdf") or (output == "geoframe") or (output == "geodataframe"):
        geos = geopandas.GeoDataFrame(
            df.apply(PlacemarkHandler.spatializer, axis=1))
        result = geopandas.GeoDataFrame(pd.concat([df, geos], axis=1))

    elif (output == "geojson") or (output == "json"):
        geos = geopandas.GeoDataFrame(
            df.apply(PlacemarkHandler.spatializer, axis=1))
        gdf = geopandas.GeoDataFrame(pd.concat([df, geos], axis=1))
        out_filename = file[:-3] + "geojson"
        gdf.to_file(out_filename, driver="GeoJSON")
        validation = geojson.is_valid(
            geojson.load(open(out_filename)))["valid"]
        if validation == "yes":
            result = ("Successfully converted {0} to GeoJSON and output to  disk at {1}".format(
                file, out_filename))
        else:
            raise ValueError(
                "Geojson conversion failed. Try to clean the input data or another file.")

    elif (output == "shapefile") or (output == "shp") or (output == "esri shapefile"):
        geos = geopandas.GeoDataFrame(
            df.apply(PlacemarkHandler.spatializer, axis=1))
        gdf = geopandas.GeoDataFrame(pd.concat([df, geos], axis=1))
        out_filename = file[:-3] + "shp"
        gdf.to_file(out_filename, driver="ESRI Shapefile")

        sf = shapefile.Reader(out_filename)
        if len(sf.shapes()) > 0:
            validation = "yes"
        else:
            validation = "no"
        if validation == "yes":
            result = ("Successfully converted {0} to Shapefile and output to disk at {1}".format(
                file, out_filename))
        else:
            raise ValueError(
                "Shapefile conversion did not create a valid shapefile object.\nTry to clean up the input data or another file.")
    else:
        raise ValueError(
            "Conversion returned no data; check if a correct output file type was provided.\nValid output types are geojson, shapefile, csv, geodataframe, and/or pandas dataframe.")

    return result
