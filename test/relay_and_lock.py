import RPi.GPIO as GPIO
import time

# Set up the GPIO pin
relay_pin = 26  # Change to your GPIO pin for the relay
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

def activate_relay(duration=1):
    """Activate the relay for a specified duration in seconds."""
    GPIO.output(relay_pin, GPIO.HIGH)  # Energize the relay (lock open)
    time.sleep(duration)
    GPIO.output(relay_pin, GPIO.LOW)  # De-energize the relay (lock closed)

try:
    while True:
        activate_relay(5)  # Activate for 5 seconds
        time.sleep(10)  # Wait for 10 seconds
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
