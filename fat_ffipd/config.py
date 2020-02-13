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
from fat_ffipd.utils.env import resolve_env_variable

"""
This file contains environment specific configuration information
All of this information is found using environment variables
"""

recaptcha_site_key = resolve_env_variable("RECAPTCHA_SITE_KEY", nullable=True)
"""
The (public) recaptcha site key
"""

recaptcha_secret_key = resolve_env_variable("RECAPTCHA_SECRET_KEY",
                                            nullable=True)
"""
The secret recaptcha key used to validate the recaptcha result
"""

db_mode = resolve_env_variable("DB_MODE", default="sqlite")
"""
The database mode to use. Currently, options are mysql and sqlite
"""

db_host = resolve_env_variable("DB_HOST", default="localost")
"""
The database host
"""

db_port = resolve_env_variable("DB_PORT", _type=int, default=3306)
"""
The database port
"""

db_user = resolve_env_variable("DB_USER", nullable=True)
"""
The database user
"""

db_name = resolve_env_variable("DB_NAME", nullable=True)
"""
The database name
"""

db_key = resolve_env_variable("DB_KEY", nullable=True)
"""
The database key
"""

logging_path = os.path.join(
    str(resolve_env_variable("PROJECT_ROOT_PATH", default="/tmp")),
    "fat_ffipd.log"
)
