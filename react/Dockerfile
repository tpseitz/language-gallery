FROM node:14-alpine AS webapp

#RUN useradd --home-dir /home/sid --create-home --uid 1002 sid
RUN adduser -h /home/sid -u 1002 -D sid
USER sid

ADD . /home/sid/app
VOLUME --chown=1002 /home/sid/app
VOLUME /home/sid/app/node_modules
WORKDIR /home/sid/app

EXPOSE 3000/tcp

CMD npm install && \
    npm start

