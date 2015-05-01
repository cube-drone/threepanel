#!/bin/bash

sudo apt-get -y update
sudo apt-get -y upgrade

echo 'Dev Tools'
apt-get install -y ack-grep vim

echo 'Shortcuts'
echo "alias dj='python3 /home/vagrant/synced/threepanel/manage.py'" >> /home/vagrant/.bashrc

echo "PostgreSQL"
sudo apt-get install -y postgresql postgresql-contrib libpq-dev
sudo -u postgres createuser --superuser threepanel
sudo -u postgres createdb threepanel
sudo -u postgres psql --command "ALTER USER threepanel WITH password 'threepass';"
sudo -u postgres psql --command "GRANT ALL PRIVILEGES ON DATABASE threepanel TO threepanel;"

echo "Python, PIP, & Python Libraries"
sudo apt-get install -y python3 python3-dev
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo pip install -r /home/vagrant/synced/requirements.txt --upgrade
