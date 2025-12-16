# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# 소스 코드 경로 추가 (예: 상위 폴더에 코드가 있는 경우)
sys.path.insert(0, os.path.abspath(".."))

project = "mdfix"
copyright = "2025, rwiv"
author = "rwiv"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # Docstring 자동화
    "sphinx.ext.napoleon",  # Google/NumPy 스타일 지원
    "sphinx_markdown_builder",
]

# Napoleon 설정 (Google 스타일)
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# Markdown 파일 확장자 지원
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
