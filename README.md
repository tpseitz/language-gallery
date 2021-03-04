language-gallery
================

This is a project to learn different programming languages and frameworks by
creating similar gallery with each. Currently there is Django based web server
and React skeleton for future.


Starting service
----------------

For development environment you will need docker and docker or podman installed
with docker compose. After you have cloned the server you can start it with
following steps.

- Run docker compose

  `docker-compose up`

- Execute shell in running Django container

  `docker-compose exec runserver /bin/bash`

- Run init script in container

  `init_django.sh`

- Activate Python venu

  `. ~/venv/bin/activate`

- Create superuser

  `python manage.py createsuperuser`

After this server is available in address http://localhost:8000/ and React is
accessible with address http://localhost:3000/

