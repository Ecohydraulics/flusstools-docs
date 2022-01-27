.. _install:

Installation
============

Working with *flusstools* is platform independent, but the favorable installation procedure varies among platforms (e.g., *Linux* or *Windows*).

We recommend *Windows* user to use *Anaconda* and *conda* environments. *Linux* users will have a better experience with *pip*-installing *flusstools*. The differences stem from the way how GDAL is installed on the two platforms. *macOS* users may want to follow the *Linux* instructions, even though we could not yet test the installation of *flusstools* on *macOS*. For *Linux* users: before `pip install flusstools`, make sure your *pip* is updated (`python -m pip install --upgrade pip`) to avoid incompatibilities with Python wheels in Linux.

**flusstools** is tailored for applications in water resources research and engineering and this is why the detailed instructions about the installation of flusstools are provided with the `hydro-informatics eBook <https://hydro-informatics.com/python-basics/pyinstall.html>`_ (at `https://hydro-informatics.com <https://hydro-informatics.com>`_).**


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

New to Python? Take a look at the Python tutorial for water resources engineering and research at `hydro-informatics.com <https://hydro-informatics.com/python-basics/python.html>`_


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

FlussTools requires geospatial processing libraries, which cannot be directly resolved by running *setup.py*. For this reason, we recommend to either install a `virtual environment <https://hydro-informatics.com/python-basics/pyinstall.html#venv>`_ with `requirements.txt`_ or a `conda environment <https://hydro-informatics.com/python-basics/pyinstall.html#conda-env>`_ with `environment.yml`_ to check out the following dependencies on non-standard Python libraries:

+-------------+--------------+--------------+
| Ext. libs.  |              |              |
+=============+==============+==============+
| alphashape  | laspy        | rasterio     |
+-------------+--------------+--------------+
| earthpy     | mapclassify  | rasterstats  |
+-------------+--------------+--------------+
| gdal        | matplotlib   | tk           |
+-------------+--------------+--------------+
| geojson     | numpy        | scipy        |
+-------------+--------------+--------------+
| geopandas   | pandas       | shapely      |
+-------------+--------------+--------------+
| h5py        | pip          | tabulate     |
+-------------+--------------+--------------+
| networkx    | pyshp        | plotly       |
+-------------+--------------+--------------+


.. _Anaconda docs: https://docs.anaconda.com/anaconda/install/
.. _environment.yml: https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/main/environment.yml
.. _git: https://hydro-informatics.com/get-started/git.html
.. _git bash: https://git-scm.com/downloads
.. _gdal: https://gdal.org/
.. _QGIS: https://qgis.org/en/site/
.. _requirements.txt: https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/main/requirements.txt
.. _Windows Command Prompt: https://www.wikihow.com/Open-the-Command-Prompt-in-Windows
