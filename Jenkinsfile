pipeline {
    agent any

    tools {
        allure 'allure-2.36.0'
    }

    environment {
        // Переменные для Docker
        DOCKER_COMPOSE = 'docker-compose'
        SELENOID_HOST = 'localhost'
        SELENOID_PORT = '4444'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Environment') {
            steps {
                bat '''
                    mkdir allure-results
                    mkdir test-logs
                    mkdir allure-reports

                    // Проверяем наличие Docker
                    docker --version
                    docker-compose --version
                '''
            }
        }

        stage('Start Selenoid') {
            steps {
                bat '''
                    echo Starting Selenoid...
                    docker-compose up -d selenoid

                    // Ждём запуска Selenoid
                    timeout /t 15 /nobreak

                    // Проверяем статус
                    docker ps | findstr selenoid
                '''
            }
        }

        stage('Run Tests in Docker') {
            steps {
                bat '''
                    echo Running tests in Docker container...

                    // Запускаем тесты в контейнере
                    docker-compose run --rm tests

                    // Копируем результаты из контейнера (если нужно)
                    // Но у нас уже есть volume в docker-compose
                '''
            }
            post {
                always {
                    bat '''
                        echo Tests completed, collecting results...
                    '''
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat '''
                    echo Generating Allure report...

                    // Генерируем отчёт через Docker или локально
                    allure generate allure-results -o allure-reports --clean
                '''
            }
        }
    }

    post {
        always {
            // Останавливаем контейнеры
            bat '''
                echo Stopping containers...
                docker-compose down
            '''

            // Публикуем Allure отчёт
            allure([
                results: [[path: 'allure-results']],
                report: 'allure-reports',
                reportBuildPolicy: 'ALWAYS'
            ])

            // Публикуем JUnit результаты
            junit 'test-results.xml'

            // Архивируем логи
            archiveArtifacts artifacts: 'test-logs/**/*.log', allowEmptyArchive: true
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
        }

        failure {
            bat '''
                echo Tests failed! Check logs for details.
                docker-compose logs selenoid > test-logs/selenoid.log
                docker-compose logs tests > test-logs/tests.log
            '''
        }
    }
}