"""Original Classes written by Linwood Creekmore III (modified for flusstools)

Flavored with code blocks from:

- http://programmingadvent.blogspot.com/2013/06/kmzkml-file-parsing-with-python.html
- http://gis.stackexchange.com/questions/159681/geopandas-cant-save-geojson
- https://gist.github.com/mciantyre/32ff2c2d5cd9515c1ee7

"""

from helpers import *

import ast
import xml.sax
import xml.sax.handler
from html.parser import HTMLParser


class ModHTMLParser(HTMLParser):
    """A child of HTMLParser, tailored (modified) for kml/kmy parsing."""

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_table = False
        self.mapping = {}
        self.buffer = ""
        self.name_tag = ""
        self.series = pd.Series()

    def handle_starttag(self, tag, attrs):
        """Enables a table if a table-tag is provided.

        Args:
            tag (str): Set to "table" for enabling usage of a table.
            attrs (list): List of additional attributes (currently unused).

        Returns:
            None: Verifies if the ``tag`` argument contains the string ``"table"``
        """

        if tag == "table":
            self.in_table = True

    def handle_data(self, data):
        """Generates mapping and series if ``in_table`` is ``True``.

        Args:
            data (str): Text lines of data divided by colons.

        Returns:
            None: Assigns ``ModHTMLParser.mapping`` and ``ModHTMLParser.series`` attributes
        """
        if self.in_table:
            self.buffer = data.strip(" \n\t").split(":")
            if len(self.buffer) == 2:
                self.mapping[self.buffer[0]] = self.buffer[1]
                self.series = pd.Series(self.mapping)


class PlacemarkHandler(xml.sax.handler.ContentHandler):
    """Child of ``xml.sax.handler.ContentHandler``, tailored for handling kml files."""

    def __init__(self):
        #super().__init__()
        self.inName = False  # handle XML parser events
        self.inPlacemark = False
        self.mapping = {}
        self.buffer = ""
        self.name_tag = ""

    def start_element(self, name):
        """Looks for the first Placemark element in a kml file.

        Args:
            name (str): Name-tag of the element

        Returns:
            None
        """

        if name == "Placemark":
            self.inPlacemark = True
            self.buffer = ""

        if self.inPlacemark:
            if name == "name":
                # save name text to follow
                self.inName = True

    def characters(self, data):
        """Adds a line of data to the read-buffer.

        Args:
            data (str)

        Returns:
            None
        """
        if self.inPlacemark:
            # save text if in title in tag
            self.buffer += data

    def end_element(self, name):
        """Sets the end (last) element.

        Args:
            name (str)

        Returns:
            None
        """
        self.buffer = self.buffer.strip("\n\t")

        if name == "Placemark":
            # clear the current placemark and name
            self.inPlacemark = False
            self.name_tag = ""
        elif name == "name" and self.inPlacemark:
            # on end title tag
            self.inName = False
            self.name_tag = self.buffer.strip()
            self.mapping[self.name_tag] = {}
        elif self.inPlacemark and self.name_tag:
            try:
                if name in self.mapping[self.name_tag]:
                    self.mapping[self.name_tag][name] += self.buffer
                else:
                    self.mapping[self.name_tag][name] = self.buffer
            except KeyError:
                pass
        self.buffer = ""

    def spatializer(row):
        """Converts string objects to spatial Python objects.

        Args:
            row (pandas.df): List of strings for conversion

        Returns:
            None
        """

        try:
            # check if the coordinates column exists
            data = row["coordinates"].strip(" \t\n\r")
        except KeyError:
            pass
        except AttributeError:
            pass

        lsp = data.strip().split(" ")
        linestring = map(lambda x: ast.literal_eval(x), lsp)
        try:
            spatial = Polygon(LineString(linestring))
            converted_poly = pd.Series({"geometry": spatial})
            return converted_poly
        except:
            try:
                g = ast.literal_eval(data)
                points = pd.Series({"geometry": Point(g[:2]),
                                    "altitude": g[-1]})
                return points
            except:
                pass

        try:
            # check if there are latitude and longitude columns
            point = Point(float(row["longitude"]), float(row["latitude"]))
            converted_poly = pd.Series({"geometry": point})
            return converted_poly
        except KeyError:
            pass

    def htmlizer(row):
        """Creates an html file.

        Args:
            row (pandas.df): List of strings for conversion

        Returns:
            htmlparser.series: An instance of the ``ModHTMLParser()`` class
        """
        htmlparser = ModHTMLParser()
        htmlparser.feed(row["description"])
        return htmlparser.series
