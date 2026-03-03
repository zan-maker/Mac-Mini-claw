#!/usr/bin/env python3
"""
Stripe Invoice Setup for Contingency and Success-Fee Services
Creates invoice templates for expense reduction and deal origination services
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

def create_invoice_templates():
    """Create invoice templates for contingency and success-fee services"""
    
    print("=" * 60)
    print("CREATING INVOICE TEMPLATES")
    print("=" * 60)
    print()
    
    # Load existing config
    config_file = "/Users/cubiczan/.openclaw/workspace/stripe-config.json"
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Create invoice items for contingency services
    invoice_items = {}
    
    # Expense Reduction Service Invoice Item
    try:
        expense_invoice_item = stripe.InvoiceItem.create(
            amount=0,  # $0 - will be customized per invoice
            currency="usd",
            description="Expense Reduction Service - 30% of verified first-year savings",
            metadata={
                "service_type": "expense_reduction",
                "fee_percentage": "30",
                "pricing_model": "contingency",
                "min_savings": "50000"
            }
        )
        invoice_items["expense_reduction"] = expense_invoice_item.id
        print(f"✅ Created invoice item for Expense Reduction: {expense_invoice_item.id}")
    except Exception as e:
        print(f"❌ Error creating expense reduction invoice item: {str(e)}")
    
    # Deal Origination Invoice Item
    try:
        deal_invoice_item = stripe.InvoiceItem.create(
            amount=0,  # $0 - will be customized per invoice
            currency="usd",
            description="Deal Origination Referral Fee - 1-3% of successful deal value",
            metadata={
                "service_type": "deal_origination",
                "fee_percentage_range": "1-3",
                "pricing_model": "success_fee",
                "min_deal_size": "1000000"
            }
        )
        invoice_items["deal_origination"] = deal_invoice_item.id
        print(f"✅ Created invoice item for Deal Origination: {deal_invoice_item.id}")
    except Exception as e:
        print(f"❌ Error creating deal origination invoice item: {str(e)}")
    
    # Create invoice templates
    invoice_templates = {}
    
    # Expense Reduction Invoice Template
    try:
        expense_template = stripe.Invoice.create(
            auto_advance=False,
            collection_method="send_invoice",
            days_until_due=30,
            metadata={
                "template_type": "expense_reduction",
                "description": "Template for expense reduction service invoices"
            }
        )
        invoice_templates["expense_reduction"] = expense_template.id
        print(f"✅ Created invoice template for Expense Reduction: {expense_template.id}")
    except Exception as e:
        print(f"❌ Error creating expense reduction invoice template: {str(e)}")
    
    # Deal Origination Invoice Template
    try:
        deal_template = stripe.Invoice.create(
            auto_advance=False,
            collection_method="send_invoice",
            days_until_due=30,
            metadata={
                "template_type": "deal_origination",
                "description": "Template for deal origination referral invoices"
            }
        )
        invoice_templates["deal_origination"] = deal_template.id
        print(f"✅ Created invoice template for Deal Origination: {deal_template.id}")
    except Exception as e:
        print(f"❌ Error creating deal origination invoice template: {str(e)}")
    
    # Update configuration
    config["invoice_items"] = invoice_items
    config["invoice_templates"] = invoice_templates
    config["invoice_setup_date"] = datetime.now().isoformat()
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print()
    print(f"✅ Configuration updated: {config_file}")
    
    return config

def create_service_agreement_links():
    """Create service agreement links (PDFs or web pages) for contingency services"""
    
    print()
    print("=" * 60)
    print("SERVICE AGREEMENT LINKS")
    print("=" * 60)
    print()
    
    # These would be links to service agreement documents
    # For now, we'll create placeholder links that would be replaced with actual documents
    
    service_agreements = {
        "expense_reduction": {
            "name": "Expense Reduction Service Agreement",
            "description": "Contingency-based agreement - 30% of verified savings",
            "agreement_url": "https://impactquadrant.info/agreements/expense-reduction",
            "terms": "No upfront cost. Client pays 30% of verified first-year savings.",
            "process": "1. Free audit → 2. Identify savings → 3. Implement changes → 4. Verify savings → 5. Invoice 30%"
        },
        "deal_origination": {
            "name": "Deal Origination Referral Agreement",
            "description": "Success-based referral fee - 1-3% of deal value",
            "agreement_url": "https://impactquadrant.info/agreements/deal-origination",
            "terms": "No upfront cost. Client pays 1-3% fee upon successful deal closing.",
            "process": "1. Match with buyer → 2. Facilitate introduction → 3. Support negotiations → 4. Deal closes → 5. Invoice fee"
        },
        "ai_agency_monthly": {
            "name": "AI Agency Subscription Agreement",
            "description": "Monthly subscription - $997/month",
            "agreement_url": "https://buy.stripe.com/aFa14nfHp7MSa6a7Fo8g000",  # Stripe checkout
            "terms": "Monthly subscription, cancel anytime.",
            "process": "1. Sign up → 2. Monthly billing → 3. Service delivery"
        }
    }
    
    # Update config
    config_file = "/Users/cubiczan/.openclaw/workspace/stripe-config.json"
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    config["service_agreements"] = service_agreements
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created service agreement links:")
    for service, agreement in service_agreements.items():
        print(f"   {agreement['name']}:")
        print(f"     URL: {agreement['agreement_url']}")
        print(f"     Terms: {agreement['terms']}")
        print()
    
    return service_agreements

def generate_invoice_examples():
    """Generate example invoices for testing"""
    
    print()
    print("=" * 60)
    print("EXAMPLE INVOICES")
    print("=" * 60)
    print()
    
    examples = []
    
    # Example 1: Expense Reduction Invoice
    example1 = {
        "service": "expense_reduction",
        "company": "Example Manufacturing Co.",
        "savings_verified": 125000,  # $125,000 in savings
        "fee_percentage": 30,
        "invoice_amount": 37500,  # 30% of $125,000
        "description": "Expense Reduction Service - 30% of verified $125,000 annual savings",
        "terms": "Payable within 30 days of savings verification"
    }
    examples.append(example1)
    
    # Example 2: Deal Origination Invoice
    example2 = {
        "service": "deal_origination",
        "company": "Example Tech Startup",
        "deal_value": 5000000,  # $5M deal
        "fee_percentage": 2,
        "invoice_amount": 100000,  # 2% of $5M
        "description": "Deal Origination Referral Fee - 2% of $5,000,000 successful acquisition",
        "terms": "Payable upon deal closing"
    }
    examples.append(example2)
    
    # Save examples
    examples_file = "/Users/cubiczan/.openclaw/workspace/stripe-invoice-examples.json"
    with open(examples_file, 'w') as f:
        json.dump(examples, f, indent=2)
    
    print("✅ Created invoice examples:")
    for i, example in enumerate(examples, 1):
        print(f"   Example {i}: {example['service'].replace('_', ' ').title()}")
        print(f"     Company: {example['company']}")
        print(f"     Amount: ${example['invoice_amount']:,.2f}")
        print(f"     Description: {example['description']}")
        print()
    
    print(f"✅ Examples saved to: {examples_file}")
    
    return examples

def main():
    """Main setup function"""
    
    print("=" * 60)
    print("STRIPE INVOICE SYSTEM SETUP")
    print("=" * 60)
    print()
    
    # Create invoice templates
    config = create_invoice_templates()
    
    # Create service agreement links
    agreements = create_service_agreement_links()
    
    # Generate examples
    examples = generate_invoice_examples()
    
    print("=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)
    print()
    print("📋 What was created:")
    print()
    print("1. Invoice Items:")
    print("   • Expense Reduction (contingency-based)")
    print("   • Deal Origination (success-fee)")
    print()
    print("2. Invoice Templates:")
    print("   • Reusable templates for each service type")
    print("   • 30-day payment terms")
    print()
    print("3. Service Agreement Links:")
    print("   • Expense Reduction: https://impactquadrant.info/agreements/expense-reduction")
    print("   • Deal Origination: https://impactquadrant.info/agreements/deal-origination")
    print("   • AI Agency: https://buy.stripe.com/aFa14nfHp7MSa6a7Fo8g000")
    print()
    print("4. Example Invoices:")
    print("   • Expense Reduction: $37,500 (30% of $125K savings)")
    print("   • Deal Origination: $100,000 (2% of $5M deal)")
    print()
    print("📚 How to use:")
    print()
    print("For contingency/success-fee services:")
    print("1. Client signs service agreement")
    print("2. Service is delivered")
    print("3. Savings/deal value is verified")
    print("4. Create invoice with actual amount")
    print("5. Send invoice via Stripe")
    print("6. Client pays via Stripe")
    print()
    print("For subscription services:")
    print("1. Client signs up via Stripe checkout")
    print("2. Monthly billing automatically")
    print("3. Service delivered continuously")
    print()
    print("Configuration: /Users/cubiczan/.openclaw/workspace/stripe-config.json")
    print("Examples: /Users/cubiczan/.openclaw/workspace/stripe-invoice-examples.json")
    print()

if __name__ == "__main__":
    main()
