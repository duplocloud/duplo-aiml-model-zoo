

minikube delete --all

minikube config set memory 50000
minikube config set cpu 20
minikube delete --all
minikube stop 

sudo apt remove podman-docker




################
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# https://r2schools.com/how-to-install-minikube-on-ubuntu-22-04-lts/

sudo install minikube-linux-amd64 /usr/local/bin/minikube





minikube version

# sudo apt install podman-docker -y
# podman: Suggestion: Add your user to the 'sudoers' file: 
 # prav ALL=(ALL) NOPASSWD: /usr/bin/podman 
# or run 'minikube config set rootless true' <https://podman.io>


minikube config set rootless false

minikube delete --all

minikube config set memory 50000
minikube config set cpus 20
minikube delete --all
minikube stop
minikube start




# minikube config set memory 9001

# minikube start

# need docker or podman 
# minikube kubectl -- get po -A
#  minikube dashboard
# minikube pause  stop unpause
# minikube delete --all
# https://minikube.sigs.k8s.io/docs/start/

