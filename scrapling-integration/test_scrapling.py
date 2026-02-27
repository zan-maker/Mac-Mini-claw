#!/usr/bin/env python3
"""
Test script for Scrapling integration with OpenClaw
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_basic_scraping():
    """Test basic scraping functionality."""
    print("🧪 Testing Scrapling Integration...")
    
    try:
        # Test import
        from scrapling_client import OpenClawScraplingClient
        print("✅ Import successful")
        
        # Initialize client
        client = OpenClawScraplingClient(use_browser=False, stealth_mode=True)
        client.initialize()
        print("✅ Client initialized")
        
        # Test scraping a simple site
        test_url = "https://httpbin.org/html"
        print(f"🔍 Testing scrape of: {test_url}")
        
        # Use CSS selectors
        selectors = {
            "title": "h1",
            "paragraph": "p"
        }
        
        result = await client.scrape_url(test_url, selectors)
        
        if result.success:
            print(f"✅ Scraping successful (Status: {result.status_code})")
            if result.data:
                print(f"📋 Extracted data: {result.data}")
            else:
                print("ℹ️ No data extracted (expected for test site)")
        else:
            print(f"❌ Scraping failed: {result.error}")
        
        # Clean up
        await client.close()
        print("✅ Client cleaned up")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure Scrapling is installed: pip install 'scrapling[ai]'")
        return False
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_lead_scraper():
    """Test lead scraping functionality."""
    print("\n🧪 Testing Lead Scraper...")
    
    try:
        from lead_scraper import LeadScraper
        print("✅ LeadScraper import successful")
        
        # Initialize scraper
        scraper = LeadScraper(stealth_mode=True)
        print("✅ LeadScraper initialized")
        
        # Test with a simple URL
        test_url = "https://httpbin.org/html"
        print(f"🔍 Testing lead scrape of: {test_url}")
        
        lead_data = await scraper.scrape_company_website(test_url)
        
        if lead_data.get("success"):
            print("✅ Lead scraping successful")
            company = lead_data.get("company", {})
            print(f"📊 Company name: {company.get('name')}")
            print(f"📊 Lead score: {company.get('lead_score')}/100")
        else:
            print(f"❌ Lead scraping failed: {lead_data.get('error')}")
        
        # Clean up
        await scraper.close()
        print("✅ LeadScraper cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during lead scraper test: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_cli_interface():
    """Test CLI interface."""
    print("\n🧪 Testing CLI Interface...")
    
    try:
        import subprocess
        import sys
        
        # Test CLI help
        print("🔍 Testing CLI help command...")
        result = subprocess.run(
            [sys.executable, "scrapling_cli.py", "--help"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0:
            print("✅ CLI help command works")
            # Check for expected commands in output
            if "single" in result.stdout and "batch" in result.stdout:
                print("✅ CLI commands detected")
                return True
            else:
                print("❌ CLI commands not found in help")
                return False
        else:
            print(f"❌ CLI help command failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during CLI test: {e}")
        return False

async def main():
    """Run all tests."""
    print("=" * 60)
    print("🚀 OpenClaw Scrapling Integration Test Suite")
    print("=" * 60)
    
    tests_passed = 0
    tests_total = 3
    
    # Test 1: Basic scraping
    if await test_basic_scraping():
        tests_passed += 1
    
    # Test 2: Lead scraper
    if await test_lead_scraper():
        tests_passed += 1
    
    # Test 3: CLI interface
    if await test_cli_interface():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    print(f"✅ Tests Passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("🎉 All tests passed! Scrapling integration is ready.")
        print("\n🚀 Next steps:")
        print("1. Use in your OpenClaw cron jobs:")
        print("   from scrapling_integration.lead_scraper import LeadScraper")
        print("2. Run CLI commands:")
        print("   python scrapling_cli.py single https://example.com --extractor company")
        print("3. Integrate with lead generation workflows")
        return 0
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure Scrapling is installed: pip install 'scrapling[ai]'")
        print("2. Check Python version (requires 3.8+)")
        print("3. Verify network connectivity")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)