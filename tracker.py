"""
Manages price tracking - stores and retrieves price history.
Uses a simple JSON file for storage with timestamps for graphing.
"""

import json
import os
from datetime import datetime


# File to store price history
PRICE_FILE = 'price_history.json'


def _load_price_data():
    """Load price data from JSON file."""
    if not os.path.exists(PRICE_FILE):
        return {}

    try:
        with open(PRICE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading price file: {e}")
        return {}


def _save_price_data(data):
    """Save price data to JSON file."""
    try:
        with open(PRICE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error saving price file: {e}")


def get_last_price(url):
    """
    Gets the last known price for a given URL.

    Args:
        url: The ticket URL

    Returns:
        float: The last known price, or None if no price has been stored yet
    """
    data = _load_price_data()
    history = data.get(url, [])

    if not history:
        return None

    return history[-1]['price']


def get_price_history(url):
    """
    Gets the full price history for a given URL.

    Args:
        url: The ticket URL

    Returns:
        list: List of {price, timestamp} dicts, or empty list if none
    """
    data = _load_price_data()
    return data.get(url, [])


def get_all_urls():
    """
    Gets all tracked URLs.

    Returns:
        list: List of all tracked URLs
    """
    data = _load_price_data()
    return list(data.keys())


def save_price(url, price):
    """
    Saves the current price for a given URL with timestamp.

    Args:
        url: The ticket URL
        price: The price to save (float)
    """
    data = _load_price_data()

    if url not in data:
        data[url] = []

    # Add new price entry with timestamp
    data[url].append({
        'price': price,
        'timestamp': datetime.now().isoformat()
    })

    _save_price_data(data)
    print(f"Saved price ${price:.2f} for {url}")


def has_price_dropped(current_price, last_price):
    """
    Checks if the current price is lower than the last known price.

    Args:
        current_price: The current price (float)
        last_price: The last known price (float, or None)

    Returns:
        bool: True if price dropped, False otherwise
    """
    if last_price is None:
        return False

    return current_price < last_price
