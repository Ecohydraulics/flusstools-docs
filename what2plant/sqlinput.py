"""
Description
"""

import os, sys
sys.path.insert(0, os.path.abspath("."))
from import_mgmt import *

connection = sqlite3.connect("Pflanzendaten.db")
cursor = connection.cursor()


sql_command ="""
CREATE TABLE IF NOT EXISTS plants (
species VARCHAR(255),
name VARCHAR(255),
nativ BOOLEAN,
endangered VARCHAR(255),
habitat VARCHAR(255),
waterdepthmin INTEGER(255),
waterdepthmax  INTEGER(255),
rootdepth INTEGER(255),
groundwatertablechange VARCHAR(255),
floodheightmax INTEGER(255),
floodloss REAL(255),
floodduration INTEGER(255),
PRIMARY KEY (species, name, habitat)
);"""

cursor.execute(sql_command)


def inputquestion():
    """function that lets the user put data into the database

    the function provides 2 options for data input, if option 1 is chosen via console input "1", the user can provide the name of a csv file
    if option 2 is chosen, the user can add a single row via sql command. If neither of those two options is chosen, the function will print a string in the python console

    Returns:
        string in console if none of the two options above is chosen

    """
    print('Enter 1 to input data from csv file\n Enter 2 to input data via sql command')
    src = int(input('Enter here:'))
    if src == 1:

        with open(input('enter csv-filename')+'.csv') as csvfile:
            csv_reader_object = csv.reader(csvfile, delimiter=',')
            with sqlite3.connect("Pflanzendaten.db") as connection:
                cursor = connection.cursor()
                sql_command = """
                INSERT INTO plants (species,name,nativ,endangered,habitat,waterdepthmin,waterdepthmax,rootdepth,groundwatertablechange,floodheightmax,floodloss,floodduration)
                VALUES (:species, :name, :nativ, :endangered, :habitat, :waterdepthmin, :waterdepthmax, :rootdepth, :groundwatertablechange, :floodheightmax, :floodloss, :floodduration)
                """
                cursor.executemany(sql_command, csv_reader_object)
    elif src == 2:
        connection = sqlite3.connect("Pflanzendaten.db")
        cursor = connection.cursor()
        sql_command = (input("""Insert sql command"""))
        cursor.execute(sql_command)
        cursor.execute("COMMIT")
    else:
        print('only able to import data to table using csv file or sql command')


inputquestion()
cursor.execute("SELECT * FROM plants")
content = cursor.fetchall()
print(content)




