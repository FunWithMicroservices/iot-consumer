sudo apt-get update

# Docker setup
sudo apt install docker.io -y

# Post installation
# There is a warning: https://docs.docker.com/engine/install/linux-postinstall/
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

# Docker Compose
sudo apt  install docker-compose -y

# Firewall settings
sudo ufw allow OpenSSH
echo "y" | sudo ufw enable
sudo ufw allow 8086
