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
import uinput
import subprocess
import time
import os
import sys
from Xlib import display
from Xlib.ext import xtest
import pwd
import shutil

# Add color formatting for terminal output
class TermColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Updated print functions to ensure clean line breaks
def print_status(message):
    # Force a carriage return to ensure we start at the left margin
    print(f"\r{TermColors.BLUE}[*] {message}{TermColors.ENDC}")
    sys.stdout.flush()  # Ensure output is displayed immediately
    
def print_success(message):
    print(f"\r{TermColors.GREEN}[✓] {message}{TermColors.ENDC}")
    sys.stdout.flush()
    
def print_error(message):
    print(f"\r{TermColors.RED}[✗] {message}{TermColors.ENDC}")
    sys.stdout.flush()
    
def print_warning(message):
    print(f"\r{TermColors.YELLOW}[!] {message}{TermColors.ENDC}")
    sys.stdout.flush()

def print_header(message):
    print(f"\n{TermColors.HEADER}{TermColors.BOLD}{message}{TermColors.ENDC}\n")  # Added extra newline

# Show a simple progress indicator
def progress_indicator(message, duration, steps=10):
    print_status(message)
    step_time = duration / steps
    for i in range(steps):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(step_time)
    print()

# Use try/except block to handle uinput import error
try:
    import uinput
except TypeError as e:
    if "concatenate str (not \"NoneType\") to str" in str(e):
        print_warning("Patching uinput module to fix SO variable error...")
        import os
        import sys
        import site
        import sysconfig
        
        # Find where uinput is installed
        site_packages = site.getsitepackages()
        
        for path in site_packages:
            uinput_init = os.path.join(path, 'uinput', '__init__.py')
            if os.path.exists(uinput_init):
                # Simplified message
                print_status(f"Found uinput module")
                
                # Read the file
                with open(uinput_init, 'r') as f:
                    content = f.read()
                
                # Replace the problematic line with a safer version
                if "_libsuinput_path = os.path.abspath(os.path.join(os.path.dirname(__file__), \"..\", \"_libsuinput\" + sysconfig.get_config_var(\"SO\")))" in content:
                    new_content = content.replace(
                        "_libsuinput_path = os.path.abspath(os.path.join(os.path.dirname(__file__), \"..\", \"_libsuinput\" + sysconfig.get_config_var(\"SO\")))",
                        "_libsuinput_path = os.path.abspath(os.path.join(os.path.dirname(__file__), \"..\", \"_libsuinput\" + (sysconfig.get_config_var(\"SO\") or \".so\")))"
                    )
                    
                    # Write the patched file
                    with open(uinput_init, 'w') as f:
                        f.write(new_content)
                    
                    print_success("Successfully patched uinput module")
                    import uinput
                    break
        else:
            print_error("Could not find uinput module. Please run setup script first.")
            sys.exit(1)
    else:
        # Re-raise the exception if it's not the one we're looking for
        raise

def cleanup_chrome():
    """Kill any existing Chrome processes"""
    try:
        subprocess.run(['pkill', '-9', 'chrome'], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['pkill', '-9', 'chromium'], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['pkill', '-9', 'chromedriver'], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['pkill', '-9', 'google-chrome'], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.5)
        print_status("Cleaned up Chrome processes")
    except Exception as e:
        print_warning(f"Chrome cleanup warning: {e}")

def perform_mouse_click(x, y, description=""):
    """Perform mouse click using Xlib for absolute positioning"""
    print_status(f"Clicking: {description}")
    
    d = display.Display()
    root = d.screen().root
    
    # Move mouse to exact coordinates
    root.warp_pointer(x, y)
    d.sync()
    time.sleep(0.5)
    
    # Click
    xtest.fake_input(d, 4, 1)  # 4 is ButtonPress
    d.sync()
    time.sleep(0.1)
    xtest.fake_input(d, 5, 1)  # 5 is ButtonRelease
    d.sync()
    time.sleep(0.5)
    print()  # Add newline after each click

def type_url(device):
    """Type cursor.com in the address bar"""
    print_status("Focusing address bar")
    device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_L])
    time.sleep(0.5)
    print()  # Add newline
    
    print_status("Typing URL")
    url_keys = [
        uinput.KEY_C, uinput.KEY_U, uinput.KEY_R, uinput.KEY_S,
        uinput.KEY_O, uinput.KEY_R, uinput.KEY_DOT,
        uinput.KEY_C, uinput.KEY_O, uinput.KEY_M
    ]
    
    for key in url_keys:
        device.emit_click(key)
        time.sleep(0.05)
    
    device.emit_click(uinput.KEY_ENTER)
    time.sleep(1)
    print()  # Add newline

def main():
    if os.geteuid() != 0:
        print_error("This script requires sudo for mouse control")
        print_status("Please run: sudo python3 cursor_signup.py")
        sys.exit(1)
    
    # Get the actual user (not root)
    sudo_user = os.environ.get('SUDO_USER')
    if not sudo_user:
        print_error("This script must be run with sudo")
        sys.exit(1)
    
    # Allow root access to X server
    try:
        subprocess.run(['sudo', '-u', sudo_user, 'xhost', '+SI:localuser:root'], 
                      check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print_warning("Could not set X server permissions. Visual feedback may be limited.")
        
    # Display welcome banner
    print_header("CURSOR - Automated Account Creation Tool")
    
    # Initialize uinput for keyboard only
    print_status("Initializing input control...")
    events = [
        uinput.KEY_LEFTCTRL,
        uinput.KEY_L,
        uinput.KEY_ENTER,
        uinput.KEY_C,
        uinput.KEY_U,
        uinput.KEY_R,
        uinput.KEY_S,
        uinput.KEY_O,
        uinput.KEY_M,
        uinput.KEY_DOT
    ]
    
    device = uinput.Device(events)
    time.sleep(1)
    
    cleanup_chrome()
    
    # Launch Chrome with proper environment
    print_status(f"Starting Chrome as user {sudo_user}...")
    
    # Redirect stderr to suppress D-Bus errors
    chrome_cmd = [
        'sudo', '-u', sudo_user,
        'google-chrome',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--start-maximized',
        '--disable-gpu',  # Disable GPU to reduce errors
        '--no-first-run',  # Skip first run dialogs
        'about:blank'
    ]
    
    try:
        print_status("Attempting to launch Chrome...")
        with open(os.devnull, 'w') as devnull:
            chrome_process = subprocess.Popen(chrome_cmd, stderr=devnull)
        
        print_status("Waiting for Chrome to load...")
        time.sleep(2)  # Give Chrome more time to start
        print()  # Add blank line for cleaner separation
        
        # Check if Chrome is running
        try:
            # Redirect both stdout and stderr to /dev/null to prevent diagonal output
            subprocess.run(['pgrep', 'chrome'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print_error("Error: Chrome failed to start!")
            sys.exit(1)
        
        print_success("Chrome is running, proceeding with automation...")
        print()  # Add newline
        
        # Type the URL
        type_url(device)
        print()  # Add newline
        
        # First click - top right
        perform_mouse_click(1813, 230, "first target") #1444
        print()  # Add newline
        time.sleep(3.6)
        perform_mouse_click(1465, 230, "first target") #1920
        print()  # Add newline
        time.sleep(2.5)
        
        # Second click - bottom
        perform_mouse_click(1291, 920, "second target") #1920
        print()  # Add newline
        perform_mouse_click(971, 711, "second target") #1444
        print()  # Add newline
        
        print_success("Navigation and clicks completed!")
        print()  # Add newline
        input("Press Enter to close Chrome...")
        chrome_process.terminate()
        cleanup_chrome()
        device.destroy()
        
        # Remove root access to X server
        subprocess.run(['sudo', '-u', sudo_user, 'xhost', '-SI:localuser:root'], check=False)
        print_success("Removed X server access from root")
        
    except Exception as e:
        print_error(f"Error during main execution: {e}")
        # Remove root access to X server even on error
        subprocess.run(['sudo', '-u', sudo_user, 'xhost', '-SI:localuser:root'], check=False)
        sys.exit(1)

if __name__ == "__main__":
    main() 