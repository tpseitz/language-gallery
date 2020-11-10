FROM python:3.8-alpine AS runserver

RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev

RUN adduser -h /home/sid -D sid
USER sid

ADD . /home/sid/app
VOLUME ["/home/sid/app"]
WORKDIR /home/sid/app

RUN python3.8 -m venv ~/venv
RUN ~/venv/bin/pip install --upgrade pip wheel
RUN ~/venv/bin/pip install -r requirements.txt

EXPOSE 8000/tcp

CMD ~/venv/bin/python manage.py runserver 0.0.0.0:8000

