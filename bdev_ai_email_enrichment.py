#!/usr/bin/env python3
"""
Enrich Bdev.ai generated messages with email addresses from contacts database
"""

import pandas as pd
import json
from datetime import datetime
import sys
import os

def enrich_with_emails(ai_file=None, contacts_file=None, output_file=None):
    """Enrich AI-generated messages with email addresses"""
    
    # Default file paths
    if ai_file is None:
        # Find latest AI-generated file
        ai_files = sorted([f for f in os.listdir('.') if f.startswith('bdev_ai_openclaw_') and f.endswith('.csv')])
        if not ai_files:
            print("❌ No AI-generated files found")
            return None
        ai_file = ai_files[-1]
    
    if contacts_file is None:
        contacts_file = "data/family-office-contacts.csv"
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"bdev_ai_enriched_{timestamp}.csv"
    
    print(f"📄 Loading AI messages: {ai_file}")
    print(f"📄 Loading contacts: {contacts_file}")
    
    # Load AI messages
    ai_df = pd.read_csv(ai_file)
    print(f"   Found {len(ai_df)} AI messages")
    
    # Load contacts
    contacts_df = pd.read_csv(contacts_file)
    print(f"   Found {len(contacts_df)} contacts")
    
    # Clean company names for matching
    def clean_name(name):
        if pd.isna(name):
            return ""
        return str(name).strip().lower()
    
    ai_df['company_clean'] = ai_df['company'].apply(clean_name)
    contacts_df['company_clean'] = contacts_df['Company Name'].apply(clean_name)
    
    # Create a mapping of company to email
    company_emails = {}
    for _, row in contacts_df.iterrows():
        company = row['company_clean']
        email = row['Primary Email']
        if pd.notna(email) and email.strip():
            if company not in company_emails:
                company_emails[company] = []
            company_emails[company].append(email.strip())
    
    print(f"   Found emails for {len(company_emails)} unique companies")
    
    # Add emails to AI messages
    enriched_count = 0
    emails_added = []
    
    # Ensure email column exists and is string type
    if 'email' not in ai_df.columns:
        ai_df['email'] = ''
    ai_df['email'] = ai_df['email'].astype(str)
    
    for i, row in ai_df.iterrows():
        company = row['company_clean']
        if company in company_emails:
            # Use first email for this company
            email = company_emails[company][0]
            ai_df.at[i, 'email'] = email
            emails_added.append(email)
            enriched_count += 1
    
    print(f"   ✅ Added emails to {enriched_count} messages")
    
    # Save enriched file
    ai_df.to_csv(output_file, index=False)
    print(f"💾 Saved enriched file: {output_file}")
    
    # Also create a summary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'ai_file': ai_file,
        'contacts_file': contacts_file,
        'output_file': output_file,
        'total_messages': len(ai_df),
        'enriched_count': enriched_count,
        'enrichment_rate': enriched_count / len(ai_df) if len(ai_df) > 0 else 0,
        'unique_emails_added': len(set(emails_added))
    }
    
    summary_file = output_file.replace('.csv', '_summary.json')
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"📊 Summary saved: {summary_file}")
    
    return output_file

if __name__ == "__main__":
    # Run enrichment
    enriched_file = enrich_with_emails()
    
    if enriched_file:
        print(f"\n✅ Email enrichment complete!")
        print(f"   Next step: Run AgentMail sender on {enriched_file}")
        print(f"   Command: python3 bdev_ai_agentmail_sender_working.py --input {enriched_file}")