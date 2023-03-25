source ./destroy-kubeflow.sh

microk8s_version=1.24
kubflow_version=1.6/stable #1.7/beta

microk8s_version=1.21
kubflow_version=1.5/stable

microk8s_version=1.24
kubflow_version=1.7/beta

# #failed
# microk8s_version=1.24
# kubflow_version=1.6/stable

#failed
microk8s_version=1.22
kubflow_version=1.6/stable

# sudo snap install microk8s --channel=1.21/stable --classic
# sudo snap refresh microk8s --channel=1.22/stable --classic
# sudo snap install microk8s --classic --channel=1.24/stable

sudo snap install microk8s --classic --channel=${microk8s_version}/stable

sudo snap install juju --classic

microk8s config > ~/.kube/config
microk8s kubectl -n kubeflow get all -A
microk8s enable rbac dns storage hostpath-storage metallb:10.64.140.43-10.64.140.49
microk8s enable dns storage
#
microk8s enable dns
microk8s enable storage
microk8s enable ingress
microk8s enable metallb:10.64.140.43-10.64.140.49
microk8s enable dashboard
microk8s enable istio

microk8s kubectl get pod  -n metallb-system 
# echo microk8s kubectl set image deployment/my-deployment mycontainer=myimage:1.9.1

# microk8s status
microk8s kubectl -n kubeflow get all -A
sleep 120
microk8s kubectl -n kubeflow get all -A
sleep 120
microk8s kubectl -n kubeflow get all -A 

juju bootstrap --quiet   microk8s uk8sx
sleep 120 
juju add-model kubeflow
# juju deploy kubeflow  --show-log --trust --channel=1.6/stable
# juju deploy kubeflow --channel 1.7/beta --trust  --show-log 
# juju deploy kubeflow --channel ${kubflow_version} --trust  --show-log
juju deploy kubeflow  --trust  --show-log

microk8s kubectl -n kubeflow get all -A 
microk8s kubectl -n kubeflow get pod -A | grep PodInitializing

for i in `seq 1 20`; do
 juju status; sleep 10;
 microk8s kubectl -n kubeflow get pod -A | grep PodInitializing
done

microk8s  kubectl patch role -n kubeflow istio-ingressgateway -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istio-ingressgateway"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
microk8s  kubectl patch role -n kubeflow istio-pilot -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istio-pilot"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
microk8s  kubectl patch role -n kubeflow istiod-kubeflow -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istiod-kubeflow"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
microk8s  kubectl patch role -n kubeflow istiod -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istiod"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
microk8s  kubectl patch role -n kubeflow istio-ingressgateway-workload-sds -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istio-ingressgateway-workload-sds"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
juju run --unit istio-pilot/0 -- "export JUJU_DISPATCH_PATH=hooks/config-changed; ./dispatch"

juju config dex-auth public-url=http://10.64.140.43.nip.io
juju config oidc-gatekeeper public-url=http://10.64.140.43.nip.io
juju config dex-auth static-username=admin
juju config dex-auth static-password=admin 
juju config dex-auth static-username
juju config dex-auth static-password

for i in `seq 1 20`; do
 juju status; sleep 10;
 microk8s kubectl -n kubeflow get pod -A | grep PodInitializing
done

microk8s  kubectl  -n  metallb-system  set image  deployment/controller  controller=bitnami/metallb-controller:0.9.6
microk8s kubectl  -n  metallb-system   set image  daemonset.apps/speaker    speaker=bitnami/metallb-speaker:0.9.6
mk -n metallb-system   get all 


microk8s  kubectl patch role -n kubeflow istio-ingressgateway -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istio-ingressgateway"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
microk8s  kubectl patch role -n kubeflow istio-pilot -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istio-pilot"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
microk8s  kubectl patch role -n kubeflow istiod-kubeflow -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istiod-kubeflow"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
microk8s  kubectl patch role -n kubeflow istiod -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istiod"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
microk8s  kubectl patch role -n kubeflow istio-ingressgateway-workload-sds -p '{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":{"name":"istio-ingressgateway-workload-sds"},"rules":[{"apiGroups":["*"],"resources":["*"],"verbs":["*"]}]}'
juju run --unit istio-pilot/0 -- "export JUJU_DISPATCH_PATH=hooks/config-changed; ./dispatch"


for i in `seq 1 20`; do
 juju status; sleep 10;
 microk8s kubectl -n kubeflow get pod -A | grep PodInitializing
done

# sudo reboot

while(true); do juju status; echo "---- sleep 10 -----n";microk8s kubectl -n kubeflow get pod -A | grep PodInitializing; sleep 10; done
#watch -c juju status

