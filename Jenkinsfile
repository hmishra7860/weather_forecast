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
                withCredentials([
                    string(
                        credentialsId: 'weather-api-key',
                        variable: 'API_KEY'
                    )
                ]) {
                    sh '''
                        set -e

                        podman stop ${CONTAINER} 2>/dev/null || true
                        podman rm ${CONTAINER} 2>/dev/null || true

                        JENKINS_NODE_COOKIE=dontKillMe \
                        podman run -d \
                            --name ${CONTAINER} \
                            -p 8000:8501 \
                            -e API_KEY="${API_KEY}" \
                            ${IMAGE_NAME}:${IMAGE_TAG}

                        sleep 5

                        podman ps -a --filter name=${CONTAINER}
                    '''
                }
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
