#!/usr/bin/env python3
"""
AuraAssist Email Outreach System
Sends personalized outreach emails to qualified leads from outreach_queue/
"""

import os
import json
import sys
import time
import logging
from typing import List, Dict
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your existing Gmail SMTP module
try:
    from scripts.gmail_smtp_standard import GmailSender, STANDARD_SIGNATURE
    GMAIL_AVAILABLE = True
except ImportError:
    print("⚠️ Warning: Gmail SMTP module not found. Using mock mode.")
    GMAIL_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/cubiczan/.openclaw/workspace/logs/email_outreach.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AuraAssistEmailOutreach:
    """Email outreach system for AuraAssist leads"""
    
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        self.outreach_dir = "/Users/cubiczan/.openclaw/workspace/outreach_queue"
        self.sent_dir = "/Users/cubiczan/.openclaw/workspace/outreach_sent"
        
        # Create directories if they don't exist
        os.makedirs(self.sent_dir, exist_ok=True)
        
        # Initialize Gmail sender
        if GMAIL_AVAILABLE and not test_mode:
            self.gmail_sender = GmailSender(account_index=0, delay_seconds=3)
            logger.info("Gmail SMTP sender initialized")
        else:
            self.gmail_sender = None
            logger.info("Running in test mode (no emails will be sent)")
    
    def send_outreach_campaign(self, campaign_file: str = None, limit: int = None) -> Dict:
        """
        Send outreach campaign to leads
        
        Args:
            campaign_file: Specific campaign file to send (optional)
            limit: Maximum number of emails to send (optional)
            
        Returns:
            Campaign results
        """
        # Find campaign file
        if not campaign_file:
            campaign_file = self._find_latest_campaign()
        
        if not campaign_file or not os.path.exists(campaign_file):
            logger.error(f"No campaign file found: {campaign_file}")
            return {"error": "No campaign file found"}
        
        logger.info(f"Sending campaign from: {campaign_file}")
        
        # Load campaign data
        with open(campaign_file, 'r') as f:
            campaign_data = json.load(f)
        
        outreach_leads = campaign_data.get("outreach_leads", [])
        metadata = campaign_data.get("metadata", {})
        
        if not outreach_leads:
            logger.error("No outreach leads found in campaign")
            return {"error": "No outreach leads found"}
        
        # Filter leads with email addresses
        email_leads = [lead for lead in outreach_leads if lead.get("email")]
        
        if not email_leads:
            logger.error("No leads with email addresses found")
            return {"error": "No leads with email addresses"}
        
        # Apply limit if specified
        if limit:
            email_leads = email_leads[:limit]
        
        logger.info(f"Found {len(email_leads)} leads with email addresses")
        
        # Send emails
        results = self._send_emails(email_leads, campaign_file)
        
        # Save campaign results
        results_file = self._save_campaign_results(results, metadata, campaign_file)
        
        # Move campaign file to sent directory
        self._archive_campaign_file(campaign_file)
        
        return {
            "campaign_file": campaign_file,
            "results_file": results_file,
            "summary": self._generate_summary(results),
            "sent_emails": results.get("sent_emails", []),
            "failed_emails": results.get("failed_emails", [])
        }
    
    def _find_latest_campaign(self) -> str:
        """Find the latest outreach campaign file"""
        if not os.path.exists(self.outreach_dir):
            return None
        
        # List all JSON files
        json_files = []
        for file in os.listdir(self.outreach_dir):
            if file.endswith(".json") and file.startswith("outreach_"):
                json_files.append(file)
        
        if not json_files:
            return None
        
        # Sort by timestamp (newest first)
        json_files.sort(reverse=True)
        return os.path.join(self.outreach_dir, json_files[0])
    
    def _send_emails(self, leads: List[Dict], campaign_file: str) -> Dict:
        """Send emails to leads"""
        sent_emails = []
        failed_emails = []
        
        for i, lead in enumerate(leads):
            try:
                # Prepare email
                email_data = self._prepare_email(lead)
                
                # Send email (or simulate in test mode)
                if self.gmail_sender and not self.test_mode:
                    success = self._send_email_via_gmail(email_data)
                else:
                    success = True  # Simulate success in test mode
                
                # Record result
                if success:
                    lead["email_sent"] = True
                    lead["email_sent_at"] = datetime.now().isoformat()
                    lead["email_subject"] = email_data["subject"]
                    sent_emails.append(lead)
                    logger.info(f"✅ Email sent to {lead['email']} ({i+1}/{len(leads)})")
                else:
                    lead["email_sent"] = False
                    lead["email_error"] = "Failed to send"
                    failed_emails.append(lead)
                    logger.error(f"❌ Failed to send email to {lead['email']}")
                
                # Add delay between emails
                if i < len(leads) - 1:
                    time.sleep(3)  # 3-second delay to avoid rate limits
                
            except Exception as e:
                logger.error(f"Error sending email to {lead.get('email', 'unknown')}: {e}")
                lead["email_sent"] = False
                lead["email_error"] = str(e)
                failed_emails.append(lead)
        
        return {
            "sent_emails": sent_emails,
            "failed_emails": failed_emails,
            "total_sent": len(sent_emails),
            "total_failed": len(failed_emails)
        }
    
    def _prepare_email(self, lead: Dict) -> Dict:
        """Prepare email data for sending"""
        # Get outreach message from lead
        outreach_message = lead.get("outreach_message", {})
        if isinstance(outreach_message, str):
            # Handle case where outreach_message is a string
            subject = f"Reduce no-shows & fill last-minute cancellations"
            body = outreach_message
        else:
            subject = outreach_message.get("subject", "Reduce no-shows & fill last-minute cancellations")
            body = outreach_message.get("body", "")
        
        # Personalize message
        business_name = lead.get("business_name", "your business")
        industry = lead.get("industry", "salons_spas").replace("_", " ")
        
        # Replace placeholders
        body = body.replace("{business_name}", business_name)
        body = body.replace("{industry}", industry)
        
        # Add signature
        body += f"\n\n{STANDARD_SIGNATURE}"
        
        return {
            "to_email": lead["email"],
            "to_name": lead.get("contact_name", ""),
            "subject": subject,
            "body": body,
            "business_name": business_name,
            "industry": industry,
            "lead_score": lead.get("lead_score", 0)
        }
    
    def _send_email_via_gmail(self, email_data: Dict) -> bool:
        """Send email using Gmail SMTP"""
        try:
            # Use your existing GmailSender
            sender_name = "Agent Manager"
            to_email = email_data["to_email"]
            subject = email_data["subject"]
            body = email_data["body"]
            
            # Send email
            self.gmail_sender.send_email(
                to_email=to_email,
                subject=subject,
                body=body,
                sender_name=sender_name,
                cc_emails=["sam@impactquadrant.info"]
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Gmail SMTP error: {e}")
            return False
    
    def _save_campaign_results(self, results: Dict, metadata: Dict, campaign_file: str) -> str:
        """Save campaign results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"campaign_results_{timestamp}.json"
        filepath = os.path.join(self.sent_dir, filename)
        
        results_data = {
            "metadata": {
                **metadata,
                "campaign_file": os.path.basename(campaign_file),
                "sent_at": timestamp,
                "test_mode": self.test_mode
            },
            "results": results
        }
        
        with open(filepath, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        logger.info(f"Campaign results saved to {filepath}")
        return filepath
    
    def _archive_campaign_file(self, campaign_file: str):
        """Move campaign file to sent directory"""
        try:
            filename = os.path.basename(campaign_file)
            archive_path = os.path.join(self.sent_dir, "archived", filename)
            os.makedirs(os.path.dirname(archive_path), exist_ok=True)
            
            # Copy and then remove original
            import shutil
            shutil.copy2(campaign_file, archive_path)
            os.remove(campaign_file)
            
            logger.info(f"Campaign file archived to {archive_path}")
        except Exception as e:
            logger.error(f"Error archiving campaign file: {e}")
    
    def _generate_summary(self, results: Dict) -> Dict:
        """Generate campaign summary"""
        return {
            "timestamp": datetime.now().isoformat(),
            "total_leads": len(results.get("sent_emails", [])) + len(results.get("failed_emails", [])),
            "sent_successfully": len(results.get("sent_emails", [])),
            "failed": len(results.get("failed_emails", [])),
            "success_rate": f"{(len(results.get('sent_emails', [])) / max(1, len(results.get('sent_emails', [])) + len(results.get('failed_emails', []))) * 100):.1f}%",
            "test_mode": self.test_mode
        }

def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Send AuraAssist outreach emails')
    parser.add_argument('--campaign', help='Specific campaign file to send')
    parser.add_argument('--limit', type=int, help='Maximum number of emails to send')
    parser.add_argument('--test', action='store_true', help='Test mode (no emails sent)')
    parser.add_argument('--dry-run', action='store_true', help='Dry run (show what would be sent)')
    
    args = parser.parse_args()
    
    print("🚀 AURAASSIST EMAIL OUTREACH SYSTEM")
    print("="*60)
    
    # Initialize outreach system
    outreach = AuraAssistEmailOutreach(test_mode=args.test or args.dry_run)
    
    if args.dry_run:
        print("🔍 DRY RUN MODE: No emails will be sent")
        print("="*60)
    
    # Send campaign
    print("📧 Sending outreach campaign...")
    result = outreach.send_outreach_campaign(args.campaign, args.limit)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    summary = result["summary"]
    
    print("✅ CAMPAIGN COMPLETE!")
    print("="*60)
    print(f"📊 CAMPAIGN SUMMARY:")
    print(f"   Total Leads: {summary['total_leads']}")
    print(f"   Sent Successfully: {summary['sent_successfully']}")
    print(f"   Failed: {summary['failed']}")
    print(f"   Success Rate: {summary['success_rate']}")
    print(f"   Test Mode: {summary['test_mode']}")
    print()
    
    if result.get("sent_emails"):
        print("🎯 SENT EMAILS:")
        for i, email in enumerate(result["sent_emails"][:5], 1):
            print(f"{i}. {email.get('business_name', 'Unknown')}")
            print(f"   📧 {email.get('email', 'No email')}")
            print(f"   🎯 Score: {email.get('lead_score', 0)}/100")
            print(f"   📋 Industry: {email.get('industry', 'Unknown')}")
            print()
    
    if result.get("failed_emails"):
        print("⚠️ FAILED EMAILS:")
        for i, email in enumerate(result["failed_emails"][:3], 1):
            print(f"{i}. {email.get('business_name', 'Unknown')}")
            print(f"   📧 {email.get('email', 'No email')}")
            print(f"   ❌ Error: {email.get('email_error', 'Unknown error')}")
            print()
    
    print(f"📁 Results saved to: {result.get('results_file')}")
    print()
    print("🎯 NEXT STEPS:")
    print("1. Monitor email replies (check sam@cubiczan.com inbox)")
    print("2. Schedule demos with interested leads")
    print("3. Follow up in 2-3 days if no response")
    print("4. Track conversions in outreach_sent/ directory")
    print()
    print("🚀 READY FOR DEMOS AND CONVERSIONS!")

if __name__ == "__main__":
    main()