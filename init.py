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

import os
from shutil import copytree


def replace_occurences(root: str, keyword: str, value: str):
    for element in os.listdir(root):
        path = os.path.join(root, element)

        if os.path.isdir(path):
            replace_occurences(path, keyword, value)
        elif os.path.isfile(path):
            with open(path, "r") as f:
                content = f.read()
            with open(path, "w") as f:
                f.write(content.replace("@{" + keyword + "}", value))


def main():
    keywords = [
        "PROJECT_NAME",
        "PROJECT_DESCRIPTION",
        "PROJECT_URL",
        "AUTHOR_NAME",
        "AUTHOR_EMAIL",
        "COPYRIGHT_YEAR",
        "DOMAIN",
        "GITHUB_USER"
    ]
    print("Please enter the project details:")
    project_info = {x: input(x + ": ") for x in keywords}
    copytree(".", "/tmp/" + project_info["PROJECT_NAME"])
    os.rename(
        "/tmp/" + project_info["PROJECT_NAME"],
        project_info["PROJECT_NAME"]
    )

    for keyword, value in project_info.items():
        replace_occurences(project_info["PROJECT_NAME"], keyword, value)


if __name__ == "__main__":
    main()
