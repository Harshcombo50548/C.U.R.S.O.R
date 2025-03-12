#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

clear

# Terminal setup
echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║          C.U.R.S.O.R Setup             ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════╝${NC}"

read -p "Resize terminal now? (recommended 100+ cols) [y/N]: " resize
[[ "$resize" =~ ^[yY]$ ]] && read -p "Resize then press Enter..."

clear

# Check requirements
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 required! Install first.${NC}"
    exit 1
fi

# System updates
echo -e "${GREEN}Updating packages...${NC}"
sudo apt update

# Install base packages
echo -e "${GREEN}Installing system dependencies...${NC}"
sudo apt install -y python3-selenium python3-requests python3-yaml python3-pip

# Python libraries
echo -e "${GREEN}Installing Python components...${NC}"
pip3 install selenium-stealth webdriver-manager python-uinput \
python-xlib undetected-chromedriver chromedriver-manager --break-system-packages

# Final check
if [ $? -eq 0 ]; then
    echo -e "${GREEN}All set! Run with: python3 account_creation.py${NC}"
else
    echo -e "${RED}Installation failed!${NC}"
    exit 1
fi 
