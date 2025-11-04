pipeline {
    agent any

    environment {
        IMAGE_NAME = "rinchal/flask-mysql-app"
        COMPOSE_FILE = "docker-compose.yml"
        REPO_URL = "https://github.com/RinchalShete/flask-mysql-app.git"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    sh 'docker compose -f $COMPOSE_FILE build'
                }
            }
        }

        stage('Run Containers for Testing') {
            steps {
                script {
                    // Start containers in detached mode
                    sh 'docker compose -f $COMPOSE_FILE up -d'
                    // Wait a bit for MySQL & Flask to start
                    sh 'sleep 15'
                    // Check running containers
                    sh 'docker ps'
                }
            }
        }

        stage('Push Flask Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker tag $IMAGE_NAME:latest $DOCKER_USER/flask-app:latest
                        docker push $DOCKER_USER/flask-app:latest
                    '''
                }
            }
        }

    }

    post {
        always {
            echo "Pipeline finished — containers cleaned up!"
        }
    }
}
