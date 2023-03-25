juju destroy-model kubeflow --yes --destroy-storage --force
juju destroy-model kubeflow --release-storage
juju destroy-controller  uk8sx --quiet 
#microk8s reset
microk8s stop

sudo update-rc.d juju remove  #--quiet
sudo update-rc.d juju-jon-sample-machine-agent remove #--quiet
sudo update-rc.d juju-jon-sample-file-storage remove #--quiet

sudo snap remove microk8s --purge 
sudo snap remove juju --purge
rm  -rf ~/.local/share/juju
rm -rf ~/.kube