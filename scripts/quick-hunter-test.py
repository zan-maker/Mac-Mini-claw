#!/usr/bin/env python3
"""
Quick test: Find emails for top 3 defense companies using Hunter.io
"""

import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace')
from hunter_io_config import hunter_client
import time

# Test with top 3 companies
test_companies = [
    {"name": "Helsing", "domain": "helsing.ai"},
    {"name": "Quantum Systems", "domain": "quantum-systems.com"},
    {"name": "Comand AI", "domain": "comand.ai"},
]

print("Testing Hunter.io email search for top 3 defense companies...")
print("=" * 60)

for company in test_companies:
    print(f"\n🔍 Searching: {company['name']} ({company['domain']})")
    
    try:
        result = hunter_client.domain_search(company['domain'], limit=5)
        
        if result.get('data') and result['data'].get('emails'):
            emails = result['data']['emails']
            print(f"   ✅ Found {len(emails)} emails")
            
            # Show top 3 emails
            for i, email in enumerate(emails[:3], 1):
                print(f"     {i}. {email.get('value', 'N/A')}")
                print(f"        Type: {email.get('type', 'N/A')}")
                print(f"        Confidence: {email.get('confidence', 'N/A')}%")
                print(f"        Position: {email.get('position', 'N/A')}")
                print(f"        Sources: {len(email.get('sources', []))}")
        else:
            print(f"   ❌ No emails found")
            if result.get('errors'):
                print(f"      Error: {result['errors']}")
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Delay between requests
    time.sleep(2)

print("\n" + "=" * 60)
print("✅ Test complete!")