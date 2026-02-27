#!/usr/bin/env python3
"""
Process Craigslist leads and send outreach emails
Focus: Referral fee opportunities
"""

import json
import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import re

# Configuration
CONFIG = {
    "leads_dir": "/Users/cubiczan/.openclaw/workspace/craigslist-leads",
    "processed_dir": "/Users/cubiczan/.openclaw/workspace/craigslist-leads/processed",
    "agentmail_api_key": "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f",
    "from_email": "Zane@agentmail.to",
    "cc_email": "sam@impactquadrant.info"
}

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def get_todays_leads():
    """Get leads from today's scraping"""
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    leads_file = f"{CONFIG['leads_dir']}/daily_leads_{date_str}.json"
    
    if not os.path.exists(leads_file):
        # Try yesterday's file
        yesterday = datetime.now() - timedelta(days=1)
        date_str = yesterday.strftime("%Y-%m-%d")
        leads_file = f"{CONFIG['leads_dir']}/daily_leads_{date_str}.json"
    
    if not os.path.exists(leads_file):
        print(f"No leads file found for today or yesterday")
        return []
    
    try:
        with open(leads_file, 'r') as f:
            leads = json.load(f)
        print(f"Loaded {len(leads)} leads from {leads_file}")
        return leads
    except Exception as e:
        print(f"Error loading leads: {e}")
        return []

def extract_contact_info(lead: Dict) -> Dict:
    """Extract contact information from lead"""
    
    title = lead.get("title", "")
    description = lead.get("description", "")
    text = f"{title} {description}"
    
    contact = {
        "email": None,
        "phone": None,
        "name": None
    }
    
    # Try to extract email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    if emails:
        contact["email"] = emails[0]
    
    # Try to extract phone
    phone_patterns = [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
    ]
    
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            contact["phone"] = phones[0]
            break
    
    # Try to extract name from title (first 2-3 words)
    words = title.split()[:3]
    if len(words) >= 2:
        contact["name"] = " ".join(words)
    
    return contact

def generate_business_sale_email(lead: Dict, contact: Dict) -> Dict:
    """Generate email for business-for-sale opportunity"""
    
    business_name = lead.get("title", "Business")[:50]
    city = lead.get("city", "").title()
    price = lead.get("price", "$XXX,XXX")
    fee_info = lead.get("referral_fee", {})
    estimated_fee = fee_info.get("estimated_fee", 0)
    
    # Use contact name or generic
    name = contact.get("name", "Business Owner")
    first_name = name.split()[0] if name else "there"
    
    subject = f"Quick question about {business_name} in {city}"
    
    body = f"""Hi {first_name},

I came across your listing for {business_name} in {city} and wanted to reach out.

Our firm specializes in connecting business sellers with qualified buyers, and we have an extensive network of investors actively looking for opportunities like yours.

We offer:
✓ **No upfront fees** - we only get paid when you sell
✓ **Access to our investor database** (149,000+ contacts)
✓ **Full confidentiality** throughout the process
✓ **Expert valuation** and deal structuring

Given the asking price of {price}, we're confident we can help you find the right buyer quickly and efficiently.

Would you be open to a brief 15-minute call next week to discuss your goals for the sale? I'd be happy to share examples of similar businesses we've successfully helped sell.

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.

P.S. Our average business sale closes within 90-120 days, and we consistently achieve premium valuations for our clients.
"""
    
    return {
        "subject": subject,
        "body": body,
        "category": "business_for_sale",
        "estimated_fee": estimated_fee
    }

def generate_service_business_email(lead: Dict, contact: Dict) -> Dict:
    """Generate email for service business expense reduction"""
    
    business_name = lead.get("title", "Business")[:50]
    city = lead.get("city", "").title()
    fee_info = lead.get("referral_fee", {})
    estimated_fee = fee_info.get("estimated_fee", 0)
    potential_savings = fee_info.get("potential_savings", 0)
    
    # Use contact name or generic
    name = contact.get("name", "Business Owner")
    first_name = name.split()[0] if name else "there"
    
    subject = f"Quick question about {business_name}'s operating expenses"
    
    body = f"""Hi {first_name},

I hope this message finds you well. I'm reaching out because we specialize in helping {business_name}-type businesses reduce operating expenses by 15-25% without compromising quality or service levels.

Our team has successfully partnered with similar organizations in {city} and consistently delivers:

✓ **15-25% reduction** in telecommunications, waste management, and utility costs
✓ **100% contingency-based model** - you only pay from savings generated
✓ **Zero upfront costs** or risks to your organization
✓ **Average client savings:** $75,000-$150,000 annually

We're confident we can identify significant savings opportunities across your vendor contracts and operational expenses.

Would you be open to a brief 15-minute call next week to explore potential areas where we might help reduce costs? I'd be happy to share specific examples from similar businesses in your industry.

If you're not the right person to speak with about this, could you point me in the right direction?

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.

P.S. There's absolutely no cost unless we deliver measurable, verified savings.
"""
    
    return {
        "subject": subject,
        "body": body,
        "category": "service_business",
        "estimated_fee": estimated_fee,
        "potential_savings": potential_savings
    }

def send_agentmail_email(to_email: str, subject: str, body: str) -> bool:
    """Send email via AgentMail API"""
    
    if not to_email:
        print("  No email address, skipping")
        return False
    
    url = "https://api.agentmail.to/v1/emails"
    
    headers = {
        "Authorization": f"Bearer {CONFIG['agentmail_api_key']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": CONFIG["from_email"],
        "to": [to_email],
        "cc": [CONFIG["cc_email"]],
        "subject": subject,
        "body": body
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            print(f"  ✅ Email sent to {to_email}")
            return True
        else:
            print(f"  ❌ Failed to send email: HTTP {response.status_code}")
            print(f"     Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error sending email: {e}")
        return False

def process_leads():
    """Main processing function"""
    
    print(f"{'='*60}")
    print(f"CRAIGSLIST LEAD PROCESSOR")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    ensure_dir(CONFIG["processed_dir"])
    
    # Get today's leads
    leads = get_todays_leads()
    if not leads:
        print("No leads to process")
        return
    
    # Sort by estimated fee (highest first)
    leads.sort(key=lambda x: x.get("referral_fee", {}).get("estimated_fee", 0), reverse=True)
    
    print(f"Processing {len(leads)} leads...")
    
    results = {
        "total_processed": 0,
        "emails_sent": 0,
        "total_estimated_fees": 0,
        "by_category": {
            "business_for_sale": {"processed": 0, "sent": 0, "fees": 0},
            "service_business": {"processed": 0, "sent": 0, "fees": 0}
        },
        "sent_emails": []
    }
    
    # Process top 10 leads (to avoid rate limiting)
    for i, lead in enumerate(leads[:10]):
        print(f"\n{i+1}. Processing: {lead.get('title', 'Unknown')[:50]}...")
        
        # Extract contact info
        contact = extract_contact_info(lead)
        print(f"   Contact: {contact.get('name', 'N/A')}, Email: {contact.get('email', 'N/A')}")
        
        if not contact.get("email"):
            print("   Skipping: No email address found")
            continue
        
        # Generate email based on category
        category = lead.get("category", "")
        fee_info = lead.get("referral_fee", {})
        estimated_fee = fee_info.get("estimated_fee", 0)
        
        if category == "business_for_sale":
            email_data = generate_business_sale_email(lead, contact)
            category_key = "business_for_sale"
        else:
            email_data = generate_service_business_email(lead, contact)
            category_key = "service_business"
        
        # Send email
        print(f"   Category: {category_key}, Est. Fee: ${estimated_fee:,.0f}")
        
        sent = send_agentmail_email(
            contact["email"],
            email_data["subject"],
            email_data["body"]
        )
        
        # Update results
        results["total_processed"] += 1
        results["by_category"][category_key]["processed"] += 1
        results["by_category"][category_key]["fees"] += estimated_fee
        
        if sent:
            results["emails_sent"] += 1
            results["by_category"][category_key]["sent"] += 1
            results["total_estimated_fees"] += estimated_fee
            
            results["sent_emails"].append({
                "to": contact["email"],
                "subject": email_data["subject"],
                "category": category_key,
                "estimated_fee": estimated_fee,
                "lead_title": lead.get("title", "")[:50],
                "sent_at": datetime.now().isoformat()
            })
        
        # Be respectful between emails
        import time
        time.sleep(2)
    
    # Save results
    date_str = datetime.now().strftime("%Y-%m-%d")
    results_file = f"{CONFIG['processed_dir']}/processing_results_{date_str}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"\n{'='*60}")
    print("PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"Total Leads Processed: {results['total_processed']}")
    print(f"Emails Sent: {results['emails_sent']}")
    print(f"Total Estimated Fees: ${results['total_estimated_fees']:,.2f}")
    
    print(f"\nBy Category:")
    for category, stats in results["by_category"].items():
        if stats["processed"] > 0:
            category_name = category.replace("_", " ").title()
            print(f"  {category_name}:")
            print(f"    Processed: {stats['processed']}")
            print(f"    Emails Sent: {stats['sent']}")
            print(f"    Estimated Fees: ${stats['fees']:,.2f}")
    
    print(f"\nResults saved to: {results_file}")
    print(f"{'='*60}")
    
    # Create Discord report
    discord_report = create_discord_report(results)
    discord_file = f"{CONFIG['processed_dir']}/discord_report_{date_str}.txt"
    
    with open(discord_file, 'w') as f:
        f.write(discord_report)
    
    print(f"Discord report: {discord_file}")
    
    return results

def create_discord_report(results: Dict) -> str:
    """Create Discord-friendly report"""
    
    message = f"**📧 Craigslist Lead Processing Report**\n"
    message += f"*{datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
    
    message += f"**Leads Processed:** {results['total_processed']}\n"
    message += f"**Emails Sent:** {results['emails_sent']}\n"
    message += f"**Total Estimated Fees:** ${results['total_estimated_fees']:,.2f}\n\n"
    
    # Category breakdown
    biz_stats = results["by_category"]["business_for_sale"]
    service_stats = results["by_category"]["service_business"]
    
    if biz_stats["processed"] > 0:
        message += f"**🏢 Business-for-Sale:**\n"
        message += f"  • Processed: {biz_stats['processed']}\n"
        message += f"  • Emails Sent: {biz_stats['sent']}\n"
        message += f"  • Est. Fees: ${biz_stats['fees']:,.0f}\n\n"
    
    if service_stats["processed"] > 0:
        message += f"**🔧 Service Businesses:**\n"
        message += f"  • Processed: {service_stats['processed']}\n"
        message += f"  • Emails Sent: {service_stats['sent']}\n"
        message += f"  • Est. Fees: ${service_stats['fees']:,.0f}\n\n"
    
    # Top opportunities
    if results["sent_emails"]:
        message += f"**🎯 Top Opportunities Sent:**\n"
        
        sorted_emails = sorted(results["sent_emails"], key=lambda x: x["estimated_fee"], reverse=True)
        
        for i, email in enumerate(sorted_emails[:3], 1):
            fee = email["estimated_fee"]
            category = "Biz Sale" if email["category"] == "business_for_sale" else "Service"
            title = email["lead_title"]
            
            message += f"{i}. **${fee:,.0f}** - {title}... ({category})\n"
    
    message += f"\n**📈 Next Steps:**\n"
    message += f"• Monitor email responses\n"
    message += f"• Schedule follow-up calls\n"
    message += f"• Track conversions in CRM\n"
    
    return message

if __name__ == "__main__":
    process_leads()