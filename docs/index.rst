.. flusstools documentation parent file.


FlussTools
==========

The analysis, research, and science-based design of hydrological ecosystems involve complex challenges for interdisciplinary experienced teams. We have created *flusstools* to meet the complex challenges and to at least partially automate time-consuming, repetitive processes of processing field data, numerical model outputs, or geospatial data. "We" stands for individuals with a great passion for rivers (German: "Flüsse") and programming. Most of us work (or have worked) at the University of Stuttgart (Germany) at the `Institute for Modelling Hydraulic and Environmental Systems`_. Because we have a strong commitment to transparent open-source applications, we created *flusstools* and we welcome new team members (for example, to add or amend a module) at any time - read more in the :ref:`contribute` section.

.. important::

    Follow the installation instructions on `hydro-informatics.com <https://hydro-informatics.com/python-basics/pyinstall.html>`_ to make sure that GDAL works on your computer as desired.

Currently, *flusstools* comes with the following modules:

* *bedanalyst* - for plotting and numeric analysis of riverbed characteristic to identify, for instance, clogging (developers: `Beatriz Negreiros`_, and `Ricardo Barros`_).
* *geotools* - versatile functions for processing spatial data for fluvial ecosystem analyses based on `gdal`_ and other open source libraries (developers: `Kilian Mouris`_, `Beatriz Negreiros`_, and `Sebastian Schwindt`_). The functions are explained with the geospatial Python `tutorials on hydro-informatics.com <https://hydro-informatics.com/jupyter/geo-shp.html>`_ and the `HydroMorphodynamics YouTube channel <https://www.youtube.com/@hydroinformatics>`_.
* *fuzzycorr* - a map comparison toolkit that builds on fuzzy sets to assess the accuracy of (numerical) river models (principal developer: `Beatriz Negreiros`_).
* *lidartools* - *Python* wrappers for `lastools`_ (forked and modified from `Kenny Larrieu`_).

.. admonition:: How to cite FlussTools

    If our codes helped you to accomplish your work, we won't ask you for a coffee, but to cite and spread the utility of our code - Thank you!

    .. code::

        @software{flussteam_tools_2023,
                  author       = {Sebastian Schwindt and
                                  Beatriz Negreiros and
                                  Ricardo Barros and
                                  Niklas Henning and
                                  Kilian Mouris},
                  title        = {FlussTools},
                  year         = 2023,
                  publisher    = {GitHub \& Center for Open Science (OSF)},
                  version      = {v1.1.7},
                  doi          = {10.17605/OSF.IO/G7K52},
                  url          = {https://doi.org/10.17605/OSF.IO/G7K52}
                }


The documentation is also as available as `style-adapted PDF <https://flusstools.readthedocs.io/_/downloads/en/latest/pdf/>`_.


.. toctree::
    :hidden:

    About <self>

.. toctree::
    :hidden:

    Installation <getstarted>

.. toctree::
    :hidden:

    Riverbed Analyst (BedAnalyst) <bedanalyst>

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
.. _Ricardo Barros: https://ricardovobarros.github.io/
.. _Sebastian Schwindt: https://sebastian-schwindt.org/
