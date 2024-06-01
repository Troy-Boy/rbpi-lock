import RPi.GPIO as GPIO
import time

# GPIO pin where the relay is connected
relay_pin = 26

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

def activate_relay(duration=5):
    GPIO.output(relay_pin, GPIO.HIGH)  # Energize the relay
    print("Relay activated, lock should be open.")
    time.sleep(duration)  # Keep it energized for 'duration' seconds
    GPIO.output(relay_pin, GPIO.LOW)   # De-energize the relay
    print("Relay deactivated, lock should be closed.")

try:
    while True:
        activate_relay(5)  # Activate the relay for 5 seconds
        time.sleep(10)  # Wait for 10 seconds before the next cycle
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
