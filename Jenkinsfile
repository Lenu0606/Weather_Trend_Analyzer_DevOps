pipeline {
    agent any

    stages {

        stages('Get Code') {
            steps {
                echo 'Getting project code'
            }
        }

        stage('Install Requirements') {
            steps {
                bat 'python -m pip install -r Requirement.txt'
            }
        }

        stage('Run Application') {
            steps {
                echo 'Deployment stage completed'
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