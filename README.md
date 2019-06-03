## Maestro

# WIP Environment setup.  These instructions are for a local running environment (not docker) in ubuntu.   
Install Redis:   to install and configure redis run redis_install.sh and configure according to instructions including
For dev:
~line 147 replace supervised no to supervised systemd
~line 507 uncomment requirepass foobared and change foobared to a secure and long password" 

To install mongodb, venv (if necessary), setup virtual env, and install dependencies,  run
maestro_environment_setup.sh

recommended dev tools:
API POST tool such as firefox rested plugin
https://addons.mozilla.org/en-US/firefox/addon/rested/?src=recommended

mongodb viewer such as mongodb compass
wget https://downloads.mongodb.com/compass/beta/mongodb-compass-community-beta_1.18.0~beta.3_amd64.deb
sudo apt install ./mongodb-compass-community-beta_1.18.0~beta.3_amd64.deb


After all dependencies have been installed:  run maestro for development:

ensure redis is running:
sudo systemctl status redis

run redis worker in new terminal
activate environment
source .envrc
python worker.py

run API in new terminal
activate environment
source .envrc
python app.py

run rq-dashboard in its own terminal
source .envrc
rq-dashboard --redis-password reallylongpasswordgoeshere

