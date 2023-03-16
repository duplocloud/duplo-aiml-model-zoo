# https://towardsdatascience.com/kubeflow-how-to-install-and-launch-kubeflow-on-your-local-machine-e0d7b4f7508f

PLATFORM=$(uname)
export PLATFORM
mkdir -p ~/bin
export KF_TAG=1.0.1
KF_BASE="https://api.github.com/repos/kubeflow/kfctl/releases"

 
KFCTL_URL=$(curl -s ${KF_BASE} |\
      grep http |\
      grep "${KF_TAG}" |\
      grep -i "${PLATFORM}" |\
      cut -d : -f 2,3 |\
      tr -d '\" ' )
wget "${KFCTL_URL}"
KFCTL_FILE=${KFCTL_URL##*/}
tar -xvf "${KFCTL_FILE}"
mv ./kfctl ~/bin/

# rm "${KFCTL_FILE}"
export PATH=$PATH:~/bin


~/bin/kfctl version



####################################
MANIFEST_BRANCH=${MANIFEST_BRANCH:-v1.2-branch}
export MANIFEST_BRANCH
MANIFEST_VERSION=${MANIFEST_VERSION:-v1.2.0}
export MANIFEST_VERSION


KF_PROJECT_NAME=${KF_PROJECT_NAME:-hello-kf-${PLATFORM}}
export KF_PROJECT_NAME
mkdir -p "${KF_PROJECT_NAME}"
pushd  "${KF_PROJECT_NAME}"

manifest_root=https://raw.githubusercontent.com/kubeflow/manifests
FILE_NAME=kfctl_k8s_istio.${MANIFEST_VERSION}.yaml
KFDEF=${manifest_root}${MANIFEST_BRANCH}/kfdef/${FILE_NAME}

sudo  ~/bin/kfctl apply -f $KFDEF -V

cd ..



  
  
  
  

 
