Plant database
======================================

.. documentation master file.

Nature-Based Solutions (NBS) for river engineering experience incresing popularity to leverage flood risk and ecosystem management in the light of climate change. Even though the demand for NBS is high, there design regarding scale and placement still is an important challenge. In some cases, missing knowledge and trust in NBS lead to overestimations of costs and time. This plant database constitutes an important step in the design of NBS with a plant data base for river engineering. 


.. This documentation is also as available as style-adapted PDF (`download <https://.readthedocs.io/plantDB/downloads/en/latest/pdf/>`_).

Installation
============

Use ``git`` to download the ``plantDB`` repository (make sure to
`install Git Bash`_):

1. Open *Git Bash* (or any other git-able *Terminal*)
2. Create or select a target directory for ``plantDB`` (e.g., in your
   *Python* project folder)
3. Type ``cd "D:/Target/Directory/"`` to change to the target
   installation directory.
4. Clone the repository.

.. code:: console

   $ cd "D:/Target/Directory/"
   $ git clone https://github.com/Lukas-create/plantDB.git

Now, ``plantDB`` lives in ``"D:/Target/Directory/plantDB/plantDB"``.

Usage
=====

Import
~~~~~~~

1. Run *Python* and add the download directory of ``plantDB`` to the
   system path:

.. code:: python

   from flusstools import what2plant as w2p


2. Import ``plantDB``:

.. code:: python

   import plantDB as 

Example
~~~~~~~

.. code:: python

   import plantDB as re

   #To search for plant data start by calling question() in search
   re.search.question()

   #choose between one of the three provided options by entering the respective number in the console

.. code:: python

   import plantDB as re

   #If you want to search for plant data in the database directly, call search_db_via_query() and provide an corresponding sql - query.
   query = "habitat = 'Alpenvorland'"
   re.search.search_db_via_query(query)

   #the above function call will print all plants including their parameters which are located in 'Alpenvorland'
   #plantDB supports arbitrary sql-querys over the datafields in the provided 'Pflanzendaten.db' database

.. code:: python

   import plantDB as re

   #to create the database Pflanzendaten.db call inputquestion() in sqlinput

   re.sqlinput.inputquestion()

   #by that you get to choose in the console if you want to add data via sql command or get the data from an existing csv file
   #the column names and entries of the csv file need to match the specified database format



Code Documentation
==================

Package structure
-----------------

.. figure:: https://en.wikipedia.org/wiki/File:UML_diagrams_overview.svg
   :alt: structure



Scripts and functions
---------------------


``plantDB`` 
~~~~~~~~~~~~~~~~~~~~~
.. automodule:: plant
   :members:

Search something
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: search
   :members:

SQL mgmt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: sqlinput
   :members:




