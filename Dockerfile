FROM ubuntu:18.04
MAINTAINER Hermann Krumrey <hermann@krumreyh.com>

ENV DEBIAN_FRONTEND=noninteractive

EXPOSE 80

ADD ./ flask-app
RUN apt update && \
    apt install -y python3 python3-pip && \
    pip3 install Flask cherrypy && \
    cd flask-app && \
    python3 setup.py install

WORKDIR flask-app

CMD ["/usr/bin/python3", "server.py"]
