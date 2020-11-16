.. geo_utils documentation master file.

GeoTools
========

**Geospatial Functions for Hydraulics and Morphodynamics**

``geotools`` provides *Python3* functions for many sorts of river-related analyses with geospatial data. The package is intended as support material for the lecture `Python programming for Water Resources Engineering and Research`_, where primarily *conda* environments are used.

.. note::
    This documentation is also as available as style-adapted PDF (`download <https://geo-utils.readthedocs.io/_/downloads/en/latest/pdf/>`_).

Usage
=====

Import
~~~~~~~

Import ``geotools`` from *flusstools*:

.. code:: python

    from flusstools import geotools as gt


Example (code block)
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import geotools as gt
    raster, array, geo_transform = gt.raster2array("/sample-data/froude.tif")
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

A showcase is provided with the *ROOT/examples/geotools-showcase/georeference_tifs.py* script that illustrates geo-referencing *tif* images that do not have a projection assigned.



Code structure
==================


The following diagram highlights function locations in *Python* scripts and how those are linked to each other.

.. figure:: https://github.com/Ecohydraulics/flusstools/raw/main/docs/img/geotools-uml.png
   :alt: structure

   *Diagram of the code structure (needs to be updated).*



Script and function docs
========================


``geotools`` (MASTER)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.geotools.geotools
    :members:
    :undoc-members:
    :show-inheritance:


``raster_mgmt`` raster management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.flusstools.geotools.raster_mgmt
    :members:


.. autofunction:: flusstools.geotools.raster_mgmt.raster2array
    :members:
    :undoc-members:
    :show-inheritance:



``shp_mgmt`` shapefile management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. automodule:: flusstools.geotools.shp_mgmt
    :members:


``srs_mgmt`` projection management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: flusstools.geotools.srs_mgmt
    :members:

``dataset_mgmt`` dataset conversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.geotools.dataset_mgmt
    :members:

KML/KML file management
~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.geotools.kml
    :members:

.. automodule:: flusstools.geotools.kmx_parser
    :members:


.. _Python programming for Water Resources Engineering and Research: https://hydro-informatics.github.io/hy_ppwrm.html
