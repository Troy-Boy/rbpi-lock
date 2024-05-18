"""
api.py

Author: Achille Lanctôt-Saumure
GitHub: Troy-Boy
Date created: May 5th, 2024

This class provides a class for making HTTP requests to an API.

License: MIT License (https://opensource.org/licenses/MIT)

Dependencies:
- Python 3.10+
- requests library

For questions or assistance, contact Achilles Lanctôt-Saumure at achille.lanctots@gmail.com.
"""

import requests
from typing import Optional, Dict, Any

class API:
    """A class for making HTTP requests to an API."""

    def __init__(self, api_key: str):
        """Initialize the API class.

        Args:
            api_key (str): The API key used for authentication.
        """
        self.__api_key = api_key
        self.__headers = {'Content-Type': 'application/json', 'x-api-key': self.__api_key}

    def post_request(self, url: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make a POST request to the specified URL with the provided data.

        Args:
            url (str): The URL to send the POST request to.
            data (Dict[str, Any]): The data to include in the request body.

        Returns:
            Optional[Dict[str, Any]]: The JSON response from the API, or None if an error occurs.
        """
        try:
            response = requests.post(url, json=data, headers=self.__headers)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error:", e)

# TODO: change function name and send config object
    def verify_access_code(self, access_code: str, device_id: str, sent: str, sender: str, scope: str, date: str) -> Optional[Dict[str, Any]]:
        """
        Verify the access code with the given parameters.

        Args:
            access_code (str): The access code to verify.
            device_id (str): The device ID.
            sent (str): The timestamp when the request is sent.
            sender (str): The sender of the request.
            scope (str): The scope of the request.
            date (str): The date for the request.

        Returns:
            Optional[Dict[str, Any]]: The response from the API.
        """
        url = "https://rc.rely.market/booking/reservations/verifyAccessCode"
        data = {
            "sent": sent,
            "sender": sender,
            "scope": scope,
            "data": {
                "code": access_code,
                "deviceId": device_id,
                "date": date
            }
        }
        return self.post_request(url, data)
