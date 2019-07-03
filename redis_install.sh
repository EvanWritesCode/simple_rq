#!/bin/bash

#Redis, RQ install
#https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04
#https://linuxize.com/post/how-to-install-and-configure-redis-on-ubuntu-18-04/

sudo apt install -y redis-server
#sudo systemctl status redis-server
echo "*********** BASIC REDIS SECURITY CONFIG ***************"
echo "*  Modify /etc/redis/redis.conf as sudo:"
echo "*  1.  ~line 147 replace `supervised no` to `supervised systemd`"
echo "*  2.  ~line 507 uncomment `requirepass foobared` and change `foobared` to a secure and long password"  
echo "*  3.  For Prod:  Rename dangerous commands that are not needed in prod such as FLUSHDB to an empty string to disable them. "
echo "*  4.  For Prod:  Configure firewall.   Configure so only specified clients can access/ reach redis"
echo "******************************************************"
#good way to generate long random password is openssl rand 60 | openssl base64 -A
read -p "Press enter to open a text editor to edit redis.conf"

sudo nano /etc/redis/redis.conf
sudo systemctl restart redis.service #redis-server

#verify running
#ss -an | grep 6379

#verify ports / binding
sudo netstat -lnp | grep redis

#see xaas environment setup for redis and rq python packages (installed under a venv)
read -p "Press enter to continue to next step"
