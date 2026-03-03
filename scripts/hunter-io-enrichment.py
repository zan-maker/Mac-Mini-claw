#!/usr/bin/env python3
"""
Hunter.io Email Enrichment Script
Finds and verifies email addresses for lead enrichment
"""

import requests
import json
import time
from datetime import datetime

# Configuration
HUNTER_API_KEY = "e76ec3ea73a64b4716e6b3c40d3d4d9cea9dc1e2"
CONFIG_FILE = "/Users/cubiczan/.openclaw/workspace/hunter-io-config.json"

def load_config():
    """Load Hunter.io configuration"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "hunter_io": {
                "api_key": HUNTER_API_KEY,
                "search_credits": 1000,
                "verification_credits": 1000
            },
            "usage": {
                "searches_used": 0,
                "verifications_used": 0,
                "last_used": None
            }
        }

def save_config(config):
    """Save Hunter.io configuration"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_account_info():
    """Get Hunter.io account information"""
    url = f"https://api.hunter.io/v2/account?api_key={HUNTER_API_KEY}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()

def find_emails(domain, company_name=None, limit=10):
    """
    Find email addresses for a domain
    
    Args:
        domain: Company domain (e.g., indsupply.com)
        company_name: Optional company name for better results
        limit: Maximum number of emails to return
    
    Returns:
        List of email objects with details
    """
    config = load_config()
    
    # Build query
    params = {
        "domain": domain,
        "api_key": HUNTER_API_KEY,
        "limit": limit
    }
    
    if company_name:
        params["company"] = company_name
    
    # Make request
    url = "https://api.hunter.io/v2/domain-search"
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    
    # Update usage
    config["usage"]["searches_used"] += 1
    config["usage"]["last_used"] = datetime.now().isoformat()
    save_config(config)
    
    return data

def verify_email(email):
    """
    Verify an email address
    
    Args:
        email: Email address to verify
    
    Returns:
        Verification result object
    """
    config = load_config()
    
    # Make request
    url = f"https://api.hunter.io/v2/email-verifier"
    params = {
        "email": email,
        "api_key": HUNTER_API_KEY
    }
    
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    
    # Update usage
    config["usage"]["verifications_used"] += 1
    config["usage"]["last_used"] = datetime.now().isoformat()
    save_config(config)
    
    return data

def enrich_lead(company_name, domain, position_filter=None):
    """
    Enrich a lead with email addresses
    
    Args:
        company_name: Company name
        domain: Company domain
        position_filter: Optional list of positions to filter for (e.g., ["CEO", "CFO"])
    
    Returns:
        Enriched lead object
    """
    print(f"Enriching lead: {company_name} ({domain})")
    
    # Get account info first
    account_info = get_account_info()
    searches_left = account_info["data"]["requests"]["searches"]["available"]
    verifications_left = account_info["data"]["requests"]["verifications"]["available"]
    
    print(f"Credits available: {searches_left} searches, {verifications_left} verifications")
    
    # Find emails
    print(f"Searching for emails at {domain}...")
    search_result = find_emails(domain, company_name)
    
    emails_found = search_result.get("data", {}).get("emails", [])
    total_emails = search_result.get("meta", {}).get("results", 0)
    
    print(f"Found {total_emails} emails, analyzing top {len(emails_found)}...")
    
    # Filter by position if specified
    if position_filter:
        emails_found = [
            email for email in emails_found 
            if email.get("position") and any(pos.lower() in email["position"].lower() for pos in position_filter)
        ]
        print(f"Filtered to {len(emails_found)} emails matching positions: {position_filter}")
    
    # Verify top emails
    verified_emails = []
    for i, email_obj in enumerate(emails_found[:5]):  # Verify top 5
        email = email_obj["value"]
        print(f"  Verifying {email}...")
        
        verification = verify_email(email)
        verification_data = verification.get("data", {})
        
        verified_email = {
            "email": email,
            "first_name": email_obj.get("first_name"),
            "last_name": email_obj.get("last_name"),
            "position": email_obj.get("position"),
            "verification_status": verification_data.get("status"),
            "verification_score": verification_data.get("score"),
            "verification_result": verification_data.get("result"),
            "sources": email_obj.get("sources", [])
        }
        
        verified_emails.append(verified_email)
        
        # Brief pause to avoid rate limiting
        if i < len(emails_found[:5]) - 1:
            time.sleep(0.5)
    
    # Prepare result
    result = {
        "company_name": company_name,
        "domain": domain,
        "organization": search_result.get("data", {}).get("organization"),
        "total_emails_found": total_emails,
        "verified_emails": verified_emails,
        "search_metadata": search_result.get("meta", {}),
        "enrichment_date": datetime.now().isoformat(),
        "credits_used": {
            "searches": 1,
            "verifications": len(verified_emails)
        }
    }
    
    return result

def main():
    """Main function for testing"""
    print("=" * 60)
    print("HUNTER.IO EMAIL ENRICHMENT TEST")
    print("=" * 60)
    
    # Test with a few companies
    test_cases = [
        {"company": "Industrial Supply Company", "domain": "indsupply.com", "positions": ["CEO", "CFO", "President"]},
        {"company": "Midwest Foods", "domain": "midwestfoods.com", "positions": ["Owner", "President", "CEO"]},
        {"company": "Precision Products Machining Group", "domain": "precprodmachgrp.com", "positions": ["CEO", "CFO"]}
    ]
    
    all_results = []
    
    for test in test_cases:
        print(f"\n{'='*40}")
        print(f"Testing: {test['company']}")
        print(f"{'='*40}")
        
        try:
            result = enrich_lead(
                company_name=test["company"],
                domain=test["domain"],
                position_filter=test["positions"]
            )
            
            all_results.append(result)
            
            # Print summary
            print(f"\n✓ Enrichment complete for {test['company']}")
            print(f"  Organization: {result.get('organization', 'N/A')}")
            print(f"  Total emails found: {result['total_emails_found']}")
            print(f"  Verified emails: {len(result['verified_emails'])}")
            
            for email in result["verified_emails"]:
                status_icon = "✅" if email["verification_status"] == "valid" else "⚠️"
                print(f"    {status_icon} {email['email']} - {email['position']} (Score: {email['verification_score']})")
            
        except Exception as e:
            print(f"✗ Error enriching {test['company']}: {str(e)}")
        
        # Pause between companies
        time.sleep(1)
    
    # Save results
    output_file = f"/Users/cubiczan/.openclaw/workspace/hunter-enrichment-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✅ All tests complete!")
    print(f"Results saved to: {output_file}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
