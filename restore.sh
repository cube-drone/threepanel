#!/bin/bash

DEPLOY_BRANCH=continuous
VAGRANT_HOSTNAME=`date +%s`-`python threepanel/random_name.py`
DEPLOY_REPO=$VAGRANT_HOSTNAME

mkdir -p deploys
pushd deploys
git clone https://github.com/classam/threepanel.git $DEPLOY_REPO
ln -sf $DEPLOY_REPO next
pushd $DEPLOY_REPO
git checkout $DEPLOY_BRANCH
git pull

pyvenv ./threepenv
source threepenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

invoke install --production --name=$VAGRANT_HOSTNAME --db=/tmp/last.db_backup --media=/tmp/last_media

popd
popd
