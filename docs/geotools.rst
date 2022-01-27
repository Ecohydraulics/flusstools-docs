.. geo_utils documentation master file.

GeoTools
========

**Geospatial Functions for Hydraulics and Morphodynamics**

The *GeoTools* (``flusstools.geotools``) modules provide *Python3* functions for many sorts of river-related analyses with geospatial data (e.g., for working with numerical model input and output). The package is intended as support material for the `hydro-informatics eBook <https://hydro-informatics.github.io/>`_.


Usage
-----

Import
~~~~~~~

Import ``geotools`` from flusstools:

.. code:: python

    from flusstools import geotools as geo


Example (code block)
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from flusstools import geotools as geo
    raster, array, geo_transform = geo.raster2array("/sample-data/froude.tif")
    type(raster)
    # >>> <class 'osgeo.gdal.Dataset'>
    type(array)
    # >>> <class 'numpy.ndarray'>
    type(geo_transform)
    # >>> <class 'tuple'>
    print(geo_transform)
    # >>> (6748604.7742, 3.0, 0.0, 2207317.1771, 0.0, -3.0)

Example (showcase)
~~~~~~~~~~~~~~~~~~

A showcase is provided with the ``ROOT/examples/geotools-showcase/georeference_tifs.py`` script that illustrates geo-referencing *tif* images that do not have a projection assigned.



Code structure
--------------

The following diagram highlights function locations in Python scripts and how those are linked to each other.

.. figure:: https://github.com/Ecohydraulics/flusstools/raw/main/docs/img/geotools-uml.png
   :alt: structure

   *Diagram of the code structure (needs to be updated).*



Script and function docs
------------------------


Package Head: ``geotools``
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.geotools.geotools
    :members:
    :undoc-members:
    :show-inheritance:


Raster Management ``raster_mgmt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.geotools.raster_mgmt
    :members:


Shapefile Management ``shp_mgmt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.geotools.shp_mgmt
    :members:

Projection Management ``srs_mgmt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: flusstools.geotools.srs_mgmt
    :members:

Dataset Management (``dataset_mgmt``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.geotools.dataset_mgmt
    :members:

KML/KML File Management
~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.geotools.kml
    :members:

.. automodule:: flusstools.geotools.kmx_parser
    :members:

Shortest Path Finder
~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.geotools.shortest_path
    :members:

.. _Python programming for Water Resources Engineering and Research: https://hydro-informatics.com/python-basics/python.html
