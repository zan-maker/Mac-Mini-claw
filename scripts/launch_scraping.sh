#!/bin/bash
# Launch Script for ClawReceptionist Multi-Platform Scraping

echo "🚀 LAUNCHING CLAWRECEPTIONIST SCRAPING SYSTEM"
echo "============================================================"
echo "📅 Date: $(date)"
echo "🎯 Target: Salon & Spa Businesses"
echo "📍 Location: New York"
echo "📊 Platforms: Craigslist → Yellow Pages → Twitter → Yelp"
echo "============================================================"

# Activate virtual environment
echo "🔧 Activating Python environment..."
cd /Users/cubiczan/.openclaw/workspace
source .venv/bin/activate

# Run the scraper
echo "🔄 Starting multi-platform scraping..."
python3 -c "
import sys
sys.path.append('.')
from scripts.multi_platform_scraper import MultiPlatformScraper

print('\\n🎯 SCRAPING SALONS & SPAS IN NEW YORK...')
scraper = MultiPlatformScraper()
result = scraper.scrape_all_platforms('salons_spas', 'new york', 25)

print('✅ SCRAPING COMPLETE!')
print('='*60)
print(f'📊 TOTAL LEADS: {result[\"total_leads\"]}')
print('📈 PLATFORM BREAKDOWN:')
for platform, count in result['platform_counts'].items():
    print(f'   • {platform.upper()}: {count} leads')
print(f'📁 RESULTS: {result[\"filepath\"]}')
print('='*60)

# Show sample leads
print('\\n🎯 TOP 5 LEADS FOR OUTREACH:')
for i, lead in enumerate(result['leads_sample'][:5], 1):
    print(f'{i}. {lead[\"business_name\"]}')
    print(f'   📞 {lead.get(\"phone\", \"N/A\")}')
    print(f'   🌐 {lead.get(\"website\", \"N/A\")}')
    print(f'   📍 {lead.get(\"location\", \"N/A\")}')
    print(f'   📋 Source: {lead.get(\"sources\", [\"N/A\"])[0]}')
    print()
"

echo "============================================================"
echo "📋 NEXT STEPS:"
echo "1. Review leads in: /Users/cubiczan/.openclaw/workspace/scraped_leads/"
echo "2. Run outreach: python3 scripts/smb_lead_targeting.py"
echo "3. Set up cron job: crontab -e"
echo "4. Check logs: tail -f logs/scraping.log"
echo ""
echo "⏰ To automate daily scraping, add to crontab:"
echo "0 8 * * * cd /Users/cubiczan/.openclaw/workspace && ./scripts/launch_scraping.sh >> logs/daily_scraping.log 2>&1"
echo ""
echo "🎉 CLAWRECEPTIONIST SCRAPING SYSTEM IS LIVE! 🚀"