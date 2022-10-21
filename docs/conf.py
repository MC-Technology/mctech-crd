"""Sphinx configuration."""
project = "MCtech Cosmic Ray Detector"
author = "MC Tech"
copyright = "2022, MC Tech"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
