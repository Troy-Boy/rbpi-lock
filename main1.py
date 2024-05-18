import requests
import configparser


def call_api(access_code, api_key):
    """Calls the rely API with the given API key and configuration.

    Args:
        access_code (string): Access code for a Navigo lock.
        api_key (string): API key 

    Returns:
        Object: return the API response
    """
    url = "https://rc.rely.market/booking/reservations/verifyAccessCode"
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }
    data = {
        'code': access_code
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error:", e)


def validate_access_code(access_code):
    if not access_code.isdigit():
        return False
    if len(access_code) != 6:
        return False
    return True

def get_api_key():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        api_key = config['API_KEYS']['api_key']
        return api_key
    except (KeyError, FileNotFoundError):
        print("No API key found in config.ini or config.ini not found.")
        api_key = input("Please enter your API key: ")
        # Optionally, you can save the API key to the config.ini file for future use
        save_api_key(api_key)
        return api_key


def save_api_key(api_key):
    config = configparser.ConfigParser()
    config['API_KEYS'] = {'api_key': api_key}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def main():
    api_key = get_api_key()
    print("API key: ", api_key)

    while True:
        # Get access code from user input
        access_code = input("Enter the access code: ")

        # Validate the access code
        if not validate_access_code(access_code):
            print("Invalid access code. Access code must contain exactly 6 digits and no other characters.")
            continue

        # Call the API
        result = call_api(access_code, api_key)
        print(result)
        break

if __name__ == "__main__":
    main()
