# Deployment Guide - Railway (Free)

This guide will help you deploy the ticket tracker bot to Railway so it runs 24/7 for free.

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

1. In your Railway project, click on your service
2. Go to the "Variables" tab
3. Add these environment variables (click "New Variable" for each):

```
EVENT_URL=https://www.vividseats.com/asap-rocky-tickets-san-francisco-chase-center-6-25-2026--concerts-rap-hip-hop/production/6547619
MY_EMAIL=your-email@gmail.com
EMAIL_FROM=your-email@gmail.com
EMAIL_PASSWORD=your_app_password_here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
CHECK_INTERVAL_HOURS=4
```

**Important:** Replace the values with your actual email and password!

## Step 5: Configure the Service Type

1. In Railway, go to your service settings
2. Under "Start Command", make sure it's set to use the Procfile:
   - It should automatically detect: `worker: python main.py`
3. If not, manually set it to: `python main.py`

## Step 6: Deploy!

Railway will automatically deploy your app. You can:
- Watch the logs in the "Deployments" tab
- See real-time output in the "Logs" tab
- The bot will start running automatically!

## Free Tier Limits

Railway's free tier includes:
- $5 credit per month (plenty for this bot)
- 500 hours of usage
- Your bot should run 24/7 within these limits

## Troubleshooting

- **Bot not running?** Check the logs in Railway dashboard
- **Email not sending?** Verify your email password is an app password, not your regular password
- **Price not found?** Check the logs to see what the scraper is finding

## Alternative: Render

If Railway doesn't work, try [Render.com](https://render.com):
1. Sign up with GitHub
2. Create a new "Background Worker"
3. Connect your GitHub repo
4. Add environment variables
5. Set start command: `python main.py`
6. Deploy!
