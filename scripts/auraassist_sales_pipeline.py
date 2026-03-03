#!/usr/bin/env python3
"""
ClawReceptionist Sales Pipeline
End-to-end pipeline: Lead → Demo → Checkout → Customer
"""

import os
import json
import sys
from datetime import datetime
from typing import Dict, List

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ClawReceptionistSalesPipeline:
    """Sales pipeline for ClawReceptionist"""
    
    def __init__(self):
        self.leads_dir = "/Users/cubiczan/.openclaw/workspace/outreach_queue"
        self.demos_dir = "/Users/cubiczan/.openclaw/workspace/demos_scheduled"
        self.customers_dir = "/Users/cubiczan/.openclaw/workspace/customers"
        
        # Create directories
        for directory in [self.demos_dir, self.customers_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Sales funnel stages
        self.funnel_stages = {
            "lead": "Qualified lead from scraping",
            "contacted": "Email sent to lead",
            "responded": "Lead replied to email",
            "demo_scheduled": "Demo scheduled with lead",
            "demo_completed": "Demo completed",
            "checkout_sent": "Checkout link sent",
            "customer": "Payment completed, customer onboarded",
            "churned": "Customer canceled"
        }
        
        # Demo to conversion rates (industry averages)
        self.conversion_rates = {
            "demo_to_checkout": 0.60,  # 60% of demos get checkout link
            "checkout_to_customer": 0.50,  # 50% of checkouts convert
            "overall_demo_to_customer": 0.30  # 30% overall conversion
        }
    
    def schedule_demo(self, lead_email: str, lead_name: str = None, 
                     business_name: str = None, scheduled_time: str = None) -> Dict:
        """
        Schedule a demo with a lead
        
        Args:
            lead_email: Lead email address
            lead_name: Lead name (optional)
            business_name: Business name (optional)
            scheduled_time: Scheduled demo time (optional)
            
        Returns:
            Demo scheduling result
        """
        # Generate demo ID
        demo_id = f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{lead_email.split('@')[0]}"
        
        # Default to tomorrow at 2 PM if not specified
        if not scheduled_time:
            scheduled_time = (datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
                            .replace(day=datetime.now().day + 1)
                            .isoformat())
        
        demo_data = {
            "demo_id": demo_id,
            "lead_email": lead_email,
            "lead_name": lead_name or "",
            "business_name": business_name or "",
            "scheduled_time": scheduled_time,
            "status": "scheduled",
            "created_at": datetime.now().isoformat(),
            "notes": "",
            "follow_up_actions": [
                "Send calendar invite",
                "Prepare demo script",
                "Test ClawReceptionist demo environment"
            ]
        }
        
        # Save demo
        demo_file = os.path.join(self.demos_dir, f"{demo_id}.json")
        with open(demo_file, 'w') as f:
            json.dump(demo_data, f, indent=2)
        
        print(f"✅ Demo scheduled: {demo_id}")
        print(f"   📧 Lead: {lead_email}")
        print(f"   ⏰ Time: {scheduled_time}")
        print(f"   📁 File: {demo_file}")
        
        return {
            "demo_id": demo_id,
            "demo_file": demo_file,
            "data": demo_data
        }
    
    def complete_demo(self, demo_id: str, outcome: str, notes: str = "") -> Dict:
        """
        Mark demo as completed
        
        Args:
            demo_id: Demo ID
            outcome: Demo outcome (interested, not_interested, follow_up)
            notes: Demo notes
            
        Returns:
            Demo completion result
        """
        demo_file = os.path.join(self.demos_dir, f"{demo_id}.json")
        
        if not os.path.exists(demo_file):
            return {"error": f"Demo not found: {demo_id}"}
        
        # Load demo
        with open(demo_file, 'r') as f:
            demo_data = json.load(f)
        
        # Update demo
        demo_data["status"] = "completed"
        demo_data["completed_at"] = datetime.now().isoformat()
        demo_data["outcome"] = outcome
        demo_data["notes"] = notes
        
        # Determine next steps
        if outcome == "interested":
            demo_data["next_step"] = "send_checkout"
            demo_data["follow_up_actions"] = [
                "Send checkout link",
                "Follow up in 24 hours",
                "Schedule onboarding call"
            ]
        elif outcome == "follow_up":
            demo_data["next_step"] = "follow_up"
            demo_data["follow_up_actions"] = [
                "Send follow-up email",
                "Schedule second demo",
                "Address concerns"
            ]
        else:
            demo_data["next_step"] = "closed"
            demo_data["follow_up_actions"] = ["Archive lead"]
        
        # Save updated demo
        with open(demo_file, 'w') as f:
            json.dump(demo_data, f, indent=2)
        
        print(f"✅ Demo completed: {demo_id}")
        print(f"   📊 Outcome: {outcome}")
        print(f"   🎯 Next step: {demo_data['next_step']}")
        
        return {
            "demo_id": demo_id,
            "outcome": outcome,
            "next_step": demo_data["next_step"],
            "data": demo_data
        }
    
    def send_checkout(self, demo_id: str, plan: str = "convert") -> Dict:
        """
        Send checkout link after successful demo
        
        Args:
            demo_id: Demo ID
            plan: Plan to offer (capture, convert, grow)
            
        Returns:
            Checkout sending result
        """
        demo_file = os.path.join(self.demos_dir, f"{demo_id}.json")
        
        if not os.path.exists(demo_file):
            return {"error": f"Demo not found: {demo_id}"}
        
        # Load demo
        with open(demo_file, 'r') as f:
            demo_data = json.load(f)
        
        if demo_data.get("outcome") != "interested":
            return {"error": "Demo outcome must be 'interested' to send checkout"}
        
        lead_email = demo_data["lead_email"]
        lead_name = demo_data.get("lead_name", "")
        business_name = demo_data.get("business_name", "")
        
        # Generate checkout link using Stripe
        try:
            from scripts.stripe_payment_system import StripePaymentSystem
            
            payment_system = StripePaymentSystem(test_mode=False)
            checkout_result = payment_system.create_checkout_session(
                customer_email=lead_email,
                plan_id=plan
            )
            
            if not checkout_result.get("success"):
                return {"error": f"Failed to create checkout: {checkout_result.get('error')}"}
            
            # Update demo with checkout info
            demo_data["checkout_sent"] = True
            demo_data["checkout_sent_at"] = datetime.now().isoformat()
            demo_data["checkout_session_id"] = checkout_result["session_id"]
            demo_data["checkout_url"] = checkout_result["url"]
            demo_data["plan_offered"] = plan
            demo_data["next_step"] = "awaiting_payment"
            
            with open(demo_file, 'w') as f:
                json.dump(demo_data, f, indent=2)
            
            print(f"✅ Checkout sent: {demo_id}")
            print(f"   📧 To: {lead_email}")
            print(f"   💰 Plan: {plan}")
            print(f"   🔗 URL: {checkout_result['url']}")
            
            return {
                "demo_id": demo_id,
                "checkout_session_id": checkout_result["session_id"],
                "checkout_url": checkout_result["url"],
                "plan": plan,
                "lead_email": lead_email
            }
            
        except ImportError:
            print("⚠️ Stripe payment system not available. Simulating checkout.")
            
            # Simulate checkout for testing
            checkout_url = f"https://checkout.stripe.com/simulated/{demo_id}"
            
            demo_data["checkout_sent"] = True
            demo_data["checkout_sent_at"] = datetime.now().isoformat()
            demo_data["checkout_session_id"] = f"cs_test_{demo_id}"
            demo_data["checkout_url"] = checkout_url
            demo_data["plan_offered"] = plan
            demo_data["next_step"] = "awaiting_payment"
            
            with open(demo_file, 'w') as f:
                json.dump(demo_data, f, indent=2)
            
            return {
                "demo_id": demo_id,
                "checkout_session_id": f"cs_test_{demo_id}",
                "checkout_url": checkout_url,
                "plan": plan,
                "lead_email": lead_email,
                "simulated": True
            }
    
    def onboard_customer(self, checkout_session_id: str) -> Dict:
        """
        Onboard customer after successful payment
        
        Args:
            checkout_session_id: Stripe checkout session ID
            
        Returns:
            Customer onboarding result
        """
        # In a real implementation, this would:
        # 1. Verify payment with Stripe webhook
        # 2. Create customer account
        # 3. Set up ClawReceptionist service
        # 4. Send welcome email
        # 5. Schedule onboarding call
        
        # For now, simulate onboarding
        customer_id = f"cust_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        customer_data = {
            "customer_id": customer_id,
            "checkout_session_id": checkout_session_id,
            "onboarded_at": datetime.now().isoformat(),
            "status": "active",
            "service_status": "provisioning",
            "next_actions": [
                "Send welcome email",
                "Schedule onboarding call",
                "Configure business settings",
                "Train AI receptionist"
            ]
        }
        
        # Save customer
        customer_file = os.path.join(self.customers_dir, f"{customer_id}.json")
        with open(customer_file, 'w') as f:
            json.dump(customer_data, f, indent=2)
        
        print(f"✅ Customer onboarded: {customer_id}")
        print(f"   📁 File: {customer_file}")
        print(f"   🚀 Status: {customer_data['status']}")
        
        return {
            "customer_id": customer_id,
            "customer_file": customer_file,
            "data": customer_data
        }
    
    def get_pipeline_metrics(self) -> Dict:
        """
        Get sales pipeline metrics
        
        Returns:
            Pipeline metrics
        """
        # Count leads in outreach queue
        lead_count = 0
        if os.path.exists(self.leads_dir):
            lead_count = len([f for f in os.listdir(self.leads_dir) 
                            if f.endswith('.json') and f.startswith('outreach_')])
        
        # Count scheduled demos
        demo_count = 0
        if os.path.exists(self.demos_dir):
            demo_count = len([f for f in os.listdir(self.demos_dir) 
                            if f.endswith('.json') and f.startswith('demo_')])
        
        # Count customers
        customer_count = 0
        if os.path.exists(self.customers_dir):
            customer_count = len([f for f in os.listdir(self.customers_dir) 
                                if f.endswith('.json') and f.startswith('cust_')])
        
        # Calculate conversion rates
        email_to_demo_rate = demo_count / max(lead_count, 1)
        demo_to_customer_rate = customer_count / max(demo_count, 1)
        overall_conversion_rate = customer_count / max(lead_count, 1)
        
        # Projected revenue
        projected_mrr = customer_count * 599  # Assuming $599 Convert plan
        
        return {
            "timestamp": datetime.now().isoformat(),
            "leads": lead_count,
            "demos_scheduled": demo_count,
            "customers": customer_count,
            "conversion_rates": {
                "email_to_demo": f"{email_to_demo_rate:.1%}",
                "demo_to_customer": f"{demo_to_customer_rate:.1%}",
                "overall": f"{overall_conversion_rate:.1%}"
            },
            "revenue": {
                "projected_mrr": f"${projected_mrr:.2f}",
                "projected_arr": f"${projected_mrr * 12:.2f}"
            },
            "pipeline_value": {
                "leads_value": f"${lead_count * 599 * self.conversion_rates['overall_demo_to_customer']:.2f}",
                "demos_value": f"${demo_count * 599 * self.conversion_rates['checkout_to_customer']:.2f}"
            }
        }

def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ClawReceptionist Sales Pipeline')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Schedule demo command
    demo_parser = subparsers.add_parser('demo', help='Schedule demo')
    demo_parser.add_argument('--email', required=True, help='Lead email')
    demo_parser.add_argument('--name', help='Lead name')
    demo_parser.add_argument('--business', help='Business name')
    demo_parser.add_argument('--time', help='Scheduled time (ISO format)')
    
    # Complete demo command
    complete_parser = subparsers.add_parser('complete', help='Complete demo')
    complete_parser.add_argument('--demo', required=True, help='Demo ID')
    complete_parser.add_argument('--outcome', required=True, 
                                choices=['interested', 'not_interested', 'follow_up'],
                                help='Demo outcome')
    complete_parser.add_argument('--notes', help='Demo notes')
    
    # Send checkout command
    checkout_parser = subparsers.add_parser('checkout', help='Send checkout')
    checkout_parser.add_argument('--demo', required=True, help='Demo ID')
    checkout_parser.add_argument('--plan', default='convert', 
                                choices=['capture', 'convert', 'grow'],
                                help='Plan to offer')
    
    # Onboard customer command
    onboard_parser = subparsers.add_parser('onboard', help='Onboard customer')
    onboard_parser.add_argument('--session', required=True, help='Checkout session ID')
    
    # Metrics command
    metrics_parser = subparsers.add_parser('metrics', help='Show pipeline metrics')
    
    args = parser.parse_args()
    
    print("🚀 CLAWRECEPTIONIST SALES PIPELINE")
    print("="*60)
    
    pipeline = ClawReceptionistSalesPipeline()
    
    if args.command == 'demo':
        print(f"📅 Scheduling demo for {args.email}")
        result = pipeline.schedule_demo(args.email, args.name, args.business, args.time)
        
    elif args.command == 'complete':
        print(f"✅ Completing demo: {args.demo}")
        result = pipeline.complete_demo(args.demo, args.outcome, args.notes)
        
    elif args.command == 'checkout':
        print(f"💰 Sending checkout for demo: {args.demo}")
        result = pipeline.send_checkout(args.demo, args.plan)
        if "checkout_url" in result:
            print(f"🔗 Checkout URL: {result['checkout_url']}")
        
    elif args.command == 'onboard':
        print(f"👤 Onboarding customer from session: {args.session}")
        result = pipeline.onboard_customer(args.session)
        
    elif args.command == 'metrics':
        print("📊 SALES PIPELINE METRICS")
        print("="*60)
        metrics = pipeline.get_pipeline_metrics()
        
        print(f"📈 Pipeline Status:")
        print(f"   • Leads: {metrics['leads']}")
        print(f"   • Demos Scheduled: {metrics['demos_scheduled']}")
        print(f"   • Customers: {metrics['customers']}")
        print()
        
        print(f"📊 Conversion Rates:")
        print(f"   • Email → Demo: {metrics['conversion_rates']['email_to_demo']}")
        print(f"   • Demo → Customer: {metrics['conversion_rates']['demo_to_customer']}")
        print(f"   • Overall: {metrics['conversion_rates']['overall']}")
        print()
        
        print(f"💰 Revenue:")
        print(f"   • Projected MRR: {metrics['revenue']['projected_mrr']}")
        print(f"   • Projected ARR: {metrics['revenue']['projected_arr']}")
        print()
        
        print(f"🎯 Pipeline Value:")
        print(f"   • Leads Value: {metrics['pipeline_value']['leads_value']}")
        print(f"   • Demos Value: {metrics['pipeline_value']['demos_value']}")
        
    else:
        print("Available commands:")
        print("  demo      - Schedule demo with lead")
        print("  complete  - Complete demo with outcome")
        print("  checkout  - Send checkout after demo")
        print("  onboard   - Onboard customer after payment")
        print("  metrics   - Show pipeline metrics")
        print()
        print("🎯 Sales Funnel:")
        for stage, description in pipeline.funnel_stages.items():
            print(f"  • {stage}: {description}")
        print()
        print("💰 Expected Conversion:")
        print(f"  • Demo → Checkout: {pipeline.conversion_rates['demo_to_checkout']:.0%}")
        print(f"  • Checkout → Customer: {pipeline.conversion_rates['checkout_to_customer']:.0%}")
        print(f"  • Overall Demo → Customer: {pipeline.conversion_rates['overall_demo_to_customer']:.0%}")

if __name__ == "__main__":
    main()