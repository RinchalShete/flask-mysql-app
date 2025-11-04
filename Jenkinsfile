pipeline {
    agent any

    environment {
        IMAGE_NAME = "rinchal/flask-mysql-app"
        REPO_URL = "https://github.com/RinchalShete/flask-mysql-app.git"
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo "Cloning repository from GitHub..."
                git branch: 'main', url: "${REPO_URL}"
                echo "Repository cloned successfully."
            }
        }

        stage('Build Flask Image') {
            steps {
                script {
                    echo "Building Docker image for Flask app..."
                    sh 'docker build -t $IMAGE_NAME ./web'
                    echo "Docker image built: $IMAGE_NAME"
                }
            }
        }

        stage('Test Container') {
            steps {
                script {
                    echo "Running test container..."
                    sh 'docker run -d -p 5000:5000 --name test_flask $IMAGE_NAME'
                    sh 'sleep 10'
                    echo "Checking running containers..."
                    sh 'docker ps | grep test_flask'
                    echo "Flask container test passed."
                    sh 'docker stop test_flask && docker rm test_flask'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Logging into Docker Hub and pushing image..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker tag $IMAGE_NAME:latest $DOCKER_USER/flask-mysql-app:latest
                        docker push $DOCKER_USER/flask-mysql-app:latest
                    '''
                }
                echo "Image pushed to Docker Hub successfully!"
            }
        }
    }
}
