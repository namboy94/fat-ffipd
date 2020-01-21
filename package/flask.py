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
import pkg_resources
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from @{PACKAGE_NAME}.routes.static import static_blueprint
from @{PACKAGE_NAME}.routes.api.ping import api_ping_blueprint

app = Flask(__name__)
"""
The Flask App
"""

db = SQLAlchemy()
"""
The SQLAlchemy database connection
"""

login_manager = LoginManager(app)
"""
The Flask-Login Login Manager
"""

def configure():

    app.config["TRAP_HTTP_EXCEPTIONS"] = True
    login_manager.session_protection = "strong"


    if "FLASK_TESTING" in os.environ:
        app.testing = os.environ["FLASK_TESTING"] == "1"

    @app.context_processor
    def inject_template_variables():
        """
        Injects the project's version string so that it will be available
        in templates
        :return: The dictionary to inject
        """
        version = \
            pkg_resources.get_distribution("@{PACKAGE_NAME}").version
        return {
            "version": version,
            "env": app.env
        }

    app.register_blueprint(static_blueprint)
    app.register_blueprint(api_ping_blueprint)


configure()
