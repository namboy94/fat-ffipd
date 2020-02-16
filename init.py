"""LICENSE
Copyright 2020 Hermann Krumrey <hermann@krumreyh.com>

This file is part of fat-ffipd.

fat-ffipd is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

fat-ffipd is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with fat-ffipd.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
import argparse
from shutil import copytree, rmtree


def main():
    """
    Initializes a new project directory and replaces fat-ffipd specific
    content with the new information
    :return: None
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="The name of the project")
    parser.add_argument("project_short_description",
                        help="A short description of the project")
    parser.add_argument("project_url",
                        help="The URL to the project's page (i.e. gitlab")
    parser.add_argument("author_name", help="The name of the author")
    parser.add_argument("author_email", help="The email addres of the author")
    parser.add_argument("copyright_year",
                        help="The year to specify in the copyright notices")
    parser.add_argument("github_user",
                        help="The github user used for mirroring")
    parser.add_argument("domain",
                        help="The domain on which the website will run")
    args = parser.parse_args()

    temp_path = "/tmp/" + args.project_name
    target_path = args.project_name

    for path in [temp_path, target_path]:
        if os.path.isdir(path):
            rmtree(path)

    copytree(".", temp_path)
    copytree(temp_path, target_path)
    rmtree(temp_path)
    rmtree(os.path.join(target_path, ".git"))

    copyright_notice = "Copyright {} {} <{}>".format(
        args.copyright_year, args.author_name, args.author_email
    )
    project_name = args.project_name
    package_name = project_name.replace("-", "_")

    for key, value in [
        ("Copyright 2020 Hermann Krumrey <hermann@krumreyh.com>",
         copyright_notice),
        ("Hermann Krumrey", args.author_name),
        ("hermann@krumreyh.com", args.author_email),
        ("https://gitlab.namibsun.net/namibsun/python/fat-ffipd",
         args.project_url),
        ("fat-ffipd.namibsun.net", args.domain),
        ("github.com:namboy94", "github.com:" + args.github_user),
        ("github.com/namboy94", "github.com/" + args.github_user),
        ("fat_ffipd", package_name),
        ("fat-ffipd", project_name),
        ("Flask Application Template - For Fast Initial Project Development",
         args.project_short_description),
        ("\"Flask Application Template - \"\n"
         "                    \"For Fast Initial Project Develoment\"",
         "\"" + args.project_short_description + "\""),
    ]:
        replace_occurences(target_path, key, value)

    env_file = os.path.join(target_path, ".env")
    changelog_file = os.path.join(target_path, "CHANGELOG")
    version_file = os.path.join(target_path, "version")
    with open(env_file, "w") as f:
        f.write("MYSQL_ROOT_PASSWORD=\n"
                "MYSQL_USER=\n"
                "MYSQL_PASSWORD=\n"
                "MYSQL_DATABASE=\n"
                "MYSQL_SECRET=\n"
                "RECAPTCHA_SECRET_KEY=\n"
                "RECAPTCHA_SITE_KEY=\n"
                "SMTP_ADDRESS=\n"
                "SMTP_PASSWORD=\n"
                "SMTP_HOST=\n"
                "SMTP_PORT=\n".format())
    with open(changelog_file, "w") as f:
        f.write("V 0.0.1:\n  - Project start")
    with open(version_file, "w") as f:
        f.write("0.0.1")
    os.remove(os.path.join(target_path, "init.py"))
    readme_file = os.path.join(target_path, "README.md")
    with open(readme_file, "r") as f:
        readme_lines = f.read().split("\n")

    readme_content = readme_lines[0:10] \
        + [readme_lines[18]] \
        + readme_lines[24:]
    with open(readme_file, "w") as f:
        f.write("\n".join(readme_content))


def replace_occurences(root: str, keyword: str, value: str):
    """
    Replaces any occurrences of a string with another string
    :param root: The directory to traverse
    :param keyword: The keyword to replace
    :param value: The value with which to replace the keyword
    :return: None
    """
    for element in os.listdir(root):
        path = os.path.join(root, element)

        new_name = element.replace(keyword, value)
        new_path = os.path.join(root, new_name)
        os.rename(path, new_path)
        path = new_path

        if os.path.isdir(path):
            replace_occurences(path, keyword, value)

        elif os.path.isfile(path):
            with open(path, "r") as f:
                try:
                    content = f.read()
                except UnicodeDecodeError:
                    continue

            with open(path, "w") as f:
                replaced = content.replace(keyword, value)
                f.write(replaced)


if __name__ == "__main__":
    main()
