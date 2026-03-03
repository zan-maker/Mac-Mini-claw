#!/usr/bin/env python3
"""
Final Stripe Payment System Setup
Complete setup with all three service types working
"""

import os
import stripe
import json
from datetime import datetime

# Configuration
STRIPE_SECRET_KEY = "sk_live_vBFAd5xw4PkQBWCGKkVO63La"
STRIPE_PUBLISHABLE_KEY = "pk_live_LtA4BnpnPUYfTrc0KTUupew5"

# Initialize Stripe
stripe.api_key = STRIPE_SECRET_KEY
stripe.api_version = "2025-02-24.acacia"

def verify_stripe_connection():
    """Verify Stripe API connection"""
    
    print("🔗 Verifying Stripe connection...")
    
    try:
        balance = stripe.Balance.retrieve()
        print(f"✅ Stripe connection successful")
        print(f"   Available: ${balance.available[0].amount/100:.2f} {balance.available[0].currency}")
        print(f"   Pending: ${balance.pending[0].amount/100:.2f} {balance.pending[0].currency}")
        return True
    except Exception as e:
        print(f"❌ Stripe connection failed: {str(e)}")
        return False

def create_complete_payment_system():
    """Create complete payment system for all three services"""
    
    print()
    print("=" * 60)
    print("COMPLETE PAYMENT SYSTEM SETUP")
    print("=" * 60)
    print()
    
    # Load existing config
    config_file = "/Users/cubiczan/.openclaw/workspace/stripe-config.json"
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    print("📦 Products already created:")
    for service, product_id in config.get("products", {}).items():
        try:
            product = stripe.Product.retrieve(product_id)
            print(f"   ✅ {product.name} (ID: {product.id})")
        except:
            print(f"   ❌ {service}: Product not found")
    
    print()
    print("💰 Prices already created:")
    for service, price_id in config.get("prices", {}).items():
        try:
            price = stripe.Price.retrieve(price_id)
            amount = f"${price.unit_amount/100:.2f}" if price.unit_amount > 0 else "Contingency-based"
            print(f"   ✅ {service}: {amount}")
        except:
            print(f"   ❌ {service}: Price not found")
    
    print()
    print("🔗 Payment links:")
    
    # Create payment link for subscription service
    subscription_price_id = config["prices"]["ai_agency_monthly"]
    try:
        # Check if payment link already exists
        payment_links = stripe.PaymentLink.list(limit=10)
        existing_link = None
        for link in payment_links.data:
            if link.line_items and link.line_items[0].price == subscription_price_id:
                existing_link = link
                break
        
        if existing_link:
            print(f"   ✅ AI Agency Subscription: {existing_link.url}")
            config["payment_links"] = {
                "ai_agency_monthly": {
                    "name": "AI Agency Monthly Subscription",
                    "url": existing_link.url,
                    "price": "$997.00"
                }
            }
        else:
            # Create new payment link
            payment_link = stripe.PaymentLink.create(
                line_items=[{
                    "price": subscription_price_id,
                    "quantity": 1
                }],
                after_completion={
                    "type": "redirect",
                    "redirect": {
                        "url": "https://impactquadrant.info/thank-you"
                    }
                }
            )
            print(f"   ✅ Created AI Agency Subscription: {payment_link.url}")
            config["payment_links"] = {
                "ai_agency_monthly": {
                    "name": "AI Agency Monthly Subscription",
                    "url": payment_link.url,
                    "price": "$997.00"
                }
            }
    except Exception as e:
        print(f"   ❌ Error creating payment link: {str(e)}")
    
    print()
    print("📝 Service agreements:")
    
    # Create service agreement structure
    service_agreements = {
        "expense_reduction": {
            "name": "Expense Reduction Service Agreement",
            "description": "Contingency-based - 30% of verified savings",
            "agreement_type": "contingency",
            "fee_percentage": 30,
            "process": [
                "1. Free expense audit",
                "2. Identify 15-25% savings opportunities",
                "3. Implement changes at no cost",
                "4. Verify savings",
                "5. Invoice 30% of first-year savings"
            ],
            "agreement_url": "https://impactquadrant.info/agreements/expense-reduction",
            "invoice_template": "Custom amount based on verified savings"
        },
        "deal_origination": {
            "name": "Deal Origination Referral Agreement",
            "description": "Success fee - 1-3% of deal value",
            "agreement_type": "success_fee",
            "fee_percentage_range": "1-3",
            "process": [
                "1. Match with qualified buyers",
                "2. Facilitate introductions",
                "3. Support negotiations",
                "4. Deal closes successfully",
                "5. Invoice 1-3% of deal value"
            ],
            "agreement_url": "https://impactquadrant.info/agreements/deal-origination",
            "invoice_template": "Custom amount based on deal value"
        },
        "ai_agency_monthly": {
            "name": "AI Agency Subscription Agreement",
            "description": "Monthly subscription - $997/month",
            "agreement_type": "subscription",
            "monthly_price": 99700,  # in cents
            "process": [
                "1. Sign up via Stripe",
                "2. Monthly billing automatically",
                "3. Receive 50-70 leads/day",
                "4. Automated outreach and follow-up"
            ],
            "agreement_url": "https://buy.stripe.com/aFa14nfHp7MSa6a7Fo8g000",
            "payment_link": "https://buy.stripe.com/aFa14nfHp7MSa6a7Fo8g000"
        }
    }
    
    config["service_agreements"] = service_agreements
    
    for service, agreement in service_agreements.items():
        print(f"   ✅ {agreement['name']}")
        print(f"      {agreement['description']}")
        print(f"      URL: {agreement['agreement_url']}")
    
    print()
    print("📧 Email templates:")
    
    # Create email templates for each service
    email_templates = {
        "expense_reduction": {
            "subject": "Expense Reduction Service Agreement for {company_name}",
            "body_template": """Hi {contact_name},

Thank you for your interest in our Expense Reduction Service for {company_name}.

As discussed, here are the details:

**Service:** Expense Reduction Service
**Description:** We identify 15-25% savings in your operating expenses (telecom, utilities, waste, vendor contracts)
**Pricing:** Contingency-based - 30% of verified first-year savings
**Terms:** No upfront cost. You pay only from savings we generate.

**Estimated Savings:** Based on companies of similar size, we typically identify ${estimated_savings:,.0f}+ in annual savings.

**Next Steps:**
1. Review and sign the service agreement: {agreement_url}
2. We'll conduct a free expense audit
3. Identify specific savings opportunities
4. Implement changes at no cost to you
5. You pay 30% of verified savings

This is completely risk-free - you pay nothing unless we deliver measurable savings.

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
        },
        "deal_origination": {
            "subject": "Deal Origination Referral Agreement for {company_name}",
            "body_template": """Hi {contact_name},

Thank you for your interest in our Deal Origination service for {company_name}.

As discussed, here are the details:

**Service:** Deal Origination Referral
**Description:** We match you with qualified buyers/investors from our network of 150,000+ contacts
**Pricing:** Success fee - 1-3% of successful deal value
**Terms:** No upfront cost. Pay only upon successful deal closing.

**Estimated Deal Value:** Based on similar transactions, we estimate a ${estimated_deal_value:,.0f}+ deal size.

**Next Steps:**
1. Review and sign the referral agreement: {agreement_url}
2. We'll match you with qualified buyers
3. Facilitate introductions and negotiations
4. Support through due diligence
5. You pay 1-3% fee upon successful closing

Our network includes family offices, private equity firms, and strategic buyers actively seeking opportunities.

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
        },
        "ai_agency_monthly": {
            "subject": "AI Agency Subscription for {company_name}",
            "body_template": """Hi {contact_name},

Thank you for your interest in our AI Agency service for {company_name}.

As discussed, here are the details:

**Service:** AI Agency Monthly Subscription
**Description:** 50-70 qualified leads per day with automated multi-channel outreach
**Pricing:** $997/month
**Terms:** Monthly subscription, cancel anytime

**Service Includes:**
• 50-70 qualified leads per day in your target market
• Automated email, phone, and social media outreach
• AI-powered lead scoring and prioritization
• Weekly performance reports
• Dedicated account manager

**Typical Results:** 5-10 qualified meetings per month, 2-3 new clients monthly.

**Next Steps:**
1. Sign up via our secure payment link: {payment_link}
2. We'll begin service immediately
3. You'll receive your first leads within 24 hours
4. Monthly billing of $997 automatically

Try it risk-free - cancel anytime if not satisfied.

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
        }
    }
    
    config["email_templates"] = email_templates
    print("   ✅ Created email templates for all three services")
    
    # Update configuration
    config["complete_setup_date"] = datetime.now().isoformat()
    config["stripe_secret_key"] = "sk_live_... (configured)"  # Don't store actual key
    config["stripe_publishable_key"] = STRIPE_PUBLISHABLE_KEY
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print()
    print(f"✅ Configuration saved: {config_file}")
    
    return config

def create_quick_start_guide():
    """Create quick start guide for using the payment system"""
    
    print()
    print("=" * 60)
    print("QUICK START GUIDE")
    print("=" * 60)
    print()
    
    guide = """
# Stripe Payment System - Quick Start Guide

## Three Service Models:

### 1. Expense Reduction Service (Contingency-based)
- **Pricing:** 30% of verified savings
- **Payment:** After savings verified, create invoice
- **Agreement:** https://impactquadrant.info/agreements/expense-reduction
- **Process:** Audit → Identify savings → Implement → Verify → Invoice

### 2. Deal Origination Referral (Success fee)
- **Pricing:** 1-3% of deal value
- **Payment:** Upon successful deal closing
- **Agreement:** https://impactquadrant.info/agreements/deal-origination
- **Process:** Match → Introduce → Negotiate → Close → Invoice

### 3. AI Agency Monthly Subscription
- **Pricing:** $997/month
- **Payment:** Monthly recurring via Stripe
- **Signup:** https://buy.stripe.com/aFa14nfHp7MSa6a7Fo8g000
- **Process:** Signup → Monthly billing → Service delivery

## How to Use:

### For Qualified Leads:
1. Determine which service fits the lead
2. Send appropriate email template with agreement/payment link
3. Track responses in Stripe Dashboard
4. Follow up based on payment status

### Integration with AgentMail:
Use the `stripe-agentmail-integration.py` script to:
- Generate personalized payment emails
- Send via AgentMail API
- Track sends and responses

### Monitoring Payments:
- **Dashboard:** https://dashboard.stripe.com
- **Subscriptions:** Active/Churned customers
- **Invoices:** Paid/Pending/Overdue
- **Revenue:** Monthly recurring revenue (MRR)

## Testing:
- **Test mode:** Use `sk_test_...` and `pk_test_...` keys
- **Test card:** `4242 4242 4242 4242` (success)
- **Test email:** Any email works in test mode

## Next Steps:
1. Create actual agreement documents at the URLs above
2. Integrate with lead generator cron jobs
3. Set up webhooks for payment notifications
4. Create reporting dashboard
"""
    
    guide_file = "/Users/cubiczan/.openclaw/workspace/docs/STRIPE_QUICK_START.md"
    with open(guide_file, 'w') as f:
        f.write(guide)
    
    print("✅ Quick start guide created:")
    print(f"   {guide_file}")
    print()
    print("📋 Key URLs:")
    print("   • AI Agency Signup: https://buy.stripe.com/aFa14nfHp7MSa6a7Fo8g000")
    print("   • Expense Reduction Agreement: https://impactquadrant.info/agreements/expense-reduction")
    print("   • Deal Origination Agreement: https://impactquadrant.info/agreements/deal-origination")
    print("   • Stripe Dashboard: https://dashboard.stripe.com")
    print()
    
    return guide_file

def main():
    """Main setup function"""
    
    print("=" * 60)
    print("FINAL STRIPE PAYMENT SYSTEM SETUP")
    print("=" * 60)
    print()
    
    # Verify connection
    if not verify_stripe_connection():
        print("❌ Cannot proceed without Stripe connection")
        return
    
    # Create complete system
    config = create_complete_payment_system()
    
    # Create quick start guide
    guide_file = create_quick_start_guide()
    
    print("=" * 60)
    print("✅ SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("🎉 Your Stripe payment system is ready!")
    print()
    print("What's available:")
    print("1. ✅ AI Agency Monthly Subscription - $997/month")
    print("   • Signup: https://buy.stripe.com/aFa14nfHp7MSa6a7Fo8g000")
    print("   • Monthly recurring billing")
    print()
    print("2. ✅ Expense Reduction Service - Contingency-based")
    print("   • Agreement: https://impactquadrant.info/agreements/expense-reduction")
    print("   • 30% of verified savings")
    print("   • Invoice after savings verified")
    print()
    print("3. ✅ Deal Origination Referral - Success fee")
    print("   • Agreement: https://impactquadrant.info/agreements/deal-origination")
    print("   • 1-3% of deal value")
    print("   • Invoice after deal closes")
    print()
    print("📊 Next actions:")
    print("1. Test AI Agency subscription with test card: 4242 4242 4242 4242")
    print("2. Create actual agreement documents at the URLs above")
    print("3. Integrate with lead generator for automated payment emails")
    print("4. Monitor payments in Stripe Dashboard")
    print()
    print("Configuration: /Users/cubiczan/.openclaw/workspace/stripe-config.json")
    print("Quick Start: /Users/cubiczan/.openclaw/workspace/docs/STRIPE_QUICK_START.md")
    print("Scripts: /Users/cubiczan/.openclaw/workspace/scripts/stripe-*.py")
    print()

if __name__ == "__main__":
    main()
