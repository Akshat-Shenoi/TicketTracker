"""
Main entry point for the Ticketmaster price tracker bot.
Runs both the price checker and web dashboard.
"""

import time
import threading
import os
import config
import scraper
import tracker
import notifier


def check_price():
    """
    Main function that checks the price, compares it, and sends alerts if needed.
    This is called repeatedly by the main loop.
    """
    url = config.EVENT_URL

    print(f"\n{'='*60}")
    print(f"Checking price for: {url}")
    print(f"{'='*60}")

    # Step 1: Get the current lowest price from Ticketmaster
    current_price = scraper.get_lowest_price(url)

    if current_price is None:
        print("Could not get current price. Will try again next check.")
        return

    # Step 2: Get the last known price from storage
    last_price = tracker.get_last_price(url)

    if last_price is None:
        # This is the first time checking - just save the price
        print(f"First check! Saving initial price: ${current_price:.2f}")
        tracker.save_price(url, current_price)
        return

    # Step 3: Compare prices
    print(f"Current price: ${current_price:.2f}")
    print(f"Last price: ${last_price:.2f}")

    if tracker.has_price_dropped(current_price, last_price):
        # Price dropped! Send alert
        price_drop = last_price - current_price
        print(f"Price dropped by ${price_drop:.2f}!")

        # Create and send email alert
        subject, message = notifier.create_price_alert_message(url, current_price, last_price)
        notifier.send_price_alert(config.MY_EMAIL, subject, message)

        # Save the new lower price
        tracker.save_price(url, current_price)
    elif current_price < last_price:
        # Price is lower but we already handled this above
        # This shouldn't happen, but just in case
        tracker.save_price(url, current_price)
    else:
        # Price stayed the same or increased
        print(f"Price unchanged or increased. No alert needed.")
        # Update stored price to current (in case it went up, we want to track that)
        tracker.save_price(url, current_price)


def run_price_checker():
    """
    Background thread that runs the price checker continuously.
    """
    # Run the first check immediately
    check_price()

    # Then run checks at regular intervals
    while True:
        wait_seconds = config.CHECK_INTERVAL_SECONDS
        wait_hours = wait_seconds / 3600
        print(f"\nWaiting {wait_hours:.1f} hours until next check...")
        time.sleep(wait_seconds)
        check_price()


def main():
    """
    Main function that starts both the tracker and dashboard.
    """
    print("="*60)
    print("Ticket Price Tracker Bot")
    print("="*60)

    # Validate configuration before starting
    if not config.validate_config():
        print("\nPlease fix your configuration and try again.")
        return

    print(f"\nConfiguration loaded:")
    print(f"  Event URL: {config.EVENT_URL}")
    print(f"  Email: {config.MY_EMAIL}")
    print(f"  Check interval: {config.CHECK_INTERVAL_HOURS} hours")

    # Check if we should run the dashboard
    enable_dashboard = os.environ.get('ENABLE_DASHBOARD', 'true').lower() == 'true'

    if enable_dashboard:
        # Import dashboard here to avoid circular imports
        from dashboard import app

        # Start price checker in background thread
        print("\nStarting price checker in background...")
        checker_thread = threading.Thread(target=run_price_checker, daemon=True)
        checker_thread.start()

        # Run dashboard in main thread (required for Railway)
        port = int(os.environ.get('PORT', 5000))
        print(f"\nStarting dashboard on port {port}...")
        print(f"View your price graph at: http://localhost:{port}")
        app.run(host='0.0.0.0', port=port)
    else:
        # Just run the price checker (no dashboard)
        print(f"\nStarting price monitoring (no dashboard)...")
        print(f"Press Ctrl+C to stop\n")

        try:
            run_price_checker()
        except KeyboardInterrupt:
            print("\n\nStopping price tracker. Goodbye!")
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Restart the bot to continue monitoring.")


if __name__ == "__main__":
    main()
