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
from datetime import datetime
from credentials import get_api_key, get_boat_id
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
    rows_pins = [5, 6, 13, 19]  # GPIO pins for the rows of the keypad
    cols_pins = [12, 16, 20, 21]  # GPIO pins for the columns of the keypad
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


def display_scrolling_message(message: str, row: int, delay: float):
    """Display a scrolling message on the LCD screen.
    
    Args:
        message (str): The message to display.
        row (int): The row on which to display the message (0 or 1).
        delay (float): The delay between each scroll step in seconds.
    """
    lcd_width = 16  # LCD width in characters
    display = message + ' ' * lcd_width

    for i in range(len(display) - lcd_width + 1):
        LCD1602.write(0, row, display[i:i + lcd_width])
        time.sleep(delay)


def destroy():
    """Clean up GPIO resources."""
    LCD1602.clear()
    GPIO.cleanup()


def get_current_time() -> str:
    """Get the current time in ISO format.
    
    Returns:
        str: The current time in ISO 8601 format.
    """
    current_time = datetime.utcnow()
    current_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return current_time


def submit_code(api: API, config: Config) -> int:
    """Submit the access code to the API and display the result on the LCD.
    
    Args:
        api (API): The API instance.
        code (str): The 6-digit access code.
    Returns:
        int: response https status.
    """
    response = api.verify_access_code(config.code, config.device_id, config.sent, config.sender, config.scope, config.date)
    if response and response.status_code == 201:
        LCD1602.clear()
        LCD1602.write(0, 0, "Access Granted")
    else:
        LCD1602.clear()
        LCD1602.write(0, 0, "Access Denied")
        LCD1602.write(0, 1, "Press * to clear")
    return response.status_code


# def clear_input() -> str:
#     """Clear the input and reset the LCD instructions.
    
#     Returns:
#         str: An empty string to reset the entered code.
#     """
#     LCD1602.clear()
#     LCD1602.write(0, 0, "Enter 6-digit code")
#     LCD1602.write(0, 1, "Then press #")
#     return ''


def display_entered_code(code: str):
    """Display the currently entered code on the LCD.
    
    Args:
        code (str): The currently entered code.
    """
    LCD1602.clear()
    LCD1602.write(0, 0, 'Enter your code:')
    LCD1602.write(0, 1, code)

def debounce_keypad(keypad: Keypad, debounce_time: float = 0.05) -> str:
    """Debounce the keypad input.
    
    Args:
        keypad (Keypad): The keypad instance.
        debounce_time (float): The debounce time in seconds.
    
    Returns:
        str: The debounced key press.
    """
    key = None
    while key is None:
        key = keypad.read()
        if key:
            time.sleep(debounce_time)  # Wait for debounce time
            if key == keypad.read():  # Confirm it's the same key after debounce time
                return key
        time.sleep(0.01)  # Small delay to prevent high CPU usage


def loop(keypad: Keypad, api: API, boat_id: str):
    """Loop on the keypad to read the input, then displays it on the LCD.

    Args:
        keypad (Keypad): Keypad object
        api (API): API object
        boat_id (str): Boat unique identifier
    """
    entered_code = ""
    scrolling = True
    message = '#:send *:clear'
    LCD1602.clear()
    LCD1602.write(0, 0, "Enter your code:")
    LCD1602.write(0, 1, message)
    while True:
        # if scrolling:
        #     display_scrolling_message(message, 1, 0.3)
        #     if keypad.read():
        #         scrolling = False
        #         LCD1602.clear()
        #         LCD1602.write(0, 0, "Enter code:")
        
        # key = debounce_keypad(keypad)
        key = debounce_keypad(keypad)
        if key:
            print('read key: ', key)
            if key == '#':  # Assuming '#' is used to submit the code
                if len(entered_code) == 6 and entered_code.isdigit():
                    config = Config(
                        sent=get_current_time(),
                        sender="raspberry_pi",
                        scope="navigo",
                        code=str(entered_code),
                        device_id=boat_id,  # Replace with your actual device ID
                        date=get_current_time()
                    )
                    status = submit_code(api, config)
                    print("status: ", status)
                    print("YESSSS SIR ITS OPPPPPEEEEN")
                    break
                else:
                    LCD1602.clear()
                    LCD1602.write(0, 0, "Invalid Code")
                    LCD1602.write(0,1, "Press * to clear")
                    time.sleep(1)
                entered_code = ""  # Reset entered code
            elif key == '*':  # Assuming '*' is used to clear the input
                entered_code = ""
                LCD1602.clear()
                LCD1602.write(0, 0, "Enter your code:")
                LCD1602.write(0, 1, message)
            else:
                if len(entered_code) < 6:
                    entered_code += key
                    display_entered_code(entered_code)

def main() -> None:
    try:
        api_key = get_api_key()
        boat_id = get_boat_id()
        print("API key: ", api_key)
        print("Boat ID: ", boat_id)
        api = API(api_key)
        keypad = setup_keypad()
        setup_lcd()
        loop(keypad, api, boat_id=boat_id)
    except KeyboardInterrupt:
        print("Keyboard Interrupt: ", KeyboardInterrupt)
    except Exception as e:
        print("An unknown exception occured", e)
    finally:
        destroy()



if __name__ == "__main__":
    main()
