sudo /usr/local/bin/k3s-killall.sh

sudo /usr/local/bin/k3s-uninstall.sh

##############
# sudo  k3s server
curl -sfL https://get.k3s.io | sh - 
# Check for Ready node, takes ~30 seconds 
sudo k3s kubectl get node 
