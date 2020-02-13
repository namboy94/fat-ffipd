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
import base64
import logging
from binascii import Error
from typing import Optional
from flask import render_template
from flask.logging import default_handler
from werkzeug.exceptions import HTTPException
from @{PACKAGE_NAME}.db.auth.User import User
from @{PACKAGE_NAME}.db.auth.ApiKey import ApiKey
from @{PACKAGE_NAME}.db.models import create_tables
from @{PACKAGE_NAME}.flask import app, db, login_manager
from @{PACKAGE_NAME}.routes.blueprints import register_blueprints
from @{PACKAGE_NAME}.config import logging_path, db_user, db_key, db_name


@app.before_first_request
def init():
    if not app.testing:  # pragma: no cover

        app.secret_key = os.environ["FLASK_SECRET"]

        if app.config["ENV"] == "production":
            uri = "mysql://{}:{}@localhost:3306/{}".format(
                db_user, db_key, db_name
            )
        else:
            uri = "sqlite:////tmp/@{PACKAGE_NAME}.db"

        app.config["SQLALCHEMY_DATABASE_URI"] = uri
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)

        register_blueprints(app)
        create_tables(app, db)

        # Set up login manager
        @login_manager.user_loader
        def load_user(user_id: str) -> Optional[User]:
            """
            Loads a user from an ID
            :param user_id: The ID
            :return: The User
            """
            return User.query.get(int(user_id))

        @login_manager.request_loader
        def load_user_from_request(request) -> Optional[User]:
            """
            Loads a user pased on a provided API key
            :param request: The request containing the API key in the headers
            :return: The user or None if no valid API key was provided
            """
            if "Authorization" not in request.headers:
                return None

            api_key = request.headers["Authorization"].replace("Basic ", "", 1)

            try:
                api_key = base64.b64decode(
                    api_key.encode("utf-8")
                ).decode("utf-8")
            except (TypeError, Error):
                pass

            db_api_key = ApiKey.query.get(api_key.split(":", 1)[0])

            # Check for validity of API key
            if db_api_key is None or not db_api_key.verify_key(api_key):
                return None

            elif db_api_key.has_expired():
                db.session.delete(db_api_key)
                db.session.commit()
                return None

            return User.query.get(db_api_key.user_id)

        @app.errorhandler(HTTPException)
        def error_handling(error: HTTPException):
            """
            Custom redirect for 401 errors
            :param error: The error that caused the error handler to be called
            :return: A redirect to the login page
            """
            return render_template("error.html", error=error)

        app.logger.removeHandler(default_handler)

        logging.basicConfig(
            filename=logging_path,
            level=logging.DEBUG,
            format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        )

        app.logger.error("STARTING FLASK")
        app.logger.warning("STARTING FLASK")
        app.logger.info("STARTING FLASK")
        app.logger.debug("STARTING FLASK")
