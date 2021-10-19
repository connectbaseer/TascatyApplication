node{
    def commit_id
    if (env.BRANCH_NAME == 'feature'){
        stage('Check Feature and Test Build'){
            checkout scm
            def customImage = docker.build("abdul8423/tascaty")
            
        }
        
    }

    if (env.BRANCH_NAME == 'develop'){
        stage('Build And Push To Docker Hub') {
            checkout scm
            sh "git rev-parse --short HEAD > .git/commit-id"
            commit_id = readFile('.git/commit-id').trim()
            def customImage = docker.build("abdul8423/tascaty:${commit_id}")
            customImage.push()
        }

        stage('Set New Image On Dev Environment') {
            
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
                        env.SET_IMAGE = "kubectl set image deployment/tascatyk8s-app-deployment tascatyk8s-app=abdul8423/tascaty:${commit_id} --record=true --namespace=tascaty-app"
                        sshCommand remote: remote, command: "${SET_IMAGE}"
            }
        }

        stage('Test Deployment On Dev Environment') {
             sh 'curl http://192.168.50.11:32421/ -v'
        }

        stage('Deploy to Production ?') {
            input(message: 'Please Confirm to Deploy to Prodection')
        }

        stage('Set New Image On Production Environment') {
            
            withCredentials([sshUserPrivateKey(
                credentialsId: 'tascatyk8s-master',
                keyFileVariable: 'sshKey',
                usernameVariable: 'sshUser'
            )]) {
                        def remote = [:]
                        remote.name = 'tascatyk8s-master'
                        remote.host = '192.168.30.5'
                        remote.user = sshUser
                        remote.identityFile = sshKey
                        remote.allowAnyHosts = true
                        env.SET_IMAGE = "kubectl set image deployment/tascatyk8s-app-deployment tascatyk8s-app=abdul8423/tascaty:${commit_id} --record=true --namespace=tascaty-app"
                        sshCommand remote: remote, command: "${SET_IMAGE}"
            }
        }

    }

    if (BRANCH_NAME == 'feature' || BRANCH_NAME = 'develop'){
        stage('Clean WS'){
        sh './build_cleanup.sh'
        deleteDir()
    }
    }
    
}
