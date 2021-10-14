node {

    if (env.BRANCH_NAME == 'PR*') {

        stage('This is Pull Request') {

            echo "this is ${env.BRANCH_NAME} Branch"
        }

    }

    if (env.BRANCH_NAME == 'feature*') {

        stage('This is Feature Branch') {

            echo "this is ${env.BRANCH_NAME} Branch name"
        }

    }
   
   

}










// node {
//        def commit_id
//         stage('Clone Repo') {
//                 checkout scm
//                 sh "git rev-parse --short HEAD > .git/commit-id"
//                 commit_id = readFile('.git/commit-id').trim()            
//         }
//         stage('Build Image') {
//             def customImage = docker.build("abdul8423/tascaty:${commit_id}")
//             customImage.push()
//         }

//         stage('Set New Image') {
            
//             withCredentials([sshUserPrivateKey(
//                 credentialsId: 'tascatyk8s-master',
//                 keyFileVariable: 'sshKey',
//                 usernameVariable: 'sshUser'
//             )]) {
//                         def remote = [:]
//                         remote.name = 'tascatyk8s-master'
//                         remote.host = '192.168.30.5'
//                         remote.user = sshUser
//                         remote.identityFile = sshKey
//                         remote.allowAnyHosts = true
//                         env.SET_IMAGE = "kubectl set image deployment/tascatyk8s-app-deployment tascatyk8s-app=abdul8423/tascaty:${commit_id} --record=true --namespace=tascaty-app"
//                         sshCommand remote: remote, command: "${SET_IMAGE}"
//             }
//         }
// }      
