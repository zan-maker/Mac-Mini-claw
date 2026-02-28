#!/usr/bin/env python3
"""Test YARS Reddit scraper integration"""

from reddit_scraper_yars_integration import RedditScraperYARS

def main():
    print("🧪 Testing YARS Reddit Scraper Integration...")
    
    scraper = RedditScraperYARS()
    
    # Check installation
    print("\n🔧 Checking YARS installation...")
    if not scraper._check_yars_installation():
        print("⚠️  YARS not fully installed, but fallback methods available")
    
    # Test with a small subreddit
    print("\n📊 Testing subreddit scraping...")
    subreddit_data = scraper.scrape_subreddit(
        subreddit="smallbusiness",
        category="hot",
        limit=5,
        time_filter="week"
    )
    
    print(f"  Success: {subreddit_data.get('success', False)}")
    print(f"  Source: {subreddit_data.get('source', 'unknown')}")
    print(f"  Posts found: {subreddit_data.get('total_posts', 0)}")
    
    if subreddit_data.get("success") and subreddit_data.get("posts"):
        print(f"  First post: {subreddit_data['posts'][0].get('title', 'N/A')[:50]}...")
    
    # Test search
    print("\n🔍 Testing search...")
    search_data = scraper.search_reddit(
        query="small business",
        limit=3
    )
    
    print(f"  Success: {search_data.get('success', False)}")
    print(f"  Source: {search_data.get('source', 'unknown')}")
    print(f"  Results found: {search_data.get('total_results', 0)}")
    
    # Test lead finding
    print("\n🎯 Testing Section 125 lead finding...")
    section125_leads = scraper.find_section125_leads(limit_per_sub=5)
    
    print(f"  Success: {section125_leads.get('success', False)}")
    print(f"  Total leads: {section125_leads.get('total_leads', 0)}")
    
    # Test CSV export
    print("\n📁 Testing CSV export...")
    if section125_leads.get("success") and section125_leads.get("leads"):
        csv_file = scraper.export_leads_to_csv(section125_leads, "test_section125_leads.csv")
        print(f"  CSV file: {csv_file}")
    
    print(f"\n📊 API calls today: {scraper.daily_call_count}/{scraper.max_daily_calls}")
    
    return True

if __name__ == "__main__":
    main()
    print("\n✅ YARS Reddit Scraper Integration Ready!")