Plant database
======================================

.. documentation master file.

Nature-Based Solutions (NBS) for river engineering experience increasing popularity to leverage flood risk and ecosystem management in the light of climate change. Even though the demand for NBS is high, their design regarding scale and placement still is an important challenge. In some cases, missing knowledge and trust in NBS lead to overestimations of costs and time. This plant database constitutes an important step in the design of NBS with a plant data base for river engineering.


.. This documentation is also as available as style-adapted PDF (`download <https://.readthedocs.io/plantDB/downloads/en/latest/pdf/>`_).

Usage
=====

Import
~~~~~~~

.. code:: python

   from flusstools import what2plant as w2p



Example
~~~~~~~

The following will show how the tool can be used to search for suitable vegetation.
To choose between the three provided ways to search for vegetation, start by calling the ``question()`` function.


.. code:: python

   import what2plant as w2p

   w2p.search.question()


This results in an console output informing the user about the possible choices and asking for an decision.


::

   Enter 1 to search database by habitat with detailed information
   Enter 2 to search database by coordinates
   Enter 3 to search by habitat in csv file for a quick overview without detail
   habitat search options so far:
   Alpenvorland, Niederrheinisches Tiefland, Oberrheinisches Tiefland
   Enter here:


If you want to search for plant data in the database directly, call search_db_via_query() and provide an corresponding sql - query.


.. code:: python

   import what2plant as w2p

   query = "habitat = 'Alpenvorland'"
   w2p.search.search_db_via_query(query)


.. note:: If you start by calling question(),  you get asked for a query in the console and don't need to manually add it.


The above function call will print all plants including their parameters which are located in 'Alpenvorland'. ``plantDB`` supports arbitrary sql-querys over the datafields in the provided 'Pflanzendaten.db' database.
To search directly for vegetation via coordinate input without starting with question() first, simply call search_by_coordinates().


.. code:: python

   import what2plant as w2p

   w2p.search.search_by_coordinates()


By doing so, you will get asked to provide x and y coordinates in the console


::

    CRS used is EPSG:3857
    for reference check https://epsg.io/3857
    Enter x coordinate
    1267965.259120
    Enter y coordinate
    6090686.743663


The possibility to receive additional elevation data for the above entered coordinates is then offered through the then called function point_in_bound()  via the console.


::

    Enter 1 if you want elevation data for the coordinates
    Enter 2 if you dont want elevation data
    Enter here:


The last available search option is to search for vegetation in the csv file. To achieve this, call search_by_habitat().


.. code:: python

   import what2plant as w2p

   w2p.search.search_by_habitat()


You will get asked to provide a habitat name you want to search plants for, afterwards all plants where your input matches witch their habitat entry in the csv file will get printed.


::

    Enter name of habitat
    Alpenvorland

    scientific name:
    Alnus incana
    common german name:
    Grauerle
    status:
    1
    endangered?:
    not endangered


The example above is one plant that gets printed if you should choose to search for plants in the habitat 'Alpenvorland'.


Code Documentation
==================

Package structure
~~~~~~~~~~~~~~~~~~~~~

.. figure:: https://en.wikipedia.org/wiki/File:UML_diagrams_overview.svg
   :alt: structure



Scripts and functions
=====================


``plant``
~~~~~~~~~~~~~~~~~~~~~
.. automodule:: flusstools.what2plant.plant
   :members:

Search options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: flusstools.what2plant.search
   :members:

SQL management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: flusstools.what2plant.sqlinput
   :members:
