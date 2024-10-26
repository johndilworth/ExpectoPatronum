#!/usr/bin/python3
import cwiid
import time
import bluetooth
import subprocess

def check_bluetooth():
    print("\nChecking Bluetooth status...")
    
    # Check if Bluetooth service is running
    try:
        service_check = subprocess.run(['systemctl', 'is-active', 'bluetooth'], 
                                     capture_output=True, text=True)
        print(f"Bluetooth service status: {service_check.stdout.strip()}")
    except Exception as e:
        print(f"Error checking Bluetooth service: {e}")

    # Check available Bluetooth devices
    print("\nChecking Bluetooth adapter...")
    try:
        hci_check = subprocess.run(['hciconfig'], capture_output=True, text=True)
        print(hci_check.stdout)
    except Exception as e:
        print(f"Error checking Bluetooth adapter: {e}")

def scan_for_wiimotes():
    print("\nScanning for Bluetooth devices...")
    print("This may take a few seconds...")
    try:
        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True)
        print(f"Found {len(nearby_devices)} devices:")
        for addr, name in nearby_devices:
            print(f"  {addr} - {name}")
        return nearby_devices
    except Exception as e:
        print(f"Error scanning for devices: {e}")
        return []

def connect_wiimote(max_attempts=3):
    print("\nStarting Wiimote connection test...")
    check_bluetooth()
    
    for attempt in range(max_attempts):
        print(f"\nConnection attempt {attempt + 1} of {max_attempts}")
        print("\nPress and HOLD buttons 1 + 2 on your Wiimote now")
        print("(The Wiimote lights should start blinking)")
        print("Waiting for Wiimote connection...")
        
        try:
            # Scan for devices before attempting connection
            scan_for_wiimotes()
            
            # Try to connect
            wm = cwiid.Wiimote()
            print("\nWiimote connected successfully!")
            
            # Test basic functionality
            print("Testing Wiimote features...")
            
            # LED test
            print("Testing LEDs...")
            for led in range(4):
                wm.led = 1 << led
                time.sleep(0.5)
            
            # Rumble test
            print("Testing rumble...")
            wm.rumble = True
            time.sleep(0.5)
            wm.rumble = False
            
            # Set final LED pattern and report mode
            wm.led = 6  # LED 2 and 3 on
            wm.rpt_mode = cwiid.RPT_BTN
            
            print("\nWiimote is ready! Try pressing some buttons.")
            print("Press Plus (+) and Minus (-) together to exit.\n")
            
            while True:
                buttons = wm.state['buttons']
                
                # Create a list of pressed buttons
                pressed = []
                button_map = {
                    cwiid.BTN_A: 'A',
                    cwiid.BTN_B: 'B',
                    cwiid.BTN_1: '1',
                    cwiid.BTN_2: '2',
                    cwiid.BTN_PLUS: '+',
                    cwiid.BTN_MINUS: '-',
                    cwiid.BTN_HOME: 'HOME',
                    cwiid.BTN_UP: 'UP',
                    cwiid.BTN_DOWN: 'DOWN',
                    cwiid.BTN_LEFT: 'LEFT',
                    cwiid.BTN_RIGHT: 'RIGHT'
                }
                
                for button, name in button_map.items():
                    if buttons & button:
                        pressed.append(name)
                
                if pressed:
                    print(f"Buttons pressed: {', '.join(pressed)}")
                
                if buttons & cwiid.BTN_PLUS and buttons & cwiid.BTN_MINUS:
                    print("\nExiting...")
                    break
                
                time.sleep(0.1)
            
            return wm
            
        except RuntimeError as e:
            print(f"Connection attempt failed: {e}")
            if attempt < max_attempts - 1:
                print("\nWaiting 10 seconds before next attempt...")
                print("Please make sure you're holding buttons 1 + 2")
                time.sleep(10)
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            print("Try removing and reinserting the Wiimote batteries")
    
    print("\nFailed to connect after all attempts")
    return None

if __name__ == "__main__":
    try:
        # Reset bluetooth before starting
        subprocess.run(['sudo', 'hciconfig', 'hci0', 'reset'])
        time.sleep(1)
        
        wiimote = connect_wiimote()
        if wiimote:
            print("Test completed successfully")
            wiimote.led = 0
            wiimote.rumble = False
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        if 'wiimote' in locals() and wiimote:
            wiimote.led = 0
            wiimote.rumble = False