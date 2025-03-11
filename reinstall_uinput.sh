#!/bin/bash

# Make sure development packages are installed
sudo apt-get update
sudo apt-get install -y python3-dev libudev-dev

# Uninstall current possibly broken installation
sudo pip3 uninstall -y python-uinput

# Install from source with proper compilation
git clone https://github.com/tuomasjjrasanen/python-uinput.git
cd python-uinput
sudo python3 setup.py install
cd ..
rm -rf python-uinput

# Verify installation
python3 -c "import uinput; print('uinput successfully imported')" 