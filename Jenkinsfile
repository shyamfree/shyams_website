pipeline {

    agent any
    environment {
        DOCKER_USER = 'shyamfree13'
        DOCKER_REPO = 'devops-portal'
        VERSION = "${BUILD_NUMBER}"
    }
    stages {
        stage ('Git url') {
            steps {
                git url: 'https://github.com/shyamfree/shyams_website.git', branch: 'main'
            }
        }
        stage ('Docker build') {
            steps {
                sh 'docker build -t dportal:${BUILD_NUMBER} .'
            }
        }
        stage ('Docker run') {
            steps {
                sh 'docker rm -f dportal-container || true'
                //sh 'docker run -d -p 5000:5000 --name dportal-container dportal:v1'
            }
        }
        stage ('Docker test') {
            steps {
                
                sh 'docker ps'

            }
        }
        stage ('Docker login') {

            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                 sh ''' echo $DOCKER_PASS | docker login -u  $DOCKER_USER --password-stdin '''
                }
                
            }
        }
        stage('docker tag') {
            steps {
                sh 'docker tag  dportal:v1 $DOCKER_USER/$DOCKER_REPO:$VERSION'
            }
        }

        stage ('Docker push') {
            steps {
                sh 'docker push $DOCKER_USER/$DOCKER_REPO:$VERSION'
            }
        }

        stage ('k8s image update') {
            steps {
                sh '''sed -i "s|VERSION|${VERSION}|g" kubernetes/deployment.yaml '''
                sh 'echo '
            }
        }
        stage ('Deploy to k8s') {
            steps {
                sh 'kubectl delete deployment devops-portal-deployment -ndevops|| true'
                sh 'kubectl create namespace devops || true'
                sh 'kubectl apply -f kubernetes/deployment.yaml -ndevops'
                sh 'kubectl apply -f kubernetes/service.yaml -ndevops'
            }
        }
        stage ('Check the deployment and service') {
            steps {
                sh 'kubectl get pods -ndevops'
                sh 'kubectl get svc -ndevops'
            }
        }
        stage('Wait and port forward') {
             steps {
                sh 'sleep 10'
                sh 'kubectl port-forward service/devops-portal-service 9090:80 --address 0.0.0.0'
             }
        }

    }




}