pipeline {

    agent any

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