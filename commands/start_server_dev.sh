#!/bin/sh

python src/manage.py migrate
python src/manage.py loaddata fixtures/users.json
python src/manage.py loaddata fixtures/subscriptions.json
python src/manage.py loaddata fixtures/usersubscription.json
python src/manage.py loaddata fixtures/images.json
python src/manage.py runserver 0:8000