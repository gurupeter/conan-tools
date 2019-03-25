pipeline {
  agent { label 'ubuntu-18.04' }

  options {
    checkoutToSubdirectory('src')
  }

  environment {
    CONAN_USER_HOME = "${env.WORKSPACE}"
    REMOTE = "${env.CONAN_REMOTE}"
    USER = 'includeos'
    CHAN = 'default'
    BINTRAY_CREDS = credentials('devops-includeos-user-pass-bintray')
    SRC = "${env.WORKSPACE}/src"
  }

  stages {
    stage('Conan channel') {
      parallel {
        stage('Pull request') {
          when { changeRequest() }
          steps { script { CHAN = 'test' } }
        }
        stage('Master merge') {
          when { branch 'master' }
          steps { script { CHAN = 'latest' } }
        }
        stage('Stable release') {
          when { buildingTag() }
          steps { script { CHAN = 'stable' } }
        }
      }
    }
    stage('Setup') {
      steps {
        sh script: "ls -A | grep -v src | xargs rm -r || :", label: "Clean workspace"
        sh script: "conan config install https://github.com/includeos/conan_config.git", label: "conan config install"
      }
    }
    stage('Export') {
      steps {
        sh script: "conan export $SRC $USER/$CHAN", label: "Export conan package"
      }
    }
    stage('Upload to bintray') {
      when {
        anyOf {
          branch 'master'
          buildingTag()
        }
      }
      steps {
        script {
          sh script: "conan user -p $BINTRAY_CREDS_PSW -r $REMOTE $BINTRAY_CREDS_USR", label: "Login to bintray"
          def version = sh (
            script: "conan inspect -a version $SRC | cut -d ' ' -f 2",
            returnStdout: true
          ).trim()
          sh script: "conan upload --all -r $REMOTE conan-tools/${version}@$USER/$CHAN", label: "Upload conan-tools to bintray"
        }
      }
    }
  }
}
