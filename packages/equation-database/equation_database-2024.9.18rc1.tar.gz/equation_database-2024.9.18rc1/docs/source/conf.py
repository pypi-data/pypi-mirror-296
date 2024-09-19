# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime
import os
import re
import sys

import toml

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# https://github.com/sympy/sphinx-math-dollar/issues/18
from docutils.nodes import (
    doctest_block,
    image,
    literal,
    literal_block,
    math,
    math_block,
    pending,
    raw,
    rubric,
    substitution_definition,
    target,
)

sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

try:
    info = toml.load("../../pyproject.toml")
except FileNotFoundError:
    info = toml.load("pyproject.toml")
project = info["project"]["name"]
copyright = str(datetime.datetime.now().year) + ", Alexander Puck Neuwirth"
author = "Alexander Puck Neuwirth"
version = re.sub("^", "", os.popen("git describe --tags").read().strip())
rst_epilog = f""".. |project| replace:: {project} \n\n"""

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.githubpages",
    "sphinx.ext.viewcode",
    "sphinx_math_dollar",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.doctest",
    # "matplotlib.sphinxext.plot_directive",
    #'numpydoc',
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "nbsphinx",
    "jupyter_sphinx",
    #'jupyter_sphinx.execute'
    # "autoapi.extension",
]
napoleon_google_docstring = True

autosummary_generate = True
autosummary_generate_imported = True
autosummary_private_members = True
autosummary_imported_members = False
autoapi_type = "python"
autoapi_dirs = ["../../equation_database"]
autoapi_python_class_content = "both"

autodoc_default_options = {
    "private-members": False,
    "inherited-members": True,
    "special-members": False,
}


templates_path = ["_templates"]
exclude_patterns = []


math_dollar_node_blacklist = (
    literal,
    math,
    doctest_block,
    image,
    literal_block,
    math_block,
    pending,
    raw,
    rubric,
    substitution_definition,
    target,
)  # (FixedTextElement,math)
# print(NODE_BLACKLIST)


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
