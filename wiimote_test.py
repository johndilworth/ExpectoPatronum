#!/usr/bin/python3
import cwiid
import time

def test_wiimote():
    print("Press 1+2 on your Wiimote now...")
    
    try:
        wm = cwiid.Wiimote()
        print("Wiimote connected successfully!")
        
        # Turn on led 1 and 4 to indicate connection
        wm.led = 9  # Binary 1001, turns on LED 1 and 4
        
        # Set report mode to receive button presses
        wm.rpt_mode = cwiid.RPT_BTN
        
        # Do a quick rumble to confirm connection
        wm.rumble = True
        time.sleep(0.5)
        wm.rumble = False
        
        print("\nWiimote is ready! Try pressing some buttons.")
        print("Press Plus (+) and Minus (-) together to exit.\n")
        
        while True:
            buttons = wm.state['buttons']
            
            # Create a list of pressed buttons
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
            
            # Print pressed buttons
            if pressed:
                print(f"Buttons pressed: {', '.join(pressed)}")
            
            # Exit if Plus and Minus are pressed together
            if buttons & cwiid.BTN_PLUS and buttons & cwiid.BTN_MINUS:
                print("\nExiting...")
                break
            
            time.sleep(0.1)
            
    except RuntimeError:
        print("Error connecting to Wiimote. Make sure it's in discovery mode (press 1+2)")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if 'wm' in locals():
            wm.led = 0
            wm.rumble = False
            
if __name__ == "__main__":
    test_wiimote()