#!/usr/bin/env python3
"""
Test new AgentMail API key
Critical: Email outreach has been blocked for 5 days
"""

import requests
import json
from datetime import datetime

# New AgentMail API key
API_KEY = "am_us_6320cdca7bb3aef6fe7953500172394f4ef3f9c10d4a9224d576fbe394ff4138"

# AgentMail API endpoints
BASE_URL = "https://api.agentmail.to"
API_VERSION = "v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def test_api_connection():
    """Test basic API connectivity"""
    
    print("=" * 60)
    print("AGENTMAIL API TEST - CRITICAL SYSTEM CHECK")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {API_KEY[:20]}...{API_KEY[-20:]}")
    print()
    
    # Test 1: Check API status
    print("1. Testing API connectivity...")
    try:
        status_response = requests.get(
            f"{BASE_URL}/",
            headers=headers,
            timeout=30
        )
        
        print(f"   Status: {status_response.status_code}")
        
        if status_response.status_code == 200:
            print("   ✅ API is reachable!")
            try:
                status_data = status_response.json()
                print(f"   API Info: {json.dumps(status_data, indent=2)}")
            except:
                print(f"   Response: {status_response.text[:200]}")
        else:
            print(f"   Response: {status_response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Connection error: {str(e)}")
        return False
    
    return True

def test_inbox_access():
    """Test inbox access (critical for sending)"""
    
    print("\n2. Testing inbox access...")
    
    # Try to get inboxes
    try:
        inboxes_response = requests.get(
            f"{BASE_URL}/{API_VERSION}/inboxes",
            headers=headers,
            timeout=30
        )
        
        print(f"   Status: {inboxes_response.status_code}")
        
        if inboxes_response.status_code == 200:
            inboxes_data = inboxes_response.json()
            inboxes = inboxes_data.get('data', [])
            
            if inboxes:
                print(f"   ✅ Found {len(inboxes)} inbox(es)")
                for inbox in inboxes[:3]:  # Show first 3
                    print(f"      • {inbox.get('name')} ({inbox.get('email')})")
                
                # Get first inbox for further testing
                first_inbox = inboxes[0]
                inbox_id = first_inbox.get('id')
                inbox_email = first_inbox.get('email')
                
                print(f"\n   Using inbox: {inbox_email} (ID: {inbox_id})")
                return inbox_id, inbox_email
            else:
                print("   ❌ No inboxes found")
        else:
            print(f"   ❌ Inbox API error: {inboxes_response.status_code}")
            print(f"   Response: {inboxes_response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Inbox error: {str(e)}")
    
    return None, None

def test_email_sending(inbox_id, inbox_email):
    """Test sending a test email"""
    
    print("\n3. Testing email sending (CRITICAL TEST)...")
    
    test_email = {
        "to": ["test@example.com"],  # Using test email
        "from": inbox_email,
        "subject": f"AgentMail API Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "text": "This is a test email from the new AgentMail API key. If you receive this, the API is working!",
        "html": "<p>This is a test email from the new AgentMail API key.</p><p>If you receive this, the API is working!</p>",
        "cc": ["sam@impactquadrant.info"]  # Standard CC
    }
    
    try:
        send_response = requests.post(
            f"{BASE_URL}/{API_VERSION}/emails",
            headers=headers,
            json=test_email,
            timeout=30
        )
        
        print(f"   Send Status: {send_response.status_code}")
        
        if send_response.status_code == 200:
            send_data = send_response.json()
            print("   ✅ EMAIL SENDING WORKS!")
            print(f"   Response: {json.dumps(send_data, indent=2)}")
            return True
        elif send_response.status_code == 201:
            print("   ✅ EMAIL SENDING WORKS! (201 Created)")
            print(f"   Response: {send_response.text[:200]}")
            return True
        else:
            print(f"   ❌ Send failed: {send_response.status_code}")
            print(f"   Response: {send_response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Send error: {str(e)}")
    
    return False

def test_specific_endpoints():
    """Test specific endpoints that were failing"""
    
    print("\n4. Testing previously failing endpoints...")
    
    endpoints_to_test = [
        f"{BASE_URL}/{API_VERSION}/emails",
        f"{BASE_URL}/{API_VERSION}/inboxes/Zane@agentmail.to/messages",
        f"{BASE_URL}/v0/inboxes/Zane@agentmail.to/messages",
    ]
    
    for endpoint in endpoints_to_test:
        print(f"\n   Testing: {endpoint}")
        try:
            response = requests.get(endpoint, headers=headers, timeout=30)
            print(f"      Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"      ✅ Works!")
            elif response.status_code == 404:
                print(f"      ❌ 404 Not Found (same error as before)")
            elif response.status_code == 401:
                print(f"      ❌ 401 Unauthorized (API key issue)")
            else:
                print(f"      Response: {response.text[:100]}")
                
        except Exception as e:
            print(f"      Error: {str(e)}")

def check_campaign_status():
    """Check if we can resume campaigns"""
    
    print("\n" + "=" * 60)
    print("CAMPAIGN IMPACT ANALYSIS")
    print("=" * 60)
    
    # Campaigns blocked by AgentMail
    campaigns = [
        {"name": "Dorada Resort", "sent": "8/42", "blocked": "34 emails"},
        {"name": "Miami Hotels", "sent": "5/14", "blocked": "9 emails"},
        {"name": "Lead Outreach", "sent": "20+", "blocked": "Daily"},
        {"name": "Defense Sector", "sent": "0", "blocked": "15 leads ready"},
        {"name": "Expense Reduction", "sent": "6", "blocked": "Daily"}
    ]
    
    print("\n📧 Campaigns Currently Blocked:")
    for campaign in campaigns:
        print(f"   • {campaign['name']}: {campaign['sent']} sent, {campaign['blocked']} blocked")
    
    print(f"\n⏰ Blocked for: 5 DAYS (since 2026-02-20)")
    print(f"💰 Potential lost opportunities: Significant")
    
    return campaigns

def update_configuration_files():
    """Update configuration files with new API key"""
    
    print("\n" + "=" * 60)
    print("CONFIGURATION UPDATES NEEDED")
    print("=" * 60)
    
    files_to_update = [
        "/Users/cubiczan/.openclaw/workspace/scripts/send-remaining-leads.py",
        "/Users/cubiczan/.openclaw/workspace/scripts/dorada-wave2-outreach.py",
        "/Users/cubiczan/.openclaw/workspace/scripts/expense-reduction-agentmail.py",
        "/Users/cubiczan/.openclaw/workspace/skills/lead-generator/agentmail_client.py",
        "/Users/cubiczan/.openclaw/workspace/skills/expense-reduction-lead-gen/agentmail_client.py",
        "/Users/cubiczan/.openclaw/workspace/deals/dorada-outreach-campaign.md",
        "/Users/cubiczan/.openclaw/workspace/deals/miami-hotels-outreach-campaign.md",
    ]
    
    print("\n📁 Files that need API key update:")
    for file_path in files_to_update:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                if "agentmail" in content.lower() or "am_" in content:
                    print(f"   • {file_path}")
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"   • {file_path} (error reading: {str(e)})")
    
    print("\n🔧 Update command example:")
    print(f"""sed -i '' 's/am_[a-zA-Z0-9_]*/{API_KEY}/g' /path/to/file.py""")

def main():
    """Main execution"""
    
    print("\n🚀 TESTING NEW AGENTMAIL API KEY")
    print("This is CRITICAL - Email outreach blocked for 5 days")
    print()
    
    # Test basic connection
    if not test_api_connection():
        print("\n❌ API connection failed. Please check:")
        print("1. API key format (should start with 'am_us_')")
        print("2. Network connectivity")
        print("3. AgentMail service status")
        return
    
    # Test inbox access
    inbox_id, inbox_email = test_inbox_access()
    
    # Test email sending if we have an inbox
    sending_works = False
    if inbox_id and inbox_email:
        sending_works = test_email_sending(inbox_id, inbox_email)
    
    # Test specific endpoints
    test_specific_endpoints()
    
    # Check campaign impact
    campaigns = check_campaign_status()
    
    # Show configuration updates needed
    update_configuration_files()
    
    # Final status
    print("\n" + "=" * 60)
    print("FINAL STATUS")
    print("=" * 60)
    
    if sending_works:
        print("\n🎉 SUCCESS! AgentMail API is WORKING!")
        print("✅ Email outreach can be RESUMED immediately")
        print("✅ All blocked campaigns can proceed")
        print("✅ Update configuration files with new API key")
        
        print("\n🚀 IMMEDIATE ACTIONS:")
        print("1. Update API key in all configuration files")
        print("2. Run a test campaign (send 2-3 emails)")
        print("3. Monitor delivery and bounce rates")
        print("4. Resume all blocked campaigns")
        
    else:
        print("\n⚠️ PARTIAL SUCCESS or STILL BLOCKED")
        print("Some API endpoints work, but email sending may still have issues")
        print("Check the specific error messages above")
        
        print("\n🔧 NEXT STEPS:")
        print("1. Contact AgentMail support with error details")
        print("2. Continue using Gmail SMTP fallback")
        print("3. Monitor AgentMail status page")
        print("4. Consider alternative email providers")
    
    # Save test results
    try:
        results_file = '/Users/cubiczan/.openclaw/workspace/agentmail-test-results.json'
        with open(results_file, 'w') as f:
            json.dump({
                'test_timestamp': datetime.now().isoformat(),
                'api_key': API_KEY[:10] + '...' + API_KEY[-10:],
                'sending_works': sending_works,
                'inbox_found': bool(inbox_id),
                'campaigns_blocked': len(campaigns),
                'status': 'working' if sending_works else 'partial'
            }, f, indent=2)
        print(f"\n📁 Test results saved to: {results_file}")
    except Exception as e:
        print(f"\n⚠️ Could not save results: {str(e)}")

if __name__ == "__main__":
    main()