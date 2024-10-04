pipeline {
    agent any

    tools {
        git 'Default'
    }

    environment {
        DESAFIO01_ENV = 'env_desafio01'
        DESAFIO02_ENV = 'env_desafio02'
        WORKSPACE_DIR = ''
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    // Guardamos el directorio de trabajo principal
                    WORKSPACE_DIR = pwd()
                    echo "Workspace directory: ${WORKSPACE_DIR}"
                }
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
                dir('Desafio01') {
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

        stage('Configurar entorno Desafio02') {
            steps {
                script {
                    echo "Starting Desafio02 environment setup"
                    // Volvemos al directorio de trabajo principal
                    dir("${WORKSPACE_DIR}") {
                        echo "Current directory: ${pwd()}"
                        if (fileExists('Desafio02')) {
                            dir('Desafio02') {
                                echo "Entering Desafio02 directory: ${pwd()}"
                                bat '''
                                    echo Current directory: %CD%
                                    if not exist %DESAFIO02_ENV% (
                                        echo Creating virtual environment %DESAFIO02_ENV%
                                        python -m venv %DESAFIO02_ENV%
                                    ) else (
                                        echo Virtual environment %DESAFIO02_ENV% already exists
                                    )
                                    echo Activating virtual environment
                                    call %DESAFIO02_ENV%\\Scripts\\activate.bat
                                    echo Installing requirements
                                    %DESAFIO02_ENV%\\Scripts\\python.exe -m pip install -r requirements.txt
                                '''
                            }
                        } else {
                            error "Desafio02 directory not found in ${pwd()}"
                        }
                    }
                    echo "Finished Desafio02 environment setup"
                }
            }
        }

        stage('Run Behave Tests for Desafio 2') {
            steps {
                // Volvemos al directorio de trabajo principal
                dir("${WORKSPACE_DIR}") {
                    dir('Desafio02') {
                        script {
                            echo "Starting Behave tests for Desafio02"
                            echo "Current directory: ${pwd()}"
                            try {
                                bat '''
                                    echo Current directory: %CD%
                                    if not exist features\\reports mkdir features\\reports
                                    call %DESAFIO02_ENV%\\Scripts\\activate.bat
                                    echo Behave version:
                                    behave --version
                                    echo Running Behave tests
                                    behave -f pretty -f json -o features/reports/behave-report.json --junit --junit-directory features/reports
                                '''
                            } catch (Exception e) {
                                currentBuild.result = 'FAILURE'
                                error "Failed to run Behave tests for Desafio 02: ${e.message}"
                            }
                            echo "Finished Behave tests for Desafio02"
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "Archiving artifacts and test results"
                // Volvemos al directorio de trabajo principal
                dir("${WORKSPACE_DIR}") {
                    archiveArtifacts artifacts: 'Desafio01/features/reports/**/*.*,Desafio02/features/reports/**/*.*', allowEmptyArchive: true
                    junit testResults: 'Desafio01/features/reports/*.xml,Desafio02/features/reports/*.xml', allowEmptyResults: true
                }
            }
        }
    }
}
