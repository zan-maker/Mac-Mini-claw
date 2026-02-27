#!/usr/bin/env python3
"""
Yellow Pages API Integration for Lead Generation
Section 125 Wellness and Business Precision Sales
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
import requests

class YellowPagesIntegration:
    """Integration with Yellow Pages API for lead generation"""
    
    def __init__(self, cache_dir: str = None):
        self.base_url = "https://yellow-pages-end-api.vercel.app/api"
        self.cache_dir = cache_dir or "/Users/cubiczan/.openclaw/workspace/cache/yellowpages"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Rate limiting
        self.last_call_time = 0
        self.min_call_interval = 1.0
        self.daily_call_count = 0
        self.max_daily_calls = 100
        
        # Load daily stats
        self._load_daily_stats()
    
    def search_businesses(self, query: str, location: str = None, category: str = None, 
                         limit: int = 50) -> Dict[str, Any]:
        """Search for businesses on Yellow Pages"""
        
        # Check cache first
        cache_key = f"search_{hash(f'{query}_{location}_{category}_{limit}')}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                
                # Check if cache is fresh (less than 24 hours old)
                cache_time = datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))
                if (datetime.now() - cache_time).total_seconds() < 86400:
                    print(f"📄 Using cached Yellow Pages data for '{query}'")
                    return cached["data"]
            except:
                pass
        
        # Check rate limits
        if not self._check_rate_limits():
            return {"error": "Rate limit reached", "query": query}
        
        try:
            print(f"📞 Searching Yellow Pages for: '{query}' in {location or 'anywhere'}")
            
            # Prepare request
            params = {
                "query": query,
                "limit": limit
            }
            
            if location:
                params["location"] = location
            
            if category:
                params["category"] = category
            
            # Make request
            response = requests.get(
                f"{self.base_url}/search",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                result = {
                    "success": True,
                    "query": query,
                    "location": location,
                    "category": category,
                    "timestamp": datetime.now().isoformat(),
                    "total_results": len(data.get("results", [])),
                    "results": data.get("results", []),
                    "source": "yellowpages_api"
                }
                
                # Cache the result
                cache_data = {
                    "timestamp": datetime.now().isoformat(),
                    "data": result
                }
                
                with open(cache_file, 'w') as f:
                    json.dump(cache_data, f, indent=2)
                
                # Update stats
                self._update_call_stats()
                
                return result
            else:
                return {
                    "success": False,
                    "query": query,
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"❌ Yellow Pages API error: {e}")
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_section_125_leads(self, location: str = None, limit: int = 100) -> Dict[str, Any]:
        """Get leads for Section 125 Wellness plans"""
        
        # Target businesses that would benefit from Section 125 plans
        queries = [
            "small business",
            "medium business", 
            "company",
            "corporation",
            "employer",
            "business with employees"
        ]
        
        all_results = []
        
        for query in queries:
            print(f"🔍 Searching for Section 125 leads: '{query}'")
            
            result = self.search_businesses(
                query=query,
                location=location,
                category="Business & Professional Services",
                limit=min(limit, 20)  # Smaller limit per query
            )
            
            if result.get("success"):
                all_results.extend(result.get("results", []))
            
            # Delay between queries
            time.sleep(1)
        
        # Filter and enrich results
        filtered_results = self._filter_section_125_leads(all_results)
        
        return {
            "success": True,
            "purpose": "Section 125 Wellness Plan Leads",
            "timestamp": datetime.now().isoformat(),
            "total_leads": len(filtered_results),
            "leads": filtered_results,
            "source": "yellowpages_api"
        }
    
    def get_business_precision_leads(self, industry: str = None, location: str = None, 
                                    limit: int = 100) -> Dict[str, Any]:
        """Get leads for business precision sales"""
        
        # Target industries for precision sales
        industries = {
            "manufacturing": ["manufacturing", "factory", "production"],
            "construction": ["construction", "contractor", "builder"],
            "healthcare": ["medical", "healthcare", "clinic", "hospital"],
            "retail": ["retail", "store", "shop", "outlet"],
            "professional": ["consulting", "agency", "firm", "services"]
        }
        
        if industry and industry in industries:
            search_terms = industries[industry]
        else:
            # Search all industries
            search_terms = []
            for terms in industries.values():
                search_terms.extend(terms)
        
        all_results = []
        
        for term in search_terms[:5]:  # Limit to 5 terms
            print(f"🔍 Searching for business precision leads: '{term}'")
            
            result = self.search_businesses(
                query=term,
                location=location,
                limit=min(limit, 20)
            )
            
            if result.get("success"):
                all_results.extend(result.get("results", []))
            
            # Delay between queries
            time.sleep(1)
        
        # Filter and enrich results
        filtered_results = self._filter_business_precision_leads(all_results, industry)
        
        return {
            "success": True,
            "purpose": f"Business Precision Sales Leads - {industry or 'All Industries'}",
            "timestamp": datetime.now().isoformat(),
            "total_leads": len(filtered_results),
            "leads": filtered_results,
            "source": "yellowpages_api"
        }
    
    def _filter_section_125_leads(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter and enrich Section 125 leads"""
        filtered = []
        
        for result in results:
            # Enrich with Section 125 relevance
            enriched = result.copy()
            
            # Add Section 125 specific fields
            enriched["section_125_relevance"] = self._calculate_section_125_relevance(result)
            enriched["lead_type"] = "section_125_wellness"
            enriched["priority"] = self._calculate_priority_score(result)
            
            # Only include if relevant
            if enriched["section_125_relevance"] >= 0.5:
                filtered.append(enriched)
        
        # Sort by priority
        filtered.sort(key=lambda x: x.get("priority", 0), reverse=True)
        
        return filtered
    
    def _filter_business_precision_leads(self, results: List[Dict[str, Any]], industry: str = None) -> List[Dict[str, Any]]:
        """Filter and enrich business precision leads"""
        filtered = []
        
        for result in results:
            # Enrich with business precision relevance
            enriched = result.copy()
            
            # Add business precision specific fields
            enriched["business_precision_relevance"] = self._calculate_business_precision_relevance(result, industry)
            enriched["lead_type"] = "business_precision_sales"
            enriched["priority"] = self._calculate_priority_score(result)
            
            # Only include if relevant
            if enriched["business_precision_relevance"] >= 0.5:
                filtered.append(enriched)
        
        # Sort by priority
        filtered.sort(key=lambda x: x.get("priority", 0), reverse=True)
        
        return filtered
    
    def _calculate_section_125_relevance(self, business: Dict[str, Any]) -> float:
        """Calculate relevance for Section 125 plans"""
        relevance = 0.5  # Base relevance
        
        # Check business name for indicators
        name = business.get("name", "").lower()
        
        # Businesses with employees are more relevant
        employee_indicators = ["company", "corp", "llc", "inc", "enterprises", "group", "associates"]
        for indicator in employee_indicators:
            if indicator in name:
                relevance += 0.2
                break
        
        # Check category
        category = business.get("category", "").lower()
        relevant_categories = ["professional", "services", "consulting", "healthcare", "technology"]
        for rel_cat in relevant_categories:
            if rel_cat in category:
                relevance += 0.1
        
        # Cap at 1.0
        return min(1.0, relevance)
    
    def _calculate_business_precision_relevance(self, business: Dict[str, Any], industry: str = None) -> float:
        """Calculate relevance for business precision sales"""
        relevance = 0.5  # Base relevance
        
        # Check business name
        name = business.get("name", "").lower()
        
        # Industry-specific relevance
        if industry:
            industry_terms = {
                "manufacturing": ["manufacturing", "factory", "production", "fabrication"],
                "construction": ["construction", "contractor", "builder", "contracting"],
                "healthcare": ["medical", "healthcare", "clinic", "hospital", "dental"],
                "retail": ["retail", "store", "shop", "outlet", "market"],
                "professional": ["consulting", "agency", "firm", "services", "advisory"]
            }
            
            if industry in industry_terms:
                for term in industry_terms[industry]:
                    if term in name:
                        relevance += 0.3
                        break
        
        # Check for established businesses
        established_indicators = ["established", "since", "founded", "est."]
        for indicator in established_indicators:
            if indicator in name.lower():
                relevance += 0.1
        
        # Cap at 1.0
        return min(1.0, relevance)
    
    def _calculate_priority_score(self, business: Dict[str, Any]) -> float:
        """Calculate priority score for leads"""
        score = 0.0
        
        # Higher score for businesses with more information
        if business.get("name"):
            score += 0.2
        
        if business.get("phone"):
            score += 0.3
        
        if business.get("address"):
            score += 0.2
        
        if business.get("website"):
            score += 0.2
        
        if business.get("category"):
            score += 0.1
        
        return score
    
    def export_leads_to_csv(self, leads: List[Dict[str, Any]], filename: str = None):
        """Export leads to CSV file"""
        import csv
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"yellowpages_leads_{timestamp}.csv"
        
        filepath = os.path.join(self.cache_dir, filename)
        
        # Define CSV fields
        fieldnames = [
            "name", "phone", "address", "city", "state", "zip", 
            "website", "category", "lead_type", "priority", "relevance",
            "timestamp", "source"
        ]
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for lead in leads:
                    row = {
                        "name": lead.get("name", ""),
                        "phone": lead.get("phone", ""),
                        "address": lead.get("address", ""),
                        "city": lead.get("city", ""),
                        "state": lead.get("state", ""),
                        "zip": lead.get("zip", ""),
                        "website": lead.get("website", ""),
                        "category": lead.get("category", ""),
                        "lead_type": lead.get("lead_type", ""),
                        "priority": lead.get("priority", 0),
                        "relevance": lead.get("section_125_relevance", lead.get("business_precision_relevance", 0)),
                        "timestamp": datetime.now().isoformat(),
                        "source": "yellowpages_api"
                    }
                    writer.writerow(row)
            
            print(f"✅ Exported {len(leads)} leads to {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error exporting to CSV: {e}")
            return None
    
    def _check_rate_limits(self) -> bool:
        """Check if we can make another API call"""
        current_time = time.time()
        
        # Check minimum interval
        if current_time - self.last_call_time < self.min_call_interval:
            time_to_wait = self.min_call_interval - (current_time - self.last_call_time)
            print(f"⏳ Waiting {time_to_wait:.1f}s for rate limit...")
            time.sleep(time_to_wait)
        
        # Check daily limit
        if self.daily_call_count >= self.max_daily_calls:
            print(f"⚠️  Daily API limit reached ({self.max_daily_calls} calls)")
            return False
        
        return True
    
    def _update_call_stats(self):
        """Update call statistics"""
        self.last_call_time = time.time()
        self.daily_call_count += 1
        self._save_daily_stats()
        
        print(f"📊 Yellow Pages calls today: {self.daily_call_count}/{self.max_daily_calls}")
    
    def _load_daily_stats(self):
        """Load daily call statistics"""
        stats_file = os.path.join(self.cache_dir, "daily_stats.json")
        
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
                
                # Check if stats are from today
                stats_date = stats.get("date", "2000-01-01")
                if stats_date == datetime.now().strftime("%Y-%m-%d"):
                    self.daily_call_count = stats.get("call_count", 0)
                else:
                    # Reset for new day
                    self.daily_call_count = 0
                    
            except Exception as e:
                print(f"⚠️  Error loading daily stats: {e}")
                self.daily_call_count = 0
        else:
            self.daily_call_count = 0
    
    def _save_daily_stats(self):
        """Save daily call statistics"""
        stats_file = os.path.join(self.cache_dir, "daily_stats.json")
        
        stats = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "call_count": self.daily_call_count,
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving daily stats: {e}")


# Test the integration
def test_yellowpages_integration():
    """Test Yellow Pages integration"""
    print("🧪 Testing Yellow Pages Integration...")
    
    yp = YellowPagesIntegration()
    
    # Test basic search
    print("\n🔍 Testing basic search...")
    result = yp.search_businesses(query="restaurant", location="New York", limit=5)
    
    print(f"  Success: {result.get('success', False)}")
    print(f"  Total results: {result.get('total_results', 0)}")
    
    if result.get("success") and result.get("results"):
        for i, business in enumerate(result.get("results", [])[:3]):
            print(f"  {i+1}. {business.get('name', 'N/A')} - {business.get('phone', 'N/A')}")
    
    # Test Section 125 leads
    print("\n🏥 Testing Section 125 leads...")
    section125_result = yp.get_section_125_leads(location="California", limit=10)
    
    print(f"  Success: {section125_result.get('success', False)}")
    print(f"  Total leads: {section125_result.get('total_leads', 0)}")
    
    # Test business precision leads
    print("\n🏭 Testing business precision leads...")
    precision_result = yp.get_business_precision_leads(industry="manufacturing", limit=10)
    
    print(f"  Success: {precision_result.get('success', False)}")
    print(f"  Total leads: {precision_result.get('total_leads', 0)}")
    
    print(f"\n📊 API calls today: {yp.daily_call_count}/{yp.max_daily_calls}")
    
    return True


if __name__ == "__main__":
    test_yellowpages_integration()
    print("\n✅ Yellow Pages Integration Ready!")