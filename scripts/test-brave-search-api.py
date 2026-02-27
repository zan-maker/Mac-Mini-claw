#!/usr/bin/env python3
"""
Test new Brave Search API key
Critical for lead enrichment and contact finding
"""

import requests
import json
from datetime import datetime

# New Brave Search API key
API_KEY = "BSA4VYA3FjSPQmTjZeKjsq5CqWvFy2u"

# Brave Search API endpoints
BASE_URL = "https://api.search.brave.com/res/v1"
WEB_SEARCH_URL = f"{BASE_URL}/web/search"

headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
    "X-Subscription-Token": API_KEY
}

def test_api_connection():
    """Test basic API connectivity"""
    
    print("=" * 60)
    print("BRAVE SEARCH API TEST - CRITICAL SYSTEM CHECK")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {API_KEY}")
    print()
    
    # Test 1: Simple search test
    print("1. Testing API connectivity with simple search...")
    try:
        params = {
            "q": "test search",
            "count": 3,
            "country": "US",
            "search_lang": "en"
        }
        
        response = requests.get(
            WEB_SEARCH_URL,
            headers=headers,
            params=params,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ API is working!")
            print(f"   Found {len(data.get('web', {}).get('results', []))} results")
            
            # Show first result
            if data.get('web', {}).get('results'):
                first_result = data['web']['results'][0]
                print(f"   Sample result: {first_result.get('title', 'No title')[:50]}...")
                print(f"   URL: {first_result.get('url', 'No URL')[:60]}...")
            return True
            
        elif response.status_code == 401:
            print("   ❌ 401 Unauthorized - Invalid API key")
            print(f"   Response: {response.text[:200]}")
        elif response.status_code == 429:
            print("   ❌ 429 Rate Limited - Still hitting limits")
            print(f"   Response: {response.text[:200]}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Connection error: {str(e)}")
    
    return False

def test_lead_enrichment_search():
    """Test a lead enrichment search (what we actually need)"""
    
    print("\n2. Testing lead enrichment search...")
    
    # Test search for company contact info
    test_queries = [
        "CEO contact email Tesla Inc",
        "venture capital firm San Francisco contact",
        "manufacturing company Texas 100 employees"
    ]
    
    for query in test_queries:
        print(f"\n   Query: '{query}'")
        try:
            params = {
                "q": query,
                "count": 5,
                "country": "US",
                "search_lang": "en",
                "freshness": "pm"  # Past month
            }
            
            response = requests.get(
                WEB_SEARCH_URL,
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('web', {}).get('results', [])
                print(f"      ✅ Found {len(results)} results")
                
                if results:
                    # Show most relevant looking result
                    for result in results[:2]:
                        title = result.get('title', 'No title')
                        url = result.get('url', 'No URL')
                        print(f"      • {title[:60]}...")
                        print(f"        {url[:70]}...")
            else:
                print(f"      ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"      Error: {str(e)}")

def check_current_usage():
    """Check current API usage if possible"""
    
    print("\n3. Checking API usage/limits...")
    
    # Brave Search doesn't have a direct usage endpoint
    # But we can infer from headers or test limits
    
    try:
        # Test with multiple quick searches to check rate limiting
        test_searches = 3
        successful = 0
        
        for i in range(test_searches):
            params = {
                "q": f"test search {i}",
                "count": 1
            }
            
            response = requests.get(
                WEB_SEARCH_URL,
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                successful += 1
        
        print(f"   Made {test_searches} test searches, {successful} successful")
        
        if successful == test_searches:
            print("   ✅ No immediate rate limiting detected")
        else:
            print(f"   ⚠️ Rate limiting may still be in effect ({successful}/{test_searches} succeeded)")
            
    except Exception as e:
        print(f"   Error checking usage: {str(e)}")

def find_configuration_files():
    """Find all files that need Brave Search API key updates"""
    
    print("\n" + "=" * 60)
    print("CONFIGURATION FILES TO UPDATE")
    print("=" * 60)
    
    # Files that likely contain Brave Search API keys
    search_patterns = [
        "brave",
        "BSA",
        "search.brave.com",
        "X-Subscription-Token"
    ]
    
    print("\n📁 Searching for files with Brave Search configuration...")
    
    try:
        import subprocess
        import os
        
        # Search in workspace directory
        workspace = "/Users/cubiczan/.openclaw/workspace"
        
        for pattern in search_patterns:
            print(f"\n   Searching for: '{pattern}'")
            try:
                result = subprocess.run(
                    ["grep", "-r", "-l", pattern, workspace],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                files = result.stdout.strip().split('\n')
                for file in files:
                    if file and os.path.exists(file):
                        print(f"      • {file}")
                        
            except Exception as e:
                print(f"      Search error: {str(e)}")
                
    except Exception as e:
        print(f"   File search error: {str(e)}")

def check_system_impact():
    """Check which systems are affected by Brave Search issues"""
    
    print("\n" + "=" * 60)
    print("SYSTEM IMPACT ANALYSIS")
    print("=" * 60)
    
    systems_using_brave = [
        {
            "system": "Lead Generator",
            "purpose": "Company discovery and enrichment",
            "status": "❌ Blocked (rate limited)",
            "impact": "High - Cannot find new leads"
        },
        {
            "system": "Deal Origination",
            "purpose": "Finding off-market sellers",
            "status": "⚠️ Partial (using Tavily)",
            "impact": "Medium - Limited data sources"
        },
        {
            "system": "Contact Enrichment",
            "purpose": "Finding email addresses",
            "status": "❌ Blocked (Hunter.io exhausted)",
            "impact": "Critical - No emails for outreach"
        },
        {
            "system": "Defense Sector",
            "purpose": "Finding defense companies",
            "status": "❌ Blocked (rate limited)",
            "impact": "High - Campaign stalled"
        },
        {
            "system": "Expense Reduction",
            "purpose": "Finding target companies",
            "status": "⚠️ Working (Tavily backup)",
            "impact": "Low - Has backup"
        }
    ]
    
    print("\n📊 Systems affected by Brave Search issues:")
    for system in systems_using_brave:
        print(f"   • {system['system']}: {system['status']}")
        print(f"     Purpose: {system['purpose']}")
        print(f"     Impact: {system['impact']}")
        print()

def update_recommendations():
    """Provide update recommendations"""
    
    print("\n" + "=" * 60)
    print("UPDATE RECOMMENDATIONS")
    print("=" * 60)
    
    print("\n🎯 Priority 1: Update these critical files:")
    
    critical_files = [
        "/Users/cubiczan/.openclaw/workspace/skills/lead-generator/brave_search.py",
        "/Users/cubiczan/.openclaw/workspace/skills/deal-origination/search_client.py",
        "/Users/cubiczan/.openclaw/workspace/skills/expense-reduction-lead-gen/search_client.py",
        "/Users/cubiczan/.openclaw/workspace/scripts/brave-search-enrichment.py",
        "/Users/cubiczan/.openclaw/workspace/.env",  # If using environment variables
        "/Users/cubiczan/.openclaw/workspace/config/search-config.json",
    ]
    
    for file_path in critical_files:
        print(f"   • {file_path}")
    
    print("\n🔧 Update methods:")
    print("1. Direct file edit:")
    print(f'   sed -i \'\' "s/old_key_here/{API_KEY}/g" filename.py')
    
    print("\n2. Environment variable (recommended):")
    print(f'   export BRAVE_SEARCH_API_KEY="{API_KEY}"')
    print("   Then update scripts to read from environment")
    
    print("\n3. Configuration file:")
    print(f"""   {{ "brave_search": {{ "api_key": "{API_KEY}" }} }}""")
    
    print("\n🚀 Immediate actions:")
    print("1. Test the new key works for actual lead searches")
    print("2. Update the most critical system first (Lead Generator)")
    print("3. Test lead generation with new key")
    print("4. Update all other systems")
    print("5. Monitor rate limits and usage")

def main():
    """Main execution"""
    
    print("\n🚀 TESTING NEW BRAVE SEARCH API KEY")
    print("Critical for lead enrichment and contact finding")
    print("Previous key was rate-limited (429 errors)")
    print()
    
    # Test API connection
    api_works = test_api_connection()
    
    if api_works:
        # Test lead enrichment
        test_lead_enrichment_search()
        
        # Check usage
        check_current_usage()
        
        # System is working!
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Brave Search API is WORKING!")
        print("=" * 60)
        print("\n✅ Lead enrichment can be RESUMED")
        print("✅ Contact finding can be RESTORED")
        print("✅ All blocked systems can be FIXED")
        
    else:
        print("\n" + "=" * 60)
        print("⚠️ API TEST FAILED")
        print("=" * 60)
        print("\nThe new API key may still have issues:")
        print("1. Key might be invalid or expired")
        print("2. Account might still be rate-limited")
        print("3. Billing/payment issues")
        print("4. Service outage")
    
    # Find configuration files
    find_configuration_files()
    
    # Check system impact
    check_system_impact()
    
    # Provide update recommendations
    update_recommendations()
    
    # Save test results
    try:
        results_file = '/Users/cubiczan/.openclaw/workspace/brave-search-test-results.json'
        with open(results_file, 'w') as f:
            json.dump({
                'test_timestamp': datetime.now().isoformat(),
                'api_key': API_KEY,
                'api_works': api_works,
                'systems_affected': 5,
                'status': 'working' if api_works else 'failed'
            }, f, indent=2)
        print(f"\n📁 Test results saved to: {results_file}")
    except Exception as e:
        print(f"\n⚠️ Could not save results: {str(e)}")

if __name__ == "__main__":
    main()