export KF_NAME=kubeflow-easy-deploy
export BASE_DIR=${HOME}
export KF_DIR=${BASE_DIR}/${KF_NAME}
cd ${KF_DIR}
kfctl delete -f ${CONFIG_FILE}

#######################
cd
git clone https://github.com/sachua/kubeflow-easy-deploy.git

bash $HOME/kubeflow-easy-deploy/pull_images.sh
bash $HOME/kubeflow-easy-deploy/push_images.sh

export KF_NAME=kubeflow-easy-deploy
export BASE_DIR=${HOME}
export KF_DIR=${BASE_DIR}/${KF_NAME}
cd ${KF_DIR}
tar -xvf kfctl.tar.gz
export PATH=$PATH:"${KF_DIR}"


export CONFIG_FILE=${KF_DIR}/kfctl_k8s_istio.v1.0.2.yaml
kfctl apply -V -f ${CONFIG_FILE}

# Username: admin@kubeflow.org
# assword: 12341234
