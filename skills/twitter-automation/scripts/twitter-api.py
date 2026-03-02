#!/usr/bin/env python3
"""
Twitter API Client for OpenClaw
Base client with rate limiting and error handling
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitterAPIClient:
    """Base Twitter API client with rate limiting"""
    
    def __init__(self, config_path: str = None):
        """Initialize client with configuration"""
        self.config = self._load_config(config_path)
        self.rate_limit_remaining = 450  # Default for Essential tier
        self.rate_limit_reset = 0
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests
        
    def _load_config(self, config_path: str) -> Dict:
        """Load Twitter configuration"""
        default_config = {
            "api_key": os.getenv("TWITTER_API_KEY", ""),
            "api_secret": os.getenv("TWITTER_API_SECRET", ""),
            "access_token": os.getenv("TWITTER_ACCESS_TOKEN", ""),
            "access_secret": os.getenv("TWITTER_ACCESS_SECRET", ""),
            "bearer_token": os.getenv("TWITTER_BEARER_TOKEN", ""),
            "rate_limit_delay": 1.0,
            "max_posts_per_day": 50,
            "auto_follow_back": False
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                default_config.update(file_config)
            except Exception as e:
                logger.warning(f"Failed to load config file: {e}")
        
        # Check for required credentials
        missing = []
        for key in ["bearer_token"]:
            if not default_config.get(key):
                missing.append(key)
        
        if missing:
            logger.warning(f"Missing Twitter credentials: {missing}")
            logger.info("Note: Full functionality requires Twitter API credentials")
            logger.info("Get credentials from: https://developer.twitter.com/")
        
        return default_config
    
    def _check_rate_limit(self):
        """Check and respect rate limits"""
        current_time = time.time()
        
        # Check minimum interval between requests
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        # Check Twitter API rate limits
        if self.rate_limit_remaining <= 10:
            reset_in = self.rate_limit_reset - current_time
            if reset_in > 0:
                logger.warning(f"Rate limit low ({self.rate_limit_remaining} remaining). Reset in {reset_in:.0f}s")
                if reset_in < 300:  # If reset is soon, wait
                    time.sleep(reset_in + 1)
        
        self.last_request_time = time.time()
    
    def _update_rate_limits(self, headers: Dict):
        """Update rate limit tracking from response headers"""
        if 'x-rate-limit-remaining' in headers:
            try:
                self.rate_limit_remaining = int(headers['x-rate-limit-remaining'])
            except:
                pass
        
        if 'x-rate-limit-reset' in headers:
            try:
                self.rate_limit_reset = int(headers['x-rate-limit-reset'])
            except:
                pass
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """Make HTTP request with rate limiting and error handling"""
        self._check_rate_limit()
        
        # This is a placeholder - actual implementation would use requests library
        # and make real API calls when credentials are available
        
        logger.info(f"[Placeholder] Would make {method} request to {endpoint}")
        logger.info(f"Parameters: {kwargs.get('params', {})}")
        
        # Simulate API response for development
        if endpoint == "users/me":
            return {
                "data": {
                    "id": "123456789",
                    "name": "Test User",
                    "username": "testuser"
                }
            }
        elif endpoint == "tweets" and method == "POST":
            return {
                "data": {
                    "id": "987654321",
                    "text": kwargs.get('json', {}).get('text', 'Test tweet')
                }
            }
        
        return None
    
    def get_user_profile(self, user_id: str = None, username: str = None) -> Optional[Dict]:
        """Get user profile information"""
        if user_id:
            endpoint = f"users/{user_id}"
        elif username:
            endpoint = f"users/by/username/{username}"
        else:
            endpoint = "users/me"  # Authenticated user
        
        return self._make_request("GET", endpoint)
    
    def create_tweet(self, text: str, **kwargs) -> Optional[Dict]:
        """Create a new tweet/post"""
        if len(text) > 280:
            logger.warning(f"Tweet text exceeds 280 characters: {len(text)}")
            # In real implementation, would truncate or split
        
        payload = {"text": text}
        
        # Add optional parameters
        if 'reply_to' in kwargs:
            payload['reply'] = {"in_reply_to_tweet_id": kwargs['reply_to']}
        
        if 'media_ids' in kwargs:
            payload['media'] = {"media_ids": kwargs['media_ids']}
        
        return self._make_request("POST", "tweets", json=payload)
    
    def search_tweets(self, query: str, max_results: int = 10, **kwargs) -> Optional[Dict]:
        """Search for recent tweets"""
        params = {
            "query": query,
            "max_results": min(max_results, 100)  # Twitter API limit
        }
        
        # Add optional parameters
        if 'start_time' in kwargs:
            params['start_time'] = kwargs['start_time']
        
        if 'end_time' in kwargs:
            params['end_time'] = kwargs['end_time']
        
        return self._make_request("GET", "tweets/search/recent", params=params)
    
    def like_tweet(self, tweet_id: str) -> Optional[Dict]:
        """Like a tweet"""
        user = self.get_user_profile()
        if not user or 'data' not in user:
            logger.error("Cannot like tweet: Unable to get user profile")
            return None
        
        user_id = user['data']['id']
        endpoint = f"users/{user_id}/likes"
        
        return self._make_request("POST", endpoint, json={"tweet_id": tweet_id})
    
    def retweet(self, tweet_id: str) -> Optional[Dict]:
        """Retweet a tweet"""
        user = self.get_user_profile()
        if not user or 'data' not in user:
            logger.error("Cannot retweet: Unable to get user profile")
            return None
        
        user_id = user['data']['id']
        endpoint = f"users/{user_id}/retweets"
        
        return self._make_request("POST", endpoint, json={"tweet_id": tweet_id})

def main():
    """Test the Twitter API client"""
    print("Twitter API Client Test")
    print("=" * 50)
    
    # Initialize client
    client = TwitterAPIClient()
    
    # Test getting user profile
    print("\n1. Getting user profile...")
    profile = client.get_user_profile()
    if profile:
        print(f"   User: {profile.get('data', {}).get('username', 'Unknown')}")
    
    # Test creating a tweet
    print("\n2. Creating test tweet...")
    tweet = client.create_tweet("Testing Twitter API client for OpenClaw #automation")
    if tweet:
        print(f"   Tweet created: {tweet.get('data', {}).get('id', 'Unknown')}")
    
    # Test searching tweets
    print("\n3. Searching tweets...")
    search = client.search_tweets("OpenClaw automation", max_results=5)
    if search:
        print(f"   Found {len(search.get('data', []))} tweets")
    
    print("\n" + "=" * 50)
    print("Note: This is a placeholder implementation.")
    print("To use real Twitter API, set up credentials:")
    print("1. Get Twitter Developer account")
    print("2. Create app at https://developer.twitter.com/")
    print("3. Set environment variables:")
    print("   - TWITTER_BEARER_TOKEN")
    print("   - TWITTER_API_KEY, TWITTER_API_SECRET")
    print("   - TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET")

if __name__ == "__main__":
    main()
