pipeline {
    agent any
    stages {
        stage('Process Pull Request'){
            when {
                    changeRequest ()
                }
            steps {
                echo 'Processing PR'
            }
        }
        stage('Clone Repo - Feature') {
            when {
                    branch 'feature*'
            }
           
            steps {
                git branch: '${BRANCH_NAME}', credentialsId: 'gitHubCredentials', url: 'https://github.com/connectbaseer/tascaty_dev.git'
            }
        }
        stage('Build Image - Feature') {
            when {
                    branch 'feature*'
            }
           
            steps {
                sh 'docker version'
                sh 'docker build -t tascatyk8s .'
                sh 'docker image list'
                sh 'docker tag tascatyk8s abdul8423/tascatyk8s:V${BUILD_NUMBER}'
            }
        }
        stage('Clone Repo') {
            when {
                allOf { 
                    not { branch 'PR*' }
                    not { branch 'feature*' }
                }
            }
           
            steps {
                git branch: '${BRANCH_NAME}', credentialsId: 'gitHubCredentials', url: 'https://github.com/connectbaseer/tascaty_dev.git'
            }
        }
        stage('Build Image') {

            when {
                allOf { 
                    not { branch 'PR*' }
                    not { branch 'feature*' }
                }
            }
           
            steps {
                sh 'docker version'
                sh 'docker build -t tascatyk8s .'
                sh 'docker image list'
                sh 'docker tag tascatyk8s abdul8423/tascatyk8s:V${BUILD_NUMBER}'
            }
        }
        stage('Push  Image') {
            when {
                allOf { 
                    not { branch 'PR*' }
                    not { branch 'feature*' }
                }
            }
         
            steps {
                withCredentials([string(credentialsId: 'dockerHubPassword', variable: 'Password')]) {
                    sh 'docker login -u abdul8423 -p $Password'
                    sh 'docker push abdul8423/tascatyk8s:V${BUILD_NUMBER}'
                }
            }
        }

        stage('Set New Image') {
            when {
                allOf { 
                    not { branch 'PR*' }
                    not { branch 'feature*' }
                }
            }
          
            steps {
                script {
                    withCredentials([sshUserPrivateKey(
                credentialsId: 'tascatyk8s-dev-master',
                keyFileVariable: 'sshKey',
                usernameVariable: 'sshUser'
            )]) {
                        def remote = [:]
                        remote.name = 'tascatyk8s-dev-master'
                        remote.host = '192.168.50.11'
                        remote.user = sshUser
                        remote.identityFile = sshKey
                        remote.allowAnyHosts = true
                        env.SET_IMAGE = "kubectl set image deployment/tascatyk8s-app-deployment tascatyk8s-app=abdul8423/tascatyk8s:V${BUILD_NUMBER} --record=true --namespace=tascaty-app"
                        sshCommand remote: remote, command: "${SET_IMAGE}"
            }
                }
            }
        }

        stage('Test Web App'){
            when {
                allOf { 
                    not { branch 'PR*' }
                    not { branch 'feature*' }
                }
            }
            steps {
                sh 'curl http://192.168.50.11:32421/ -v'
            }
            
        }
        stage('DeploymentConfirmation'){
            when {
                beforeInput true
                allOf { 
                    not { branch 'PR*' }
                    not { branch 'feature*' }
                }
            }
            input {
                message "Deploy to Production?"
                ok "Yes, we should."
            }
            steps {
                echo 'Deploying Now'
            }
        }
        stage('Deploy to Production'){
            when {
                allOf { 
                    not { branch 'PR*' }
                    not { branch 'feature*' }
                }
            }
            steps {
                script {
                    withCredentials([sshUserPrivateKey(
                credentialsId: 'tascatyk8s-prod-master',
                keyFileVariable: 'sshKey',
                usernameVariable: 'sshUser'
            )]) {
                        def remote = [:]
                        remote.name = 'tascatyk8s-prod-master'
                        remote.host = '192.168.51.11'
                        remote.user = sshUser
                        remote.identityFile = sshKey
                        remote.allowAnyHosts = true
                        env.SET_IMAGE = "kubectl set image deployment/tascatyk8s-app-deployment tascatyk8s-app=abdul8423/tascatyk8s:V${BUILD_NUMBER} --record=true --namespace=tascaty-app"
                        sshCommand remote: remote, command: "${SET_IMAGE}"
            }
                }
            }

        }
    }
}
