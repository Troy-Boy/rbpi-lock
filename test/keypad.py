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

# Define GPIO pins for rows and columns of the keypad
# Replace these with the actual GPIO pin numbers you've connected
ROWS = [18, 23, 24, 25]
COLS = [10, 22, 27, 17]

# Define the keys of the keypad
keys = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

def setup():
    GPIO.setmode(GPIO.BCM)

def read_keypad():
    for j in range(len(COLS)):
        GPIO.setup(COLS[j], GPIO.OUT)
        GPIO.output(COLS[j], 0)

    for i in range(len(ROWS)):
        GPIO.setup(ROWS[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    row = -1
    for i in range(len(ROWS)):
        tmpRead = GPIO.input(ROWS[i])
        if tmpRead == 0:
            row = i

    if row < 0 or row >= len(ROWS):
        return None

    for j in range(len(COLS)):
        GPIO.setup(COLS[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    col = -1
    for j in range(len(COLS)):
        tmpRead = GPIO.input(COLS[j])
        if tmpRead == 1:
            col = j

    if col < 0 or col >= len(COLS):
        return None

    return keys[row][col]

def main():
    try:
        setup()
        while True:
            key = read_keypad()
            if key:
                print("Pressed:", key)
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
