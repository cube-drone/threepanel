#!/bin/bash

mkdir ${home}/db_backups
sudo -u postgres pg_dump ${project_slug} > ${home}/db_backups/`date +"%Y-%m-%d-%s"`.db_backup
