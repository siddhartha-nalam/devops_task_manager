#!/usr/bin/env bash
# Run on the EC2 instance (Ubuntu 20.04 / 22.04)
set -e
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release
# install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# install docker-compose (optional)
sudo apt-get install -y python3-pip
pip3 install docker-compose
echo "Docker installed. Log out and back in (or `newgrp docker`) to use docker without sudo."
