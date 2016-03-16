#!/bin/bash

remote_syslog --dest-host="${PAPERTRAIL_HOST}" \
        --dest-port=${PAPERTRAIL_PORT} \
        --pid-file=${HOME}/remote_syslog.pid \
        ${HOME}/logs/celery.log
