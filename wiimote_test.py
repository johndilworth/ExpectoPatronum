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

@contextmanager
def safe_wiimote_connect():
    """Safely connect and disconnect wiimote"""
    wm = None
    try:
        print("\nPress and hold 1+2 on your Wiimote now...")
        wm = cwiid.Wiimote()
        print("Connected to Wiimote successfully!")
        yield wm
    except Exception as e:
        print(f"Wiimote error: {e}")
        if wm:
            try:
                wm.close()
            except:
                pass
        raise
    finally:
        if wm:
            try:
                wm.rumble = False
                wm.led = 0
                time.sleep(0.1)
                wm.close()
            except:
                pass

def main():
    print("Setting up Bluetooth...")
    setup_bluetooth()
    
    try:
        with safe_wiimote_connect() as wiimote:
            # Set report mode
            try:
                wiimote.rpt_mode = cwiid.RPT_BTN
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