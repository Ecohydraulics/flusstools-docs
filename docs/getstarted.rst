.. _install:

Installation
============

The recommended way to install *flusstools* is inside a **conda/mamba environment** - and this is now the best practice on **every platform** (*Linux*, *Windows*, and *macOS*) alike. The reason is GDAL: *flusstools* builds on the GDAL geospatial library, which is **not** available as a pre-built *pip* wheel. The conda-forge channel ships ready-to-use GDAL binaries, so a conda/mamba environment resolves GDAL (and the rest of the geospatial stack) without any compiler or system-library setup, identically across operating systems.

We recommend `mamba <https://mamba.readthedocs.io>`_ - a fast drop-in replacement for ``conda`` - but every command below works the same if you replace ``mamba`` with ``conda``.

Quick install
-------------

Create an environment with the GDAL binaries from conda-forge, then install *flusstools* into it with *pip*:

.. code:: console

    mamba create -n flussenv -c conda-forge python=3.11 gdal
    mamba activate flussenv
    pip install flusstools

GDAL is provided by conda-forge, and *pip* resolves the remaining dependencies (``numpy``, ``geopandas``, ``rasterio``, ...) from wheels - nothing has to be compiled.

Reproducible environment
-------------------------

To recreate the exact, version-pinned environment used to develop and test *flusstools*, build it from the `environment.yml`_ that ships with the package:

.. code:: console

    curl -O https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/main/environment.yml
    mamba env create -f environment.yml
    mamba activate flussenv
    pip install flusstools

Installing with pip only
------------------------

A plain ``pip install flusstools`` (into a regular *virtualenv*) works **only if a matching system GDAL is already present** - i.e. ``gdal-config`` is on your ``PATH`` and its version matches the ``gdal`` Python bindings. Because GDAL publishes no PyPI wheels, *pip* otherwise tries to compile GDAL from source and the install fails. This is exactly why the conda/mamba route above is the platform-independent best practice. If you do go the pip route, update *pip* first (``python -m pip install --upgrade pip``).

**flusstools** is tailored for applications in water resources research and engineering, and more detailed, step-by-step installation instructions (including how to set up conda/mamba from scratch) are provided with the `hydro-informatics eBook <https://hydro-informatics.com/pyinstall>`_ (at `https://hydro-informatics.com <https://hydro-informatics.com>`_).


Basic Usage
===========

Import
------

Import ``flusstools``:

.. code:: python

    import flusstools as ft


Or one of its modules:

.. code:: python

    from flusstools import geotools

New to Python? Take a look at the Python tutorial for water resources engineering and research at `hydro-informatics.com <https://hydro-informatics.com/python>`_


Example
-------

.. code-block::

    from flusstools import geotools as gt
    raster, array, geo_transform = gt.raster2array("/sample-data/froude.tif")
    type(raster)
    <class 'osgeo.gdal.Dataset'>
    type(array)
    <class 'numpy.ndarray'>
    type(geo_transform)
    <class 'tuple'>
    print(geo_transform)
    (6748604.7742, 3.0, 0.0, 2207317.1771, 0.0, -3.0)

.. _requirements:

Requirements (Dependencies)
---------------------------

FlussTools depends on a stack of geospatial libraries - most notably GDAL, which has no *pip* wheel. As explained under `Installation`_ above, a `conda/mamba environment <https://hydro-informatics.com/pyinstall/#conda-env>`_ (built from `environment.yml`_) resolves these binaries cleanly and is the recommended setup; a pure-*pip* `virtual environment <https://hydro-informatics.com/pyinstall/#venv>`_ with `requirements.txt`_ works only where a system GDAL is available. The full set of third-party dependencies is:

+-------------+--------------+--------------+
| Ext. libs.  |              |              |
+=============+==============+==============+
| alphashape  | pyproj       | rasterio     |
+-------------+--------------+--------------+
| earthpy     | mapclassify  | rasterstats  |
+-------------+--------------+--------------+
| gdal        | matplotlib   | tk           |
+-------------+--------------+--------------+
| geojson     | numpy        | scipy        |
+-------------+--------------+--------------+
| geopandas   | pandas       | shapely      |
+-------------+--------------+--------------+
| h5py        | openpyxl     | tabulate     |
+-------------+--------------+--------------+
| networkx    | pyshp        | scikit-fuzzy |
+-------------+--------------+--------------+


.. _Anaconda docs: https://docs.anaconda.com/anaconda/install/
.. _environment.yml: https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/main/environment.yml
.. _git: https://hydro-informatics.com/get-started/git.html
.. _git bash: https://git-scm.com/downloads
.. _gdal: https://gdal.org/
.. _QGIS: https://qgis.org/en/site/
.. _requirements.txt: https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/main/requirements.txt
.. _Windows Command Prompt: https://www.wikihow.com/Open-the-Command-Prompt-in-Windows
