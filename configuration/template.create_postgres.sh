#!/bin/bash

echo "Creating Database"
sudo -u postgres createdb '${DJANGO_PROJECT_SLUG}';
echo "Creating User"
sudo -u postgres psql --command "CREATE USER ${DJANGO_PROJECT_SLUG} WITH password '${POSTGRES_DB_PASSWORD}';"
sudo -u postgres psql --command "ALTER USER ${DJANGO_PROJECT_SLUG} WITH password '${POSTGRES_DB_PASSWORD}';"
echo "Granting Privileges to User"
sudo -u postgres psql --command "GRANT ALL PRIVILEGES ON DATABASE ${DJANGO_PROJECT_SLUG} TO ${DJANGO_PROJECT_SLUG};"
sudo -u postgres psql --command "ALTER USER ${DJANGO_PROJECT_SLUG} CREATEDB;"
