#!/usr/bin/env python3
"""
Test Hunter.io API with new key
"""

import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace')
from hunter_io_config import hunter_client

def test_hunter_api():
    """Test the Hunter.io API"""
    print("Testing Hunter.io API with new key...")
    
    # Test account info
    print("\n1. Getting account info...")
    account_info = hunter_client.get_account_info()
    
    if account_info.get('data'):
        data = account_info['data']
        print(f"   ✅ API Key is valid!")
        print(f"   Account: {data.get('first_name', 'N/A')} {data.get('last_name', 'N/A')}")
        print(f"   Email: {data.get('email', 'N/A')}")
        print(f"   Plan: {data.get('plan_name', 'N/A')}")
        print(f"   Credits: {data.get('calls', {}).get('available', 'N/A')}")
        print(f"   Used: {data.get('calls', {}).get('used', 'N/A')}")
        print(f"   Reset date: {data.get('calls', {}).get('reset_date', 'N/A')}")
    else:
        print(f"   ❌ Error: {account_info.get('errors', ['Unknown error'])}")
        return False
    
    # Test domain search for a sample domain
    print("\n2. Testing domain search...")
    test_domain = "helsing.ai"  # One of the defense companies
    domain_result = hunter_client.domain_search(test_domain, limit=5)
    
    if domain_result.get('data'):
        data = domain_result['data']
        print(f"   ✅ Domain search successful for {test_domain}")
        print(f"   Organization: {data.get('organization', 'N/A')}")
        print(f"   Emails found: {len(data.get('emails', []))}")
        
        if data.get('emails'):
            print(f"   Sample emails:")
            for i, email in enumerate(data['emails'][:3], 1):
                print(f"     {i}. {email.get('value', 'N/A')} - {email.get('type', 'N/A')} - {email.get('confidence', 'N/A')}%")
    else:
        print(f"   ⚠️ No emails found or error: {domain_result.get('errors', ['No emails'])}")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("HUNTER.IO API TEST")
    print("=" * 60)
    
    success = test_hunter_api()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Hunter.io API is working with new key!")
    else:
        print("❌ Hunter.io API test failed")
    print("=" * 60)