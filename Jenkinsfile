pipeline {
    agent any

    stages {

        stage('Get Code') {
            steps {
                echo 'Getting project code'
            }
        }

        stage('Install Requirements') {
            steps {
                bat 'python -m pip install -r Requirement.txt'
            }
        }

        stage('Test Application') {
            steps {
                bat 'python -m py_compile App.py'
            }


        }

        stage('Deployment Check') {
            steps {
                echo 'Deployment  stage completed'
            }
        }
    }


    post {
        success {
            echo 'CI/CD Pipeline completed successfully'
        }

        failure {
            echo 'CI/CD Pipeline failed'
        }
    }
}