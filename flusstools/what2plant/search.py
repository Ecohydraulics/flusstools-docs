"""
Functions related to search for vegetation matching the users input
"""

from .plant import *


def search_db_via_query(query):
    """Function that checks database for matching entries with user input.

    The function takes the user input and adds it to the used sql command to search for matching entries in the provided database
    if there are matching entries these will be printed in the python console

    Args:
        query (str): habitat name in sql, provided by the user

    Returns:
        table entries matching with user input
    """
    connection = sqlite3.connect("Pflanzendaten.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM plants WHERE " + query)
    content = cursor.fetchall()
    print(tabulate((content), headers=['species', 'name', 'nativ', 'endangered', 'habitat', 'waterdepthmin', 'waterdepthmax', 'rootdepth', 'groundwatertablechange', 'floodheightmax', 'floodloss', 'floodduration']))
    print('Status 1 equals nativ')

    connection.close()


def habitat_search(column, entry):
    """Function searches in csv file for vegetation matching the user input.

    The function uses the console input to search for matching entries in the provided csv file,
    if there are matching entries the function print_habitat gets called to print the information in the python console.

    Args:
        column(str): column in the .csv file
        entry(str): entry in the .csv file

    Returns:
        String in console
    """
    df = pd.read_csv('plantdata.csv', encoding='unicode_escape')
    if platform.system() == 'Linux':
        df = pd.read_csv('plantdata.csv')
    else:
        df = pd.read_csv('plantdata.csv', encoding='unicode_escape')
    df1 = df.dropna()

    def search(column, entry, df):
        df2 = df1.to_numpy()
        column = df[column]
        for i in range(len(column)):
            if column[i] == entry:
                plant = Plant(df2[i, 0], df2[i, 1], df2[i, 2], df2[i, 3], df2[i, 4], df2[i, 5], df2[i, 6], df2[i, 7], df2[i, 8], df2[i, 9], df2[i, 10], df2[11])
                plant.print_habitat()
        else:
            print('')

    search(column, entry, df1)


def search_by_habitat():
    """Function that enables the user to provide habitat input in console.

    The function asks the user to provide the habitat name he wants to search for,
    afterwards the input is given to the habitat_search() function and habitat_search() gets called.

    Returns:
        String in console to let the user know what the Status entries mean
    """
    habitat = input('Enter name of habitat\n')
    habitat_search('habitat', habitat)
    print('Status 1 equals nativ')


def point_in_bound(filename, x, y, area):
    """Function that checks if the coordinates provided by the user are in bound of the shapefile polygon.


    If the provided coordinates are out of bounds, a string will be printed in the console to let the user know,
    if they are matching one of the shapefiles, search_db_via_query() gets called.

    Args:
        filename (str): name of the shapefile
        x (float): x - coordinate
        y (float): y - coordinate
        area (str): name of the study area

    Returns:
        String to console
    """
    file_shape = geopandas.read_file(filename)
    polygon = list(file_shape.geometry)[0]
    point = Point(x, y)
    if polygon.contains(point):
        query = "habitat = '" + area + "'"
        search_db_via_query(query)
        print('Enter 1 if you want elevation data for the coordinates\nEnter 2 if you dont want elevation data')
        src = int(input('Enter here:'))

        if src == 1:
            elevation(x, y)
        elif src == 2:
            print('done')
    else:
        print('\ncoordinates out of \n' + area + '\nplease check provided shapefile for suitable coordinates\n')


def search_by_coordinates():
    """Function that lets the user input coordinates.

    After asking the user to input x and y coordinates, point_in_bound(..) gets called for the 3 provided shapefiles.
    Afterwards the user gets asked if he wants to receive elevation data for the input coordinates.

    Returns:
    """
    print('CRS used is EPSG:3857 \n for reference check https://epsg.io/3857 ')
    x = float(input('Enter x coordinate\n'))
    y = float(input('Enter y coordinate\n'))
    point_in_bound(os.path.abspath("..")+"\Shape\prealpinebavaria.shp", x, y, 'Alpenvorland')
    point_in_bound(os.path.abspath("..")+"\Shape\oberrheinmaintiefland.shp", x, y, 'Oberrheinisches Tiefland')
    point_in_bound(os.path.abspath("..")+"\Shape\Tiefland.shp", x, y, 'Niederrheinisches Tiefland')


def elevation(x, y):
    """Function used to get information about elevation at the provided coordinates.

    Args:
        x (float): x - coordinate
        y (float): y - coordinate

    Returns:
        Elevation data for coordinate input in console
    """
    file = os.path.abspath("..") + "\Shape\Shape.vrt"
    layer = gdal.Open(file)
    gt = layer.GetGeoTransform()
    rasterx = int((x - gt[0]) / gt[1])
    rastery = int((y - gt[3]) / gt[5])
    print('elevation =', layer.GetRasterBand(1).ReadAsArray(rasterx, rastery, 1, 1)[0][0], 'm above sea level')


def question():
    """Function to let the user decide if he wants to search by habitat in csv file, search by habitat in database or search by coordinates.

    The function prints a string in the console to ask the user if he wants to search by entering coordinates or the name of the habitat,
    furthermore it is asking the user if he wants to search by the name of the habitat in the provided csv file or database.
    If option 1 is chosen, user is asked for an habitat name before calling search_db_via_query().

    Args:
        1 (int): calls search_db_via_query()
        2 (int): calls search_by_coordinates()
        3 (int): calls search_by_habitat()

    Returns:
        String in console
    """
    print('Enter 1 to search database by habitat with detailed information\nEnter 2 to search database by coordinates \nEnter 3 to search by habitat in csv file for a quick overview without detail')
    print('habitat search options so far:\n Alpenvorland, Niederrheinisches Tiefland, Oberrheinisches Tiefland')
    src = int(input('Enter here:'))

    if src == 1:
        habitat = input('Enter name of habitat\n')
        query = "habitat = '" + habitat + "'"
        search_db_via_query(query)
    elif src == 2:
        search_by_coordinates()
    elif src == 3:
        search_by_habitat()
    else:
        print('no data')
