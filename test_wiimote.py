# wiimote.py
#!/usr/bin/python2
import cwiid
import time
import logging

print('Press 1+2 on your Wiimote to begin the connection...')

class Wiimote:
    def __init__(self):
        self.wiimote = None
    
    def connect(self):
        try:
            time.sleep(1)
            print("Attempting to connect... Hold 1+2 on the Wiimote")
            self.wiimote = cwiid.Wiimote()
            print("Connected successfully!")
        except RuntimeError:
            print("Connection failed. Retrying...")
            self.connect()
    
    def connect_wiimote(self):
        self.connect()
        if self.wiimote:
            self.wiimote.led = 6
            self.wiimote.rpt_mode = cwiid.RPT_BTN
    
    def validate_connection(self):
        try:
            self.wiimote.request_status()
        except RuntimeError:
            print("Connection lost. Reconnecting...")
            self.connect_wiimote()
    
    def connection_fun(self):
        if not self.wiimote:
            return
        
        time.sleep(1)
        try:
            # Rumble pattern
            for _ in range(4):
                self.wiimote.rumble = True
                time.sleep(0.1)
                self.wiimote.rumble = False
                time.sleep(0.1)
            
            # LED pattern
            self.wiimote.led = 0
            time.sleep(1)
            for i in [1, 2, 4, 8, 4, 2, 1, 2, 4, 8, 4, 2, 1, 2, 4, 8, 4, 2, 1, 0]:
                self.wiimote.led = i
                time.sleep(0.1)
            
            self.wiimote.led = 6
            self.wiimote.rpt_mode = cwiid.RPT_BTN
        except Exception as e:
            print("Error during connection animation: %s" % str(e))

# test_wiimote.py
#!/usr/bin/python2
from wiimote import Wiimote
import cwiid
import time

def test_wiimote():
    """
    Simple test script to verify Wiimote connectivity
    """
    print("Starting Wiimote test...")
    
    # Create Wiimote instance
    wii = Wiimote()
    
    try:
        # Connect to Wiimote
        print("Attempting to connect to Wiimote...")
        wii.connect_wiimote()
        print("Connection established!")
        
        # Run the connection animation
        print("Running connection animation...")
        wii.connection_fun()
        print("Animation complete!")
        
        # Test button inputs
        print("\nButton Test:")
        print("Press buttons to see their states (Press + and - together to exit):")
        
        while True:
            try:
                buttons = wii.wiimote.state['buttons']
                
                # Create a list of active buttons
                active_buttons = []
                if buttons & cwiid.BTN_A:
                    active_buttons.append('A')
                if buttons & cwiid.BTN_B:
                    active_buttons.append('B')
                if buttons & cwiid.BTN_1:
                    active_buttons.append('1')
                if buttons & cwiid.BTN_2:
                    active_buttons.append('2')
                if buttons & cwiid.BTN_PLUS:
                    active_buttons.append('+')
                if buttons & cwiid.BTN_MINUS:
                    active_buttons.append('-')
                if buttons & cwiid.BTN_HOME:
                    active_buttons.append('HOME')
                
                # Print active buttons if any are pressed
                if active_buttons:
                    print("Pressed: " + ', '.join(active_buttons))
                
                # Exit condition: pressing + and - together
                if buttons & cwiid.BTN_PLUS and buttons & cwiid.BTN_MINUS:
                    print("\nTest complete!")
                    break
                
                # Small delay to prevent overwhelming the console
                time.sleep(0.1)
                
            except RuntimeError:
                print("Connection lost! Attempting to reconnect...")
                wii.connect_wiimote()
                
    except KeyboardInterrupt:
        print("\nTest terminated by user")
    except Exception as e:
        print("An error occurred: %s" % str(e))
    finally:
        if hasattr(wii, 'wiimote') and wii.wiimote:
            wii.wiimote.led = 0
            wii.wiimote.rumble = 0

if __name__ == "__main__":
    test_wiimote()