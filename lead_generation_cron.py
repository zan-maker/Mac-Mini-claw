#!/usr/bin/env python3
"""
Automated Lead Generation Cron Jobs
Section 125 Wellness and Business Precision Sales
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yellowpages_integration import YellowPagesIntegration
from scrapedo_integration import ScrapeDoIntegration

class LeadGenerationCron:
    """Automated lead generation with cron scheduling"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or "/Users/cubiczan/.openclaw/workspace/leads"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize integrations
        self.yp = YellowPagesIntegration()
        self.scraper = ScrapeDoIntegration()
        
        # Configuration
        self.config = {
            "section_125": {
                "enabled": True,
                "locations": ["California", "New York", "Texas", "Florida", "Illinois"],
                "daily_limit": 50,
                "schedule": "9:00 AM"  # Daily at 9 AM
            },
            "business_precision": {
                "enabled": True,
                "industries": ["manufacturing", "construction", "healthcare", "retail", "professional"],
                "daily_limit": 50,
                "schedule": "10:00 AM"  # Daily at 10 AM
            },
            "scraping": {
                "enabled": True,
                "targets": ["linkedin", "crunchbase", "google"],
                "daily_limit": 20,
                "schedule": "11:00 AM"  # Daily at 11 AM
            }
        }
    
    def run_section_125_daily(self):
        """Daily Section 125 lead generation"""
        print("="*60)
        print("SECTION 125 WELLNESS PLAN LEAD GENERATION")
        print("="*60)
        
        if not self.config["section_125"]["enabled"]:
            print("❌ Section 125 lead generation is disabled")
            return None
        
        all_leads = []
        
        for location in self.config["section_125"]["locations"]:
            print(f"\n📍 Searching in {location}...")
            
            leads = self.yp.get_section_125_leads(
                location=location,
                limit=self.config["section_125"]["daily_limit"] // len(self.config["section_125"]["locations"])
            )
            
            if leads.get("success"):
                location_leads = leads.get("leads", [])
                print(f"  ✅ Found {len(location_leads)} leads")
                all_leads.extend(location_leads)
            
            # Respect rate limits
            import time
            time.sleep(2)
        
        # Save results
        if all_leads:
            result = self._save_leads(
                leads=all_leads,
                lead_type="section_125",
                description=f"Section 125 Wellness Plan Leads - {datetime.now().strftime('%Y-%m-%d')}"
            )
            
            print(f"\n🎯 Total Section 125 leads: {len(all_leads)}")
            print(f"📁 Saved to: {result.get('filepath', 'N/A')}")
            
            return result
        else:
            print("❌ No Section 125 leads found")
            return None
    
    def run_business_precision_daily(self):
        """Daily business precision lead generation"""
        print("="*60)
        print("BUSINESS PRECISION SALES LEAD GENERATION")
        print("="*60)
        
        if not self.config["business_precision"]["enabled"]:
            print("❌ Business precision lead generation is disabled")
            return None
        
        all_leads = []
        
        for industry in self.config["business_precision"]["industries"]:
            print(f"\n🏭 Searching {industry} industry...")
            
            leads = self.yp.get_business_precision_leads(
                industry=industry,
                limit=self.config["business_precision"]["daily_limit"] // len(self.config["business_precision"]["industries"])
            )
            
            if leads.get("success"):
                industry_leads = leads.get("leads", [])
                print(f"  ✅ Found {len(industry_leads)} leads")
                all_leads.extend(industry_leads)
            
            # Respect rate limits
            import time
            time.sleep(2)
        
        # Save results
        if all_leads:
            result = self._save_leads(
                leads=all_leads,
                lead_type="business_precision",
                description=f"Business Precision Sales Leads - {datetime.now().strftime('%Y-%m-%d')}"
            )
            
            print(f"\n🎯 Total business precision leads: {len(all_leads)}")
            print(f"📁 Saved to: {result.get('filepath', 'N/A')}")
            
            return result
        else:
            print("❌ No business precision leads found")
            return None
    
    def run_scraping_daily(self):
        """Daily web scraping for lead enrichment"""
        print("="*60)
        print("WEB SCRAPING FOR LEAD ENRICHMENT")
        print("="*60)
        
        if not self.config["scraping"]["enabled"]:
            print("❌ Web scraping is disabled")
            return None
        
        # Load existing leads to enrich
        existing_leads = self._load_existing_leads()
        
        if not existing_leads:
            print("⚠️  No existing leads to enrich")
            return None
        
        enriched_leads = []
        
        for i, lead in enumerate(existing_leads[:self.config["scraping"]["daily_limit"]]):
            print(f"\n🔍 Enriching lead {i+1}/{min(len(existing_leads), self.config['scraping']['daily_limit'])}: {lead.get('name', 'Unknown')}")
            
            enriched_lead = self._enrich_lead(lead)
            enriched_leads.append(enriched_lead)
            
            # Respect rate limits
            import time
            time.sleep(1)
        
        # Save enriched leads
        if enriched_leads:
            result = self._save_leads(
                leads=enriched_leads,
                lead_type="enriched",
                description=f"Enriched Leads - {datetime.now().strftime('%Y-%m-%d')}"
            )
            
            print(f"\n🎯 Total enriched leads: {len(enriched_leads)}")
            print(f"📁 Saved to: {result.get('filepath', 'N/A')}")
            
            return result
        else:
            print("❌ No leads enriched")
            return None
    
    def _enrich_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich a lead with web scraping data"""
        enriched = lead.copy()
        
        # Try to get website
        website = lead.get("website", "")
        
        if website:
            print(f"  🌐 Scraping website: {website}")
            
            # Scrape website
            scraped = self.scraper.extract_data(website)
            
            if scraped.get("success"):
                basic_info = scraped.get("basic_info", {})
                
                # Add scraped data
                enriched["scraped_title"] = basic_info.get("title", "")
                enriched["scraped_description"] = basic_info.get("description", "")
                enriched["scraped_keywords"] = basic_info.get("keywords", [])
                enriched["website_links_count"] = basic_info.get("links_count", 0)
                enriched["scraped_timestamp"] = datetime.now().isoformat()
                enriched["enrichment_score"] = self._calculate_enrichment_score(basic_info)
        
        # Try LinkedIn if no website but has company name
        elif lead.get("name"):
            company_name = lead["name"].split()[0]  # First word as company name
            print(f"  🔗 Trying LinkedIn: {company_name}")
            
            linkedin_data = self.scraper.scrape_linkedin_company(company_name)
            
            if linkedin_data.get("success"):
                enriched["linkedin_data"] = linkedin_data.get("basic_info", {})
        
        return enriched
    
    def _calculate_enrichment_score(self, scraped_data: Dict[str, Any]) -> float:
        """Calculate enrichment score"""
        score = 0.0
        
        if scraped_data.get("title"):
            score += 0.3
        
        if scraped_data.get("description"):
            score += 0.3
        
        if scraped_data.get("keywords"):
            score += 0.2
        
        if scraped_data.get("links_count", 0) > 0:
            score += 0.2
        
        return score
    
    def _save_leads(self, leads: List[Dict[str, Any]], lead_type: str, description: str) -> Dict[str, Any]:
        """Save leads to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON file
        json_filename = f"{lead_type}_leads_{timestamp}.json"
        json_filepath = os.path.join(self.output_dir, json_filename)
        
        # CSV file
        csv_filepath = self.yp.export_leads_to_csv(leads, f"{lead_type}_leads_{timestamp}.csv")
        
        # Save JSON
        data = {
            "description": description,
            "lead_type": lead_type,
            "timestamp": datetime.now().isoformat(),
            "total_leads": len(leads),
            "leads": leads
        }
        
        with open(json_filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Create summary
        summary = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "lead_type": lead_type,
            "total_leads": len(leads),
            "json_file": json_filepath,
            "csv_file": csv_filepath,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save summary
        summary_file = os.path.join(self.output_dir, f"summary_{timestamp}.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Update daily log
        self._update_daily_log(summary)
        
        return summary
    
    def _load_existing_leads(self) -> List[Dict[str, Any]]:
        """Load existing leads from today's files"""
        today = datetime.now().strftime("%Y%m%d")
        leads = []
        
        for filename in os.listdir(self.output_dir):
            if filename.endswith(".json") and today in filename and "summary" not in filename:
                filepath = os.path.join(self.output_dir, filename)
                
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    
                    if data.get("leads"):
                        leads.extend(data["leads"])
                
                except Exception as e:
                    print(f"⚠️  Error loading {filename}: {e}")
        
        return leads
    
    def _update_daily_log(self, summary: Dict[str, Any]):
        """Update daily activity log"""
        log_file = os.path.join(self.output_dir, "daily_log.json")
        
        # Load existing log
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                log = json.load(f)
        else:
            log = []
        
        # Add new entry
        log.append(summary)
        
        # Keep only last 30 days
        if len(log) > 30:
            log = log[-30:]
        
        # Save log
        with open(log_file, 'w') as f:
            json.dump(log, f, indent=2)
    
    def run_all_daily(self):
        """Run all daily lead generation tasks"""
        print("="*60)
        print("DAILY LEAD GENERATION - ALL TASKS")
        print("="*60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        results = []
        
        # 1. Section 125 leads
        print("1️⃣  SECTION 125 WELLNESS PLANS")
        section125_result = self.run_section_125_daily()
        if section125_result:
            results.append(section125_result)
        
        print("\n" + "-"*40)
        
        # 2. Business precision leads
        print("2️⃣  BUSINESS PRECISION SALES")
        precision_result = self.run_business_precision_daily()
        if precision_result:
            results.append(precision_result)
        
        print("\n" + "-"*40)
        
        # 3. Web scraping enrichment
        print("3️⃣  WEB SCRAPING ENRICHMENT")
        scraping_result = self.run_scraping_daily()
        if scraping_result:
            results.append(scraping_result)
        
        # Summary
        print("\n" + "="*60)
        print("DAILY SUMMARY")
        print("="*60)
        
        total_leads = sum(r.get("total_leads", 0) for r in results)
        
        print(f"📊 Total leads generated today: {total_leads}")
        print(f"📁 Files created: {len(results)}")
        
        for result in results:
            print(f"  • {result.get('lead_type', 'unknown')}: {result.get('total_leads', 0)} leads")
            print(f"    JSON: {os.path.basename(result.get('json_file', ''))}")
            if result.get('csv_file'):
                print(f"    CSV: {os.path.basename(result.get('csv_file', ''))}")
        
        # Save final report
        report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_leads": total_leads,
            "tasks_completed": len(results),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        report_file = os.path.join(self.output_dir, f"daily_report_{datetime.now().strftime('%Y%m%d')}.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📋 Full report: {report_file}")
        print("\n✅ Daily lead generation complete!")


# Create cron job setup script
def setup_cron_jobs():
    """Setup cron jobs for automated lead generation"""
    print("🔄 Setting up lead generation cron jobs...")
    
    # Get script path
    script_path = os.path.abspath(__file__)
    
    # Cron job entries
    cron_jobs = [
        # Section 125 leads - Daily at 9:00 AM
        f"0 9 * * * cd /Users/cubiczan/.openclaw/workspace && /usr/bin/python3 {script_path} --section125 >> /Users/cubiczan/.openclaw/logs/section125_$(date +\\%Y-\\%m-\\%d).log 2>&1",
        
        # Business precision leads - Daily at 10:00 AM
        f"0 10 * * * cd /Users/cubiczan/.openclaw/workspace && /usr/bin/python3 {script_path} --businessprecision >> /Users/cubiczan/.openclaw/logs/businessprecision_$(date +\\%Y-\\%m-\\%d).log 2>&1",
        
        # Web scraping enrichment - Daily at 11:00 AM
        f"0 11 * * * cd /Users/cubiczan/.openclaw/workspace && /usr/bin/python3 {script_path} --scraping >> /Users/cubiczan/.openclaw/logs/scraping_$(date +\\%Y-\\%m-\\%d).log 2>&1",
        
        # All tasks - Daily at 8:00 AM (comprehensive run)
        f"0 8 * * * cd /Users/cubiczan/.openclaw/workspace && /usr/bin/python3 {script_path} --all >> /Users/cubiczan/.openclaw/logs/leadgen_$(date +\\%Y-\\%m-\\%d).log 2>&1"
    ]
    
    print("\n📅 CRON JOBS TO ADD:")
    print("="*40)
    
    for job in cron_jobs:
        print(job)
    
    print("\n📋 To add these cron jobs:")
    print("1. Open crontab: crontab -e")
    print("2. Add the lines above")
    print("3. Save and exit")
    
    print("\n🔧 Or run this command to add automatically:")
    print("(crontab -l 2>/dev/null; echo)")
    for job in cron_jobs:
        print(f'echo "{job}"')
    print(") | crontab -")
    
    return cron_jobs


# Main execution
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated Lead Generation")
    parser.add_argument("--section125", action="store_true", help="Run Section 125 lead generation")
    parser.add_argument("--businessprecision", action="store_true", help="Run business precision lead generation")
    parser.add_argument("--scraping", action="store_true", help="Run web scraping enrichment")
    parser.add_argument("--all", action="store_true", help="Run all lead generation tasks")
    parser.add_argument("--setup", action="store_true", help="Setup cron jobs")
    
    args = parser.parse_args()
    
    # Initialize
    lead_gen = LeadGenerationCron()
    
    if args.setup:
        setup_cron_jobs()
    
    elif args.section125:
        lead_gen.run_section_125_daily()
    
    elif args.businessprecision:
        lead_gen.run_business_precision_daily()
    
    elif args.scraping:
        lead_gen.run_scraping_daily()
    
    elif args.all:
        lead_gen.run_all_daily()
    
    else:
        # Interactive mode
        print("🤖 Automated Lead Generation System")
        print("="*40)
        
        print("\nChoose an option:")
        print("1. Run Section 125 lead generation")
        print("2. Run business precision lead generation")
        print("3. Run web scraping enrichment")
        print("4. Run all tasks")
        print("5. Setup cron jobs")
        print("6. Test integrations")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            lead_gen.run_section_125_daily()
        elif choice == "2":
            lead_gen.run_business_precision_daily()
        elif choice == "3":
            lead_gen.run_scraping_daily()
        elif choice == "4":
            lead_gen.run_all_daily()
        elif choice == "5":
            setup_cron_jobs()
        elif choice == "6":
            print("\n🧪 Testing integrations...")
            
            # Test Yellow Pages
            from yellowpages_integration import test_yellowpages_integration
            test_yellowpages_integration()
            
            # Test Scrape.do
            from scrapedo_integration import test_scrapedo_integration
            test_scrapedo_integration()
            
            print("\n✅ Integration tests complete!")
        else:
            print("❌ Invalid choice")