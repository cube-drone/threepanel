#!/bin/bash

mkdir -p ${HOME}/db_backups
sudo -u postgres psql -d ${DJANGO_PROJECT_SLUG} -f ${POSTGRES_DB_PASSWORD}
