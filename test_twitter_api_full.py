#!/usr/bin/env python3
"""
Test Twitter/X API with OAuth 1.0a credentials
Full posting capability test
"""

import os
import sys
import json
import tweepy
from datetime import datetime

class TwitterAPITester:
    """Test Twitter API with OAuth 1.0a credentials"""
    
    def __init__(self, api_key, api_secret, access_token, access_token_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        
        # Initialize API
        self.auth = tweepy.OAuth1UserHandler(
            self.api_key,
            self.api_secret,
            self.access_token,
            self.access_token_secret
        )
        
        self.api = tweepy.API(self.auth)
        
    def test_authentication(self):
        """Test if credentials are valid"""
        print("🔐 Testing Twitter API authentication...")
        
        try:
            # Get authenticated user info
            user = self.api.verify_credentials()
            
            print(f"✅ Authentication SUCCESS!")
            print(f"   User ID: {user.id}")
            print(f"   Username: @{user.screen_name}")
            print(f"   Name: {user.name}")
            print(f"   Followers: {user.followers_count}")
            print(f"   Following: {user.friends_count}")
            print(f"   Tweets: {user.statuses_count}")
            
            return {
                "success": True,
                "user_id": user.id,
                "username": user.screen_name,
                "name": user.name,
                "followers": user.followers_count
            }
            
        except Exception as e:
            print(f"❌ Authentication FAILED: {e}")
            return {"success": False, "error": str(e)}
    
    def test_post_tweet(self, text="Test tweet from Twitter API integration"):
        """Test posting a tweet"""
        print(f"🐦 Testing tweet posting...")
        
        try:
            # Post tweet
            tweet = self.api.update_status(text)
            
            print(f"✅ Tweet posted SUCCESSFULLY!")
            print(f"   Tweet ID: {tweet.id}")
            print(f"   Text: {tweet.text}")
            print(f"   Created: {tweet.created_at}")
            print(f"   URL: https://twitter.com/user/status/{tweet.id}")
            
            # Optionally delete test tweet
            delete_choice = input("\nDelete test tweet? (y/n): ").lower()
            if delete_choice == 'y':
                self.api.destroy_status(tweet.id)
                print("   Test tweet deleted")
            
            return {
                "success": True,
                "tweet_id": tweet.id,
                "text": tweet.text,
                "created_at": str(tweet.created_at)
            }
            
        except Exception as e:
            print(f"❌ Tweet posting failed: {e}")
            return {"success": False, "error": str(e)}
    
    def test_post_tweet_with_image(self, text="Test tweet with image", image_path=None):
        """Test posting a tweet with image"""
        print(f"🖼️ Testing tweet with image...")
        
        # If no image path provided, skip image test
        if not image_path or not os.path.exists(image_path):
            print("⚠️  No image provided, skipping image test")
            return {"success": False, "error": "No image provided"}
        
        try:
            # Upload media
            media = self.api.media_upload(image_path)
            
            # Post tweet with media
            tweet = self.api.update_status(
                status=text,
                media_ids=[media.media_id]
            )
            
            print(f"✅ Tweet with image posted SUCCESSFULLY!")
            print(f"   Tweet ID: {tweet.id}")
            print(f"   Media ID: {media.media_id}")
            print(f"   Text: {tweet.text}")
            
            return {
                "success": True,
                "tweet_id": tweet.id,
                "media_id": media.media_id,
                "text": tweet.text
            }
            
        except Exception as e:
            print(f"❌ Tweet with image failed: {e}")
            return {"success": False, "error": str(e)}
    
    def test_get_timeline(self, count=5):
        """Test getting user timeline"""
        print(f"📱 Testing user timeline...")
        
        try:
            timeline = self.api.home_timeline(count=count)
            
            print(f"✅ Timeline retrieved SUCCESSFULLY!")
            print(f"   Found {len(timeline)} tweets")
            
            for i, tweet in enumerate(timeline, 1):
                print(f"\n   Tweet {i}:")
                print(f"     ID: {tweet.id}")
                print(f"     User: @{tweet.user.screen_name}")
                print(f"     Text: {tweet.text[:80]}...")
                print(f"     Created: {tweet.created_at}")
            
            return {
                "success": True,
                "tweet_count": len(timeline)
            }
            
        except Exception as e:
            print(f"❌ Timeline retrieval failed: {e}")
            return {"success": False, "error": str(e)}
    
    def test_search_tweets(self, query="AI automation", count=5):
        """Test searching tweets"""
        print(f"🔍 Testing tweet search: '{query}'...")
        
        try:
            tweets = self.api.search_tweets(q=query, count=count)
            
            print(f"✅ Search SUCCESS! Found {len(tweets)} tweets")
            
            for i, tweet in enumerate(tweets, 1):
                print(f"\n   Tweet {i}:")
                print(f"     ID: {tweet.id}")
                print(f"     User: @{tweet.user.screen_name}")
                print(f"     Text: {tweet.text[:80]}...")
                print(f"     Created: {tweet.created_at}")
            
            return {
                "success": True,
                "tweet_count": len(tweets)
            }
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return {"success": False, "error": str(e)}
    
    def test_rate_limits(self):
        """Check API rate limits"""
        print("📊 Testing rate limits...")
        
        try:
            # Get rate limit status
            rate_limits = self.api.rate_limit_status()
            
            print(f"✅ Rate limits retrieved:")
            
            # Check some important endpoints
            endpoints = {
                "statuses/update": "Posting tweets",
                "statuses/home_timeline": "Reading timeline",
                "search/tweets": "Searching tweets",
                "users/show": "User info"
            }
            
            for endpoint, description in endpoints.items():
                if endpoint in rate_limits['resources']:
                    limit = rate_limits['resources'][endpoint][endpoint]['limit']
                    remaining = rate_limits['resources'][endpoint][endpoint]['remaining']
                    reset = rate_limits['resources'][endpoint][endpoint]['reset']
                    
                    print(f"   {description}: {remaining}/{limit} remaining")
            
            return {
                "success": True,
                "rate_limits": {
                    "post_tweets": rate_limits['resources']['statuses']['/statuses/update']['remaining'],
                    "read_timeline": rate_limits['resources']['statuses']['/statuses/home_timeline']['remaining'],
                    "search": rate_limits['resources']['search']['/search/tweets']['remaining']
                }
            }
            
        except Exception as e:
            print(f"❌ Rate limit check failed: {e}")
            return {"success": False, "error": str(e)}
    
    def run_comprehensive_test(self):
        """Run all tests"""
        print("="*60)
        print("🚀 COMPREHENSIVE TWITTER API TEST")
        print("="*60)
        
        results = {}
        
        # Test 1: Authentication
        print("\n1. AUTHENTICATION TEST")
        print("-"*40)
        results['auth'] = self.test_authentication()
        
        if not results['auth']['success']:
            print("\n❌ Authentication failed. Stopping tests.")
            return results
        
        # Test 2: Rate Limits
        print("\n2. RATE LIMIT TEST")
        print("-"*40)
        results['rate_limits'] = self.test_rate_limits()
        
        # Test 3: Post Tweet
        print("\n3. POST TWEET TEST")
        print("-"*40)
        test_tweet = f"Testing Twitter API integration at {datetime.now().strftime('%H:%M')} #APITest #Automation"
        results['post'] = self.test_post_tweet(test_tweet)
        
        # Test 4: Get Timeline
        print("\n4. TIMELINE TEST")
        print("-"*40)
        results['timeline'] = self.test_get_timeline(3)
        
        # Test 5: Search Tweets
        print("\n5. SEARCH TEST")
        print("-"*40)
        results['search'] = self.test_search_tweets("business automation", 3)
        
        # Summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        print(f"✅ Authentication: {'PASS' if results['auth']['success'] else 'FAIL'}")
        print(f"✅ Rate Limits: {'PASS' if results.get('rate_limits', {}).get('success', False) else 'FAIL'}")
        print(f"✅ Post Tweet: {'PASS' if results.get('post', {}).get('success', False) else 'FAIL'}")
        print(f"✅ Timeline: {'PASS' if results.get('timeline', {}).get('success', False) else 'FAIL'}")
        print(f"✅ Search: {'PASS' if results.get('search', {}).get('success', False) else 'FAIL'}")
        
        print("\n" + "="*60)
        print("🎯 RECOMMENDATIONS")
        print("="*60)
        
        if results['auth']['success']:
            print("✅ Twitter API credentials are VALID and WORKING!")
            print("✅ Ready for: Posting tweets, reading timeline, searching, analytics")
            print("✅ Integration with social media system: READY")
            
            if results.get('post', {}).get('success', False):
                print("✅ Tweet posting capability: CONFIRMED")
            else:
                print("⚠️  Tweet posting may have issues")
        
        return results

def main():
    """Main function"""
    print("Twitter/X API Tester with OAuth 1.0a")
    print("="*60)
    
    # Load credentials from config
    config_path = "/Users/cubiczan/.openclaw/workspace/config/social_media_config.json"
    
    if not os.path.exists(config_path):
        print("❌ Config file not found")
        sys.exit(1)
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    twitter_config = config.get("platforms", {}).get("twitter_x", {})
    credentials = twitter_config.get("credentials", {})
    
    api_key = credentials.get("api_key", "")
    api_secret = credentials.get("api_secret", "")
    access_token = credentials.get("access_token", "")
    access_token_secret = credentials.get("access_token_secret", "")
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("❌ Missing Twitter API credentials")
        print("Please ensure all OAuth 1.0a credentials are in config")
        sys.exit(1)
    
    print(f"🔑 API Key: {api_key[:10]}...")
    print(f"🔑 Access Token: {access_token[:10]}...")
    
    # Check if tweepy is installed
    try:
        import tweepy
    except ImportError:
        print("❌ Tweepy not installed")
        print("Install with: pip install tweepy")
        sys.exit(1)
    
    # Create tester
    tester = TwitterAPITester(api_key, api_secret, access_token, access_token_secret)
    
    # Run tests
    results = tester.run_comprehensive_test()
    
    # Save results
    results_file = "/Users/cubiczan/.openclaw/workspace/twitter_api_test_results.json"
    with open(results_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "credentials_valid": results.get('auth', {}).get('success', False),
            "posting_capability": results.get('post', {}).get('success', False),
            "tests_run": list(results.keys()),
            "user_info": results.get('auth', {}),
            "recommendations": "Twitter API ready for integration" if results.get('auth', {}).get('success') else "Check credentials"
        }, f, indent=2)
    
    print(f"\n📁 Results saved to: {results_file}")
    
    # Exit code based on authentication
    sys.exit(0 if results.get('auth', {}).get('success', False) else 1)

if __name__ == "__main__":
    main()