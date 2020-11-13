# -*- coding: utf-8 -*-

import sys
import os
import re
import datetime

# If we are building locally, or the build on Read the Docs looks like a PR
# build, prefer to use the version of the theme in this repo, not the installed
# version of the theme.


def is_development_build():
    # PR builds have an interger version
    re_version = re.compile(r'^[\d]+$')
    if 'READTHEDOCS' in os.environ:
        version = os.environ.get('READTHEDOCS_VERSION', '')
        if re_version.match(version):
            return True
        return False
    return True


sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.abspath('..') + '/geotools')
sys.path.append(os.path.abspath('..') + '/fuzzycorr')
sys.path.append(os.path.abspath('..') + '/what2plant')
sys.path.append(os.path.abspath('..') + '/lidartools')
sys.path.append(os.path.abspath('..') + '/examples/fuzzycorr-showcase/')
sys.path.append(os.path.abspath('..') + '/examples/geotools-showcase/')

# the following modules will be mocked (i.e. bogus imports - required for C-dependent packages)
autodoc_mock_imports = [
    "alphashape",
    "earthpy", "earthpy.plot", "ep",
    "fiona",
    "gdal", "ogr", "osr",
    "geojson",
    "geopandas",
    "laspy",
    "mapclassify", "mapclassify.classifiers", "mc",
    "matplotlib", "plt", "colors", "patches", "matplotlib.transform",
    "numpy", "np",
    "pandas", "pd",
    "pyshp", "pyproj",
    "rasterio", "rio",
    "rasterstats",
    "scipy", "scipy.stats", "stats", "interpolate",
    "shapefile",
    "shapely", "shapely.geometry", "Point", "LineString", "Polygon",
    "sqlite3",
    "tabulate",
    "tkinter", "tk", "messagebox", "filedialog",
    "pp", "prepro", "flusstools",
]

import sphinx_rtd_theme
from sphinx.locale import _

project = u'FlussTools'
slug = re.sub(r'\W+', '-', project.lower())
version = '0.1'
release = 'latest'
author = u'Sebastian Schwindt, Beatriz Negreiros, Kilian Mouris, Kenneth Larrieu, Lukas Schoeberl'
copyright = author
language = 'en'

extensions = [
    'sphinx.ext.intersphinx',
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "sphinxcontrib.bibtex",
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.todo',
    'sphinx_thebe',
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive',
    'myst_nb',
    'jupyter_sphinx',
]

templates_path = ['_templates']
source_suffix = '.rst'
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
locale_dirs = ['locale/', 'docs/']
gettext_compact = False

master_doc = 'index'
suppress_warnings = ['image.nonlocal_uri']
pygments_style = 'sphinx'

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.8", None),
    'rtd': ('https://docs.readthedocs.io/en/latest/', None),
    'sphinx': ('http://www.sphinx-doc.org/en/stable/', None),
}

nitpick_ignore = [
    ("py:class", "docutils.nodes.document"),
    ("py:class", "docutils.parsers.rst.directives.body.Sidebar"),
]

numfig = True

myst_admonition_enable = True
myst_deflist_enable = True
myst_url_schemes = ("http", "https", "mailto")
panels_add_bootstrap_css = False

html_theme = 'sphinx_book_theme'
html_theme_options = {

    "theme_dev_mode": True,
    'launch_buttons': {
        'binderhub_url': 'https://mybinder.org',
        'thebe': True,
        'notebook_interface': 'jupyterlab',
        'collapse_navigation': False
    },
    'repository_url': 'https://github.com/ecohydraulics/flusstools/',
    'repository_branch': 'main',
    'use_edit_page_button': False,
    'use_repository_button': True,
}

html_context = {
    'date': datetime.date.today().strftime('%Y-%m-%d'),
    'display_github': True,
    'github_user': 'ecohydraulics',
    'github_repo': 'flusstools',
    'github_version': 'main/',
    'conf_py_path': '/docs/'
}

if not ('READTHEDOCS' in os.environ):
    html_static_path = ['_static/']
    html_js_files = ['debug.js']

    # Add fake versions for local QA of the menu
    html_context['test_versions'] = list(map(
        lambda x: str(x / 10),
        range(1, 100)
    ))

html_last_updated_fmt = ""
html_logo = os.path.abspath('..') + '/docs/img/icon.svg'
html_show_sourcelink = True
html_title = "FlussTools " + version
htmlhelp_basename = 'FlussTools'
html_copy_source = True
html_sourcelink_suffix = ""


jupyter_execute_notebooks = "cache"
thebe_config = {
    "repository_url": "https://github.com/binder-examples/jupyter-stacks-datascience",
    "repository_branch": "master",
}

latex_documents = [
  (master_doc, '{0}.tex'.format(slug), project, author, 'manual'),
]

man_pages = [
    (master_doc, slug, project, [author], 1)
]
# allow errors
execution_allow_errors = True
# execute cells only if any of the cells is missing output
jupyter_execute_notebooks = "auto"

texinfo_documents = [
  (master_doc, slug, project, author, slug, project, 'Miscellaneous'),
]


# Extensions to theme docs
def setup(app):
    from sphinx.domains.python import PyField
    from sphinx.util.docfields import Field

    app.add_object_type(
        'confval',
        'confval',
        objname='configuration value',
        indextemplate='pair: %s; configuration value',
        doc_field_types=[
            PyField(
                'type',
                label=_('Type'),
                has_arg=False,
                names=('type',),
                bodyrolename='class'
            ),
            Field(
                'default',
                label=_('Default'),
                has_arg=False,
                names=('default',),
            ),
        ]
    )
