pipeline {
    agent any

    environment {
        // 🔴 CHANGE THIS PATH based on your system
        PYTHON = "C:\\Users\\yedve\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
        VENV = "venv"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                bat '"%PYTHON%" -m venv %VENV%'
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