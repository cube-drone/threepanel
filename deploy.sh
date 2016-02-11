#!/bin/bash

DEPLOY_REPO=`date +%s`-threepanel
DEPLOY_BRANCH=continuous

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

invoke install --production

popd
popd

