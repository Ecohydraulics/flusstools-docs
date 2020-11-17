.. flusstools documentation master file.

.. _home:

FlussTools
==========

The analysis, research and science-based design of fluvial ecosystems involve complex challenges for interdisciplinary experienced teams. We have created flusstools to meet the complex challenges and to at least partially automate time-consuming, repetitive processes. "We" stands for individuals with a great passion for rivers (in German, plural for "Fluss") and programming. Most of us work (or have worked) at the University of Stuttgart (Germany) at the `Institute for Modelling Hydraulic and Environmental Systems`_. In the context of our scientific endeavor, we have a strong commitment to transparent open-source applications. With flusstools we want to share our research-based open-source algorithms with a broad interest group in a well documented form. We welcome new team members (for example to add or amend a module) at any time - read more in the :ref:`contribute` section.

Currently, *flusstools* comes with the following modules:

* *geotools* - versatile functions for processing spatial data for fluvial ecosystem analyses based on `gdal`_ and other open source libraries.
* *fuzzycorr* - a map comparison toolkit that builds on fuzzy sets to assesss the accuracy of (numerical) river models (principal developer: `Beatriz Negreiros`_).
* *what2plant* - finds the best plant species for a fluvial ecosystems (currently implemented only for the Rhine bassin and the Bavarian Pre-Alps - principal developer: `Lukas Schoeberl`_).
* *lidartools* - *Python* wrappers for `lastools`_ (forked and modified from `Kenny Larrieu`_).

.. note::
    The documentation is also as available as `style-adapted PDF <https://flusstools.readthedocs.io/_/downloads/en/latest/pdf/>`_).

.. _install:

Installation
============

To work with *flusstools*, a couple of dependencies have to be installed and depending on what platform you are working (*Window* or *Linux*), it might be preferable to use either a *PIP3* or a *CONDA* environment. We have made good experience with *conda* environments in *Windows* and with *pip* environments in *Linux* (*Ubuntu*). However, both *pip* and *conda* both work fine on both platforms (and also with *macOS*). Since *Python 3.4* (and *Python 2.7.9*), *pip* is installed with the basic *Python* installation (`download and install Python <https://www.python.org/downloads/>`_ if you do not want to use *conda*). Find the instructions for installing *Anaconda* tailored for your ooperating system (*Linux*, *Windows*, or *macOS*) in the `Anaconda docs`_. The following paragraphs guide through setting up your system for the best experience with *flusstools* (and basically any geo-spatial *Python* application).

Get ready with Windows
~~~~~~~~~~~~~~~~~~~~~~

On *Windows*, a convenient option for working with *flusstools* is to use a conda environment. In addition, *GitBash* is necessary to clone (download) *flusstools* (and to keep posted on updates). In detail:

* Install *Anaconda*, for example, as described on `hydro-informatics.github.io/hy_ide <https://hydro-informatics.github.io/hy_ide.html#anaconda>`_.
* Alternatively, `download and install Python <https://www.python.org/downloads/>`_, open `Windows Command Prompt`_, and make sure to upgrade *pip* with your basic *Python* installer by typing: ``python -m pip install -U pip``.
* `Download <https://git-scm.com/downloads>`_ and install *GitBash*.
* We recommend to work with an *IDE*, such as `PyCharm <https://www.jetbrains.com/pycharm/download/#section=windows>`_ or `Spyder <https://www.spyder-ide.org/>`_, which is natively implemented in the *Anaconda* installation.
* Download and install `QGIS`_ to visualize and draw geospatial data.

Get ready with Linux
~~~~~~~~~~~~~~~~~~~~~~

Optional: Use a Virtual Machine (VM)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Either download a net-installer *ISO* of `Debian Linux <https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/>`_  or `Ubuntu <https://ubuntu.com/download>`_, or one of its light-weight spin-offs such as  the `Lubuntu <https://lubuntu.net/downloads/>`_, and install one of theses images as a Virtual Machine (VM). To get started with VMs read the introduction to VMs on `hydro-informatics.github.io/vm#about <https://hydro-informatics.github.io/vm.html#about>`_. Installing any other the *Linux* VM works similar, as described on `hydro-informatics.github.io/vm#create-a-vm-with-virtualbox <https://hydro-informatics.github.io/vm.html#create-a-vm-with-virtualbox>`_ for *Debian Linux*. Just use the *ISO* image in lieu of the *Debian Linux* *ISO*. After installing *Linux* as a VM, make sure to:

* `Install Guest Additions <https://hydro-informatics.github.io/vm.html#setup-debian>`_ for *Linux* VMs in *VirtualBox*.
* `Enable folder sharing <https://hydro-informatics.github.io/vm.html#share>`_ between the host and guest (*Debian*, *Ubuntu*, or *Lubuntu* image).

Other system setups described on `hydro-informatics.github.io/vm <https://hydro-informatics.github.io/vm.html>`_ (e.g., *Wine*) are not required in the following.

Prepare your system
^^^^^^^^^^^^^^^^^^^

Open *Terminal*  and update the system:

.. code:: console

    sudo apt update && sudo apt full-upgrade -y


Update Python references
^^^^^^^^^^^^^^^^^^^^^^^^

Some (basic) *Linux* distributions still have *Python2* implemented as base interpreter to be used when ``python`` is called in *Terminal*. However, *Python2* usage is deprecated, and therefore, we want to make sure to robustly use *Python3* for running any *Python* script. Check out the installed *Python3* versions:

.. code:: console

    ls /usr/bin/python*


    /usr/bin/python  /usr/bin/python2  /usr/bin/python2.7  /usr/bin/python3  /usr/bin/python3.8  /usr/bin/python3.8m  /usr/bin/python3m

In this example, *Python2.7* and *Python3.8* are installed. To overwrite *Python2* usage, set the ``python`` environment variable so that it points at *Python3*:

.. code:: console

   sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
   alias python=python3


PIP3 and additional libraries for geospatial analyses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make sure that `PyGeos <https://pygeos.readthedocs.io>`_ and `tkinter <https://hydro-informatics.github.io/hypy_gui.>`_ are available for use with `geopandas <https://geopandas.org/>`_:

.. code:: console

   sudo apt install python3-pip
   sudo apt-get install python3-tk
   sudo apt install tk8.6-dev
   sudo apt install libgeos-dev

Then install *QGIS* and ``GDAL`` for *Linux* (this should work with any *Debian* architecture):

.. code:: console

   sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
   sudo apt-get update
   sudo apt-get install gdal-bin
   sudo apt-get install libgdal-dev
   export CPLUS_INCLUDE_PATH=/usr/include/gdal
   export C_INCLUDE_PATH=/usr/include/gdal
   pip3 install GDAL

.. note::

   Check on the latest GDAL release on the `developers website <https://gdal.org/download.html#current-releases>`_.

More guidance for installing GDAL (also on other platforms) is available at `gdal.org <https://gdal.org/download.html>`_.

Install an IDE (*PyCharm*)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: IDE - your choice
   Any other Python IDE is also OK for working with *hylas*. Setting up *PyCharm* is explained here as just one option for working with *flusstools*.

Install *PyCharm* with snap (requires snap):

.. code:: console

   sudo apt install snapd
   sudo snap install pycharm-community --classic


Install flusstools
~~~~~~~~~~~~~~~~~~

.. _installcondaenv:

CONDA
^^^^^

1. Download our `environment.yml`_ file and save it in a temporary folder (e.g., *C:\temp\* or *USER/Downloads/*).

2. Open *Anaconda Prompt* (on *Windows*) or *Terminal* (on *Linux*).

3. Navigate to your download directory (e.g., ``cd C:\temp`` or ``cd Downloads/``).

4. Install the *flusstools* environment:

* ``conda env create -f environment.yml``
* Geospatial libraries and other dependencies (see below) are being installed in a new environment called *flusstools* - this may take a while ...
* Read more about installing, managing, or removing *conda* environments on `hydro-informatics.github.io/hpy_install <https://hydro-informatics.github.io/hypy_install.html#conda-env>`_.

5. Activate the *flusstools* environment:
    * ``conda activate flusstools``

6. Install *flusstools* in the new environments:
    * ``pip install flusstools``

.. _installvenv:

PIP / VENV
^^^^^^^^^^

Consider to create and activate a new virtual environment before installing *flusstools* requirements (read more at `python.org <https://docs.python.org/3/library/venv.html>`_). Then, download our `requirements.txt`_ file and save it in a temporary folder (e.g., *C:\temp\* or *USER/Downloads/*). In *Terminal* (*Linux* / *macOS*) or `Windows Command Prompt`_ type:

.. code:: console

    cd C:\temp # or cd Downloads/
    pip install -r requirements.txt
    pip install flusstools


Setup *IDE* environment
~~~~~~~~~~~~~~~~~~~~~~~

Depending on the *IDE* you are using, create a new project and define the above created environment (either *conda* or *pip*) as project interpreter.

* *PyCharm* users get help at `jetbrains.com <https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#default-interpreter>`_
* *Spyder* users find help at `spyder-ide.org <https://docs.spyder-ide.org/current/installation.html>`_
* *Notebook* users are served at `jupyter.org <https://jupyter.org/install>`_


Usage
=====

Import
~~~~~~~

1. Run *Python* and add the download directory of ``flusstools`` to the system path:

.. code:: python

    import os, sys
    sys.path.append("D:/Target/Directory/flusstools/")  # Of course: replace "D:/Target/Directory/", e.g., with  r'' + os.path.abspath('')

2. Import ``flusstools``:

.. code:: python

    import flusstools as ft


Example
~~~~~~~

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

Requirements
============

*FlussTools* requires geo-spatial processing libraries, which cannot be directly resolved by running *setup.py*. For this reason, we recommend to either install a virtual environment (:ref:`installvenv`) with `requirements.txt`_ (*pip* / *venv*) or a conda environment (:ref:`installcondaenv`) with `environment.yml`_  (*conda*) to check out the following dependencies:

* pip
* tabulate
* numpy
* platform
* pandas
* matplotlib
* plotly
* alphashape
* earthpy
* gdal
* geopandas
* geojson
* laspy
* mapclassify
* pyshp
* rasterio
* rasterstats
* shapely
* tk


Module documentation
====================

.. toctree::
    :maxdepth: 1
    :caption: Home

    self

.. toctree::
    :maxdepth: 2
    :caption: Geo-spatial analyst tools

    geotools

.. toctree::
    :maxdepth: 2
    :caption: Map correlation

    fuzzycorr

.. toctree::
    :maxdepth: 2
    :caption: Lidar tools (las / laz analyst)

    lidartools

.. toctree::
    :maxdepth: 2
    :caption: Plant database

    what2plant

.. toctree::
    :maxdepth: 3
    :caption: Contributing

    contribute

.. toctree::
    :maxdepth: 3
    :caption: Disclaimer and License

    license

More information and examples are available in the docs of every *flusstools* module.

.. _Anaconda docs: https://docs.anaconda.com/anaconda/install/
.. _hydro-informatics.github.io: https://hydro-informatics.github.io
.. _environment.yml: https://raw.githubusercontent.com/Ecohydraulics/flusstools/main/environment.yml
.. _git: https://hydro-informatics.github.io/hy_git.html
.. _git bash: https://git-scm.com/downloads
.. _Institute for Modelling Hydraulic and Environmental Systems: https://www.iws.uni-stuttgart.de/en/lww/
.. _gdal: https://gdal.org/
.. _lastools: http://lastools.org/
.. _Beatriz Negreiros: https://beatriznegreiros.github.io/
.. _Kilian Mouris: https://www.iws.uni-stuttgart.de/en/institute/team/Mouris/
.. _Kenny Larrieu: https://klarrieu.github.io/
.. _Lukas Schoeberl: https://github.com/Lukas-create/
.. _QGIS: https://qgis.org/en/site/
.. _requirements.txt: https://raw.githubusercontent.com/Ecohydraulics/flusstools/main/requirements.txt
.. _Sebastian Schwindt: https://sebastian-schwindt.org/
.. _Windows Command Prompt: https://www.wikihow.com/Open-the-Command-Prompt-in-Windows