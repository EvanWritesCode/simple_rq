#!/bin/bash

mkdir ~/dev
mkdir ~/dev/irad
mkdir ~/dev/irad/maestro
cd ~/dev/irad/maestro

#pull down repo
git clone https://github.com/EvanWritesCode/maestro.git ~/dev/irad/maestro

#install virtual env venv (only needed for ubuntu/debian)
sudo apt install -y python3-venv


##user profile located virtual environments
#mkdir ~/virtualenvs
#create environment
#python3 -m venv ~/virtualenvs/env1
#activate environment
#source ~/virtualenvs/env1/bin/activate

##OR project located virtual enviornments
python3 -m venv ./venv
source ./venv/bin/activate
#default venv environment does not have a few things so install them
pip install --upgrade setuptools wheel


pip install -r requirements.txt

#this is only for initial setup where requirements.txt is not yet created
##set up virtual environment
##install flask
#pip install flask
##install redis and rq tools
#pip install redis rq rq-dashboard
##install mongo tooling
#pip install pymongo
#pip freeze > requirements.txt


echo "https://addons.mozilla.org/en-US/firefox/addon/rested/?src=recommended"
read -p "Optional: see above url to manually install firefox plugin rested for api debugging"

read -p "Optional: press enter to install mongodb compass.  run with mongodb-compass or from application menu"
wget https://downloads.mongodb.com/compass/beta/mongodb-compass-community-beta_1.18.0~beta.3_amd64.deb
sudo apt install ./mongodb-compass-community-beta_1.18.0~beta.3_amd64.deb

#touch app.py config.py .gitignore README.md requirements.txt
