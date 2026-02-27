#!/usr/bin/env python3
"""
Scrapling Client for OpenClaw
Advanced web scraping with AI-powered extraction, Cloudflare bypass, and stealth capabilities.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
import httpx
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
    - 774x faster than BeautifulSoup with Lxml
    - Bypasses ALL types of Cloudflare Turnstile automatically
    - Adaptive scraping with AI-powered extraction
    - Stealth mode with browser fingerprinting
    - Async sessions for parallel scraping
    """
    
    def __init__(self, use_browser: bool = False, stealth_mode: bool = True):
        """
        Initialize Scrapling client.
        
        Args:
            use_browser: Use browser automation (Playwright) for JavaScript-heavy sites
            stealth_mode: Enable anti-detection measures (recommended)
        """
        self.use_browser = use_browser
        self.stealth_mode = stealth_mode
        self.scraper = None
        self.browser_scraper = None
        self.async_scraper = None
        
    def initialize(self):
        """Initialize the scraper instance."""
        if self.use_browser:
            self.browser_scraper = BrowserScraper(
                headless=True,
                stealth=self.stealth_mode,
                browser_type="chromium"  # chromium, firefox, webkit
            )
        else:
            self.scraper = Scraper(
                stealth=self.stealth_mode,
                max_retries=3,
                timeout=30
            )
            self.async_scraper = AsyncScraper(
                stealth=self.stealth_mode,
                max_retries=3,
                timeout=30
            )
    
    async def scrape_url(self, url: str, extractors: Optional[Dict[str, Any]] = None) -> ScrapingResult:
        """
        Scrape a URL with optional extraction rules.
        
        Args:
            url: URL to scrape
            extractors: Dictionary of extraction rules
                Example: {
                    "title": CSSExtractor("h1"),
                    "articles": CSSExtractor(".article", multiple=True),
                    "price": XPathExtractor("//span[@class='price']"),
                    "email": RegexExtractor(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
                }
        
        Returns:
            ScrapingResult object with extracted data
        """
        result = ScrapingResult(url=url, success=False)
        
        try:
            if self.use_browser and self.browser_scraper:
                # Use browser for JavaScript-heavy sites
                async with self.browser_scraper as browser:
                    page = await browser.new_page()
                    await page.goto(url)
                    
                    # Get HTML content
                    html = await page.content()
                    result.html = html
                    
                    # Extract data if extractors provided
                    if extractors:
                        extracted_data = {}
                        for key, extractor in extractors.items():
                            try:
                                if isinstance(extractor, (CSSExtractor, XPathExtractor)):
                                    extracted_data[key] = await extractor.extract(page)
                                else:
                                    extracted_data[key] = extractor.extract(html)
                            except Exception as e:
                                extracted_data[key] = f"Extraction error: {str(e)}"
                        result.data = extracted_data
                    
                    result.success = True
                    result.status_code = 200
                    
            elif self.scraper:
                # Use HTTP scraper for static sites
                response = self.scraper.get(url)
                result.html = response.text
                result.status_code = response.status_code
                
                # Extract data if extractors provided
                if extractors:
                    extracted_data = {}
                    for key, extractor in extractors.items():
                        try:
                            extracted_data[key] = extractor.extract(response.text)
                        except Exception as e:
                            extracted_data[key] = f"Extraction error: {str(e)}"
                    result.data = extracted_data
                
                result.success = response.status_code == 200
                
        except Exception as e:
            result.error = str(e)
            result.success = False
        
        return result
    
    async def scrape_multiple(self, urls: List[str], extractors: Optional[Dict[str, Any]] = None) -> List[ScrapingResult]:
        """
        Scrape multiple URLs concurrently.
        
        Args:
            urls: List of URLs to scrape
            extractors: Extraction rules (same for all URLs)
        
        Returns:
            List of ScrapingResult objects
        """
        if not self.async_scraper:
            self.async_scraper = AsyncScraper(stealth=self.stealth_mode)
        
        tasks = []
        for url in urls:
            task = self._async_scrape_single(url, extractors)
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
    
    async def _async_scrape_single(self, url: str, extractors: Optional[Dict[str, Any]] = None) -> ScrapingResult:
        """Internal method for async single URL scraping."""
        result = ScrapingResult(url=url, success=False)
        
        try:
            async with self.async_scraper as scraper:
                response = await scraper.get(url)
                result.html = response.text
                result.status_code = response.status_code
                
                if extractors:
                    extracted_data = {}
                    for key, extractor in extractors.items():
                        try:
                            extracted_data[key] = extractor.extract(response.text)
                        except Exception as e:
                            extracted_data[key] = f"Extraction error: {str(e)}"
                    result.data = extracted_data
                
                result.success = response.status_code == 200
                
        except Exception as e:
            result.error = str(e)
        
        return result
    
    def extract_with_ai(self, html: str, extraction_prompt: str) -> Dict[str, Any]:
        """
        Use AI to extract data from HTML based on natural language prompts.
        
        Args:
            html: HTML content
            extraction_prompt: Natural language description of what to extract
                Example: "Extract all product names, prices, and descriptions"
        
        Returns:
            Dictionary with extracted data
        """
        # Note: This requires the AI extension of Scrapling
        # In practice, you'd use: scrapling.ai.extract(html, extraction_prompt)
        # For now, we'll implement a placeholder
        
        try:
            # This is a simplified version - actual implementation would use Scrapling's AI module
            from scrapling.ai import AIExtractor
            
            extractor = AIExtractor()
            result = extractor.extract(html, extraction_prompt)
            return result
            
        except ImportError:
            # Fallback to basic extraction if AI module not available
            return {
                "note": "AI extraction requires 'scrapling[ai]' installation",
                "html_length": len(html),
                "prompt": extraction_prompt
            }
    
    def save_to_file(self, result: ScrapingResult, output_path: str):
        """Save scraping result to file."""
        import os
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            if result.html:
                f.write(result.html)
            elif result.data:
                json.dump(result.data, f, indent=2, ensure_ascii=False)
    
    def close(self):
        """Clean up resources."""
        if self.browser_scraper:
            asyncio.run(self.browser_scraper.close())
        if self.scraper:
            self.scraper.close()


# Utility functions for common scraping tasks
def create_company_extractor():
    """Create extractor for company information."""
    return {
        "company_name": CSSExtractor("h1, .company-name, .brand"),
        "description": CSSExtractor(".description, .about, .company-description"),
        "employees": RegexExtractor(r"(\d+)\s*(employees|staff|people)"),
        "location": CSSExtractor(".location, .address, [itemprop='address']"),
        "website": RegexExtractor(r"(https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"),
        "email": RegexExtractor(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
        "phone": RegexExtractor(r"(\+?\d[\d\s\-\(\)]{7,}\d)"),
        "industry": CSSExtractor(".industry, .sector, .category")
    }

def create_product_extractor():
    """Create extractor for e-commerce product information."""
    return {
        "product_name": CSSExtractor("h1.product-title, .product-name"),
        "price": CSSExtractor(".price, .product-price, [itemprop='price']"),
        "description": CSSExtractor(".product-description, .description"),
        "sku": CSSExtractor(".sku, [itemprop='sku']"),
        "availability": CSSExtractor(".availability, .stock-status"),
        "images": CSSExtractor(".product-image img", attr="src", multiple=True),
        "reviews": CSSExtractor(".review, .rating", multiple=True),
        "specifications": CSSExtractor(".specs, .features li", multiple=True)
    }

def create_news_extractor():
    """Create extractor for news/article content."""
    return {
        "title": CSSExtractor("h1, .article-title, .headline"),
        "author": CSSExtractor(".author, .byline, [itemprop='author']"),
        "date": CSSExtractor(".date, .published, [itemprop='datePublished']"),
        "content": CSSExtractor(".article-content, .post-content, [itemprop='articleBody']"),
        "summary": CSSExtractor(".summary, .excerpt, .lead"),
        "tags": CSSExtractor(".tags a, .categories a", multiple=True),
        "image": CSSExtractor(".article-image img", attr="src")
    }


# Example usage
async def example_usage():
    """Example of how to use the Scrapling client."""
    
    # Initialize client
    client = OpenClawScraplingClient(use_browser=False, stealth_mode=True)
    client.initialize()
    
    # Example 1: Scrape a single URL with extractors
    url = "https://example.com"
    extractors = {
        "title": CSSExtractor("h1"),
        "links": CSSExtractor("a", attr="href", multiple=True)
    }
    
    result = await client.scrape_url(url, extractors)
    print(f"Success: {result.success}")
    print(f"Data: {json.dumps(result.data, indent=2)}")
    
    # Example 2: Scrape multiple URLs concurrently
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    ]
    
    results = await client.scrape_multiple(urls, extractors)
    for r in results:
        print(f"URL: {r.url}, Success: {r.success}")
    
    # Example 3: Use AI extraction
    html = "<html><body><h1>Example</h1><p>Some content</p></body></html>"
    ai_result = client.extract_with_ai(html, "Extract the main heading and paragraph")
    print(f"AI Extraction: {ai_result}")
    
    # Clean up
    client.close()


if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())