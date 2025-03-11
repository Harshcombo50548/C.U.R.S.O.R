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


# Function to check if a command succeeded
check_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed"
        exit 1
    fi
}

# Check if script is run with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo ./setup.sh)"
    exit 1
fi

# Store the actual username (not root)
ACTUAL_USER=$SUDO_USER
if [ -z "$ACTUAL_USER" ]; then
    echo "This script must be run with sudo"
    exit 1
fi

echo "Starting setup..."

# Add Chrome repository and key
echo "Setting up Chrome repository..."
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
check_status "Chrome repository setup"

# Download Chrome directly as backup method
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
check_status "Chrome download"

# 1. Install system packages
echo "Installing system packages..."
apt-get update
check_status "apt-get update"

# Install all required system packages
apt-get install -y \
    python3-dev \
    libudev-dev \
    python3-xlib \
    python3-pip \
    google-chrome-stable \
    build-essential \
    xdotool \
    x11-utils \
    x11-xserver-utils \
    python3-tk \
    python3-setuptools \
    gcc \
    pkg-config \
    libx11-dev \
    wget \
    gnupg2 \
    python3-uinput
check_status "package installation"

# Try installing Chrome from the downloaded deb as backup
dpkg -i google-chrome-stable_current_amd64.deb || true
apt-get install -f -y
rm google-chrome-stable_current_amd64.deb

# Create requirements.txt
cat > requirements.txt << EOF
selenium==4.11.2
selenium-stealth==1.0.6
webdriver-manager==4.0.1
requests==2.31.0
pyyaml==6.0.1
python-xlib==0.33
python-uinput==0.11.2
EOF

# Install Python packages system-wide
echo "Installing Python packages..."
pip3 install --break-system-packages -r requirements.txt
check_status "Python package installation"

# 2. Enable uinput kernel module
echo "Configuring uinput kernel module..."
modprobe uinput
check_status "modprobe uinput"
echo "uinput" > /etc/modules-load.d/uinput.conf
check_status "uinput module configuration"

# 3. Create udev rule for uinput permissions
echo "Setting up udev rules..."
echo 'KERNEL=="uinput", GROUP="input", MODE="0660"' > /etc/udev/rules.d/99-input.rules
check_status "udev rules creation"

# 4. Add user to input and required groups
echo "Adding user to required groups..."
usermod -a -G input,video,plugdev $ACTUAL_USER
check_status "user group modification"

# 5. Reload udev rules
echo "Reloading udev rules..."
udevadm control --reload-rules
udevadm trigger
check_status "udev rules reload"

# 6. Set immediate permissions
chmod 666 /dev/uinput
check_status "uinput permissions"

# Create a script to run after reboot
AFTER_REBOOT_SCRIPT="/home/$ACTUAL_USER/after_reboot_setup.sh"
cat > "$AFTER_REBOOT_SCRIPT" << EOF
#!/bin/bash

# Verify uinput is working
if ! lsmod | grep -q uinput; then
    echo "Error: uinput module not loaded!"
    exit 1
fi

if [ ! -c /dev/uinput ]; then
    echo "Error: /dev/uinput device not found!"
    exit 1
fi

# Set permissions again just to be sure
sudo chmod 666 /dev/uinput

# Add udev rule again just to be sure
sudo sh -c 'echo "KERNEL==\"uinput\", GROUP=\"input\", MODE=\"0660\"" > /etc/udev/rules.d/99-input.rules'
sudo udevadm control --reload-rules
sudo udevadm trigger

# Verify groups
if ! groups \$USER | grep -q input; then
    echo "Warning: User not in input group. Adding now..."
    sudo usermod -a -G input \$USER
fi

# Verify Chrome installation
if ! which google-chrome > /dev/null; then
    echo "Warning: Chrome not found, attempting to reinstall..."
    sudo apt-get update
    sudo apt-get install -y google-chrome-stable
fi

echo "Setup completed successfully!"
echo "To run the script, use:"
echo "sudo -E python3 cursor_signup.py"

# Test uinput access
if python3 -c "import uinput" 2>/dev/null; then
    echo "uinput module test: SUCCESS"
else
    echo "Warning: uinput module test failed. You may need to log out and log back in."
fi

# Test selenium
if python3 -c "from selenium import webdriver" 2>/dev/null; then
    echo "selenium test: SUCCESS"
else
    echo "Warning: selenium not properly installed"
fi
EOF

# Make the after-reboot script executable and owned by the user
chmod +x "$AFTER_REBOOT_SCRIPT"
chown $ACTUAL_USER:$ACTUAL_USER "$AFTER_REBOOT_SCRIPT"

# Add the after-reboot script to user's .profile to run on next login
PROFILE_FILE="/home/$ACTUAL_USER/.profile"
echo "if [ -f ~/after_reboot_setup.sh ]; then" >> "$PROFILE_FILE"
echo "    ~/after_reboot_setup.sh" >> "$PROFILE_FILE"
echo "    rm ~/after_reboot_setup.sh" >> "$PROFILE_FILE"
echo "fi" >> "$PROFILE_FILE"

echo "Initial setup complete. System will reboot in 3 seconds..."
echo "After reboot, log in normally and the setup will complete automatically."

# Sleep for 3 seconds then reboot
sleep 3
reboot

# Check if Python development headers are installed
echo "Checking for Python development headers..."
dpkg -l | grep python3-dev > /dev/null
if [ $? -ne 0 ]; then
    echo "Python development headers not found. Installing..."
    apt-get install -y python3-dev
    check_status "Python development headers installation"
else
    echo "Python development headers are already installed."
fi