#!/usr/bin/env python3
"""
Stripe Payment System for AuraAssist
Handles subscriptions, payments, and customer management
"""

import os
import json
import stripe
from typing import Dict, List, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/cubiczan/.openclaw/workspace/logs/stripe_payments.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class StripePaymentSystem:
    """Stripe payment system for AuraAssist"""
    
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        
        # Load Stripe API keys from environment or config
        self.publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_live_LtA4BnpnPUYfTrc0KTUupew5')
        self.secret_key = os.getenv('STRIPE_SECRET_KEY', '')
        
        if not self.secret_key:
            logger.warning("Stripe secret key not configured. Running in test mode.")
            self.test_mode = True
        
        # Configure Stripe
        if not self.test_mode:
            stripe.api_key = self.secret_key
            logger.info("Stripe API configured (live mode)")
        else:
            # Use test keys if available
            test_secret_key = os.getenv('STRIPE_TEST_SECRET_KEY', '')
            if test_secret_key:
                stripe.api_key = test_secret_key
                logger.info("Stripe API configured (test mode)")
            else:
                logger.info("Running in simulation mode (no real Stripe calls)")
        
        # AuraAssist pricing plans
        self.plans = {
            "capture": {
                "name": "Capture Plan",
                "price": 29900,  # $299.00 in cents
                "interval": "month",
                "currency": "usd",
                "features": [
                    "24/7 AI Receptionist",
                    "Call & Text Capture",
                    "Basic Appointment Reminders",
                    "Email Support",
                    "Up to 50 appointments/month"
                ],
                "stripe_price_id": None  # Will be set when created
            },
            "convert": {
                "name": "Convert Plan",
                "price": 59900,  # $599.00 in cents
                "interval": "month",
                "currency": "usd",
                "features": [
                    "Everything in Capture Plan",
                    "Advanced Appointment Scheduling",
                    "Waitlist Management",
                    "Cancellation Fill Automation",
                    "Priority Support",
                    "Up to 200 appointments/month",
                    "Instagram DM Integration"
                ],
                "stripe_price_id": None
            },
            "grow": {
                "name": "Grow Plan",
                "price": 99900,  # $999.00 in cents
                "interval": "month",
                "currency": "usd",
                "features": [
                    "Everything in Convert Plan",
                    "Multi-location Support",
                    "Custom Workflow Automation",
                    "Dedicated Account Manager",
                    "API Access",
                    "Unlimited appointments",
                    "Advanced Analytics Dashboard"
                ],
                "stripe_price_id": None
            }
        }
        
        # Trial period (14 days)
        self.trial_period_days = 14
        
        logger.info(f"Payment system initialized. Test mode: {self.test_mode}")
    
    def setup_products_and_prices(self) -> Dict:
        """
        Create Stripe products and prices for AuraAssist
        
        Returns:
            Dictionary with created products and prices
        """
        if self.test_mode:
            logger.info("Test mode: Simulating product creation")
            return {"simulated": True, "message": "Running in test mode"}
        
        try:
            results = {}
            
            # Create main product
            product = stripe.Product.create(
                name="AuraAssist - AI Business Assistant",
                description="24/7 AI receptionist for salons, home services, and small businesses. Reduces no-shows, captures leads, and automates appointments.",
                metadata={
                    "product_type": "saas",
                    "target_audience": "smb",
                    "version": "1.0"
                }
            )
            
            results["product"] = product.id
            
            # Create prices for each plan
            for plan_id, plan_config in self.plans.items():
                price = stripe.Price.create(
                    product=product.id,
                    unit_amount=plan_config["price"],
                    currency=plan_config["currency"],
                    recurring={
                        "interval": plan_config["interval"]
                    },
                    metadata={
                        "plan_id": plan_id,
                        "plan_name": plan_config["name"]
                    }
                )
                
                # Store price ID
                self.plans[plan_id]["stripe_price_id"] = price.id
                results[plan_id] = {
                    "price_id": price.id,
                    "amount": plan_config["price"] / 100,
                    "currency": plan_config["currency"]
                }
            
            logger.info(f"Products and prices created: {results}")
            
            # Save configuration
            self._save_configuration()
            
            return {
                "success": True,
                "product_id": product.id,
                "prices": results,
                "plans": self.plans
            }
            
        except Exception as e:
            logger.error(f"Error creating products/prices: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_customer(self, email: str, name: str = None, 
                       metadata: Dict = None) -> Dict:
        """
        Create a Stripe customer
        
        Args:
            email: Customer email
            name: Customer name (optional)
            metadata: Additional metadata (optional)
            
        Returns:
            Customer information
        """
        if self.test_mode:
            logger.info(f"Test mode: Simulating customer creation for {email}")
            return {
                "simulated": True,
                "customer_id": f"cust_test_{email.replace('@', '_').replace('.', '_')}",
                "email": email,
                "name": name
            }
        
        try:
            customer_data = {
                "email": email,
                "metadata": metadata or {}
            }
            
            if name:
                customer_data["name"] = name
            
            customer = stripe.Customer.create(**customer_data)
            
            logger.info(f"Customer created: {customer.id}")
            
            return {
                "success": True,
                "customer_id": customer.id,
                "email": customer.email,
                "name": customer.name,
                "created": customer.created
            }
            
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_subscription(self, customer_id: str, plan_id: str, 
                           trial_days: int = None) -> Dict:
        """
        Create a subscription for a customer
        
        Args:
            customer_id: Stripe customer ID
            plan_id: Plan ID (capture, convert, grow)
            trial_days: Trial period in days (optional)
            
        Returns:
            Subscription information
        """
        if self.test_mode:
            logger.info(f"Test mode: Simulating subscription for {customer_id} to {plan_id}")
            return {
                "simulated": True,
                "subscription_id": f"sub_test_{customer_id}_{plan_id}",
                "customer_id": customer_id,
                "plan_id": plan_id,
                "status": "active",
                "trial_end": None
            }
        
        try:
            # Get price ID for the plan
            plan_config = self.plans.get(plan_id)
            if not plan_config:
                return {
                    "success": False,
                    "error": f"Unknown plan: {plan_id}"
                }
            
            price_id = plan_config.get("stripe_price_id")
            if not price_id:
                return {
                    "success": False,
                    "error": f"Price not configured for plan: {plan_id}"
                }
            
            # Create subscription
            subscription_data = {
                "customer": customer_id,
                "items": [{"price": price_id}],
                "payment_behavior": "default_incomplete",
                "expand": ["latest_invoice.payment_intent"]
            }
            
            # Add trial if specified
            if trial_days:
                subscription_data["trial_period_days"] = trial_days
            elif self.trial_period_days:
                subscription_data["trial_period_days"] = self.trial_period_days
            
            subscription = stripe.Subscription.create(**subscription_data)
            
            logger.info(f"Subscription created: {subscription.id}")
            
            return {
                "success": True,
                "subscription_id": subscription.id,
                "customer_id": customer_id,
                "plan_id": plan_id,
                "status": subscription.status,
                "current_period_start": subscription.current_period_start,
                "current_period_end": subscription.current_period_end,
                "trial_end": subscription.trial_end,
                "latest_invoice": subscription.latest_invoice.id if hasattr(subscription, 'latest_invoice') else None
            }
            
        except Exception as e:
            logger.error(f"Error creating subscription: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_checkout_session(self, customer_email: str, plan_id: str, 
                               success_url: str = None, cancel_url: str = None) -> Dict:
        """
        Create a Stripe Checkout session
        
        Args:
            customer_email: Customer email
            plan_id: Plan ID (capture, convert, grow)
            success_url: URL to redirect after success
            cancel_url: URL to redirect after cancel
            
        Returns:
            Checkout session information
        """
        if self.test_mode:
            logger.info(f"Test mode: Simulating checkout for {customer_email} to {plan_id}")
            return {
                "simulated": True,
                "session_id": f"cs_test_{customer_email.replace('@', '_').replace('.', '_')}",
                "url": "https://checkout.stripe.com/test/simulated",
                "customer_email": customer_email,
                "plan_id": plan_id
            }
        
        try:
            # Get price ID for the plan
            plan_config = self.plans.get(plan_id)
            if not plan_config:
                return {
                    "success": False,
                    "error": f"Unknown plan: {plan_id}"
                }
            
            price_id = plan_config.get("stripe_price_id")
            if not price_id:
                return {
                    "success": False,
                    "error": f"Price not configured for plan: {plan_id}"
                }
            
            # Default URLs
            if not success_url:
                success_url = "https://auraassist.com/success?session_id={CHECKOUT_SESSION_ID}"
            if not cancel_url:
                cancel_url = "https://auraassist.com/cancel"
            
            # Create checkout session
            session = stripe.checkout.Session.create(
                customer_email=customer_email,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                subscription_data={
                    'trial_period_days': self.trial_period_days
                } if self.trial_period_days else {},
                metadata={
                    'plan_id': plan_id,
                    'product': 'auraassist'
                }
            )
            
            logger.info(f"Checkout session created: {session.id}")
            
            return {
                "success": True,
                "session_id": session.id,
                "url": session.url,
                "customer_email": customer_email,
                "plan_id": plan_id,
                "amount": plan_config["price"] / 100,
                "currency": plan_config["currency"]
            }
            
        except Exception as e:
            logger.error(f"Error creating checkout session: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_subscription(self, subscription_id: str) -> Dict:
        """
        Get subscription details
        
        Args:
            subscription_id: Stripe subscription ID
            
        Returns:
            Subscription details
        """
        if self.test_mode:
            logger.info(f"Test mode: Simulating subscription retrieval for {subscription_id}")
            return {
                "simulated": True,
                "subscription_id": subscription_id,
                "status": "active",
                "plan_id": "convert",
                "current_period_end": 1941004800,  # Future date
                "cancel_at_period_end": False
            }
        
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            return {
                "success": True,
                "subscription_id": subscription.id,
                "status": subscription.status,
                "customer_id": subscription.customer,
                "current_period_start": subscription.current_period_start,
                "current_period_end": subscription.current_period_end,
                "cancel_at_period_end": subscription.cancel_at_period_end,
                "canceled_at": subscription.canceled_at,
                "items": [
                    {
                        "price_id": item.price.id,
                        "quantity": item.quantity
                    }
                    for item in subscription.items.data
                ]
            }
            
        except Exception as e:
            logger.error(f"Error retrieving subscription: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def cancel_subscription(self, subscription_id: str, 
                           at_period_end: bool = True) -> Dict:
        """
        Cancel a subscription
        
        Args:
            subscription_id: Stripe subscription ID
            at_period_end: Cancel at period end (default) or immediately
            
        Returns:
            Cancellation result
        """
        if self.test_mode:
            logger.info(f"Test mode: Simulating subscription cancellation for {subscription_id}")
            return {
                "simulated": True,
                "subscription_id": subscription_id,
                "canceled": True,
                "cancel_at_period_end": at_period_end
            }
        
        try:
            if at_period_end:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
            else:
                subscription = stripe.Subscription.delete(subscription_id)
            
            logger.info(f"Subscription canceled: {subscription_id}")
            
            return {
                "success": True,
                "subscription_id": subscription_id,
                "status": subscription.status,
                "cancel_at_period_end": subscription.cancel_at_period_end if hasattr(subscription, 'cancel_at_period_end') else False,
                "canceled_at": subscription.canceled_at if hasattr(subscription, 'canceled_at') else None
            }
            
        except Exception as e:
            logger.error(f"Error canceling subscription: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def calculate_mrr(self) -> Dict:
        """
        Calculate Monthly Recurring Revenue (MRR)
        
        Returns:
            MRR statistics
        """
        if self.test_mode:
            logger.info("Test mode: Simulating MRR calculation")
            return {
                "simulated": True,
                "total_mrr": 2990.00,  # $2,990
                "active_subscriptions": 10,
                "plan_distribution": {
                    "capture": {"count": 3, "mrr": 897.00},
                    "convert": {"count": 5, "mrr": 2995.00},
                    "grow": {"count": 2, "mrr": 1998.00}
                },
                "churn_rate": 0.05,  # 5%
                "arr": 35880.00  # Annual Run Rate
            }
        
        try:
            # Get all active subscriptions
            subscriptions = stripe.Subscription.list(
                status="active",
                limit=100
            )
            
            total_mrr = 0
            plan_counts = {"capture": 0, "convert": 0, "grow": 0}
            plan_mrr = {"capture": 0, "convert": 0, "grow": 0}
            
            for sub in subscriptions.data:
                for item in sub.items.data:
                    price_id = item.price.id
                    
                    # Determine which plan this is
                    plan_id = None
                    for pid, config in self.plans.items():
                        if config.get("stripe_price_id") == price_id:
                            plan_id = pid
                            break
                    
                    if plan_id:
                        plan_counts[plan_id] += 1
                        amount = item.price.unit_amount / 100  # Convert to dollars
                        plan_mrr[plan_id] += amount
                        total_mrr += amount
            
            # Calculate ARR (Annual Run Rate)
            arr = total_mrr * 12
            
            return {
                "success": True,
                "total_mrr": round(total_mrr, 2),
                "active_subscriptions": sum(plan_counts.values()),
                "plan_distribution": {
                    plan: {
                        "count": plan_counts[plan],
                        "mrr": round(plan_mrr[plan], 2)
                    }
                    for plan in plan_counts
                },
                "arr": round(arr, 2),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating MRR: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _save_configuration(self):
        """Save Stripe configuration to file"""
        config = {
            "publishable_key": self.publishable_key,
            "test_mode": self.test_mode,
            "plans": self.plans,
            "trial_period_days": self.trial_period_days,
            "configured_at": datetime.now().isoformat()
        }
        
        config_dir = "/Users/cubiczan/.openclaw/workspace/config"
        os.makedirs(config_dir, exist_ok=True)
        
        config_file = os.path.join(config_dir, "stripe_config.json")
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Configuration saved to {config_file}")

def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Stripe Payment System for AuraAssist')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Setup products and prices')
    
    # Create customer command
    customer_parser = subparsers.add_parser('customer', help='Create customer')
    customer_parser.add_argument('--email', required=True, help='Customer email')
    customer_parser.add_argument('--name', help='Customer name')
    
    # Create subscription command
    sub_parser = subparsers.add_parser('subscription', help='Create subscription')
    sub_parser.add_argument('--customer', required=True, help='Customer ID')
    sub_parser.add_argument('--plan', required=True, choices=['capture', 'convert', 'grow'], help='Plan ID')
    sub_parser.add_argument('--trial', type=int, help='Trial days')
    
    # Checkout command
    checkout_parser = subparsers.add_parser('checkout', help='Create checkout session')
    checkout_parser.add_argument('--email', required=True, help='Customer email')
    checkout_parser.add_argument('--plan', required=True, choices=['capture', 'convert', 'grow'], help='Plan ID')
    
    # MRR command
    mrr_parser = subparsers.add_parser('mrr', help='Calculate MRR')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test payment system')
    
    args = parser.parse_args()
    
    print("💰 AURAASSIST STRIPE PAYMENT SYSTEM")
    print("="*60)
    
    # Initialize payment system
    payment_system = StripePaymentSystem(test_mode=False)
    
    if args.command == 'setup':
        print("🔧 Setting up products and prices...")
        result = payment_system.setup_products_and_prices()
        print(f"✅ Setup complete: {result}")
        
    elif args.command == 'customer':
        print(f"👤 Creating customer: {args.email}")
        result = payment_system.create_customer(args.email, args.name)
        print(f"✅ Customer created: {result}")
        
    elif args.command == 'subscription':
        print(f"📅 Creating subscription: {args.customer} → {args.plan}")
        result = payment_system.create_subscription(args.customer, args.plan, args.trial)
        print(f"✅ Subscription created: {result}")
        
    elif args.command == 'checkout':
        print(f"🛒 Creating checkout: {args.email} → {args.plan}")
        result = payment_system.create_checkout_session(args.email, args.plan)
        if result.get('success'):
            print(f"✅ Checkout URL: {result['url']}")
            print(f"📋 Session ID: {result['session_id']}")
        else:
            print(f"❌ Error: {result.get('error')}")
            
    elif args.command == 'mrr':
        print("📊 Calculating MRR...")
        result = payment_system.calculate_mrr()
        if result.get('success') or result.get('simulated'):
            print(f"💰 Total MRR: ${result.get('total_mrr', 0):.2f}")
            print(f"📈 Active Subscriptions: {result.get('active_subscriptions', 0)}")
            print(f"📅 ARR: ${result.get('arr', 0):.2f}")
            print()
            print("📋 Plan Distribution:")
            for plan, data in result.get('plan_distribution', {}).items():
                print(f"  • {plan}: {data.get('count', 0)} customers, ${data.get('mrr', 0):.2f} MRR")
        else:
            print(f"❌ Error: {result.get('error')}")
            
    elif args.command == 'test':
        print("🧪 Testing payment system...")
        
        # Test customer creation
        print("1. Creating test customer...")
        customer_result = payment_system.create_customer("test@example.com", "Test Customer")
        print(f"   Result: {customer_result}")
        
        # Test checkout session
        print("2. Creating test checkout session...")
        checkout_result = payment_system.create_checkout_session("test@example.com", "convert")
        print(f"   Result: {checkout_result}")
        
        # Test MRR calculation
        print("3. Calculating test MRR...")
        mrr_result = payment_system.calculate_mrr()
        print(f"   Result: {mrr_result}")
        
        print("✅ Payment system test complete")
        
    else:
        print("Available commands:")
        print("  setup       - Setup products and prices")
        print("  customer    - Create customer")
        print("  subscription - Create subscription")
        print("  checkout    - Create checkout session")
        print("  mrr         - Calculate MRR")
        print("  test        - Test payment system")
        print()
        print("💰 Pricing Plans:")
        for plan_id, plan_config in payment_system.plans.items():
            print(f"  • {plan_config['name']}: ${plan_config['price']/100:.0f}/month")
            for feature in plan_config['features'][:3]:
                print(f"    - {feature}")

if __name__ == "__main__":
    main()