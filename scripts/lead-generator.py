#!/usr/bin/env python3
"""
Daily Lead Generator for Wellness 125 Cafeteria Plan
Identifies 15-20 qualified B2B leads with 20+ employees

IMPORTANT: Abstract API rate limit is 1 request per second
"""

import requests
import json
from datetime import datetime
import os
import time

# API Keys
HUNTER_API_KEY = "f701d171cf7decf7e730a6b1c6e9b74f29f39b6e"
ABSTRACT_API_KEY = "38aeec02e6f6469983e0856dfd147b10"

# Rate limiting for Abstract API (1 request per second)
class AbstractAPIRateLimiter:
    def __init__(self):
        self.last_request_time = 0
        self.min_interval = 1.0  # 1 second
    
    def wait_if_needed(self):
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        if elapsed < self.min_interval:
            sleep_time = self.min_interval - elapsed
            print(f"⏳ Rate limiting: Waiting {sleep_time:.2f}s before next Abstract API request")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

# Global rate limiter instance
abstract_api_rate_limiter = AbstractAPIRateLimiter()

# Lead generation targets
TARGET_INDUSTRIES = [
    "healthcare hospice",
    "senior living facility",
    "medical transportation",
    "hospitality hotel",
    "restaurant franchise",
    "manufacturing",
    "transportation trucking"
]

MIN_EMPLOYEES = 20
MAX_EMPLOYEES = 500

def search_companies(industry, location="United States"):
    """Search for companies in target industry"""
    # This would integrate with actual business directories
    # For now, returns placeholder structure
    leads = []
    # TODO: Integrate with Google Places API, LinkedIn, or industry directories
    return leads

def enrich_company(domain):
    """Enrich company data using Abstract API with rate limiting"""
    try:
        # Apply rate limiting (1 request per second)
        abstract_api_rate_limiter.wait_if_needed()
        
        url = f"https://companyenrichment.abstractapi.com/v1/"
        params = {
            "api_key": ABSTRACT_API_KEY,
            "domain": domain
        }
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Abstract API error for {domain}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Enrichment error for {domain}: {e}")
    return None

def find_decision_maker_email(domain, role="CEO"):
    """Find decision-maker email using Hunter.io"""
    try:
        url = "https://api.hunter.io/v2/domain-search"
        params = {
            "api_key": HUNTER_API_KEY,
            "domain": domain,
            "seniority": "executive",
            "department": "executive"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            emails = data.get("data", {}).get("emails", [])
            # Filter for decision makers
            for email in emails:
                if any(title in email.get("position", "").lower() for title in ["ceo", "owner", "hr", "cfo", "benefits"]):
                    return {
                        "email": email.get("value"),
                        "name": email.get("first_name", "") + " " + email.get("last_name", ""),
                        "title": email.get("position"),
                        "confidence": email.get("confidence")
                    }
    except Exception as e:
        print(f"Hunter error for {domain}: {e}")
    return None

def score_lead(company_data):
    """Score lead based on criteria (0-100)"""
    score = 0

    # Company size (0-25 points)
    employees = company_data.get("employees_count", 0)
    if 20 <= employees <= 50:
        score += 15
    elif 51 <= employees <= 100:
        score += 20
    elif 101 <= employees <= 500:
        score += 25

    # Industry fit (0-25 points)
    industry = company_data.get("industry", "").lower()
    if "healthcare" in industry or "medical" in industry:
        score += 25
    elif "hospitality" in industry or "hotel" in industry or "restaurant" in industry:
        score += 20
    elif "manufacturing" in industry:
        score += 20
    elif "transportation" in industry or "trucking" in industry:
        score += 20
    else:
        score += 10

    # Decision maker found (0-25 points)
    if company_data.get("decision_maker"):
        score += 25

    # Contact quality (0-25 points)
    if company_data.get("email"):
        score += 20
    if company_data.get("phone"):
        score += 5

    return score

def calculate_potential_savings(employee_count):
    """Calculate potential annual savings"""
    fica_savings = employee_count * 681  # $681 per employee

    # Estimate workers comp savings (assume 30% of $500 average premium)
    workers_comp_savings = employee_count * 500 * 0.30

    total_savings = fica_savings + workers_comp_savings

    return {
        "fica": fica_savings,
        "workers_comp": int(workers_comp_savings),
        "total": int(total_savings)
    }

def save_daily_leads(leads, date_str):
    """Save leads to daily file"""
    workspace = "/Users/cubiczan/.openclaw/workspace/leads"
    os.makedirs(workspace, exist_ok=True)

    filename = f"{workspace}/daily-leads-{date_str}.md"

    with open(filename, 'w') as f:
        f.write(f"# Daily Leads - {date_str}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Leads:** {len(leads)}\n\n")
        f.write("---\n\n")

        # Sort by score
        leads_sorted = sorted(leads, key=lambda x: x.get('score', 0), reverse=True)

        for i, lead in enumerate(leads_sorted, 1):
            score = lead.get('score', 0)
            priority = "🔴 HIGH" if score >= 70 else "🟡 MEDIUM" if score >= 50 else "🟢 LOW"

            f.write(f"## Lead #{i} - {lead.get('company_name', 'Unknown')}\n\n")
            f.write(f"**Priority:** {priority} (Score: {score}/100)\n\n")
            f.write(f"**Company:** {lead.get('company_name', 'N/A')}\n")
            f.write(f"**Industry:** {lead.get('industry', 'N/A')}\n")
            f.write(f"**Employees:** {lead.get('employees_count', 'N/A')}\n")
            f.write(f"**Location:** {lead.get('location', 'N/A')}\n")
            f.write(f"**Website:** {lead.get('domain', 'N/A')}\n\n")

            savings = lead.get('potential_savings', {})
            f.write(f"**Potential Annual Savings:**\n")
            f.write(f"- FICA: ${savings.get('fica', 0):,}\n")
            f.write(f"- Workers Comp: ${savings.get('workers_comp', 0):,}\n")
            f.write(f"- **Total: ${savings.get('total', 0):,}**\n\n")

            contact = lead.get('decision_maker', {})
            if contact:
                f.write(f"**Decision Maker:**\n")
                f.write(f"- Name: {contact.get('name', 'N/A')}\n")
                f.write(f"- Title: {contact.get('title', 'N/A')}\n")
                f.write(f"- Email: {contact.get('email', 'N/A')}\n")
                f.write(f"- Confidence: {contact.get('confidence', 'N/A')}%\n\n")

            f.write(f"---\n\n")

    return filename

def generate_sample_leads():
    """Generate sample leads for testing"""
    sample_companies = [
        {
            "company_name": "Sunrise Senior Living - Phoenix",
            "domain": "sunriseseniorliving.com",
            "industry": "Healthcare - Senior Living",
            "employees_count": 85,
            "location": "Phoenix, AZ"
        },
        {
            "company_name": "Metro Medical Transport",
            "domain": "metromedicaltransport.com",
            "industry": "Healthcare - Medical Transportation",
            "employees_count": 45,
            "location": "Denver, CO"
        },
        {
            "company_name": "Hospice Care Partners",
            "domain": "hospicecarepartners.com",
            "industry": "Healthcare - Hospice",
            "employees_count": 120,
            "location": "Atlanta, GA"
        },
        {
            "company_name": "Mountain View Manufacturing",
            "domain": "mvmanuf.com",
            "industry": "Manufacturing",
            "employees_count": 75,
            "location": "Salt Lake City, UT"
        },
        {
            "company_name": "Premier Hotel Group",
            "domain": "premierhotelgroup.com",
            "industry": "Hospitality - Hotels",
            "employees_count": 150,
            "location": "Orlando, FL"
        }
    ]
    return sample_companies

def main():
    print("\n" + "="*60)
    print("Daily Lead Generator - Wellness 125 Cafeteria Plan")
    print("="*60 + "\n")

    date_str = datetime.now().strftime('%Y-%m-%d')

    # For now, use sample leads (in production, would fetch from APIs)
    companies = generate_sample_leads()

    leads = []
    for company in companies:
        print(f"Processing: {company['company_name']}...")

        # Enrich company data
        # enriched = enrich_company(company['domain'])

        # Find decision maker
        # decision_maker = find_decision_maker_email(company['domain'])

        # For demo, use placeholder data
        lead = {
            **company,
            "decision_maker": {
                "name": "Decision Maker",
                "title": "HR Director",
                "email": f"hr@{company['domain']}",
                "confidence": 85
            },
            "potential_savings": calculate_potential_savings(company['employees_count'])
        }

        # Score the lead
        lead['score'] = score_lead(lead)

        leads.append(lead)

    # Save leads
    filename = save_daily_leads(leads, date_str)

    print(f"\n✅ Generated {len(leads)} leads")
    print(f"📁 Saved to: {filename}")

    # Summary stats
    high_priority = sum(1 for l in leads if l['score'] >= 70)
    total_potential_savings = sum(l['potential_savings']['total'] for l in leads)

    print(f"\n📊 Summary:")
    print(f"   High Priority: {high_priority}")
    print(f"   Total Potential Savings: ${total_potential_savings:,}")

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
