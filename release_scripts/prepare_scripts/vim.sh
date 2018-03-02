#!/bin/bash

# Given a destination, this script builds the sublime plugin for distribution
# at the destination. The destination supplied should be a local copy of the
# plugin repository.

if [[ "$1" == "" ]]; then
  echo "ERROR: Please supply a path to the plugin target destination."
  exit 1
fi

SCRIPT_PATH=$( cd $(dirname $0) ; pwd -P )
INSTALL_PATH="$1"

# Make sure the path is up-to-date
cd $INSTALL_PATH
git checkout master
git pull origin master
cd $SCRIPT_PATH

# Clean existing items in plugin path
rm -rf $INSTALL_PATH/plugin
rm -f $INSTALL_PATH/*

# Create plugin, lib, agent and crdt subdirectories
mkdir $INSTALL_PATH/plugin/
mkdir $INSTALL_PATH/plugin/tandem_lib/
mkdir $INSTALL_PATH/plugin/tandem_lib/agent/
mkdir $INSTALL_PATH/plugin/tandem_lib/crdt/

# Agent
$(
  cd $SCRIPT_PATH/../../agent/;
  rm -f **/*.pyc
)
cp -r $SCRIPT_PATH/../../agent/ $INSTALL_PATH/plugin/tandem_lib/agent/

# CRDT
$(
  cd $SCRIPT_PATH/../../crdt/;
  npm run clean;
  rm -rf node_modules;
  npm install;
  npm run build
)
cp -r $SCRIPT_PATH/../../crdt/build/ $INSTALL_PATH/plugin/tandem_lib/crdt/build/

# Sublime specific files
cd $SCRIPT_PATH/../../plugins/vim/
cp tandem_lib/*.py $INSTALL_PATH/plugin/tandem_lib/
cp tandem_vim.vim $INSTALL_PATH/plugin/
cp README_vim.md $INSTALL_PATH/README.md

echo "Release succesfully prepared."
