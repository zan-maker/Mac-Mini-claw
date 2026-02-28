#!/usr/bin/env python3
"""Test Tomba API with BOTH key and secret"""

import requests
import json
from datetime import datetime

def test_tomba_full_auth():
    """Test Tomba with both key and secret"""
    print("🔑 Testing Tomba API with Key + Secret...")
    
    # Tomba requires BOTH key and secret
    api_key = "ta_hsrcgwy0fwj29bbxm0ar3dns0nc6e5p2151pg"
    api_secret = "ts_576b466c-6d2a-4d3d-8730-6c6e9fe12958"
    
    headers = {
        "X-Tomba-Key": api_key,
        "X-Tomba-Secret": api_secret,
        "Content-Type": "application/json",
        "User-Agent": "OpenClaw/1.0"
    }
    
    # Test 1: Check account info
    print("\n1️⃣ Testing account info (/me endpoint)...")
    try:
        url = "https://api.tomba.io/v1/me"
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS! Authentication working")
            print(f"   Email: {data.get('data', {}).get('email', 'unknown')}")
            print(f"   Plan: {data.get('data', {}).get('plan', {}).get('name', 'unknown')}")
            print(f"   Credits remaining: {data.get('data', {}).get('credits', {}).get('remaining', 0)}")
            print(f"   Monthly limit: {data.get('data', {}).get('credits', {}).get('limit', 0)}")
            return True
        else:
            print(f"   ❌ FAILED: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    return False

def test_tomba_domain_search():
    """Test Tomba domain search"""
    print("\n2️⃣ Testing domain search...")
    
    api_key = "ta_hsrcgwy0fwj29bbxm0ar3dns0nc6e5p2151pg"
    api_secret = "ts_576b466c-6d2a-4d3d-8730-6c6e9fe12958"
    
    headers = {
        "X-Tomba-Key": api_key,
        "X-Tomba-Secret": api_secret,
        "Content-Type": "application/json",
        "User-Agent": "OpenClaw/1.0"
    }
    
    try:
        url = "https://api.tomba.io/v1/domain-search"
        params = {
            "domain": "openai.com",
            "limit": 5
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS! Domain search working")
            print(f"   Total emails: {data.get('data', {}).get('total', 0)}")
            print(f"   Emails found: {len(data.get('data', {}).get('emails', []))}")
            
            if data.get("data", {}).get("emails"):
                for i, email in enumerate(data["data"]["emails"][:3]):
                    print(f"   {i+1}. {email.get('email', 'No email')}")
                    print(f"      Name: {email.get('first_name', '')} {email.get('last_name', '')}")
                    print(f"      Position: {email.get('position', 'N/A')}")
                    print(f"      Department: {email.get('department', 'N/A')}")
            
            return True
        else:
            print(f"   ❌ FAILED: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_tomba_email_verification():
    """Test Tomba email verification"""
    print("\n3️⃣ Testing email verification...")
    
    api_key = "ta_hsrcgwy0fwj29bbxm0ar3dns0nc6e5p2151pg"
    api_secret = "ts_576b466c-6d2a-4d3d-8730-6c6e9fe12958"
    
    headers = {
        "X-Tomba-Key": api_key,
        "X-Tomba-Secret": api_secret,
        "Content-Type": "application/json",
        "User-Agent": "OpenClaw/1.0"
    }
    
    try:
        url = "https://api.tomba.io/v1/email-verifier/test@example.com"
        
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS! Email verification working")
            print(f"   Email: {data.get('data', {}).get('email', 'unknown')}")
            print(f"   Valid: {data.get('data', {}).get('valid', False)}")
            print(f"   MX records: {data.get('data', {}).get('mx_records', False)}")
            print(f"   Disposable: {data.get('data', {}).get('disposable', False)}")
            return True
        else:
            print(f"   ❌ FAILED: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def test_tomba_company_search():
    """Test Tomba company search"""
    print("\n4️⃣ Testing company search...")
    
    api_key = "ta_hsrcgwy0fwj29bbxm0ar3dns0nc6e5p2151pg"
    api_secret = "ts_576b466c-6d2a-4d3d-8730-6c6e9fe12958"
    
    headers = {
        "X-Tomba-Key": api_key,
        "X-Tomba-Secret": api_secret,
        "Content-Type": "application/json",
        "User-Agent": "OpenClaw/1.0"
    }
    
    try:
        url = "https://api.tomba.io/v1/companies/find"
        params = {
            "domain": "stripe.com"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ SUCCESS! Company search working")
            print(f"   Company: {data.get('data', {}).get('name', 'unknown')}")
            print(f"   Domain: {data.get('data', {}).get('domain', 'unknown')}")
            print(f"   Industry: {data.get('data', {}).get('industry', 'unknown')}")
            print(f"   Employees: {data.get('data', {}).get('employees', 'unknown')}")
            return True
        else:
            print(f"   ❌ FAILED: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False

def main():
    print("🧪 Tomba API Full Authentication Test")
    print("="*60)
    print(f"Key: ta_hsrcgwy0fwj29bbxm0ar3dns0nc6e5p2151pg")
    print(f"Secret: ts_576b466c-6d2a-4d3d-8730-6c6e9fe12958")
    print("="*60)
    
    results = {
        "Account Info": test_tomba_full_auth(),
        "Domain Search": test_tomba_domain_search(),
        "Email Verification": test_tomba_email_verification(),
        "Company Search": test_tomba_company_search()
    }
    
    print("\n" + "="*60)
    print("📊 FINAL RESULTS:")
    print("="*60)
    
    working = 0
    for test, success in results.items():
        status = "✅ WORKING" if success else "❌ FAILED"
        print(f"   {test}: {status}")
        if success:
            working += 1
    
    print("\n" + "="*60)
    print(f"   {working}/{len(results)} tests passed")
    
    if working == len(results):
        print("\n🎉 TOMBA API IS 100% WORKING!")
        print("   Ready for lead generation!")
    elif working >= 2:
        print(f"\n👍 {working} out of {len(results)} tests passed")
        print("   Tomba API is partially working")
    else:
        print("\n⚠️  Tomba API needs attention")
    
    print("\n🔧 Next steps:")
    if results.get("Domain Search"):
        print("   - Ready for B2B email finding")
    if results.get("Email Verification"):
        print("   - Ready for email validation")
    if results.get("Company Search"):
        print("   - Ready for company enrichment")

if __name__ == "__main__":
    main()