# Maestro

## WIP Environment setup.  These instructions are for a local running environment (not docker) in ubuntu.   
Install dependencies:   
Run 
`sudo bash maestro_dependencies.sh`

Configure Redis.  open `/etc/redis/redis.conf` as sudo and modify:

For dev:
* ~line 147 replace `supervised no` to `supervised systemd`
* ~line 507 uncomment `requirepass foobared` and change `foobared` to a secure and long password of your choosing.  The code is configured to use password `reallylongpasswordgoeshere` (TODO:  change to env var) 

For Prod:  WIP

For Dev environment, run:
`./maestro_dev_environment_setup.sh`

recommended dev tools:
API POST tool such as firefox rested plugin  
https://addons.mozilla.org/en-US/firefox/addon/rested/?src=recommended

mongodb viewer such as mongodb compass  (see maestro_dev_environment.sh for install)


After all dependencies have been installed:  run maestro for development:

ensure redis is running:
`sudo systemctl status redis.service`

run redis worker in new terminal
activate environment

`source .envrc`

`python worker.py`

run API in new terminal
```
source .envrc
python app.py
```

See if API is running by going to http://localhost:5000/heartbeat in a browser


run rq-dashboard in new terminal
```
source .envrc
rq-dashboard --redis-password reallylongpasswordgoeshere
```

To go to rq-dashboard,  navigate to http://localhost:9181/


Submit a job:  WIP

Open Firefox RESTED plugin (or CURL, or other API tool)
Set it to POST  http://192.168.0.1:5000/
Headers:  `Content-Type: application/json`
Request body: type json
parameters:  see models/training_task.py for all available parameters
For example
name:your name here
description:your description here



