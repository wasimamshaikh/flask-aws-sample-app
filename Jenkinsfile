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

        stage('Login to ECR') {
            steps {
                withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
                    script {
                        sh '''
                        aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin 592546279953.dkr.ecr.us-east-1.amazonaws.com
                        '''
                    }
                }
            }
        }
     
        stage('Push Image to ECR') {
            steps {
                script {
                    sh '''
                    docker tag flask-aws-sample-app:$IMAGE_TAG $ECR_REPO:$IMAGE_TAG
                    docker push $ECR_REPO:$IMAGE_TAG
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Successfully built and pushed image to ECR: $ECR_REPO:$IMAGE_TAG"
        }
        failure {
            echo "❌ Build failed!"
        }
    }

}
