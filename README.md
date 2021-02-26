## FlussTools

Head for Python scripts for river analyses.

The full documentation is available at [https://flusstools.readthedocs.io](https://flusstools.readthedocs.io/en/latest/) (currently still under construction).

# HowTo Sphinx RTD

This workflow builds on the developer's [online guide](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html).

## Install packages and Spyder IDE

On Debian, install:

```
sudo apt install python3-sphinx spyder
pip install sphinx
pip install sphinx-rtd-theme
pip install sphinx-book-theme
```

## Create base-case

```
mkdir docs
cd docs
sphinx-quickstart
```

Sphinx quickstart will guide through the process of building the documentation framework in the docs folder.

Verify settings in new folder `docs/source/conf.py`

## Generate docs

In `docs/` directory tap:

```
make html
```

After building, the website lives in `build/html`. On Debian systems open the generated website depending on the installed desktop type:

* Lubuntu: `xdg-open`
* Gnome: `gnome-open`
* Xfce (Xubuntu): `exo-open`
* KDE: `kde-open`

## Modify documentation

The source files for the website live in `docs/source/` and the default main document is called *index.rst* (can be modified in *conf.py*). All other *rst*-files containing documentatopm need to be linked here.

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


```


## Rendering tools

Render *rst* files instantaneously while typing in a web browser for example with [Socrates](http://socrates.io/) (or [install locally](https://socrates.readthedocs.io/en/latest/installation.html) with `pip install socrates`).

## Deploy website

Cleanup the docs directory (the `build/` folder is not needed - consider excluding it with a *.gitignore* file). Then push your website to GitHub or GitLab, create an account on [readthedocs.org](https://readthedocs.org/) and import your project from GitHub or GitLab. 

*readthedocs.org* will generate the website and publish it on *https://YOUR-REPO-NAME.readthedocs.io*.
