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

import cherrypy
from fat_ffipd.run import app, init
from fat_ffipd.bg_tasks import bg_tasks

if __name__ == '__main__':

    init()
    for task in bg_tasks.values():
        task.start()

    cherrypy.tree.graft(app, "/")

    cherrypy.server.unsubscribe()

    # noinspection PyProtectedMember
    server = cherrypy._cpserver.Server()

    server.socket_host = "0.0.0.0"
    server.socket_port = 8000
    server.thread_pool = 30

    server.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()
