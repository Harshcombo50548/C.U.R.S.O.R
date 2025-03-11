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

def cleanup_chrome():
    """Kill any existing Chrome processes"""
    try:
        subprocess.run(['pkill', '-9', 'chrome'], check=False)
        subprocess.run(['pkill', '-9', 'chromium'], check=False)
        subprocess.run(['pkill', '-9', 'chromedriver'], check=False)
        subprocess.run(['pkill', '-9', 'google-chrome'], check=False)
        time.sleep(0.5)
        print("Cleaned up existing Chrome processes")
    except Exception as e:
        print(f"Warning during cleanup: {e}")

def perform_mouse_click(x, y, description=""):
    """Perform mouse click using Xlib for absolute positioning"""
    print(f"Moving to {description} ({x}, {y})...")
    
    d = display.Display()
    root = d.screen().root
    
    # Move mouse to exact coordinates
    root.warp_pointer(x, y)
    d.sync()
    time.sleep(0.5)
    
    # Click
    print(f"Clicking at {description}...")
    xtest.fake_input(d, 4, 1)  # 4 is ButtonPress
    d.sync()
    time.sleep(0.1)
    xtest.fake_input(d, 5, 1)  # 5 is ButtonRelease
    d.sync()
    time.sleep(0.5)

def type_url(device):
    """Type cursor.com in the address bar"""
    print("Focusing address bar...")
    device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_L])
    time.sleep(0.5)
    
    print("Typing URL...")
    url_keys = [
        uinput.KEY_C, uinput.KEY_U, uinput.KEY_R, uinput.KEY_S,
        uinput.KEY_O, uinput.KEY_R, uinput.KEY_DOT,
        uinput.KEY_C, uinput.KEY_O, uinput.KEY_M
    ]
    
    for key in url_keys:
        device.emit_click(key)
        time.sleep(0.05)
    
    device.emit_click(uinput.KEY_ENTER)
    print("URL typed and entered")
    time.sleep(1)

def main():
    if os.geteuid() != 0:
        print("This script requires sudo for mouse control")
        print("Please run: sudo python3 step5.py")
        sys.exit(1)
    
    # Get the actual user (not root)
    sudo_user = os.environ.get('SUDO_USER')
    if not sudo_user:
        print("This script must be run with sudo")
        sys.exit(1)
    
    # Allow root access to X server
    try:
        subprocess.run(['sudo', '-u', sudo_user, 'xhost', '+SI:localuser:root'], check=True)
        print("Granted X server access to root")
    except subprocess.CalledProcessError as e:
        print(f"Failed to grant X server access: {e}")
        sys.exit(1)
    
    # Initialize uinput for keyboard only
    print("Initializing input control...")
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
    print(f"Starting Chrome as user {sudo_user}...")
    
    chrome_cmd = [
        'sudo', '-u', sudo_user,
        'google-chrome',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--start-maximized',
        'about:blank'
    ]
    
    try:
        print("Attempting to launch Chrome...")
        chrome_process = subprocess.Popen(chrome_cmd)
        print("Waiting for Chrome to load...")
        time.sleep(0.5)
        
        # Type the URL
        type_url(device)
        time.sleep(0.5)
        
        # First click - top right
        perform_mouse_click(1465, 230, "first target")
        time.sleep(1.5)
        
        # Second click - bottom
        perform_mouse_click(971, 711, "second target")
        
        print("Navigation and clicks completed!")
        input("Press Enter to close Chrome...")
        chrome_process.terminate()
        cleanup_chrome()
        device.destroy()
        
        # Remove root access to X server
        subprocess.run(['sudo', '-u', sudo_user, 'xhost', '-SI:localuser:root'], check=False)
        print("Removed X server access from root")
        
        # Run create_accounts.py after cursor_signup.py finishes
        print("Running create_accounts.py...")
        subprocess.run(['python3', 'create_accounts.py'], check=True)
        print("create_accounts.py finished execution")

    except Exception as e:
        print(f"Error during main execution: {e}")
        # Remove root access to X server even on error
        subprocess.run(['sudo', '-u', sudo_user, 'xhost', '-SI:localuser:root'], check=False)
        sys.exit(1)

if __name__ == "__main__":
    main() 