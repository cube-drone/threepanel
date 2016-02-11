#!/bin/bash

nohup celery worker --app=${project_slug} \
             --loglevel=info \
             --beat \
             --pidfile=${home}/celery.pid \
             --logfile=${home}/logs/celery.log 2>&1 &
