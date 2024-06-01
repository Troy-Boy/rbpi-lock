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
        save_value(value=api_key, section="API_KEY", name="api_key")
        return api_key

def save_value(value: str, section: str, name: str) -> None:
    """Save the value to the configuration file.
    
    Args:
        value (str): The value to be saved.
        section (str): The section of the value.
        name (str): The name of the value.
    """
    config = configparser.ConfigParser()
    config[section] = {name: value}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def get_boat_id() -> str:
    """Gets the boat id from the config.ini file or add it if not there.

    Returns:
        str: the boat id
    """
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config['BOAT_IDS']['boat_id']
    except (KeyError, FileNotFoundError):
        print("No API key found in config.ini or config.ini not found.")
        boat_id = input("Please enter your boat id: ")
        save_value(value=boat_id, section="BOAT_IDS", name="boat_id")
        return boat_id
