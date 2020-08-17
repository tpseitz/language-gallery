FROM python:3.8 AS runserver

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client zsh \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --home-dir /home/sid --create-home --uid 1001 sid

USER sid
COPY . /home/sid/app
WORKDIR /home/sid/app

RUN python3.8 -m venv ~/.venv \
  && . ~/.venv/bin/activate \
  && pip install -r requirements.txt

EXPOSE 8000

CMD . ~/.venv/bin/activate \
  && python manage.py runserver 0.0.0.0:8000

