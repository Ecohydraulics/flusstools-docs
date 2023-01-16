.. bedanalyst documentation

BedAnalyst
==========

**Algorithms for analyzing riverbed clogging through visualization functions, geospatial interpolation, and a novel fuzzy degree of clogging**

The *BedAnalyst* (``flusstools.bedanalyst``) modules provide *Python3* functions for substrate sample analysis and  a fuzzy logic assessment of so-called `riverbed clogging <https://hydro-informatics.com/documentation/glossary.html#term-Clogging>`_.


Usage
-----


Import
~~~~~~~

Import ``bedanalyst`` from flusstools:

.. code:: python

    from flusstools import bedanalyst as bea


Example (code block)
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from flusstools import bedanalyst as bea
    clogging_pars = bea.fuzzy_analyze("/sample-data/sample.csv")

Example (showcase)
~~~~~~~~~~~~~~~~~~

A showcase is provided with the ``ROOT/examples/bedanalyst-showcase/degree_clogging/main.py`` script that illustrates 


Code structure
--------------

The following diagram highlights function locations in Python scripts and how those are linked to each other.

.. figure:: https://github.com/Ecohydraulics/flusstools/raw/main/docs/img/degree_clogging_uml.jpg
   :alt: structure

The modules ``cd_profiles``, ``nABP_degree_clogging``, and ``interp_z2shp`` are independent from the ``degree_clogging`` module.


Script and function docs
------------------------

Package Head: ``bedanalyst``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.bedanalyst.config
    :members:
    :undoc-members:
    :show-inheritance:


Another algorithm ``degree_clogging``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.bedanalyst.degree_clogging
    :members:


Another algorithm ``interp_z2shp``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: flusstools.bedanalyst.interp_z2shp
    :members:

