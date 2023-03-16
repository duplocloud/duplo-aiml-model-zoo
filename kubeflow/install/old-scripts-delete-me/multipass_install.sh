sudo snap install  multipass


sudo  multipass find

sudo multipass launch jammy -n kubeflow --cpus 4 --disk 100G --memory 20G

sudo multipass list
sudo  multipass  delete feasible-skua
sudo  multipass  purge


sudo snap install multipass --beta --classic
wget https://bit.ly/2tOfMUA -O kubeflow.init
sudo multipass launch jammy -n kubeflow -m 20G -d 100G -c 4  



sudo multipass shell kubeflow













# Available commands:
#   alias         Create an alias
#   aliases       List available aliases
#   authenticate  Authenticate client
#   delete        Delete instances
#   exec          Run a command on an instance
#   find          Display available images to create instances from
#   get           Get a configuration setting
#   help          Display help about a command
#   info          Display information about instances
#   launch        Create and start an Ubuntu instance
#   list          List all available instances
#   mount         Mount a local directory in the instance
#   networks      List available network interfaces
#   purge         Purge all deleted instances permanently
#   recover       Recover deleted instances
#   restart       Restart instances
#   set           Set a configuration setting
#   shell         Open a shell on a running instance
#   start         Start instances
#   stop          Stop running instances
#   suspend       Suspend running instances
#   transfer      Transfer files between the host and instances
#   umount        Unmount a directory from an instance
#   unalias       Remove aliases
