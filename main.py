"""
main.py

Author: Achille Lanctôt-Saumure
GitHub: Troy-Boy
Date created: May 5th, 2024

This script interacts with an API using the API class defined in api.py and manages API keys using the functions in credentials.py.

License: MIT License (https://opensource.org/licenses/MIT)

Dependencies:
- Python 3.10+
- requests library

For questions or assistance, contact Achilles Lanctôt-Saumure at achille.lanctots@gmail.com.
"""

from api import API
from config import Config
from credentials import get_api_key
from keypad import Keypad
from typing import List

import LCD1602
import RPi.GPIO as GPIO 
import time

def setup_keypad() -> Keypad:
    """Instantiate the keypad with the relevant keys.
    
    Returns:
        Keypad: An instance of the Keypad class.
    """
    rows_pins = [18, 23, 24, 25]  # GPIO pins for the rows of the keypad
    cols_pins = [10, 22, 27, 17]  # GPIO pins for the columns of the keypad
    keys = [
        "1", "2", "3", "A",
        "4", "5", "6", "B",
        "7", "8", "9", "C",
        "*", "0", "#", "D"
    ]  # Keys corresponding to the keypad layout

    keypad = Keypad(rows_pins, cols_pins, keys)
    return keypad

def setup_lcd():
    """Initialize the LCD screen."""
    LCD1602.init(None, 1)  # Init(slave address, background light)
    LCD1602.clear()
    LCD1602.write(0, 0, 'Enter 6-digit code')
    LCD1602.write(0, 1, 'Then press #. Use * to clear input')

def destroy():
    """Clean up GPIO resources."""
    LCD1602.clear()
    GPIO.cleanup()

def get_current_time() -> str:
    """Get the current time in ISO format.
    
    Returns:
        str: The current time in ISO 8601 format.
    """
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())

def submit_code(api: API, config: Config):
    """Submit the access code to the API and display the result on the LCD.
    
    Args:
        api (API): The API instance.
        code (str): The 6-digit access code.
    """
    sent = get_current_time()
    device_id = "HGC123"  # Replace with your actual device ID
    sender = "raspberry_pi"
    scope = "navigo"
    date = get_current_time()

    result = api.verify_access_code(config.code, config.device_id, config.sent, config.sender, config.scope, config.date)
    if result and result.get('status') == 'success':
        LCD1602.clear()
        LCD1602.write(0, 0, "Access Granted")
        # Add code to unlock the door
        # TODO: code to unlock
    else:
        LCD1602.clear()
        LCD1602.write(0, 0, "Access Denied")

def clear_input() -> str:
    """Clear the input and reset the LCD instructions.
    
    Returns:
        str: An empty string to reset the entered code.
    """
    LCD1602.clear()
    LCD1602.write(0, 0, 'Enter 6-digit code')
    LCD1602.write(0, 1, 'Then press #')
    return ''

def display_entered_code(code: str):
    """Display the currently entered code on the LCD.
    
    Args:
        code (str): The currently entered code.
    """
    LCD1602.clear()
    LCD1602.write(0, 0, 'Enter code:')
    LCD1602.write(0, 1, code)

def loop(keypad: Keypad, api: API):
    """Main loop to read keypad input and validate via API."""
    entered_code = ''
    while True:
        key = keypad.read()
        if key:
            if key == '#':  # Assuming '#' is used to submit the code
                if len(entered_code) == 6 and entered_code.isdigit():
                    config = Config(
                        sent=get_current_time(),
                        sender="raspberry_pi",
                        scope="navigo",
                        code=entered_code,
                        device_id="HGC123",  # Replace with your actual device ID
                        date=get_current_time()
                    )
                    submit_code(api, config)
                else:
                    LCD1602.clear()
                    LCD1602.write(0, 0, "Invalid Code")
                    LCD1602.write(0, 1, "Code must be 6 digits, followed by '#'")
                entered_code = ''  # Reset entered code
            elif key == '*':  # Assuming '*' is used to clear the input
                entered_code = clear_input()
            else:
                if len(entered_code) < 6:
                    entered_code += key
                    display_entered_code(entered_code)

# def loop(keypad: Keypad, api: API):
#     """Main loop to read keypad input and validate via API."""
#     entered_code = ''
#     while True:
#         key = keypad.read()
#         if key:
#             if key == '#':  # Assuming '#' is used to submit the code
#                 if len(entered_code) == 6 and entered_code.isdigit():
#                     sent = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
#                     device_id = "HGC123"  # Replace with your actual device ID
#                     sender = "raspberry_pi"
#                     scope = "navigo"
#                     date = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())

#                     # TODO: change function name and send config object
#                     result = api.verify_access_code(entered_code, device_id, sent, sender, scope, date)
#                     if result and result.get('status') == 'success':
#                         LCD1602.clear()
#                         LCD1602.write(0, 0, "Access Granted")
#                         # Add code to unlock the door
#                         # TODO: code to unlock
#                     else:
#                         LCD1602.clear()
#                         LCD1602.write(0, 0, "Access Denied")
#                 else:
#                     LCD1602.clear()
#                     LCD1602.write(0, 0, "Invalid Code")
#                     LCD1602.write(0, 0, "Code must be 6 digits, followed by '#'")
#                 entered_code = ''  # Reset entered code
#             elif key == '*':  # Assuming '*' is used to clear the input
#                 entered_code = ''
#                 LCD1602.clear()
#                 LCD1602.write(0, 0, 'Enter 6-digit code')
#                 LCD1602.write(0, 1, 'Then press #')
#             else:
#                 if len(entered_code) < 6:
#                     entered_code += key
#                     LCD1602.clear()
#                     LCD1602.write(0, 0, 'Enter code:')
#                     LCD1602.write(0, 1, entered_code)  # Display entered code

def main() -> None:
    try:
        api_key = get_api_key()
        print("API key: ", api_key)

        api = API(api_key)
        keypad = setup_keypad()
        setup_lcd()
        loop(keypad, api)
    # # Call the API
    # result = api.post_request("https://rc.rely.market/booking/reservations/verifyAccessCode", {'code': access_code})
    # print(result)
    # break
    except KeyboardInterrupt:
        destroy()



if __name__ == "__main__":
    main()
