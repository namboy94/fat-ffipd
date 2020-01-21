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

# imports
from setuptools import setup, find_packages


if __name__ == "__main__":

    setup(
        name="@{PACKAGE_NAME}",
        version=open("version", "r").read(),
        description="@{PROJECT_DESCRIPTION}",
        long_description=open("README.md", "r").read(),
        long_description_content_type="text/markdown",
        classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        ],
        url="@{PROJECT_URL}",
        author="@{AUTHOR_NAME}",
        author_email="@{AUTHOR_EMAIL}",
        license="GNU GPL3",
        packages=find_packages(),
        install_requires=[
            "flask",
            "flask_sqlalchemy",
            "flask_login",
            "puffotter"
        ],
        include_package_data=True,
        zip_safe=False
    )
