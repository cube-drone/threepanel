#!/bin/bash

nohup uwsgi --chdir=${HOME}/vagrant_django/${DJANGO_PROJECT_SLUG}/ \
            --module=${DJANGO_PROJECT_SLUG}.wsgi:application \
            --env DJANGO_SETTINGS_MODULE=${DJANGO_PROJECT_SLUG}.settings \
            --master --socket=/tmp/${DJANGO_PROJECT_SLUG}.sock \
            --home=${HOME}/django_environment \
            --chmod-socket=666 \
            --processes=4 \
            --die-on-term \
            --harakiri=60 \
            --max-requests=5000 \
            --pidfile=${HOME}/uwsgi.pid \
            --vacuum > ${HOME}/logs/uwsgi.log 2>&1 &
