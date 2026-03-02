#!/usr/bin/env python3
"""
Stripe Payment System Configuration
Setup and initialize Stripe integration for AI agency services
"""

import os
import stripe
import json
from datetime import datetime

# Configuration
STRIPE_PUBLISHABLE_KEY = "pk_live_LtA4BnpnPUYfTrc0KTUupew5"
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")  # Get from environment
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# Initialize Stripe
stripe.api_key = STRIPE_SECRET_KEY
stripe.api_version = "2025-02-24.acacia"  # Latest stable version

class StripePaymentSystem:
    """Main Stripe payment system class"""
    
    def __init__(self):
        """Initialize Stripe payment system"""
        if not STRIPE_SECRET_KEY:
            print("⚠️ WARNING: STRIPE_SECRET_KEY not set in environment")
            print("   Get from: https://dashboard.stripe.com/apikeys")
            print("   Export: export STRIPE_SECRET_KEY='sk_live_...'")
        
        self.products = {}
        self.prices = {}
        
    def create_products(self):
        """Create standard products in Stripe"""
        
        products_to_create = [
            {
                "id": "expense_reduction_service",
                "name": "Expense Reduction Service",
                "description": "15-25% OPEX reduction with contingency-based pricing. We identify savings in telecommunications, waste management, utilities, and vendor contracts.",
                "metadata": {
                    "service_type": "expense_reduction",
                    "pricing_model": "contingency",
                    "fee_percentage": "30",
                    "min_savings": "50000"
                }
            },
            {
                "id": "deal_origination_referral",
                "name": "Deal Origination Referral Fee",
                "description": "Success-based referral fee for business acquisitions. We match sellers with qualified buyers and facilitate transactions.",
                "metadata": {
                    "service_type": "deal_origination",
                    "pricing_model": "success_fee",
                    "fee_percentage": "1-3",
                    "deal_size_min": "1000000"
                }
            },
            {
                "id": "ai_agency_monthly",
                "name": "AI Agency Monthly Subscription",
                "description": "Monthly AI-powered lead generation and outreach service. Includes 50-70 qualified leads per day with automated follow-up.",
                "metadata": {
                    "service_type": "ai_agency",
                    "pricing_model": "subscription",
                    "billing_period": "monthly",
                    "lead_volume": "50-70/day"
                }
            }
        ]
        
        created_products = []
        
        for product_data in products_to_create:
            try:
                # Check if product already exists
                existing_products = stripe.Product.list(limit=100)
                existing = None
                for prod in existing_products.data:
                    if prod.get("metadata", {}).get("service_type") == product_data["metadata"]["service_type"]:
                        existing = prod
                        break
                
                if existing:
                    print(f"✅ Product already exists: {product_data['name']} (ID: {existing.id})")
                    self.products[product_data["id"]] = existing
                else:
                    # Create new product
                    product = stripe.Product.create(
                        name=product_data["name"],
                        description=product_data["description"],
                        metadata=product_data["metadata"]
                    )
                    print(f"✅ Created product: {product.name} (ID: {product.id})")
                    self.products[product_data["id"]] = product
                    created_products.append(product)
                    
            except Exception as e:
                print(f"❌ Error creating product {product_data['name']}: {str(e)}")
        
        return created_products
    
    def create_prices(self):
        """Create prices for products"""
        
        prices_to_create = [
            {
                "product_id": "expense_reduction_service",
                "unit_amount": 0,  # $0 upfront - contingency based
                "currency": "usd",
                "recurring": None,  # One-time
                "nickname": "Contingency Fee (30% of savings)",
                "metadata": {
                    "fee_type": "contingency",
                    "percentage": "30",
                    "payment_trigger": "savings_verified"
                }
            },
            {
                "product_id": "deal_origination_referral", 
                "unit_amount": 0,  # $0 upfront - success fee
                "currency": "usd",
                "recurring": None,  # One-time
                "nickname": "Success Fee (1-3% of deal)",
                "metadata": {
                    "fee_type": "success_fee",
                    "percentage_range": "1-3",
                    "payment_trigger": "deal_closed"
                }
            },
            {
                "product_id": "ai_agency_monthly",
                "unit_amount": 99700,  # $997.00
                "currency": "usd",
                "recurring": {
                    "interval": "month",
                    "interval_count": 1
                },
                "nickname": "Monthly Subscription",
                "metadata": {
                    "fee_type": "subscription",
                    "amount": "997",
                    "billing_period": "monthly"
                }
            }
        ]
        
        created_prices = []
        
        for price_data in prices_to_create:
            try:
                # Get product
                product = self.products.get(price_data["product_id"])
                if not product:
                    print(f"❌ Product not found: {price_data['product_id']}")
                    continue
                
                # Check if price already exists
                existing_prices = stripe.Price.list(
                    product=product.id,
                    limit=10
                )
                
                existing = None
                for price in existing_prices.data:
                    if price.get("metadata", {}).get("fee_type") == price_data["metadata"]["fee_type"]:
                        existing = price
                        break
                
                if existing:
                    print(f"✅ Price already exists for {product.name}: {price_data['nickname']}")
                    self.prices[price_data["product_id"]] = existing
                else:
                    # Create price
                    price_params = {
                        "product": product.id,
                        "unit_amount": price_data["unit_amount"],
                        "currency": price_data["currency"],
                        "nickname": price_data["nickname"],
                        "metadata": price_data["metadata"]
                    }
                    
                    if price_data["recurring"]:
                        price_params["recurring"] = price_data["recurring"]
                    
                    price = stripe.Price.create(**price_params)
                    print(f"✅ Created price for {product.name}: {price.nickname} (${price.unit_amount/100:.2f})")
                    self.prices[price_data["product_id"]] = price
                    created_prices.append(price)
                    
            except Exception as e:
                print(f"❌ Error creating price for {price_data['product_id']}: {str(e)}")
        
        return created_prices
    
    def create_checkout_session(self, price_id, customer_email, success_url, cancel_url, metadata=None):
        """Create a Stripe Checkout session"""
        
        try:
            session_params = {
                "payment_method_types": ["card"],
                "line_items": [{
                    "price": price_id,
                    "quantity": 1,
                }],
                "mode": "payment" if "subscription" not in price_id else "subscription",
                "customer_email": customer_email,
                "success_url": success_url,
                "cancel_url": cancel_url,
                "allow_promotion_codes": True,
                "billing_address_collection": "required",
            }
            
            if metadata:
                session_params["metadata"] = metadata
            
            session = stripe.checkout.Session.create(**session_params)
            
            print(f"✅ Created checkout session for {customer_email}")
            print(f"   Session URL: {session.url}")
            print(f"   Session ID: {session.id}")
            
            return {
                "session_id": session.id,
                "url": session.url,
                "customer_email": customer_email,
                "amount_total": session.amount_total,
                "currency": session.currency
            }
            
        except Exception as e:
            print(f"❌ Error creating checkout session: {str(e)}")
            return None
    
    def create_invoice(self, customer_email, amount, description, metadata=None):
        """Create an invoice for a customer"""
        
        try:
            # First, get or create customer
            customers = stripe.Customer.list(email=customer_email, limit=1)
            if customers.data:
                customer = customers.data[0]
            else:
                customer = stripe.Customer.create(email=customer_email)
            
            # Create invoice item
            invoice_item = stripe.InvoiceItem.create(
                customer=customer.id,
                amount=amount,  # in cents
                currency="usd",
                description=description
            )
            
            # Create invoice
            invoice = stripe.Invoice.create(
                customer=customer.id,
                auto_advance=True,
                collection_method="send_invoice",
                days_until_due=30,
                metadata=metadata or {}
            )
            
            # Send invoice
            sent_invoice = stripe.Invoice.finalize_invoice(invoice.id)
            
            print(f"✅ Created invoice for {customer_email}: ${amount/100:.2f}")
            print(f"   Invoice ID: {sent_invoice.id}")
            print(f"   Invoice URL: {sent_invoice.hosted_invoice_url}")
            
            return {
                "invoice_id": sent_invoice.id,
                "invoice_url": sent_invoice.hosted_invoice_url,
                "customer_email": customer_email,
                "amount": amount,
                "status": sent_invoice.status
            }
            
        except Exception as e:
            print(f"❌ Error creating invoice: {str(e)}")
            return None
    
    def get_payment_links(self):
        """Generate payment links for different services"""
        
        payment_links = {}
        
        for product_id, product in self.products.items():
            price = self.prices.get(product_id)
            if price:
                # Create payment link
                try:
                    payment_link = stripe.PaymentLink.create(
                        line_items=[{
                            "price": price.id,
                            "quantity": 1
                        }],
                        after_completion={
                            "type": "redirect",
                            "redirect": {
                                "url": "https://impactquadrant.info/thank-you"
                            }
                        }
                    )
                    
                    payment_links[product_id] = {
                        "name": product.name,
                        "url": payment_link.url,
                        "price": f"${price.unit_amount/100:.2f}" if price.unit_amount > 0 else "Contingency-based"
                    }
                    
                    print(f"✅ Created payment link for {product.name}: {payment_link.url}")
                    
                except Exception as e:
                    print(f"❌ Error creating payment link for {product.name}: {str(e)}")
        
        return payment_links

def main():
    """Main setup function"""
    
    print("=" * 60)
    print("STRIPE PAYMENT SYSTEM SETUP")
    print("=" * 60)
    print()
    
    # Check for secret key
    if not STRIPE_SECRET_KEY:
        print("❌ STRIPE_SECRET_KEY not found in environment")
        print()
        print("To set up:")
        print("1. Get secret key from: https://dashboard.stripe.com/apikeys")
        print("2. Add to environment:")
        print("   export STRIPE_SECRET_KEY='sk_live_...'")
        print("   export STRIPE_WEBHOOK_SECRET='whsec_...'")
        print()
        print("For testing, use test keys:")
        print("   export STRIPE_SECRET_KEY='sk_test_...'")
        print("   export STRIPE_PUBLISHABLE_KEY='pk_test_...'")
        print()
        return
    
    # Initialize system
    payment_system = StripePaymentSystem()
    
    print("📦 Creating products...")
    products = payment_system.create_products()
    print(f"   Created/Found: {len(products)} products")
    
    print()
    print("💰 Creating prices...")
    prices = payment_system.create_prices()
    print(f"   Created/Found: {len(prices)} prices")
    
    print()
    print("🔗 Generating payment links...")
    payment_links = payment_system.get_payment_links()
    
    print()
    print("=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)
    
    if payment_links:
        print()
        print("📋 PAYMENT LINKS:")
        for service, link_info in payment_links.items():
            print(f"   {link_info['name']}:")
            print(f"     Price: {link_info['price']}")
            print(f"     URL: {link_info['url']}")
            print()
    
    # Save configuration
    config = {
        "stripe_publishable_key": STRIPE_PUBLISHABLE_KEY,
        "products": {pid: prod.id for pid, prod in payment_system.products.items()},
        "prices": {pid: price.id for pid, price in payment_system.prices.items()},
        "payment_links": payment_links,
        "setup_date": datetime.now().isoformat()
    }
    
    config_file = "/Users/cubiczan/.openclaw/workspace/stripe-config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration saved to: {config_file}")
    print()
    print("📚 Next steps:")
    print("1. Test payment links with test cards")
    print("2. Set up webhook endpoint for payment notifications")
    print("3. Integrate with AgentMail for automated payment links")
    print("4. Create invoice templates for contingency fees")
    print()

if __name__ == "__main__":
    main()
