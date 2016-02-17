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

echo "Install fail2ban"
sudo apt-get install -y fail2ban

echo "Create a Virtual Environment, Install Pip & Python Dependencies"
mkdir $VIRTUALENV
pyvenv $VIRTUALENV
source $VIRTUALENV/bin/activate && pip install -r $HOME/vagrant_django/configuration/requirements.txt

echo "Removing default nginx page"
sudo rm /etc/nginx/sites-enabled/default

echo "Install remote_syslog2"
pushd /tmp
wget https://github.com/papertrail/remote_syslog2/releases/download/v0.17-beta-pkgs/remote-syslog2_0.17_amd64.deb
dpkg -i remote-syslog2_0.17_amd64.deb
popd

mkdir -p $HOME/logs
mkdir -p $HOME/vagrant_django/scripts
