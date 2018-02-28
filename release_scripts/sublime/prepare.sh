#!/bin/bash

# Given a destination, this script builds the sublime plugin for distribution
# at the destination. The destination supplied should be a local copy of the
# plugin repository.

SCRIPT_PATH=$( cd $(dirname $0) ; pwd -P )

cd $SCRIPT_PATH
MASTER_HASH=$( git rev-parse master )
HASH=$( git rev-parse HEAD )

if [[ $MASTER_HASH != $HASH ]]; then
  echo "ERROR: You must be on master when preparing a release."
  exit 1
fi

if [[ "$1" == "" ]]; then
  echo "ERROR: Please supply a path to the plugin target destination."
  exit 1
fi

INSTALL_PATH="$1"

# Make sure the path is up-to-date
cd $INSTALL_PATH
git checkout master
git pull origin master
cd $SCRIPT_PATH

# Clean existing items in plugin path
rm -rf $INSTALL_PATH/agent
rm -rf $INSTALL_PATH/crdt
rm -rf $INSTALL_PATH/enum-dist
rm -f $INSTALL_PATH/*

# Create agent and crdt subdirectories
mkdir $INSTALL_PATH/agent/
mkdir $INSTALL_PATH/crdt/

# Agent
$(
  cd $SCRIPT_PATH/../../agent/;
  rm -f **/*.pyc
)
cp -r $SCRIPT_PATH/../../agent/ $INSTALL_PATH/agent/

# CRDT
$(
  cd $SCRIPT_PATH/../../crdt/;
  npm run clean;
  rm -rf node_modules;
  npm install;
  npm run build
)
cp -r $SCRIPT_PATH/../../crdt/build/ $INSTALL_PATH/crdt/build/

# Sublime specific files
cd $SCRIPT_PATH/../../plugins/sublime/
cp -r enum-dist/ $INSTALL_PATH/enum-dist/
cp *.py $INSTALL_PATH
cp *.sublime-* $INSTALL_PATH
cp README.md $INSTALL_PATH

# Required by Package Control
touch $INSTALL_PATH/.no-sublime-package

echo "Release succesfully prepared."
