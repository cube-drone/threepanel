#!/bin/bash

nohup celery worker --app=${DJANGO_PROJECT_SLUG} \
             --loglevel=info \
             --beat \
             --pidfile=${HOME}/celery.pid \
             --concurrency=1 \
             --logfile=${HOME}/logs/celery.log 2>&1 &
