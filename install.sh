#!/bin/bash

sudo apt-get -y update
sudo apt-get -y upgrade

echo 'Dev Tools'
sudo apt-get install -y ack-grep vim

echo 'Shortcuts'
echo "alias dj='python3 /home/vagrant/synced/threepanel/manage.py'" >> /home/vagrant/.bashrc
echo "alias in='cd /home/vagrant/synced/ && invoke'" >> /home/vagrant/.bashrc
echo "export PYTHONPATH=/home/vagrant/synced/threepanel" >> /home/vagrant/.bashrc

echo "Redis"
sudo apt-get install -y redis-server
cp /home/vagrant/synced/redis.conf /etc/redis/redis.conf
sudo service redis-server restart

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

echo "Pythonpath"
export PYTHONPATH=/home/vagrant/synced/threepanel
