#!/usr/bin/env python3
"""
Complete Lead Generation Integration
Connects: Formbricks → n8n → Supabase → AgentMail → Discord
"""

import json
import urllib.request
import urllib.error
from datetime import datetime

# API Keys
SUPABASE_URL = "https://utsqbuwkwsidvqvrodtf.supabase.co"
SUPABASE_KEY = "sb_publishable_H7oSoGx02K5ic0MlodC_ng_8DApe4FN"

FORMBRICKS_ENV = "cmlolpn609uahre01dm4yoqxe"
FORMBRICKS_URL = "https://app.formbricks.com"

VAPI_KEY = "24455236-8179-4d7b-802a-876aa44d4677"
VAPI_PHONE_ID = "07867d73-85a2-475c-b7c1-02f2879a4916"
VAPI_AGENT_ID = "3f5b4b81-9975-4f29-958b-cadd7694deca"

AGENTMAIL_KEY = "am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68"
AGENTMAIL_INBOX = "Zander@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"

# Discord webhook (replace with actual)
DISCORD_WEBHOOK = "YOUR_DISCORD_WEBHOOK"

def process_lead(lead_data):
    """Process incoming lead from any source"""
    
    # Calculate savings
    employees = lead_data.get("employee_count", 0)
    savings = employees * 681
    
    # Calculate score
    score = 0
    if employees >= 100: score += 30
    elif employees >= 50: score += 20
    elif employees >= 20: score += 10
    
    if lead_data.get("challenge"):
        score += 20
    
    # Determine status
    status = "qualified" if score >= 50 else "nurture"
    
    return {
        **lead_data,
        "estimated_savings": savings,
        "qualification_score": score,
        "status": status
    }

def save_to_supabase(lead):
    """Save lead to Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/leads"
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    data = json.dumps(lead).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            return {"success": True, "data": json.loads(response.read())}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": e.read().decode()}

def send_email(lead):
    """Send email via AgentMail"""
    url = f"https://api.agentmail.to/v0/inboxes/{AGENTMAIL_INBOX}/messages"
    
    headers = {
        "Authorization": f"Bearer {AGENTMAIL_KEY}",
        "Content-Type": "application/json"
    }
    
    email_data = {
        "to": [lead.get("email")],
        "cc": [CC_EMAIL],
        "subject": f"Your Savings Estimate: ${lead['estimated_savings']:,}",
        "text": f"""
Hi {lead.get('contact_name', 'there')},

Thanks for your interest in expense reduction!

Based on companies similar to {lead.get('company_name', 'yours')} with {lead.get('employee_count', 0)} employees, we estimate potential annual savings of ${lead['estimated_savings']:,}.

Would you like to schedule a brief call to see the detailed breakdown?

Best,
Zander
"""
    }
    
    data = json.dumps(email_data).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            return {"success": True}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": e.read().decode()}

def notify_discord(lead):
    """Send Discord notification"""
    if DISCORD_WEBHOOK == "YOUR_DISCORD_WEBHOOK":
        return {"success": False, "error": "Discord webhook not configured"}
    
    message = {
        "content": f"🎯 **New Lead Captured!**\n\n" +
                   f"**Company:** {lead.get('company_name', 'N/A')}\n" +
                   f"**Employees:** {lead.get('employee_count', 'N/A')}\n" +
                   f"**Est. Savings:** ${lead.get('estimated_savings', 0):,}\n" +
                   f"**Score:** {lead.get('qualification_score', 0)}\n" +
                   f"**Status:** {lead.get('status', 'new')}"
    }
    
    data = json.dumps(message).encode('utf-8')
    req = urllib.request.Request(DISCORD_WEBHOOK, data=data, 
                                  headers={"Content-Type": "application/json"}, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            return {"success": True}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": e.read().decode()}

def handle_new_lead(lead_data):
    """Main handler for new leads"""
    print(f"\n🎯 Processing lead: {lead_data.get('company_name', 'Unknown')}")
    
    # 1. Process and score
    lead = process_lead(lead_data)
    print(f"   Score: {lead['qualification_score']} | Status: {lead['status']}")
    
    # 2. Save to Supabase
    result = save_to_supabase(lead)
    if result["success"]:
        print("   ✅ Saved to Supabase")
    else:
        print(f"   ⚠️ Supabase: {result.get('error', 'Unknown error')}")
    
    # 3. Send email (qualified leads only)
    if lead['status'] == 'qualified' and lead.get('email'):
        result = send_email(lead)
        if result["success"]:
            print("   ✅ Email sent")
        else:
            print(f"   ⚠️ Email: {result.get('error', 'Unknown error')}")
    
    # 4. Discord notification
    result = notify_discord(lead)
    if result["success"]:
        print("   ✅ Discord notified")
    
    return lead

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Lead Generation Integration Test")
    print("="*60)
    
    # Test with sample lead
    test_lead = {
        "company_name": "Acme Corporation",
        "contact_name": "John Smith",
        "email": "john@acme.com",
        "employee_count": 150,
        "industry": "Technology",
        "challenge": "High SaaS costs and vendor contracts",
        "source": "test"
    }
    
    result = handle_new_lead(test_lead)
    print(f"\n📋 Result: {json.dumps(result, indent=2)}")
    
    print("\n" + "="*60 + "\n")
