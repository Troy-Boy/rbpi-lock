#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500
SERVO_PIN = 18

p = None  # PWM object will be initialized in setup()

def map(value, inMin, inMax, outMin, outMax):
    return (outMax - outMin) * (value - inMin) / (inMax - inMin) + outMin

def setup():
    global p
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    p = GPIO.PWM(SERVO_PIN, 50)  # 50Hz
    p.start(0)
    time.sleep(0.5)  # Give the servo time to initialize

def set_angle(angle):
    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    duty_cycle = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Let the servo reach the position
    p.ChangeDutyCycle(0)  # Stop sending signal to avoid buzzing

def unlock_locker():
    try:
        setup()
        print("Unlocking locker (180°)...")
        set_angle(180)  # Move to unlock position
        time.sleep(1)

        # Optional: Reset to locked position after a delay
        print("Locking again (0°)...")
        set_angle(0)
        time.sleep(1)
    finally:
        destroy()

def destroy():
    if p:
        p.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    unlock_locker()
