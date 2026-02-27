#!/usr/bin/env python3
"""
Scrapling Integration for OpenClaw Cron Jobs

This module provides Scrapling-powered data extraction for all cron jobs.
Use this BEFORE falling back to Brave Search or Tavily APIs.
"""

import asyncio
import json
import re
import sys
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from scrapling_client import OpenClawScraplingClient, create_company_selectors
    from lead_scraper import LeadScraper
    SCRAPLING_AVAILABLE = True
except ImportError:
    SCRAPLING_AVAILABLE = False
    print("⚠️ Scrapling not available. Falling back to traditional APIs.")


class ScraplingCronIntegration:
    """
    Scrapling integration for OpenClaw cron jobs.
    
    Provides enhanced data extraction for:
    1. Lead generation
    2. Company research
    3. Market intelligence
    4. Contact discovery
    """
    
    def __init__(self, stealth_mode: bool = True, use_browser: bool = False):
        self.stealth_mode = stealth_mode
        self.use_browser = use_browser
        self.client = None
        self.lead_scraper = None
        
    async def initialize(self):
        """Initialize Scrapling clients."""
        if not SCRAPLING_AVAILABLE:
            return False
        
        try:
            self.client = OpenClawScraplingClient(
                use_browser=self.use_browser,
                stealth_mode=self.stealth_mode
            )
            self.client.initialize()
            
            self.lead_scraper = LeadScraper(stealth_mode=self.stealth_mode)
            
            print("✅ Scrapling cron integration initialized")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize Scrapling: {e}")
            return False
    
    async def scrape_company_data(self, url: str) -> Dict[str, Any]:
        """
        Scrape company data from website.
        
        Args:
            url: Company website URL
        
        Returns:
            Dictionary with company information
        """
        if not self.client:
            return {"error": "Scrapling not initialized", "success": False}
        
        try:
            # Use company selectors
            selectors = create_company_selectors()
            
            # Add additional selectors for cron jobs
            selectors.update({
                "technologies": ".tech-stack, .technologies, .tools",
                "funding": ".funding, .investment, .raised",
                "team": ".team-member, .employee, .staff",
                "testimonials": ".testimonial, .review, .quote",
                "blog_posts": ".post, .article, .blog-entry",
                "careers": ".careers, .jobs, .open-positions",
                "investors": ".investors, .backers, .partners"
            })
            
            result = await self.client.scrape_url(url, selectors)
            
            if not result.success:
                return {
                    "success": False,
                    "error": result.error,
                    "status_code": result.status_code
                }
            
            # Extract emails and phones
            emails = []
            phones = []
            
            if result.html:
                # Extract emails
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                email_matches = re.findall(email_pattern, result.html)
                emails = [email.lower() for email in email_matches 
                         if not any(placeholder in email.lower() 
                                   for placeholder in ["example.com", "test.com", "placeholder"])]
                
                # Extract phones
                phone_pattern = r'(\+?\d[\d\s\-\(\)]{7,}\d)'
                phone_matches = re.findall(phone_pattern, result.html)
                phones = phone_matches
            
            # Process company data
            company_data = {
                "url": url,
                "scraped_at": datetime.now().isoformat(),
                "status_code": result.status_code,
                "html_size": len(result.html) if result.html else 0,
                "extracted_data": result.data,
                "emails": list(set(emails))[:5],  # Unique emails, max 5
                "phones": list(set(phones))[:3],  # Unique phones, max 3
                "success": True
            }
            
            return company_data
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url
            }
    
    async def generate_expense_reduction_leads(self, search_queries: List[str], limit: int = 20) -> List[Dict[str, Any]]:
        """
        Generate expense reduction leads using Scrapling.
        
        Args:
            search_queries: List of search queries
            limit: Maximum number of leads to generate
        
        Returns:
            List of lead dictionaries
        """
        if not self.lead_scraper:
            return []
        
        leads = []
        
        try:
            # For each search query, find company URLs
            for query in search_queries:
                if len(leads) >= limit:
                    break
                
                print(f"🔍 Searching for: {query}")
                
                # In a real implementation, we would:
                # 1. Search for company directories
                # 2. Extract company URLs
                # 3. Scrape each company
                # For now, we'll simulate with example URLs
                
                # Example: Search for manufacturing companies
                if "manufacturing" in query.lower():
                    example_urls = [
                        "https://example-manufacturing.com",
                        "https://industrial-solutions.com",
                        "https://precision-parts.com"
                    ]
                elif "technology" in query.lower():
                    example_urls = [
                        "https://tech-solutions.com",
                        "https://software-company.com",
                        "https://saas-provider.com"
                    ]
                elif "healthcare" in query.lower():
                    example_urls = [
                        "https://medical-devices.com",
                        "https://healthcare-tech.com",
                        "https://pharma-company.com"
                    ]
                else:
                    example_urls = [
                        "https://example-company.com",
                        "https://business-solutions.com"
                    ]
                
                # Scrape each company
                for url in example_urls:
                    if len(leads) >= limit:
                        break
                    
                    lead_data = await self.scrape_company_data(url)
                    
                    if lead_data.get("success"):
                        # Enrich with expense reduction specific data
                        enriched_lead = self._enrich_expense_lead(lead_data)
                        leads.append(enriched_lead)
                        print(f"✅ Found lead: {enriched_lead.get('company_name', 'Unknown')}")
            
            return leads
            
        except Exception as e:
            print(f"❌ Error generating leads: {e}")
            return []
    
    def _enrich_expense_lead(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich company data for expense reduction leads."""
        # Estimate employee count based on website size
        html_size = company_data.get("html_size", 0)
        if html_size > 10000:
            estimated_employees = 200
        elif html_size > 5000:
            estimated_employees = 100
        elif html_size > 2000:
            estimated_employees = 50
        else:
            estimated_employees = 20
        
        # Estimate OPEX
        # Average OPEX per employee: $8K-$15K annually
        avg_opex_per_employee = 11500  # $11,500 average
        estimated_opex = estimated_employees * avg_opex_per_employee
        
        # Calculate potential savings (15-30% of OPEX)
        min_savings = estimated_opex * 0.15
        max_savings = estimated_opex * 0.30
        avg_savings = (min_savings + max_savings) / 2
        
        # Extract company name
        extracted_data = company_data.get("extracted_data", {})
        company_name = extracted_data.get("company_name", "")
        if not company_name:
            # Try to extract from URL
            from urllib.parse import urlparse
            parsed = urlparse(company_data.get("url", ""))
            domain = parsed.netloc.replace("www.", "")
            company_name = domain.split(".")[0].title()
        
        # Determine industry
        industry = self._classify_industry(extracted_data, company_data.get("url", ""))
        
        # Calculate lead score (0-100)
        lead_score = self._calculate_expense_lead_score(
            estimated_employees,
            industry,
            len(company_data.get("emails", [])),
            html_size
        )
        
        return {
            "company_name": company_name,
            "url": company_data.get("url"),
            "industry": industry,
            "estimated_employees": estimated_employees,
            "estimated_opex": f"${estimated_opex:,.0f}",
            "potential_savings_range": f"${min_savings:,.0f} - ${max_savings:,.0f}",
            "average_potential_savings": f"${avg_savings:,.0f}",
            "emails": company_data.get("emails", []),
            "phones": company_data.get("phones", []),
            "lead_score": lead_score,
            "priority": "High" if lead_score >= 70 else "Medium" if lead_score >= 50 else "Low",
            "scraped_at": company_data.get("scraped_at"),
            "source": "Scrapling"
        }
    
    def _classify_industry(self, extracted_data: Dict[str, Any], url: str) -> str:
        """Classify company industry."""
        industry_keywords = {
            "Technology": ["tech", "software", "saas", "platform", "api", "cloud", "ai", "machine learning"],
            "Manufacturing": ["manufacturing", "factory", "production", "industrial", "machinery"],
            "Healthcare": ["health", "medical", "hospital", "clinic", "pharma", "biotech"],
            "Professional Services": ["consulting", "services", "agency", "advisory", "solutions"],
            "Financial Services": ["finance", "bank", "investment", "insurance", "fintech"],
            "Retail/E-commerce": ["shop", "store", "marketplace", "retail", "ecommerce"],
            "Construction": ["construction", "building", "contractor", "engineering"],
            "Education": ["education", "learning", "school", "university", "training"]
        }
        
        # Combine all text for analysis
        all_text = url.lower()
        for key, value in extracted_data.items():
            if isinstance(value, str):
                all_text += " " + value.lower()
        
        # Find matching industry
        best_industry = "Other"
        best_score = 0
        
        for industry, keywords in industry_keywords.items():
            score = sum(1 for keyword in keywords if keyword in all_text)
            if score > best_score:
                best_score = score
                best_industry = industry
        
        return best_industry
    
    def _calculate_expense_lead_score(self, employees: int, industry: str, 
                                    email_count: int, html_size: int) -> int:
        """Calculate lead score for expense reduction (0-100)."""
        score = 0
        
        # Employee count (25 points)
        if employees >= 200:
            score += 25
        elif employees >= 100:
            score += 20
        elif employees >= 50:
            score += 15
        elif employees >= 20:
            score += 10
        elif employees >= 10:
            score += 5
        
        # Industry (25 points)
        high_opex_industries = ["Technology", "Healthcare", "Financial Services", "Manufacturing"]
        if industry in high_opex_industries:
            score += 25
        elif industry in ["Professional Services", "Construction"]:
            score += 15
        elif industry != "Other":
            score += 10
        
        # Contact information (25 points)
        if email_count >= 3:
            score += 25
        elif email_count >= 2:
            score += 20
        elif email_count >= 1:
            score += 15
        
        # Website quality (25 points)
        if html_size > 10000:
            score += 25
        elif html_size > 5000:
            score += 20
        elif html_size > 2000:
            score += 15
        elif html_size > 1000:
            score += 10
        else:
            score += 5
        
        return min(score, 100)
    
    async def scrape_defense_companies(self, search_terms: List[str]) -> List[Dict[str, Any]]:
        """
        Scrape defense companies for defense sector lead gen.
        
        Args:
            search_terms: List of defense-related search terms
        
        Returns:
            List of defense company data
        """
        if not self.client:
            return []
        
        companies = []
        
        try:
            # Defense company selectors
            defense_selectors = {
                "company_name": "h1, .company-name, .brand, [itemprop='name']",
                "description": ".description, .about, .company-description",
                "sector": ".sector, .industry, .focus-area, .expertise",
                "technologies": ".technologies, .tech-stack, .capabilities",
                "clients": ".clients, .partners, .customers",
                "contracts": ".contracts, .projects, .engagements",
                "team": ".team, .leadership, .executives",
                "location": ".location, .address, .headquarters"
            }
            
            # For each search term, find and scrape companies
            for term in search_terms:
                print(f"🔍 Searching defense companies: {term}")
                
                # In real implementation, search for company URLs
                # For now, use example defense company URLs
                example_defense_urls = [
                    "https://example-defense-tech.com",
                    "https://cybersecurity-solutions.com",
                    "https://drone-technology.com",
                    "https://space-defense.com",
                    "https://military-ai.com"
                ]
                
                for url in example_defense_urls:
                    result = await self.client.scrape_url(url, defense_selectors)
                    
                    if result.success:
                        company_data = {
                            "url": url,
                            "company_name": result.data.get("company_name", ""),
                            "description": result.data.get("description", ""),
                            "sector": result.data.get("sector", ""),
                            "technologies": result.data.get("technologies", ""),
                            "clients": result.data.get("clients", ""),
                            "location": result.data.get("location", ""),
                            "status_code": result.status_code,
                            "html_size": len(result.html) if result.html else 0,
                            "success": True
                        }
                        
                        # Score defense company
                        company_data["defense_score"] = self._score_defense_company(company_data)
                        company_data["priority"] = "High" if company_data["defense_score"] >= 70 else "Medium"
                        
                        companies.append(company_data)
                        print(f"✅ Found defense company: {company_data.get('company_name')}")
            
            return companies
            
        except Exception as e:
            print(f"❌ Error scraping defense companies: {e}")
            return []
    
    def _score_defense_company(self, company_data: Dict[str, Any]) -> int:
        """Score defense company (0-100)."""
        score = 0
        
        # Sector fit (30 points)
        sector = company_data.get("sector", "").lower()
        defense_keywords = ["defense", "military", "security", "cyber", "drone", "space", "surveillance"]
        if any(keyword in sector for keyword in defense_keywords):
            score += 30
        elif "technology" in sector or "tech" in sector:
            score += 20
        else:
            score += 10
        
        # Technology depth (25 points)
        technologies = company_data.get("technologies", "").lower()
        tech_keywords = ["ai", "machine learning", "autonomous", "sensor", "satellite", "encryption"]
        tech_score = sum(1 for keyword in tech_keywords if keyword in technologies)
        score += min(tech_score * 5, 25)
        
        # Client mentions (20 points)
        clients = company_data.get("clients", "").lower()
        if "government" in clients or "military" in clients or "defense" in clients:
            score += 20
        elif "enterprise" in clients or "corporate" in clients:
            score += 10
        
        # Website quality (15 points)
        html_size = company_data.get("html_size", 0)
        if html_size > 5000:
            score += 15
        elif html_size > 2000:
            score += 10
        elif html_size > 1000:
            score += 5
        
        # Location (10 points)
        location = company_data.get("location", "").lower()
        if "us" in location or "united states" in location or "uk" in location or "europe" in location:
            score += 10
        elif "canada" in location or "australia" in location:
            score += 5
        
        return min(score, 100)
    
    async def scrape_pe_vc_funds(self, regions: List[str], focus: str = "defense") -> List[Dict[str, Any]]:
        """
        Scrape PE/VC fund websites.
        
        Args:
            regions: List of regions to search
            focus: Investment focus area
        
        Returns:
            List of fund data
        """
        # Placeholder implementation
        return []
