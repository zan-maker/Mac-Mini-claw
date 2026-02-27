#!/usr/bin/env python3
"""
Supabase Integration for Lead Generation
Project: https://utsqbuwkwsidvqvrodtf.supabase.co
"""

import urllib.request
import urllib.error
import json
from datetime import datetime

# Supabase Configuration
SUPABASE_URL = "https://utsqbuwkwsidvqvrodtf.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_H7oSoGx02K5ic0MlodC_ng_8DApe4FN"

def get_headers():
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def insert_lead(lead_data):
    """Insert a new lead into Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/leads"
    
    data = json.dumps(lead_data).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=get_headers(), method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            return {"success": True, "data": json.loads(response.read().decode())}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": e.read().decode()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_leads(limit=100):
    """Get leads from Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/leads?select=*&order=created_at.desc&limit={limit}"
    
    req = urllib.request.Request(url, headers=get_headers(), method='GET')
    
    try:
        with urllib.request.urlopen(req) as response:
            return {"success": True, "data": json.loads(response.read().decode())}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": e.read().decode()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def update_lead_status(lead_id, status):
    """Update lead status"""
    url = f"{SUPABASE_URL}/rest/v1/leads?id=eq.{lead_id}"
    
    data = json.dumps({"status": status}).encode('utf-8')
    headers = get_headers()
    req = urllib.request.Request(url, data=data, headers=headers, method='PATCH')
    
    try:
        with urllib.request.urlopen(req) as response:
            return {"success": True}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": e.read().decode()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def calculate_lead_score(employee_count, industry, challenge):
    """Calculate qualification score"""
    score = 0
    
    # Employee count scoring
    if employee_count >= 100:
        score += 30
    elif employee_count >= 50:
        score += 20
    elif employee_count >= 20:
        score += 10
    
    # Industry scoring
    high_value_industries = ["technology", "healthcare", "manufacturing", "financial services"]
    if industry and industry.lower() in high_value_industries:
        score += 25
    else:
        score += 15
    
    # Challenge scoring
    if challenge and len(challenge) > 20:
        score += 20
    else:
        score += 10
    
    return min(score, 100)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Supabase Lead Integration")
    print("="*60 + "\n")
    
    # Test connection
    print("Testing connection...")
    result = get_leads(limit=5)
    
    if result["success"]:
        print(f"✅ Connected! Found {len(result['data'])} leads.")
        for lead in result['data'][:3]:
            print(f"   - {lead.get('company_name', 'N/A')}: {lead.get('email', 'N/A')}")
    else:
        print(f"⚠️ {result['error']}")
        print("\n📋 You need to create the 'leads' table in Supabase first.")
        print("   See: /workspace/infrastructure/supabase-setup.md")
    
    print("\n" + "="*60 + "\n")
