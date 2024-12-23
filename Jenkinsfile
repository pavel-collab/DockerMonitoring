pipeline {
    // Есть 2 принципиальных подхода к написанию Jenkins файлов: скриптовый и декларативный.
    // Здесь мы используем более подзний декларативный подход.

    agent any // Использует любого доступного агента

    parameters {
        string(name: 'DATABASE_HOST', defaultValue: 'localhost', description: 'Setup the data base ip address')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check data base status') {
            steps {
                sh """
                if ping -c 4 ${params.DATABASE_HOST} > /dev/null; then
                    echo "хост доступен"
                else
                    echo "хост недоступен"
                    exit 1 
                fi
                """
            }
        }

        stage('Check Tools') {
            steps {
                sh 'python3 --version || (echo "Python is not installed" && exit 1)'
            }
        }

        //! сейчас есть проблема с установкой зависимостей из requirements.txt
        //TODO: Поправить файл зависимостей и раскомментить последнюю строчку для установки зависимостей
        stage("Build Virtual Environment"){
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip3 install --upgrade pip
                    # pip3 install -r requirements.txt
                '''
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                sh '''
                echo 'Run tests'
                '''
            }
        }
    }

    // Секция определяет действия, которые надо произвести после прохождения всех шагов.
    // Секция success отрабатывает, если ВСЕ шаги пайплайна прошли успешно.
    post {
        success {
            echo 'Tests passed!'
        }
        failure {
            echo 'Tests failed!'
        }
    }
}