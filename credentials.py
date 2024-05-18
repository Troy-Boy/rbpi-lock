"""
credentials.py

Author: Achille Lanctôt-Saumure
GitHub: Troy-Boy
Date created: May 5th, 2024

This module contains functions for retrieving and saving API keys.

License: MIT License (https://opensource.org/licenses/MIT)

Dependencies:
- Python 3.10+
- configparser library

For questions or assistance, contact Achilles Lanctôt-Saumure at achille.lanctots@gmail.com.
"""

import configparser

def get_api_key() -> str:
    """Retrieve the API key from the configuration file.
    
    Returns:
        str: The API key.
    """
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config['API_KEYS']['api_key']
    except (KeyError, FileNotFoundError):
        print("No API key found in config.ini or config.ini not found.")
        api_key = input("Please enter your API key: ")
        save_api_key(api_key)
        return api_key

def save_api_key(api_key: str) -> None:
    """Save the API key to the configuration file.
    
    Args:
        api_key (str): The API key to be saved.
    """
    config = configparser.ConfigParser()
    config['API_KEYS'] = {'api_key': api_key}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
