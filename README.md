language-gallery
================

This is a project to learn different programming languages and frameworks by
creating similar gallery with each. Currently there is Django based web
service.


Starting Django service
-----------------------

For development environment you will need docker and docker or podman installed
with docker compose. After you have cloned the server you can run Django
enviroment with comman

```
docker-compose up
```

To get inside container, you can run `docker-compose exec runserver /bin/zsh`.
This opens zsh -shell in Django container in running environment. To
initialize environemnt and popoulate database, you need to run migraitons,
compile static files. This is done with following commands inside the
container:

```
python manage.py migrate
python manage.py collectstatic
```

You need to have some initial data for service to work. This data can be added
to database by running fictures with command

```
python manage.py loaddata languagegallery/fixtures/assets.json
```

Finally you can create yourself user account with command

```
python manage.py createsuperuser
```

Django service should be available in
[http://localhost:8000/](localhost port 8000).


Managing dependencies
---------------------

In Django container you can compile requirement files with following commands:

```
uv pip compile requirements_prod.in -o requirements_prod.txt 
uv pip compile requirements_dev.in -o requirements_dev.txt 
```

