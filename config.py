"""
Configuration settings for the price tracker bot.
Loads settings from environment variables for security.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Vivid Seats URL to monitor (or any ticket vendor URL)
EVENT_URL = os.getenv('EVENT_URL', '')

# Your email address for receiving alerts
MY_EMAIL = os.getenv('MY_EMAIL', '')

# Email settings for sending notifications
# Use your Gmail address (or any email that supports SMTP)
EMAIL_FROM = os.getenv('EMAIL_FROM', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')  # Use an app password, not your regular password

# SMTP server settings
# Default is Gmail, but you can use other providers
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))

# How often to check prices (in hours)
CHECK_INTERVAL_HOURS = float(os.getenv('CHECK_INTERVAL_HOURS', '4'))

# Convert hours to seconds for time.sleep()
CHECK_INTERVAL_SECONDS = CHECK_INTERVAL_HOURS * 3600


def validate_config():
    """
    Check that all required configuration values are set.
    Returns True if valid, False otherwise.
    """
    required_vars = [
        ('EVENT_URL', EVENT_URL),
        ('MY_EMAIL', MY_EMAIL),
        ('EMAIL_FROM', EMAIL_FROM),
        ('EMAIL_PASSWORD', EMAIL_PASSWORD),
    ]
    
    missing = []
    for name, value in required_vars:
        if not value:
            missing.append(name)
    
    if missing:
        print(f"Error: Missing required configuration: {', '.join(missing)}")
        print("Please check your .env file.")
        return False
    
    return True
