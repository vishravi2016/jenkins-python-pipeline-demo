pipeline {

    agent any

    stages {
        stage('checkout information') {
            steps{
                echo 'jenkins automatically checked out the repo'
                bat 'git branch'
                bat 'git log -1 --oneline'
            }
        }
        stage('Build'){
            steps{
                bat 'python -m compileall app'
            }
        }

    }
}