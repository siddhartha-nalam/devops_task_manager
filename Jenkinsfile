pipeline {
  agent any
  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // configure in Jenkins
    EC2_SSH = credentials('ec2-ssh') // username and private key configured in Jenkins
    EC2_HOST = "YOUR.EC2.IP.OR.HOSTNAME" // replace in Jenkins job or use parameter
    IMAGE_NAME = "yourdockerhubusername/devops-task-manager"
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Unit Tests') {
      steps {
        sh 'python -m pip install --upgrade pip'
        sh 'pip install -r requirements.txt'
        sh 'python -m pytest -q || true' // optional tests placeholder
      }
    }
    stage('Build Docker Image') {
      steps {
        sh "docker build -t $IMAGE_NAME:${env.BUILD_NUMBER} ."
        sh "docker tag $IMAGE_NAME:${env.BUILD_NUMBER} $IMAGE_NAME:latest"
      }
    }
    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
          sh "docker push $IMAGE_NAME:${env.BUILD_NUMBER}"
          sh "docker push $IMAGE_NAME:latest"
        }
      }
    }
    stage('Deploy to EC2') {
      steps {
        // deploy using SSH - ensure ec2 key is added to Jenkins credentials and host is reachable
        sh '''
        ssh -o StrictHostKeyChecking=no -i $EC2_SSH $EC2_HOST "docker pull $IMAGE_NAME:latest && docker stop devops_task || true && docker rm devops_task || true && docker run -d --name devops_task -p 80:5000 $IMAGE_NAME:latest"
        '''
      }
    }
  }
  post {
    failure {
      echo 'Build or deploy failed.'
    }
  }
}
