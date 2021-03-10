FROM python:3.8-alpine AS runserver

RUN apk update && \
    apk add sudo bash zsh \
        gcc postgresql-dev python3-dev musl-dev jpeg-dev zlib-dev

RUN adduser -h /home/sid -D sid
RUN mkdir /home/sid/upload /home/sid/cache /home/sid/brython && \
    chown sid.sid /home/sid/upload /home/sid/cache /home/sid/brython && \
    chmod 755 /home/sid/upload /home/sid/cache /home/sid/brython

USER sid

ADD . /home/sid/app
VOLUME ["/home/sid/app"]

WORKDIR /home/sid/app
RUN python3.8 -m venv ~/venv
RUN ~/venv/bin/pip install --upgrade pip wheel brython
RUN ~/venv/bin/pip install -r requirements.txt

WORKDIR /home/sid/brython
RUN ~/venv/bin/brython-cli --install

EXPOSE 8000/tcp

WORKDIR /home/sid/app
CMD ~/venv/bin/python manage.py runserver 0.0.0.0:8000

