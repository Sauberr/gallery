#!/bin/bash

python src/manage.py migrate
python src/manage.py collectstatic --noinput

gunicorn -w ${WSGI_WORKERS} -b 0:${WSGI_PORT} --chdir ./test_assignment config.wsgi:application --log-level=${WSGI_LOG_LEVEL}