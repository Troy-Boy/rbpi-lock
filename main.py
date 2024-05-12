import requests

def call_api(access_code, api_key):
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

def main():
    # Get API key from user input
    api_key = input("Enter your API key: ")

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
