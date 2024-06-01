"""
keypad.py

Author: Achille Lanctôt-Saumure
GitHub: Troy-Boy
Date created: May 5th, 2024

This script tests the keypad for sanity checks.

License: MIT License (https://opensource.org/licenses/MIT)

Dependencies:
- Python 3.10+

For questions or assistance, contact Achilles Lanctôt-Saumure at achille.lanctots@gmail.com.
"""


import RPi.GPIO as GPIO
import time

class Keypad:
    def __init__(self, row_pins, col_pins, keys):
        self.row_pins = row_pins
        self.col_pins = col_pins
        self.keys = keys
        self.keypad_matrix = [
            keys[i:i + len(col_pins)] for i in range(0, len(keys), len(col_pins))
        ]
        self.setup_pins()

    def setup_pins(self):
        GPIO.setmode(GPIO.BCM)
        for row_pin in self.row_pins:
            GPIO.setup(row_pin, GPIO.OUT)
            GPIO.output(row_pin, GPIO.LOW)
        for col_pin in self.col_pins:
            GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_key(self):
        for row_num, row_pin in enumerate(self.row_pins):
            GPIO.output(row_pin, GPIO.HIGH)
            for col_num, col_pin in enumerate(self.col_pins):
                if GPIO.input(col_pin) == GPIO.LOW:
                    GPIO.output(row_pin, GPIO.LOW)
                    return self.keypad_matrix[row_num][col_num]
            GPIO.output(row_pin, GPIO.LOW)
        return None

def main():
    rows_pins = [5, 6, 13, 19]
    cols_pins = [12, 16, 20, 21]
    keys = [
        "1", "2", "3", "A",
        "4", "5", "6", "B",
        "7", "8", "9", "C",
        "*", "0", "#", "D"
    ]
    keypad = Keypad(rows_pins, cols_pins, keys)

    print("Press keys on the keypad. Press Ctrl+C to exit.")
    try:
        while True:
            key = keypad.read_key()
            if key:
                print(f"Key pressed: {key}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()