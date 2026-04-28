pipeline {

    agent any

    stages {
        stage ('Git url') {
            steps {
                sh 'git pull origin https://github.com/shyamfree/shyams_website.git'
            }
        }
        stage ('Docker build') {
            steps {
                sh 'docker build -t dportal:v1 .'
            }
        }
        stage ('Docker run') {
            steps {
                sh 'docker run -d -p 5000:5000 dportal:v1'
            }
        }
        stage ('Docker test') {
            steps {
                
                sh 'docker ps'

            }
        }
    }



}