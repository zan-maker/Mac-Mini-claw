#!/usr/bin/env python3
"""
Bdev.ai → AgentMail Integration
Automated email sending for AI-generated messages
"""

import os
import sys
import pandas as pd
import json
from datetime import datetime

# AgentMail API configuration
AGENTMAIL_API_KEY = "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"
AGENTMAIL_BASE_URL = "https://api.agentmail.com"  # Update with actual URL

def send_to_agentmail(email_data):
    """Send email via AgentMail API"""
    # This is a template - update with actual AgentMail API calls
    print(f"📧 Preparing email for: {email_data['name']}")
    print(f"   To: {email_data['email']}")
    print(f"   Subject: {email_data.get('subject', 'Potential Synergy')}")
    print(f"   Status: ✅ Ready for AgentMail delivery")
    return True

def process_bdev_ai_output(csv_path, limit=50):
    """Process Bdev.ai output for AgentMail"""
    print(f"Processing {csv_path}...")
    
    try:
        df = pd.read_csv(csv_path)
        print(f"Found {len(df)} AI-generated messages")
        
        sent_count = 0
        for idx, row in df.head(limit).iterrows():
            try:
                email = str(row.get('email', '')).strip()
                if not email or '@' not in email:
                    continue
                
                # Prepare email data
                email_data = {
                    'name': str(row.get('contact_name', 'Investor')),
                    'email': email,
                    'company': str(row.get('company', '')),
                    'subject': f"Re: {row.get('company', 'Opportunity')} - AI-Powered Insights",
                    'message': str(row.get('personalized_message', '')),
                    'sectors': str(row.get('sectors', '')),
                    'timestamp': datetime.now().isoformat()
                }
                
                # Send via AgentMail
                if send_to_agentmail(email_data):
                    sent_count += 1
                    print(f"  {idx+1}. {email_data['name']} - ✅ Ready")
                
            except Exception as e:
                print(f"  {idx+1}. Error: {e}")
                continue
        
        return sent_count
        
    except Exception as e:
        print(f"Error processing CSV: {e}")
        return 0

def main():
    """Main function"""
    print("Bdev.ai → AgentMail Integration")
    print("="*60)
    
    # Find latest Bdev.ai output
    import glob
    bdev_files = glob.glob("bdev_ai_openclaw_*.csv")
    
    if not bdev_files:
        print("❌ No Bdev.ai output files found")
        return
    
    latest_file = max(bdev_files, key=os.path.getctime)
    print(f"Source: {latest_file}")
    
    # Process and send
    sent_count = process_bdev_ai_output(latest_file, limit=50)
    
    # Log results
    log_entry = {
        'date': datetime.now().isoformat(),
        'source_file': latest_file,
        'messages_sent': sent_count,
        'integration': 'Bdev.ai → AgentMail'
    }
    
    log_file = "bdev_ai_agentmail_log.json"
    logs = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = json.load(f)
    
    logs.append(log_entry)
    
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
    
    print(f"\n🎉 Results:")
    print(f"   Messages processed: {sent_count}")
    print(f"   Log saved to: {log_file}")
    print("="*60)

if __name__ == "__main__":
    main()
