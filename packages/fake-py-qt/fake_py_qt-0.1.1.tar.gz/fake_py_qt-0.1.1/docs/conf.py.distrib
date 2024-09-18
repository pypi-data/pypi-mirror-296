# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

try:
    import fake_py_qt

    version = fake_py_qt.__version__
    project = fake_py_qt.__title__
    copyright = fake_py_qt.__copyright__
    author = fake_py_qt.__author__
except ImportError:
    version = "0.1"
    project = "fake-py-qt"
    copyright = "2024, Artur Barseghyan <artur.barseghyan@gmail.com>"
    author = "Artur Barseghyan <artur.barseghyan@gmail.com>"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx_no_pragma",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "en"

release = version

# The suffix of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
}

pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
# html_extra_path = ["examples"]

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True

# -- Options for Epub output  ----------------------------------------------
epub_title = project
epub_author = author
epub_publisher = "GitHub"
epub_copyright = copyright
epub_identifier = "https://github.com/barseghyanartur/fake-py-qt"  # URL or ISBN
epub_scheme = "URL"  # or "ISBN"
epub_uid = "https://github.com/barseghyanartur/fake-py-qt"
