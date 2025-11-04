pipeline {
    agent any

    environment {
        GIT_PAT = credentials('github-pat')  // Jenkins credential ID for GitHub PAT
        IMAGE_NAME = "rinchal/flask-mysql-app"
        CONTAINER_NAME = "flask-mysql-container-${env.BUILD_NUMBER}"
        REPO_URL = "https://github.com/RinchalShete/flask-mysql-app.git"
        SAFE_BUILD_DIR = "/home/jenkins/tmpbuild"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                echo '🧹 Cleaning workspace...'
                deleteDir()
            }
        }

        stage('Clone Repository') {
            steps {
                echo '🚀 Cloning private repository...'
                sh '''
                rm -rf flask-mysql-app || true
                git clone https://RinchalShete:${GIT_PAT}@github.com/RinchalShete/flask-mysql-app.git
                cd flask-mysql-app
                git checkout main
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image from /home/jenkins/tmpbuild (snap-safe)...'
                sh '''
                # Ensure safe directory exists
                mkdir -p ${SAFE_BUILD_DIR}
                rm -rf ${SAFE_BUILD_DIR}/* || true

                # Copy only the web folder into safe directory
                cp -R flask-mysql-app/web ${SAFE_BUILD_DIR}/

                # Build inside safe directory
                cd ${SAFE_BUILD_DIR}/web
                docker build --no-cache -t ${IMAGE_NAME} .

                # Optional cleanup
                rm -rf ${SAFE_BUILD_DIR}/web
                '''
            }
        }

        stage('Test Docker Container') {
            steps {
                echo '🏃 Running Docker container for testing...'
                sh '''
                docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}
                echo "Container ${CONTAINER_NAME} is running!"
                sleep 10
                docker ps | grep ${CONTAINER_NAME} || (echo "Container failed to start!" && exit 1)
                docker stop ${CONTAINER_NAME} && docker rm ${CONTAINER_NAME}
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo '📦 Pushing image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker tag ${IMAGE_NAME}:latest $DOCKER_USER/flask-mysql-app:latest
                    docker push $DOCKER_USER/flask-mysql-app:latest
                    '''
                }
                echo '✅ Image pushed to Docker Hub successfully!'
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs for details.'
        }
    }
}
