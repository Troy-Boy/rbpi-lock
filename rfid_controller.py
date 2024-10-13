import time
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import threading

class RFIDReader:
    def __init__(self, callback):
        self.reader = SimpleMFRC522()
        self.callback = callback
        self.running = True
        self.thread = threading.Thread(target=self.read_rfid)
        self.thread.start()

    def read_rfid(self):
        while self.running:
            try:
                print("Waiting for RFID tag...")
                _id, text = self.reader.read()
                print(f"RFID ID: {_id}\nText: {text}")
                if text:
                    self.callback(text.strip())
                time.sleep(1)
            except Exception as e:
                print(f"Error reading RFID: {e}")
                time.sleep(1)

    def stop(self):
        self.running = False
        self.thread.join()
        GPIO.cleanup()
