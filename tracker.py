"""
Manages price tracking - stores and retrieves the last known price.
Uses a simple JSON file for storage.
"""

import json
import os


# File to store the last known price
PRICE_FILE = 'last_price.json'


def get_last_price(url):
    """
    Gets the last known price for a given URL.
    
    Args:
        url: The Ticketmaster URL
        
    Returns:
        float: The last known price, or None if no price has been stored yet
    """
    # If the file doesn't exist, return None (no previous price)
    if not os.path.exists(PRICE_FILE):
        return None
    
    try:
        with open(PRICE_FILE, 'r') as f:
            price_data = json.load(f)
            # Return the price for this URL, or None if not found
            return price_data.get(url)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading price file: {e}")
        return None


def save_price(url, price):
    """
    Saves the current price for a given URL.
    
    Args:
        url: The Ticketmaster URL
        price: The price to save (float)
    """
    # Load existing data or create new dict
    price_data = {}
    if os.path.exists(PRICE_FILE):
        try:
            with open(PRICE_FILE, 'r') as f:
                price_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            # If file is corrupted, start fresh
            price_data = {}
    
    # Update with new price
    price_data[url] = price
    
    # Save back to file
    try:
        with open(PRICE_FILE, 'w') as f:
            json.dump(price_data, f, indent=2)
        print(f"Saved price ${price:.2f} for {url}")
    except IOError as e:
        print(f"Error saving price file: {e}")


def has_price_dropped(current_price, last_price):
    """
    Checks if the current price is lower than the last known price.
    
    Args:
        current_price: The current price (float)
        last_price: The last known price (float, or None)
        
    Returns:
        bool: True if price dropped, False otherwise
    """
    # If we don't have a previous price, this is the first check
    # We'll consider this as "no drop" since there's nothing to compare
    if last_price is None:
        return False
    
    # Price dropped if current is less than last
    return current_price < last_price
