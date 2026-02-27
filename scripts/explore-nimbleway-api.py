#!/usr/bin/env python3
"""
Explore Nimbleway API to find correct endpoints
"""

import requests
import json

API_KEY = "5b98a2e870df43059dfe1c39a23468db2e63e4e830dc4902a23501bf22706a31"
BASE_URL = "https://api.nimbleway.com"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def explore_api():
    """Explore API structure"""
    
    # Common API patterns for search/browser services
    endpoints = [
        # Search endpoints
        "/v1/search",
        "/api/v1/search", 
        "/search",
        "/v1/query",
        "/api/query",
        "/query",
        
        # Browser/automation endpoints
        "/v1/browser/search",
        "/api/v1/browser/search",
        "/browser/search",
        "/v1/scrape",
        "/api/v1/scrape",
        "/scrape",
        
        # Web search endpoints
        "/v1/web/search",
        "/api/v1/web/search",
        "/web/search",
        
        # Generic endpoints
        "/v1/execute",
        "/api/v1/execute",
        "/execute",
        
        # Health/status
        "/health",
        "/status",
        "/v1/health",
        "/api/v1/health"
    ]
    
    methods = ["GET", "POST"]
    
    for endpoint in endpoints:
        for method in methods:
            url = f"{BASE_URL}{endpoint}"
            print(f"\n🔍 Testing: {method} {url}")
            
            try:
                if method == "GET":
                    # Try with query parameters
                    params = {"q": "test", "limit": 1}
                    response = requests.get(url, headers=headers, params=params, timeout=10)
                else:  # POST
                    payload = {"query": "test", "num_results": 1}
                    response = requests.post(url, headers=headers, json=payload, timeout=10)
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code != 404:
                    print(f"   Headers: {dict(response.headers)}")
                    
                    # Try to parse response
                    try:
                        if response.text:
                            data = response.json()
                            print(f"   Response keys: {list(data.keys())}")
                            if 'results' in data:
                                print(f"   Results count: {len(data['results'])}")
                            elif 'data' in data:
                                print(f"   Data type: {type(data['data'])}")
                    except:
                        print(f"   Response: {response.text[:200]}...")
                
            except requests.exceptions.RequestException as e:
                print(f"   Error: {e}")
            except Exception as e:
                print(f"   Unexpected error: {e}")

def check_openapi_spec():
    """Check for OpenAPI/Swagger specification"""
    print("\n📋 Checking for API documentation...")
    
    spec_endpoints = [
        "/swagger.json",
        "/swagger/v1/swagger.json",
        "/openapi.json",
        "/openapi/v1/openapi.json",
        "/v3/api-docs",
        "/api-docs",
        "/docs",
        "/redoc"
    ]
    
    for endpoint in spec_endpoints:
        url = f"{BASE_URL}{endpoint}"
        print(f"\n🔍 Checking: {url}")
        try:
            response = requests.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                print(f"   Content-Type: {content_type}")
                if 'json' in content_type:
                    try:
                        data = response.json()
                        print(f"   OpenAPI version: {data.get('openapi', data.get('swagger', 'unknown'))}")
                        print(f"   Title: {data.get('info', {}).get('title', 'N/A')}")
                    except:
                        print(f"   Response: {response.text[:200]}...")
        except Exception as e:
            print(f"   Error: {e}")

def test_with_nimble_sdk_pattern():
    """Test with patterns from Nimble Browser SDK"""
    print("\n🔧 Testing Nimble Browser SDK patterns...")
    
    # Based on Nimble Browser documentation patterns
    test_cases = [
        {
            "url": f"{BASE_URL}/v1/browser/execute",
            "payload": {
                "command": "search",
                "params": {
                    "query": "mining investors Canada",
                    "engine": "google",
                    "num_results": 5
                }
            }
        },
        {
            "url": f"{BASE_URL}/v1/execute",
            "payload": {
                "action": "search",
                "query": "mining investors Canada",
                "options": {"limit": 5}
            }
        },
        {
            "url": f"{BASE_URL}/v1/search/web",
            "payload": {
                "q": "mining investors Canada",
                "n": 5
            }
        }
    ]
    
    for test in test_cases:
        print(f"\n🔍 Testing: POST {test['url']}")
        try:
            response = requests.post(test['url'], headers=headers, json=test['payload'], timeout=15)
            print(f"   Status: {response.status_code}")
            
            if response.status_code != 404:
                print(f"   Headers: {dict(response.headers)}")
                try:
                    if response.text:
                        data = response.json()
                        print(f"   Response: {json.dumps(data, indent=2)[:500]}...")
                except:
                    print(f"   Response: {response.text[:500]}...")
        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    print("🚀 Exploring Nimbleway API Structure")
    print(f"API Key: {API_KEY[:10]}...{API_KEY[-10:]}")
    print(f"Base URL: {BASE_URL}")
    
    # Check OpenAPI spec first
    check_openapi_spec()
    
    # Explore API endpoints
    explore_api()
    
    # Test Nimble Browser patterns
    test_with_nimble_sdk_pattern()
    
    print("\n📋 Next steps if API not found:")
    print("1. Check https://online.nimbleway.com/ for documentation")
    print("2. Look for 'API Keys' section in account settings")
    print("3. Contact Nimbleway support for API documentation")
    print("4. Check email for welcome/onboarding materials")
    print("5. Try different base URL (maybe https://api.nimble.com or similar)")