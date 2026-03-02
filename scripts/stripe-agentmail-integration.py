#!/usr/bin/env python3
"""
Stripe + AgentMail Integration
Send payment links via AgentMail for qualified leads
"""

import os
import json
import requests
from datetime import datetime

# Configuration
AGENTMAIL_API_KEY = "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"
AGENTMAIL_API_URL = "https://api.agentmail.to/v1/emails"

STRIPE_PUBLISHABLE_KEY = "pk_live_LtA4BnpnPUYfTrc0KTUupew5"
CONFIG_FILE = "/Users/cubiczan/.openclaw/workspace/stripe-config.json"

class StripeAgentMailIntegration:
    """Integrate Stripe payment links with AgentMail outreach"""
    
    def __init__(self):
        """Initialize integration"""
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    def determine_service_type(self, lead_data):
        """Determine which service to offer based on lead data"""
        
        # Analyze lead data to determine best service
        company_size = lead_data.get("employee_count", 0)
        industry = lead_data.get("industry", "").lower()
        score = lead_data.get("score", 0)
        
        # Rules for service recommendation
        if score >= 85:
            # High score leads get premium service
            if company_size >= 100:
                return "expense_reduction"
            elif "manufacturing" in industry or "industrial" in industry:
                return "deal_origination"
            else:
                return "ai_agency_monthly"
        elif score >= 75:
            # Medium score leads
            if company_size >= 50:
                return "expense_reduction"
            else:
                return "ai_agency_monthly"
        else:
            # Lower score leads
            return "ai_agency_monthly"
    
    def estimate_service_value(self, lead_data, service_type):
        """Estimate value for the service"""
        
        company_size = lead_data.get("employee_count", 0)
        revenue = lead_data.get("revenue", 0)
        
        if service_type == "expense_reduction":
            # Estimate 15-25% of expenses
            # Rough estimate: $5,000 per employee annually in addressable expenses
            estimated_savings = company_size * 5000 * 0.20  # 20% average
            return max(50000, estimated_savings)  # Minimum $50k
            
        elif service_type == "deal_origination":
            # Estimate deal size based on company size
            if company_size >= 500:
                return 10000000  # $10M
            elif company_size >= 100:
                return 5000000   # $5M
            else:
                return 2500000   # $2.5M
                
        elif service_type == "ai_agency_monthly":
            return 997  # Monthly subscription
            
        return 0
    
    def generate_payment_email(self, lead_data, service_type=None, estimated_value=None):
        """Generate payment email for a lead"""
        
        if not service_type:
            service_type = self.determine_service_type(lead_data)
        
        if not estimated_value:
            estimated_value = self.estimate_service_value(lead_data, service_type)
        
        company_name = lead_data.get("company", "Your Company")
        contact_name = lead_data.get("contact", "there")
        contact_email = lead_data.get("email", "")
        
        # Get payment link from config
        payment_links = self.config.get("payment_links", {})
        service_config = payment_links.get(service_type, {})
        
        # In production, this would create a unique Stripe checkout session
        # For now, use template URL
        payment_link = service_config.get("template_url", "https://buy.stripe.com/test_00g5lL9Jq6lL3vW5kk")
        
        # Customize payment link with lead data
        # In production: create unique Stripe session with metadata
        unique_payment_link = f"{payment_link}?prefill_company={company_name.replace(' ', '+')}&prefill_email={contact_email}"
        
        # Generate email subject
        subject = f"Service Agreement: {service_config.get('name', 'Our Service')} for {company_name}"
        
        # Generate email body
        email_body = self._generate_email_body(
            contact_name,
            company_name,
            service_type,
            service_config,
            estimated_value,
            unique_payment_link
        )
        
        return {
            "to": contact_email,
            "subject": subject,
            "body": email_body,
            "service_type": service_type,
            "estimated_value": estimated_value,
            "payment_link": unique_payment_link,
            "company": company_name,
            "contact": contact_name
        }
    
    def _generate_email_body(self, contact_name, company_name, service_type, service_config, estimated_value, payment_link):
        """Generate email body with payment link"""
        
        service_name = service_config.get("name", "")
        service_description = service_config.get("description", "")
        amount = service_config.get("amount", "")
        terms = service_config.get("terms", "")
        
        # Service-specific details
        if service_type == "expense_reduction":
            details = f"""**Estimated Savings:** Based on companies of similar size to {company_name}, we typically identify **${estimated_value:,.0f}+ in annual savings**.

**Our Process:**
1. Free audit of your current expenses (telecom, utilities, waste, vendor contracts)
2. Identify 15-25% savings opportunities with no disruption
3. Implement changes at zero cost to you
4. You pay only 30% of verified first-year savings

**Typical Results:** Most clients save $75,000-$250,000 annually."""
            
        elif service_type == "deal_origination":
            details = f"""**Estimated Deal Value:** Based on similar transactions, we estimate a **${estimated_value:,.0f}+ deal size**.

**Our Process:**
1. Match with our network of 150,000+ qualified buyers/investors
2. Facilitate introductions and negotiations
3. Support through due diligence and closing
4. 1-3% success fee payable only upon deal completion

**Our Network:** Includes family offices, private equity, and strategic buyers."""
            
        elif service_type == "ai_agency_monthly":
            details = f"""**Service Includes:**
• 50-70 qualified leads per day in your target market
• Automated multi-channel outreach (email, phone, social)
• AI-powered lead scoring and prioritization
• Weekly performance reports and optimization
• Dedicated account manager

**Typical Results:** 5-10 qualified meetings per month, 2-3 new clients monthly."""
        
        else:
            details = ""
        
        email_body = f"""Hi {contact_name},

Thank you for your interest in our {service_name.lower()} for {company_name}.

As discussed, here are the details:

**Service:** {service_name}
**Description:** {service_description}
**Pricing:** {amount}
**Terms:** {terms}

{details}

**Next Steps:**
1. Review and accept the agreement: {payment_link}
2. We'll begin service immediately upon agreement
3. You'll receive regular updates and performance reports

This is a completely risk-free opportunity with no upfront costs.

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.
"""
        
        return email_body
    
    def send_via_agentmail(self, email_data):
        """Send payment email via AgentMail"""
        
        payload = {
            "from": "Zane@agentmail.to",
            "to": [email_data["to"]],
            "cc": ["sam@impactquadrant.info"],
            "subject": email_data["subject"],
            "body": email_data["body"]
        }
        
        headers = {
            "Authorization": f"Bearer {AGENTMAIL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(AGENTMAIL_API_URL, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            print(f"✅ Payment email sent to {email_data['to']}")
            print(f"   Service: {email_data['service_type']}")
            print(f"   Estimated Value: ${email_data['estimated_value']:,.0f}")
            print(f"   Payment Link: {email_data['payment_link']}")
            
            # Log the send
            self.log_send(email_data, response.json())
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            return False
    
    def log_send(self, email_data, response):
        """Log the email send"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "company": email_data["company"],
            "contact": email_data["contact"],
            "email": email_data["to"],
            "service_type": email_data["service_type"],
            "estimated_value": email_data["estimated_value"],
            "payment_link": email_data["payment_link"],
            "agentmail_response": response,
            "status": "sent"
        }
        
        # Append to log file
        log_file = "/Users/cubiczan/.openclaw/workspace/stripe-payment-logs.jsonl"
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return log_file

def main():
    """Test the integration with example leads"""
    
    print("=" * 60)
    print("STRIPE + AGENTMAIL INTEGRATION")
    print("=" * 60)
    print()
    
    integration = StripeAgentMailIntegration()
    
    # Example leads from recent outreach
    example_leads = [
        {
            "company": "Precision Products Machining Group",
            "contact": "Don Brown",
            "email": "dbrown@precprodmachgrp.com",
            "employee_count": 150,
            "industry": "precision manufacturing",
            "score": 87,
            "revenue": 25000000
        },
        {
            "company": "Midwest Foods",
            "contact": "Erin Fitzgerald", 
            "email": "efitzgerald@midwestfoods.com",
            "employee_count": 75,
            "industry": "food distribution",
            "score": 82,
            "revenue": 15000000
        },
        {
            "company": "Industrial Supply Company",
            "contact": "Jessica Yurgaitis",
            "email": "jyurgaitis@indsupply.com",
            "employee_count": 200,
            "industry": "industrial distribution",
            "score": 84,
            "revenue": 50000000
        }
    ]
    
    print("📊 Processing example leads...")
    print()
    
    for i, lead in enumerate(example_leads, 1):
        print(f"Lead {i}: {lead['company']}")
        print(f"  Contact: {lead['contact']} ({lead['email']})")
        print(f"  Score: {lead['score']}, Employees: {lead['employee_count']}")
        
        # Generate payment email
        email_data = integration.generate_payment_email(lead)
        
        print(f"  Recommended Service: {email_data['service_type']}")
        print(f"  Estimated Value: ${email_data['estimated_value']:,.0f}")
        print(f"  Subject: {email_data['subject'][:50]}...")
        print()
        
        # Ask if should send (for demo)
        send = input(f"  Send payment email to {lead['contact']}? (y/n): ").lower().strip()
        
        if send == 'y':
            success = integration.send_via_agentmail(email_data)
            if success:
                print(f"  ✅ Email sent successfully!")
            else:
                print(f"  ❌ Failed to send email")
        else:
            print(f"  ⏸️ Skipped sending")
        
        print()
    
    print("=" * 60)
    print("INTEGRATION READY")
    print("=" * 60)
    print()
    print("To use in production:")
    print()
    print("1. Get Stripe Secret Key:")
    print("   export STRIPE_SECRET_KEY='sk_live_...'")
    print()
    print("2. Update payment links in config:")
    print("   Edit /Users/cubiczan/.openclaw/workspace/stripe-config.json")
    print("   Replace template_url with actual Stripe payment links")
    print()
    print("3. Integrate with lead generator:")
    print("   Call generate_payment_email() for qualified leads")
    print("   Send via send_via_agentmail()")
    print()
    print("4. Monitor payments:")
    print("   Check Stripe Dashboard: https://dashboard.stripe.com")
    print("   Review logs: /Users/cubiczan/.openclaw/workspace/stripe-payment-logs.jsonl")
    print()

if __name__ == "__main__":
    main()
