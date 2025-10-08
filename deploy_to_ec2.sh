#!/usr/bin/env bash
# Usage: ./deploy_to_ec2.sh <ec2-user> <ec2-host> <docker-image>
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <ec2-user> <ec2-host> <docker-image>"
  exit 1
fi
USER=$1
HOST=$2
IMAGE=$3

ssh -o StrictHostKeyChecking=no ${USER}@${HOST} "docker pull ${IMAGE} && docker stop devops_task || true && docker rm devops_task || true && docker run -d --name devops_task -p 80:5000 ${IMAGE}"
