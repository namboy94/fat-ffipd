#!/usr/bin/env python3
"""LICENSE
Copyright @{COPYRIGHT_YEAR} @{AUTHOR_NAME} <@{AUTHOR_EMAIL}>

This file is part of @{PROJECT_NAME}.

@{PROJECT_NAME} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

@{PROJECT_NAME} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with @{PROJECT_NAME}.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

# noinspection PyPackageRequirements
import sphinx_rtd_theme
# noinspection PyPackageRequirements
from sphinx.ext.autodoc import between

# noinspection PyShadowingBuiltins
copyright = '@{COPYRIGHT_YEAR} @{AUTHOR_NAME}'
author = '@{AUTHOR_NAME}'
project = '@{PROJECT_NAME}'

extensions = ["sphinx.ext.autodoc"]
master_doc = "index"

with open("../../../version", "r") as version_file:
    version = version_file.read()
    release = version

# HTML Theme Config
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


def setup(app):
    """
    Registers an autodoc between listener to ignore License texts

    :param app: The sphinx app
    :return:    None
    """
    app.connect('autodoc-process-docstring',
                between('^.*LICENSE.*$', exclude=True))
    app.connect("autodoc-skip-member",
                lambda a, b, name, d, skipper, f:
                False if name == "__init__" else skipper)
    return app
