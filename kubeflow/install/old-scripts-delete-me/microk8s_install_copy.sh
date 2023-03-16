# https://microk8s.io/docs/command-reference
# https://openebs.io/docs/user-guides/localpv-hostpath
# https://hackmd.io/@k402xxxcenxxx/HkooUL43v

# https://charmed-kubeflow.io/docs/dashboard

Password1234
############################################################
juju destroy-model kubeflow --yes --destroy-storage --force
juju destroy-model kubeflow --release-storage
juju destroy-controller microk8s-localhost
microk8s reset
microk8s stop

sudo update-rc.d juju remove
sudo update-rc.d juju-jon-sample-machine-agent remove
sudo update-rc.d juju-jon-sample-file-storage remove
sudo snap remove microk8s --purge 
sudo snap remove juju --purge
rm  -rf ~/.local/share/juju
rm -rf ~/.kube
############################################################


# sudo snap install microk8s --classic --channel=1.22/stable
# sudo snap install microk8s --classic --channel=1.24/stable
# sudo snap install microk8s --classic --channel=1.20/stable
############################################################

sudo snap install juju --classic 
sudo snap install microk8s  --classic --channel=1.22/stable
sudo snap install microk8s --classic --channel=1.21/stable
sudo snap install kubectl --classic
# juju (2.9/stable) 2.9.42 from Canonical✓ installed
# microk8s (1.22/stable) v1.22.17 from Canonical✓ installed

sudo apt -y install open-iscsi
sudo systemctl enable iscsid

sudo usermod -a -G microk8s $USER 
newgrp microk8s 
rm -rf ~/.kube
mkdir -p ~/.kube
sudo chown -f -R $USER ~/.kube

microk8s enable  gpu dns dashboard storage ingress metallb:10.64.140.43-10.64.140.49
# microk8s enable hostpath-storage dns dashboard storage ingress metallb:10.64.140.43-10.64.140.49
sleep 120 # enable takes time
microk8s status --wait-ready
# Added 'kubeflow' model on microk8s/localhost with credential 'microk8s' for user 'admin'
juju bootstrap microk8s 
juju add-model kubeflow 
juju deploy kubeflow --trust --show-logs

# https://v1-5-branch.kubeflow.org/docs/distributions/charmed/install-kubeflow/
# juju deploy kubeflow --trust  --channel=1.6/stable 

microk8s kubectl patch role -n kubeflow istio-ingressgateway-workload-sds -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istio-ingressgateway-workload-sds"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
microk8s kubectl patch role -n kubeflow istio-ingressgateway-operator -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istio-ingressgateway-operator"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
juju run --unit istio-pilot/0 -- "export JUJU_DISPATCH_PATH=hooks/config-changed; ./dispatch"

########################################

watch -c juju status --color
juju status --color
microk8s kubectl -n kubeflow get all -A  | grep istio
# # https://github.com/istio/istio/issues/5056
# microk8s kubectl patch role -n kubeflow istio-ingressgateway-workload-sds -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istio-ingressgateway-workload-sds"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
# #
# kubectl patch role -n kubeflow istio-ingressgateway-operator -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istio-ingressgateway-operator"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
# juju run --unit istio-pilot/0 -- "export JUJU_DISPATCH_PATH=hooks/config-changed; ./dispatch"
########################################
microk8s kubectl get gateway -A
microk8s kubectl get pod -n kubeflow -o wide
microk8s kubectl get gateway -n kubeflow kubeflow-gateway -o yaml
microk8s kubectl logs -f -n kubeflow istio-ingressgateway-0 --tail=2
microk8s kubectl get svc -n kubeflow istio-ingressgateway -o jsonpath='{.metadata.labels}'
microk8s kubectl get pod -n kubeflow istio-ingressgateway-0 -o jsonpath='{.metadata.labels}'
microk8s kubectl get pod -n kubeflow istio-ingressgateway-workload-89ff56576-qjsnj  -o jsonpath='{.metadata.labels}'


curl http://10.64.140.43.nip.io


# microk8s.enable kubeflow
# microk8s.enable dns storage dashboard

# sudo snap refresh microk8s --channel=1.21/stable --classic 
# microk8s status --wait-ready

microk8s kubectl -n kubeflow get svc istio-ingressgateway-workload -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

juju config dex-auth public-url=http://10.64.140.43.nip.io
juju config oidc-gatekeeper public-url=http://10.64.140.43.nip.io

microk8s kubectl -n kubeflow get svc istio-ingressgateway-workload -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

juju config dex-auth static-username=admin
juju config dex-auth static-password=admin


juju config dex-auth static-username
juju config dex-auth static-password


# http://10.64.140.43.nip.io

###############################################
  
# stop juju-jon-sample-file-storage
# sudo rm /etc/init/juju-jon-sample-file-storage.

# juju unregister -y microk8s-localhost
# juju unregister -y microk8s-localhost
 
###########

# Hard reinstall of clients


# Hard re-install of controllers or machines needs a bit more
# Gladly juju leaves a helper to do so
$ sudo /usr/sbin/remove-juju-services

###########
sudo microk8s stop
sudo microk8s reset
sudo snap remove --purge  juju 
sudo snap remove --purge microk8s  

sudo apt-get remove juju  microk8s
sudo apt-get purge juju microk8s
sudo apt-get autoremove
rm  -rf ~/.local/share/juju

#####################


sudo snap install juju --classic

juju bootstrap microk8s
    
# su - $USER
microk8s enable istio
microk8s enable gpu
microk8s enable openebs
microk8s enable hostpath-storage
microk8s enable dashboard

microk8s start
microk8s status
microk8s status --wait-ready

microk8s kubectl get nodes

alias kubectl='microk8s kubectl'
#echo vm.nr_hugepages = 1024 | sudo tee -a /etc/sysctl.d/20-microk8s-hugepages.conf


microk8s enable istio
microk8s enable gpu
microk8s enable openebs
microk8s enable hostpath-storage
microk8s enable dashboard

microk8s enable dns
microk8s enable community
microk8s enable mayastor
microk8s enable minio
microk8s enable observability
microk8s enable prometheus
microk8s enable ingress
microk8s enable argocd
microk8s enable portainer

# https://microk8s.io/docs/command-reference
# microk8s cilium
# microk8s helm
# microk8s istioctl
# microk8s linkerd

# ddons:
#   enabled:
#     community            # (core) The community addons repository
#     dashboard            # (core) The Kubernetes dashboard
#     dns                  # (core) CoreDNS
#     ha-cluster           # (core) Configure high availability on the current node
#     helm                 # (core) Helm - the package manager for Kubernetes
#     helm3                # (core) Helm 3 - the package manager for Kubernetes
#     hostpath-storage     # (core) Storage class; allocates storage from host directory
#     metrics-server       # (core) K8s Metrics Server for API access to service metrics
#     minio                # (core) MinIO object storage
#     observability        # (core) A lightweight observability stack for logs, traces and metrics
#     storage              # (core) Alias to hostpath-storage add-on, deprecated
#   disabled:
#     argocd               # (community) Argo CD is a declarative continuous deployment for Kubernetes.
#     cilium               # (community) SDN, fast with full network policy
#     dashboard-ingress    # (community) Ingress definition for Kubernetes dashboard
#     fluentd              # (community) Elasticsearch-Fluentd-Kibana logging and monitoring
#     gopaddle-lite        # (community) Cheapest, fastest and simplest way to modernize your applications
#     inaccel              # (community) Simplifying FPGA management in Kubernetes
#     istio                # (community) Core Istio service mesh services
#     jaeger               # (community) Kubernetes Jaeger operator with its simple config
#     kata                 # (community) Kata Containers is a secure runtime with lightweight VMS
#     keda                 # (community) Kubernetes-based Event Driven Autoscaling
#     knative              # (community) Knative Serverless and Event Driven Applications
#     kwasm                # (community) WebAssembly support for WasmEdge (Docker Wasm) and Spin (Azure AKS WASI)
#     linkerd              # (community) Linkerd is a service mesh for Kubernetes and other frameworks
#     multus               # (community) Multus CNI enables attaching multiple network interfaces to pods
#     nfs                  # (community) NFS Server Provisioner
#     ondat                # (community) Ondat is a software-defined, cloud native storage platform for Kubernetes.
#     openebs              # (community) OpenEBS is the open-source storage solution for Kubernetes
#     openfaas             # (community) OpenFaaS serverless framework
#     osm-edge             # (community) osm-edge is a lightweight SMI compatible service mesh for the edge-computing.
#     portainer            # (community) Portainer UI for your Kubernetes cluster
#     sosivio              # (community) Kubernetes Predictive Troubleshooting, Observability, and Resource Optimization
#     traefik              # (community) traefik Ingress controller
#     trivy                # (community) Kubernetes-native security scanner
#     cert-manager         # (core) Cloud native certificate management
#     gpu                  # (core) Automatic enablement of Nvidia CUDA
#     host-access          # (core) Allow Pods connecting to Host services smoothly
#     ingress              # (core) Ingress controller for external access
#     kube-ovn             # (core) An advanced network fabric for Kubernetes
#     mayastor             # (core) OpenEBS MayaStor
#     metallb              # (core) Loadbalancer for your Kubernetes cluster
#     prometheus           # (core) Prometheus operator for monitoring and logging
#     rbac                 # (core) Role-Based Access Control for authorisation
#     registry             # (core) Private image registry exposed on localhost:32000  


microk8s kubectl get pods -A
microk8s config


# microk8s reset
# microk8s start
# microk8s status
# microk8s stop

# https://charmed-kubeflow.io/docs/get-started-with-charmed-kubeflow#heading--install-and-prepare-microk8s-


sudo ssh -L 9000:localhost:3000 \ 
    -i /var/snap/multipass/common/data/multipassd/ssh-keys/id_rsa \
    ubuntu@kubeflow