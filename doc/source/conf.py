# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "onc"
copyright = "2024, ONC Data Team"
author = "ONC Data Team"
release = "2.3.5"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_nb",
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]

exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_favicon = "https://data.oceannetworks.ca/favicon.ico"

# -- Extension configuration -------------------------------------------------

myst_enable_extensions = [
    "colon_fence",  # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#code-fences-using-colons
]
myst_heading_anchors = 2

# -- MyST NB --
# https://myst-nb.readthedocs.io/en/latest/configuration.html
nb_execution_mode = "off"  # off for faster local build. It is deleted in doc.yml for building doc in GitHub Actions
nb_merge_streams = True
nb_execution_timeout = 90
nb_execution_raise_on_error = True
nb_execution_excludepatterns = ["Code_Examples/*"]

# -- Sphinx AutoAPI --
# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html
autoapi_dirs = ["../../src"]
autoapi_ignore = ["*modules*"]
suppress_warnings = ["autoapi.python_import_resolution"]
