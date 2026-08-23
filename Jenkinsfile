pipeline{
    agent any
    environment {
        IMAGE_NAME= "my-python-app"
        IMAGE_TAG= "${BUILD_NUMBER}"
        CONTAINER = "my-python-app"
    }
    stages{
        stage('Checkout'){
            steps {
                checkout scm
            }
        }
        stage('Test'){
            steps {
                sh '''
                    set -e
                    python3 -m venv venv
                    . venv/bin/activate
                    
                    pip install -r requirements.txt
                   
                   '''
            }
        }
        stage('Build Image'){
            steps {
                sh '''
                   set -e 
                   
                   podman build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                   
                   '''
            }
        }
          
        stage('Run Container'){
            steps {
                sh '''
                   set -e 
                   
                   echo "starting new container"
                   
                   podman run -dt --name ${CONTAINER} -p 8000:8501/tcp ${IMAGE_NAME}:${IMAGE_TAG}
                   
                   echo "container started"
                   
                   podman ps --filter name=${CONTAINER}
                   
                   '''
                   
            }
        }
        
    }
    
    post {
        always {
            sh 'podman images'
        }
        success{
            echo 'pipeline completed successfully'
        }
        failure{
            echo 'pipeline failed!'
        }
    }
}
