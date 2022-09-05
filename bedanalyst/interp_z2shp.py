from geotools import *
from shapely.geometry import Point
from scipy import interpolate


def interp_z2shp(df, lonlat, crs, sample_column, interp_at_z_stamps, new_attr_names, meas_at_cols, path_shp):
    """Interpolates vertical riverbed measurements (e.g., kf, IDOS) to desired z (vertical) stamps, enters them as attributes
    for creating a point shapefile

    Args:
        df (pandas.DataFrame): df with rows indicating samples and columns indicating parameters
        lonlat (tuple of str): name of the columns containing longitude and latitude, respectively (x, y)
        crs (str): of type 'epsg:xxxx or xxxxx', coordinate system of the input longitude and latitude values
        sample_column (str): name of the column in the df which contains the sample names
        interp_at_z_stamps (numpy.array of floats): contains the z (vertical) stamps where the measurement should be interpolated
        new_attr_names (list of str): names of the attributes referring to the selected new z stamps.
        meas_at_cols (tuple of str): contains the column names as a tuple (z_stamp, measurement) of the df that have the vertical spatial stamp of the measurement and the value measured at the corresponding z stamp.
        path_shp (str): path to save the shapefile

    Returns:
        geopandas.GeoDataFrame

    """
    standard_df = pd.DataFrame([], columns=new_attr_names)
    z_stamps, values = meas_at_cols[0], meas_at_cols[1]
    lon, lat = lonlat[0], lonlat[1]
    # loop through sample names at the indicated df-column
    for sam in df[sample_column].unique().tolist():
        sample_df = df[df[sample_column] == sam]
        sample_array = sample_df[values].to_numpy()
        sample_array_depth = sample_df[z_stamps].to_numpy()
        f = interpolate.interp1d(sample_array_depth, sample_array, bounds_error=False)
        value_new = f(interp_at_z_stamps)
        dict_to_conv = dict(zip(new_attr_names, list(value_new)))
        dict_to_conv.update({'lat': sample_df[lat].iloc[0],
                             'lon': sample_df[lon].iloc[0]})
        value_new_per_sample = pd.DataFrame(dict_to_conv, index=[sam])
        standard_df = pd.concat([standard_df, value_new_per_sample])

    # df to gdf
    standard_df['geometry'] = standard_df.apply(lambda x: Point((float(x.lon), float(x.lat))), axis=1)
    gdf = gpd.GeoDataFrame(standard_df, geometry='geometry')
    gdf.crs = crs

    # gdf to shp
    gdf.to_file(path_shp, driver='ESRI Shapefile', index=True)

    return gdf

