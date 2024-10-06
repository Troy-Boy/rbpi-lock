import RPi.GPIO as GPIO
import time

# Define the GPIO pins for rows and columns
row_pins = [5, 6, 13, 19]
col_pins = [12, 16, 20, 21]


def setup_pins():
    GPIO.setmode(GPIO.BCM)
    for row_pin in row_pins:
        GPIO.setup(row_pin, GPIO.OUT)
        GPIO.output(row_pin, GPIO.LOW)
    for col_pin in col_pins:
        GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def test_keypad():
    setup_pins()
    try:
        while True:
            for row_pin in row_pins:
                GPIO.output(row_pin, GPIO.HIGH)
                for col_pin in col_pins:
                    if GPIO.input(col_pin) == GPIO.LOW:
                        print(f"Key detected at Row {row_pins.index(row_pin) + 1}, Col {col_pins.index(col_pin) + 1}")
                GPIO.output(row_pin, GPIO.LOW)
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    test_keypad()
