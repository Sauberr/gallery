#!/bin/sh

python src/manage.py migrate
python src/manage.py runserver 0:8000