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
from datetime import datetime, timezone

class API:
	"""A class for making HTTP requests to an API."""

	def __init__(self, api_key: str):
		"""Initialize the API class.

		Args:
			api_key (str): The API key used for authentication.
		"""
		self.__api_key = api_key
		self.__headers = {'Content-Type': 'application/json', 'x-api-key': self.__api_key}

	def post_request(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
		"""
		Make a POST request to the specified URL with proper error handling.

		Args:
			url (str): The URL to send the request to.
			data (Dict[str, Any]): The request payload.

		Returns:
			Dict[str, Any]: A structured response with `success`, `status_code`, and `data` or `error`.
		"""
		try:
			response = requests.post(url, json=data, headers=self.__headers)
			
			result = {
				"success": response.ok,  # True if 2XX, False otherwise
				"status_code": response.status_code
			}

			# Try to parse JSON, otherwise return raw response
			try:
				result["data"] = response.json()
			except requests.exceptions.JSONDecodeError:
				result["error"] = "Response is not valid JSON"
				result["data"] = None
			
			return result
		
		except requests.exceptions.RequestException as e:
			#Handle network failures, timeouts, etc.
			return {
				"success": False,
				"status_code": None,
				"error": str(e),
				"data": None
			}

	# TODO: change function name and send config object
	def verify_access_code(self, access_code: str, boat_id: str, sender: str="raspberry_pi", scope: str="navigo") -> Dict[str, Any]:
		"""
		Verify an access code using the API.

		Returns:
			Dict[str, Any]: A structured response indicating success/failure.
		"""
		url = "https://rc.rely.market/booking/reservations/verifyAccessCode"
		data = {
			"sent": get_current_time(),
			"sender": sender,
			"scope": scope,
			"data": {
				"code": access_code,
				"deviceId": boat_id,
				"date": get_current_time()
			}
		}

		response = self.post_request(url, data)

		# Extra error handling (e.g., specific handling for 404)
		if not response["success"]:
			if response["status_code"] == 404:
				response["error"] = "Access code not found."
			elif response["status_code"] == 500:
				response["error"] = "Server error. Please try again."
		
		return response
		

def get_current_time() -> str:
	"""Get the current time in ISO format.
	
	Returns:
		str: The current time in ISO 8601 format.
	"""
	current_time = datetime.now(timezone.utc)
	current_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
	return current_time