import os
import sys
import sysconfig

# Find where uinput is installed
import site
site_packages = site.getsitepackages()

for path in site_packages:
    uinput_init = os.path.join(path, 'uinput', '__init__.py')
    if os.path.exists(uinput_init):
        print(f"Found uinput at: {uinput_init}")
        
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
            
            print("Successfully patched uinput module")
            sys.exit(0)

print("Could not find uinput module in site-packages. Please ensure it's installed correctly.")
sys.exit(1) 