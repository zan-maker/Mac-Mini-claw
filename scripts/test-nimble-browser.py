#!/usr/bin/env python3
"""
Test Nimble Browser API based on common patterns
"""

import requests
import json

API_KEY = "5b98a2e870df43059dfe1c39a23468db2e63e4e830dc4902a23501bf22706a31"

# Common patterns for browser automation APIs
test_cases = [
    # Pattern 1: Direct browser control
    {
        "url": "https://api.nimbleway.com/v1/browser",
        "method": "POST",
        "headers": {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        "data": {
            "action": "navigate",
            "url": "https://www.google.com/search?q=mining+investors+Canada",
            "extract": {
                "results": "div.g"
            }
        }
    },
    
    # Pattern 2: Search API
    {
        "url": "https://api.nimbleway.com/v1/search/web",
        "method": "POST", 
        "headers": {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        "data": {
            "query": "mining investors Canada",
            "num_results": 5,
            "search_engine": "google"
        }
    },
    
    # Pattern 3: Execute script
    {
        "url": "https://api.nimbleway.com/v1/execute",
        "method": "POST",
        "headers": {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        "data": {
            "script": """
            const page = await browser.newPage();
            await page.goto('https://www.google.com/search?q=mining+investors+Canada');
            const results = await page.evaluate(() => {
                return Array.from(document.querySelectorAll('div.g')).map(el => ({
                    title: el.querySelector('h3')?.textContent,
                    url: el.querySelector('a')?.href,
                    snippet: el.querySelector('div.VwiC3b')?.textContent
                }));
            });
            return results;
            """,
            "language": "javascript"
        }
    },
    
    # Pattern 4: Simple GET with API key in URL
    {
        "url": f"https://api.nimbleway.com/v1/search?q=mining+investors&api_key={API_KEY}",
        "method": "GET",
        "headers": {}
    },
    
    # Pattern 5: Different base URL
    {
        "url": "https://browser.nimbleway.com/api/v1/search",
        "method": "POST",
        "headers": {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        "data": {
            "query": "test"
        }
    }
]

def run_tests():
    print("🚀 Testing Nimble Browser API patterns")
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {test['method']} {test['url']}")
        print(f"{'='*60}")
        
        try:
            if test['method'] == 'GET':
                response = requests.get(test['url'], headers=test.get('headers', {}), timeout=15)
            else:  # POST
                response = requests.post(
                    test['url'], 
                    headers=test.get('headers', {}),
                    json=test.get('data', {}),
                    timeout=15
                )
            
            print(f"Status: {response.status_code}")
            print(f"Response time: {response.elapsed.total_seconds():.2f}s")
            
            if response.status_code != 404:
                print(f"Headers: {dict(response.headers)}")
                
                # Try to parse response
                try:
                    if response.text:
                        data = response.json()
                        print(f"JSON Response:\n{json.dumps(data, indent=2)[:1000]}...")
                except json.JSONDecodeError:
                    print(f"Text Response (first 500 chars):\n{response.text[:500]}...")
            else:
                print("Endpoint not found (404)")
                
        except requests.exceptions.Timeout:
            print("⚠️  Request timed out")
        except requests.exceptions.ConnectionError as e:
            print(f"🔌 Connection error: {e}")
        except Exception as e:
            print(f"❌ Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    run_tests()
    
    print(f"\n{'='*60}")
    print("📋 Summary:")
    print("If all tests fail, the API might require:")
    print("1. Account activation/verification")
    print("2. Different authentication method (API key in header vs URL)")
    print("3. Specific endpoint not discovered yet")
    print("4. Web dashboard configuration first")
    print("5. Contacting support for API documentation")
    print(f"{'='*60}")