pipeline {
    agent any

    tools {
        allure 'allure-2.36.0'
    }

    stages {
        stage('Install') {
            steps {
                bat '''
                    C:\\Python39\\python.exe -m pip install -r requirements.txt
                    C:\\Python39\\python.exe -m pip install allure-pytest==2.13.2
                '''
            }
        }
        stage('Test') {
            steps {
                bat '''
                    C:\\Python39\\python.exe -m pytest tests ^
                        --junitxml=test-results.xml ^
                        -v ^
                        --alluredir=allure-results
                '''
            }
        }
    }

    post {
        always {
            allure([
                results: [[path: 'allure-results']],
                reportBuildPolicy: 'ALWAYS'
            ])
            junit 'test-results.xml'
        }
    }
}