#!/usr/bin/env python3
"""
Scrapling CLI for OpenClaw
Command-line interface for AI-powered web scraping.
"""

import asyncio
import json
import sys
import argparse
from pathlib import Path
from typing import List, Optional
from scrapling_client import OpenClawScraplingClient, create_company_selectors, create_product_selectors, create_news_selectors


class ScraplingCLI:
    """Command-line interface for Scrapling."""
    
    def __init__(self):
        self.client = None
    
    async def initialize_client(self, use_browser: bool = False, stealth: bool = True):
        """Initialize the Scrapling client."""
        self.client = OpenClawScraplingClient(use_browser=use_browser, stealth_mode=stealth)
        self.client.initialize()
    
    async def scrape_single(self, url: str, extractor_type: Optional[str] = None, 
                           output_file: Optional[str] = None, use_browser: bool = False):
        """
        Scrape a single URL.
        
        Args:
            url: URL to scrape
            extractor_type: Type of extractor to use (company, product, news, or custom JSON file)
            output_file: Path to save output
            use_browser: Use browser automation
        """
        print(f"🔍 Scraping: {url}")
        
        # Select extractor
        extractors = None
        if extractor_type:
            if extractor_type == "company":
                extractors = create_company_extractor()
                print("📊 Using company information extractor")
            elif extractor_type == "product":
                extractors = create_product_extractor()
                print("🛍️ Using product information extractor")
            elif extractor_type == "news":
                extractors = create_news_extractor()
                print("📰 Using news/article extractor")
            elif extractor_type.endswith(".json"):
                # Load custom extractor from JSON file
                with open(extractor_type, 'r') as f:
                    extractor_config = json.load(f)
                # Convert to Scrapling extractors (simplified)
                extractors = {}
                for key, selector in extractor_config.items():
                    if selector.get("type") == "css":
                        extractors[key] = CSSExtractor(selector["selector"], 
                                                      multiple=selector.get("multiple", False),
                                                      attr=selector.get("attr"))
                    elif selector.get("type") == "xpath":
                        extractors[key] = XPathExtractor(selector["selector"],
                                                        multiple=selector.get("multiple", False))
                    elif selector.get("type") == "regex":
                        extractors[key] = RegexExtractor(selector["pattern"])
                print(f"📁 Using custom extractor from {extractor_type}")
        
        # Initialize client if not already done
        if not self.client:
            await self.initialize_client(use_browser=use_browser)
        
        # Perform scraping
        result = await self.client.scrape_url(url, extractors)
        
        # Display results
        if result.success:
            print(f"✅ Success! Status: {result.status_code}")
            
            if result.data:
                print("\n📋 Extracted Data:")
                print(json.dumps(result.data, indent=2, ensure_ascii=False))
            
            if output_file:
                self.client.save_to_file(result, output_file)
                print(f"💾 Saved to: {output_file}")
            
            # Show HTML stats
            if result.html:
                print(f"\n📄 HTML size: {len(result.html):,} characters")
                
        else:
            print(f"❌ Failed: {result.error}")
    
    async def scrape_batch(self, urls_file: str, extractor_type: Optional[str] = None,
                          output_dir: str = "./scraping_results", use_browser: bool = False):
        """
        Scrape multiple URLs from a file.
        
        Args:
            urls_file: Path to file containing URLs (one per line)
            extractor_type: Type of extractor to use
            output_dir: Directory to save results
            use_browser: Use browser automation
        """
        # Read URLs from file
        with open(urls_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"📋 Processing {len(urls)} URLs from {urls_file}")
        
        # Initialize client
        if not self.client:
            await self.initialize_client(use_browser=use_browser)
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Select extractor
        extractors = None
        if extractor_type == "company":
            extractors = create_company_extractor()
        elif extractor_type == "product":
            extractors = create_product_extractor()
        elif extractor_type == "news":
            extractors = create_news_extractor()
        
        # Scrape all URLs concurrently
        print("🚀 Starting concurrent scraping...")
        results = await self.client.scrape_multiple(urls, extractors)
        
        # Process results
        success_count = sum(1 for r in results if r.success)
        print(f"\n📊 Results: {success_count}/{len(urls)} successful")
        
        # Save results
        for i, result in enumerate(results):
            if result.success:
                filename = output_path / f"result_{i:03d}_{Path(urls[i]).name or 'page'}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump({
                        "url": result.url,
                        "success": result.success,
                        "status_code": result.status_code,
                        "data": result.data,
                        "html_preview": result.html[:500] + "..." if result.html else None
                    }, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {output_dir}")
    
    async def ai_extract(self, html_file: str, prompt: str, output_file: Optional[str] = None):
        """
        Use AI to extract data from HTML file.
        
        Args:
            html_file: Path to HTML file
            prompt: Natural language extraction prompt
            output_file: Path to save extracted data
        """
        print(f"🤖 AI Extraction from: {html_file}")
        print(f"📝 Prompt: {prompt}")
        
        # Read HTML file
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Initialize client
        if not self.client:
            await self.initialize_client()
        
        # Perform AI extraction
        result = self.client.extract_with_ai(html_content, prompt)
        
        # Display results
        print("\n🎯 AI Extraction Results:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Save results
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved to: {output_file}")
    
    def close(self):
        """Clean up resources."""
        if self.client:
            self.client.close()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Scrapling CLI - AI-powered web scraping for OpenClaw",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape a single URL with company extractor
  %(prog)s single https://example.com --extractor company
  
  # Scrape with browser automation (for JavaScript sites)
  %(prog)s single https://example.com --extractor company --browser
  
  # Scrape multiple URLs from file
  %(prog)s batch urls.txt --extractor company --output ./results
  
  # Use AI to extract data from HTML file
  %(prog)s ai page.html "Extract all product names and prices"
  
  # Use custom extractor from JSON file
  %(prog)s single https://example.com --extractor custom_extractor.json
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Single URL scraping
    single_parser = subparsers.add_parser("single", help="Scrape a single URL")
    single_parser.add_argument("url", help="URL to scrape")
    single_parser.add_argument("--extractor", choices=["company", "product", "news"], 
                              help="Type of extractor to use")
    single_parser.add_argument("--custom-extractor", help="Path to custom extractor JSON file")
    single_parser.add_argument("--output", "-o", help="Output file path")
    single_parser.add_argument("--browser", "-b", action="store_true", 
                              help="Use browser automation (for JavaScript sites)")
    single_parser.add_argument("--no-stealth", action="store_true", 
                              help="Disable stealth mode (not recommended)")
    
    # Batch scraping
    batch_parser = subparsers.add_parser("batch", help="Scrape multiple URLs from file")
    batch_parser.add_argument("urls_file", help="File containing URLs (one per line)")
    batch_parser.add_argument("--extractor", choices=["company", "product", "news"], 
                             help="Type of extractor to use")
    batch_parser.add_argument("--output", "-o", default="./scraping_results",
                             help="Output directory (default: ./scraping_results)")
    batch_parser.add_argument("--browser", "-b", action="store_true",
                             help="Use browser automation")
    batch_parser.add_argument("--no-stealth", action="store_true",
                             help="Disable stealth mode")
    
    # AI extraction
    ai_parser = subparsers.add_parser("ai", help="Use AI to extract data from HTML")
    ai_parser.add_argument("html_file", help="Path to HTML file")
    ai_parser.add_argument("prompt", help="Natural language extraction prompt")
    ai_parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Create CLI instance
    cli = ScraplingCLI()
    
    try:
        if args.command == "single":
            # Determine extractor
            extractor_type = args.extractor
            if args.custom_extractor:
                extractor_type = args.custom_extractor
            
            asyncio.run(cli.scrape_single(
                url=args.url,
                extractor_type=extractor_type,
                output_file=args.output,
                use_browser=args.browser
            ))
            
        elif args.command == "batch":
            asyncio.run(cli.scrape_batch(
                urls_file=args.urls_file,
                extractor_type=args.extractor,
                output_dir=args.output,
                use_browser=args.browser
            ))
            
        elif args.command == "ai":
            asyncio.run(cli.ai_extract(
                html_file=args.html_file,
                prompt=args.prompt,
                output_file=args.output
            ))
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        cli.close()


if __name__ == "__main__":
    main()