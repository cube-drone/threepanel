#!/bin/bash

nohup uwsgi --chdir=${home}/vagrant_django/${project_slug}/ \
            --module=threepanel.wsgi:application \
            --env DJANGO_SETTINGS_MODULE=threepanel.settings \
            --master --socket=/tmp/threepanel.sock \
            --home=${home}/django_environment \
            --chmod-socket=666 \
            --processes=4 \
            --die-on-term \
            --harakiri=60 \
            --max-requests=5000 \
            --pidfile=${home}/uwsgi.pid \
            --vacuum > ${home}/logs/uwsgi.log 2>&1 &