pipeline {

    agent any 
    environment {
       PYTHON_EXECUTABLE_DIR = 'C:\Users\Adriele\AppData\Local\Microsoft\WindowsApps\python'
        
        PATH = "${PYTHON_EXECUTABLE_DIR};${PYTHON_EXECUTABLE_DIR}\\Scripts;${env.PATH}"
        
        
        SONAR_ORGANIZATION = 'adriele-mesquita'
        SONAR_PROJECT_KEY = 'adriele-mesquita_foodTravelWebII'         //
        SONAR_LOGIN = credentials('sonarcloud-token')   ;
    }

    stages {
        stage('Checkout do Código') {
            steps {
                git branch: 'main', url: 'https://github.com/adriele-mesquita/foodTravelWebII'
            }
        }
        stage('Configurar Ambiente Virtual') {
            steps {
                script {
                    if (!fileExists('venv/Scripts/activate')) {
                        echo 'Criando ambiente virtual...'
                        bat 'python -m venv venv' 
                    } else {
                        echo 'Ambiente virtual já existe.'
                    }
                    
                    echo 'Instalando dependências...'
                    bat 'venv\\Scripts\\activate && pip install -r requirements.txt' 
                }
            }
        }
        stage('Executar Migrações') {
            steps {
                script {
                    echo 'Executando migrações...'
                    bat 'venv\\Scripts\\activate && python manage.py makemigrations foodtravel_app --no-input && python manage.py migrate --no-input' 
                }
            }
        }
        stage('Executar Testes Django') {
            steps {
                script {
                    echo 'Executando testes Django...'
                    bat 'venv\\Scripts\\activate && python manage.py test foodtravel_app' 
                }
            }
        }

        stage('Análise de Código com SonarCloud') {
            steps {
                script {
                    echo 'Iniciando análise com SonarCloud...'
                    withSonarQubeEnv('SonarCloud') { 
                        bat "sonar-scanner.bat -Dsonar.projectKey=${SONAR_PROJECT_KEY} -Dsonar.organization=${SONAR_ORGANIZATION} -Dsonar.sources=foodtravel_app -Dsonar.login=${SONAR_LOGIN}"
                    }
                }
            }
        }

  
    }

    post {
        always {
            echo 'Pipeline feito.'
        }
        success {
            echo 'Build feita! '
        }
        failure {
            echo 'Build falhou!'
        }
      
    }
}
