#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

SERVO_PIN = 18           # GPIO pin connected to servo
FREQUENCY = 50           # 50Hz for standard servo
MIN_DUTY = 2.5           # ~0°
MAX_DUTY = 12.5          # ~180°

def set_angle(pwm, angle):
    """Set servo to angle between 0 and 180."""
    angle = max(0, min(180, angle))
    duty = MIN_DUTY + (angle / 180.0) * (MAX_DUTY - MIN_DUTY)
    pwm.ChangeDutyCycle(duty)
    print(f"→ Moved to {angle}° (duty: {duty:.2f})")
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # Avoid jitter

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    pwm = GPIO.PWM(SERVO_PIN, FREQUENCY)
    pwm.start(0)

    try:
        print("Moving to 0°...")
        set_angle(pwm, 0)
        time.sleep(1)

        print("Rotating to 180°...")
        set_angle(pwm, 180)
        time.sleep(1)

    finally:
        print("Cleaning up")
        pwm.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    main()
