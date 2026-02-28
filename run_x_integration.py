#!/usr/bin/env python3
"""
Run X (Twitter) Integration System
"""

import os
import json
import requests
import time
from datetime import datetime, timedelta

class XIntegration:
    """Simple X API integration"""
    
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"
        self.headers = {"Authorization": f"Bearer {bearer_token}"}
    
    def search_tweets(self, query, max_results=10):
        """Search for tweets"""
        print(f"🔍 Searching: '{query}'...")
        
        params = {
            "query": f"{query} -is:retweet",
            "max_results": min(max_results, 10),
            "tweet.fields": "created_at,public_metrics",
            "user.fields": "username,name"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/tweets/search/recent",
                headers=self.headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                tweets = data.get("data", [])
                print(f"✅ Found {len(tweets)} tweets")
                return tweets
            else:
                print(f"❌ Search failed: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def get_trending_insights(self):
        """Get business trending insights"""
        print("📈 Getting business trends...")
        
        business_queries = [
            "business automation",
            "lead generation", 
            "AI marketing",
            "SMB growth",
            "digital transformation"
        ]
        
        all_trends = []
        
        for query in business_queries[:2]:  # Limit to 2 queries
            tweets = self.search_tweets(query, max_results=5)
            
            if tweets:
                for tweet in tweets:
                    trend = {
                        "topic": query,
                        "sample": tweet.get("text", "")[:100],
                        "engagement": tweet.get("public_metrics", {}).get("like_count", 0),
                        "time": tweet.get("created_at", "")
                    }
                    all_trends.append(trend)
            
            time.sleep(1)  # Rate limiting
        
        return all_trends

def main():
    """Main function"""
    print("🚀 X (Twitter) Integration Setup")
    print("="*60)
    
    # Load config
    config_path = "/Users/cubiczan/.openclaw/workspace/config/social_media_config.json"
    
    if not os.path.exists(config_path):
        print("❌ Config file not found")
        return
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    bearer_token = config.get("platforms", {}).get("twitter_x", {}).get("credentials", {}).get("bearer_token", "")
    
    if not bearer_token:
        print("❌ Bearer Token not found in config")
        print("\nPlease add your Bearer Token to the config file:")
        print('''"twitter_x": {
  "enabled": true,
  "method": "api",
  "credentials": {
    "bearer_token": "AAAAAAAAAAAAAAAAAAAAALPN7QEAAAAAE%2FzdYiwIFUznOIq0AMuGfm9XiTQ%3DqG2GS41y1x6BScR90xrbkzrK3eOmijtefTzuJtrkfQgt2kkQxT"
  }
}''')
        return
    
    print(f"✅ Bearer Token loaded")
    
    # Initialize
    x_api = XIntegration(bearer_token)
    
    # Test the API
    print("\n🧪 Testing X API...")
    test_tweets = x_api.search_tweets("business automation", max_results=3)
    
    if test_tweets:
        print("✅ X API is WORKING!")
        print(f"   Found {len(test_tweets)} tweets about business automation")
        
        # Get trends
        print("\n📊 Getting business trends...")
        trends = x_api.get_trending_insights()
        
        if trends:
            print(f"✅ Found {len(trends)} trending insights")
            
            # Save results
            results_dir = "/Users/cubiczan/.openclaw/workspace/results"
            os.makedirs(results_dir, exist_ok=True)
            
            results = {
                "timestamp": datetime.now().isoformat(),
                "bearer_token_valid": True,
                "test_tweets_count": len(test_tweets),
                "trending_insights": trends,
                "integration_status": "active"
            }
            
            results_file = os.path.join(results_dir, "x_integration_results.json")
            with open(results_file, "w") as f:
                json.dump(results, f, indent=2)
            
            print(f"\n📁 Results saved to: {results_file}")
            
            # Update social media config
            print("\n🔗 Updating social media configuration...")
            
            # Enable Twitter/X if not already enabled
            if not config["platforms"]["twitter_x"].get("enabled", False):
                config["platforms"]["twitter_x"]["enabled"] = True
                print("   ✅ Twitter/X enabled in social media system")
            
            # Ensure Bearer Token is saved
            config["platforms"]["twitter_x"]["credentials"]["bearer_token"] = bearer_token
            
            # Save updated config
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            
            print("   ✅ Configuration updated")
            
            # Create sample content
            print("\n💡 Creating sample content...")
            sample_content = []
            
            for i, trend in enumerate(trends[:3], 1):
                content = {
                    "platform": "twitter",
                    "type": "trending_topic",
                    "content": f"Interesting discussion on {trend['topic']}:\n\n{trend['sample']}\n\nWhat are your thoughts? #Business #Trending",
                    "hashtags": ["#" + trend["topic"].replace(" ", ""), "#Business", "#Trending"],
                    "engagement_estimate": trend.get("engagement", 0)
                }
                sample_content.append(content)
            
            # Add generic posts
            generic_posts = [
                {
                    "platform": "twitter",
                    "type": "question",
                    "content": "What's your biggest challenge with lead generation right now?\n\n#LeadGeneration #Business #Marketing",
                    "hashtags": ["#LeadGeneration", "#Business", "#Marketing"],
                    "engagement_estimate": 50
                },
                {
                    "platform": "twitter", 
                    "type": "tip",
                    "content": "Tip: Automating lead qualification can save 10+ hours/week.\n\nWhat's your favorite automation tool?\n\n#Automation #BusinessTips",
                    "hashtags": ["#Automation", "#BusinessTips", "#Productivity"],
                    "engagement_estimate": 75
                }
            ]
            
            sample_content.extend(generic_posts)
            
            # Save sample content
            content_file = os.path.join(results_dir, "x_sample_content.json")
            with open(content_file, "w") as f:
                json.dump(sample_content, f, indent=2)
            
            print(f"   ✅ Created {len(sample_content)} sample posts")
            print(f"   📁 Saved to: {content_file}")
            
            # Final summary
            print("\n" + "="*60)
            print("🎯 X INTEGRATION COMPLETE!")
            print("="*60)
            
            print(f"\n✅ Bearer Token: VALID")
            print(f"✅ API Access: WORKING")
            print(f"✅ Social Media Integration: ACTIVE")
            print(f"✅ Sample Content: READY ({len(sample_content)} posts)")
            print(f"✅ Configuration: UPDATED")
            
            print("\n🚀 Ready for:")
            print("   • Content discovery")
            print("   • Trend monitoring")
            print("   • Competitor analysis")
            print("   • Social media posting")
            
            print("\n📋 Next steps:")
            print("   1. Test Instagram/Facebook posting")
            print("   2. Set up daily automation")
            print("   3. Integrate with HubSpot CRM")
            print("   4. Monitor analytics")
            
        else:
            print("⚠️  Could not get trends, but API is working")
    
    else:
        print("❌ X API test failed")
        print("   Bearer Token may be invalid or have limited permissions")

if __name__ == "__main__":
    main()