# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import supriya_midi

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "supriya-midi"
copyright = "2026-, Josephine Wolf Oberholtzer"
author = "Joséphine Wolf Oberholtzer"
version = release = supriya_midi.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

add_module_names = False
exclude_patterns = []
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_immaterial",
]
templates_path = ["_templates"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_favicon = "favicon.ico"
html_logo = "icon.svg"
html_static_path = ["_static"]
html_theme = "sphinx_immaterial"
html_theme_options = {
    "globaltoc_collapse": False,
    "icon": {"repo": "fontawesome/brands/github"},
    "features": [
        "content.action.view",
        "content.tabs.link",
        "content.tooltips",
        "navigation.footer",
        # "navigation.tabs",
        "navigation.top",
        "toc.follow",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "blue-grey",
            "accent": "lime",
            "toggle": {
                "icon": "material/toggle-switch",
                "name": "Switch to light mode",
            },
        },
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "indigo",
            "accent": "teal",
            "toggle": {
                "icon": "material/toggle-switch-off-outline",
                "name": "Switch to dark mode",
            },
        },
    ],
    "repo_name": "supriya-midi",
    "repo_url": "https://github.com/supriya-project/supriya-midi/",
    "site_url": "https://supriya-project.github.io/supriya-midi/",
    "version_dropdown": False,
}
html_title = "Supriya MIDI"
object_description_options = [
    ("py:.*", dict(include_fields_in_toc=False)),  # Hide "Parameters" in TOC
    ("py:exception", {"toc_icon_class": "data", "toc_icon_text": "X"}),
    ("py:parameter", dict(include_in_toc=False)),  # Hide "p" parameter entries in TOC
]
