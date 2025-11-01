pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        IMAGE_TAG = "${env.BUILD_NUMBER}"     // Jenkins build number as image tag
        ECR_REPO = '592546279953.dkr.ecr.us-east-1.amazonaws.com/aws-flask-repo'
        KUBECONFIG = '/var/lib/jenkins/.kube/config'
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

        stage('Deploy to Minikube') {
            steps {
                script {
                    sh '''
                    echo "Deploying to Minikube cluster..."

                    # Apply deployment and service
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
          
                    # Update the deployment image
                    kubectl set image deployment/flask-app flask-app=${ECR_REPO}:${BUILD_NUMBER} --record

                    echo "Updated deployment.yaml to use image: ${ECR_REPO}:${BUILD_NUMBER}"
                    
                    kubectl rollout status deployment flask-app --timeout=120s
                    echo "Deployment successfully rolled out!"
                    '''
                }
            }
        }

        stage('Cleanup') {
            steps {
                sh '''
                echo "🧹 Cleaning up old Docker images..."
                docker image prune -af
                '''
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