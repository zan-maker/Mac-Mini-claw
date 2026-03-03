#!/usr/bin/env python3
"""
Global Private Markets Outreach Script
Matches 26 opportunities to investor database and sends personalized emails.
"""

import os
import sys
import json
import csv
import random
from datetime import datetime
import time

# Add workspace to path
sys.path.append('/Users/cubiczan/.openclaw/workspace')

try:
    from scripts.gmail_smtp_standard import GmailSender, STANDARD_SIGNATURE
except ImportError:
    print("❌ ERROR: Could not import GmailSender. Make sure gmail_smtp_standard.py exists.")
    sys.exit(1)

# Configuration
INVESTOR_DB = '/Users/cubiczan/.openclaw/workspace/data/master-investor-database.csv'
OPPORTUNITIES_FILE = '/Users/cubiczan/.openclaw/workspace/deals/global-private-markets-opportunities.md'
LOG_FILE = '/Users/cubiczan/.openclaw/workspace/deals/global-markets-outreach-log.md'
DAILY_TARGET = 10  # Emails per day
GMAIL_ACCOUNT_INDEX = 0  # Use first Gmail account
DELAY_SECONDS = 4  # Delay between emails

# Opportunity categories
OPPORTUNITY_CATEGORIES = {
    'hospitality': [1, 2, 3, 4, 5, 18, 19],
    'healthcare': [6, 25, 26],
    'energy': [7, 9, 22],
    'technology': [8, 10, 16, 20, 21],
    'alternatives': [11, 12, 13, 14, 15, 17, 23, 24]
}

# Email templates
EMAIL_TEMPLATES = {
    'hospitality': {
        'subject': 'Exclusive: Curated Hospitality Opportunities (Greece, Caribbean, Costa Rica)',
        'body': '''Hi {investor_name},

I'm reaching out with exclusive access to 7 curated hospitality opportunities:

1. **Greek Boutique Hotels** (€1.5M-€4.985M) - 3 distressed/development assets
2. **Dominican Beachfront Peninsula** ($90M) - 133 acres, >1% of national coastline
3. **US Hotel Fund** ($150M) - Value-add hospitality strategy
4. **Costa Rica Oceanfront** ($20M) - 120-hectare luxury community

These opportunities offer:
- Distressed entry points (Greek hotels)
- Government incentives (Dominican Republic - 100% tax exemption)
- Premium coastal locations
- Professional management available

Are any of these sectors/geographies of interest?

{signature}'''
    },
    'multi_sector': {
        'subject': 'Global Private Markets Portfolio: 26 Opportunities Across Sectors',
        'body': '''Hi {investor_name},

I have exclusive access to 26 private market opportunities across:

• **Hospitality/Tourism** (7 deals) - Greece, Caribbean, Costa Rica, US
• **Healthcare** (3 deals) - Saudi robotic rehab, US healthtech
• **Energy/Infrastructure** (3 deals) - UAE oil, Bulgarian renewables, Georgian refinery
• **Technology** (5 deals) - AI, Web3, fintech, media
• **Alternatives** (8 deals) - Litigation funding, vertical farming, commodities, honey

Ticket sizes: €1.5M - $150M
Geographies: Global (Greece, UAE, Saudi, US, Australia, NZ, etc.)

Would you like me to share a shortlist based on your mandate?

{signature}'''
    }
}

def load_investors():
    """Load investor database."""
    investors = []
    try:
        with open(INVESTOR_DB, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                investors.append(row)
        print(f"✅ Loaded {len(investors)} investors from database")
        return investors
    except FileNotFoundError:
        print(f"❌ Investor database not found: {INVESTOR_DB}")
        return []
    except Exception as e:
        print(f"❌ Error loading investors: {e}")
        return []

def categorize_investor(investor):
    """Categorize investor based on their profile."""
    # Simple categorization based on investment thesis/sector focus
    profile = (investor.get('Investment Thesis', '') + ' ' + 
               investor.get('Sector Focus', '')).lower()
    
    categories = []
    if any(word in profile for word in ['hotel', 'hospitality', 'real estate', 'tourism', 'resort']):
        categories.append('hospitality')
    if any(word in profile for word in ['health', 'medical', 'biotech', 'life science']):
        categories.append('healthcare')
    if any(word in profile for word in ['energy', 'oil', 'renewable', 'infrastructure']):
        categories.append('energy')
    if any(word in profile for word in ['tech', 'software', 'ai', 'fintech', 'digital']):
        categories.append('technology')
    if any(word in profile for word in ['credit', 'debt', 'fixed income', 'alternative', 'litigation']):
        categories.append('alternatives')
    
    # Default to multi-sector if no clear category
    if not categories:
        categories.append('multi_sector')
    
    return categories[0]  # Return primary category

def select_investors_for_outreach(investors, count=DAILY_TARGET):
    """Select investors for today's outreach."""
    # Filter investors with email
    investors_with_email = [
        inv for inv in investors 
        if inv.get('Email') and '@' in inv.get('Email', '')
    ]
    
    print(f"📧 Found {len(investors_with_email)} investors with email addresses")
    
    # Categorize each investor
    categorized = []
    for inv in investors_with_email:
        category = categorize_investor(inv)
        categorized.append({
            'investor': inv,
            'category': category,
            'name': inv.get('Contact Name', inv.get('Firm Name', 'Investor')),
            'email': inv['Email'],
            'firm': inv.get('Firm Name', ''),
            'focus': inv.get('Investment Thesis', '')
        })
    
    # Shuffle and select target count
    random.shuffle(categorized)
    selected = categorized[:count]
    
    print(f"🎯 Selected {len(selected)} investors for outreach")
    return selected

def send_outreach_emails(selected_investors):
    """Send personalized outreach emails."""
    gmail_sender = GmailSender(account_index=GMAIL_ACCOUNT_INDEX, delay_seconds=DELAY_SECONDS)
    
    sent_count = 0
    failed_count = 0
    results = []
    
    for i, investor in enumerate(selected_investors, 1):
        try:
            # Get template based on category
            if investor['category'] == 'multi_sector':
                template = EMAIL_TEMPLATES['multi_sector']
            else:
                template = EMAIL_TEMPLATES.get(investor['category'], EMAIL_TEMPLATES['multi_sector'])
            
            # Personalize email
            subject = template['subject']
            body = template['body'].format(
                investor_name=investor['name'],
                signature=STANDARD_SIGNATURE
            )
            
            # Add personalization based on investor focus
            if investor['focus']:
                body = body.replace(
                    "Would you like me to share a shortlist based on your mandate?",
                    f"Based on your focus on {investor['focus']}, I believe Projects {', '.join(map(str, OPPORTUNITY_CATEGORIES.get(investor['category'], [])))} may be of particular interest.\n\nWould you like me to share detailed memos for these?"
                )
            
            print(f"📧 Sending to {investor['email']} ({i}/{len(selected_investors)})...")
            
            # Send email
            result = gmail_sender.send_email(
                to_emails=investor['email'],
                subject=subject,
                body_text=body,
                cc_emails=['sam@impactquadrant.info']
            )
            
            if result.get('success'):
                sent_count += 1
                print(f"✅ Email sent to {investor['email']}")
                results.append({
                    'investor': investor['name'],
                    'email': investor['email'],
                    'firm': investor['firm'],
                    'category': investor['category'],
                    'status': 'sent',
                    'timestamp': datetime.now().isoformat()
                })
            else:
                failed_count += 1
                print(f"❌ Failed to send to {investor['email']}: {result.get('message', 'Unknown error')}")
                results.append({
                    'investor': investor['name'],
                    'email': investor['email'],
                    'firm': investor['firm'],
                    'category': investor['category'],
                    'status': 'failed',
                    'error': result.get('message', 'Unknown error'),
                    'timestamp': datetime.now().isoformat()
                })
            
            # Add delay between emails
            if i < len(selected_investors):
                time.sleep(DELAY_SECONDS)
                
        except Exception as e:
            print(f"❌ Error sending to {investor.get('email', 'unknown')}: {e}")
            failed_count += 1
            results.append({
                'investor': investor.get('name', 'Unknown'),
                'email': investor.get('email', ''),
                'firm': investor.get('firm', ''),
                'category': investor.get('category', ''),
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
    
    return sent_count, failed_count, results

def update_log(results):
    """Update outreach log file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Create log entry
    log_entry = f"""## Outreach Batch - {timestamp}

### Summary
- **Total Attempted:** {len(results)}
- **Sent Successfully:** {sum(1 for r in results if r['status'] == 'sent')}
- **Failed:** {sum(1 for r in results if r['status'] in ['failed', 'error'])}

### Details
"""
    
    for result in results:
        status_emoji = '✅' if result['status'] == 'sent' else '❌'
        log_entry += f"- {status_emoji} **{result['investor']}** ({result['firm']}) - {result['email']}\n"
        if result['status'] != 'sent':
            log_entry += f"  - Error: {result.get('error', 'Unknown')}\n"
    
    log_entry += "\n---\n\n"
    
    # Append to log file
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        print(f"📁 Log updated: {LOG_FILE}")
    except Exception as e:
        print(f"❌ Error updating log: {e}")
    
    # Also save detailed results as JSON
    json_file = LOG_FILE.replace('.md', f'_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': timestamp,
                'results': results,
                'summary': {
                    'total': len(results),
                    'sent': sum(1 for r in results if r['status'] == 'sent'),
                    'failed': sum(1 for r in results if r['status'] in ['failed', 'error'])
                }
            }, f, indent=2)
        print(f"📁 Detailed results saved: {json_file}")
    except Exception as e:
        print(f"❌ Error saving JSON results: {e}")

def main():
    """Main execution function."""
    print("🚀 GLOBAL PRIVATE MARKETS OUTREACH")
    print("=" * 50)
    
    # Load investors
    investors = load_investors()
    if not investors:
        print("❌ No investors loaded. Exiting.")
        return
    
    # Select investors for outreach
    selected = select_investors_for_outreach(investors)
    if not selected:
        print("❌ No investors selected for outreach. Exiting.")
        return
    
    # Send emails
    print("\n📤 SENDING OUTREACH EMAILS...")
    print("=" * 50)
    
    sent, failed, results = send_outreach_emails(selected)
    
    # Print summary
    print("\n" + "=" * 50)
    print("✅ OUTREACH COMPLETE!")
    print("=" * 50)
    print(f"📊 RESULTS:")
    print(f"   Total Attempted: {len(selected)}")
    print(f"   Sent Successfully: {sent}")
    print(f"   Failed: {failed}")
    print(f"   Success Rate: {(sent / len(selected) * 100):.1f}%")
    print()
    
    # Update log
    update_log(results)
    
    print("🎯 NEXT STEPS:")
    print("1. Monitor email replies in sam@cubiczan.com inbox")
    print("2. Check spam folder for responses")
    print("3. Schedule calls with interested investors")
    print("4. Share deal memos based on expressed interest")
    print("5. Track allocations and follow up")
    print()
    print("💰 Potential allocations from this batch: 2-3 interested investors")

if __name__ == "__main__":
    main()