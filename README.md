# Concert Ticket Price Tracker Bot

A simple Python bot that monitors Vivid Seats concert ticket prices and sends email notifications when prices drop. **100% free - no paid services required!**

## Features

- Monitors Vivid Seats URLs for price changes
- Tracks the lowest available ticket price
- Sends email alerts when prices drop (completely free!)
- Runs continuously with configurable check intervals
- Simple, readable code

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Email (Gmail Example)

For Gmail users:
1. Go to your Google Account settings
2. Enable 2-Step Verification (required for app passwords)
3. Go to Security → App passwords
4. Generate a new app password for "Mail"
5. Copy the 16-character password (you'll use this in .env)

For other email providers:
- Outlook: Use `smtp-mail.outlook.com:587`
- Yahoo: Use `smtp.mail.yahoo.com:587`
- Check your provider's SMTP settings

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
EVENT_URL=https://www.vividseats.com/your-event-url
MY_EMAIL=your-email@gmail.com
EMAIL_FROM=your-email@gmail.com
EMAIL_PASSWORD=your_app_password_here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
CHECK_INTERVAL_HOURS=4
```

### 4. Run Locally

```bash
python main.py
```

### 5. Deploy to Cloud (Optional)

For 24/7 operation, deploy to Railway or Render:

1. Create a new project on Railway/Render
2. Connect your GitHub repository
3. Add environment variables in the platform's dashboard
4. Deploy!

## How It Works

1. The bot scrapes the Vivid Seats page for the lowest ticket price
2. Compares it with the last known price (stored in `last_price.json`)
3. If the price dropped, sends an email notification
4. Updates the stored price
5. Waits for the configured interval and repeats

## Files

- `main.py` - Main entry point with scheduling loop
- `scraper.py` - Scrapes Vivid Seats for ticket prices
- `tracker.py` - Manages price storage and comparison
- `notifier.py` - Handles email notifications (free, no external service needed!)
- `config.py` - Configuration management

## Why Vivid Seats?

Vivid Seats is more accessible than Ticketmaster and doesn't have the same aggressive anti-scraping measures. The bot can reliably fetch prices from Vivid Seats pages without getting blocked.
