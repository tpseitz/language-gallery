#!/bin/bash
. ~/venv/bin/activate
python manage.py migrate
python manage.py collectstatic --no-input
if [ -n "$FIXTURES" ]; then
  python manage.py loaddata $FIXTURES
fi

