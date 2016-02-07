#!/bin/bash

echo "Creating Database"
sudo -u postgres createdb '${project_slug}';
echo "Creating User"
sudo -u postgres psql --command "CREATE USER ${project_slug} WITH password '${db_password}';"
sudo -u postgres psql --command "ALTER USER ${project_slug} WITH password '${db_password}';"
echo "Granting Privileges to User"
sudo -u postgres psql --command "GRANT ALL PRIVILEGES ON DATABASE ${project_slug} TO ${project_slug};"
sudo -u postgres psql --command "ALTER USER ${project_slug} CREATEDB;"
