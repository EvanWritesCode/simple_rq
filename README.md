# Maestro

## WIP Environment setup.  These instructions are for a local running environment (not docker) in ubuntu.   
Install dependencies:   
Run `sudo bash maestro_dependencies.sh`

Configure Redis:
For dev:
* ~line 147 replace `supervised no` to `supervised systemd`
* ~line 507 uncomment `requirepass foobared` and change `foobared` to a secure and long password of your choosing" 

For Prod:  WIP

For Dev environment, run:
`./maestro_dev_environment_setup.sh`

recommended dev tools:
API POST tool such as firefox rested plugin  
https://addons.mozilla.org/en-US/firefox/addon/rested/?src=recommended

mongodb viewer such as mongodb compass  (Note that the dev env script will install this for you if you let it)
wget https://downloads.mongodb.com/compass/beta/mongodb-compass-community-beta_1.18.0~beta.3_amd64.deb
sudo apt install ./mongodb-compass-community-beta_1.18.0~beta.3_amd64.deb


After all dependencies have been installed:  run maestro for development:

ensure redis is running:
`sudo systemctl status redis.service`

run redis worker in new terminal
activate environment
`source .envrc`
`python worker.py`

run API in new terminal
activate environment
```
source .envrc
python app.py
```

run rq-dashboard in its own terminal
```
source .envrc
rq-dashboard --redis-password reallylongpasswordgoeshere
```

