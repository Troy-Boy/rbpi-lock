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
from kivy.config import Config

# Prevent double input (touch + mouse)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Set window size if you're not running fullscreen
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'fullscreen', '1')  # or 0 if you want windowed

# Optional: Better font scaling for touch
Config.set('graphics', 'dpi', '160')

from credentials import get_api_key, get_boat_id
import RPi.GPIO as GPIO
from kayak import KayakApp
from api import API
import servo as servo

def destroy():
	"""Clean up GPIO resources."""
	servo.destroy()
	GPIO.cleanup()

def set_up():
	servo.setup()

def main() -> None:
	try:
		api_key = get_api_key()
		boat_id = get_boat_id()
		# set_up()
		print("API key: ", api_key)
		print("Boat ID: ", boat_id)
		api = API(api_key)
		app = KayakApp(api, boat_id)
		app.run()
	except KeyboardInterrupt:
		print("Keyboard Interrupt: ", KeyboardInterrupt)
	except Exception as e:
		print("An unknown exception occured", e)
	finally:
		destroy()


if __name__ == "__main__":
	main()
