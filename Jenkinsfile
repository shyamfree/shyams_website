pipeline {

    agent any
    environment {
        DOCKER_USER = 'shyamfree13'
        DOCKER_REPO = 'devops-portal'
        VERSION = '${BUILD_NUMBER}'
    }
    stages {
        stage ('Git url') {
            steps {
                git url: 'https://github.com/shyamfree/shyams_website.git', branch: 'main'
            }
        }
        stage ('Docker build') {
            steps {
                sh 'docker build -t dportal:v1 .'
            }
        }
        stage ('Docker run') {
            steps {
                sh 'docker rm -f dportal:v1 || true'
                sh 'docker run -d -p 5000:5000 dportal:v1'
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
                    usernameVariable: 'DOCKR_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                 sh ''' echo $DOCKER_PASS | docker login -DOCKR_USER $DOCKER_USER --password-stdin'''
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


    }



}