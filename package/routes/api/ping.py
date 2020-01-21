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

from flask import Blueprint
from flask_login import login_required
from @{PACKAGE_NAME}.utils.decorators import api, api_login_required

api_ping_blueprint = Blueprint("api_ping", __name__)


@api_ping_blueprint.route("/api/v1/ping")
@api
def ping():
    return {"ANSWER": "PONG"}


@api_ping_blueprint.route("/api/v1/auth_ping")
@api_login_required
@login_required
@api
def auth_ping():
    return "AuthPong"
