#!/usr/bin/python3
import cwiid
import time
import bluetooth
import subprocess
from contextlib import contextmanager

def setup_bluetooth():
    """Reset and setup bluetooth"""
    try:
        subprocess.run(['sudo', 'hciconfig', 'hci0', 'reset'], check=True)
        time.sleep(1)
        subprocess.run(['sudo', 'hciconfig', 'hci0', 'up'], check=True)
        time.sleep(1)
        subprocess.run(['sudo', 'hciconfig', 'hci0', 'piscan'], check=True)
        time.sleep(1)
        print("Bluetooth setup complete")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up Bluetooth: {e}")

def main():
    print("Setting up Bluetooth...")
    setup_bluetooth()
    
    print("\nPress and hold 1+2 on your Wiimote now...")
    
    try:
        # Connect to the Wiimote
        wiimote = cwiid.Wiimote()
        print("Connected to Wiimote successfully!")
        
        # Set report mode
        try:
            wiimote.rpt_mode = cwiid.RPT_BTN
            print("Report mode set successfully")
        except Exception as e:
            print(f"Warning: Couldn't set report mode: {e}")
        
        print("\nWiimote connected and ready!")
        print("Press + and - together to exit")
        
        while True:
            try:
                buttons = wiimote.state['buttons']
                
                # Check for exit condition first
                if buttons & cwiid.BTN_PLUS and buttons & cwiid.BTN_MINUS:
                    print("\nExiting...")
                    break
                
                # Check other buttons
                pressed = []
                if buttons & cwiid.BTN_A:
                    pressed.append("A")
                if buttons & cwiid.BTN_B:
                    pressed.append("B")
                if buttons & cwiid.BTN_1:
                    pressed.append("1")
                if buttons & cwiid.BTN_2:
                    pressed.append("2")
                if buttons & cwiid.BTN_PLUS:
                    pressed.append("+")
                if buttons & cwiid.BTN_MINUS:
                    pressed.append("-")
                if buttons & cwiid.BTN_HOME:
                    pressed.append("HOME")
                if buttons & cwiid.BTN_UP:
                    pressed.append("UP")
                if buttons & cwiid.BTN_DOWN:
                    pressed.append("DOWN")
                if buttons & cwiid.BTN_LEFT:
                    pressed.append("LEFT")
                if buttons & cwiid.BTN_RIGHT:
                    pressed.append("RIGHT")
                
                if pressed:
                    print(f"Buttons pressed: {', '.join(pressed)}")
                
                time.sleep(0.1)
                
            except RuntimeError as e:
                print(f"Error reading Wiimote state: {e}")
                break
            except KeyboardInterrupt:
                print("\nExiting due to keyboard interrupt...")
                break
                
    except RuntimeError as e:
        print(f"Failed to connect: {e}")
    except KeyboardInterrupt:
        print("\nExiting due to keyboard interrupt...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if 'wiimote' in locals():
            try:
                wiimote.rumble = False
                wiimote.led = 0
                wiimote.close()
            except:
                pass

if __name__ == "__main__":
    main()