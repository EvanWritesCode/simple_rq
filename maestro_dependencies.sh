#!/bin/bash

[[ $EUID -ne 0 ]] && echo "This script must be run as root/sudo." && exit 1
read -p "press enter to begin maestro dependencies"

#if on desktop ubuntu, remove snapd which causes hangups in the update and upgrade process
apt -y purge snapd

apt -y update
apt -y upgrade


#install basic prereqs
apt -y install curl software-properties-common apt-transport-https wget ca-certificates git ssh net-tools nano

#install python and python related
apt -y install python3 python3-pip libpq-dev python3-venv

apt -y install awscli bash-completion


#install redis
read -p "Press enter to install redis"
bash redis_install.sh

#install mongodb
read -p "Press enter to install mongodb"
sudo apt install -y mongodb

