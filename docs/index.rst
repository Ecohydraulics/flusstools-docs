.. flusstools documentation master file.

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

Either download a net-installer *ISO* of `Debian Linux <https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/>`_  or `Ubuntu <https://ubuntu.com/download>`_, or one of its light-weight spin-offs such as  the `Lubuntu <https://lubuntu.net/downloads/>`_, and install one of theses images as a Virtual Machine (VM). To get started with VMs read the introduction to VMs on `hydro-informatics.github.io <https://hydro-informatics.github.io/vm.html#about>`_. Installing any other the *Linux* VM works similar, as described on `hydro-informatics.github.io <https://hydro-informatics.github.io/vm.html#create-a-vm-with-virtualbox>`_ for *Debian Linux*. Just use the *ISO* image in lieu of the *Debian Linux* *ISO*. After installing *Linux* as a VM, make sure to:

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


PIP3 and additional libraries for geospatial analysis
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


Clone flusstools
~~~~~~~~~~~~~~~~

Use ``git`` to download the ``flusstools`` repository (*Windows* users make sure to install `git bash`_):

1. Open *Git Bash* or any other git-able *Terminal* (standard in most *Linux* systems and *macOS*)
2. Create or select a target directory for ``flusstools`` (e.g., in a local *Python* project folder)
3. Type ``cd "D:/Target/Directory/"`` to change to the target installation directory.
4. Clone the repository.

.. code:: console

    cd "D:/Target/Directory/"
    git clone https://github.com/ecohydraulics/flusstools.git

Now, ``flusstools`` lives in ``"D:/Target/Directory/flusstools"``.

Setup  *Python* environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Anaconda
^^^^^^^^

Open  *Terminal* (*Linux* / *macOS*) or `Anaconda Prompt <https://docs.anaconda.com/anaconda/install/verify-install/>`_ (*Windows*) and install the *flusstools* environment by typing:

.. code:: console

    cd to\flusstools\directory
    conda env create -f environment.yml

.. admonition:: Be patient...

    Installing the *flusstools* environment takes a while (> 30 min.).

Read more about installing, managing, or removing *conda* environments on `hydro-informatics.github.io/hpy_install <https://hydro-informatics.github.io/hypy_install.html#conda-env>`_.


PIP
^^^

Consider to create and activate a new virtual environment before installing *flusstools* requirements (read more at `python.org <https://docs.python.org/3/library/venv.html>`_). Then, in *Terminal* (*Linux* / *macOS*) or `Windows Command Prompt`_ type:

.. code:: console

    cd to\flusstools\directory
    pip install -r requirements.txt


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

.. code:: python

    from flusstools import geo_utils as gu
    raster, array, geo_transform = gu.raster2array("/sample-data/froude.tif")
    type(raster)
    <class 'osgeo.gdal.Dataset'>
    type(array)
    <class 'numpy.ndarray'>
    type(geo_transform)
    <class 'tuple'>
    print(geo_transform)
    (6748604.7742, 3.0, 0.0, 2207317.1771, 0.0, -3.0)


Requirements
============

Have a look at the *requirements.txt* (*pip* / *venv*) or the *environment.yml* (*conda*) to check out dependencies.

Module documentation
====================

.. toctree::
    :maxdepth: 2
    :caption: Home

    index

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

Contributing
============

.. _contribute:

Become a contributor
~~~~~~~~~~~~~~~~~~~~

Most team members joined in the framework of their Bachelor or Master's Thesis with innovative contributions. So if you are a student and you want to contribute to *flusstools*, why not in the scope of an innovative thesis? Check out our currently open `Bachelor and Master Thesis topics <https://www.iws.uni-stuttgart.de/en/lww/education/>`_.

Obviously you do not have to be a student to join us - please use `Sebastian Schwindt`_s informal contact form - quick response (most of the time) for sure.


How to document
~~~~~~~~~~~~~~~~

This package uses *Sphinx* `readthedocs <https://readthedocs.org/>`_ and the documentation regenerates automatically after pushing changes to the repositories ``main`` branch.

To set styles, configure or add extensions to the documentation use ``ROOT/.readthedocs.yml`` and ``ROOT/docs/conf.py``.

Functions and classes are automatically parsed for `docstrings <https://www.python.org/dev/peps/pep-0257/>`_ and implemented in the documentation. ``hylas`` docs use `google style <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_ docstring formats - please familiarize with the style format and strictly apply in all commits.

To modify this documentation file, edit ``ROOT/docs/index.rst`` (uses `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ format).

In the class or function docstrings use the following section headers:

* ``Args`` (alias of ``Parameters``)
* ``Arguments`` (alias of ``Parameters``)
* ``Attention``
* ``Attributes``
* ``Caution``
* ``Danger``
* ``Error``
* ``Example``
* ``Examples``
* ``Hint``
* ``Important``
* ``Keyword Args`` (alias of ``Keyword Arguments``)
* ``Keyword Arguments``
* ``Methods``
* ``Note``
* ``Notes``
* ``Other Parameters``
* ``Parameters``
* ``Return`` (alias of ``Returns``)
* ``Returns``
* ``Raise`` (alias of ``Raises``)
* ``Raises``
* ``References``
* ``See Also``
* ``Tip``
* ``Todo``
* ``Warning``
* ``Warnings`` (alias of ``Warning``)
* ``Warn`` (alias of ``Warns``)
* ``Warns``
* ``Yield`` (alias of ``Yields``)
* ``Yields``

For local builds of the documentation, the following packages are required:

.. code:: console

   sudo apt-get install build-essential
   sudo apt-get install python-dev python-pip python-setuptools
   sudo apt-get install libxml2-dev libxslt1-dev zlib1g-dev
   apt-cache search libffi
   sudo apt-get install -y libffi-dev
   sudo apt-get install python3-dev default-libmysqlclient-dev
   sudo apt-get install python3-dev
   sudo apt-get install redis-server

To generate a local html version of the ``hylas`` documentation, ``cd`` into the  ``docs`` directory  and type:

.. code:: console

   make html

Learn more about *Sphinx* documentation and the automatic generation of *Python* code docs through docstrings in the tutorial provided at `github.com/sschwindt/docs-with-sphinx <https://github.com/sschwindt/docs-with-sphinx>`_.


Implement new stuff
~~~~~~~~~~~~~~~~~~~

All contributors, please respect the *Zen of Python* (``import this``).

How to add new package or library imports:

* Add it to the global import management file (*ROOT/import_mgmt.py*) within an *try-except-ImportError* statement (`read more <https://hydro-informatics.github.io/hypy_pyerror.html#try-except>`_).
* If you need to import a library or package that is not yet listed in the *ROOT/environments.yml* and *ROOT/requirements.txt* files, please make sure to add the new library or package in both files.
* Add the new library or package to the ``autodoc_mock_imports`` *list* in *ROOT/docs/conf.py*.

Please use *PEP 8* for any code (read more on `hydro-informatics.github.io <https://hydro-informatics.github.io/hypy_pystyle.html>`_) and try to keep the number of lines per script below 150 (it's hard or even apparently impossible sometimes - just try please).

.. important::

    Only push debugged code to the main branch - Thank you!


Disclaimer and License
======================

Disclaimer (general)
--------------------

No warranty is expressed or implied regarding the usefulness or completeness of the information provided for *fuzzycorr* and its documentation. References to commercial products do not imply endorsement by the Authors of *fuzzycorr*. The concepts, materials, and methods used in the codes and described in the docs are for informational purposes only. The Authors have made substantial effort to ensure the accuracy of the code and the docs and the Authors shall not be held liable, nor their employers or funding sponsors, for calculations and/or decisions made on the basis of application of *fuzzycorr*. The information is provided "as is" and anyone who chooses to use the information is responsible for her or his own choices as to what to do with the code, docs, and data and the individual is responsible for the results that follow from their decisions.

BSD 3-Clause License
--------------------

Copyright (c) 2020, Beatriz Negreiros and all other the Authors of *fuzzycorr*.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


.. _Anaconda docs: https://docs.anaconda.com/anaconda/install/
.. _hydro-informatics.github.io: https://hydro-informatics.github.io
.. _git: https://hydro-informatics.github.io/hy_git.html
.. _git bash: https://git-scm.com/downloads
.. _Institute for Modelling Hydraulic and Environmental Systems: https://www.iws.uni-stuttgart.de/en/lww/
.. _write an email: sebastian.schwindtA@Tiws.uni-stuttgart.de
.. _gdal: https://gdal.org/
.. _Beatriz Negreiros: https://beatriznegreiros.github.io/
.. _Kilian Mouris: https://www.iws.uni-stuttgart.de/en/institute/team/Mouris/
.. _Kenny Larrieu: https://klarrieu.github.io/
.. _Lukas Schoeberl: https://github.com/Lukas-create/
.. _QGIS: https://qgis.org/en/site/
.. _Sebastian Schwindt: https://sebastian-schwindt.org/
.. _Windows Command Prompt: https://www.wikihow.com/Open-the-Command-Prompt-in-Windows