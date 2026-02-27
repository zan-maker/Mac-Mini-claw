#!/bin/bash
# Daily Craigslist Lead Processor
# Processes scraped leads and sends outreach emails

cd /Users/cubiczan/.openclaw/workspace

# Activate virtual environment
source craigslist-env/bin/activate

# Run the lead processor
echo "Starting lead processor at $(date)"
python scripts/process_craigslist_leads.py

# Deactivate virtual environment
deactivate

echo "Lead processor completed at $(date)"