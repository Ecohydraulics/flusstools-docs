.. fuzzycorr documentation master file, created by
   sphinx-quickstart on Tue Nov 04 10:43:23 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root ``toctree`` directive.


FuzzyCorr
=========

This repository contains the work developed for a Master Thesis on fuzzy map comparison methods to evaluate the performance of hydro-morphodynamic numerical models. Please read the License terms for code usage and re-distribution.

Sediment transport and hydraulic processes can be reproduced with numerical models such as SSIIMM, Hydro_AS_2D, TELEMAC and many more. The accuracy of numerical models is assessed through comparing the simulated and the observed datasets, which constitutes a model validation. With the purpose of analyzing simulated and observed bed elevation change, two methods of comparison can be applied:

1. Comparison via statistical methods such as RMSE (Root Mean Squared Error) or visual human comparison. However, local measures of similarity (or a similarity) like the RMSE are very sensible to uncertainty of location and amount, thus indicating low agreement even when overall patterns were adequately simulated.

2. Visual comparison captures global similarity, which is one of the reasons why modelers often use it for model validation. Humans are capable of finding patterns without deliberately trying, and therefore, this type of comparison provides substantial advantages over local similarity measures. Nevertheless, more research has to be done to implement automated validation tools that emulate human thinking. This is necessary because human comparison is not transparent, prone to subjective interpretations, time consuming, and hardly reproducible.

In this context, the concept of fuzzy set theory has capacities to consider similarity of spatial pattern analogous to human thinking. For instance, fuzziness of location introduces a tolerance regarding spatial uncertainty in the results of hydro-morphodynamic models. To this end, fuzzy logic enables an objective validation of such models by overcoming  uncertainties in the model structure, parameters and input data.

The algorithms provided with ``fuzzycorr`` address the necessity in evaluating (or validating) model performance through the use of fuzzy map comparison. Future developments aim to go beyond a one-way validation towards a two-way communication between the validation algorithms and the models. The two-way communication represents a feedback loop that will eventually enable an automated calibration of numerical hydro-morphodynamic models.

Usage
-----

Basics
~~~~~~~

The following code block exemplifies the usage of *fuzzycorr* to explore the fuzzy correlation between two (e.g., observed and modeled) maps (in *GeoTIFF* format):

.. code:: python

   from flusstools import fuzzycorr as fc


Example (showcase)
~~~~~~~~~~~~~~~~~~

The best way to learn the usage is by examples. In the directory  ``examples``, the usage of the modules are demonstrated in a case study. Inside the folder ``salzach_case``, the results from a hydro-morphodynamic numerical simulation ( i.e., simulated bed elevation change, deltaZ) are located in ``raw_data``. For more details on the hydro-morphodynamic numerical refer to `Beckers et al. (2020) <https://www.researchgate.net/publication/342181386_Bayesian_Calibration_and_Validation_of_a_Large-scale_and_Time-demanding_Sediment_Transport_Model>`__.

The following showcase scripts live in *ROOT/examples/fuzzycorr-showcase/*:

-  ``prepro_salzach.py``: example of the usage of the class ``FuzzyPreProcessor`` of the module ``prepro.py``, where vector data is interpolated and rasterized.
-  ``classification_salzach.py``: example of the usage of the class ``PreProCategorization`` of the module ``prepro.py``.
-  ``fuzzycomparison_salzach.py``: example of the usage of the class ``FuzzyComparison`` of the module ``fuzzycomp.py``, which creates a correlation (similarity) measure between simulated and observed datasets.
-  ``plot_salzach.py``, ``plot_class_rasters.py`` and ``performance_salzach``: example of the usage of the module ``plotter.py``.
-  ``random_map``: example of generating a raster following a uniform random distribution, which uses the module ``prepro.py``.


Structure
---------

This package contains the following modules, which were designed in *Python 3.6*:

- *prepro.py* includes functions for reading, normalizing and rasterizing vector data. These are preprocessing steps for fuzzy map comparison (module fuzzycomp).
- *fuzzycomp.py* provides routines for fuzzy map comparison in continuous valued rasters. Refer to `Hagen (2006) <https://www.researchgate.net/publication/242690490_Comparing_Continuous_Valued_Raster_Data_A_Cross_Disciplinary_Literature_Scan>`__ for more details.
- *plotter.py*: Visualization routines for output and input rasters.
-  The package documentation is located in the folder *docs*.


Pre-processing: prepro.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.fuzzycorr.prepro
   :members:
   :private-members:

Fuzzy map comparison core: fuzzycomp.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.fuzzycorr.fuzzycomp
   :members:
   :private-members:

Plot routines: plotter.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flusstools.fuzzycorr.plotter
   :members:
   :private-members:


References
----------

* `Ross Kushnereit <https://github.com/rosskush/skspatial>`__
* `Chris Wills <http://chris35wills.github.io/gridding_data/>`__
