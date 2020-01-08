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
from @{PACKAGE_NAME}.utils.env import load_secrets


secrets_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "secrets.json"
)
load_secrets(secrets_file)
os.environ["PROJECT_ROOT_PATH"] = os.path.abspath(os.path.dirname(__file__))

from @{PROJECT_NAME}.run import app as application
