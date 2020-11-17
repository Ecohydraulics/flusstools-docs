from setuptools import setup, find_packages
from pathlib import Path

lines = Path(".").joinpath("__init__.py")
version = "0.1"  # will be overwritten if defined in init
for line in lines.read_text().split("\n"):
    if line.startswith("__version__ ="):
        version = line.split(" = ")[-1].strip('"')
        break

setup(
    name="flusstools",
    version=version,
    python_requires=">=3.4",
    author="FlussTeam",
    author_email="sebastian.schwindt@iws.uni-stuttgart.de",
    url="https://github.com/Ecohydraulics/flusstools-pckg",
    project_urls={
        "Documentation": "https://flusstools.readthedocs.io/",
        "Funding": "https://www.uni-stuttgart.de/",
        "Source": "https://github.com/Ecohydraulics/flusstools",
        "Tracker": "https://github.com/Ecohydraulics/flusstools/issues",
    },
    # this should be a whitespace separated string of keywords, not a list
    keywords="rivers geo-spatial data processing numerical model validation",
    description="Analyze and design fluvial ecosystems",
    license="BSD License",
    long_description=Path("./README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "docutils>=0.15",
        "sphinx",
        "click",
        "pydata-sphinx-theme~=0.4.1",
        "beautifulsoup4",
        "flusstools @ git+https://github.com/ecohydraulics/flusstools-pckg#egg=0.1",
        'importlib-resources~=3.0.0; python_version < "3.7"',
    ],
    dependency_links=[
        "git+https://github.com/ecohydraulics/flusstools-pckg#egg=0.1"
    ],
    extras_require={
        "code_style": ["pre-commit~=2.7.0"],
        "sphinx": [
            "folium",
            "numpy",
            "matplotlib",
            "ipywidgets",
            "pandas",
            "nbclient",
            "myst-nb~=0.10.1",
            "sphinx-togglebutton>=0.2.1",
            "sphinx-copybutton",
            "plotly",
            "sphinxcontrib-bibtex",
            "sphinx-thebe",
            "ablog~=0.10.11",
        ],
        "testing": [
            "myst_nb~=0.10.1",
            "sphinx_thebe",
            "coverage",
            "pytest~=6.0.1",
            "pytest-cov",
            "pytest-regressions~=2.0.1",
        ],
        "live-dev": ["sphinx-autobuild", "web-compile~=0.2.1"],
    },
    entry_points={"sphinx.html_themes": ["sphinx_book_theme = sphinx_book_theme"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 2 - Pre-Alpha",
    ],
)
