#!/bin/bash

export VIRTUALENV=$HOME/django_environment
echo "Home: $HOME"
echo "Virtualenv: $VIRTUALENV"

sudo apt-get -y update

echo 'Install Dev Tools'
sudo apt-get install -y ack-grep vim dos2unix git

echo 'Install Build Tools'
sudo apt-get install -y build-essential gcc

echo "Install Redis"
sudo apt-get install -y redis-server

echo "Install PostgreSQL"
sudo apt-get install -y postgresql postgresql-contrib libpq-dev

echo "Install NGINX"
sudo apt-get install -y nginx

echo "Install Python"
sudo apt-get install -y python3 python3-dev python3-venv

echo "Create a Virtual Environment, Install Pip & Python Dependencies"
mkdir $VIRTUALENV
pyvenv $VIRTUALENV
source $VIRTUALENV/bin/activate && pip install -r $HOME/vagrant_django/configuration/requirements.txt

sudo rm /etc/nginx/sites-enabled/default

mkdir -p $HOME/logs
mkdir -p $HOME/vagrant_django/scripts
