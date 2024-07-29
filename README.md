## FlussTools

Head for Python scripts for the FlussTools docs. The user documentation is available at [https://flusstools.readthedocs.io](https://flusstools.readthedocs.io/en/latest/). This repository hosts the documentation for [[https://github.com/ecohydraulics/flusstools-pckg/]]. It is intended to be used by developers/contributors only (and those who are interested in becoming a FlussTools contributor).

## Working with Readthedocs

### Update FlussTools

**IMPORTANT:** The documentation is hosted on readthedocs.org, which **cannot import gdal**. Thus, also the automatic pip-installation of flusstools is not possible and the Python scripts need to be copied into the `flusstools/` folder of this repository. For this reason, the import management script (`ROOT/flusstools/import_mgmt.py`) in this repository does not raise import errors; it only prints warning messages. Moreover, the `ROOT/flusstools/` folder contains modified versions of `gdal` in **the `ROOT/flusstools/osgeo/` folder**, which **should never be modified**.

To update the documentation according to a new version of FlussTools, please use the following workflow:

* Update the FlussTools pip-package repository ([[https://github.com/ecohydraulics/flusstools-pckg/]])
* Copy updated Python files to `ROOT/flusstools/` in this repository, but **never overwrite `import_mgmt.py` in this (docs) repository**.
* Determine the new version number of FlussTools according to the [Python package rules](https://py-pkgs.org/07-releasing-versioning.html#version-numbering):
  - Patch release (0.1.0 -> 0.1.1): use for bug fixes, which are backward compatible. Backward compatibility refers to the compatibility of the package with previous versions of itself. For example, if a user was using v0.1.0, they should be able to upgrade to v0.1.1 and have any code they previously wrote still work. It is fine to have so many patch releases that we need to use two digits (e.g., 0.1.27).
  - Minor release (0.1.0 -> 0.2.0): a minor release includes larger bug fixes or new features that are backward compatible, for example, the addition of a new function. It is fine to have so many minor releases that we need to use two digits (e.g., 0.13.0).
  - Major release (0.1.0 -> 1.0.0): release 1.0.0 is used for the new stable releases. Major releases are made for changes that are not backward compatible and may affect many users. Changes that are not backward compatible are called *breaking changes*. For example, changing the name of one of the modules in FlussTools would be a breaking change; if users upgraded to the new major release, any code they had written using the old release name would no longer work, and they would have to change it.
* Update the new version number in `ROOT/docs/conf.py` (find the `version` string variable approximately in line 57) and in `ROOT/setup.py` (not strictly needed - find the `version` string variable approximately in line 8)
* Make potentially required changes in the description of your module (see file structure section below). Note that you will not need to update descriptions of (keyword) arguments and output for your functions because those will be read with [Sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) directly from your updated Python file. So it is important to implement and update docstrings in your Python scripts.
* Finally, push your changes to the main branch of this repository. Sebastian will receive an email and trigger the re-build of the docs, which will include your updates.

Thanks for maintaining FlussTools!

### File structure
The source files for the website live in `docs/` and the default main document is called *index.rst* (can be modified in *conf.py*). All other *rst*-files containing documentatopm need to be linked here.


Add a new section in *index.rst*, define the section depth to use, for example with links to two other files called *license.rst* and *help.rst*, and add some code block:

```
Intro
^^^^^

.. toctree::
	:maxdepth: 2

	license
	help


This is a code block.::

    print("Icecream")
    >> Icecream
```

Note that every file cited in the `toctree` of *index.rst* needs to have a header with `====` underline (level). Make sure that `license` and `help` are exactly indented four spaces, after one empty line after `:maxdepth:`, and directly under the first `:` of `:maxdepth:`.

## Embedd other files

### Link to Python code

Files to embedd should live in `docs/`.
.. literalinclude:: ../code.py
    :lines: 1-

### Image

Images to embedd should live in `docs/img/`. Define reference to image:

```
.. |imageAliasName| image:: ../img/image-name.png
   :align: middle
```

Place image in document:

```
  |imageAliasName|
```

# Use Sphinx RTD Locally

This workflow builds on the developer's [online guide](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html).

## Install packages and an IDE

On Debian, install:

```
sudo apt install python3-sphinx spyder
pip install sphinx
pip install sphinxjp.themes.basicstrap
pip install sphinx-rtd-theme
pip install sphinx-book-theme
pip install sphinx_bootstrap_theme
```

To install an IDE (**recommended**) such as [sublime text](https://www.sublimetext.com/3).


Alternatively, install Spyder IDE:

```
sudo apt install spyder
```

## Build Docs

### Create Base-case

```
mkdir docs
cd docs
sphinx-quickstart
```

Sphinx quickstart will guide through the process of building the documentation framework in the docs folder.

Verify settings in new folder `docs/source/conf.py`.

### Include *markdown* files

To enable markdown with *Sphinx*, install *recommonmark* and *pandoc*:

```
pip install recommonmark
pip install sphinx-markdown-tables
pip install --upgrade recommonmark
sudo apt install pandoc
```

Then, add *recommonmark* to the `extensions` list in *conf.py*:

```
extensions = [
    "recommonmark",
]
```

<!-- with earlier than Sphinx 1.4:

Open *conf.py* and add the following lines at the beginning of the file:

```
# this is conf.py
import recommonmark
from recommonmark.transform import AutoStructify
from recommonmark.parser import CommonMarkParser
source_parsers - {
   ".md": CommonMarkParser
}
```

Still in *conf.py*, go to the bottom of the file and implement the following in the `setup()` function:

```
# [...] bottom of conf.py
def setup(app):
    app.add_config_value("recommonmark_config", {
            "enable_math": True,
            "enable_eval_rst": True,
            "enable_auto_doc_ref": True,
            "auto_code_block": True,
            }, True)
    app.add_transform(AutoStructify)
```
-->

To also enable markdown tables, further extend the `extensions` list in *conf.py*:

```
# conf.py
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.githubpages",
    "sphinx_markdown_tables",
]
```

If markdown is hidden in other file types than `.md` (e.g., in `.txt` files), those can be defined as being understood as markdown files through editing the `source_suffix` variable:

```
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}
```

Read more about *Sphinx* and markdown implementation in the [Sphinx docs](https://www.sphinx-doc.org/en/master/usage/markdown.html).

Another guide was written by [johncrossland](https://gist.github.com/johncrossland/9f6f54d559e9136773172aa0a429b46f) (*GitHub* *gist*) for *Sphinx 1.3* (do not use with Sphinx 1.4 and younger).

## Generate docs

### HTML Website

In `docs/` directory tap:

```
make html
```

After building, the website lives in `build/html`. On Debian systems open the generated website depending on the installed desktop type:

* Lubuntu: `xdg-open`
* Gnome: `gnome-open`
* Xfce (Xubuntu): `exo-open`
* KDE: `kde-open`

### PDF with LaTex

For PDF output, install *Tex Live*:

```
 sudo apt install texlive-full -y
```


## Rendering tools

Render *rst* files instantaneously while typing in a web browser for example with [Socrates](http://socrates.io/) (or [install locally](https://socrates.readthedocs.io/en/latest/installation.html) with `pip install socrates`).

## Deploy website

Cleanup the docs directory (the `build/` folder is not needed - consider excluding it with a *.gitignore* file). Then push your website to GitHub or GitLab, create an account on [readthedocs.org](https://readthedocs.org/) and import your project from GitHub or GitLab.

*readthedocs.org* will generate the website and publish it on *https://YOUR-REPO-NAME.readthedocs.io*.
