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
import pkg_resources
from typing import Optional


class Config:
    """
    Class that stores configuration data
    """

    @property
    def version(self) -> str:
        """
        :return: The version of the program
        """
        return pkg_resources.get_distribution("fat_ffipd").version

    @property
    def recaptcha_site_key(self) -> Optional[str]:
        """
        :return: The (public) recaptcha site key
        """
        return os.environ.get("RECAPTCHA_SITE_KEY")

    @property
    def recaptcha_secret_key(self) -> Optional[str]:
        """
        :return: The secret recaptcha key used to validate the recaptcha result
        """
        return os.environ.get("RECAPTCHA_SECRET_KEY")

    @property
    def db_uri(self) -> str:
        """
        :return: The database URI to use in this application
        """
        db_mode = os.environ.get("DB_MODE", "sqlite")

        if os.environ.get("FLASK_TESTING") or os.environ.get("TESTING"):
            db_mode = "sqlite"

        if db_mode == "sqlite":
            return "sqlite:////tmp/fat_ffipd.db"
        else:
            prefix = db_mode.upper()

            default_port = 3306

            return "{}://{}:{}@{}:{}/{}".format(
                db_mode,
                os.environ[prefix + "_USER"],
                os.environ[prefix + "_PASSWORD"],
                os.environ.get(prefix + "_HOST", "localhost"),
                os.environ.get(prefix + "_PORT", default_port),
                os.environ[prefix + "_DATABASE"],
            )

    @property
    def smtp_host(self) -> str:
        """
        :return: The SMTP host used for outbound emails
        """
        return os.environ["SMTP_HOST"]

    @property
    def smtp_port(self) -> int:
        """
        :return: The SMTP host used for outbound emails
        """
        return int(os.environ["SMTP_PORT"])

    @property
    def smtp_address(self) -> str:
        """
        :return: The SMTP host used for outbound emails
        """
        return os.environ["SMTP_ADDRESS"]

    @property
    def smtp_password(self) -> str:
        """
        :return: The SMTP host used for outbound emails
        """
        return os.environ["SMTP_PASSWORD"]

    @property
    def logging_path(self) -> str:
        """
        :return: The file in which to store logging data
        """
        return os.path.join(
            os.environ.get("LOGGING_PATH", default="/tmp"),
            "fat_ffipd.log"
        )

    MIN_USERNAME_LENGTH = 1
    """
    The minimum length of a username
    """

    MAX_USERNAME_LENGTH = 12
    """
    The maximum length of a username
    """
