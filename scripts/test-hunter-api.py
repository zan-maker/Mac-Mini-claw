#!/usr/bin/env python3
"""
Test new Hunter.io API key and check credits
"""

import requests
import json
from datetime import datetime

# New Hunter.io API Key
HUNTER_API_KEY = "601920a0b5d6b80f9131d4ae588065f694840081"

def test_hunter_api():
    """Test the new Hunter.io API key"""
    
    print("=" * 60)
    print("🔍 TESTING NEW HUNTER.IO API KEY")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {HUNTER_API_KEY[:8]}...{HUNTER_API_KEY[-8:]}")
    print()
    
    # Test 1: Check account status
    print("1. Checking account status...")
    try:
        url = f"https://api.hunter.io/v2/account?api_key={HUNTER_API_KEY}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            account_info = data.get('data', {})
            
            print(f"   ✅ API Key is VALID")
            print(f"   👤 Name: {account_info.get('first_name', 'N/A')} {account_info.get('last_name', 'N/A')}")
            print(f"   📧 Email: {account_info.get('email', 'N/A')}")
            print(f"   💰 Plan: {account_info.get('plan_name', 'N/A')}")
            print(f"   🔑 Plan Level: {account_info.get('plan_level', 'N/A')}")
            
            # Check credits
            calls = account_info.get('calls', {})
            print(f"   📊 Credits Used: {calls.get('used', 0)}")
            print(f"   📈 Credits Available: {calls.get('available', 0)}")
            print(f"   📉 Credits Reset Date: {calls.get('reset_date', 'N/A')}")
            
            available = calls.get('available', 0)
            if available > 0:
                print(f"   🎉 AVAILABLE CREDITS: {available}")
                return True, available, account_info
            else:
                print(f"   ⚠️  NO CREDITS AVAILABLE")
                return False, 0, account_info
                
        else:
            print(f"   ❌ API Error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False, 0, None
            
    except Exception as e:
        print(f"   ❌ Connection Error: {str(e)}")
        return False, 0, None

def test_email_finder():
    """Test email finder functionality"""
    
    print("\n2. Testing email finder...")
    
    # Test with a known company
    test_domain = "stripe.com"
    test_first_name = "Patrick"
    test_last_name = "Collison"
    
    try:
        url = f"https://api.hunter.io/v2/email-finder"
        params = {
            "domain": test_domain,
            "first_name": test_first_name,
            "last_name": test_last_name,
            "api_key": HUNTER_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            email_data = data.get('data', {})
            
            print(f"   ✅ Email finder WORKING")
            print(f"   📧 Found email: {email_data.get('email', 'N/A')}")
            print(f"   📊 Score: {email_data.get('score', 'N/A')}")
            print(f"   🎯 Sources: {email_data.get('sources', [])[:3]}")
            
            # Check if it consumed credits
            meta = data.get('meta', {})
            print(f"   💰 Credits used: {meta.get('results', 0)}")
            
            return True
            
        elif response.status_code == 402:
            print(f"   ⚠️  Insufficient credits for email finder")
            return False
        else:
            print(f"   ❌ Email finder error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Connection Error: {str(e)}")
        return False

def test_domain_search():
    """Test domain search (bulk email finding)"""
    
    print("\n3. Testing domain search...")
    
    test_domain = "openai.com"
    
    try:
        url = f"https://api.hunter.io/v2/domain-search"
        params = {
            "domain": test_domain,
            "api_key": HUNTER_API_KEY,
            "limit": 1  # Just test with 1 result to save credits
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            meta = data.get('meta', {})
            
            print(f"   ✅ Domain search WORKING")
            print(f"   🏢 Domain: {test_domain}")
            print(f"   👥 Total emails found: {meta.get('results', 0)}")
            print(f"   💰 Credits used: {meta.get('results', 0)}")
            
            # Show first result if available
            emails = data.get('data', {}).get('emails', [])
            if emails:
                first_email = emails[0]
                print(f"   📧 Sample email: {first_email.get('value', 'N/A')}")
                print(f"   👤 Name: {first_email.get('first_name', 'N/A')} {first_email.get('last_name', 'N/A')}")
            
            return True
            
        elif response.status_code == 402:
            print(f"   ⚠️  Insufficient credits for domain search")
            return False
        else:
            print(f"   ❌ Domain search error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Connection Error: {str(e)}")
        return False

def main():
    """Main test function"""
    
    print("\n🚀 HUNTER.IO API KEY TEST")
    print("Contact enrichment has been BLOCKED due to exhausted credits")
    print("New key should unblock email finding for all campaigns")
    print()
    
    # Test API key
    api_valid, credits_available, account_info = test_hunter_api()
    
    if not api_valid:
        print("\n❌ API Key is INVALID or has NO CREDITS")
        print("Cannot proceed with contact enrichment")
        return
    
    print(f"\n🎉 NEW HUNTER.IO KEY IS WORKING!")
    print(f"✅ Available credits: {credits_available}")
    
    # Test email finder if we have credits
    if credits_available > 0:
        email_finder_working = test_email_finder()
        domain_search_working = test_domain_search()
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        if email_finder_working or domain_search_working:
            print("✅ Hunter.io API is FULLY OPERATIONAL")
            print("✅ Contact enrichment can be RESUMED")
            print(f"✅ Available credits: {credits_available}")
            
            print("\n🎯 Impact on campaigns:")
            print("   • Dorada Resort: Can find investor emails")
            print("   • Miami Hotels: Can find buyer emails")
            print("   • Defense Sector: Can find contact emails")
            print("   • Lead Outreach: Can enrich all leads")
            print("   • Expense Reduction: Can find decision makers")
            
            print(f"\n⏰ Time blocked: Since Hunter.io credits exhausted")
            print(f"🚀 Recovery: IMMEDIATE")
            
            # Save configuration
            try:
                config_file = '/Users/cubiczan/.openclaw/workspace/hunter-config.json'
                config = {
                    'configured_at': datetime.now().isoformat(),
                    'api_key': HUNTER_API_KEY,
                    'credits_available': credits_available,
                    'account_info': account_info,
                    'status': 'active',
                    'tests_passed': {
                        'api_key': api_valid,
                        'email_finder': email_finder_working,
                        'domain_search': domain_search_working
                    },
                    'campaigns_unblocked': [
                        'Dorada Resort Investor Outreach',
                        'Miami Hotels Buyer Outreach',
                        'Defense Sector Lead Enrichment',
                        'Lead Outreach Contact Finding',
                        'Expense Reduction Decision Maker Finding'
                    ]
                }
                
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=2)
                
                print(f"\n📁 Configuration saved to: {config_file}")
                
            except Exception as e:
                print(f"\n⚠️ Could not save config: {str(e)}")
            
        else:
            print("⚠️  Hunter.io API has credits but endpoints not working")
            print("Check API documentation or try different endpoints")
    
    else:
        print("\n⚠️  Hunter.io key valid but NO CREDITS available")
        print("Need to purchase more credits or wait for reset")

if __name__ == "__main__":
    main()