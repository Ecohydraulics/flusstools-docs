.. flusstools documentation parent file.


FlussTools
==========

The analysis, research and science-based design of fluvial ecosystems involve complex challenges for interdisciplinary experienced teams. We have created *flusstools* to meet the complex challenges and to at least partially automate time-consuming, repetitive processes. "We" stands for individuals with a great passion for rivers (German: "Flüsse") and programming. Most of us work (or have worked) at the University of Stuttgart (Germany) at the `Institute for Modelling Hydraulic and Environmental Systems`_. In the context of our scientific endeavor, we have a strong commitment to transparent open-source applications. With *flusstools*, we want to share our research-based open-source algorithms with a broad interest group in a well documented form. We welcome new team members (for example to add or amend a module) at any time - read more in the :ref:`contribute` section.

.. important::

	Follow the installation instructions on `hydro-informatics.com <https://hydro-informatics.com/python-basics/pyinstall.html>` to make sure that GDAL works on your computer as desired.

Currently, *flusstools* comes with the following modules:

* *geotools* - versatile functions for processing spatial data for fluvial ecosystem analyses based on `gdal`_ and other open source libraries (developers: `Kilian Mouris`_, `Beatriz Negreiros`_, and `Sebastian Schwindt`_).
* *fuzzycorr* - a map comparison toolkit that builds on fuzzy sets to assess the accuracy of (numerical) river models (principal developer: `Beatriz Negreiros`_).
* *lidartools* - *Python* wrappers for `lastools`_ (forked and modified from `Kenny Larrieu`_).

.. note::
    The documentation is also as available as `style-adapted PDF <https://flusstools.readthedocs.io/_/downloads/en/latest/pdf/>`_.


.. toctree::
    :hidden:

    About <self>

.. toctree::
    :hidden:

    Installation <getstarted>

.. toctree::
    :hidden:

    Geospatial Analyst (GeoTools) <geotools>

.. toctree::
    :hidden:

    Map Correlation (FuzzyCorr) <fuzzycorr>

.. toctree::
    :hidden:

    Lidar Tools (LasPy/LasTools) <lidartools>

.. toctree::
    :hidden:

    Contributing <contribute>

.. toctree::
    :hidden:

    Disclaimer and License <license>

More information and examples are available in the docs of every *flusstools* module.

.. _Institute for Modelling Hydraulic and Environmental Systems: https://www.iws.uni-stuttgart.de/en/lww/
.. _Beatriz Negreiros: https://beatriznegreiros.github.io/
.. _gdal: https://gdal.org/
.. _Kilian Mouris: https://www.iws.uni-stuttgart.de/en/institute/team/Mouris/
.. _Kenny Larrieu: https://klarrieu.github.io/
.. _lastools: https://rapidlasso.com/lastools/
.. _QGIS: https://qgis.org/en/site/
.. _Sebastian Schwindt: https://sebastian-schwindt.org/
