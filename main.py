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

from config import Config
from datetime import datetime, timezone
from credentials import get_api_key, get_boat_id
# import RPi.GPIO as GPIO
from kayak import KayakApp
from api import API

def destroy():
    """Clean up GPIO resources."""
    # LCD1602.clear()
    # GPIO.cleanup()


def get_current_time() -> str:
    """Get the current time in ISO format.
    
    Returns:
        str: The current time in ISO 8601 format.
    """
    current_time = datetime.now(timezone.utc)
    current_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return current_time


# def submit_code(api: API, config: Config) -> int:
#     """Submit the access code to the API and display the result on the LCD.
    
#     Args:
#         api (API): The API instance.
#         code (str): The 6-digit access code.
#     Returns:
#         int: response https status.
#     """
#     response = api.verify_access_code(config.code, config.device_id, config.sent, config.sender, config.scope, config.date)
#     if response:
#         LCD1602.clear()
#         LCD1602.write(0, 0, "Access Granted")
#     else:
#         LCD1602.clear()
#         LCD1602.write(0, 0, "Access Denied")
#         LCD1602.write(0, 1, "Press * to clear")
#     return response.status_code

def main() -> None:
    try:
        api_key = get_api_key()
        boat_id = get_boat_id()
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
