#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Clear the screen
clear

# Function to check terminal size
check_terminal_size() {
    if command -v tput > /dev/null 2>&1; then
        TERM_WIDTH=$(tput cols)
    else
        read -r _ TERM_WIDTH < <(stty size)
    fi
    echo "$TERM_WIDTH"
}

# Initial terminal setup prompt
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                   Welcome to C.U.R.S.O.R Setup                 ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo
echo -e "${YELLOW}For the best experience, please make your terminal wider.${NC}"
echo -e "${YELLOW}Current terminal width: $(check_terminal_size) columns${NC}"
echo -e "${YELLOW}Recommended width: 100 columns or more${NC}"
echo
echo -e "${GREEN}Would you like to resize your terminal now? (y/n)${NC}"
read -r resize_response

if [[ "$resize_response" =~ ^[yY]$ ]]; then
    echo
    echo -e "${BLUE}Please resize your terminal window now...${NC}"
    echo -e "${BLUE}Once you've adjusted the size, press Enter to continue.${NC}"
    read -r
    
    # Check new size
    NEW_WIDTH=$(check_terminal_size)
    echo -e "${GREEN}New terminal width: $NEW_WIDTH columns${NC}"
    sleep 1
fi

# Clear screen before starting the actual installation
clear

# Prepare tools for beautiful ASCII display
prepare_visual_enhancements() {
    echo -e "${BLUE}Preparing visual enhancements...${NC}"
    
    # Check if lolcat is installed (for rainbow effect)
    if ! command -v lolcat &> /dev/null; then
        echo -e "${BLUE}Installing lolcat for beautiful rainbow effects...${NC}"
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if command -v apt &> /dev/null; then
                # Debian/Ubuntu
                sudo apt update
                sudo apt install -y lolcat
            elif command -v dnf &> /dev/null; then
                # Fedora
                sudo dnf install -y lolcat
            elif command -v yum &> /dev/null; then
                # CentOS/RHEL
                sudo yum install -y lolcat
            elif command -v ruby &> /dev/null || command -v gem &> /dev/null; then
                # Ruby/gem is available
                sudo gem install lolcat
            else
                echo -e "${YELLOW}Could not install lolcat automatically. Continuing without enhanced visuals.${NC}"
            fi
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command -v brew &> /dev/null; then
                brew install lolcat
            elif command -v ruby &> /dev/null || command -v gem &> /dev/null; then
                sudo gem install lolcat
            else
                echo -e "${YELLOW}Could not install lolcat automatically. Continuing without enhanced visuals.${NC}"
            fi
        fi
    fi
    
    clear
}

# Display banner text in an awesome way
display_banner_text() {
    text="$1"
    
    if command -v lolcat &> /dev/null; then
        echo "$text" | lolcat -a -d 1 -s 150
    else
        echo -e "${MAGENTA}$text${NC}"
    fi
}

# Get terminal dimensions (silently)
get_terminal_size() {
    if command -v tput > /dev/null 2>&1; then
        TERM_WIDTH=$(tput cols)
        TERM_HEIGHT=$(tput lines)
    else
        # Fallback method
        read -r TERM_HEIGHT TERM_WIDTH < <(stty size)
    fi
}

# Animation function
animate_text() {
    text=$1
    speed=${2:-0.01}  # Default speed 0.01s, can be overridden
    for ((i=0; i<${#text}; i++)); do
        echo -n "${text:$i:1}"
        sleep $speed
    done
    echo
}

# Better ASCII art display considering terminal width
display_ascii_art() {
    get_terminal_size
    
    # Create the cursor.txt content
    cat << "EOF" > /tmp/cursor.txt
                                     WELCOME TO
 .d8888b.      888     888     8888888b.       .d8888b.       .d88888b.      8888888b.  
d88P  Y88b     888     888     888   Y88b     d88P  Y88b     d88P" "Y88b     888   Y88b 
888    888     888     888     888    888     Y88b.          888     888     888    888 
888            888     888     888   d88P      "Y888b.       888     888     888   d88P 
888            888     888     8888888P"          "Y88b.     888     888     8888888P"  
888    888     888     888     888 T88b             "888     888     888     888 T88b   
Y88b  d88P d8b Y88b. .d88P d8b 888  T88b  d8b Y88b  d88P d8b Y88b. .d88P d8b 888  T88b  
 "Y8888P"  Y8P  "Y88888P"  Y8P 888   T88b Y8P  "Y8888P"  Y8P  "Y88888P"  Y8P 888   T88b

     {Creating User Registrations with Scripted Optimization and Replication}
EOF
    
    # Display the ASCII art with proper formatting
    if command -v lolcat &> /dev/null; then
        # If lolcat is available, use it for a beautiful rainbow effect
        cat /tmp/cursor.txt | lolcat -a -d 1
    else
        # Otherwise, display with normal color
        while IFS= read -r line; do
            # Center the line in terminal if possible
            if [ "${#line}" -lt "$TERM_WIDTH" ]; then
                padding=$(( (TERM_WIDTH - ${#line}) / 2 ))
                printf "%${padding}s%s\n" "" "${CYAN}$line${NC}"
            else
                echo -e "${CYAN}$line${NC}"
            fi
            sleep 0.03
        done < /tmp/cursor.txt
    fi
    
    # Clean up temp file
    rm -f /tmp/cursor.txt
}

# Main script execution starts here
prepare_visual_enhancements

# Display the ASCII art
display_ascii_art
sleep 0.5

# Introduction message with proper colors
echo
display_banner_text "Welcome to the C.U.R.S.O.R Installer!"
sleep 0.3
echo
echo -e "${GREEN}This script will install all necessary dependencies and set up the C.U.R.S.O.R tool on your system.${NC}"
echo

# Ask for confirmation
echo -e "${YELLOW}Do you want to continue with the installation? (y/n)${NC}"
read -r response
if [[ ! "$response" =~ ^[yY]$ ]]; then
    echo -e "${RED}Installation aborted.${NC}"
    exit 1
fi

echo
animate_text "${GREEN}Starting installation...${NC}" 0.02
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

echo -e "${BLUE}Checking Python version...${NC}"
python_version=$(python3 --version)
echo -e "${GREEN}$python_version detected${NC}"

# Create directory for the project
echo -e "${BLUE}Creating project directory...${NC}"
mkdir -p ~/C.U.R.S.O.R
cd ~/C.U.R.S.O.R

# Clone the repository
echo -e "${BLUE}Cloning the repository...${NC}"
git clone https://github.com/Harshcombo50548/C.U.R.S.O.R.git .

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to clone the repository. Please check your internet connection and try again.${NC}"
    exit 1
fi

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip3 install selenium undetected-chromedriver pyyaml requests

# Check if Chrome is installed
if ! command -v google-chrome &> /dev/null && ! command -v google-chrome-stable &> /dev/null; then
    echo -e "${YELLOW}Google Chrome is required but not detected.${NC}"
    echo -e "${YELLOW}Would you like to install Google Chrome? (y/n)${NC}"
    read -r chrome_response
    if [[ "$chrome_response" =~ ^[yY]$ ]]; then
        # Detect OS and install Chrome
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if command -v apt &> /dev/null; then
                # Debian/Ubuntu
                echo -e "${BLUE}Installing Chrome on Debian/Ubuntu...${NC}"
                wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
                echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
                sudo apt update
                sudo apt install -y google-chrome-stable
            elif command -v dnf &> /dev/null; then
                # Fedora
                echo -e "${BLUE}Installing Chrome on Fedora...${NC}"
                sudo dnf install -y google-chrome-stable
            elif command -v yum &> /dev/null; then
                # CentOS/RHEL
                echo -e "${BLUE}Installing Chrome on CentOS/RHEL...${NC}"
                sudo yum install -y google-chrome-stable
            else
                echo -e "${RED}Unsupported Linux distribution. Please install Google Chrome manually.${NC}"
            fi
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            echo -e "${BLUE}Installing Chrome on macOS...${NC}"
            brew install --cask google-chrome
        else
            echo -e "${RED}Unsupported operating system. Please install Google Chrome manually.${NC}"
        fi
    else
        echo -e "${YELLOW}Skipping Chrome installation. Please install it manually to use C.U.R.S.O.R.${NC}"
    fi
fi

# Create a simple launcher script
echo -e "${BLUE}Creating launcher script...${NC}"
cat > ~/cursor-launcher.sh << 'EOF'
#!/bin/bash
cd ~/C.U.R.S.O.R
python3 "Create account.py"
EOF

chmod +x ~/cursor-launcher.sh

# Create desktop shortcut (optional)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${YELLOW}Would you like to create a desktop shortcut? (y/n)${NC}"
    read -r shortcut_response
    if [[ "$shortcut_response" =~ ^[yY]$ ]]; then
        echo -e "${BLUE}Creating desktop shortcut...${NC}"
        cat > ~/.local/share/applications/cursor.desktop << EOF
[Desktop Entry]
Name=C.U.R.S.O.R
Comment=Cursor Account Creator
Exec=~/cursor-launcher.sh
Icon=utilities-terminal
Terminal=true
Type=Application
Categories=Utility;
EOF
        echo -e "${GREEN}Desktop shortcut created!${NC}"
    fi
fi

# Completion message
echo
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║      Installation completed successfully!   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo
echo -e "${YELLOW}You can now run C.U.R.S.O.R by executing:${NC}"
echo -e "${BLUE}~/cursor-launcher.sh${NC}"
echo
animate_text "${CYAN}Thank you for installing C.U.R.S.O.R!${NC}" 0.02 