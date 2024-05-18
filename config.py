"""
config.py

Author: Achille Lanctôt-Saumure
GitHub: Troy-Boy
Date created: May 12th, 2024

This file defines a configuration class for API requests.

License: MIT License (https://opensource.org/licenses/MIT)

Dependencies:
- Python 3.10+

For questions or assistance, contact Achilles Lanctôt-Saumure at achille.lanctots@gmail.com.
"""

from dataclasses import dataclass

@dataclass
class Config:
    sent: str
    sender: str
    scope: str
    code: str
    device_id: str
    date: str
