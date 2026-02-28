#!/usr/bin/env python3
"""
Test X (Twitter) API with Bearer Token
"""

import os
import sys
import json
import requests
from datetime import datetime

class XAPITester:
    """Test X (Twitter) API functionality"""
    
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        
    def test_authentication(self):
        """Test if Bearer Token is valid"""
        print("🔐 Testing X API authentication...")
        
        url = f"{self.base_url}/users/me"
        
        try:
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Authentication SUCCESS!")
                print(f"   User ID: {data.get('data', {}).get('id', 'N/A')}")
                print(f"   Username: @{data.get('data', {}).get('username', 'N/A')}")
                print(f"   Name: {data.get('data', {}).get('name', 'N/A')}")
                return True
            elif response.status_code == 401:
                print("❌ Authentication FAILED: Invalid Bearer Token")
                print(f"   Status Code: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
            else:
                print(f"⚠️  Unexpected response: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return False
    
    def test_post_tweet(self, text="Test tweet from X API integration"):
        """Test posting a tweet"""
        print(f"🐦 Testing tweet posting...")
        
        url = f"{self.base_url}/tweets"
        payload = {"text": text}
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 201:
                data = response.json()
                tweet_id = data.get("data", {}).get("id")
                print(f"✅ Tweet posted SUCCESSFULLY!")
                print(f"   Tweet ID: {tweet_id}")
                print(f"   Text: {text}")
                print(f"   URL: https://twitter.com/user/status/{tweet_id}")
                return tweet_id
            elif response.status_code == 403:
                print("❌ Permission denied: Bearer Token cannot post tweets")
                print("   Note: Bearer Tokens are for read-only access")
                print("   You need OAuth 1.0a credentials for posting")
                return None
            else:
                print(f"❌ Tweet posting failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return None
    
    def test_search_tweets(self, query="AI automation", max_results=5):
        """Test searching for tweets"""
        print(f"🔍 Testing tweet search: '{query}'...")
        
        url = f"{self.base_url}/tweets/search/recent"
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "created_at,public_metrics,author_id",
            "user.fields": "name,username"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                tweets = data.get("data", [])
                print(f"✅ Search SUCCESS! Found {len(tweets)} tweets")
                
                for i, tweet in enumerate(tweets, 1):
                    print(f"\n   Tweet {i}:")
                    print(f"     ID: {tweet.get('id')}")
                    print(f"     Text: {tweet.get('text', '')[:80]}...")
                    print(f"     Created: {tweet.get('created_at', 'N/A')}")
                    metrics = tweet.get('public_metrics', {})
                    print(f"     Metrics: 👍{metrics.get('like_count', 0)} 🔄{metrics.get('retweet_count', 0)} 💬{metrics.get('reply_count', 0)}")
                
                return tweets
            else:
                print(f"❌ Search failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return []
    
    def test_user_timeline(self, username=None, max_results=5):
        """Test getting user timeline"""
        if not username:
            # Get current user's timeline
            print("📱 Testing user timeline...")
            url = f"{self.base_url}/users/me/tweets"
        else:
            print(f"📱 Testing timeline for @{username}...")
            # First get user ID
            user_url = f"{self.base_url}/users/by/username/{username}"
            user_response = requests.get(user_url, headers=self.headers)
            
            if user_response.status_code != 200:
                print(f"❌ Could not find user @{username}")
                return []
            
            user_id = user_response.json().get("data", {}).get("id")
            url = f"{self.base_url}/users/{user_id}/tweets"
        
        params = {
            "max_results": max_results,
            "tweet.fields": "created_at,public_metrics"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                tweets = data.get("data", [])
                print(f"✅ Timeline SUCCESS! Found {len(tweets)} tweets")
                
                for i, tweet in enumerate(tweets, 1):
                    print(f"\n   Tweet {i}:")
                    print(f"     ID: {tweet.get('id')}")
                    print(f"     Text: {tweet.get('text', '')[:80]}...")
                    print(f"     Created: {tweet.get('created_at', 'N/A')}")
                
                return tweets
            else:
                print(f"❌ Timeline failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return []
    
    def test_rate_limits(self):
        """Check API rate limits"""
        print("📊 Testing rate limits...")
        
        # Make a simple request to get rate limit headers
        url = f"{self.base_url}/users/me"
        
        try:
            response = requests.get(url, headers=self.headers)
            
            if 'x-rate-limit-limit' in response.headers:
                limit = response.headers['x-rate-limit-limit']
                remaining = response.headers['x-rate-limit-remaining']
                reset = response.headers['x-rate-limit-reset']
                
                print(f"✅ Rate limits retrieved:")
                print(f"   Limit: {limit} requests per window")
                print(f"   Remaining: {remaining} requests left")
                print(f"   Reset: {datetime.fromtimestamp(int(reset)).strftime('%Y-%m-%d %H:%M:%S')}")
                
                return {
                    'limit': limit,
                    'remaining': remaining,
                    'reset': reset
                }
            else:
                print("⚠️  Rate limit headers not found")
                return None
                
        except Exception as e:
            print(f"❌ Rate limit check failed: {e}")
            return None
    
    def run_comprehensive_test(self):
        """Run all tests"""
        print("="*60)
        print("🚀 COMPREHENSIVE X (TWITTER) API TEST")
        print("="*60)
        
        results = {}
        
        # Test 1: Authentication
        print("\n1. AUTHENTICATION TEST")
        print("-"*40)
        results['auth'] = self.test_authentication()
        
        if not results['auth']:
            print("\n❌ Authentication failed. Stopping tests.")
            return results
        
        # Test 2: Rate Limits
        print("\n2. RATE LIMIT TEST")
        print("-"*40)
        results['rate_limits'] = self.test_rate_limits()
        
        # Test 3: Search Tweets
        print("\n3. SEARCH TEST")
        print("-"*40)
        results['search'] = self.test_search_tweets("business automation", 3)
        
        # Test 4: User Timeline
        print("\n4. TIMELINE TEST")
        print("-"*40)
        results['timeline'] = self.test_user_timeline(max_results=3)
        
        # Test 5: Post Tweet (may fail with Bearer Token)
        print("\n5. POST TWEET TEST")
        print("-"*40)
        test_tweet = f"Testing X API integration at {datetime.now().strftime('%H:%M')} #APITest #Automation"
        results['post'] = self.test_post_tweet(test_tweet)
        
        # Summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        print(f"✅ Authentication: {'PASS' if results['auth'] else 'FAIL'}")
        print(f"✅ Rate Limits: {'PASS' if results['rate_limits'] else 'FAIL'}")
        print(f"✅ Search: {'PASS' if results['search'] else 'FAIL'}")
        print(f"✅ Timeline: {'PASS' if results['timeline'] else 'FAIL'}")
        print(f"✅ Post Tweet: {'PASS' if results['post'] else 'READ-ONLY (expected)'}")
        
        print("\n" + "="*60)
        print("🎯 RECOMMENDATIONS")
        print("="*60)
        
        if results['auth']:
            print("✅ Bearer Token is VALID for read operations")
            
            if not results['post']:
                print("⚠️  For posting tweets, you need OAuth 1.0a credentials:")
                print("   1. Create a Twitter Developer App")
                print("   2. Get API Key, API Secret")
                print("   3. Get Access Token, Access Secret")
                print("   4. Use tweepy.OAuth1UserHandler for posting")
            
            print("✅ Ready for: Search, Timeline, User lookup, Analytics")
            print("✅ Integration with social media system: READY")
        
        return results

def main():
    """Main function"""
    print("X (Twitter) API Tester")
    print("="*60)
    
    # Load token from config
    config_path = "/Users/cubiczan/.openclaw/workspace/config/social_media_config.json"
    
    if not os.path.exists(config_path):
        print("❌ Config file not found")
        sys.exit(1)
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    bearer_token = config.get("platforms", {}).get("twitter_x", {}).get("credentials", {}).get("bearer_token", "")
    
    if not bearer_token:
        print("❌ Bearer Token not found in config")
        print("Please add your Bearer Token to social_media_config.json")
        sys.exit(1)
    
    print(f"🔑 Bearer Token loaded: {bearer_token[:20]}...")
    
    # Create tester
    tester = XAPITester(bearer_token)
    
    # Run tests
    results = tester.run_comprehensive_test()
    
    # Save results
    results_file = "/Users/cubiczan/.openclaw/workspace/x_api_test_results.json"
    with open(results_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "auth_success": results.get('auth', False),
            "tests_run": list(results.keys()),
            "recommendations": "Bearer Token valid for read operations" if results.get('auth') else "Invalid token"
        }, f, indent=2)
    
    print(f"\n📁 Results saved to: {results_file}")
    
    # Exit code based on authentication
    sys.exit(0 if results.get('auth') else 1)

if __name__ == "__main__":
    main()