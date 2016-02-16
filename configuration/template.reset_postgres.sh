#!/bin/bash

sudo -u postgres dropdb ${DJANGO_PROJECT_SLUG}
sudo -u postgres createdb ${DJANGO_PROJECT_SLUG}
sudo -u postgres psql --command "GRANT ALL PRIVILEGES ON DATABASE ${DJANGO_PROJECT_SLUG} TO ${DJANGO_PROJECT_SLUG};"
