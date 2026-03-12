#!/usr/bin/env python3
"""
Agent-Friendly Web Scraper using Firecrawl
Production-ready web scraping for AI agents
"""

import os
import sys
import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum
import subprocess
import tempfile

# Try to import Firecrawl SDK
try:
    from firecrawl import Firecrawl
    FIRECRAWL_AVAILABLE = True
except ImportError:
    FIRECRAWL_AVAILABLE = False
    print("⚠️  Firecrawl SDK not installed. Install with: pip install firecrawl-py")

class ScraperType(Enum):
    """Types of scrapers available"""
    FIRECRAWL = "firecrawl"  # Primary - production ready
    CLI = "cli"              # Firecrawl CLI fallback
    BASIC = "basic"          # Basic Python fallback
    SELENIUM = "selenium"    # Selenium for complex JS

@dataclass
class ScrapeResult:
    """Standardized scrape result"""
    success: bool
    content: Optional[str] = None
    metadata: Optional[Dict] = None
    error: Optional[str] = None
    source: Optional[str] = None
    scraper_type: Optional[ScraperType] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "success": self.success,
            "content": self.content,
            "metadata": self.metadata or {},
            "error": self.error,
            "source": self.source,
            "scraper_type": self.scraper_type.value if self.scraper_type else None
        }

class AgentWebScraper:
    """
    Production-ready web scraper for AI agents
    Uses Firecrawl as primary, with fallbacks
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize scraper with Firecrawl API key
        
        Args:
            api_key: Firecrawl API key (defaults to FIRECRAWL_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        self.firecrawl_client = None
        self.scraper_type = None
        
        # Initialize Firecrawl if available
        if FIRECRAWL_AVAILABLE and self.api_key:
            try:
                self.firecrawl_client = Firecrawl(api_key=self.api_key)
                self.scraper_type = ScraperType.FIRECRAWL
                print(f"✅ Firecrawl initialized (API key: {self.api_key[:10]}...)")
            except Exception as e:
                print(f"⚠️  Firecrawl initialization failed: {e}")
                self.scraper_type = ScraperType.CLI
        else:
            print("⚠️  Firecrawl not available, using CLI or basic fallback")
            self.scraper_type = ScraperType.CLI if self._check_cli_available() else ScraperType.BASIC
    
    def _check_cli_available(self) -> bool:
        """Check if Firecrawl CLI is available"""
        try:
            result = subprocess.run(["which", "firecrawl"], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def scrape_url(self, url: str, format: str = "markdown") -> ScrapeResult:
        """
        Scrape a single URL
        
        Args:
            url: URL to scrape
            format: Output format (markdown, html, json, etc.)
            
        Returns:
            ScrapeResult object
        """
        print(f"🌐 Scraping: {url}")
        
        # Try Firecrawl SDK first
        if self.scraper_type == ScraperType.FIRECRAWL and self.firecrawl_client:
            return self._scrape_with_firecrawl(url, format)
        
        # Try Firecrawl CLI
        elif self.scraper_type == ScraperType.CLI:
            return self._scrape_with_cli(url, format)
        
        # Fallback to basic Python
        else:
            return self._scrape_with_basic(url)
    
    def _scrape_with_firecrawl(self, url: str, format: str) -> ScrapeResult:
        """Scrape using Firecrawl SDK"""
        try:
            result = self.firecrawl_client.scrape(
                url,
                formats=[format]
            )
            
            return ScrapeResult(
                success=True,
                content=result.markdown if format == "markdown" else str(result),
                metadata={
                    "title": result.metadata.get("title", ""),
                    "sourceURL": result.metadata.get("sourceURL", url),
                    "statusCode": result.metadata.get("statusCode", 200)
                },
                source="firecrawl_sdk",
                scraper_type=ScraperType.FIRECRAWL
            )
            
        except Exception as e:
            return ScrapeResult(
                success=False,
                error=f"Firecrawl SDK error: {str(e)}",
                source="firecrawl_sdk",
                scraper_type=ScraperType.FIRECRAWL
            )
    
    def _scrape_with_cli(self, url: str, format: str) -> ScrapeResult:
        """Scrape using Firecrawl CLI"""
        try:
            # Create temp file for output
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
                tmp_path = tmp.name
            
            # Run firecrawl CLI command
            cmd = ["firecrawl", url, "--output", tmp_path]
            if format == "markdown":
                cmd.append("--only-main-content")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Read output from temp file
                with open(tmp_path, 'r') as f:
                    data = json.load(f)
                
                # Clean up temp file
                os.unlink(tmp_path)
                
                return ScrapeResult(
                    success=True,
                    content=data.get("markdown", "") if format == "markdown" else str(data),
                    metadata={
                        "title": data.get("metadata", {}).get("title", ""),
                        "sourceURL": url,
                        "cli_output": result.stdout[:200]
                    },
                    source="firecrawl_cli",
                    scraper_type=ScraperType.CLI
                )
            else:
                return ScrapeResult(
                    success=False,
                    error=f"CLI error: {result.stderr[:200]}",
                    source="firecrawl_cli",
                    scraper_type=ScraperType.CLI
                )
                
        except subprocess.TimeoutExpired:
            return ScrapeResult(
                success=False,
                error="CLI timeout after 30 seconds",
                source="firecrawl_cli",
                scraper_type=ScraperType.CLI
            )
        except Exception as e:
            return ScrapeResult(
                success=False,
                error=f"CLI execution error: {str(e)}",
                source="firecrawl_cli",
                scraper_type=ScraperType.CLI
            )
    
    def _scrape_with_basic(self, url: str) -> ScrapeResult:
        """Basic fallback scraping with requests/BeautifulSoup"""
        try:
            import requests
        except ImportError:
            return ScrapeResult(
                success=False,
                error="Basic scraping requires 'requests' package. Install with: pip install requests",
                source="basic_python",
                scraper_type=ScraperType.BASIC
            )
        
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            # Try to get at least some text without BeautifulSoup
            return self._scrape_with_requests_only(url)
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Break into lines and remove leading/trailing space
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return ScrapeResult(
                success=True,
                content=text,
                metadata={
                    "title": soup.title.string if soup.title else "",
                    "sourceURL": url,
                    "statusCode": response.status_code
                },
                source="basic_python",
                scraper_type=ScraperType.BASIC
            )
            
        except Exception as e:
            return ScrapeResult(
                success=False,
                error=f"Basic scraping error: {str(e)}",
                source="basic_python",
                scraper_type=ScraperType.BASIC
            )
    
    def _scrape_with_requests_only(self, url: str) -> ScrapeResult:
        """Fallback scraping with only requests (no BeautifulSoup)"""
        try:
            import requests
            import re
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Very basic HTML tag removal with regex
            text = response.text
            # Remove script tags
            text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
            # Remove style tags
            text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', ' ', text)
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Extract title if possible
            title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
            title = title_match.group(1) if title_match else ""
            
            return ScrapeResult(
                success=True,
                content=text[:5000],  # Limit output
                metadata={
                    "title": title,
                    "sourceURL": url,
                    "statusCode": response.status_code,
                    "note": "Basic scraping without BeautifulSoup"
                },
                source="basic_python_requests_only",
                scraper_type=ScraperType.BASIC
            )
            
        except Exception as e:
            return ScrapeResult(
                success=False,
                error=f"Requests-only scraping error: {str(e)}",
                source="basic_python_requests_only",
                scraper_type=ScraperType.BASIC
            )
    
    def search_and_scrape(self, query: str, limit: int = 5) -> List[ScrapeResult]:
        """
        Search the web and scrape results
        
        Args:
            query: Search query
            limit: Number of results to scrape
            
        Returns:
            List of ScrapeResult objects
        """
        print(f"🔍 Searching: {query}")
        
        if self.scraper_type == ScraperType.FIRECRAWL and self.firecrawl_client:
            try:
                # Use Firecrawl search
                results = self.firecrawl_client.search(query, limit=limit)
                
                scrape_results = []
                for result in results.data.get("web", [])[:limit]:
                    url = result.get("url")
                    if url:
                        scrape_result = self.scrape_url(url)
                        scrape_results.append(scrape_result)
                
                return scrape_results
                
            except Exception as e:
                print(f"⚠️  Firecrawl search failed: {e}")
                # Fallback to basic search simulation
                return self._simulate_search(query, limit)
        else:
            # Fallback to simulated search
            return self._simulate_search(query, limit)
    
    def _simulate_search(self, query: str, limit: int) -> List[ScrapeResult]:
        """Simulate search when Firecrawl search is not available"""
        # This is a placeholder - in production, you'd use a real search API
        # or Firecrawl's agent feature
        print(f"⚠️  Using simulated search for: {query}")
        
        # For demo purposes, return some example URLs based on query
        example_urls = {
            "finance": ["https://www.investopedia.com", "https://www.bloomberg.com"],
            "tech": ["https://techcrunch.com", "https://news.ycombinator.com"],
            "news": ["https://www.bbc.com/news", "https://www.reuters.com"],
            "default": ["https://www.wikipedia.org", "https://www.example.com"]
        }
        
        # Find relevant category
        category = "default"
        for key in example_urls:
            if key in query.lower():
                category = key
                break
        
        urls = example_urls[category][:limit]
        results = []
        
        for url in urls:
            result = self.scrape_url(url)
            results.append(result)
        
        return results
    
    def extract_structured(self, url: str, schema: Dict) -> ScrapeResult:
        """
        Extract structured data using a schema
        
        Args:
            url: URL to scrape
            schema: JSON schema for extraction
            
        Returns:
            ScrapeResult with structured data
        """
        if self.scraper_type == ScraperType.FIRECRAWL and self.firecrawl_client:
            try:
                result = self.firecrawl_client.scrape(
                    url,
                    formats=[{"type": "json", "schema": schema}]
                )
                
                return ScrapeResult(
                    success=True,
                    content=json.dumps(result.json, indent=2),
                    metadata={"sourceURL": url, "extraction_type": "structured"},
                    source="firecrawl_structured",
                    scraper_type=ScraperType.FIRECRAWL
                )
            except Exception as e:
                return ScrapeResult(
                    success=False,
                    error=f"Structured extraction failed: {e}",
                    source="firecrawl_structured",
                    scraper_type=ScraperType.FIRECRAWL
                )
        else:
            return ScrapeResult(
                success=False,
                error="Structured extraction requires Firecrawl SDK",
                source="firecrawl_structured",
                scraper_type=ScraperType.FIRECRAWL
            )

# Example usage and testing
def main():
    """Test the scraper"""
    print("🧪 Testing Agent Web Scraper...")
    
    # Initialize scraper
    scraper = AgentWebScraper()
    print(f"Scraper type: {scraper.scraper_type}")
    
    # Test scraping
    test_urls = [
        "https://example.com",
        "https://httpbin.org/html"
    ]
    
    for url in test_urls:
        print(f"\n📄 Testing: {url}")
        result = scraper.scrape_url(url)
        
        if result.success:
            print(f"✅ Success! Content length: {len(result.content or '')} chars")
            print(f"   Title: {result.metadata.get('title', 'N/A')}")
            print(f"   Source: {result.source}")
        else:
            print(f"❌ Failed: {result.error}")
    
    # Test search
    print(f"\n🔍 Testing search...")
    search_results = scraper.search_and_scrape("finance news", limit=2)
    print(f"Found {len(search_results)} results")
    
    for i, result in enumerate(search_results):
        status = "✅" if result.success else "❌"
        url = result.metadata.get('sourceURL', 'Unknown') if result.metadata else 'Unknown'
        print(f"  {status} Result {i+1}: {url}")

if __name__ == "__main__":
    main()