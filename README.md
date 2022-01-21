## FlussTools

Head for Python scripts for river analyses.

The full documentation is available at [https://flusstools.readthedocs.io](https://flusstools.readthedocs.io/en/latest/) (currently still under construction).

# HowTo Sphinx RTD

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

To install the *ATOM* IDE (**recommended**) tap:

Read more about [ATOM](https://atom.io/) or how to [install *ATOM* on any platform](https://flight-manual.atom.io/getting-started/sections/installing-atom).

```
wget -qO - https://packagecloud.io/AtomEditor/atom/gpgkey | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main" > /etc/apt/sources.list.d/atom.list'
sudo apt update
sudo apt install atom
```

Alternatively to *ATOM*, install Spyder IDE with:

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

## Update documentation

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



## Rendering tools

Render *rst* files instantaneously while typing in a web browser for example with [Socrates](http://socrates.io/) (or [install locally](https://socrates.readthedocs.io/en/latest/installation.html) with `pip install socrates`).

## Deploy website

Cleanup the docs directory (the `build/` folder is not needed - consider excluding it with a *.gitignore* file). Then push your website to GitHub or GitLab, create an account on [readthedocs.org](https://readthedocs.org/) and import your project from GitHub or GitLab.

*readthedocs.org* will generate the website and publish it on *https://YOUR-REPO-NAME.readthedocs.io*.
