pipeline {
    agent any


    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/wasimamshaikh/flask-aws-sample-app.git'
            }
        }

        stage('Docker Build Image') {
            steps {
                script {
                    sh 'docker build -t flask-aws-sample-app:$IMAGE_TAG .'
                }
            }
        }
   }
}
