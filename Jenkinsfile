pipeline {
    agent any

    tools {
        git 'Default'
    }

    environment {
        DESAFIO01_ENV = 'env_desafio01'
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: '5ef87ef9-9de4-4fb9-970c-fc57d71562a1', url: 'https://github.com/wiemor/qadesafios.git', branch: 'main'
            }
        }

        stage('Configurar entorno Desafio01') {
            steps {
                script{
                    def pythonPath = 'C:\\Users\\Wiemor\\AppData\\Local\\Programs\\Python\\Python311'
                    env.PATH = "${pythonPath};${pythonPath}\\Scripts;${env.PATH}"

                    bat 'python --version'
                    bat 'pip --version'
                    
                    dir('Desafio01') {
                        script {
                            bat '''
                                python -m venv %DESAFIO01_ENV%
                                call %DESAFIO01_ENV%\\Scripts\\activate.bat
                                %DESAFIO01_ENV%\\Scripts\\python.exe -m pip install -r requirements.txt
                            ''' 
                        }
                    }
                }
            }
        }

        stage('Run Behave Tests for Desafio 1') {
            steps {
                dir('desafio01') {
                    script {
                        try {
                            bat '''
                                if not exist features\\reports mkdir features\\reports
                                call %DESAFIO01_ENV%\\Scripts\\activate.bat
                                behave --version
                                behave -f pretty -f json -o features/reports/behave-report.json --junit --junit-directory features/reports
                            '''
                        } catch (Exception e) {
                            currentBuild.result = 'FAILURE'
                            error "Failed to run Behave tests for Desafio 01: ${e.message}"
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'Desafio01/features/reports/**/*.*', allowEmptyArchive: true
            junit testResults: 'Desafio01/features/reports/*.xml', allowEmptyResults: true
        }
    }
}
