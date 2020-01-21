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
import logging
from flask.logging import default_handler
from @{PACKAGE_NAME}.flask import app, db
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

        # DB Model imports

        with app.app_context():
            db.create_all()

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
