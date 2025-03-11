import subprocess
import time

print("Move your mouse over the button, then note the X and Y coordinates below.")
print("Press Ctrl+C to exit.")

try:
    while True:
        # Run xdotool and get output
        output = subprocess.check_output(['xdotool', 'getmouselocation']).decode()
        # Parse the output (format is "x:123 y:456 screen:0 window:123456")
        coords = dict(item.split(":") for item in output.strip().split())
        x, y = coords['x'], coords['y']
        print(f"X: {x}, Y: {y}    ", end='\r')  # Extra spaces to clear previous output
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nDone.")
except FileNotFoundError:
    print("\nError: xdotool not found. Please install it with: sudo apt-get install xdotool") 