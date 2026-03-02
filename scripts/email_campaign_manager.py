#!/usr/bin/env python3
"""
Email Campaign Manager for ClawReceptionist
Manages end-to-end email campaigns: scheduling, sending, tracking, follow-ups
"""

import os
import json
import sys
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import schedule
import threading

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/cubiczan/.openclaw/workspace/logs/email_campaigns.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EmailCampaignManager:
    """Manages email campaigns for ClawReceptionist"""
    
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        self.campaigns_dir = "/Users/cubiczan/.openclaw/workspace/campaigns"
        self.templates_dir = "/Users/cubiczan/.openclaw/workspace/email_templates"
        self.results_dir = "/Users/cubiczan/.openclaw/workspace/campaign_results"
        
        # Create directories
        for directory in [self.campaigns_dir, self.templates_dir, self.results_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Campaign schedule
        self.schedule = {
            "monday": ["10:00", "14:00"],
            "tuesday": ["10:00", "14:00"],
            "wednesday": ["10:00", "14:00"],
            "thursday": ["10:00", "14:00"],
            "friday": ["10:00"],
            "saturday": [],
            "sunday": []
        }
        
        # Default campaign settings
        self.default_settings = {
            "daily_limit": 20,
            "delay_between_emails": 3,  # seconds
            "max_emails_per_campaign": 50,
            "follow_up_days": [3, 7, 14],
            "optimal_send_times": ["10:00-12:00", "14:00-16:00"],
            "avoid_times": ["18:00-08:00", "12:00-13:00"]  # Evenings and lunch
        }
        
        logger.info("Email Campaign Manager initialized")
    
    def create_campaign(self, name: str, industry: str, template: str = None, 
                       settings: Dict = None) -> Dict:
        """
        Create a new email campaign
        
        Args:
            name: Campaign name
            industry: Target industry
            template: Email template name (optional)
            settings: Campaign settings (optional)
            
        Returns:
            Campaign configuration
        """
        campaign_id = f"campaign_{name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        
        # Default settings
        campaign_settings = {
            **self.default_settings,
            "name": name,
            "industry": industry,
            "status": "draft",
            "created_at": datetime.now().isoformat(),
            "total_sent": 0,
            "total_replies": 0,
            "total_demos": 0,
            "total_conversions": 0
        }
        
        # Merge custom settings
        if settings:
            campaign_settings.update(settings)
        
        # Load template if specified
        if template:
            template_content = self._load_template(template)
            if template_content:
                campaign_settings["template"] = template_content
        
        # Save campaign
        campaign_file = os.path.join(self.campaigns_dir, f"{campaign_id}.json")
        with open(campaign_file, 'w') as f:
            json.dump(campaign_settings, f, indent=2)
        
        logger.info(f"Campaign created: {campaign_id}")
        
        return {
            "campaign_id": campaign_id,
            "campaign_file": campaign_file,
            "settings": campaign_settings
        }
    
    def schedule_campaign(self, campaign_id: str, send_time: str = None, 
                         day_of_week: str = None) -> bool:
        """
        Schedule a campaign for sending
        
        Args:
            campaign_id: Campaign ID
            send_time: Time to send (HH:MM)
            day_of_week: Day of week (optional)
            
        Returns:
            Success status
        """
        campaign_file = os.path.join(self.campaigns_dir, f"{campaign_id}.json")
        
        if not os.path.exists(campaign_file):
            logger.error(f"Campaign not found: {campaign_id}")
            return False
        
        # Load campaign
        with open(campaign_file, 'r') as f:
            campaign = json.load(f)
        
        # Update campaign status
        campaign["status"] = "scheduled"
        campaign["scheduled_for"] = send_time or "10:00"
        if day_of_week:
            campaign["scheduled_day"] = day_of_week
        
        # Save updated campaign
        with open(campaign_file, 'w') as f:
            json.dump(campaign, f, indent=2)
        
        # Schedule the campaign
        if send_time:
            # Parse time
            hour, minute = map(int, send_time.split(":"))
            
            # Schedule using schedule library
            if day_of_week:
                # Schedule for specific day
                getattr(schedule.every(), day_of_week.lower()).at(send_time).do(
                    self._execute_campaign, campaign_id
                )
            else:
                # Schedule for every day
                schedule.every().day.at(send_time).do(
                    self._execute_campaign, campaign_id
                )
            
            logger.info(f"Campaign {campaign_id} scheduled for {send_time} {day_of_week or 'daily'}")
        
        return True
    
    def _execute_campaign(self, campaign_id: str):
        """Execute a scheduled campaign"""
        logger.info(f"Executing campaign: {campaign_id}")
        
        # Load campaign
        campaign_file = os.path.join(self.campaigns_dir, f"{campaign_id}.json")
        with open(campaign_file, 'r') as f:
            campaign = json.load(f)
        
        # Update status
        campaign["status"] = "running"
        campaign["last_run"] = datetime.now().isoformat()
        
        # Get leads for this campaign
        leads = self._get_leads_for_campaign(campaign)
        
        if not leads:
            logger.warning(f"No leads found for campaign {campaign_id}")
            campaign["status"] = "completed"
            return
        
        # Send emails (using your existing outreach system)
        results = self._send_campaign_emails(campaign, leads)
        
        # Update campaign stats
        campaign["total_sent"] += results.get("sent", 0)
        campaign["status"] = "completed"
        campaign["last_results"] = results
        
        # Save updated campaign
        with open(campaign_file, 'w') as f:
            json.dump(campaign, f, indent=2)
        
        # Save results
        self._save_campaign_results(campaign_id, results)
        
        logger.info(f"Campaign {campaign_id} completed: {results.get('sent', 0)} emails sent")
    
    def _get_leads_for_campaign(self, campaign: Dict) -> List[Dict]:
        """Get leads for a campaign"""
        industry = campaign.get("industry", "")
        limit = campaign.get("daily_limit", self.default_settings["daily_limit"])
        
        # Look for leads in outreach_queue
        outreach_dir = "/Users/cubiczan/.openclaw/workspace/outreach_queue"
        if not os.path.exists(outreach_dir):
            return []
        
        # Find latest outreach file for this industry
        json_files = []
        for file in os.listdir(outreach_dir):
            if file.endswith(".json") and file.startswith("outreach_"):
                if industry in file:
                    json_files.append(file)
        
        if not json_files:
            return []
        
        # Get latest file
        latest_file = sorted(json_files)[-1]
        filepath = os.path.join(outreach_dir, latest_file)
        
        # Load leads
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        leads = data.get("outreach_leads", [])
        
        # Filter by industry and limit
        filtered_leads = [lead for lead in leads if lead.get("industry") == industry]
        return filtered_leads[:limit]
    
    def _send_campaign_emails(self, campaign: Dict, leads: List[Dict]) -> Dict:
        """Send campaign emails"""
        # This would integrate with your existing email sending system
        # For now, simulate sending
        
        sent = 0
        failed = 0
        
        for lead in leads:
            try:
                # Simulate email sending
                if not self.test_mode:
                    # TODO: Integrate with actual email sending
                    pass
                
                sent += 1
                time.sleep(campaign.get("delay_between_emails", 3))
                
            except Exception as e:
                logger.error(f"Error sending to {lead.get('email')}: {e}")
                failed += 1
        
        return {
            "sent": sent,
            "failed": failed,
            "total": len(leads),
            "success_rate": f"{(sent / max(1, len(leads)) * 100):.1f}%"
        }
    
    def _save_campaign_results(self, campaign_id: str, results: Dict):
        """Save campaign results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{campaign_id}_results_{timestamp}.json"
        filepath = os.path.join(self.results_dir, filename)
        
        results_data = {
            "campaign_id": campaign_id,
            "timestamp": timestamp,
            "results": results
        }
        
        with open(filepath, 'w') as f:
            json.dump(results_data, f, indent=2)
    
    def _load_template(self, template_name: str) -> Optional[Dict]:
        """Load email template"""
        template_file = os.path.join(self.templates_dir, f"{template_name}.json")
        
        if not os.path.exists(template_file):
            logger.warning(f"Template not found: {template_name}")
            return None
        
        with open(template_file, 'r') as f:
            return json.load(f)
    
    def create_template(self, name: str, subject: str, body: str, 
                       variables: List[str] = None) -> bool:
        """
        Create an email template
        
        Args:
            name: Template name
            subject: Email subject
            body: Email body
            variables: List of variables to replace
            
        Returns:
            Success status
        """
        template = {
            "name": name,
            "subject": subject,
            "body": body,
            "variables": variables or [],
            "created_at": datetime.now().isoformat(),
            "usage_count": 0
        }
        
        template_file = os.path.join(self.templates_dir, f"{name}.json")
        with open(template_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        logger.info(f"Template created: {name}")
        return True
    
    def get_campaign_stats(self) -> Dict:
        """Get overall campaign statistics"""
        campaigns = []
        total_sent = 0
        total_replies = 0
        total_demos = 0
        total_conversions = 0
        
        # Load all campaigns
        for file in os.listdir(self.campaigns_dir):
            if file.endswith(".json"):
                filepath = os.path.join(self.campaigns_dir, file)
                with open(filepath, 'r') as f:
                    campaign = json.load(f)
                    campaigns.append(campaign)
                    
                    total_sent += campaign.get("total_sent", 0)
                    total_replies += campaign.get("total_replies", 0)
                    total_demos += campaign.get("total_demos", 0)
                    total_conversions += campaign.get("total_conversions", 0)
        
        return {
            "total_campaigns": len(campaigns),
            "total_emails_sent": total_sent,
            "total_replies": total_replies,
            "total_demos_scheduled": total_demos,
            "total_conversions": total_conversions,
            "reply_rate": f"{(total_replies / max(1, total_sent) * 100):.1f}%",
            "demo_rate": f"{(total_demos / max(1, total_sent) * 100):.1f}%",
            "conversion_rate": f"{(total_conversions / max(1, total_sent) * 100):.1f}%",
            "active_campaigns": len([c for c in campaigns if c.get("status") in ["scheduled", "running"]]),
            "completed_campaigns": len([c for c in campaigns if c.get("status") == "completed"])
        }
    
    def run_scheduler(self):
        """Run the campaign scheduler"""
        logger.info("Starting campaign scheduler...")
        
        # Run scheduler in background thread
        def run_schedule():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        scheduler_thread = threading.Thread(target=run_schedule, daemon=True)
        scheduler_thread.start()
        
        logger.info("Campaign scheduler running in background")

def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage ClawReceptionist email campaigns')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Create campaign command
    create_parser = subparsers.add_parser('create', help='Create a new campaign')
    create_parser.add_argument('--name', required=True, help='Campaign name')
    create_parser.add_argument('--industry', required=True, help='Target industry')
    create_parser.add_argument('--template', help='Email template name')
    create_parser.add_argument('--limit', type=int, help='Daily email limit')
    
    # Schedule campaign command
    schedule_parser = subparsers.add_parser('schedule', help='Schedule a campaign')
    schedule_parser.add_argument('--campaign', required=True, help='Campaign ID')
    schedule_parser.add_argument('--time', help='Send time (HH:MM)')
    schedule_parser.add_argument('--day', help='Day of week')
    
    # Create template command
    template_parser = subparsers.add_parser('template', help='Create email template')
    template_parser.add_argument('--name', required=True, help='Template name')
    template_parser.add_argument('--subject', required=True, help='Email subject')
    template_parser.add_argument('--body', required=True, help='Email body')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show campaign statistics')
    
    # Start scheduler command
    scheduler_parser = subparsers.add_parser('scheduler', help='Start campaign scheduler')
    
    args = parser.parse_args()
    
    print("🚀 CLAWRECEPTIONIST EMAIL CAMPAIGN MANAGER")
    print("="*60)
    
    manager = EmailCampaignManager(test_mode=False)
    
    if args.command == 'create':
        print(f"📝 Creating campaign: {args.name}")
        settings = {}
        if args.limit:
            settings["daily_limit"] = args.limit
        
        result = manager.create_campaign(args.name, args.industry, args.template, settings)
        print(f"✅ Campaign created: {result['campaign_id']}")
        print(f"📁 File: {result['campaign_file']}")
        
    elif args.command == 'schedule':
        print(f"⏰ Scheduling campaign: {args.campaign}")
        success = manager.schedule_campaign(args.campaign, args.time, args.day)
        if success:
            print(f"✅ Campaign scheduled")
        else:
            print(f"❌ Failed to schedule campaign")
    
    elif args.command == 'template':
        print(f"📧 Creating template: {args.name}")
        success = manager.create_template(args.name, args.subject, args.body)
        if success:
            print(f"✅ Template created")
        else:
            print(f"❌ Failed to create template")
    
    elif args.command == 'stats':
        print("📊 CAMPAIGN STATISTICS")
        print("="*60)
        stats = manager.get_campaign_stats()
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    elif args.command == 'scheduler':
        print("⏰ STARTING CAMPAIGN SCHEDULER")
        print("="*60)
        manager.run_scheduler()
        print("✅ Scheduler running in background")
        print("Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Scheduler stopped")
    
    else:
        print("Available commands:")
        print("  create    - Create a new campaign")
        print("  schedule  - Schedule a campaign")
        print("  template  - Create email template")
        print("  stats     - Show campaign statistics")
        print("  scheduler - Start campaign scheduler")

if __name__ == "__main__":
    main()