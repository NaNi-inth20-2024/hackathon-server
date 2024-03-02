#!/bin/sh

python manage.py flush --no-input
python manage.py migrate
python manage.py runserver $SERVER_IP:$SERVER_PORT

exec "$@"