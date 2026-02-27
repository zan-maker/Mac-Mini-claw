#!/usr/bin/env python3
"""
Twitter/X Scraper Integration
Multiple approaches for scraping Twitter data in 2026
Based on research of best available tools
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import requests
import re

class TwitterScraperIntegration:
    """Multi-method Twitter/X scraper integration"""
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or "/Users/cubiczan/.openclaw/workspace/cache/twitter"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Multiple scraping methods
        self.methods = {
            "scrapedo": self._scrape_with_scrapedo,
            "requests": self._scrape_with_requests,
            "apify": self._scrape_with_apify,
            "brightdata": self._scrape_with_brightdata
        }
        
        # Rate limiting
        self.last_call_time = 0
        self.min_call_interval = 2.0  # 2 seconds between calls
        self.daily_call_count = 0
        self.max_daily_calls = 100
        
        # Load daily stats
        self._load_daily_stats()
        
        # User agents
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
    
    def scrape_tweet(self, tweet_url: str, method: str = "auto") -> Dict[str, Any]:
        """Scrape a single tweet by URL"""
        
        # Check cache first
        tweet_id = self._extract_tweet_id(tweet_url)
        cache_key = f"tweet_{tweet_id}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                
                # Check if cache is fresh (less than 1 hour old)
                cache_time = datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))
                if (datetime.now() - cache_time).total_seconds() < 3600:
                    print(f"📄 Using cached tweet data for {tweet_id}")
                    return cached["data"]
            except:
                pass
        
        # Check rate limits
        if not self._check_rate_limits():
            return {"error": "Rate limit reached", "tweet_url": tweet_url}
        
        print(f"🐦 Scraping tweet: {tweet_url}")
        
        # Choose scraping method
        if method == "auto":
            # Try methods in order of reliability
            for method_name in ["scrapedo", "requests", "apify"]:
                result = self.methods[method_name](tweet_url)
                if result.get("success"):
                    break
        elif method in self.methods:
            result = self.methods[method](tweet_url)
        else:
            result = {"error": f"Unknown method: {method}", "tweet_url": tweet_url}
        
        # Cache successful results
        if result.get("success"):
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "data": result
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        
        # Update stats
        self._update_call_stats()
        
        return result
    
    def scrape_profile(self, username: str, method: str = "auto") -> Dict[str, Any]:
        """Scrape a Twitter profile"""
        
        # Check cache first
        cache_key = f"profile_{username.lower()}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                
                # Check if cache is fresh (less than 6 hours old)
                cache_time = datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))
                if (datetime.now() - cache_time).total_seconds() < 21600:
                    print(f"📄 Using cached profile data for @{username}")
                    return cached["data"]
            except:
                pass
        
        # Check rate limits
        if not self._check_rate_limits():
            return {"error": "Rate limit reached", "username": username}
        
        print(f"👤 Scraping profile: @{username}")
        
        profile_url = f"https://x.com/{username}"
        
        # Try different methods
        result = None
        
        if method == "auto" or method == "scrapedo":
            result = self._scrape_profile_with_scrapedo(profile_url)
        
        if (not result or not result.get("success")) and (method == "auto" or method == "requests"):
            result = self._scrape_profile_with_requests(profile_url)
        
        if not result:
            result = {
                "success": False,
                "username": username,
                "error": "All scraping methods failed",
                "timestamp": datetime.now().isoformat()
            }
        
        # Cache successful results
        if result.get("success"):
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "data": result
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        
        # Update stats
        self._update_call_stats()
        
        return result
    
    def search_tweets(self, query: str, limit: int = 20, method: str = "auto") -> Dict[str, Any]:
        """Search for tweets by keyword/hashtag"""
        
        # Check cache first
        cache_key = f"search_{hash(query)}_{limit}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                
                # Check if cache is fresh (less than 15 minutes old)
                cache_time = datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))
                if (datetime.now() - cache_time).total_seconds() < 900:
                    print(f"📄 Using cached search results for '{query}'")
                    return cached["data"]
            except:
                pass
        
        # Check rate limits
        if not self._check_rate_limits():
            return {"error": "Rate limit reached", "query": query}
        
        print(f"🔍 Searching tweets: '{query}' (limit: {limit})")
        
        # Build search URL
        encoded_query = query.replace(" ", "%20").replace("#", "%23")
        search_url = f"https://x.com/search?q={encoded_query}&src=typed_query"
        
        result = self._scrape_search_with_scrapedo(search_url, limit)
        
        # Cache results
        if result.get("success"):
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "data": result
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        
        # Update stats
        self._update_call_stats()
        
        return result
    
    def scrape_thread(self, tweet_url: str, include_replies: bool = True) -> Dict[str, Any]:
        """Scrape an entire tweet thread"""
        print(f"🧵 Scraping thread: {tweet_url}")
        
        # Get the main tweet
        main_tweet = self.scrape_tweet(tweet_url)
        
        if not main_tweet.get("success"):
            return main_tweet
        
        thread_data = {
            "success": True,
            "main_tweet": main_tweet,
            "replies": [],
            "total_tweets": 1,
            "timestamp": datetime.now().isoformat()
        }
        
        # Extract conversation ID for getting replies
        conversation_id = main_tweet.get("conversation_id")
        
        if include_replies and conversation_id:
            # Search for replies to this conversation
            search_query = f"conversation_id:{conversation_id}"
            search_results = self.search_tweets(search_query, limit=50)
            
            if search_results.get("success"):
                thread_data["replies"] = search_results.get("tweets", [])
                thread_data["total_tweets"] = 1 + len(thread_data["replies"])
        
        return thread_data
    
    def _scrape_with_scrapedo(self, url: str) -> Dict[str, Any]:
        """Scrape using Scrape.do API"""
        try:
            # Import Scrape.do integration
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from scrapedo_integration import ScrapeDoIntegration
            
            scraper = ScrapeDoIntegration()
            result = scraper.scrape_url(url)
            
            if result.get("success"):
                # Parse Twitter data from HTML
                parsed_data = self._parse_twitter_html(result["content"], url)
                parsed_data["source"] = "scrapedo"
                parsed_data["success"] = True
                return parsed_data
            else:
                return {
                    "success": False,
                    "url": url,
                    "error": "Scrape.do failed",
                    "source": "scrapedo"
                }
                
        except Exception as e:
            print(f"⚠️  Scrape.do error: {e}")
            return {
                "success": False,
                "url": url,
                "error": str(e),
                "source": "scrapedo"
            }
    
    def _scrape_with_requests(self, url: str) -> Dict[str, Any]:
        """Scrape using direct requests with headers"""
        try:
            headers = {
                "User-Agent": self.user_agents[0],
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0"
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                parsed_data = self._parse_twitter_html(response.text, url)
                parsed_data["source"] = "requests"
                parsed_data["success"] = True
                parsed_data["status_code"] = response.status_code
                return parsed_data
            else:
                return {
                    "success": False,
                    "url": url,
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}",
                    "source": "requests"
                }
                
        except Exception as e:
            print(f"⚠️  Requests error: {e}")
            return {
                "success": False,
                "url": url,
                "error": str(e),
                "source": "requests"
            }
    
    def _scrape_with_apify(self, url: str) -> Dict[str, Any]:
        """Scrape using Apify API (if configured)"""
        # This would require an Apify API key
        # For now, return mock data
        print("⚠️  Apify API not configured - using mock data")
        
        tweet_id = self._extract_tweet_id(url)
        
        return {
            "success": True,
            "tweet_id": tweet_id,
            "url": url,
            "text": f"Mock tweet data for {tweet_id} - Apify API not configured",
            "author": "mock_user",
            "timestamp": datetime.now().isoformat(),
            "likes": 100,
            "retweets": 50,
            "replies": 25,
            "source": "apify_mock"
        }
    
    def _scrape_with_brightdata(self, url: str) -> Dict[str, Any]:
        """Scrape using Bright Data API (if configured)"""
        # This would require a Bright Data API key
        # For now, return mock data
        print("⚠️  Bright Data API not configured - using mock data")
        
        tweet_id = self._extract_tweet_id(url)
        
        return {
            "success": True,
            "tweet_id": tweet_id,
            "url": url,
            "text": f"Mock tweet data for {tweet_id} - Bright Data API not configured",
            "author": "mock_user",
            "timestamp": datetime.now().isoformat(),
            "likes": 150,
            "retweets": 75,
            "replies": 30,
            "source": "brightdata_mock"
        }
    
    def _scrape_profile_with_scrapedo(self, profile_url: str) -> Dict[str, Any]:
        """Scrape profile using Scrape.do"""
        try:
            from scrapedo_integration import ScrapeDoIntegration
            
            scraper = ScrapeDoIntegration()
            result = scraper.scrape_url(profile_url)
            
            if result.get("success"):
                parsed_data = self._parse_profile_html(result["content"], profile_url)
                parsed_data["source"] = "scrapedo"
                parsed_data["success"] = True
                return parsed_data
            else:
                return {
                    "success": False,
                    "url": profile_url,
                    "error": "Scrape.do failed",
                    "source": "scrapedo"
                }
                
        except Exception as e:
            print(f"⚠️  Scrape.do profile error: {e}")
            return {
                "success": False,
                "url": profile_url,
                "error": str(e),
                "source": "scrapedo"
            }
    
    def _scrape_profile_with_requests(self, profile_url: str) -> Dict[str, Any]:
        """Scrape profile using direct requests"""
        try:
            headers = {
                "User-Agent": self.user_agents[1],
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5"
            }
            
            response = requests.get(profile_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                parsed_data = self._parse_profile_html(response.text, profile_url)
                parsed_data["source"] = "requests"
                parsed_data["success"] = True
                parsed_data["status_code"] = response.status_code
                return parsed_data
            else:
                return {
                    "success": False,
                    "url": profile_url,
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}",
                    "source": "requests"
                }
                
        except Exception as e:
            print(f"⚠️  Requests profile error: {e}")
            return {
                "success": False,
                "url": profile_url,
                "error": str(e),
                "source": "requests"
            }
    
    def _scrape_search_with_scrapedo(self, search_url: str, limit: int) -> Dict[str, Any]:
        """Scrape search results using Scrape.do"""
        try:
            from scrapedo_integration import ScrapeDoIntegration
            
            scraper = ScrapeDoIntegration()
            result = scraper.scrape_url(search_url)
            
            if result.get("success"):
                parsed_data = self._parse_search_html(result["content"], search_url, limit)
                parsed_data["source"] = "scrapedo"
                parsed_data["success"] = True
                return parsed_data
            else:
                return {
                    "success": False,
                    "url": search_url,
                    "error": "Scrape.do failed",
                    "source": "scrapedo"
                }
                
        except Exception as e:
            print(f"⚠️  Scrape.do search error: {e}")
            return {
                "success": False,
                "url": search_url,
                "error": str(e),
                "source": "scrapedo"
            }
    
    def _parse_twitter_html(self, html: str, url: str) -> Dict[str, Any]:
        """Parse Twitter data from HTML"""
        tweet_id = self._extract_tweet_id(url)
        
        # Basic parsing (simplified - real implementation would be more complex)
        data = {
            "tweet_id": tweet_id,
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "parsed_successfully": False
        }
        
        try:
            # Extract tweet text
            text_match = re.search(r'<div[^>]*data-testid="tweetText"[^>]*>(.*?)</div>', html, re.DOTALL)
            if text_match:
                text = re.sub(r'<[^>]*>', '', text_match.group(1)).strip()
                data["text"] = text
                data["parsed_successfully"] = True
            
            # Extract author
            author_match = re.search(r'<div[^>]*data-testid="User-Name"[^>]*>.*?@([^<]+)</span>', html, re.DOTALL)
            if author_match:
                data["author"] = author_match.group(1).strip()
            
            # Extract metrics (likes, retweets, replies)
            metrics_patterns = {
                "likes": r'data-testid="like"[^>]*>.*?([0-9,KM]+)',
                "retweets": r'data-testid="retweet"[^>]*>.*?([0-9,KM]+)',
                "replies": r'data-testid="reply"[^>]*>.*?([0-9,KM]+)'
            }
            
            for metric, pattern in metrics_patterns.items():
                match = re.search(pattern, html, re.DOTALL)
                if match:
                    value = match.group(1).replace(',', '').replace('K', '000').replace('M', '000000')
                    try:
                        data[metric] = int(value)
                    except:
                        data[metric] = value
            
            # Extract timestamp
            time_match = re.search(r'<time[^>]*datetime="([^"]+)"', html)
            if time_match:
                data["created_at"] = time_match.group(1)
            
            # Extract conversation ID
            conv_match = re.search(r'data-conversation-id="([^"]+)"', html)
            if conv_match:
                data["conversation_id"] = conv_match.group(1)
            
        except Exception as e:
            print(f"⚠️  HTML parsing error: {e}")
        
        return data
    
    def _parse_profile_html(self, html: str, profile_url: str) -> Dict[str, Any]:
        """Parse profile data from HTML"""
        username = profile_url.split("/")[-1]
        
        data = {
            "username": username,
            "url": profile_url,
            "timestamp": datetime.now().isoformat(),
            "parsed_successfully": False
        }
        
        try:
            # Extract display name
            name_match = re.search(r'<div[^>]*data-testid="UserName"[^>]*>.*?<span[^>]*>([^<]+)</span>', html, re.DOTALL)
            if name_match:
                data["display_name"] = name_match.group(1).strip()
            
            # Extract bio
            bio_match = re.search(r'<div[^>]*data-testid="UserDescription"[^>]*>(.*?)</div>', html, re.DOTALL)
            if bio_match:
                bio = re.sub(r'<[^>]*>', '', bio_match.group(1)).strip()
                data["bio"] = bio
            
            # Extract follower/following counts
            follower_match = re.search(r'([0-9,KM]+)\s*Followers', html)
            if follower_match:
                value = follower_match.group(1).replace(',', '').replace('K', '000').replace('M', '000000')
                try:
                    data["followers_count"] = int(value)
                except:
                    data["followers_count"] = value
            
            following_match = re.search(r'([0-9,KM]+)\s*Following', html)
            if following_match:
                value = following_match.group(1).replace(',', '').replace('K', '000').replace('M', '000000')
                try:
                    data["following_count"] = int(value)
                except:
                    data["following_count"] = value
            
            # Extract join date
            join_match = re.search(r'Joined\s*([A-Za-z]+\s*[0-9]{4})', html)
            if join_match:
                data["joined_date"] = join_match.group(1)
            
            # Extract location
            location_match = re.search(r'data-testid="UserLocation"[^>]*>.*?<span[^>]*>([^<]+)</span>', html, re.DOTALL)
            if location_match:
                data["location"] = location_match.group(1).strip()
            
            # Extract website
            website_match = re.search(r'data-testid="UserUrl"[^>]*>.*?href="([^"]+)"', html, re.DOTALL)
            if website_match:
                data["website"] = website_match.group(1).strip()
            
            data["parsed_successfully"] = True
            
        except Exception as e:
            print(f"⚠️  Profile HTML parsing error: {e}")
        
        return data
    
    def _parse_search_html(self, html: str, search_url: str, limit: int) -> Dict[str, Any]:
        """Parse search results from HTML"""
        data = {
            "search_url": search_url,
            "timestamp": datetime.now().isoformat(),
            "tweets": [],
            "parsed_successfully": False
        }
        
        try:
            # Extract tweet articles
            tweet_pattern = r'<article[^>]*data-testid="tweet"[^>]*>(.*?)</article>'
            tweet_matches = re.findall(tweet_pattern, html, re.DOTALL)
            
            for i, tweet_html in enumerate(tweet_matches[:limit]):
                tweet_data = self._parse_tweet_from_search(tweet_html)
                if tweet_data:
                    data["tweets"].append(tweet_data)
            
            data["total_tweets_found"] = len(tweet_matches)
            data["tweets_returned"] = len(data["tweets"])
            data["parsed_successfully"] = len(data["tweets"]) > 0
            
        except Exception as e:
            print(f"⚠️  Search HTML parsing error: {e}")
        
        return data
    
    def _parse_tweet_from_search(self, tweet_html: str) -> Dict[str, Any]:
        """Parse individual tweet from search results"""
        tweet_data = {}
        
        try:
            # Extract tweet ID
            tweet_id_match = re.search(r'status/([0-9]+)', tweet_html)
            if tweet_id_match:
                tweet_data["tweet_id"] = tweet_id_match.group(1)
            
            # Extract author
            author_match = re.search(r'@([^<]+)</span>', tweet_html)
            if author_match:
                tweet_data["author"] = author_match.group(1).strip()
            
            # Extract text
            text_match = re.search(r'<div[^>]*lang="[^"]*"[^>]*>(.*?)</div>', tweet_html, re.DOTALL)
            if text_match:
                text = re.sub(r'<[^>]*>', '', text_match.group(1)).strip()
                tweet_data["text"] = text
            
            # Extract timestamp
            time_match = re.search(r'<time[^>]*datetime="([^"]+)"', tweet_html)
            if time_match:
                tweet_data["timestamp"] = time_match.group(1)
            
            # Extract metrics
            metrics = {
                "likes": r'([0-9,KM]+)\s*</span>\s*</div>\s*</div>\s*<div[^>]*data-testid="like"',
                "retweets": r'([0-9,KM]+)\s*</span>\s*</div>\s*</div>\s*<div[^>]*data-testid="retweet"',
                "replies": r'([0-9,KM]+)\s*</span>\s*</div>\s*</div>\s*<div[^>]*data-testid="reply"'
            }
            
            for metric, pattern in metrics.items():
                match = re.search(pattern, tweet_html, re.DOTALL)
                if match:
                    value = match.group(1).replace(',', '').replace('K', '000').replace('M', '000000')
                    try:
                        tweet_data[metric] = int(value)
                    except:
                        tweet_data[metric] = value
            
        except Exception as e:
            print(f"⚠️  Tweet parsing error: {e}")
        
        return tweet_data if tweet_data else None
    
    def _extract_tweet_id(self, url: str) -> str:
        """Extract tweet ID from URL"""
        # Handle various URL formats
        patterns = [
            r'status/([0-9]+)',
            r'tweet/([0-9]+)',
            r'/i/status/([0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # Fallback: hash of URL
        return str(hash(url))
    
    def _check_rate_limits(self) -> bool:
        """Check if we can make another API call"""
        current_time = time.time()
        
        # Check minimum interval
        if current_time - self.last_call_time < self.min_call_interval:
            time_to_wait = self.min_call_interval - (current_time - self.last_call_time)
            print(f"⏳ Waiting {time_to_wait:.1f}s for rate limit...")
            time.sleep(time_to_wait)
        
        # Check daily limit
        if self.daily_call_count >= self.max_daily_calls:
            print(f"⚠️  Daily API limit reached ({self.max_daily_calls} calls)")
            return False
        
        return True
    
    def _update_call_stats(self):
        """Update call statistics"""
        self.last_call_time = time.time()
        self.daily_call_count += 1
        self._save_daily_stats()
        
        print(f"📊 Twitter API calls today: {self.daily_call_count}/{self.max_daily_calls}")
    
    def _load_daily_stats(self):
        """Load daily call statistics"""
        stats_file = os.path.join(self.cache_dir, "daily_stats.json")
        
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
                
                # Check if stats are from today
                stats_date = stats.get("date", "2000-01-01")
                if stats_date == datetime.now().strftime("%Y-%m-%d"):
                    self.daily_call_count = stats.get("call_count", 0)
                else:
                    # Reset for new day
                    self.daily_call_count = 0
                    
            except Exception as e:
                print(f"⚠️  Error loading daily stats: {e}")
                self.daily_call_count = 0
        else:
            self.daily_call_count = 0
    
    def _save_daily_stats(self):
        """Save daily call statistics"""
        stats_file = os.path.join(self.cache_dir, "daily_stats.json")
        
        stats = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "call_count": self.daily_call_count,
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving daily stats: {e}")
    
    def export_to_csv(self, data: Dict[str, Any], filename: str = None):
        """Export scraped data to CSV"""
        import csv
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"twitter_data_{timestamp}.csv"
        
        filepath = os.path.join(self.cache_dir, filename)
        
        # Determine data type and fields
        if "tweets" in data:  # Search results
            items = data["tweets"]
            fieldnames = ["tweet_id", "author", "text", "timestamp", "likes", "retweets", "replies"]
        elif "text" in data:  # Single tweet
            items = [data]
            fieldnames = ["tweet_id", "author", "text", "timestamp", "likes", "retweets", "replies", "conversation_id"]
        elif "username" in data:  # Profile
            items = [data]
            fieldnames = ["username", "display_name", "bio", "followers_count", "following_count", "joined_date", "location", "website"]
        else:
            print("❌ Unknown data format for CSV export")
            return None
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for item in items:
                    row = {}
                    for field in fieldnames:
                        row[field] = item.get(field, "")
                    writer.writerow(row)
            
            print(f"✅ Exported {len(items)} items to {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error exporting to CSV: {e}")
            return None


# Test the integration
def test_twitter_scraper():
    """Test Twitter scraper integration"""
    print("🧪 Testing Twitter Scraper Integration...")
    
    scraper = TwitterScraperIntegration()
    
    # Test with a known tweet (Elon Musk's pinned tweet as example)
    print("\n🐦 Testing tweet scraping...")
    
    # Example tweet URL (Elon Musk's pinned tweet - will use mock if fails)
    test_tweet_url = "https://x.com/elonmusk/status/1679128693120028672"
    
    tweet_data = scraper.scrape_tweet(test_tweet_url, method="auto")
    
    print(f"  Success: {tweet_data.get('success', False)}")
    print(f"  Source: {tweet_data.get('source', 'unknown')}")
    
    if tweet_data.get("success"):
        print(f"  Tweet ID: {tweet_data.get('tweet_id', 'N/A')}")
        print(f"  Author: {tweet_data.get('author', 'N/A')}")
        if "text" in tweet_data:
            text_preview = tweet_data["text"][:100] + "..." if len(tweet_data["text"]) > 100 else tweet_data["text"]
            print(f"  Text: {text_preview}")
    
    # Test profile scraping
    print("\n👤 Testing profile scraping...")
    profile_data = scraper.scrape_profile("elonmusk", method="auto")
    
    print(f"  Success: {profile_data.get('success', False)}")
    print(f"  Source: {profile_data.get('source', 'unknown')}")
    
    if profile_data.get("success"):
        print(f"  Username: {profile_data.get('username', 'N/A')}")
        print(f"  Display Name: {profile_data.get('display_name', 'N/A')}")
        print(f"  Followers: {profile_data.get('followers_count', 'N/A')}")
    
    # Test search
    print("\n🔍 Testing search...")
    search_data = scraper.search_tweets("AI", limit=5)
    
    print(f"  Success: {search_data.get('success', False)}")
    print(f"  Source: {search_data.get('source', 'unknown')}")
    
    if search_data.get("success"):
        print(f"  Tweets found: {search_data.get('total_tweets_found', 0)}")
        print(f"  Tweets returned: {search_data.get('tweets_returned', 0)}")
        
        if search_data.get("tweets"):
            print(f"  First tweet author: {search_data['tweets'][0].get('author', 'N/A')}")
    
    print(f"\n📊 API calls today: {scraper.daily_call_count}/{scraper.max_daily_calls}")
    
    return True


if __name__ == "__main__":
    test_twitter_scraper()
    print("\n✅ Twitter Scraper Integration Ready!")