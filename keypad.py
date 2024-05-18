"""
keypad.py

Author: Achille Lanctôt-Saumure
GitHub: Troy-Boy
Date created: May 9th, 2024

This module provides a class for interfacing with a keypad.

License: MIT License (https://opensource.org/licenses/MIT)

Dependencies:
- RPi.GPIO library

For questions or assistance, contact Achilles Lanctôt-Saumure at achille.lanctots@gmail.com.

------
in the loop we'll need to  verify that the code is 6 digits with '#' at the end (for submit). Here are the logical conditions to verify code and sanity, we might want to export to another function for clearer code.

* if a non-digit key is entered before we have 6 digits, print "invalid character, only digi
"""

import RPi.GPIO as GPIO 
import time
from typing import List

class Keypad:
    """A class for interfacing with a keypad."""

    def __init__(self, rows_pins: List[int], cols_pins: List[int], keys: List[str]):
        """Initialize the Keypad class.
        
        Args:
            rows_pins (List[int]): A list of GPIO pins corresponding to the keypad rows.
            cols_pins (List[int]): A list of GPIO pins corresponding to the keypad columns.
            keys (List[str]): A list of keys representing the keypad layout.
        """

        # Store the GPIO pins and keypad layout
        self.__rows_pins = rows_pins
        self.__cols_pins = cols_pins
        self.__keys = keys
        
        # Configure GPIO settings for the keypad
        GPIO.setwarnings(False)  # Disable GPIO warnings
        GPIO.setmode(GPIO.BCM)   # Use BCM GPIO numbering
        GPIO.setup(self._rows_pins, GPIO.OUT, initial=GPIO.LOW)  # Set rows as output pins, initialize to LOW
        GPIO.setup(self._cols_pins, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set columns as input pins with pull-down resistor
        ### Explanations ###
        # - The rows of the keypad are configured as output pins because they will be driven HIGH or LOW to detect key presses.
        # - The columns of the keypad are configured as input pins with pull-down resistors to detect key presses when a row is activated.
        # - GPIO.setmode(GPIO.BCM) specifies that we are using BCM (Broadcom) pin numbering, which is the default for Raspberry Pi.
        # - GPIO.setup() is used to configure GPIO pins for input or output mode and to set their initial state.
        # - pull_up_down=GPIO.PUD_DOWN specifies that the input pins should have a pull-down resistor enabled, which helps to ensure stable readings.

    def read(self) -> str:
        """Read the pressed key from the keypad.
        
        Returns:
            str: The pressed key, or an empty string if no key is pressed.
        """
        pressed_key = ''
       
        # Iterate over each row of the keypad
        for i, row in enumerate(self.__rows_pins):
            GPIO.output(row, GPIO.HIGH)  # Activate the current row

            # Iterate over each column of the keypad
            for j, col in enumerate(self.__cols_pins):
                index = i * len(self.__cols_pins) + j  # Calculate the index of the current key
                if GPIO.input(col) == 1:  # Check if the current key is pressed (input is HIGH)
                    pressed_key = self.__keys[index]  # Store the pressed key
            GPIO.output(row, GPIO.LOW)  # Deactivate the current row

        return pressed_key
