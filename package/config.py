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
from @{PACKAGE_NAME}.utils.env import resolve_env_variable

"""
This file contains environment specific configuration information
All of this information is found using environment variables
"""

recaptcha_site_key = resolve_env_variable("RECAPTCHA_SITE_KEY")
"""
The (public) recaptcha site key
"""

recaptcha_secret_key = resolve_env_variable("RECAPTCHA_SECRET_KEY")
"""
The secret recaptcha key used to validate the recaptcha result
"""

db_user = resolve_env_variable("DB_USER")
"""
The database user
"""

db_name = resolve_env_variable("DB_NAME")
"""
The database name
"""

db_key = resolve_env_variable("DB_KEY")
"""
The database key
"""

logging_path = os.path.join(
    str(resolve_env_variable("PROJECT_ROOT_PATH", default="/tmp")),
    "@{PACKAGE_NAME}.log"
)
