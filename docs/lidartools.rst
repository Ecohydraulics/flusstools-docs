.. lidartools documentation master file.

LidarTools
===========

The *laspy_X* modules are universal *Python3* scripts, which are completely open-source and can be applied on any platform (*Window*, *Linux*). However, *laspy* may crash with larger *las* files (> 1 GB), and in particular, when the available system memory is small. For these reasons, preferably use the inter-platform and open source *laspy_X* modules, but if you need to deal with large *las* files on a weak system, use the *Windows*-only *lastools*. Note that *lastools* builds on `LAStools from rapidlasso <https://rapidlasso.com/lastools/>`_. It might be possible to run *LAStools* on *Linux* with `wine`_ (not yet tested with *flusstools*).


LasPy
-----

The *laspy_X* modules extract geospatial information from *las* files and convert them to ESRI shapefiles or GeoTIFF rasters. *las* is the typical file format for storing airborne lidar (`Light Detection and Ranging <https://oceanservice.noaa.gov/facts/lidar.html>`_) data. The *flusstools* *laspy_X* modules make use of the inter-platform and open source `laspy`_ *Python* package. The currently implemented capacities involve:

* A point shapefile with user-defined point attributes such as *intensity*, *waveform*, or *nir*.
* Digital elevation model (DEM) with user-defined resolution (pixel size).
* *GeoTIFF* rasters with user-defined resolution (pixel size) for any attribute of a *las* file (e.g., *intensity*, *waveform*, or *nir*).

.. admonition:: Computation Power and Memory Errors

    *Las* files can be very large and the *laspy_X* modules load entire *las* files in the system memory. A large *las* file (> 1 GB) may result in your system shutting down *Python* because it is *eating* more memory than available. Therefore, consider using *las* file subsets or computers with large memory. Read more about memory errors in the Troubleshooting section (see below :ref:`memory_error`_).

Usage
~~~~~

Basics
^^^^^^

To convert a *las* file to an ESRI shapefile or GeoTIFF, load *flusstools.lidartools.laspy_main* in Python:

.. code-block:: python

   import flusstools.lidartools.laspy_main as hylas
   las_file_name = "path/to/a/las-file.las"
   methods = ["las2shp", "las2tif"]
   hylas.process_file(las_file_name, epsg=3857, methods=methods)


The above code block defines a ``las_file_name`` variable and ``methods`` to be used with ``flusstools.lidartools.laspy_main.process_file`` (see :ref:`hylas`). The function accepts many more optional arguments:

.. automodule:: flusstools.lidartools.laspy_main.process_file
   :special-members:

.. note::
   The ``LasPoint`` class (see :ref:`hylas`) can also be directly called in any script with ``laspy_processor.LasPoint``. Have a look at the ``laspy_processor.process_file`` function (:ref:`hylas`) to see how an instance of the ``LasPoint`` class is used.

Application example
^^^^^^^^^^^^^^^^^^^

The following code block converts a file called *las-example.las* first into a shapefile and then into a *GeoTIFF*. By using the attributes ``"aci"``, the ``scan_angle`` (``a``), the ``classification_flags`` (``c``), and the ``intensity`` (``i``) are extracted from the *las* file. Find out more about applicable attributes in the *flusstools.lidartools.laspy_config.wattr* dictionary (see below :ref:`laspy_config`_).

.. code-block:: python

   import flusstools.lidartools.laspy_main as hylas
   import os

   las_file_name = os.path.abspath("") + "/data/las-example.las"
   shp_file_name = os.path.abspath("") + "/data/example.shp"
   epsg = 25832
   methods = ["las2tif"]
   attribs = "aci"
   px_size = 2
   tif_prefix = os.path.abspath("") + "/data/sub"

   hylas.process_file(las_file_name,
                      epsg=epsg,
                      methods=methods,
                      extract_attributes=attribs,
                      pixel_size=px_size,
                      shapefile_name=shp_file_name,
                      tif_prefix=tif_prefix)


.. note::
   The method ``las2tif`` automatically calls the ``las2shp`` (``flusstools.lidartools.laspy_processor.LasPoint.export2shp``) method because the GeoTIFF pixel values are extracted from the attribute table of the point shapefile. So ``las2shp`` is the baseline for any other operation.


Code Documentation
~~~~~~~~~~~~~~~~~~

.. _hylas:

LasFile main
^^^^^^^^^^^^

.. automodule:: flusstools.lidartools.laspy_main
   :members:

.. topic:: ``process_file(source_file_name, epsg, **opts)``

   Loads a las-file and converts it to another geospatial file format (keyword arguments ``**opts``).

   Note that this function documentation is currently manually implemented because of *Sphinx* having troubles to look behind decorators.

Arguments:
      * **source_file_name** (``str``): Full directory of the source file to use with methods
         * if ``method="las2*"``: provide a las-file name
         * if ``method="shp2*"``: provide a shapefile name
      * **epsg** (``int``): Authority code to use (try ``hylas.lookup_epsg(las_file_name)`` to look up the epsg online).

Keyword Arguments (``**opts``):
      * **create_dem** (``bool``): Set to True for creating a digital elevation model (DEM - default: ``False``)

      * **extract_attributes** (``str``): Attributes to extract from the las-file available in ``pattr`` (``config.py``)

      * **methods** (``list`` [``str``]): Enabled list strings are ``las2shp``, ``las2tif``, ``shp2tif``, ``las2dem``.

      * **overwrite** (``bool``): Overwrite existing shapefiles and/or GeoTIFFs (default: ``True``).

      * **pixel_size** (``float``): Use with *2tif  to set the size of pixels relative to base units (``pixel_size=5`` indicates 5x5-m pixels)

      * **shapefile_name** (``str``): Name of the point shapefile to produce with ``las2*``

      * **tif_prefix** (``str``): Prefix include folder path to use for GeoTiFFs (defined extract_attributes are appended to file name)

      * **interpolate_gap_pixels** (``bool``): Fill empty pixels that are not touched by a shapefile point with interpolated values (default: ``True``)

      * **radius1** (``float``): Define the x-radius for interpolating pixels (default: ``-1``, corresponding to infinity). Only applicable ``with interpolate_gap_pixels``.

      * **radius2** (``float``): Define the y-radius for interpolating pixels (default: ``-1``, corresponding to infinity). Only applicable ``with interpolate_gap_pixels``.

      * **power** (``float``): Power of the function for interpolating pixel values (default: ``1.0``, corresponding to linear).

      * **smoothing** (``float``): Smoothing parameter for interpolating pixel values (default: ``0.0``).

      * **min_points** (``int``): Minimum number of points to use for interpolation. If the interpolator cannot find at least ``min_points`` for a pixel, it assigns a ``no_data`` value to that pixel  (default: ``0``).

      * **max_points** (``int``): Maximum number of points to use for interpolation. The interpolator will not use more than ``max_points`` closest points to interpolate a pixel value (default: ``0``).

Returns:
      ``bool``: ``True`` if successful, ``False`` otherwise.

More information on pixel value interpolation:
* ``interpolate_gap_pixels=True`` interpolates values at pixels that are not touched by any las point.
* The pixel value interpolation uses ``gdal_grid`` (i.e., its Python bindings through ``gdal.Grid()``).
* Control the interpolation parameters with the keyword arguments ``radius1``, ``radius2``, ``power``, ``max_points``, ``min_points``,  and ``smoothing``.

.. seealso:: All variables are illustratively explained on the `GDAL website <https://gdal.org/tutorials/gdal_grid_tut.html?highlight=grid>`_.

Las processor
^^^^^^^^^^^^^^

.. automodule:: flusstools.lidartools.laspy_processor
   :members:

.. _laspy_config:
Analysis config
^^^^^^^^^^^^^^^

.. automodule:: flusstools.lidartools.laspy_config
   :members:

Troubleshooting
~~~~~~~~~~~~~~~

.. _memory_error:
Memory errors
^^^^^^^^^^^^^

.. admonition:: MemoryError

   **Cause**: *las* files may have a size of several GiB, which may quickly cause a ``MemoryError`` (e.g., ``MemoryError: Unable to allocate 9.1 GiB for an array with shape ...``). In particular, the *Linux* kernel will not attempt to run actions that exceed the commit-able memory.

   **Solution**: Enable memory over-committing:
      * Check the current over-commit mode in *Terminal*:
         ``cat /proc/sys/vm/overcommit_memory``
      * If ``0`` is the answer, the system calculates array dimensions and the required memory (e.g., an array with dimensions ``(266838515, 12, 49)`` requires a memory of ``266838515 * 12 *49 / 1024.0**3`` = ``146`` GiB, which is unlikely to fit in the memory).
      * To enable over-committing, set the commit mode to ``1``:
         ``echo 1 | sudo tee /proc/sys/vm/overcommit_memory``

    **Alternative Solution**: Use *LasTools* (see below), which has better capacity to deal with system memory limitations, but works on *Windows* only (not yet tested: implementation of *LasTools* in *Linux* with `wine`_).


LasTools (Windows only)
-----------------------

*lastools* is forked from `GCS_scripts by Kenny Larrieu <https://github.com/klarrieu>`_. The original code is designed for *Python2* and the commercial ``arcpy`` library. The tweaked codes of *las4windows* run with Python 3.8 and work without ``arcpy``. This repository only uses the GUI for lidar processing with `LASTools <https://rapidlasso.com/lastools/>`_.

Because *LASTools* is proprietary, its executables can hardly be run on Linux or other UNIX-based systems (not yet tested: implementation of *LasTools* in *Linux* with `wine`_). This is why *LasTools* is a *Windows*-only application.

.. admonition:: Use the GUI

    Launch ``flusstools.lidartools.lastools_GUI.create_gui()`` to open a graphical user interface that walks you through the *lastools* scripts implemented in *flusstools*, and calls relevant functions by a simple mouse click.

Additional requirements
~~~~~~~~~~~~~~~~~~~~~~~~

*LASTools* is used for LiDAR Data Processing and can be downloaded `here <https://rapidlasso.com/lastools/>`_.

Usage
~~~~~

The main function to start processing a *las* or *laz* file with *lastools* is ``process_lidar``, which can be called as follows:

.. code-block:: python

    import flusstools.lidartools.lastools_core as lastools

    lastools.process_lidar(
        lastoolsdir="C:/dir/to/LAStools/bin",
        lidardir="C:/LiDAR/file/directory",  # las or laz file
        ground_poly="C:/dir/to/Ground-area-shp-file (optional)",  # limit the analysis region
        cores=4,  # numbers of cores to use
        units_code="Meters",  # alternative: "Feet"
        keep_orig_pts=False,  # Keep original ground/veg points (True or False)
        coarse_step="",  # numeric as string (do not use None)
        coarse_bulge="",  # numeric as string (do not use None)
        coarse_spike="",  # numeric as string (do not use None)
        coarse_down_spike="",  # numeric as string (do not use None)
        coarse_offset="",  # numeric as string (do not use None)
        fine_step="",  # numeric as string (do not use None)
        fine_bulge="",  # numeric as string (do not use None)
        fine_spike="",  # numeric as string (do not use None)
        fine_down_spike="",  # numeric as string (do not use None)
        fine_offset=""  # numeric as string (do not use None)
    )

Alternatively, *lastools* can be started as a graphical user interface as follows (from *Windows Prompt*):

.. code:: console

    cd C:\dir\to\flusstools\lidartools
    python LiDAR_processing_GUI



Code Documentation
~~~~~~~~~~~~~~~~~~


LiDAR processing
^^^^^^^^^^^^^^^^
.. automodule:: flusstools.lidartools.lastools_core
   :members:

File functions
^^^^^^^^^^^^^^
.. automodule:: flusstools.lidartools.lastools_fun
   :members:


.. _laspy: https://laspy.readthedocs.io/
.. _wine: https://hydro-informatics.github.io/vm.html#wine