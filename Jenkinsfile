pipeline {
    agent any
    stages {

        stage('Clone Repo') {

            steps {
                git credentialsId: 'gitHubCredentials', url: 'https://github.com/connectbaseer/TascatyApplication.git'
            }
        }
        stage('Build Image') {

            steps {
                sh 'docker version'
                sh 'docker build -t tascaty .'
                sh 'docker image list'
                sh 'docker tag tascaty abdul8423/tascaty:V${BUILD_NUMBER}'
            }
        }
        stage('Push  Image') {

            steps {
                withCredentials([string(credentialsId: 'dockerHubPassword', variable: 'Password')]) {
                    sh 'docker login -u abdul8423 -p $Password'
                    sh 'docker push abdul8423/tascaty:V${BUILD_NUMBER}'
                }
            }
        }

        stage('Set New Image') {

            steps {
                script {
                    withCredentials([sshUserPrivateKey(
                credentialsId: 'tascatyk8s-dev-master',
                keyFileVariable: 'sshKey',
                usernameVariable: 'sshUser'
            )]) {
                        def remote = [:]
                        remote.name = 'tascatyk8s-master'
                        remote.host = '192.168.30.5'
                        remote.user = sshUser
                        remote.identityFile = sshKey
                        remote.allowAnyHosts = true
                        env.SET_IMAGE = "kubectl set image deployment/tascatyk8s-app-deployment tascatyk8s-app=abdul8423/tascaty:V${BUILD_NUMBER} --record=true --namespace=tascaty-app"
                        sshCommand remote: remote, command: "${SET_IMAGE}"
            }
                }
            }
        }

    }
}
