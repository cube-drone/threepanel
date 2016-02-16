#!/bin/bash

nohup uwsgi --chdir=${HOME}/vagrant_django/${PROJECT_SLUG}/ \
            --module=${PROJECT_SLUG}.wsgi:application \
            --env DJANGO_SETTINGS_MODULE=${PROJECT_SLUG}.settings \
            --master --socket=/tmp/${PROJECT_SLUG}.sock \
            --home=${HOME}/django_environment \
            --chmod-socket=666 \
            --processes=4 \
            --die-on-term \
            --harakiri=60 \
            --max-requests=5000 \
            --pidfile=${HOME}/uwsgi.pid \
            --vacuum > ${HOME}/logs/uwsgi.log 2>&1 &
