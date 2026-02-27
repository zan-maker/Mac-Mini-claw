#!/usr/bin/env python3
"""
Scrapling Client for OpenClaw - Fixed Version
Using actual Scrapling API structure.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from scrapling.fetchers import Fetcher, AsyncFetcher, DynamicFetcher, StealthyFetcher
from scrapling.parser import Selector

@dataclass
class ScrapingResult:
    """Result container for scraping operations."""
    url: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    html: Optional[str] = None
    markdown: Optional[str] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    extraction_time: Optional[float] = None

class OpenClawScraplingClient:
    """
    Scrapling client for OpenClaw with AI-powered extraction capabilities.
    
    Features:
    - Fast scraping with Lxml backend
    - Cloudflare bypass capabilities
    - Adaptive scraping with selector-based extraction
    - Stealth mode with anti-detection
    - Async sessions for parallel scraping
    """
    
    def __init__(self, use_browser: bool = False, stealth_mode: bool = True):
        """
        Initialize Scrapling client.
        
        Args:
            use_browser: Use browser automation (DynamicFetcher) for JavaScript-heavy sites
            stealth_mode: Enable anti-detection measures (recommended)
        """
        self.use_browser = use_browser
        self.stealth_mode = stealth_mode
        self.fetcher = None
        self.async_fetcher = None
        self.dynamic_fetcher = None
        
    def initialize(self):
        """Initialize the fetcher instances."""
        if self.use_browser:
            self.dynamic_fetcher = DynamicFetcher(
                headless=True,
                stealth=self.stealth_mode
            )
        else:
            if self.stealth_mode:
                self.fetcher = StealthyFetcher()
            else:
                self.fetcher = Fetcher()
            
            self.async_fetcher = AsyncFetcher(stealth=self.stealth_mode)
    
    async def scrape_url(self, url: str, selectors: Optional[Dict[str, str]] = None) -> ScrapingResult:
        """
        Scrape a URL with optional CSS selectors.
        
        Args:
            url: URL to scrape
            selectors: Dictionary of CSS selectors for extraction
                Example: {
                    "title": "h1",
                    "articles": ".article",
                    "links": "a[href]"
                }
        
        Returns:
            ScrapingResult object with extracted data
        """
        result = ScrapingResult(url=url, success=False)
        
        try:
            if self.use_browser and self.dynamic_fetcher:
                # Use dynamic fetcher for JavaScript-heavy sites
                response = await self.dynamic_fetcher.get(url)
                result.html = response.text
                result.status_code = response.status
                
                # Extract data if selectors provided
                if selectors and result.html:
                    result.data = self._extract_with_selectors(result.html, selectors)
                
                result.success = response.status == 200
                
            elif self.fetcher:
                # Use HTTP fetcher for static sites
                # Handle different fetcher types
                if hasattr(self.fetcher, 'fetch'):
                    response = self.fetcher.fetch(url)
                elif hasattr(self.fetcher, 'get'):
                    response = self.fetcher.get(url)
                else:
                    raise AttributeError("Fetcher has neither 'fetch' nor 'get' method")
                    
                result.html = response.text
                result.status_code = response.status
                
                # Extract data if selectors provided
                if selectors and result.html:
                    result.data = self._extract_with_selectors(result.html, selectors)
                
                result.success = response.status == 200
                
        except Exception as e:
            result.error = str(e)
            result.success = False
        
        return result
    
    def _extract_with_selectors(self, html: str, selectors: Dict[str, str]) -> Dict[str, Any]:
        """
        Extract data from HTML using CSS selectors.
        
        Args:
            html: HTML content
            selectors: Dictionary of CSS selectors
        
        Returns:
            Dictionary with extracted data
        """
        extracted_data = {}
        selector = Selector(html)
        
        for key, css_selector in selectors.items():
            try:
                elements = selector.css(css_selector)
                if elements:
                    if len(elements) == 1:
                        extracted_data[key] = elements[0].text()
                    else:
                        extracted_data[key] = [elem.text() for elem in elements]
                else:
                    extracted_data[key] = None
            except Exception as e:
                extracted_data[key] = f"Extraction error: {str(e)}"
        
        return extracted_data
    
    async def scrape_multiple(self, urls: List[str], selectors: Optional[Dict[str, str]] = None) -> List[ScrapingResult]:
        """
        Scrape multiple URLs concurrently.
        
        Args:
            urls: List of URLs to scrape
            selectors: CSS selectors (same for all URLs)
        
        Returns:
            List of ScrapingResult objects
        """
        if not self.async_fetcher:
            self.async_fetcher = AsyncFetcher(stealth=self.stealth_mode)
        
        tasks = []
        for url in urls:
            task = self._async_scrape_single(url, selectors)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(ScrapingResult(
                    url=urls[i],
                    success=False,
                    error=str(result)
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _async_scrape_single(self, url: str, selectors: Optional[Dict[str, str]] = None) -> ScrapingResult:
        """Internal method for async single URL scraping."""
        result = ScrapingResult(url=url, success=False)
        
        try:
            response = await self.async_fetcher.get(url)
            result.html = response.text
            result.status_code = response.status_code
            
            if selectors and result.html:
                result.data = self._extract_with_selectors(result.html, selectors)
            
            result.success = response.status_code == 200
            
        except Exception as e:
            result.error = str(e)
        
        return result
    
    def extract_with_regex(self, html: str, patterns: Dict[str, str]) -> Dict[str, Any]:
        """
        Extract data from HTML using regex patterns.
        
        Args:
            html: HTML content
            patterns: Dictionary of regex patterns
                Example: {
                    "emails": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                    "phones": r"(\+?\d[\d\s\-\(\)]{7,}\d)"
                }
        
        Returns:
            Dictionary with extracted data
        """
        import re
        
        extracted_data = {}
        
        for key, pattern in patterns.items():
            try:
                matches = re.findall(pattern, html)
                if matches:
                    extracted_data[key] = matches[0] if len(matches) == 1 else matches
                else:
                    extracted_data[key] = None
            except Exception as e:
                extracted_data[key] = f"Regex error: {str(e)}"
        
        return extracted_data
    
    def save_to_file(self, result: ScrapingResult, output_path: str):
        """Save scraping result to file."""
        import os
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            if result.html:
                f.write(result.html)
            elif result.data:
                json.dump(result.data, f, indent=2, ensure_ascii=False)
    
    async def close(self):
        """Clean up resources."""
        # Scrapling fetchers don't have close methods
        # They use context managers internally
        pass


# Utility functions for common scraping tasks
def create_company_selectors():
    """Create selectors for company information."""
    return {
        "company_name": "h1, .company-name, .brand, [itemprop='name']",
        "description": ".description, .about, .company-description, [itemprop='description']",
        "location": ".location, .address, [itemprop='address']",
        "industry": ".industry, .sector, .category",
        "social_links": "a[href*='linkedin'], a[href*='twitter'], a[href*='facebook']",
        "team_members": ".team-member, .employee, .staff",
        "testimonials": ".testimonial, .review, .quote"
    }

def create_product_selectors():
    """Create selectors for e-commerce product information."""
    return {
        "product_name": "h1.product-title, .product-name, [itemprop='name']",
        "price": ".price, .product-price, [itemprop='price']",
        "description": ".product-description, .description, [itemprop='description']",
        "sku": ".sku, [itemprop='sku']",
        "availability": ".availability, .stock-status, [itemprop='availability']",
        "images": ".product-image img, [itemprop='image']",
        "reviews": ".review, .rating, [itemprop='review']",
        "specifications": ".specs, .features li"
    }

def create_news_selectors():
    """Create selectors for news/article content."""
    return {
        "title": "h1, .article-title, .headline, [itemprop='headline']",
        "author": ".author, .byline, [itemprop='author']",
        "date": ".date, .published, [itemprop='datePublished']",
        "content": ".article-content, .post-content, [itemprop='articleBody']",
        "summary": ".summary, .excerpt, .lead",
        "tags": ".tags a, .categories a",
        "image": ".article-image img, [itemprop='image']"
    }


# Example usage
async def example_usage():
    """Example of how to use the Scrapling client."""
    
    # Initialize client
    client = OpenClawScraplingClient(use_browser=False, stealth_mode=True)
    client.initialize()
    
    # Example 1: Scrape a single URL with selectors
    url = "https://httpbin.org/html"
    selectors = {
        "title": "h1",
        "paragraph": "p"
    }
    
    result = await client.scrape_url(url, selectors)
    print(f"Success: {result.success}")
    print(f"Data: {json.dumps(result.data, indent=2)}")
    
    # Example 2: Scrape multiple URLs concurrently
    urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/headers",
        "https://httpbin.org/user-agent"
    ]
    
    results = await client.scrape_multiple(urls, selectors)
    for r in results:
        print(f"URL: {r.url}, Success: {r.success}")
    
    # Example 3: Use regex extraction
    html = "<html><body>Email: test@example.com, Phone: +1-555-123-4567</body></html>"
    patterns = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"(\+?\d[\d\s\-\(\)]{7,}\d)"
    }
    regex_result = client.extract_with_regex(html, patterns)
    print(f"Regex Extraction: {regex_result}")
    
    # Clean up
    await client.close()


if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())