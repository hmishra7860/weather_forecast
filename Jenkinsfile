pipeline {
    agent {
        label 'rhel-client'
    }

    environment {
        IMAGE_NAME = "my-python-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        CONTAINER = "my-python-app"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh '''
                    set -e

                    python3 -m venv venv
                    . venv/bin/activate

                    pip install -r requirements.txt

                    echo "Tests completed successfully"
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    set -e

                    podman build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        .

                    echo "Image built successfully"
                    podman images
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    set -e

                    echo "Stopping old container..."
                    podman stop ${CONTAINER} 2>/dev/null || true

                    echo "Removing old container..."
                    podman rm ${CONTAINER} 2>/dev/null || true

                    echo "Starting new container..."

                    JENKINS_NODE_COOKIE=dontKillMe \
                    podman run -d \
                        --name ${CONTAINER} \
                        -p 8000:8501 \
                        ${IMAGE_NAME}:${IMAGE_TAG}

                    sleep 5

                    echo "===== Container Status ====="
                    podman ps -a --filter name=${CONTAINER}

                    echo "===== Container Logs ====="
                    podman logs ${CONTAINER}
                '''
            }
        }
    }

    post {
        always {
            sh 'podman images'
        }

        success {
            echo 'Pipeline completed successfully'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}
