.. las4windows documentation master file.

The las4windows docs
====================

*las4windows* is forked from `GCS_scripts by Kenny Larrieu <https://github.com/klarrieu>`_. The original code is designed for *Python2* and the commercial ``arcpy`` library. The tweaked codes of *las4windows* run with Python 3.8 and work without ``arcpy``. This repository only uses the GUI for lidar processing with `LASTools <https://rapidlasso.com/lastools/>`_.

Because *LASTools* is proprietary, its executables can hardly be run on Linux or other UNIX-based systems. This is why *las4windows* is a *Windows*-only (*nomen est omen*).

Prerequisites
=============


*LASTools* is used for LiDAR Data Processing and can be downloaded `here <https://rapidlasso.com/lastools/>`_.

Python 3.x dependencies are provided with ``requirements.txt`` (most modern IDEs will provide to auto-install the packages listed in ``requirements.txt``). Otherwise, make sure to install the following libraries in the *Python3.x* environment:

   * numpy
   * scipy
   * tkinter
   * pandas


Code Documentation
==================


The GUI script
~~~~~~~~~~~~~~
.. automodule:: LiDAR_processing_GUI
   :members:

LiDAR processing
~~~~~~~~~~~~~~~~
.. automodule:: lidar_core
   :members:

File functions
~~~~~~~~~~~~~~
.. automodule:: file_functions
   :members:

Disclaimer and License
======================

Disclaimer (general)
--------------------

No warranty is expressed or implied regarding the usefulness or completeness of the information provided for *las4windows* and its documentation. References to commercial products do not imply endorsement by the Authors of *las4windows*. The concepts, materials, and methods used in the codes and described in the docs are for informational purposes only. The Authors have made substantial effort to ensure the accuracy of the code and the docs and the Authors shall not be held liable, nor their employers or funding sponsors, for calculations and/or decisions made on the basis of application of *las4windows*. The information is provided "as is" and anyone who chooses to use the information is responsible for her or his own choices as to what to do with the code, docs, and data and the individual is responsible for the results that follow from their decisions.

BSD 3-Clause License
--------------------

Copyright (c) 2020, the Authors of *las4windows*.
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

