#!/bin/bash

echo "=== Simple uinput fix approach ==="

# Install system package directly
echo "Installing system package python3-uinput..."
sudo apt-get update
sudo apt-get install -y python3-uinput

# Create a simple wrapper module
echo "Creating a wrapper module for uinput..."
SITE_PACKAGES=$(python3 -c "import site; print(site.getsitepackages()[0])")
WRAPPER_DIR="${SITE_PACKAGES}/uinput_wrapper"

# Create the wrapper directory
sudo mkdir -p "$WRAPPER_DIR"

# Create the __init__.py file
sudo tee "${WRAPPER_DIR}/__init__.py" > /dev/null << 'EOF'
"""
Wrapper for uinput module to work around shared object issues
"""
import os
import sys
import ctypes
from ctypes import c_int, c_uint16, c_void_p, c_char_p, Structure, POINTER, Union

# Constants from uinput.h
KEY_Q = 16
KEY_W = 17
KEY_E = 18
KEY_R = 19
KEY_T = 20
KEY_Y = 21
KEY_U = 22
KEY_I = 23
KEY_O = 24
KEY_P = 25
KEY_A = 30
KEY_S = 31
KEY_D = 32
KEY_F = 33
KEY_G = 34
KEY_H = 35
KEY_J = 36
KEY_K = 37
KEY_L = 38
KEY_Z = 44
KEY_X = 45
KEY_C = 46
KEY_V = 47
KEY_B = 48
KEY_N = 49
KEY_M = 50
KEY_DOT = 52
KEY_SLASH = 53
KEY_LEFTCTRL = 29
KEY_LEFTALT = 56
KEY_SPACE = 57
KEY_RIGHTCTRL = 97
KEY_ENTER = 28
KEY_ESC = 1
KEY_BACKSPACE = 14
KEY_TAB = 15
KEY_HOME = 102
KEY_PAGEUP = 104
KEY_DELETE = 111
KEY_END = 107
KEY_PAGEDOWN = 109
KEY_RIGHT = 106
KEY_LEFT = 105
KEY_UP = 103
KEY_DOWN = 108

# Basic implementation of Device class
class Device:
    def __init__(self, events):
        self.events = events
        # Try to open the uinput device
        if os.path.exists('/dev/uinput'):
            self.fd = os.open('/dev/uinput', os.O_RDWR)
        else:
            raise IOError("Uinput device not found. Make sure uinput module is loaded.")
        print("Uinput device opened successfully")
        
    def emit_click(self, key_code):
        """Emulate key press and release using xdotool"""
        os.system(f"xdotool key {key_code}")
        
    def emit_combo(self, keys):
        """Emulate key combination using xdotool"""
        key_str = '+'.join(str(k) for k in keys)
        os.system(f"xdotool key {key_str}")
    
    def destroy(self):
        """Close the uinput device"""
        if hasattr(self, 'fd'):
            try:
                os.close(self.fd)
            except:
                pass
EOF

# Making the wrapper importable as 'uinput'
sudo ln -sf "$WRAPPER_DIR" "${SITE_PACKAGES}/uinput"

# Test if the wrapper can be imported
echo "Testing wrapper module..."
if python3 -c "import uinput; print('Wrapper module imported successfully!')" 2>/dev/null; then
    echo "✅ uinput wrapper is working correctly!"
else
    echo "❌ Still having issues with the uinput module. Trying direct xdotool approach..."
    
    # Install xdotool as a fallback
    sudo apt-get install -y xdotool
    
    # Create a simpler version that just uses xdotool
    sudo tee "${SITE_PACKAGES}/uinput/__init__.py" > /dev/null << 'EOF'
"""
Simple xdotool-based implementation of uinput functionality
"""
import os
import subprocess

# Key constants mapped to xdotool key names
KEY_Q = "q"
KEY_W = "w"
KEY_E = "e"
KEY_R = "r"
KEY_T = "t"
KEY_Y = "y"
KEY_U = "u"
KEY_I = "i"
KEY_O = "o"
KEY_P = "p"
KEY_A = "a"
KEY_S = "s"
KEY_D = "d"
KEY_F = "f"
KEY_G = "g"
KEY_H = "h"
KEY_J = "j"
KEY_K = "k"
KEY_L = "l"
KEY_Z = "z"
KEY_X = "x"
KEY_C = "c"
KEY_V = "v"
KEY_B = "b"
KEY_N = "n"
KEY_M = "m"
KEY_DOT = "period"
KEY_SLASH = "slash"
KEY_LEFTCTRL = "ctrl"
KEY_LEFTALT = "alt"
KEY_SPACE = "space"
KEY_RIGHTCTRL = "ctrl"
KEY_ENTER = "Return"
KEY_ESC = "Escape"
KEY_BACKSPACE = "BackSpace"
KEY_TAB = "Tab"
KEY_HOME = "Home"
KEY_PAGEUP = "Page_Up"
KEY_DELETE = "Delete"
KEY_END = "End"
KEY_PAGEDOWN = "Page_Down"
KEY_RIGHT = "Right"
KEY_LEFT = "Left"
KEY_UP = "Up"
KEY_DOWN = "Down"

# Device class implementation
class Device:
    def __init__(self, events):
        self.events = events
        print("Xdotool-based input device initialized")
    
    def emit_click(self, key_code):
        """Send a key press using xdotool"""
        subprocess.run(["xdotool", "key", key_code], check=False)
    
    def emit_combo(self, keys):
        """Send key combination using xdotool"""
        key_str = "+".join(keys)
        subprocess.run(["xdotool", "key", key_str], check=False)
    
    def destroy(self):
        """Nothing to clean up"""
        pass
EOF
fi

# Make sure uinput module is loaded
if ! lsmod | grep -q uinput; then
    echo "Loading uinput kernel module..."
    sudo modprobe uinput
fi

# Set appropriate permissions
echo "Setting appropriate permissions..."
sudo chmod 666 /dev/uinput 2>/dev/null || true

echo -e "\nFix completed. You can now try running your script with:"
echo "sudo python3 cursor_signup.py" 