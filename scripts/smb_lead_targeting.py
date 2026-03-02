#!/usr/bin/env python3
"""
SMB AI Receptionist Lead Targeting
Targets small businesses for ClawReceptionist product
"""

import os
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/cubiczan/.openclaw/workspace/logs/smb_leads.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SMBLeadTargeter:
    """Target small businesses for AI receptionist product"""
    
    def __init__(self):
        # Target industries from the document
        self.target_industries = {
            "home_services": {
                "keywords": ["HVAC", "plumbing", "electrician", "roofing", "pest control"],
                "subcategories": [
                    "Heating & Air Conditioning/HVAC",
                    "Plumber", 
                    "Electrician",
                    "Roofing Contractor",
                    "Pest Control Service"
                ],
                "pain_points": [
                    "after-hours emergency calls",
                    "missed appointment revenue",
                    "scheduling conflicts",
                    "customer no-shows"
                ],
                "avg_ticket": 300,  # Average job value
                "target_mrr": 1000   # Target monthly subscription
            },
            "salons_spas": {
                "keywords": ["hair salon", "nail salon", "barber shop", "spa", "aesthetics"],
                "subcategories": [
                    "Hair Salon",
                    "Nail Salon", 
                    "Barber Shop",
                    "Day Spa",
                    "Medical Spa",
                    "Beauty Salon"
                ],
                "pain_points": [
                    "no-shows costing revenue",
                    "DM/Instagram leads lost",
                    "phone calls after hours",
                    "waitlist management",
                    "rebooking automation"
                ],
                "avg_ticket": 80,    # Average service value
                "target_mrr": 599     # Convert plan
            },
            "medical_practices": {
                "keywords": ["dentist", "chiropractor", "physical therapy", "optometry", "clinic"],
                "subcategories": [
                    "Dentist",
                    "Chiropractor",
                    "Physical Therapist",
                    "Optometrist",
                    "Medical Clinic"
                ],
                "pain_points": [
                    "patient no-shows",
                    "insurance pre-check",
                    "appointment reminders",
                    "recall scheduling",
                    "intake forms"
                ],
                "avg_ticket": 150,   # Average appointment value
                "target_mrr": 800     # Target monthly subscription
            },
            "auto_repair": {
                "keywords": ["auto repair", "car detailing", "tire shop", "mechanic"],
                "subcategories": [
                    "Auto Repair Shop",
                    "Car Detailing Service",
                    "Tire Shop",
                    "Auto Body Shop"
                ],
                "pain_points": [
                    "estimate requests",
                    "appointment scheduling",
                    "status updates",
                    "review generation",
                    "follow-up for referrals"
                ],
                "avg_ticket": 200,   # Average service value
                "target_mrr": 600     # Target monthly subscription
            }
        }
        
        # Lead qualification criteria
        self.qualification_criteria = {
            "employee_count": {"min": 1, "max": 10},
            "revenue_range": {"min": 100000, "max": 2000000},
            "has_website": True,
            "has_phone": True,
            "review_count": {"min": 5},
            "booking_system": ["none", "paper", "basic", "google_calendar"]
        }
        
        # Outreach messaging templates
        self.outreach_templates = {
            "home_services": {
                "subject": "Stop missing emergency calls & reduce no-shows",
                "body": """Hi {business_owner},

I noticed {business_name} provides {service_type} services in {location}.

Quick question: Do you ever miss emergency calls after hours or have customers not show up for appointments?

Most {industry} businesses lose 15-30% of potential revenue to missed calls and no-shows.

We've built an AI receptionist specifically for service businesses that:
• Answers calls 24/7 and captures emergency leads
• Sends appointment reminders (reduces no-shows by 60%+)
• Books appointments automatically
• Qualifies leads with "what's your address + issue + photos"

It pays for itself with just 1-2 extra jobs per month.

Would 15 minutes next week make sense to show you how it works?

Best,
{your_name}
ClawReceptionist""",
                "value_prop": "Never miss an emergency call, reduce no-shows, automate scheduling"
            },
            "salons_spas": {
                "subject": "Reduce no-shows & fill last-minute cancellations automatically",
                "body": """Hi {business_owner},

I came across {business_name} and your great work with {mention_positive_review}.

I help salons/spas reduce no-shows and fill empty chairs automatically.

Most salons lose 20-30% of revenue to:
• No-shows and last-minute cancellations
• Missed calls/texts after hours  
• Lost leads in Instagram DMs
• Empty chairs from cancellations

Our AI receptionist for salons:
• Sends smart reminders (72h, 24h, 2h with confirm/reschedule options)
• Captures leads from calls, texts, and DMs 24/7
• Fills cancellations automatically from a waitlist
• Books appointments with staff approval (no double-booking)

It typically pays for itself by filling just 2-3 cancellation gaps per month.

Would you have 15 minutes next week to see how it works?

Best,
{your_name}
ClawReceptionist""",
                "value_prop": "Fewer no-shows, more filled chairs, less phone time"
            }
        }
        
        logger.info("SMB Lead Targeter initialized")
    
    def find_leads(self, industry: str, location: str = None, limit: int = 50) -> List[Dict]:
        """
        Find leads for specific industry
        
        Args:
            industry: Industry to target (home_services, salons_spas, etc.)
            location: Location filter (optional)
            limit: Maximum leads to return
            
        Returns:
            List of qualified leads
        """
        if industry not in self.target_industries:
            raise ValueError(f"Invalid industry: {industry}. Choose from: {list(self.target_industries.keys())}")
        
        industry_config = self.target_industries[industry]
        leads = []
        
        logger.info(f"Finding leads for {industry} in {location or 'any location'}")
        
        # This would integrate with your existing lead sources:
        # 1. Google Maps API
        # 2. Yelp API  
        # 3. Industry directories
        # 4. Social media scraping
        
        # For now, return mock data structure
        # TODO: Integrate with actual lead sources
        
        mock_leads = self._generate_mock_leads(industry, location, limit)
        
        # Qualify leads
        for lead in mock_leads:
            if self._qualify_lead(lead, industry_config):
                leads.append(lead)
        
        logger.info(f"Found {len(leads)} qualified leads for {industry}")
        return leads
    
    def _generate_mock_leads(self, industry: str, location: str, limit: int) -> List[Dict]:
        """Generate mock leads for testing"""
        industry_config = self.target_industries[industry]
        
        mock_data = {
            "home_services": [
                {
                    "business_name": "ABC Heating & Cooling",
                    "owner_name": "John Smith",
                    "phone": "(555) 123-4567",
                    "email": "john@abcheating.com",
                    "website": "https://abcheating.com",
                    "address": "123 Main St, Anytown, USA",
                    "services": ["HVAC", "Heating Repair", "AC Installation"],
                    "employee_count": 5,
                    "estimated_revenue": 750000,
                    "review_count": 42,
                    "avg_rating": 4.7,
                    "booking_system": "paper",
                    "pain_points": ["after-hours calls", "scheduling", "no-shows"]
                },
                {
                    "business_name": "Reliable Plumbing Co",
                    "owner_name": "Mike Johnson",
                    "phone": "(555) 987-6543",
                    "email": "mike@reliableplumbing.com",
                    "website": "https://reliableplumbing.com",
                    "address": "456 Oak Ave, Anytown, USA",
                    "services": ["Emergency Plumbing", "Pipe Repair", "Water Heater"],
                    "employee_count": 3,
                    "estimated_revenue": 450000,
                    "review_count": 28,
                    "avg_rating": 4.8,
                    "booking_system": "google_calendar",
                    "pain_points": ["missed calls", "appointment reminders"]
                }
            ],
            "salons_spas": [
                {
                    "business_name": "Bliss Hair Studio",
                    "owner_name": "Sarah Wilson",
                    "phone": "(555) 555-1212",
                    "email": "sarah@blisshairstudio.com",
                    "website": "https://blisshairstudio.com",
                    "address": "789 Beauty Blvd, Anytown, USA",
                    "services": ["Haircuts", "Color", "Styling"],
                    "employee_count": 4,
                    "estimated_revenue": 320000,
                    "review_count": 156,
                    "avg_rating": 4.9,
                    "booking_system": "instagram_dm",
                    "pain_points": ["no-shows", "DM management", "waitlist"]
                },
                {
                    "business_name": "Nailed It Salon",
                    "owner_name": "Lisa Chen",
                    "phone": "(555) 444-3333",
                    "email": "lisa@naileditsalon.com",
                    "website": "https://naileditsalon.com",
                    "address": "321 Nail St, Anytown, USA",
                    "services": ["Manicures", "Pedicures", "Nail Art"],
                    "employee_count": 6,
                    "estimated_revenue": 280000,
                    "review_count": 89,
                    "avg_rating": 4.6,
                    "booking_system": "phone_only",
                    "pain_points": ["cancellations", "phone calls", "rebooking"]
                }
            ]
        }
        
        return mock_data.get(industry, [])[:limit]
    
    def _qualify_lead(self, lead: Dict, industry_config: Dict) -> bool:
        """Qualify lead based on criteria"""
        try:
            # Check employee count
            if not (self.qualification_criteria["employee_count"]["min"] <= 
                    lead.get("employee_count", 0) <= 
                    self.qualification_criteria["employee_count"]["max"]):
                return False
            
            # Check revenue range
            if not (self.qualification_criteria["revenue_range"]["min"] <= 
                    lead.get("estimated_revenue", 0) <= 
                    self.qualification_criteria["revenue_range"]["max"]):
                return False
            
            # Check website
            if self.qualification_criteria["has_website"] and not lead.get("website"):
                return False
            
            # Check phone
            if self.qualification_criteria["has_phone"] and not lead.get("phone"):
                return False
            
            # Check reviews
            if lead.get("review_count", 0) < self.qualification_criteria["review_count"]["min"]:
                return False
            
            # Check booking system (prefer simpler systems)
            booking_system = lead.get("booking_system", "").lower()
            valid_systems = [bs.lower() for bs in self.qualification_criteria["booking_system"]]
            if booking_system not in valid_systems:
                return False
            
            # Check for pain points match
            lead_pain_points = [p.lower() for p in lead.get("pain_points", [])]
            industry_pain_points = [p.lower() for p in industry_config.get("pain_points", [])]
            
            # At least one pain point should match
            if not any(pain in lead_pain_points for pain in industry_pain_points):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error qualifying lead {lead.get('business_name')}: {e}")
            return False
    
    def prepare_outreach(self, lead: Dict, industry: str, your_name: str = "Sam") -> Dict:
        """
        Prepare outreach message for lead
        
        Args:
            lead: Lead information
            industry: Industry type
            your_name: Your name for signature
            
        Returns:
            Prepared outreach message
        """
        if industry not in self.outreach_templates:
            raise ValueError(f"No template for industry: {industry}")
        
        template = self.outreach_templates[industry]
        
        # Extract positive review if available
        mention_positive_review = ""
        if lead.get("review_count", 0) > 10 and lead.get("avg_rating", 0) >= 4.5:
            mention_positive_review = f"your {lead.get('review_count')} reviews with {lead.get('avg_rating')} stars"
        
        # Prepare variables
        variables = {
            "business_owner": lead.get("owner_name", "Business Owner"),
            "business_name": lead.get("business_name", ""),
            "service_type": lead.get("services", [""])[0] if lead.get("services") else "services",
            "location": lead.get("address", "").split(",")[-2].strip() if "," in lead.get("address", "") else "",
            "industry": industry.replace("_", " ").title(),
            "mention_positive_review": mention_positive_review,
            "your_name": your_name
        }
        
        # Format message
        subject = template["subject"]
        body = template["body"].format(**variables)
        
        return {
            "to_email": lead.get("email"),
            "to_name": lead.get("owner_name"),
            "subject": subject,
            "body": body,
            "value_prop": template["value_prop"],
            "lead_score": self._calculate_lead_score(lead, industry)
        }
    
    def _calculate_lead_score(self, lead: Dict, industry: str) -> int:
        """Calculate lead score (0-100)"""
        score = 50  # Base score
        
        # Employee count (1-10 is ideal)
        emp_count = lead.get("employee_count", 0)
        if 1 <= emp_count <= 5:
            score += 10
        elif 6 <= emp_count <= 10:
            score += 5
        
        # Revenue (ideal: $100K-$1M)
        revenue = lead.get("estimated_revenue", 0)
        if 100000 <= revenue <= 500000:
            score += 15
        elif 500001 <= revenue <= 1000000:
            score += 10
        elif revenue > 1000000:
            score += 5
        
        # Reviews (more is better)
        review_count = lead.get("review_count", 0)
        if review_count >= 50:
            score += 10
        elif review_count >= 20:
            score += 5
        
        # Rating (higher is better)
        rating = lead.get("avg_rating", 0)
        if rating >= 4.5:
            score += 10
        elif rating >= 4.0:
            score += 5
        
        # Booking system (simpler is better for our solution)
        booking_system = lead.get("booking_system", "").lower()
        if booking_system in ["none", "paper", "phone_only"]:
            score += 15  # High pain point
        elif booking_system in ["google_calendar", "basic"]:
            score += 10
        elif booking_system in ["instagram_dm", "facebook"]:
            score += 5
        
        # Pain points match
        industry_config = self.target_industries.get(industry, {})
        lead_pains = [p.lower() for p in lead.get("pain_points", [])]
        industry_pains = [p.lower() for p in industry_config.get("pain_points", [])]
        
        matching_pains = sum(1 for pain in lead_pains if any(ip in pain for ip in industry_pains))
        score += matching_pains * 5
        
        return min(100, score)
    
    def generate_roi_calculation(self, lead: Dict, industry: str, plan_mrr: int) -> Dict:
        """
        Generate ROI calculation for lead
        
        Args:
            lead: Lead information
            industry: Industry type
            plan_mrr: Monthly subscription price
            
        Returns:
            ROI calculation
        """
        industry_config = self.target_industries[industry]
        avg_ticket = industry_config["avg_ticket"]
        
        # Calculate break-even appointments
        break_even = plan_mrr / avg_ticket
        
        # Typical improvement metrics
        typical_improvements = {
            "no_show_reduction": 0.6,  # 60% reduction
            "lead_conversion_improvement": 0.2,  # 20% improvement
            "cancellation_fill_rate": 0.7,  # 70% of cancellations filled
        }
        
        # Estimate current metrics (simplified)
        estimated_monthly_appointments = 50  # Conservative estimate
        estimated_no_show_rate = 0.15  # 15% no-show rate
        estimated_cancellations = 10  # Monthly cancellations
        
        # Calculate potential savings
        no_show_savings = (estimated_monthly_appointments * estimated_no_show_rate * 
                          typical_improvements["no_show_reduction"] * avg_ticket)
        
        cancellation_fill_revenue = (estimated_cancellations