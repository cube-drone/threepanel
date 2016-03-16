#!/bin/bash

export VIRTUALENV=$HOME/django_environment
whoami
echo "Home: $HOME"
echo "Virtualenv: $VIRTUALENV"

sudo apt-get -y update

echo 'Install Dev Tools'
sudo apt-get install -y ack-grep vim dos2unix git

echo 'Install Build Tools'
sudo apt-get install -y build-essential gcc

echo "Install Redis"
sudo apt-get install -y redis-server
echo never > /sys/kernel/mm/transparent_hugepage/enabled

echo "Install PostgreSQL"
sudo apt-get install -y postgresql postgresql-contrib libpq-dev

echo "Install NGINX"
sudo apt-get install -y nginx

echo "Install Python"
sudo apt-get install -y python3 python3-dev python3-venv python3-setuptools

echo "Install Pillow dependencies"
sudo apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev
sudo apt-get install -y liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev

echo "Install IMAGE CROOSHER"
sudo apt-get install -y optipng

echo "Install fail2ban"
sudo apt-get install -y fail2ban

echo "Install rsyslog daemon"
pushd /tmp
wget https://github.com/papertrail/remote_syslog2/releases/download/v0.17-beta-pkgs/remote-syslog2_0.17_i386.deb
sudo dpkg -i remote-syslog2_0.17_i386.deb
popd

echo "Crank up the soft file descriptor cap to the maximum available"
ulimit -n 65536

echo "And the global file descriptor cap. That too"
sudo sysctl -w fs.file-max=800000

echo "Create a Virtual Environment, Install Pip & Python Dependencies"
mkdir $VIRTUALENV
pyvenv $VIRTUALENV
source $VIRTUALENV/bin/activate && pip install -r $HOME/vagrant_django/configuration/requirements.txt

echo "Removing default nginx page"
sudo rm /etc/nginx/sites-enabled/default

mkdir -p $HOME/logs
mkdir -p $HOME/vagrant_django/nginx
mkdir -p $HOME/vagrant_django/nginx/static
mkdir -p $HOME/vagrant_django/nginx/media
mkdir -p $HOME/vagrant_django/nginx/media/upload
mkdir -p $HOME/vagrant_django/scripts
