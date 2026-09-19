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
                bat 'C:\\Users\\PC\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe -m pip install -r Requirements.txt'
            }
        }

        stage('Test Application') {
            steps {
                bat 'C:\\Users\\PC\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe -m py_compile App.py'
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