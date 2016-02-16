#!/bin/bash

mkdir ${HOME}/db_backups
sudo -u postgres pg_dump ${DJANGO_PROJECT_SLUG} > ${HOME}/db_backups/`date +"%Y-%m-%d-%s"`.db_backup
