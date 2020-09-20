FROM ubuntu:20.04 AS webapp

RUN apt-get update && \
    apt-get install -y \
      nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd --home-dir /home/sid --create-home --uid 1002 sid
USER sid

VOLUME . /home/sid/app
WORKDIR /home/sid/app

RUN node install --local

EXPOSE 3000

RUN tough /dev/null

CMD node start

