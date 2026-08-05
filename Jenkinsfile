pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    parameters {
        choice(
            name: 'TEST_TYPE',
            choices: ['smoke', 'regression', 'all'],
            description: 'Select the test suite'
        )

        choice(
            name: 'TARGET_ENVIRONMENT',
            choices: ['development', 'testing', 'production'],
            description: 'Select target environment'
        )

        booleanParam(
            name: 'GENERATE_HTML_REPORT',
            defaultValue: true,
            description: 'Generate pytest HTML report'
        )
    }

    environment {
        APPLICATION_NAME = 'calculator-service'
        VENV_DIRECTORY = 'venv'
        REPORT_DIRECTORY = 'reports'
    }

    stages {
        stage('Environment Information') {
            steps {
                echo "Application: ${env.APPLICATION_NAME}"
                echo "Job: ${env.JOB_NAME}"
                echo "Build: ${env.BUILD_NUMBER}"
                echo "Workspace: ${env.WORKSPACE}"

                bat 'python --version'
                bat 'git --version'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                    if exist %VENV_DIRECTORY% rmdir /s /q %VENV_DIRECTORY%
                    python -m venv %VENV_DIRECTORY%
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    call %VENV_DIRECTORY%\\Scripts\\activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Build') {
            steps {
                bat '''
                    call %VENV_DIRECTORY%\\Scripts\\activate
                    python -m compileall app
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                script {
                    bat 'if not exist reports mkdir reports'

                    if (params.TEST_TYPE == 'all') {
                        bat '''
                            call venv\\Scripts\\activate
                            python -m pytest -v --junitxml=reports\\test-results.xml
                        '''
                    } else {
                        bat """
                            call venv\\Scripts\\activate
                            python -m pytest -v -m ${params.TEST_TYPE} --junitxml=reports\\test-results.xml
                        """
                    }
                }
            }
        }

        stage('HTML Report') {
            when {
                expression {
                    params.GENERATE_HTML_REPORT
                }
            }

            steps {
                script {
                    if (params.TEST_TYPE == 'all') {
                        bat '''
                            call venv\\Scripts\\activate
                            python -m pytest --html=reports\\test-report.html --self-contained-html
                        '''
                    } else {
                        bat """
                            call venv\\Scripts\\activate
                            python -m pytest -m ${params.TEST_TYPE} --html=reports\\test-report.html --self-contained-html
                        """
                    }
                }
            }
        }

        stage('Testing Environment Validation') {
            when {
                expression {
                    params.TARGET_ENVIRONMENT == 'testing'
                }
            }

            steps {
                echo 'Running testing-environment validation'
            }
        }

        stage('Production Approval') {
            when {
                expression {
                    params.TARGET_ENVIRONMENT == 'production'
                }
            }

            steps {
                input message: 'Approve production deployment?',
                      ok: 'Approve'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed'

            junit allowEmptyResults: true,
                  testResults: 'reports/test-results.xml'

            archiveArtifacts artifacts: 'reports/**/*',
                             allowEmptyArchive: true
        }

        success {
            echo "Build ${env.BUILD_NUMBER} completed successfully"
        }

        failure {
            echo "Build ${env.BUILD_NUMBER} failed"
        }

        unstable {
            echo "Build ${env.BUILD_NUMBER} is unstable"
        }

        cleanup {
            echo 'Cleaning workspace resources'
        }
    }
}