pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        IMAGE_TAG = "${env.BUILD_NUMBER}"     // Jenkins build number as image tag
        ECR_REPO = '592546279953.dkr.ecr.us-east-1.amazonaws.com/flask-aws-sample-app'
    }


    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/wasimamshaikh/flask-aws-sample-app.git'
            }
        }

        stage('Docker Build Image') {
            steps {
                script {
                    sh "docker build -t flask-aws-sample-app:${IMAGE_TAG} ."
                }
            }
        }
   }
}