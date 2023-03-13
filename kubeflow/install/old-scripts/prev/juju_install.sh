
# juju (the Juju CLI, the Juju client)
# juju help
# juju commands
sudo snap remove juju  

###############################3

sudo snap install juju --classic

juju bootstrap microk8s

juju add-model kubeflow


# juju switch controller
# juju deploy juju-dashboard
# juju integrate juju-dashboard controller
# juju expose juju-dashboard
# juju dashboard


# juju bootstrap aws aws-controller
juju controllers
# juju show-controller localhost-controller
# juju switch localhost-controller-prod

