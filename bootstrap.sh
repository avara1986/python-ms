#!/bin/bash

echo "Updating package repositories..."
apt-get update

echo "Install opencv..."
apt-get -y install build-essential cmake pkg-config git
apt-get -y install libffi-dev libffi6
apt-get -y install libjpeg-dev libpng-dev
apt-get -y install libsm6 libxrender1 libfontconfig1
apt-get -y install python-dev python-tk python-setuptools python-virtualenv

echo "Installing python3.6.."
add-apt-repository ppa:jonathonf/python-3.6
apt-get update
apt-get -y install python3.6

echo "Installing Nginx..."
apt-get -y install nginx
cat <<EOT >> /etc/nginx/sites-enabled/docker.conf
server {
    listen 8888;

    server_name localhost;

    proxy_redirect off;
    proxy_buffering off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
EOT

echo "Installing Docker..."
apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
apt-key fingerprint 0EBFCD88
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
apt-get update
apt-get -y install docker-ce
groupadd docker
usermod -aG docker vagrant

echo "Installing Docker compose..."
curl -L https://github.com/docker/compose/releases/download/1.19.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
