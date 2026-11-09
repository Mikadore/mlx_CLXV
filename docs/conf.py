"""Sphinx configuration for the MinilibX Python API documentation."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python" / "src"))

project = "MinilibX Python API"
copyright = "2000–2026, Olivier Crouzet"
author = "Olivier Crouzet"
release = (ROOT / "version").read_text(encoding="utf-8").strip()

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]

autosummary_generate = True
autoclass_content = "both"
autodoc_typehints = "description"
autodoc_member_order = "bysource"
napoleon_numpy_docstring = False
napoleon_google_docstring = True

templates_path = []
exclude_patterns = ["_build"]
language = "en"

html_theme = "sphinx_rtd_theme"
html_title = "MinilibX Python API"
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
    "sticky_navigation": True,
}
