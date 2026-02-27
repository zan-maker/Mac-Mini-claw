#!/usr/bin/env python3
"""
Lead Scraper for OpenClaw using Scrapling
Enhanced lead generation with AI-powered web scraping.
"""

import asyncio
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from scrapling_client import OpenClawScraplingClient, create_company_selectors


class LeadScraper:
    """
    Advanced lead scraper using Scrapling for OpenClaw.
    
    Features:
    - Company information extraction from websites
    - Email and phone number discovery
    - Employee count estimation
    - Industry classification
    - Lead scoring based on scraped data
    """
    
    def __init__(self, stealth_mode: bool = True):
        self.client = OpenClawScraplingClient(use_browser=False, stealth_mode=stealth_mode)
        self.client.initialize()
        self.lead_counter = 0
    
    async def scrape_company_website(self, url: str) -> Dict[str, Any]:
        """
        Scrape company website for lead information.
        
        Args:
            url: Company website URL
        
        Returns:
            Dictionary with company information
        """
        print(f"🔍 Scraping company: {url}")
        
        # Use company selectors
        selectors = create_company_selectors()
        
        # Add additional selectors for lead generation
        selectors.update({
            "technologies": ".tech-stack, .technologies, .tools",
            "funding": ".funding, .investment, .raised",
            "team": ".team-member, .employee, .staff",
            "testimonials": ".testimonial, .review, .quote",
            "blog_posts": ".post, .article, .blog-entry"
        })
        
        result = await self.client.scrape_url(url, selectors)
        
        if not result.success:
            return {
                "url": url,
                "success": False,
                "error": result.error
            }
        
        # Process and enrich the data
        company_data = self._process_company_data(result.data, url, result.html)
        
        return {
            "url": url,
            "success": True,
            "scraped_at": datetime.now().isoformat(),
            "status_code": result.status_code,
            "html_size": len(result.html) if result.html else 0,
            "company": company_data
        }
    
    def _process_company_data(self, raw_data: Dict[str, Any], url: str, html: str) -> Dict[str, Any]:
        """
        Process and enrich scraped company data.
        
        Args:
            raw_data: Raw extracted data
            url: Company URL
            html: HTML content
        
        Returns:
            Enriched company data
        """
        # Extract emails and phones using regex
        email = self._find_best_email(html)
        phone = self._extract_phone(html)
        
        company = {
            "name": self._extract_company_name(raw_data, url, html),
            "domain": self._extract_domain(url),
            "description": raw_data.get("description", ""),
            "industry": self._classify_industry(raw_data, html),
            "estimated_employees": self._estimate_employee_count(raw_data, html),
            "location": raw_data.get("location", ""),
            "email": email,
            "phone": phone,
            "technologies": raw_data.get("technologies", ""),
            "social_links": raw_data.get("social_links", ""),
            "funding_mentions": raw_data.get("funding", ""),
            "team_size": len(str(raw_data.get("team", "")).split(',')) if raw_data.get("team") else None,
            "testimonial_count": len(str(raw_data.get("testimonials", "")).split(',')) if raw_data.get("testimonials") else 0,
            "blog_activity": len(str(raw_data.get("blog_posts", "")).split(',')) if raw_data.get("blog_posts") else 0,
            "website_quality": self._assess_website_quality(html),
            "lead_score": 0  # Will be calculated
        }
        
        # Calculate lead score
        company["lead_score"] = self._calculate_lead_score(company)
        
        return company
    
    def _extract_company_name(self, raw_data: Dict[str, Any], url: str, html: str) -> str:
        """Extract company name from various sources."""
        # Try extracted name first
        if raw_data.get("company_name"):
            return str(raw_data["company_name"])
        
        # Try to extract from title tag
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
            # Clean up title (remove common suffixes)
            clean_title = re.sub(r'\s*[-|:]\s*.*$', '', title)
            clean_title = re.sub(r'\s*-\s*Home$', '', clean_title, flags=re.IGNORECASE)
            if clean_title and len(clean_title) > 3:
                return clean_title
        
        # Fallback to domain name
        domain = self._extract_domain(url)
        return domain.replace("www.", "").split(".")[0].title()
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    
    def _classify_industry(self, raw_data: Dict[str, Any], html: str) -> str:
        """Classify company industry based on content."""
        industry_keywords = {
            "Technology": ["software", "tech", "saas", "platform", "api", "cloud", "ai", "machine learning"],
            "Healthcare": ["health", "medical", "hospital", "clinic", "pharma", "biotech", "wellness"],
            "Finance": ["finance", "bank", "investment", "insurance", "fintech", "payments", "wealth"],
            "E-commerce": ["shop", "store", "marketplace", "retail", "ecommerce", "buy", "sell"],
            "Manufacturing": ["manufacturing", "factory", "production", "industrial", "machinery"],
            "Professional Services": ["consulting", "services", "agency", "advisory", "solutions"],
            "Education": ["education", "learning", "school", "university", "training", "course"]
        }
        
        # Combine all text for analysis
        all_text = html.lower()
        if raw_data.get("description"):
            all_text += " " + str(raw_data["description"]).lower()
        if raw_data.get("industry"):
            all_text += " " + str(raw_data["industry"]).lower()
        
        # Find matching industry
        best_industry = "Other"
        best_score = 0
        
        for industry, keywords in industry_keywords.items():
            score = sum(1 for keyword in keywords if keyword in all_text)
            if score > best_score:
                best_score = score
                best_industry = industry
        
        return best_industry
    
    def _estimate_employee_count(self, raw_data: Dict[str, Any], html: str) -> Optional[int]:
        """Estimate employee count based on various signals."""
        # Try to extract from raw data first
        if raw_data.get("employees"):
            employees_str = str(raw_data["employees"])
            match = re.search(r'(\d+)', employees_str)
            if match:
                return int(match.group(1))
        
        # Estimate based on team size
        if raw_data.get("team"):
            team_size = len(raw_data["team"])
            # Team page usually shows key people, multiply by factor
            return team_size * 10  # Rough estimate
        
        # Estimate based on website complexity
        lines_of_html = html.count('\n')
        if lines_of_html > 5000:
            return 100  # Large, complex site
        elif lines_of_html > 1000:
            return 50   # Medium site
        elif lines_of_html > 200:
            return 10   # Small site
        
        return None
    
    def _find_best_email(self, html: str) -> Optional[str]:
        """Find the best email address from HTML."""
        import re
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, html)
        
        # Filter and prioritize
        valid_emails = []
        for email in emails:
            email = email.strip().lower()
            # Skip common placeholder emails
            if any(placeholder in email for placeholder in 
                  ["example.com", "test.com", "placeholder", "noreply", "no-reply"]):
                continue
            # Skip email harvesters
            if email.endswith(".png") or email.endswith(".jpg"):
                continue
            valid_emails.append(email)
        
        # Return the first valid email, or None
        return valid_emails[0] if valid_emails else None
    
    def _extract_phone(self, html: str) -> Optional[str]:
        """Extract phone number from HTML."""
        import re
        
        phone_pattern = r'(\+?\d[\d\s\-\(\)]{7,}\d)'
        phones = re.findall(phone_pattern, html)
        
        return phones[0] if phones else None
    
    def _assess_website_quality(self, html: str) -> str:
        """Assess website quality based on HTML analysis."""
        # Check for modern web features
        has_react = "react" in html.lower() or "react-dom" in html
        has_vue = "vue" in html.lower()
        has_angular = "angular" in html.lower()
        
        # Check for analytics
        has_google_analytics = "google-analytics" in html.lower() or "gtag" in html.lower()
        has_meta_tags = '<meta ' in html
        
        # Check for structured data
        has_json_ld = 'application/ld+json' in html
        
        # Determine quality level
        if has_json_ld and (has_react or has_vue or has_angular):
            return "High"
        elif has_google_analytics and has_meta_tags:
            return "Medium"
        else:
            return "Basic"
    
    def _calculate_lead_score(self, company: Dict[str, Any]) -> int:
        """Calculate lead score (0-100) based on company data."""
        score = 0
        
        # Company name (5 points)
        if company["name"] and len(company["name"]) > 2:
            score += 5
        
        # Description (10 points)
        if company["description"] and len(company["description"]) > 50:
            score += 10
        
        # Industry classification (10 points)
        if company["industry"] != "Other":
            score += 10
        
        # Employee count (20 points)
        if company["estimated_employees"]:
            if company["estimated_employees"] >= 100:
                score += 20
            elif company["estimated_employees"] >= 50:
                score += 15
            elif company["estimated_employees"] >= 20:
                score += 10
            elif company["estimated_employees"] >= 10:
                score += 5
        
        # Contact information (25 points)
        if company["email"]:
            score += 15
        if company["phone"]:
            score += 10
        
        # Website quality (15 points)
        if company["website_quality"] == "High":
            score += 15
        elif company["website_quality"] == "Medium":
            score += 10
        elif company["website_quality"] == "Basic":
            score += 5
        
        # Additional signals (15 points)
        if company["social_links"]:
            score += min(len(company["social_links"]) * 3, 10)
        if company["blog_activity"] > 0:
            score += 5
        
        return min(score, 100)
    
    async def scrape_multiple_companies(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Scrape multiple company websites concurrently."""
        print(f"🚀 Starting concurrent scraping of {len(urls)} companies...")
        
        tasks = []
        for url in urls:
            task = self.scrape_company_website(url)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"❌ Error scraping {urls[i]}: {result}")
                processed_results.append({
                    "url": urls[i],
                    "success": False,
                    "error": str(result)
                })
            else:
                processed_results.append(result)
                if result.get("success"):
                    company = result.get("company", {})
                    print(f"✅ {urls[i]}: {company.get('name')} - Score: {company.get('lead_score')}/100")
        
        return processed_results
    
    def save_leads_to_file(self, leads: List[Dict[str, Any]], output_file: str):
        """Save leads to JSON file."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Filter successful leads
        successful_leads = [lead for lead in leads if lead.get("success")]
        
        # Sort by lead score
        successful_leads.sort(key=lambda x: x.get("company", {}).get("lead_score", 0), reverse=True)
        
        # Prepare data for saving
        data = {
            "generated_at": datetime.now().isoformat(),
            "total_leads": len(leads),
            "successful_leads": len(successful_leads),
            "leads": successful_leads
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(successful_leads)} leads to {output_file}")
        
        # Also create a summary CSV
        self._create_lead_summary(successful_leads, output_path.with_suffix('.csv'))
    
    def _create_lead_summary(self, leads: List[Dict[str, Any]], csv_path: Path):
        """Create CSV summary of leads."""
        import csv
        
        fieldnames = [
            "Company Name", "Domain", "Industry", "Estimated Employees",
            "Location", "Email", "Phone", "Lead Score", "Website Quality",
            "URL", "Description Preview"
        ]
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for lead in leads:
                company = lead.get("company", {})
                writer.writerow({
                    "Company Name": company.get("name", ""),
                    "Domain": company.get("domain", ""),
                    "Industry": company.get("industry", ""),
                    "Estimated Employees": company.get("estimated_employees", ""),
                    "Location": company.get("location", ""),
                    "Email": company.get("email", ""),
                    "Phone": company.get("phone", ""),
                    "Lead Score": company.get("lead_score", 0),
                    "Website Quality": company.get("website_quality", ""),
                    "URL": lead.get("url", ""),
                    "Description Preview": (company.get("description", "")[:100] + "...") 
                                          if company.get("description") else ""
                })
        
        print(f"📊 Created summary CSV: {csv_path}")
    
    async def close(self):
        """Clean up resources."""
        if self.client:
            await self.client.close()


# Example usage
async def example_scraping():
    """Example of lead scraping."""
    
    # Initialize scraper
    scraper = LeadScraper(stealth_mode=True)
    
    # Example company URLs
    urls = [
        "https://stripe.com",
        "https://airbnb.com",
        "https://slack.com",
        "https://notion.so",
        "https://figma.com"
    ]
    
    # Scrape companies
    leads = await scraper.scrape_multiple_companies(urls)
    
    # Save results
    scraper.save_leads_to_file(leads, "./leads/company_leads.json")
    
    # Display top leads
    print("\n🏆 Top Leads:")
    successful_leads = [lead for lead in leads if lead.get("success")]
    for i, lead in enumerate(successful_leads[:5], 1):
        company = lead.get("company", {})
        print(f"{i}. {company.get('name')} - Score: {company.get('lead_score')}/100")
        print(f"   Industry: {company.get('industry')}")
        print(f"   Employees: {company.get('estimated_employees')}")
        print(f"   Email: {company.get('email')}")
        print()
    
    # Clean up
    scraper.close()


if __name__ == "__main__":
    # Run example
    asyncio.run(example_scraping())