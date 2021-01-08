language-gallery
================

This is a project to learn different programming languages and frameworks by
creating similar gallery with each.

Starting service
----------------

Go to docker container `docker-compose exec runserver sh` and do following steps

1. Activate Python venv `. ~/venv/bin/activate`
2. Run Django migrations `python manage.py migrate`
3. Create static files `python manage.py collectstatic --no-input`
4. Load initial data `python manage.py loaddata languagegallery/fixtures/assets.json`
5. Create superuser `python manage.py createsuperuser --username=sid --email=sid@example.com`

