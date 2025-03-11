#!/bin/bash

# Exit on error
set -e

echo "=== Fixing python-uinput installation ==="

# Make sure required system packages are installed
echo "Installing required system packages..."
sudo apt-get update
sudo apt-get install -y python3-dev libudev-dev build-essential

# Locate the uinput module installation
echo "Locating uinput module..."
UINPUT_DIR=$(python3 -c "import site; import os; site_packages = site.getsitepackages(); \
  uinput_dirs = [os.path.join(p, 'uinput') for p in site_packages if os.path.exists(os.path.join(p, 'uinput'))]; \
  print(uinput_dirs[0] if uinput_dirs else '')")

if [ -z "$UINPUT_DIR" ]; then
  echo "Error: Cannot find uinput module. Please reinstall it."
  exit 1
fi

echo "Found uinput module at: $UINPUT_DIR"

# Fix the __init__.py file to handle None value for SO
echo "Patching uinput/__init__.py..."
INIT_PY="$UINPUT_DIR/__init__.py"
if [ -f "$INIT_PY" ]; then
  sudo sed -i 's/_libsuinput_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "_libsuinput" + sysconfig.get_config_var("SO")))/_libsuinput_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "_libsuinput" + (sysconfig.get_config_var("SO") or ".so")))/' "$INIT_PY"
  echo "Patched $INIT_PY successfully"
else
  echo "Error: Cannot find $INIT_PY"
  exit 1
fi

# Create or fix the missing _libsuinput.so file
echo "Checking for missing _libsuinput.so..."
PARENT_DIR=$(dirname "$UINPUT_DIR")
if [ ! -f "$PARENT_DIR/_libsuinput.so" ]; then
  echo "Compiling _libsuinput.so from source..."
  
  # Create a temporary directory
  TEMP_DIR=$(mktemp -d)
  cd "$TEMP_DIR"
  
  # Clone the repository
  git clone https://github.com/tuomasjjrasanen/python-uinput.git
  cd python-uinput
  
  # Find the source file (debugging the structure)
  echo "Checking repository structure..."
  find . -name "*.c" | grep -i uinput
  
  # Compile the C library with corrected path
  if [ -f "libsuinput/src/libuinput.c" ]; then
    echo "Found source at libsuinput/src/libuinput.c"
    gcc -fPIC -shared -o _libsuinput.so libsuinput/src/libuinput.c
  elif [ -f "_libsuinput.c" ]; then
    echo "Found source at _libsuinput.c"
    gcc -fPIC -shared -o _libsuinput.so _libsuinput.c
  else
    echo "Searching for C source files..."
    find . -name "*.c" -type f
    
    # Try with setup.py as a last resort
    echo "Trying to build using setup.py..."
    python3 setup.py build_ext --inplace
    
    # Find the built .so file
    SO_FILE=$(find . -name "_libsuinput*.so")
    if [ -n "$SO_FILE" ]; then
      echo "Found compiled library at $SO_FILE"
      cp "$SO_FILE" _libsuinput.so
    else
      echo "Failed to build the library. Trying direct pip installation..."
      sudo pip3 install --force-reinstall --break-system-packages python-uinput
      exit 0
    fi
  fi
  
  # Copy to the correct location
  if [ -f "_libsuinput.so" ]; then
    sudo cp _libsuinput.so "$PARENT_DIR/"
    sudo chmod 755 "$PARENT_DIR/_libsuinput.so"
    echo "Successfully installed _libsuinput.so to $PARENT_DIR/"
  else
    echo "Failed to compile _libsuinput.so"
    # Try direct installation as a fallback
    sudo pip3 install --force-reinstall --break-system-packages python-uinput
  fi
  
  # Clean up
  cd /
  rm -rf "$TEMP_DIR"
else
  echo "_libsuinput.so already exists at $PARENT_DIR/_libsuinput.so"
fi

# Load the uinput kernel module if not already loaded
if ! lsmod | grep -q uinput; then
  echo "Loading uinput kernel module..."
  sudo modprobe uinput
fi

# Test if uinput can be imported now
echo "Testing uinput module..."
if python3 -c "import uinput; print('SUCCESS: uinput module is working properly!')" 2>/dev/null; then
  echo "✅ python-uinput is now working correctly!"
else
  echo "❌ Still having issues with the uinput module. Error details:"
  python3 -c "import uinput" 2>&1
  
  echo -e "\nAdditional debugging info:"
  ls -la "$PARENT_DIR/"*uinput* 2>/dev/null || echo "No uinput files found in $PARENT_DIR"
  
  # Try a more aggressive solution - direct binary installation
  echo "Trying alternative solution - using apt package..."
  sudo apt-get install -y python3-uinput
  
  if ! python3 -c "import uinput; print('SUCCESS: uinput module is working properly!')" 2>/dev/null; then
    echo "Final attempt - force installing with pip..."
    sudo pip3 install --force-reinstall --break-system-packages python-uinput
  fi
fi

echo -e "\nNote: If you're still having issues, you may need to make sure your user has access to the uinput device:"
echo "sudo chmod 666 /dev/uinput" 