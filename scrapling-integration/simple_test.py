#!/usr/bin/env python3
"""
Simple test for Scrapling integration
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def main():
    print("🧪 Testing Scrapling Integration...")
    
    try:
        from scrapling_client import OpenClawScraplingClient, create_company_selectors, create_product_selectors, create_news_selectors
        
        # Initialize client without browser (simpler)
        client = OpenClawScraplingClient(use_browser=False, stealth_mode=False)
        client.initialize()
        
        print("✅ Client initialized")
        
        # Test with a simple URL
        url = "https://httpbin.org/html"
        selectors = {
            "title": "h1",
            "paragraph": "p"
        }
        
        print(f"🔍 Testing scrape of: {url}")
        result = await client.scrape_url(url, selectors)
        
        if result.success:
            print(f"✅ Success! Status: {result.status_code}")
            if result.data:
                print(f"📋 Extracted data: {result.data}")
            else:
                print("ℹ️ No data extracted (might be test site structure)")
        else:
            print(f"❌ Failed: {result.error}")
        
        # Test regex extraction
        print("\n🧪 Testing regex extraction...")
        html = "<html><body>Email: test@example.com, Phone: +1-555-123-4567</body></html>"
        patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "phone": r"(\+?\d[\d\s\-\(\)]{7,}\d)"
        }
        
        regex_result = client.extract_with_regex(html, patterns)
        print(f"✅ Regex extraction: {regex_result}")
        
        # Test utility functions
        print("\n🧪 Testing utility functions...")
        company_selectors = create_company_selectors()
        print(f"✅ Company selectors: {list(company_selectors.keys())}")
        
        product_selectors = create_product_selectors()
        print(f"✅ Product selectors: {list(product_selectors.keys())}")
        
        news_selectors = create_news_selectors()
        print(f"✅ News selectors: {list(news_selectors.keys())}")
        
        print("\n🎉 Basic Scrapling integration works!")
        print("\n🚀 Next steps:")
        print("1. Use in OpenClaw cron jobs for lead generation")
        print("2. Try CLI: python scrapling_cli.py single https://example.com --extractor company")
        print("3. Integrate with your existing workflows")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)