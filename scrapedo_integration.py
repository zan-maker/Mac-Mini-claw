#!/usr/bin/env python3
"""
Scrape.do API Integration for Web Scraping
API Token: fc729705ffd04cc89cf0be3a681c1ab75076da07f22
Documentation: https://scrape.do/documentation/
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
import requests

class ScrapeDoIntegration:
    """Integration with Scrape.do API for web scraping"""
    
    def __init__(self, api_token: str = None, cache_dir: str = None):
        self.api_token = api_token or "fc729705ffd04cc89cf0be3a681c1ab75076da07f22"
        self.base_url = "https://api.scrape.do"
        self.cache_dir = cache_dir or "/Users/cubiczan/.openclaw/workspace/cache/scrapedo"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Rate limiting
        self.last_call_time = 0
        self.min_call_interval = 1.0  # 1 second between calls
        self.daily_call_count = 0
        self.max_daily_calls = 1000  # Scrape.do free tier limit
        
        # Headers
        self.headers = {
            "X-API-KEY": self.api_token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # Load daily stats
        self._load_daily_stats()
    
    def scrape_url(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Scrape a URL using Scrape.do API"""
        
        # Check cache first
        cache_key = f"scrape_{hash(url)}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                
                # Check if cache is fresh (less than 1 hour old)
                cache_time = datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))
                if (datetime.now() - cache_time).total_seconds() < 3600:
                    print(f"📄 Using cached data for {url}")
                    return cached["data"]
            except:
                pass
        
        # Check rate limits
        if not self._check_rate_limits():
            return {"error": "Rate limit reached", "url": url}
        
        try:
            print(f"🌐 Scraping: {url}")
            
            # Prepare request
            request_params = {
                "url": url,
                "render": "true",  # Render JavaScript
                "geo": "us",  # US geography
                "device": "desktop"
            }
            
            if params:
                request_params.update(params)
            
            # Make request
            response = requests.get(
                f"{self.base_url}/",
                params=request_params,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = {
                    "success": True,
                    "url": url,
                    "status_code": response.status_code,
                    "content": response.text,
                    "content_type": response.headers.get("content-type", ""),
                    "timestamp": datetime.now().isoformat(),
                    "source": "scrapedo"
                }
                
                # Cache the result
                cache_data = {
                    "timestamp": datetime.now().isoformat(),
                    "data": data
                }
                
                with open(cache_file, 'w') as f:
                    json.dump(cache_data, f, indent=2)
                
                # Update stats
                self._update_call_stats()
                
                return data
            else:
                return {
                    "success": False,
                    "url": url,
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"❌ Scrape.do error for {url}: {e}")
            return {
                "success": False,
                "url": url,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def scrape_multiple(self, urls: List[str], delay: float = 2.0) -> List[Dict[str, Any]]:
        """Scrape multiple URLs with delay between requests"""
        results = []
        
        for url in urls:
            result = self.scrape_url(url)
            results.append(result)
            
            # Delay between requests
            if delay > 0 and url != urls[-1]:
                time.sleep(delay)
        
        return results
    
    def extract_data(self, url: str, selector: str = None) -> Dict[str, Any]:
        """Scrape and extract specific data from a URL"""
        result = self.scrape_url(url)
        
        if not result.get("success"):
            return result
        
        # Basic data extraction
        extracted = {
            "url": url,
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "basic_info": self._extract_basic_info(result["content"])
        }
        
        # Extract with selector if provided
        if selector:
            extracted["selector_data"] = self._extract_with_selector(result["content"], selector)
        
        return extracted
    
    def _extract_basic_info(self, html: str) -> Dict[str, Any]:
        """Extract basic information from HTML"""
        import re
        
        info = {
            "title": "",
            "description": "",
            "keywords": [],
            "links_count": 0,
            "text_length": len(html)
        }
        
        try:
            # Extract title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE)
            if title_match:
                info["title"] = title_match.group(1).strip()
            
            # Extract meta description
            desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE)
            if desc_match:
                info["description"] = desc_match.group(1).strip()
            
            # Extract meta keywords
            keywords_match = re.search(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE)
            if keywords_match:
                info["keywords"] = [k.strip() for k in keywords_match.group(1).split(",")]
            
            # Count links
            links = re.findall(r'<a[^>]*href=["\'](.*?)["\'][^>]*>', html, re.IGNORECASE)
            info["links_count"] = len(links)
            
        except Exception as e:
            print(f"⚠️  Error extracting basic info: {e}")
        
        return info
    
    def _extract_with_selector(self, html: str, selector: str) -> List[str]:
        """Extract data using CSS selector (basic implementation)"""
        # For production, use BeautifulSoup or lxml
        # This is a simple regex-based implementation
        import re
        
        extracted = []
        
        if selector.startswith("."):  # Class selector
            class_name = selector[1:]
            pattern = rf'<[^>]*class=["\'][^"\']*{re.escape(class_name)}[^"\']*["\'][^>]*>(.*?)</[^>]*>'
            matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
            extracted = [m.strip() for m in matches]
        
        elif selector.startswith("#"):  # ID selector
            id_name = selector[1:]
            pattern = rf'<[^>]*id=["\']{re.escape(id_name)}["\'][^>]*>(.*?)</[^>]*>'
            matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
            extracted = [m.strip() for m in matches]
        
        elif selector == "a":  # Link selector
            pattern = r'<a[^>]*href=["\'](.*?)["\'][^>]*>(.*?)</a>'
            matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
            extracted = [f"{text.strip()} ({href.strip()})" for href, text in matches if href and text]
        
        return extracted
    
    def scrape_linkedin_company(self, company_name: str) -> Dict[str, Any]:
        """Scrape LinkedIn company page"""
        url = f"https://www.linkedin.com/company/{company_name}"
        return self.extract_data(url)
    
    def scrape_crunchbase(self, company_name: str) -> Dict[str, Any]:
        """Scrape Crunchbase company page"""
        url = f"https://www.crunchbase.com/organization/{company_name}"
        return self.extract_data(url)
    
    def scrape_google_search(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """Scrape Google search results"""
        encoded_query = query.replace(" ", "+")
        url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"
        
        result = self.scrape_url(url)
        
        if result.get("success"):
            # Extract search results
            import re
            content = result["content"]
            
            # Simple extraction of search results
            results = []
            pattern = r'<div[^>]*class="[^"]*g[^"]*"[^>]*>.*?<a[^>]*href=["\']/url\?q=(.*?)&[^>]*>(.*?)</a>'
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            
            for href, title in matches[:num_results]:
                results.append({
                    "title": re.sub(r'<[^>]*>', '', title).strip(),
                    "url": href,
                    "query": query
                })
            
            result["search_results"] = results
        
        return result
    
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
        
        print(f"📊 Scrape.do calls today: {self.daily_call_count}/{self.max_daily_calls}")
    
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
def test_scrapedo_integration():
    """Test Scrape.do integration"""
    print("🧪 Testing Scrape.do Integration...")
    
    scraper = ScrapeDoIntegration()
    
    # Test with a simple website
    print("\n🌐 Testing with example.com...")
    result = scraper.scrape_url("https://example.com")
    
    print(f"  Success: {result.get('success', False)}")
    print(f"  Status: {result.get('status_code', 0)}")
    print(f"  Content length: {len(result.get('content', ''))} chars")
    
    # Test data extraction
    print("\n🔍 Testing data extraction...")
    extracted = scraper.extract_data("https://example.com")
    
    if extracted.get("success"):
        basic_info = extracted.get("basic_info", {})
        print(f"  Title: {basic_info.get('title', 'N/A')}")
        print(f"  Description: {basic_info.get('description', 'N/A')[:50]}...")
        print(f"  Links count: {basic_info.get('links_count', 0)}")
    
    print(f"\n📊 API calls today: {scraper.daily_call_count}/{scraper.max_daily_calls}")
    
    return True


if __name__ == "__main__":
    test_scrapedo_integration()
    print("\n✅ Scrape.do Integration Ready!")