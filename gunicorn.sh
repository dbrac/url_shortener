#!/bin/bash

echo Migrate database if needed..
python ./manage.py migrate

echo Collect static files if needed..
python ./manage.py collectstatic --noinput

echo Starting Gunicron
exec gunicorn \
  --access-logfile - \
  --bind 0.0.0.0:8000 \
  --error-logfile - \
  --workers 2 \
  --worker-class eventlet \
  --no-sendfile \
  --timeout 60 \
  url_shortener.wsgi:application