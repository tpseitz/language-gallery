FROM node:14-alpine AS webapp

RUN apk update && \
    apk add sudo bash zsh \
        yarn

ADD . /home/node/app
VOLUME /home/node/app

USER node

WORKDIR /home/node/app

CMD npm start
