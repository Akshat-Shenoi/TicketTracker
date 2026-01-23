"""
Sends email notifications when ticket prices drop.
Uses Python's built-in smtplib - completely free!
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config


def send_price_alert(email_address, subject, message):
    """
    Sends an email alert using SMTP (Gmail, Outlook, etc.).
    
    Args:
        email_address: The email address to send to
        subject: The email subject line
        message: The message text to send
        
    Returns:
        bool: True if message sent successfully, False otherwise
    """
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = config.EMAIL_FROM
        msg['To'] = email_address
        msg['Subject'] = subject
        
        # Add the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to the email server and send
        # Using Gmail's SMTP server (works with Gmail, Google Workspace, etc.)
        # For Outlook, use smtp-mail.outlook.com:587
        smtp_server = config.SMTP_SERVER
        smtp_port = config.SMTP_PORT
        
        print(f"Sending email to {email_address}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable encryption
        server.login(config.EMAIL_FROM, config.EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent successfully to {email_address}!")
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        print("Make sure your email credentials are correct in the .env file.")
        return False


def create_price_alert_message(ticket_url, current_price, last_price):
    """
    Creates a formatted message for price drop alerts.
    
    Args:
        ticket_url: The Ticketmaster URL
        current_price: The current (lower) price
        last_price: The previous (higher) price
        
    Returns:
        tuple: (subject, message_body) for the email
    """
    price_drop = last_price - current_price
    savings_percent = (price_drop / last_price) * 100
    
    subject = f"🎵 Ticket Price Drop Alert! Save ${price_drop:.2f} 🎵"
    
    message = f"Ticket Price Drop Alert!\n\n"
    message += f"Current price: ${current_price:.2f}\n"
    message += f"Previous price: ${last_price:.2f}\n"
    message += f"You save: ${price_drop:.2f} ({savings_percent:.1f}%)\n\n"
    message += f"Check it out: {ticket_url}"
    
    return subject, message
