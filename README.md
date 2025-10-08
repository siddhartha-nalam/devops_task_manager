# DevOps Task Manager - End-to-End Project

A simple Flask-based Task Manager app (CRUD) with full DevOps setup:
- Dockerized Flask application
- `docker-compose.yml` for local runs
- `Jenkinsfile` to build, push to Docker Hub, and deploy to AWS EC2
- Deployment scripts for EC2

## What's included
- `app.py` - Flask app + SQLAlchemy (SQLite)
- `templates/` and `static/` - UI files
- `Dockerfile` & `docker-compose.yml`
- `Jenkinsfile` - pipeline (build -> push -> deploy)
- `deploy_to_ec2.sh` - simple SSH deploy helper
- `provision_ec2.sh` - bootstrap script for EC2
- `init_db.py` - initialize DB
- `requirements.txt`

## Quick local run (fast demo) in windows
1. Install Python 3.11+ and Docker.
2. Create venv and install:  
```bash
python -m venv venv
venv/bin/activate
pip install -r requirements.txt
python init_db.py
python app.py
```
Open http://localhost:5000

Or run with Docker:
```bash
docker build -t devops-task-manager:local .
docker run -p 5000:5000 devops-task-manager:local
```

## Deploy to AWS EC2 (manual steps)
1. Launch an EC2 instance (Ubuntu 22.04 recommended). Open ports: 22 (SSH), 80 (HTTP).
2. SSH into the instance and run `provision_ec2.sh` to install Docker:
```bash
ssh -i yourkey.pem ubuntu@YOUR.EC2.IP
# on EC2
bash -s < provision_ec2.sh
```
3. On your local machine build & push the Docker image to Docker Hub:
```bash
docker build -t yourdockerhubusername/devops-task-manager:latest .
docker login
docker push yourdockerhubusername/devops-task-manager:latest
```
4. Deploy on EC2:
```bash
ssh -i yourkey.pem ubuntu@YOUR.EC2.IP "docker pull yourdockerhubusername/devops-task-manager:latest && docker run -d --name devops_task -p 80:5000 yourdockerhubusername/devops-task-manager:latest"
```

## Jenkins setup (high-level)
1. Install Jenkins (on a CI server) and enable Docker on Jenkins host.
2. Add Jenkins credentials:
   - `dockerhub-creds` (username/password)
   - `ec2-ssh` (private key or username/key pair)
3. Create a pipeline job pointing to this repo. The provided `Jenkinsfile` will:
   - Run tests (placeholder)
   - Build Docker image
   - Push to Docker Hub
   - SSH to EC2 and deploy

> Notes: The Jenkinsfile contains placeholders for `EC2_HOST` and credential IDs — replace them in Jenkins job configuration. Fine-tune security (SSH keys, secrets) for production.



## Troubleshooting
- If Jenkins can't SSH to EC2: ensure security group allows Jenkins IP and the private key is correct.
- If app doesn't start: check Docker logs `docker logs devops_task`.
