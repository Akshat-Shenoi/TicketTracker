# Deployment Guide - Railway

This guide will help you deploy the ticket tracker bot to Railway so it runs 24/7 with a web dashboard to view price graphs.

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right → "New repository"
3. Name it `TicketTracker` (or anything you want)
4. Make it **Public** (required for free Railway tier)
5. Click "Create repository"
6. **Don't** initialize with README (we already have files)

## Step 2: Push Your Code to GitHub

Run these commands in your terminal (from the TicketTracker directory):

```bash
cd /Users/as/Documents/TicketTracker

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Ticket price tracker bot"

# Add your GitHub repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/TicketTracker.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Railway

1. Go to [railway.app](https://railway.app) and sign up (use "Sign in with GitHub")
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `TicketTracker` repository
5. Railway will automatically detect it's a Python project

## Step 4: Configure Environment Variables

**IMPORTANT: On Railway, you set environment variables in the dashboard, NOT in a .env file!**

1. In your Railway project, click on your service
2. Go to the **"Variables"** tab
3. Add these environment variables (click "New Variable" for each):

| Variable | Value | Description |
|----------|-------|-------------|
| `EVENT_URL` | `https://www.vividseats.com/...` | The ticket URL to monitor |
| `MY_EMAIL` | `your-email@gmail.com` | Your email (send & receive alerts) |
| `EMAIL_PASSWORD` | `your_app_password` | Gmail App Password (see below) |
| `CHECK_INTERVAL_HOURS` | `4` | How often to check (in hours) |

Optional variables (have defaults):
| `SMTP_SERVER` | `smtp.gmail.com` | SMTP server |
| `SMTP_PORT` | `587` | SMTP port |

### Getting a Gmail App Password

Gmail requires an "App Password" (not your regular password):

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification if not already enabled
3. Go to "App passwords" (search for it in your Google Account settings)
4. Create a new app password for "Mail"
5. Copy the 16-character password and use it for `EMAIL_PASSWORD`

## Step 5: Deploy and Access Dashboard

Railway will automatically deploy your app as a **web service**. After deployment:

1. Go to your service in Railway
2. Click on "Settings" → "Networking" → "Generate Domain"
3. Railway will give you a URL like `your-app.railway.app`
4. Visit this URL to see your **price graph dashboard**!

The dashboard shows:
- Current price
- Lowest/highest price recorded
- Interactive price history graph
- Number of data points collected

## Step 6: Verify It's Working

1. Check the "Logs" tab in Railway to see the bot running
2. You should see messages like:
   ```
   Ticket Price Tracker Bot
   Starting price checker in background...
   Starting dashboard on port 5000...
   Checking price for: https://...
   ```
3. Visit your Railway URL to see the dashboard
4. The graph will populate as the bot collects more price data over time

## Troubleshooting

### "Missing required configuration" error
Make sure all environment variables are set in Railway's Variables tab. Railway does NOT use .env files - you must set each variable in the dashboard.

### Email not sending
1. Make sure you're using a Gmail **App Password**, not your regular password
2. Check that `EMAIL_FROM` matches the Gmail account that created the App Password
3. Verify 2-Step Verification is enabled on your Google account

### Dashboard not loading
1. Make sure you generated a domain in Railway settings
2. Check the logs for any startup errors
3. Ensure the `PORT` environment variable is NOT set manually (Railway sets this automatically)

### Price not found / scraping errors
Check the logs to see what the scraper is returning. The ticket page structure may have changed.

## Free Tier Limits

Railway's free tier includes:
- $5 credit per month (plenty for this bot)
- 500 hours of usage
- Your bot should run 24/7 within these limits

## Optional: Disable Dashboard

If you only want the price checker without the dashboard, add this variable:
```
ENABLE_DASHBOARD=false
```

This will run the bot as a background worker only.

## Alternative: Render

If Railway doesn't work, try [Render.com](https://render.com):
1. Sign up with GitHub
2. Create a new "Web Service"
3. Connect your GitHub repo
4. Add environment variables
5. Set start command: `python main.py`
6. Deploy!
