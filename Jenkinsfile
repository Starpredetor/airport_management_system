pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    stages {

        stage('Checkout Code') {
            steps {
                // Jenkins automatically clones the repo where this Jenkinsfile exists
                checkout scm
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                bat 'python -m venv %VENV%'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '%VENV%\\Scripts\\pip install --upgrade pip'
                bat '%VENV%\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Run Application') {
            steps {
                bat '%VENV%\\Scripts\\python main.py'
            }
        }
    }

    post {
        success {
            echo 'Build Successful ✅'
        }
        failure {
            echo 'Build Failed ❌'
        }
    }
}