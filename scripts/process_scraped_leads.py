#!/usr/bin/env python3
"""
Process Scraped Leads for ClawReceptionist Outreach
Takes scraped leads, qualifies them, and prepares for outreach
"""

import os
import json
import pandas as pd
from typing import List, Dict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/cubiczan/.openclaw/workspace/logs/lead_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LeadProcessor:
    """Process scraped leads for ClawReceptionist outreach"""
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or "/Users/cubiczan/.openclaw/workspace/scraped_leads"
        self.output_dir = "/Users/cubiczan/.openclaw/workspace/outreach_queue"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Lead qualification criteria for ClawReceptionist
        self.qualification_criteria = {
            "min_lead_score": 70,
            "required_fields": ["business_name", "phone", "location"],
            "preferred_sources": ["craigslist", "yellow_pages"],
            "industry_priority": ["salons_spas", "home_services", "medical_practices"]
        }
        
        logger.info(f"Lead processor initialized. Data: {self.data_dir}")
    
    def process_latest_leads(self, industry: str = None, location: str = None) -> Dict:
        """
        Process latest scraped leads for outreach
        
        Args:
            industry: Specific industry to process (optional)
            location: Specific location to process (optional)
            
        Returns:
            Processing results
        """
        # Find latest combined leads file
        latest_file = self._find_latest_leads_file(industry, location)
        if not latest_file:
            logger.error("No scraped leads found")
            return {"error": "No scraped leads found"}
        
        logger.info(f"Processing leads from: {latest_file}")
        
        # Load leads
        with open(latest_file, 'r') as f:
            data = json.load(f)
        
        leads = data.get("leads", [])
        metadata = data.get("metadata", {})
        
        # Qualify leads
        qualified_leads = self._qualify_leads(leads)
        
        # Prepare outreach messages
        outreach_leads = self._prepare_outreach(qualified_leads)
        
        # Save to outreach queue
        output_file = self._save_to_outreach_queue(outreach_leads, metadata)
        
        # Generate summary
        summary = self._generate_summary(leads, qualified_leads, outreach_leads, metadata)
        
        logger.info(f"Processed {len(leads)} leads → {len(qualified_leads)} qualified → {len(outreach_leads)} for outreach")
        
        return {
            "input_file": latest_file,
            "output_file": output_file,
            "summary": summary,
            "outreach_leads_sample": outreach_leads[:5]
        }
    
    def _find_latest_leads_file(self, industry: str = None, location: str = None) -> str:
        """Find the latest scraped leads file"""
        combined_dir = os.path.join(self.data_dir, "combined")
        if not os.path.exists(combined_dir):
            return None
        
        # List all JSON files
        json_files = []
        for file in os.listdir(combined_dir):
            if file.endswith(".json"):
                json_files.append(file)
        
        if not json_files:
            return None
        
        # Sort by timestamp (newest first)
        json_files.sort(reverse=True)
        
        # Filter by industry/location if specified
        if industry or location:
            filtered_files = []
            for file in json_files:
                if industry and industry not in file:
                    continue
                if location and location.replace(" ", "_") not in file:
                    continue
                filtered_files.append(file)
            
            if filtered_files:
                return os.path.join(combined_dir, filtered_files[0])
        
        # Return latest file
        return os.path.join(combined_dir, json_files[0])
    
    def _qualify_leads(self, leads: List[Dict]) -> List[Dict]:
        """Qualify leads for ClawReceptionist"""
        qualified = []
        
        for lead in leads:
            try:
                # Calculate lead score
                score = self._calculate_lead_score(lead)
                lead["lead_score"] = score
                
                # Check minimum score
                if score < self.qualification_criteria["min_lead_score"]:
                    continue
                
                # Check required fields
                missing_fields = []
                for field in self.qualification_criteria["required_fields"]:
                    if not lead.get(field):
                        missing_fields.append(field)
                
                if missing_fields:
                    logger.debug(f"Lead {lead.get('business_name')} missing fields: {missing_fields}")
                    continue
                
                # Add to qualified leads
                qualified.append(lead)
                
            except Exception as e:
                logger.error(f"Error qualifying lead {lead.get('business_name')}: {e}")
                continue
        
        # Sort by score (descending)
        qualified.sort(key=lambda x: x.get("lead_score", 0), reverse=True)
        
        return qualified
    
    def _calculate_lead_score(self, lead: Dict) -> int:
        """Calculate lead score (0-100) for ClawReceptionist"""
        score = 50  # Base score
        
        # Source platform (Craigslist/Yellow Pages preferred)
        source = lead.get("sources", [""])[0] if lead.get("sources") else ""
        if source in self.qualification_criteria["preferred_sources"]:
            score += 15
        elif source:
            score += 5
        
        # Contact info completeness
        if lead.get("phone"):
            score += 10
        if lead.get("email"):
            score += 10
        if lead.get("website"):
            score += 10
        
        # Business signals
        if lead.get("description"):
            # Check for keywords indicating established business
            keywords = ["licensed", "insured", "professional", "established", "years"]
            desc = lead["description"].lower()
            for keyword in keywords:
                if keyword in desc:
                    score += 5
                    break
        
        # Industry match
        industry = lead.get("industry", "")
        if industry in self.qualification_criteria["industry_priority"]:
            score += 10
        
        return min(100, score)
    
    def _prepare_outreach(self, leads: List[Dict]) -> List[Dict]:
        """Prepare leads for ClawReceptionist outreach"""
        outreach_leads = []
        
        for lead in leads:
            try:
                # Determine outreach method
                outreach_method = self._determine_outreach_method(lead)
                
                # Prepare message template
                message = self._prepare_outreach_message(lead)
                
                # Create outreach record
                outreach_lead = {
                    "business_name": lead.get("business_name"),
                    "contact_name": lead.get("contact_name", ""),
                    "phone": lead.get("phone"),
                    "email": lead.get("email", ""),
                    "website": lead.get("website", ""),
                    "location": lead.get("location", ""),
                    "industry": lead.get("industry", ""),
                    "source": lead.get("sources", [""])[0],
                    "lead_score": lead.get("lead_score", 0),
                    "outreach_method": outreach_method,
                    "outreach_message": message,
                    "prepared_at": datetime.now().isoformat(),
                    "status": "pending",
                    "outreach_date": datetime.now().strftime("%Y-%m-%d")
                }
                
                outreach_leads.append(outreach_lead)
                
            except Exception as e:
                logger.error(f"Error preparing outreach for {lead.get('business_name')}: {e}")
                continue
        
        return outreach_leads
    
    def _determine_outreach_method(self, lead: Dict) -> str:
        """Determine best outreach method for lead"""
        if lead.get("email"):
            return "email"
        elif lead.get("phone"):
            return "sms"
        elif lead.get("website"):
            return "website_contact"
        else:
            return "unknown"
    
    def _prepare_outreach_message(self, lead: Dict) -> str:
        """Prepare personalized outreach message for ClawReceptionist"""
        business_name = lead.get("business_name", "your business")
        industry = lead.get("industry", "salons_spas").replace("_", " ")
        
        # Industry-specific messaging
        if industry == "salons spas":
            subject = "Reduce no-shows & fill last-minute cancellations"
            body = f"""Hi there,

I noticed {business_name} provides {industry.replace('s', '')} services.

Do you struggle with no-shows or last-minute cancellations?

Most {industry} lose 20-30% of revenue to:
• No-shows and cancellations
• Missed calls/texts after hours
• Lost leads in Instagram DMs
• Empty chairs from cancellations

Our AI receptionist for {industry}:
• Sends smart reminders (72h, 24h, 2h)
• Captures leads 24/7 from calls/texts/DMs
• Fills cancellations automatically from waitlist
• Books appointments with staff approval

It pays for itself by filling just 2-3 cancellation gaps per month.

Would you have 15 minutes next week to see how it works?

Best,
Sam
ClawReceptionist"""
        else:
            subject = "Stop missing calls & reduce no-shows"
            body = f"""Hi there,

I noticed {business_name} provides {industry} services.

Quick question: Do you ever miss calls after hours or have customers not show up?

Most {industry} businesses lose 15-30% of revenue to missed calls and no-shows.

We've built an AI receptionist that:
• Answers calls 24/7 and captures leads
• Sends appointment reminders (reduces no-shows by 60%+)
• Books appointments automatically
• Qualifies leads instantly

It pays for itself with just 1-2 extra appointments per month.

Would 15 minutes next week make sense to show you how it works?

Best,
Sam
ClawReceptionist"""
        
        return {
            "subject": subject,
            "body": body,
            "personalization_fields": {
                "business_name": business_name,
                "industry": industry
            }
        }
    
    def _save_to_outreach_queue(self, leads: List[Dict], metadata: Dict) -> str:
        """Save qualified leads to outreach queue"""
        if not leads:
            return None
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        industry = metadata.get("industry", "all")
        location = metadata.get("location", "all").replace(" ", "_")
        filename = f"outreach_{industry}_{location}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        # Save to JSON
        with open(filepath, 'w') as f:
            json.dump({
                "metadata": {
                    **metadata,
                    "processed_at": timestamp,
                    "total_outreach_leads": len(leads)
                },
                "outreach_leads": leads
            }, f, indent=2)
        
        logger.info(f"Saved {len(leads)} outreach leads to {filepath}")
        return filepath
    
    def _generate_summary(self, all_leads: List[Dict], qualified: List[Dict], 
                         outreach: List[Dict], metadata: Dict) -> Dict:
        """Generate processing summary"""
        return {
            "timestamp": datetime.now().isoformat(),
            "total_leads_scraped": len(all_leads),
            "total_leads_qualified": len(qualified),
            "total_leads_outreach": len(outreach),
            "qualification_rate": f"{(len(qualified)/len(all_leads)*100):.1f}%" if all_leads else "0%",
            "outreach_rate": f"{(len(outreach)/len(all_leads)*100):.1f}%" if all_leads else "0%",
            "industry": metadata.get("industry"),
            "location": metadata.get("location"),
            "platform_counts": metadata.get("platform_counts", {}),
            "lead_score_distribution": {
                "90+": len([l for l in qualified if l.get("lead_score", 0) >= 90]),
                "80-89": len([l for l in qualified if 80 <= l.get("lead_score", 0) < 90]),
                "70-79": len([l for l in qualified if 70 <= l.get("lead_score", 0) < 80]),
                "<70": len([l for l in qualified if l.get("lead_score", 0) < 70])
            },
            "outreach_methods": {
                "email": len([l for l in outreach if l.get("outreach_method") == "email"]),
                "sms": len([l for l in outreach if l.get("outreach_method") == "sms"]),
                "website": len([l for l in outreach if l.get("outreach_method") == "website_contact"]),
                "unknown": len([l for l in outreach if l.get("outreach_method") == "unknown"])
            }
        }

def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process scraped leads for ClawReceptionist outreach')
    parser.add_argument('--industry', help='Industry to process (salons_spas, home_services, etc.)')
    parser.add_argument('--location', help='Location to process')
    parser.add_argument('--auto', action='store_true', help='Automatically process latest leads')
    
    args = parser.parse_args()
    
    processor = LeadProcessor()
    
    if args.auto or not (args.industry or args.location):
        print("🔄 Processing latest scraped leads...")
        result = processor.process_latest_leads()
    else:
        print(f"🔄 Processing leads for {args.industry} in {args.location}...")
        result = processor.process_latest_leads(args.industry, args.location)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    summary = result["summary"]
    
    print("✅ LEAD PROCESSING COMPLETE!")
    print("="*60)
    print(f"📊 PROCESSING SUMMARY:")
    print(f"   Total Leads Scraped: {summary['total_leads_scraped']}")
    print(f"   Qualified Leads: {summary['total_leads_qualified']} ({summary['qualification_rate']})")
    print(f"   Outreach Ready: {summary['total_leads_outreach']} ({summary['outreach_rate']})")
    print(f"   Industry: {summary['industry']}")
    print(f"   Location: {summary['location']}")
    print()
    print(f"📈 LEAD SCORE DISTRIBUTION:")
    for score_range, count in summary['lead_score_distribution'].items():
        if count > 0:
            print(f"   • {score_range}: {count} leads")
    print()
    print(f"📱 OUTREACH METHODS:")
    for method, count in summary['outreach_methods'].items():
        if count > 0:
            print(f"   • {method}: {count} leads")
    print()
    print(f"📁 OUTPUT FILE: {result['output_file']}")
    print()
    print("🎯 SAMPLE OUTREACH LEADS:")
    for i, lead in enumerate(result['outreach_leads_sample'][:3], 1):
        print(f"{i}. {lead['business_name']}")
        print(f"   📞 {lead['phone']}")
        print(f"   📧 {lead['email'] or 'No email'}")
        print(f"   🎯 Score: {lead['lead_score']}/100")
        print(f"   📨 Method: {lead['outreach_method']}")
        print()

if __name__ == "__main__":
    main()