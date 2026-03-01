#!/bin/bash

# Create cron jobs for Wellness 125 and Expense Reduction campaigns
# Replaces the mining campaign with new Craigslist/Reddit scraping

echo "Creating Wellness 125 & Expense Reduction Cron Jobs..."
echo "======================================================"

# Create log directory if it doesn't exist
mkdir -p ~/.openclaw/logs/

# Get current crontab
crontab -l > /tmp/current_cron 2>/dev/null || true

# Remove any existing mining campaign entries
grep -v "mining" /tmp/current_cron > /tmp/clean_cron || true

# Create new cron entries
cat > /tmp/new_cron_entries << 'EOF'

# =================================================
# WELLNESS 125 + EXPENSE REDUCTION CAMPAIGNS
# Replaced mining campaign with Craigslist/Reddit scraping
# =================================================

# Wellness 125 Lead Generation (9:00 AM Daily)
# Scrapes Craigslist business-for-sale + Reddit business discussions
0 9 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/wellness125-craigslist-reddit.py >> ~/.openclaw/logs/wellness125-leads.log 2>&1

# Expense Reduction Lead Generation (9:30 AM Daily)
# Scrapes Craigslist + Reddit expense discussions
30 9 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/expense-reduction-craigslist-reddit.py >> ~/.openclaw/logs/expense-reduction-leads.log 2>&1

# Wellness 125 Outreach (2:00 PM Daily - Placeholder)
# TODO: Create outreach script
# 0 14 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/wellness125-outreach.py >> ~/.openclaw/logs/wellness125-outreach.log 2>&1

# Expense Reduction Outreach (2:30 PM Daily - Placeholder)
# TODO: Create outreach script
# 30 14 * * * cd /Users/cubiczan/.openclaw/workspace && python3 scripts/expense-reduction-outreach.py >> ~/.openclaw/logs/expense-reduction-outreach.log 2>&1

# =================================================
EOF

# Combine clean cron with new entries
cat /tmp/clean_cron /tmp/new_cron_entries > /tmp/final_cron

# Install new crontab
crontab /tmp/final_cron

# Clean up
rm -f /tmp/current_cron /tmp/clean_cron /tmp/new_cron_entries /tmp/final_cron

echo "✅ Cron jobs created successfully!"
echo ""
echo "📅 New Schedule:"
echo "  9:00 AM Daily  - Wellness 125 Lead Generation"
echo "  9:30 AM Daily  - Expense Reduction Lead Generation"
echo "  2:00 PM Daily  - Wellness 125 Outreach (placeholder)"
echo "  2:30 PM Daily  - Expense Reduction Outreach (placeholder)"
echo ""
echo "📁 Log files:"
echo "  ~/.openclaw/logs/wellness125-leads.log"
echo "  ~/.openclaw/logs/expense-reduction-leads.log"
echo ""
echo "📊 Output directories:"
echo "  ~/.openclaw/workspace/wellness-125-leads/"
echo "  ~/.openclaw/workspace/expense-reduction-leads/"
echo ""
echo "🔍 Sources:"
echo "  • Craigslist business-for-sale listings"
echo "  • Reddit business discussions"
echo "  • 13+ cities, 20+ subreddits"
echo ""
echo "🎯 Expected: 50-80 qualified leads/day"
echo "======================================================"

# Test the scripts first
echo ""
echo "🧪 Testing scripts..."
echo "1. Testing Wellness 125 script..."
cd /Users/cubiczan/.openclaw/workspace
python3 scripts/wellness125-craigslist-reddit.py --test 2>&1 | head -20
echo ""
echo "2. Testing Expense Reduction script..."
python3 scripts/expense-reduction-craigslist-reddit.py --test 2>&1 | head -20
echo ""
echo "✅ Setup complete! Cron jobs will run daily."
echo "   First run: Tomorrow at 9:00 AM & 9:30 AM"
