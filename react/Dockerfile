FROM node:14 AS webapp

USER sid
VOLUME . /home/sid/app
WORKDIR /home/sid/app

RUN node install --local

EXPOSE 3000

CMD node

