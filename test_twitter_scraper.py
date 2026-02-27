#!/usr/bin/env python3
"""Quick test of Twitter scraper with Scrape.do"""

from twitter_scraper_integration import TwitterScraperIntegration

def main():
    print("🧪 Testing Twitter Scraper with Scrape.do...")
    
    scraper = TwitterScraperIntegration()
    
    # Test 1: Basic functionality
    print("\n1️⃣ Testing basic tweet scraping...")
    tweet_data = scraper.scrape_tweet(
        "https://x.com/elonmusk/status/1679128693120028672",
        method="scrapedo"
    )
    
    print(f"   Success: {tweet_data.get('success', False)}")
    print(f"   Source: {tweet_data.get('source', 'unknown')}")
    print(f"   Tweet ID: {tweet_data.get('tweet_id', 'N/A')}")
    
    # Test 2: Profile scraping
    print("\n2️⃣ Testing profile scraping...")
    profile_data = scraper.scrape_profile("elonmusk", method="scrapedo")
    
    print(f"   Success: {profile_data.get('success', False)}")
    print(f"   Source: {profile_data.get('source', 'unknown')}")
    print(f"   Username: {profile_data.get('username', 'N/A')}")
    
    # Test 3: Search
    print("\n3️⃣ Testing search...")
    search_data = scraper.search_tweets("web scraping", limit=3)
    
    print(f"   Success: {search_data.get('success', False)}")
    print(f"   Source: {search_data.get('source', 'unknown')}")
    
    if search_data.get("success"):
        print(f"   Tweets found: {search_data.get('total_tweets_found', 0)}")
        print(f"   Tweets returned: {search_data.get('tweets_returned', 0)}")
    
    # Test 4: Export
    print("\n4️⃣ Testing CSV export...")
    if tweet_data.get("success"):
        csv_file = scraper.export_to_csv(tweet_data, "test_tweet.csv")
        print(f"   CSV file: {csv_file}")
    
    print(f"\n📊 Total API calls: {scraper.daily_call_count}")
    print("\n✅ Twitter Scraper Test Complete!")

if __name__ == "__main__":
    main()