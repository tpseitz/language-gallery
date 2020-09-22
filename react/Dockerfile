FROM ubuntu:20.04 AS webapp

RUN apt-get update && \
    apt-get install -y \
      nodejs npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd --home-dir /home/sid --create-home --uid 1002 sid
USER sid

ADD . /home/sid/app
VOLUME ["/home/sid/app"]
WORKDIR /home/sid/app

RUN npm install --local

EXPOSE 3000

RUN tough /dev/null

CMD node start

