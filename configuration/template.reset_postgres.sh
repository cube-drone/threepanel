#!/bin/bash

sudo -u postgres dropdb ${project_slug}
sudo -u postgres createdb ${project_slug}
sudo -u postgres psql --command "GRANT ALL PRIVILEGES ON DATABASE ${project_slug} TO ${project_slug};"
