FROM node:14-alpine AS webapp

RUN adduser -h /home/sid -D sid
USER sid

ADD . /home/sid/app
VOLUME /home/sid/app

WORKDIR /home/sid/app

ENTRYPOINT ["/usr/local/bin/npm"]
