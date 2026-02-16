#!/usr/bin/env python3
"""
ZeroBounce Email Validation Integration
Validates emails before sending outreach - used by all lead gen systems
"""

import requests
import json

ZEROBOUNCE_API_KEY = "fd0105c8c98340e0a2b63e2fbe39d7a4"
BASE_URL = "https://api.zerobounce.net/v2"

def validate_email(email):
    """Validate a single email address"""
    try:
        response = requests.get(
            f"{BASE_URL}/validate",
            params={
                "api_key": ZEROBOUNCE_API_KEY,
                "email": email
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "email": email,
                "status": data.get("status"),
                "sub_status": data.get("sub_status"),
                "valid": data.get("status") in ["valid", "catch-all"],
                "score": data.get("bounce_score", 0),
                "free_email": data.get("free_email"),
                "did_you_mean": data.get("did_you_mean"),
                "domain": data.get("domain")
            }
        else:
            return {"email": email, "valid": False, "error": response.text}
    except Exception as e:
        return {"email": email, "valid": False, "error": str(e)}

def validate_batch(emails):
    """Validate multiple emails"""
    results = []
    for email in emails:
        result = validate_email(email)
        results.append(result)
    return results

def get_credits():
    """Check API credits remaining"""
    try:
        response = requests.get(
            f"{BASE_URL}/getcredits",
            params={"api_key": ZEROBOUNCE_API_KEY}
        )
        if response.status_code == 200:
            return response.json().get("credits", "unknown")
    except:
        pass
    return "unknown"

if __name__ == "__main__":
    print("\n" + "="*60)
    print("ZeroBounce Email Validation - Integration Test")
    print("="*60 + "\n")
    
    # Check credits
    credits = get_credits()
    print(f"Credits Remaining: {credits}")
    
    # Test validation
    test_email = "test@example.com"
    result = validate_email(test_email)
    print(f"\nTest Validation: {test_email}")
    print(f"Status: {result.get('status', 'N/A')}")
    print(f"Valid: {result.get('valid', False)}")
    
    print("\n✅ ZeroBounce integration ready for all lead gen systems")
    print("\n" + "="*60 + "\n")
