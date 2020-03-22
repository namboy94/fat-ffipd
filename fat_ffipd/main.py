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
from typing import List
from flask.blueprints import Blueprint
from puffotter.flask.base import db
from puffotter.flask.Config import Config
from puffotter.flask.initialize import init_flask
from puffotter.flask.wsgi import start_server
from fat_ffipd import sentry_dsn
from fat_ffipd.bg_tasks import bg_tasks

blueprints: List[Blueprint] = []
"""
The route blueprints of the application
"""

models: List[db.Model] = []
"""
The database models of the application
"""

root_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)))
"""
The root path of the application
"""


def main():
    """
    Starts the flask application
    :return: None
    """
    init_flask(
        "fat_ffipd",
        sentry_dsn,
        root_path,
        Config,
        models,
        blueprints
    )
    start_server(Config, bg_tasks)
