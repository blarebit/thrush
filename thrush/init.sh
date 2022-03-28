#!/bin/bash
if [ "$1" == "--with-delay" ]; then
    sleep 10  # Useful for docker-compose.
fi
python manage.py migrate --database=production
python manage.py collectstatic --noinput
python manage.py loaddata tests/fixtures/sample.json --database=production
gunicorn aap.wsgi -b 0.0.0.0:8000

