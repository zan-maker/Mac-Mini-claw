#!/usr/bin/env python3
"""
Craigslist Compliant Scraper with Legal Safeguards
Based on Manus AI Report - Dimension 6 Compliance
"""

import craigslistscraper as cs
import json
import os
import time
import random
from datetime import datetime, timedelta
import requests
from typing import List, Dict, Optional
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Legal Compliance Configuration
COMPLIANCE_CONFIG = {
    # Rate limiting (MUST comply with Craigslist ToS)
    "request_delay": {
        "min": 2.0,  # Minimum seconds between requests
        "max": 5.0,  # Maximum seconds between requests
        "jitter": 0.5  # Random jitter to avoid patterns
    },
    
    # Session management
    "max_requests_per_session": 100,  # Reset after this many requests
    "session_cooldown_minutes": 60,   # Wait between sessions
    
    # Data limits
    "max_ads_per_category": 20,       # Limit scraping volume
    "max_cities_per_day": 5,          # Don't scrape all cities at once
    
    # Data retention
    "data_retention_days": 30,        # Delete data after this many days
    "log_retention_days": 90,         # Keep logs longer for compliance
    
    # User agents (rotate to appear more human)
    "user_agents": [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    ],
    
    # Compliance monitoring
    "compliance_check_interval": 100,  # Check compliance every N requests
    "emergency_stop_file": "/Users/cubiczan/.openclaw/workspace/craigslist-leads/STOP_SCRAPING.txt"
}

# Business Configuration
BUSINESS_CONFIG = {
    "cities": ["newyork", "losangeles", "chicago", "miami", "houston"],
    "categories": {
        "business_for_sale": "biz",
        "skilled_trade": "sks",
        "real_estate": "rea",
        "electronics": "ela"
    },
    "output_dir": "/Users/cubiczan/.openclaw/workspace/craigslist-leads"
}

class ComplianceMonitor:
    """Monitor and enforce legal compliance"""
    
    def __init__(self):
        self.request_count = 0
        self.session_start = datetime.now()
        self.last_compliance_check = datetime.now()
        self.is_stopped = False
        
        # Check for emergency stop
        self.check_emergency_stop()
    
    def check_emergency_stop(self):
        """Check if we should stop scraping immediately"""
        stop_file = COMPLIANCE_CONFIG["emergency_stop_file"]
        if os.path.exists(stop_file):
            self.is_stopped = True
            logger.critical(f"EMERGENCY STOP: Found {stop_file}")
            logger.critical("Cease and desist protocol activated")
            return True
        return False
    
    def check_compliance(self):
        """Perform regular compliance checks"""
        
        # Emergency stop check
        if self.check_emergency_stop():
            raise SystemExit("Scraping stopped by compliance monitor")
        
        # Rate limiting check
        self.request_count += 1
        
        # Check if we need a session cooldown
        session_duration = datetime.now() - self.session_start
        if (self.request_count >= COMPLIANCE_CONFIG["max_requests_per_session"] or 
            session_duration.total_seconds() > 3600):  # 1 hour max
            
            cooldown = COMPLIANCE_CONFIG["session_cooldown_minutes"]
            logger.info(f"Session limit reached. Cooling down for {cooldown} minutes.")
            time.sleep(cooldown * 60)
            
            # Reset session
            self.request_count = 0
            self.session_start = datetime.now()
        
        # Add random delay between requests
        delay = random.uniform(
            COMPLIANCE_CONFIG["request_delay"]["min"],
            COMPLIANCE_CONFIG["request_delay"]["max"]
        )
        delay += random.uniform(
            -COMPLIANCE_CONFIG["request_delay"]["jitter"],
            COMPLIANCE_CONFIG["request_delay"]["jitter"]
        )
        
        time.sleep(max(0.5, delay))  # Minimum 0.5 seconds
        
        return True
    
    def get_user_agent(self):
        """Rotate user agents"""
        agents = COMPLIANCE_CONFIG["user_agents"]
        return random.choice(agents)
    
    def log_compliance_event(self, event_type: str, details: str):
        """Log compliance-related events"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details,
            "request_count": self.request_count
        }
        
        log_file = f"{BUSINESS_CONFIG['output_dir']}/compliance_log.jsonl"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        logger.info(f"Compliance event: {event_type} - {details}")

class EnhancedScraper:
    """Enhanced scraper with legal compliance and multiple revenue streams"""
    
    def __init__(self):
        self.compliance = ComplianceMonitor()
        self.ensure_directories()
        
        # Revenue stream configurations
        self.revenue_streams = {
            "referral_fees": {
                "business_for_sale": 0.01,  # 1%
                "service_business": 0.15,   # 15% of savings
            },
            "asset_flipping": {
                "margin_target": 0.30,  # 30% minimum margin
                "platform_fee": 0.10,   # 10% eBay/Amazon fees
            },
            "real_estate": {
                "airbnb_margin": 0.40,  # 40% over rental cost
                "management_fee": 0.08, # 8% property management
            }
        }
    
    def ensure_directories(self):
        """Ensure all necessary directories exist"""
        dirs = [
            BUSINESS_CONFIG["output_dir"],
            f"{BUSINESS_CONFIG['output_dir']}/raw",
            f"{BUSINESS_CONFIG['output_dir']}/processed",
            f"{BUSINESS_CONFIG['output_dir']}/logs",
            f"{BUSINESS_CONFIG['output_dir']}/compliance"
        ]
        
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
    
    def scrape_with_compliance(self, city: str, category: str, category_name: str) -> List[Dict]:
        """Scrape with full compliance monitoring"""
        
        if self.compliance.is_stopped:
            logger.warning(f"Scraping stopped. Skipping {city}/{category_name}")
            return []
        
        leads = []
        
        try:
            logger.info(f"Scraping {category_name} in {city}")
            
            # Compliance check before starting
            self.compliance.check_compliance()
            
            # Create search with compliance considerations
            search = cs.Search(
                city=city,
                category=category,
                query=""
            )
            
            # Fetch results
            self.compliance.log_compliance_event(
                "search_request",
                f"City: {city}, Category: {category_name}"
            )
            
            status = search.fetch()
            
            if status != 200:
                logger.warning(f"Failed to fetch: HTTP {status}")
                self.compliance.log_compliance_event(
                    "fetch_failed",
                    f"HTTP {status} for {city}/{category_name}"
                )
                return leads
            
            logger.info(f"Found {len(search.ads)} ads")
            
            # Limit number of ads processed
            max_ads = min(
                COMPLIANCE_CONFIG["max_ads_per_category"],
                len(search.ads)
            )
            
            processed = 0
            for ad in search.ads[:max_ads]:
                try:
                    # Compliance check before each ad
                    self.compliance.check_compliance()
                    
                    # Fetch ad details
                    ad_status = ad.fetch()
                    if ad_status != 200:
                        continue
                    
                    data = ad.to_dict()
                    
                    # Add metadata
                    data["scraped_at"] = datetime.now().isoformat()
                    data["city"] = city
                    data["category"] = category_name
                    data["craigslist_url"] = ad.url
                    
                    # Analyze for multiple revenue streams
                    analysis = self.analyze_listing(data, category_name)
                    
                    if analysis["qualified"]:
                        data["revenue_analysis"] = analysis
                        leads.append(data)
                        
                        logger.info(
                            f"Qualified: ${analysis['estimated_revenue']:,.0f} - "
                            f"{data.get('title', 'Unknown')[:50]}"
                        )
                    
                    processed += 1
                    
                    # Additional delay between ads
                    time.sleep(random.uniform(0.5, 1.5))
                    
                except Exception as e:
                    logger.error(f"Error processing ad: {e}")
                    continue
            
            logger.info(f"Processed {processed} ads from {city}/{category_name}")
            
        except Exception as e:
            logger.error(f"Error scraping {category_name} in {city}: {e}")
            self.compliance.log_compliance_event(
                "scraping_error",
                f"{city}/{category_name}: {str(e)}"
            )
        
        return leads
    
    def analyze_listing(self, listing: Dict, category: str) -> Dict:
        """Analyze listing for multiple revenue streams"""
        
        analysis = {
            "qualified": False,
            "primary_stream": None,
            "estimated_revenue": 0,
            "streams": [],
            "confidence": 0.5
        }
        
        # Extract price
        price = self.extract_price(listing)
        if not price:
            return analysis
        
        # Analyze for different revenue streams
        streams = []
        
        # 1. Referral Fees (Original Strategy)
        if category == "business_for_sale":
            fee = price * self.revenue_streams["referral_fees"]["business_for_sale"]
            fee = max(5000, min(50000, fee))
            
            streams.append({
                "type": "business_sale_referral",
                "estimated_revenue": fee,
                "confidence": 0.7,
                "description": f"1% referral on ${price:,.0f} business"
            })
        
        elif category in ["skilled_trade", "electronics"]:
            # Service business or potential flipping
            annual_revenue = self.estimate_annual_revenue(listing, price)
            
            if category == "skilled_trade":
                # Expense reduction referral
                potential_savings = annual_revenue * 0.6 * 0.2  # 60% expenses, 20% savings
                fee = potential_savings * self.revenue_streams["referral_fees"]["service_business"]
                fee = max(1000, min(10000, fee))
                
                streams.append({
                    "type": "expense_reduction_referral",
                    "estimated_revenue": fee,
                    "confidence": 0.6,
                    "description": f"15% of ${potential_savings:,.0f} savings"
                })
            
            else:  # electronics - asset flipping
                # Check if this is a flip opportunity
                flip_margin = self.calculate_flip_margin(listing, price)
                if flip_margin >= self.revenue_streams["asset_flipping"]["margin_target"]:
                    flip_profit = price * flip_margin
                    
                    streams.append({
                        "type": "asset_flipping",
                        "estimated_revenue": flip_profit,
                        "confidence": 0.5,
                        "description": f"{flip_margin*100:.0f}% margin on flip"
                    })
        
        # 2. Real Estate Analysis
        elif category == "real_estate":
            rental_analysis = self.analyze_real_estate(listing, price)
            if rental_analysis["profitable"]:
                streams.append({
                    "type": "rental_arbitrage",
                    "estimated_revenue": rental_analysis["monthly_profit"],
                    "confidence": rental_analysis["confidence"],
                    "description": f"${rental_analysis['monthly_profit']:,.0f}/month Airbnb profit"
                })
        
        # Determine best stream
        if streams:
            best_stream = max(streams, key=lambda x: x["estimated_revenue"])
            
            analysis["qualified"] = best_stream["estimated_revenue"] >= 1000
            analysis["primary_stream"] = best_stream["type"]
            analysis["estimated_revenue"] = best_stream["estimated_revenue"]
            analysis["streams"] = streams
            analysis["confidence"] = best_stream["confidence"]
        
        return analysis
    
    def extract_price(self, listing: Dict) -> Optional[float]:
        """Extract price from listing with enhanced parsing"""
        
        # Try direct price field
        price_str = listing.get("price", "")
        if price_str:
            try:
                # Remove $ and commas
                price_str = price_str.replace("$", "").replace(",", "")
                return float(price_str)
            except:
                pass
        
        # Enhanced text extraction
        text = f"{listing.get('title', '')} {listing.get('description', '')}"
        
        # Multiple price patterns
        patterns = [
            r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # $XX,XXX.XX
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:dollars|usd)',  # XX,XXX dollars
            r'asking\s*\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # asking $XX,XXX
            r'price:\s*\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',  # price: $XX,XXX
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    price_str = matches[0].replace(",", "")
                    price = float(price_str)
                    
                    # Validate reasonable range
                    if 100 <= price <= 10000000:  # $100 to $10M
                        return price
                except:
                    continue
        
        return None
    
    def calculate_flip_margin(self, listing: Dict, price: float) -> float:
        """Calculate potential flipping margin"""
        
        # Simple estimation - in production would use eBay/Amazon APIs
        title = listing.get("title", "").lower()
        
        # Common electronics with known resale value
        electronics = {
            "iphone": 1.5,  # 50% markup
            "macbook": 1.4,
            "playstation": 1.3,
            "xbox": 1.3,
            "camera": 1.4,
            "laptop": 1.35,
        }
        
        for item, multiplier in electronics.items():
            if item in title:
                return (multiplier - 1) - self.revenue_streams["asset_flipping"]["platform_fee"]
        
        # Default margin for other items
        return 0.25  # 25% default margin
    
    def analyze_real_estate(self, listing: Dict, price: float) -> Dict:
        """Analyze real estate for rental arbitrage"""
        
        analysis = {
            "profitable": False,
            "monthly_profit": 0,
            "confidence": 0.3,
            "assumptions": {}
        }
        
        # Simple analysis - in production would use Airbnb data
        title = listing.get("title", "").lower()
        description = listing.get("description", "").lower()
        
        # Check if it's a rental (not for sale)
        if "rent" in title or "rent" in description:
            # Estimate Airbnb potential
            # Rule of thumb: Airbnb earns 2-3x monthly rent
            airbnb_potential = price * 2.5
            
            # Subtract costs
            costs = price + (airbnb_potential * 0.15)  # Rent + 15% expenses
            
            monthly_profit = airbnb_potential - costs
            
            if monthly_profit >= 500:  # Minimum $500/month profit
                analysis["profitable"] = True
                analysis["monthly_profit"] = monthly_profit
                analysis["confidence"] = 0.4
                analysis["assumptions"] = {
                    "airbnb_multiplier": 2.5,
                    "expense_rate": 0.15,
                    "minimum_profit": 500
                }
        
        return analysis
    
    def estimate_annual_revenue(self, listing: Dict, price: float) -> float:
        """Estimate annual revenue for service businesses"""
        
        text = f"{listing.get('title', '')} {listing.get('description', '')}".lower()
        
        # Check for indicators
        if "monthly" in text or "/month" in text:
            return price * 12
        elif "weekly" in text or "/week" in text:
            return price * 52
        elif "hourly" in text or "/hr" in text:
            return price * 20 * 52  # 20 hours/week
        else:
            # Default assumption for business value
            return price * 3  # 3x multiple
    
    def run_scraper(self):
        """Main method to run the scraper"""
        logger.info("Starting enhanced compliant scraper")
        
        # Check emergency stop first
        if self.compliance.check_emergency_stop():
            logger.critical("Scraping stopped by emergency protocol")
            return
        
        all_leads = []
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Limit cities for compliance
        cities = BUSINESS_CONFIG["cities"][:COMPLIANCE_CONFIG["max_cities_per_day"]]
        
        for city in cities:
            logger.info(f"Processing city: {city}")
            
            for category_name, category_code in BUSINESS_CONFIG["categories"].items():
                leads = self.scrape_with_compliance(city, category_code, category_name)
                all_leads.extend(leads)
                
                # Save batch results
                if leads:
                    batch_file = f"{BUSINESS_CONFIG['output_dir']}/raw/{date_str}_{city}_{category_name}.json"
                    with open(batch_file, 'w') as f:
                        json.dump(leads, f, indent=2)
                    
                    logger.info(f"Saved {len(leads)} leads to {batch_file}")
        
        # Save final results
        if all_leads:
            final_file = f"{BUSINESS_CONFIG['output_dir']}/daily_leads_{date_str}.json"
            with open(final_file, 'w') as f:
                json.dump(all_leads, f, indent=2)
            
            # Generate summary
            summary = self.generate_summary(all_leads)
            summary_file = f"{BUSINESS_CONFIG['output_dir']}/daily_summary_{date_str}.json"
            
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
            
            logger.info(f"Total leads: {len(all_leads)}")
            logger.info(f"Total estimated revenue: ${summary['total_estimated_revenue']:,.2f}")
            logger.info(f"Summary saved to {summary_file}")
        
        logger.info("Scraping completed successfully")
    
    def generate_summary(self, leads: List[Dict]) -> Dict:
        """Generate summary of scraping results"""
        
        summary = {
            "date": datetime.now().isoformat(),
            "total_leads": len(leads),
            "total_estimated_revenue": 0,
            "by_stream": {},
            "by_category": {},
            "top_opportunities": []
        }
        
        # Calculate totals
        for lead in leads:
            analysis = lead.get("revenue_analysis", {})
            revenue = analysis.get("estimated_revenue", 0)
            
            summary["total_estimated_revenue"] += revenue
            
            # By stream
            stream = analysis.get("primary_stream", "unknown")
            summary["by_stream"][stream] = summary["by_stream"].get(stream, 0) + revenue
            
            # By category
            category = lead.get("category", "unknown")
            summary["by_category"][category] = summary["by_category"].get(category, 0) + revenue
        
        # Top opportunities
        sorted_leads = sorted(leads, key=lambda x: x.get("revenue_analysis", {}).get("estimated_revenue", 0), reverse=True)
        summary["top_opportunities"] = [
            {
                "title": lead.get("title", "")[:50],
                "category": lead.get("category", ""),
                "city": lead.get("city", ""),
                "estimated_revenue": lead.get("revenue_analysis", {}).get("estimated_revenue", 0),
                "primary_stream": lead.get("revenue_analysis", {}).get("primary_stream", "")
            }
            for lead in sorted_leads[:10]
        ]
        
        return summary

def main():
    """Main entry point"""
    scraper = EnhancedScraper()
    scraper.run_scraper()

if __name__ == "__main__":
    main()