#!/bin/bash
# Daily Craigslist Referral Fee Scraper
# Runs as cron job to find business-for-sale and service business opportunities

cd /Users/cubiczan/.openclaw/workspace

# Activate virtual environment
source craigslist-env/bin/activate

# Run the scraper
echo "Starting Craigslist scraper at $(date)"
python scripts/craigslist_daily_scraper.py

# Deactivate virtual environment
deactivate

echo "Craigslist scraper completed at $(date)"