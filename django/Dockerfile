FROM ubuntu:20.04 AS runserver

RUN apt-get update && \
    apt-get install -y \
       python3.8 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd --home-dir /home/sid --create-home --uid 1002 sid
USER sid

VOLUME . /home/sid/app
WORKDIR /home/sid/app

RUN df -hT

RUN ls -lh

RUN python3.8 -m venv ~/.venv
RUN ~/.venv/bin/pip install -r requirements.txt

EXPOSE 8000

#CMD . ~/.venv/bin/activate && \
#  python manage.py runserver 0.0.0.0:8000

