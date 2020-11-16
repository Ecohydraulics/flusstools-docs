.. lidartools documentation master file.

LidarTools
====================

*las4windows* is forked from `GCS_scripts by Kenny Larrieu <https://github.com/klarrieu>`_. The original code is designed for *Python2* and the commercial ``arcpy`` library. The tweaked codes of *las4windows* run with Python 3.8 and work without ``arcpy``. This repository only uses the GUI for lidar processing with `LASTools <https://rapidlasso.com/lastools/>`_.

Because *LASTools* is proprietary, its executables can hardly be run on Linux or other UNIX-based systems. This is why *las4windows* is a *Windows*-only (*nomen est omen*).

Additional requirements
==========================

*LASTools* is used for LiDAR Data Processing and can be downloaded `here <https://rapidlasso.com/lastools/>`_.

Usage
=====

*lidartools* starts as a graphical user interface and can be started as follows (from *Windows Prompt*):

.. code:: console

    cd C:\dir\to\flusstools\lidartools
    python LiDAR_processing_GUI

.. admonition:: To-Do

    A future creation of a GUI interface for *flusstools* will integrate *lidartools* as a module-window. Currently, the direct way for using *lidartools* in *Python* script requires to ``import flusstools.lidartools.lidar_core``.


Code Documentation
==================


The GUI script
~~~~~~~~~~~~~~
.. automodule:: flusstools.lidartools.LiDAR_processing_GUI
   :members:

LiDAR processing
~~~~~~~~~~~~~~~~
.. automodule:: flusstools.lidartools.lidar_core
   :members:

File functions
~~~~~~~~~~~~~~
.. automodule:: flusstools.lidartools.file_functions
   :members:

