.. bedanalyst documentation

BedAnalyst
==========

**Aglorithms for analyzing riverbed clogging and substrate samples**

The *BedAnalyst* (``flusstools.bedanalyst``) modules provide *Python3* functions for many sorts of substrate samples to analyze so-called `riverbed clogging <https://hydro-informatics.com/documentation/glossary.html#term-Clogging>`_.


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

A showcase is provided with the ``ROOT/examples/bedanalyst-showcase/use_bea_analysis.py`` script that illustrates ...



Code structure
--------------

The following diagram highlights function locations in Python scripts and how those are linked to each other.

.. figure:: https://github.com/Ecohydraulics/flusstools/raw/main/docs/img/geotools-uml.png
   :alt: structure

   *Diagram of the code structure (needs to be updated).*


Script and function docs
------------------------


Package Head: ``bedanalyst``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.bedanalyst.config
    :members:
    :undoc-members:
    :show-inheritance:


Another algorithm ``another_script``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.bedanalyst.cd_profiles
    :members:


