pipeline {

    agent any

    stages {
        stage ('Git url') {
            steps {
                sh 'git pull origin https://github.com/shyamfree/shyams_website.git'
            }
        }
        stage ('test file') {
            steps {
                sh 'ls Dockerfile'
            }
        }
    }



}