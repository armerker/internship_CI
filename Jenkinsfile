pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        REPO_URL = 'https://github.com/armerker/internship_CI'
        BRANCH = 'master'
    }

    tools {
        allure 'allure-2.36.0'
    }

    stages {
        stage('Test in Docker') {
            steps {
                bat '''
                    docker-compose up -d selenoid
                    timeout /t 15
                    docker-compose run --rm tests
                '''
            }
        }
    }

    post {
        always {
            bat 'docker-compose down'
            allure results: [[path: 'allure-results']]
            junit 'test-results.xml'
        }
    }
}