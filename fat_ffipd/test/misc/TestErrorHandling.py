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

from unittest.mock import patch
from fat_ffipd.test.TestFramework import _TestFramework


class TestErrorHandling(_TestFramework):
    """
    Class that tests the flask error handling
    """

    def test_exception(self):
        """
        Tests if unexpected exceptions are caught correctly
        :return: None
        """

        def render_template(*_, **__):
            print(1/0)
        with patch("puffotter.flask.routes.static.render_template",
                   render_template):
            resp = self.client.get("/", follow_redirects=True)
            with open("/tmp/index.html", "wb") as f:
                f.write(resp.data)
            self.assertTrue(b"Error 500" in resp.data)

    def test_404(self):
        """
        Tests if a 404 error is handled correctly
        :return: None
        """
        resp = self.client.get("/baba", follow_redirects=True)
        self.assertTrue(b"Error 404" in resp.data)
