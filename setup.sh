#                                     WELCOME TO
#
#  .d8888b.      888     888     8888888b.       .d8888b.       .d88888b.      8888888b.  
# d88P  Y88b     888     888     888   Y88b     d88P  Y88b     d88P" "Y88b     888   Y88b 
# 888    888     888     888     888    888     Y88b.          888     888     888    888 
# 888            888     888     888   d88P      "Y888b.       888     888     888   d88P 
# 888            888     888     8888888P"          "Y88b.     888     888     8888888P"  
# 888    888     888     888     888 T88b             "888     888     888     888 T88b   
# Y88b  d88P d8b Y88b. .d88P d8b 888  T88b  d8b Y88b  d88P d8b Y88b. .d88P d8b 888  T88b  
#  "Y8888P"  Y8P  "Y88888P"  Y8P 888   T88b Y8P  "Y8888P"  Y8P  "Y88888P"  Y8P 888   T88b 
#
#        {Creating User Registrations with Scripted Optimization and Replication}
#
#!/bin/bash

sudo apt update
sudo apt install -y python3 python3-pip python3-venv

pip3 install -r requirements.txt --break-system-packages

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f -y

rm google-chrome-stable_current_amd64.deb

echo "Setup completed successfully!"