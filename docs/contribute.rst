.. _contribute:

Contributing
============

Become a contributor
--------------------

Many team members joined while working on their Bachelor's or Master's thesis. If you are a student, why not contribute to *flusstools* within an innovative thesis? Have a look at the open `Bachelor and Master Thesis topics <https://www.iws.uni-stuttgart.de/en/lww/education/>`_.

You do not have to be a student to join - just reach out to `Sebastian Schwindt`_.


How the project is organized
----------------------------

*flusstools* lives in **two** GitHub repositories:

* `flusstools-pckg <https://github.com/Ecohydraulics/flusstools-pckg>`_ - the Python **code**, released to `PyPI <https://pypi.org/project/flusstools/>`_.
* `flusstools-docs <https://github.com/Ecohydraulics/flusstools-docs>`_ - **this documentation** (the ``.rst`` text files).

The documentation installs *flusstools* straight from PyPI and builds the function/class reference **automatically from the docstrings in the code**. So you never copy code into the docs repo - you publish a release of the code, and edit the text here.


Set up a development environment
--------------------------------

GDAL only installs reliably with conda/mamba (see :ref:`install`). Clone the code repo, create the environment, and install *flusstools* in editable mode:

.. code:: console

    git clone https://github.com/Ecohydraulics/flusstools-pckg.git
    cd flusstools-pckg
    mamba env create -f environment.yml
    mamba activate flussenv
    pip install -e . --no-deps

``--no-deps`` is used because all dependencies already come from ``environment.yml``. "Editable" (``-e``) means your code changes take effect immediately, without reinstalling.


Write code
----------

A few rules keep the package clean and the docs working:

* **Imports:** every module imports exactly what it uses, at the top of the file - there is no central import file. To use a function from another *flusstools* module, import it directly from where it is defined, e.g. ``from ..geotools.geotools import rasterize``.
* **Docstrings are the docs.** Write a `Google-style <https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html>`_ docstring for every public function and class; it is exactly what shows up in this documentation. The sections you normally need:

  * ``Args:`` - describe each parameter
  * ``Returns:`` - describe what comes back
  * ``Raises:`` - errors it may raise *(optional)*
  * ``Example:`` - a short usage snippet *(optional, but appreciated)*

* **Make a function public:** if users should be able to call your new function or class, add its name to the ``__all__`` list in that subpackage's ``__init__.py``.
* **Added a new library?** Declare it in three places: ``pyproject.toml`` (``dependencies``), ``environment.yml``, and - using its *import* name (e.g. ``skfuzzy``, not ``scikit-fuzzy``) - the ``autodoc_mock_imports`` list in ``flusstools-docs/docs/conf.py``.
* Keep it readable, and only push code that actually runs.


Release a new version
---------------------

Once your code works and is merged, publish it to PyPI so that users - and these docs - receive it. The full recipe is in `CONTRIBUTING.md <https://github.com/Ecohydraulics/flusstools-pckg/blob/main/docs/CONTRIBUTING.md>`_; the short version:

1. Bump ``version`` in ``flusstools-pckg/pyproject.toml`` (e.g. ``2.0.1`` to ``2.0.2``).
2. Build and upload (needs a PyPI API token):

   .. code:: console

       mamba run -n flussenv python -m build
       TWINE_USERNAME=__token__ python -m twine upload dist/*

3. Tag the release on GitHub:

   .. code:: console

       git tag -a v2.0.2 -m "FlussTools 2.0.2"
       git push --tags


Update this documentation
-------------------------

Edit (or add) the matching ``.rst`` file in ``flusstools-docs/docs/`` and push to ``main`` - Read the Docs rebuilds automatically:

.. code:: console

    git clone https://github.com/Ecohydraulics/flusstools-docs.git
    cd flusstools-docs
    # edit docs/<module>.rst
    git commit -am "docs: describe <something>"
    git push

To document a **new module**, add a ``.. automodule:: flusstools.<subpackage>.<module>`` block to the matching ``.rst`` file (copy the pattern from ``geotools.rst``) and list the page in the ``toctree`` of ``index.rst``.

.. important::

    Only push code that you have run successfully - thank you!

.. _Sebastian Schwindt: https://sebastian-schwindt.org/
