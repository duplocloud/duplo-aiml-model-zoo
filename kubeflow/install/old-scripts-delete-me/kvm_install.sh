# https://www.asus.com/us/support/FAQ/1045141/

egrep -c '(vmx|svm)' /proc/cpuinfo

sudo apt install qemu-kvm libvirt-daemon-system virtinst libvirt-clients bridge-utils
 
sudo apt install qemu qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager

sudo systemctl enable --now libvirtd

sudo systemctl enable --now virtlogd
 
echo 1 | sudo tee /sys/module/kvm/parameters/ignore_msrs



sudo modprobe kvm

sudo systemctl enable libvirtd
sudo systemctl start libvirtd
sudo systemctl status libvirtd

sudo usermod -aG kvm $USER
sudo usermod -aG libvirt $USER
sudo nano /etc/netplan/01-netcfg.yaml
# https://linuxhint.com/install-kvm-ubuntu-22-04/

sudo netplan apply
ip addr show



sudo vi /etc/modules
# Add these lines to /etc/modules file so that these modules load on reboot:
# kvm
# kvm-amd

lsmod | grep kvm

# enable bois