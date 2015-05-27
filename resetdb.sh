#!/bin/bash

sudo -u postgres pg_dump threepanel > `date +"%s"`.db_backup
sudo -u postgres dropdb threepanel
sudo -u postgres createdb threepanel
sudo -u postgres psql --command "ALTER USER threepanel WITH password 'threepass';"
sudo -u postgres psql --command "GRANT ALL PRIVILEGES ON DATABASE threepanel TO threepanel;"
