#!/bin/bash

echo 'python tools'
apt-get install -y python3-pip python-dev sqlite3
echo 'necessary for bcrypt'
apt-get install -y libffi-dev

echo 'pip'
pip3 install -r ../deps
echo 'dev tools'
apt-get install -y ack-grep
