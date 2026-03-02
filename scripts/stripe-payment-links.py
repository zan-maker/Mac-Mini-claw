#!/usr/bin/env python3
"""
Stripe Payment Link Generator for Outreach Emails
Generates payment links to include in AgentMail outreach
"""

import os
import json
from datetime import datetime

# Configuration
STRIPE_PUBLISHABLE_KEY = "pk_live_LtA4BnpnPUYfTrc0KTUupew5"
CONFIG_FILE = "/Users/cubiczan/.openclaw/workspace/stripe-config.json"

class PaymentLinkGenerator:
    """Generate payment links for different services"""
    
    # Pre-defined payment links (these would be created in Stripe Dashboard)
    PAYMENT_LINKS = {
        "expense_reduction": {
            "name": "Expense Reduction Service Agreement",
            "description": "15-25% OPEX reduction contingency fee (30% of verified savings)",
            "template_url": "https://buy.stripe.com/test_00g5lL9Jq6lL3vW5kk",  # Example
            "amount": "Contingency-based (30% of savings)",
            "terms": "No upfront cost. Pay only from verified savings."
        },
        "deal_origination": {
            "name": "Deal Origination Referral Agreement", 
            "description": "Success-based referral fee (1-3% of deal value)",
            "template_url": "https://buy.stripe.com/test_00g5lL9Jq6lL3vW5kk",  # Example
            "amount": "Success fee (1-3% of deal)",
            "terms": "Payable upon successful deal closing."
        },
        "ai_agency_monthly": {
            "name": "AI Agency Monthly Subscription",
            "description": "Monthly lead generation service (50-70 leads/day)",
            "template_url": "https://buy.stripe.com/test_00g5lL9Jq6lL3vW5kk",  # Example
            "amount": "$997/month",
            "terms": "Monthly subscription, cancel anytime."
        }
    }
    
    def generate_payment_email(self, service_type, company_name, contact_name, estimated_value=None):
        """Generate email text with payment link"""
        
        if service_type not in self.PAYMENT_LINKS:
            raise ValueError(f"Unknown service type: {service_type}")
        
        service = self.PAYMENT_LINKS[service_type]
        
        # Customize the payment link (in production, this would create a unique link)
        payment_link = service["template_url"]  # In production: create unique Stripe session
        
        # Generate email text
        email_text = f"""Hi {contact_name},

Thank you for your interest in our {service['name'].lower()} for {company_name}.

As discussed, here are the details:

**Service:** {service['name']}
**Description:** {service['description']}
**Pricing:** {service['amount']}
**Terms:** {service['terms']}

{self._get_service_specific_text(service_type, estimated_value)}

**Next Steps:**
1. Review and accept the agreement via this link: {payment_link}
2. We'll begin service immediately upon agreement
3. You'll receive regular updates and reports

If you have any questions, please don't hesitate to reach out.

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.
"""
        
        return email_text, payment_link
    
    def _get_service_specific_text(self, service_type, estimated_value):
        """Get service-specific text"""
        
        if service_type == "expense_reduction":
            return f"""**Estimated Savings:** Based on companies of similar size, we typically identify ${estimated_value or '75,000'}-${int(estimated_value or 150000) * 1.5 if estimated_value else '150,000'}+ in annual savings.

**Our Process:**
1. Free audit of your current expenses
2. Identify 15-25% savings opportunities
3. Implement changes at no cost to you
4. You pay 30% of verified first-year savings"""
        
        elif service_type == "deal_origination":
            return f"""**Deal Value:** Based on similar transactions, estimated deal size: ${estimated_value or '2,500,000'}

**Our Process:**
1. Match with qualified buyers/investors
2. Facilitate introductions and negotiations
3. Support through due diligence
4. 1-3% fee payable upon successful closing"""
        
        elif service_type == "ai_agency_monthly":
            return f"""**Service Includes:**
• 50-70 qualified leads per day
• Automated outreach and follow-up
• Lead scoring and prioritization
• Weekly performance reports
• Dedicated account manager

**Results:** Typical clients see 5-10 qualified meetings per month from our service."""
        
        return ""
    
    def generate_agentmail_integration(self, service_type, company_name, contact_name, contact_email, estimated_value=None):
        """Generate AgentMail API payload with payment link"""
        
        email_text, payment_link = self.generate_payment_email(
            service_type, company_name, contact_name, estimated_value
        )
        
        subject = f"Service Agreement: {self.PAYMENT_LINKS[service_type]['name']} for {company_name}"
        
        payload = {
            "from": "Zane@agentmail.to",
            "to": [contact_email],
            "cc": ["sam@impactquadrant.info"],
            "subject": subject,
            "body": email_text
        }
        
        return payload
    
    def save_to_config(self):
        """Save payment link configuration"""
        
        config = {
            "stripe_publishable_key": STRIPE_PUBLISHABLE_KEY,
            "payment_links": self.PAYMENT_LINKS,
            "last_updated": datetime.now().isoformat(),
            "note": "Replace template_url with actual Stripe payment links once secret key is available"
        }
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Configuration saved to: {CONFIG_FILE}")
        return config

def main():
    """Test the payment link generator"""
    
    print("=" * 60)
    print("PAYMENT LINK GENERATOR FOR OUTREACH")
    print("=" * 60)
    print()
    
    generator = PaymentLinkGenerator()
    
    # Test examples
    test_cases = [
        {
            "service": "expense_reduction",
            "company": "Precision Products Machining Group",
            "contact": "Don Brown",
            "email": "dbrown@precprodmachgrp.com",
            "value": 103875  # Annual savings estimate
        },
        {
            "service": "deal_origination", 
            "company": "Midwest Foods",
            "contact": "Erin Fitzgerald",
            "email": "efitzgerald@midwestfoods.com",
            "value": 2500000  # Deal estimate
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"📧 Example {i}: {test['service'].replace('_', ' ').title()}")
        print(f"   Company: {test['company']}")
        print(f"   Contact: {test['contact']}")
        print()
        
        # Generate email
        email_text, payment_link = generator.generate_payment_email(
            test["service"],
            test["company"],
            test["contact"],
            test["value"]
        )
        
        print(f"   Payment Link: {payment_link}")
        print(f"   Email Preview: {email_text[:200]}...")
        print()
        
        # Generate AgentMail payload
        payload = generator.generate_agentmail_integration(
            test["service"],
            test["company"],
            test["contact"],
            test["email"],
            test["value"]
        )
        
        print(f"   AgentMail Subject: {payload['subject']}")
        print()
    
    # Save configuration
    config = generator.save_to_config()
    
    print("=" * 60)
    print("SETUP INSTRUCTIONS")
    print("=" * 60)
    print()
    print("1. Get Stripe Secret Key:")
    print("   • Go to: https://dashboard.stripe.com/apikeys")
    print("   • Copy 'Secret Key' (starts with sk_live_)")
    print("   • Export: export STRIPE_SECRET_KEY='sk_live_...'")
    print()
    print("2. Create actual payment links in Stripe:")
    print("   • Products → Payment Links → Create")
    print("   • Update template_url in PAYMENT_LINKS dictionary")
    print()
    print("3. Integrate with AgentMail:")
    print("   • Use generate_agentmail_integration() method")
    print("   • Send via AgentMail API")
    print()
    print("4. Test with test mode:")
    print("   • Use test keys: sk_test_..., pk_test_...")
    print("   • Test card: 4242 4242 4242 4242")
    print()

if __name__ == "__main__":
    main()
