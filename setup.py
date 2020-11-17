from setuptools import setup, find_packages
from pathlib import Path
import subprocess
import sys


lines = Path(".").joinpath("__init__.py")
version = "0.1"
for line in lines.read_text().split("\n"):
    if line.startswith("__version__ ="):
        version = line.split(" = ")[-1].strip('"')
        break


def GDAL_with_version():
    try:
        tmp = subprocess.check_output(["gdal-config", "--version"])
        return "gdal==" + str(tmp.decode("utf8").replace("\n", ""))
    except NOT_FOUND_EXCEPTION:
        print("The gdal-config binary was not found")
        raise
    except:
        raise


def command_call(cmd, *args, **kwargs):
    print("Calling the following command: '{}'".format(" ".join(cmd)))
    process = subprocess.Popen(cmd, *args, **kwargs)
    process.wait()
    if process.returncode != 0:
        raise RuntimeError(
            "The return code of the process is {}".format(process.returncode))


if sys.version_info[0] < 3:
    NOT_FOUND_EXCEPTION = OSError
    NUMPY = "numpy<1.17"
    CFTIME = "cftime==1.1.1"
    setup_kwargs = {"setup_requires": [NUMPY]}
else:
    NOT_FOUND_EXCEPTION = FileNotFoundError
    NUMPY = "numpy"
    CFTIME = "cftime"
    setup_kwargs = {}


setup(
    name="flusstools-docs",
    version=version,
    python_requires=">=3.6",
    author="FlussTeam",
    author_email="sebastian.schwindt@iws.uni-stuttgart.de",
    url="https://github.com/Ecohydraulics/flusstools-docs",
    project_urls={
        "Documentation": "https://flusstools.readthedocs.io/",
        "Funding": "https://www.uni-stuttgart.de/",
        "Source": "https://github.com/Ecohydraulics/flusstools-docs",
    },
    # this should be a whitespace separated string of keywords, not a list
    keywords="rivers geo-spatial data processing numerical model validation",
    description="Analyze and design fluvial ecosystems",
    license="BSD License",
    long_description=Path("./README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        GDAL_with_version(),
        NUMPY,
        CFTIME,
        "pyyaml",
        "docutils>=0.15",
        "sphinx",
        "click",
        "pydata-sphinx-theme~=0.4.1",
        "beautifulsoup4",
        "flusstools", ## --always-copy
        'importlib-resources~=3.0.0; python_version < "3.7"',
    ],
    # dependency_links=[
    #     "git+https://github.com/ecohydraulics/flusstools-pckg#egg=flusstools-pckg"
    # ],
    include_package_data=True,
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
    entry_points={
        "sphinx.html_themes": ["sphinx_book_theme = sphinx_book_theme"],
        "console_scripts": ['pycif=pycif.__main__:main'],
    },
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
    **setup_kwargs
)
