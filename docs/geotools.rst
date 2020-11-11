.. geo_utils documentation master file.

The geo-utils docs
==================

**Geospatial Utility Functions for Hydraulics and Morphodynamics**

``geo_utils`` provides *Python3* functions for many sorts of
river-related analyses with geospatial data. The package is intended as
support material for the lecture `Python programming for Water Resources
Engineering and Research`_, where primarily *conda* environments are
used. Even though ``geo_utils`` basically works in all *Python3*
environments, make sure to follow the *Get Started* instructions on
`hydro-informatics.github.io`_ to get ready with *Anaconda* and
familiarize with `git`_.

.. note::
    This documentation is also as available as style-adapted PDF (`download <https://geo-utils.readthedocs.io/_/downloads/en/latest/pdf/>`_).

Installation
============

Use ``git`` to download the ``geo_utils`` repository (make sure to
`install Git Bash`_):

1. Open *Git Bash* (or any other git-able *Terminal*)
2. Create or select a target directory for ``geo_utils`` (e.g., in your
   *Python* project folder)
3. Type ``cd "D:/Target/Directory/"`` to change to the target
   installation directory.
4. Clone the repository.

.. code:: console

    cd "D:/Target/Directory/"
    git clone https://github.com/hydro-informatics/geo-utils.git

Now, ``geo_utils`` lives in ``"D:/Target/Directory/geo-utils/geo_utils"``.

Usage
=====

Import
~~~~~~~

1. Run *Python* and add the download directory of ``geo-utils`` to the
   system path:

.. code:: python

    import os, sys
    sys.path.append("D:/Target/Directory/geo-utils/")  # Of course: replace "D:/Target/Directory/", e.g., with  r'' + os.path.abspath('')

2. Import ``geo_utils``:

.. code:: python

    import geo_utils.geo_utils as gu


Example
~~~~~~~

.. code:: python

    import geo_utils as gu
    raster, array, geo_transform = gu.raster2array("/sample-data/froude.tif")
    type(raster)
    # >>> <class 'osgeo.gdal.Dataset'>
    type(array)
    # >>> <class 'numpy.ndarray'>
    type(geo_transform)
    # >>> <class 'tuple'>
    print(geo_transform)
    # >>> (6748604.7742, 3.0, 0.0, 2207317.1771, 0.0, -3.0)


Requirements
============

*  Python 3.x (read more on `hydro-informatics.github.io`_)
*  Dependencies:

    * alphashape
    * fiona
    * gdal (read more on `hydro-informatics.github.io/geo-pckg <https://hydro-informatics.github.io/geo-pckg.html#gdal>`_)
    * geojson
    * geopandas
    * numpy
    * pandas
    * pyshp
    * shapely


Code structure
==================


The following diagram highlights function locations in *Python* scripts and how those are linked to each other.

.. figure:: https://github.com/hydro-informatics/geo-utils/raw/master/graphs/geo-utils-uml.png
   :alt: structure

   *Diagram of the code structure (needs to be updated).*



Script and function docs
========================


``geo_utils`` (MASTER)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: geo_utils.geo_utils
   :members:

``raster_mgmt`` raster management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: geo_utils.raster_mgmt
   :members:

``shp_mgmt`` shapefile management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: geo_utils.shp_mgmt
   :members:

``srs_mgmt`` projection management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: geo_utils.srs_mgmt
   :members:

``dataset_mgmt`` dataset conversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: geo_utils.dataset_mgmt
   :members:

KML/KML file management
~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: geo_utils.kml
   :members:

.. automodule:: geo_utils.kmx_parser
   :members:

Examples
========

.. automodule:: georeference_tifs
   :members:


Contributing
=======================

How to document
~~~~~~~~~~~~~~~~

This package uses *Sphinx* `readthedocs <https://readthedocs.org/>`_ and the documentation regenerates automatically after pushing changes to the repositories ``main`` branch.

To set styles, configure or add extensions to the documentation use ``ROOT/.readthedocs.yml`` and ``ROOT/docs/conf.py``.

Functions and classes are automatically parsed for `docstrings <https://www.python.org/dev/peps/pep-0257/>`_ and implemented in the documentation. ``hylas`` docs use `google style <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_ docstring formats - please familiarize with the style format and strictly apply in all commits.

To modify this documentation file, edit ``ROOT/docs/index.rst`` (uses `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ format).

In the class or function docstrings use the following section headers:

* ``Args (alias of Parameters)``
* ``Arguments (alias of Parameters)``
* ``Attention``
* ``Attributes``
* ``Caution``
* ``Danger``
* ``Error``
* ``Example``
* ``Examples``
* ``Hint``
* ``Important``
* ``Keyword Args (alias of Keyword Arguments)``
* ``Keyword Arguments``
* ``Methods``
* ``Note``
* ``Notes``
* ``Other Parameters``
* ``Parameters``
* ``Return (alias of Returns)``
* ``Returns``
* ``Raise (alias of Raises)``
* ``Raises``
* ``References``
* ``See Also``
* ``Tip``
* ``Todo``
* ``Warning``
* ``Warnings (alias of Warning)``
* ``Warn (alias of Warns)``
* ``Warns``
* ``Yield (alias of Yields)``
* ``Yields``

For local builds of the documentation, the following packages are required:

.. code:: console

   $ sudo apt-get install build-essential
   $ sudo apt-get install python-dev python-pip python-setuptools
   $ sudo apt-get install libxml2-dev libxslt1-dev zlib1g-dev
   $ apt-cache search libffi
   $ sudo apt-get install -y libffi-dev
   $ sudo apt-get install python3-dev default-libmysqlclient-dev
   $ sudo apt-get install python3-dev
   $ sudo apt-get install redis-server

To generate a local html version of the ``hylas`` documentation, ``cd`` into the  ``docs`` directory  and type:

.. code:: console

   make html

Learn more about *Sphinx* documentation and the automatic generation of *Python* code docs through docstrings in the tutorial provided at `github.com/sschwindt/docs-with-sphinx <https://github.com/sschwindt/docs-with-sphinx>`_

Indices and tables
==================

* :ref:``genindex``
* :ref:``modindex``
* :ref:``search``


.. _Python programming for Water Resources Engineering and Research: https://hydro-informatics.github.io/hy_ppwrm.html
.. _hydro-informatics.github.io: https://hydro-informatics.github.io/hy_ide.html
.. _git: https://hydro-informatics.github.io/hy_git.html
.. _install Git Bash: https://git-scm.com/downloads
.. _course function: https://hydro-informatics.github.io/geo-shp.html#create-a-new-shapefile

