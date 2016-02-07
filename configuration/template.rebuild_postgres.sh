#!/bin/bash

mkdir ${home}/db_backups
sudo -u postgres psql -d ${project_slug} -f ${db_password}
