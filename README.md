## FlussTools — Documentation

This repository holds the **documentation sources** (reStructuredText `.rst` files) for [`flusstools`](https://github.com/Ecohydraulics/flusstools-pckg). The rendered documentation is published at **[flusstools.readthedocs.io](https://flusstools.readthedocs.io/en/latest/)**.

The Python **code** lives in a separate repository — [flusstools-pckg](https://github.com/Ecohydraulics/flusstools-pckg) — and is released to [PyPI](https://pypi.org/project/flusstools/). Read the Docs **installs `flusstools` from PyPI** and generates the function/class reference automatically from the docstrings in the code. This repository therefore contains **no copy of the package code**.

### How the build is wired

- **`.readthedocs.yaml`** — installs the Sphinx toolchain from `requirements.txt`, then `pip install --no-deps flusstools` (so GDAL and the other heavy dependencies are never built on Read the Docs).
- **`docs/conf.py`** — Sphinx configuration. The geospatial / C-dependent imports (GDAL, numpy, rasterio, …) are listed in `autodoc_mock_imports`, so autodoc can import `flusstools` without them.
- **`docs/*.rst`** — the documentation pages; `docs/index.rst` is the landing page.
- **`examples/`** — showcase scripts referenced from the documentation.

### Build the docs locally

```sh
mamba create -n flussdocs -c conda-forge python=3.11 gdal
mamba activate flussdocs
pip install -r requirements.txt   # Sphinx toolchain
pip install flusstools            # so autodoc can import the real package
sphinx-build -b html docs _build/html
```

Then open `_build/html/index.html` in a browser.

### Editing & contributing

Edit the relevant `docs/<module>.rst` file and push to `main` — Read the Docs rebuilds automatically. The full workflow (writing docstrings, documenting a new module, and releasing a new `flusstools` version) is on the [Contributing page](https://flusstools.readthedocs.io/en/latest/contribute.html).
