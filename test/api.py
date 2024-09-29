import requests
from datetime import datetime, timezone

def get_current_time() -> str:
    """Get the current time in ISO format.
    
    Returns:
        str: The current time in ISO 8601 format.
    """
    current_time = datetime.now(timezone.utc)
    current_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return current_time

def verify_access_code(
        api_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbnYiOiJwcm9kdWN0aW9uIiwic2NvcGUiOiJuYXZpZ28iLCJjbGllbnQiOjQxNywia2V5IjoiczBzYUZyN3FESkgtaVhla1JpLTdKIiwiaWF0IjoxNzE1NzUzODQyLCJleHAiOjE3NDgyMTc2MDB9.ENeAaxn41Ism61izwtoH-r-hautzwOp4D9VmTIgKULM",
        code: str = "831228",
        device_id: str = "IGK3194003c6dv") -> None:
    """Make a POST request to verify the access code.
    
    Args:
        api_key (str): The API key for authentication.
        code (str): The access code to verify.
        device_id (str): The device ID.
    """
    url = "https://rc.rely.market/booking/reservations/verifyAccessCode"
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }
    data = {
        "sent": get_current_time(),
        "sender": "raspberry_pi",
        "scope": "navigo",
        "data": {
            "code": code,
            "deviceId": device_id,
            "date": get_current_time()
        }
    }

    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response}")

if __name__ == "__main__":
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbnYiOiJwcm9kdWN0aW9uIiwic2NvcGUiOiJuYXZpZ28iLCJjbGllbnQiOjQxNywia2V5IjoiczBzYUZyN3FESkgtaVhla1JpLTdKIiwiaWF0IjoxNzE1NzUzODQyLCJleHAiOjE3NDgyMTc2MDB9.ENeAaxn41Ism61izwtoH-r-hautzwOp4D9VmTIgKULM"
    code = "666666"  # Replace with the code you want to test
    device_id = "IGK3194003c6dv"  # Replace with your actual device ID

    verify_access_code()
