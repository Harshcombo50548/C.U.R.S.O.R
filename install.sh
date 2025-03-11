#!/bin/bash

# Print colorful messages
print_message() {
    echo -e "\e[1;34m[CURSOR INSTALLER]\e[0m $1"
}

print_error() {
    echo -e "\e[1;31m[ERROR]\e[0m $1"
}

print_success() {
    echo -e "\e[1;32m[SUCCESS]\e[0m $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python3 is not installed. Installing Python3..."
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3 python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-pip
    elif command -v brew &> /dev/null; then
        brew install python3
    else
        print_error "Could not install Python3. Please install it manually."
        exit 1
    fi
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Installing pip3..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py --user
    rm get-pip.py
fi

# Install Chrome if not present
if ! command -v google-chrome &> /dev/null; then
    print_message "Installing Google Chrome..."
    if command -v apt &> /dev/null; then
        wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        sudo apt install -y ./google-chrome-stable_current_amd64.deb
        rm google-chrome-stable_current_amd64.deb
    elif command -v yum &> /dev/null; then
        sudo yum install -y https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install --cask google-chrome
    else
        print_error "Could not install Chrome. Please install it manually."
        exit 1
    fi
fi

# Create directory for CURSOR
print_message "Creating CURSOR directory..."
mkdir -p ~/CURSOR
cd ~/CURSOR

# Download the script from GitHub
print_message "Downloading CURSOR scripts..."
curl -L https://github.com/Harshcombo50548/C.U.R.S.O.R/archive/main.zip -o cursor.zip
unzip -o cursor.zip
rm cursor.zip
mv C.U.R.S.O.R-main/* .
rm -rf C.U.R.S.O.R-main

# Install Python dependencies
print_message "Installing Python dependencies..."
pip3 install --no-cache-dir selenium undetected-chromedriver pyyaml requests

# Make the script executable
chmod +x "Create account.py"

print_success "Installation completed successfully!"
print_message "You can now run the script using: python3 ~/CURSOR/Create\ account.py"

# Create an alias for easier access (optional)
if [[ -f ~/.bashrc ]]; then
    echo 'alias cursor="python3 ~/CURSOR/Create\ account.py"' >> ~/.bashrc
    print_message "Added alias 'cursor' to ~/.bashrc"
    print_message "Please run 'source ~/.bashrc' or restart your terminal to use the alias"
elif [[ -f ~/.zshrc ]]; then
    echo 'alias cursor="python3 ~/CURSOR/Create\ account.py"' >> ~/.zshrc
    print_message "Added alias 'cursor' to ~/.zshrc"
    print_message "Please run 'source ~/.zshrc' or restart your terminal to use the alias"
fi 