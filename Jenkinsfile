pipeline {
    agent any

    stages {
        stage('Environment Check') {
            steps {
                echo '=== Stage 1: Checking environment tools ==='
                bat '''
                    set PATH=C:\\Users\\Saloni\\AppData\\Local\\Programs\\Python\\Python311;C:\\Users\\Saloni\\AppData\\Local\\Programs\\Python\\Python311\\Scripts;C:\\Program Files\\nodejs;C:\\Users\\Saloni\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;%PATH%
                    cd /d "C:\\Users\\Saloni\\Documents\\Devops Lab mini project"
                    python --version
                    node --version
                    docker --version
                    docker-compose --version
                '''
            }
        }

        stage('Train ML Model') {
            steps {
                echo '=== Stage 2: Training Demonstration Random Forest Model ==='
                bat '''
                    set PATH=C:\\Users\\Saloni\\AppData\\Local\\Programs\\Python\\Python311;C:\\Users\\Saloni\\AppData\\Local\\Programs\\Python\\Python311\\Scripts;%PATH%
                    cd /d "C:\\Users\\Saloni\\Documents\\Devops Lab mini project"
                    python ml\\train.py
                '''
            }
        }

        stage('Python Unit Tests') {
            steps {
                echo '=== Stage 3: Running Python Microservices Test Suite ==='
                bat '''
                    set PATH=C:\\Users\\Saloni\\AppData\\Local\\Programs\\Python\\Python311;C:\\Users\\Saloni\\AppData\\Local\\Programs\\Python\\Python311\\Scripts;%PATH%
                    cd /d "C:\\Users\\Saloni\\Documents\\Devops Lab mini project"
                    pytest tests\\python -q
                '''
            }
        }

        stage('API Gateway Tests') {
            steps {
                echo '=== Stage 4: Running Node.js API Gateway Tests ==='
                bat '''
                    set PATH=C:\\Program Files\\nodejs;%PATH%
                    cd /d "C:\\Users\\Saloni\\Documents\\Devops Lab mini project\\api-gateway"
                    npm test
                '''
            }
        }

        stage('Frontend Tests & Build') {
            steps {
                echo '=== Stage 5: Running Frontend Vitest and Production Build ==='
                bat '''
                    set PATH=C:\\Program Files\\nodejs;%PATH%
                    cd /d "C:\\Users\\Saloni\\Documents\\Devops Lab mini project\\frontend"
                    npm test
                    npm run build
                '''
            }
        }

        stage('Docker Compose Build') {
            steps {
                echo '=== Stage 6: Building Microservices Docker Images ==='
                bat '''
                    set PATH=C:\\Users\\Saloni\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;C:\\Users\\Saloni\\.docker\\cli-plugins;%PATH%
                    cd /d "C:\\Users\\Saloni\\Documents\\Devops Lab mini project"
                    docker-compose build
                '''
            }
        }

        stage('Deploy & Verify Stack') {
            steps {
                echo '=== Stage 7: Starting Stack and Verifying Health Check ==='
                bat '''
                    set PATH=C:\\Users\\Saloni\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;C:\\Users\\Saloni\\.docker\\cli-plugins;%PATH%
                    cd /d "C:\\Users\\Saloni\\Documents\\Devops Lab mini project"
                    docker-compose up -d
                    curl.exe -s http://localhost:8088/health
                '''
            }
        }
    }

    post {
        always {
            echo '=== Pipeline Execution Completed ==='
        }
        success {
            echo 'SUCCESS: All tests, builds, and container deployments passed cleanly!'
        }
        failure {
            echo 'FAILURE: Pipeline encountered an error.'
        }
    }
}
