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

Install dependencies
--------------------

The necessary modules for running this repo are specified in ``environment.yml``. To install all packages in the environment:

* Navigate ( ``cd``) with the Anaconda Prompt through your directories to the ``.yml`` file
* Type ``conda env create -f environment.yml``
* Active the new environment with ``conda activate env-fuzzycorr``

Usage
=====

The best way to learn the usage is by examples. In the directory  ``examples``, the usage of the modules are demonstrated in a case study. Inside the folder ``salzach_case``, the results from a hydro-morphodynamic numerical simulation ( i.e., simulated bed elevation change, deltaZ) are located in ``raw_data``. For more details on the hydro-morphodynamic numerical refer to `Beckers et al. (2020) <https://www.researchgate.net/publication/342181386_Bayesian_Calibration_and_Validation_of_a_Large-scale_and_Time-demanding_Sediment_Transport_Model>`__.

   -  ``prepro_salzach.py``: example of the usage of the class ``PreProFuzzy`` of the module ``prepro.py``, where vector data is interpolated and rasterized.
   -  ``classification_salzach.py``: example of the usage of the class ``PreProCategorization`` of the module ``prepro.py``.
   -  ``fuzzycomparison_salzach.py``: example of the usage of the class ``FuzzyComparison`` of the module ``fuzzycomp.py``, which creates a correlation (similarity) measure between simulated and observed datasets.
   -  ``plot_salzach.py``, ``plot_class_rasters.py`` and ``performance_salzach``: example of the usage of the module ``plotter.py``.
   -  ``random_map``: example of generating a raster following a uniform random distribution, which uses the module ``prepro.py``.

Structure
=======================

This package contains the following modules, which were designed in *Python 3.6*:

- ``prepro.py``: Includes functions for reading, normalizing and rasterizing vector data. These are preprocessing steps for fuzzy map comparison (module fuzzycomp).
- ``fuzzycomp.py``: Provides routines for fuzzy map comparison in continuous valued rasters. The reader is referred to `Hagen(2006) <https://www.researchgate.net/publication/242690490_Comparing_Continuous_Valued_Raster_Data_A_Cross_Disciplinary_Literature_Scan>`__ for more details (more to come).
- ``plotter.py``: Visualization routines for output and input rasters.
-  The package documentation is located in the folder ``docs``.


Pre- and post-processing: prepro.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: prepro
   :members:
   :private-members:

Fuzzy map comparison core: fuzzycomp.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: fuzzycomp
   :members:
   :private-members:

Plot routines: plotter.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: plotter
   :members:
   :private-members:




References
----------

* `Ross Kushnereit <https://github.com/rosskush/skspatial>`__
* `Chris Wills <http://chris35wills.github.io/gridding_data/>`__

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
