.. _troubleshoot:
Troubleshoot
============

GDAL
----

*FlussTools* fundamentally depends on many *gdal* functions and scripts, but the installation of *gdal* involves dependencies that often break with new developments on different platforms.


On Windows
^^^^^^^^^^

Currently, there is an issue with installing GDAL when *Microsoft Visual C++* is missing or outdated. This issue typically leads to an error message such as:

.. code:: console

   Running GDAL-3.3.0\setup.py -q bdist_egg --dist-dir C:\Users\schwindt\AppData\Local\Temp\easy_install-nikwt0b0\GDAL-3.3.0\egg-dist-tmp-gidl99xl
   error: Setup script exited with error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

Thus, to enable the installation of GDAL on *Windows*, first download and install **Microsoft Visual C++** from `Microsoft C++ Build Tools <https://visualstudio.microsoft.com/visual-cpp-build-tools/>`_.
