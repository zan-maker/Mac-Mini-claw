#!/usr/bin/env python3
"""
AuraAssist Payment System
Stripe integration for subscription billing
"""

import os
import json
import stripe
from datetime import datetime
from typing import Dict, Optional, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/cubiczan/.openclaw/workspace/logs/payments.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PaymentSystem:
    """Stripe payment processing for AuraAssist"""
    
    def __init__(self, stripe_secret_key: Optional[str] = None):
        """
        Initialize Stripe payment system
        
        Args:
            stripe_secret_key: Stripe secret key (defaults to env var)
        """
        self.stripe_key = stripe_secret_key or os.getenv("STRIPE_SECRET_KEY")
        if not self.stripe_key:
            raise ValueError("Stripe secret key required. Set STRIPE_SECRET_KEY environment variable.")
        
        stripe.api_key = self.stripe_key
        
        # Define pricing plans (create these in Stripe Dashboard first)
        self.plans = {
            "capture": {
                "monthly": "price_capture_monthly_299",
                "annual": "price_capture_annual_2990",  # ~2 months free
                "amount": 29900,  # cents
                "name": "Capture Plan"
            },
            "convert": {
                "monthly": "price_convert_monthly_599", 
                "annual": "price_convert_annual_5990",  # ~2 months free
                "amount": 59900,  # cents
                "name": "Convert Plan"
            },
            "grow": {
                "monthly": "price_grow_monthly_999",
                "annual": "price_grow_annual_9990",  # ~2 months free
                "amount": 99900,  # cents
                "name": "Grow Plan"
            }
        }
        
        logger.info("Payment system initialized")
    
    def create_customer(self, email: str, name: str, business_name: str, 
                       phone: Optional[str] = None, metadata: Optional[Dict] = None) -> str:
        """
        Create a new Stripe customer
        
        Args:
            email: Customer email
            name: Customer name
            business_name: Business name
            phone: Customer phone (optional)
            metadata: Additional metadata (optional)
            
        Returns:
            Stripe customer ID
        """
        try:
            customer_data = {
                "email": email,
                "name": name,
                "phone": phone,
                "metadata": {
                    "business_name": business_name,
                    "signup_date": datetime.now().isoformat(),
                    "source": "auraassist",
                    "lead_source": metadata.get("lead_source", "direct") if metadata else "direct"
                }
            }
            
            # Add any additional metadata
            if metadata:
                customer_data["metadata"].update(metadata)
            
            customer = stripe.Customer.create(**customer_data)
            logger.info(f"Created customer: {customer.id} for {business_name}")
            
            return customer.id
            
        except stripe.error.StripeError as e:
            logger.error(f"Error creating customer: {e}")
            raise
    
    def create_subscription(self, customer_id: str, plan_type: str = "convert", 
                          billing_cycle: str = "monthly", trial_days: int = 14) -> Dict:
        """
        Create subscription for customer
        
        Args:
            customer_id: Stripe customer ID
            plan_type: "capture", "convert", or "grow"
            billing_cycle: "monthly" or "annual"
            trial_days: Free trial days (default 14)
            
        Returns:
            Subscription object
        """
        try:
            # Get plan price ID
            if plan_type not in self.plans:
                raise ValueError(f"Invalid plan type: {plan_type}. Choose from: {list(self.plans.keys())}")
            
            if billing_cycle not in ["monthly", "annual"]:
                raise ValueError(f"Invalid billing cycle: {billing_cycle}. Choose 'monthly' or 'annual'")
            
            price_id = self.plans[plan_type][billing_cycle]
            
            # Create subscription
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
                trial_period_days=trial_days,
                payment_settings={
                    "payment_method_types": ["card"],
                    "save_default_payment_method": "on_subscription"
                },
                expand=["latest_invoice.payment_intent"],
                metadata={
                    "plan_type": plan_type,
                    "billing_cycle": billing_cycle,
                    "signup_date": datetime.now().isoformat()
                }
            )
            
            logger.info(f"Created subscription: {subscription.id} for customer {customer_id}")
            
            return {
                "subscription_id": subscription.id,
                "status": subscription.status,
                "current_period_start": subscription.current_period_start,
                "current_period_end": subscription.current_period_end,
                "trial_end": subscription.trial_end,
                "plan": plan_type,
                "billing_cycle": billing_cycle,
                "amount": self.plans[plan_type]["amount"],
                "client_secret": subscription.latest_invoice.payment_intent.client_secret if hasattr(subscription.latest_invoice.payment_intent, 'client_secret') else None
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Error creating subscription: {e}")
            raise
    
    def create_checkout_session(self, customer_id: str, plan_type: str = "convert",
                               billing_cycle: str = "monthly", success_url: str = None,
                               cancel_url: str = None) -> Dict:
        """
        Create Stripe Checkout session for payment
        
        Args:
            customer_id: Stripe customer ID
            plan_type: "capture", "convert", or "grow"
            billing_cycle: "monthly" or "annual"
            success_url: URL to redirect after success
            cancel_url: URL to redirect after cancel
            
        Returns:
            Checkout session object
        """
        try:
            price_id = self.plans[plan_type][billing_cycle]
            
            # Default URLs
            if not success_url:
                success_url = "https://auraassist.com/success?session_id={CHECKOUT_SESSION_ID}"
            if not cancel_url:
                cancel_url = "https://auraassist.com/cancel"
            
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                subscription_data={
                    'trial_period_days': 14,
                    'metadata': {
                        'plan_type': plan_type,
                        'billing_cycle': billing_cycle
                    }
                }
            )
            
            logger.info(f"Created checkout session: {session.id}")
            
            return {
                "session_id": session.id,
                "url": session.url,
                "expires_at": session.expires_at
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Error creating checkout session: {e}")
            raise
    
    def handle_webhook(self, payload: bytes, sig_header: str, webhook_secret: str) -> bool:
        """
        Process Stripe webhook events
        
        Args:
            payload: Raw webhook payload
            sig_header: Stripe signature header
            webhook_secret: Webhook secret from Stripe
            
        Returns:
            True if successful
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
            
            logger.info(f"Processing webhook: {event['type']}")
            
            # Handle different event types
            event_handlers = {
                'customer.subscription.created': self._on_subscription_created,
                'customer.subscription.updated': self._on_subscription_updated,
                'customer.subscription.deleted': self._on_subscription_deleted,
                'invoice.payment_succeeded': self._on_payment_succeeded,
                'invoice.payment_failed': self._on_payment_failed,
                'checkout.session.completed': self._on_checkout_completed,
            }
            
            handler = event_handlers.get(event['type'])
            if handler:
                handler(event['data']['object'])
            
            return True
            
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Webhook signature verification failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            raise
    
    def _on_subscription_created(self, subscription):
        """Handle new subscription"""
        logger.info(f"New subscription created: {subscription.id}")
        # TODO: Activate service, send welcome email, etc.
        
    def _on_subscription_updated(self, subscription):
        """Handle subscription update"""
        logger.info(f"Subscription updated: {subscription.id}")
        
    def _on_subscription_deleted(self, subscription):
        """Handle subscription cancellation"""
        logger.info(f"Subscription cancelled: {subscription.id}")
        # TODO: Deactivate service, send cancellation email, etc.
        
    def _on_payment_succeeded(self, invoice):
        """Handle successful payment"""
        logger.info(f"Payment succeeded for invoice: {invoice.id}")
        # TODO: Update billing status, send receipt
        
    def _on_payment_failed(self, invoice):
        """Handle failed payment"""
        logger.error(f"Payment failed for invoice: {invoice.id}")
        # TODO: Send payment failure notification, retry logic
        
    def _on_checkout_completed(self, session):
        """Handle checkout completion"""
        logger.info(f"Checkout completed: {session.id}")
        # TODO: Activate account, send onboarding instructions
    
    def get_subscription(self, subscription_id: str) -> Dict:
        """Get subscription details"""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return {
                "id": subscription.id,
                "status": subscription.status,
                "current_period_start": subscription.current_period_start,
                "current_period_end": subscription.current_period_end,
                "cancel_at_period_end": subscription.cancel_at_period_end,
                "plan": subscription.items.data[0].price.id if subscription.items.data else None,
                "amount": subscription.items.data[0].price.unit_amount if subscription.items.data else None
            }
        except stripe.error.StripeError as e:
            logger.error(f"Error getting subscription: {e}")
            raise
    
    def cancel_subscription(self, subscription_id: str, cancel_at_period_end: bool = True) -> Dict:
        """Cancel subscription"""
        try:
            if cancel_at_period_end:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
                logger.info(f"Subscription {subscription_id} scheduled for cancellation at period end")
            else:
                subscription = stripe.Subscription.delete(subscription_id)
                logger.info(f"Subscription {subscription_id} cancelled immediately")
            
            return {
                "id": subscription.id,
                "status": subscription.status,
                "cancel_at_period_end": subscription.cancel_at_period_end if hasattr(subscription, 'cancel_at_period_end') else True
            }
        except stripe.error.StripeError as e:
            logger.error(f"Error cancelling subscription: {e}")
            raise
    
    def update_subscription(self, subscription_id: str, new_plan_type: str, 
                           new_billing_cycle: str = None) -> Dict:
        """Update subscription plan"""
        try:
            # Get current subscription
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            # Get new price ID
            price_id = self.plans[new_plan_type][new_billing_cycle or "monthly"]
            
            # Update subscription
            updated = stripe.Subscription.modify(
                subscription_id,
                items=[{
                    "id": subscription.items.data[0].id,
                    "price": price_id
                }],
                proration_behavior="create_prorations"
            )
            
            logger.info(f"Updated subscription {subscription_id} to {new_plan_type}")
            
            return {
                "id": updated.id,
                "status": updated.status,
                "new_plan": new_plan_type,
                "proration_date": updated.proration_date if hasattr(updated, 'proration_date') else None
            }
        except stripe.error.StripeError as e:
            logger.error(f"Error updating subscription: {e}")
            raise
    
    def create_portal_session(self, customer_id: str, return_url: str = None) -> str:
        """Create customer portal session for self-service"""
        try:
            if not return_url:
                return_url = "https://auraassist.com/account"
            
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url
            )
            
            logger.info(f"Created portal session for customer {customer_id}")
            return session.url
        except stripe.error.StripeError as e:
            logger.error(f"Error creating portal session: {e}")
            raise
    
    def calculate_mrr(self) -> Dict:
        """Calculate Monthly Recurring Revenue"""
        try:
            # Get all active subscriptions
            subscriptions = stripe.Subscription.list(
                status="active",
                limit=100
            )
            
            mrr = 0
            plan_counts = {"capture": 0, "convert": 0, "grow": 0}
            
            for sub in subscriptions.auto_paging_iter():
                if sub.items.data:
                    amount = sub.items.data[0].price.unit_amount or 0
                    mrr += amount / 100  # Convert cents to dollars
                    
                    # Count by plan type (simplified - would need mapping from price ID to plan)
                    if amount == 29900:
                        plan_counts["capture"] += 1
                    elif amount == 59900:
                        plan_counts["convert"] += 1
                    elif amount == 99900:
                        plan_counts["grow"] += 1
            
            return {
                "mrr": mrr,
                "active_subscriptions": sum(plan_counts.values()),
                "plan_counts": plan_counts,
                "timestamp": datetime.now().isoformat()
            }
        except stripe.error.StripeError as e:
            logger.error(f"Error calculating MRR: {e}")
            raise

def main():
    """Command-line interface for payment system"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AuraAssist Payment System')
    parser.add_argument('--create-customer', action='store_true', help='Create new customer')
    parser.add_argument('--create-subscription', action='store_true', help='Create subscription')
    parser.add_argument('--create-checkout', action='store_true', help='Create checkout session')
    parser.add_argument('--get-mrr', action='store_true', help='Calculate MRR')
    parser.add_argument('--email', help='Customer email')
    parser.add_argument('--name', help='Customer name')
    parser.add_argument('--business', help='Business name')
    parser.add_argument('--plan', default='convert', help='Plan type (capture/convert/grow)')
    parser.add_argument('--billing', default='monthly', help='Billing cycle (monthly/annual)')
    
    args = parser.parse_args()
    
    # Initialize payment system
    stripe_key = os.getenv("STRIPE_SECRET_KEY")
    if not stripe_key:
        print("❌ STRIPE_SECRET_KEY environment variable not set")
        print("Get your key from: https://dashboard.stripe.com/apikeys")
        return
    
    payment = PaymentSystem(stripe_key)
    
    if args.create_customer:
        if not all([args.email, args.name, args.business]):
            print("❌ Missing required arguments: --email, --name, --business")
            return
        
        customer_id = payment.create_customer(
            email=args.email,
            name=args.name,
            business_name=args.business
        )
        print(f"✅ Customer created: {customer_id}")
        
    elif args.create_subscription:
        # This would typically follow customer creation
        print("Use --create-checkout for new subscriptions")
        
    elif args.create_checkout:
        if not all([args.email, args.name, args.business]):
            print("❌ Missing required arguments: --email, --name, --business")
            return
        
        # Create customer first
        customer_id = payment.create_customer(
            email=args.email,
            name=args.name,
            business_name=args.business
        )
        
        # Create checkout session
        session = payment.create_checkout_session(
            customer_id=customer_id,
            plan_type=args.plan,
            billing_cycle=args.billing
        )
        
        print(f"✅ Checkout session created")
        print(f"   Session ID: {session['session_id']}")
        print(f"   URL: {session['url']}")
        print(f"   Expires: {datetime.fromtimestamp(session['expires_at'])}")
        
    elif args.get_mrr:
        mrr_data = payment.calculate_mrr()
        print(f"📊 MRR Report:")
        print(f"   Monthly Recurring Revenue: ${mrr_data['mrr']:,.2f}")
        print(f"   Active Subscriptions: {mrr_data['active_subscriptions']}")
        print(f"   Plan Breakdown:")
        for plan, count in mrr_data['plan_counts'].items():
            if count > 0:
                print(f"     • {plan}: {count}")
        
    else:
        print("Please specify an action. Use --help for options.")

if __name__ == "__main__":
    main()