FROM node:14-alpine AS webapp

ENV NODE_PATH /home/sid

RUN adduser -h /home/sid -D sid
USER sid

ADD . /home/sid/app
VOLUME /home/sid/app

RUN mkdir /home/sid/node_modules
RUN cp -f /home/sid/app/package.json /home/sid/
WORKDIR /home/sid/node_modules
RUN npm install

WORKDIR /home/sid/app

RUN npm install

CMD npm start

