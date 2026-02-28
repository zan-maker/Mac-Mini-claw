#!/usr/bin/env python3
"""
Reddit Scraper Integration - YARS Edition
Using YARS (Yet Another Reddit Scraper) - NO API KEYS REQUIRED!
Repository: https://github.com/datavorous/yars
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import requests

class RedditScraperYARS:
    """Integration with YARS Reddit scraper (no API keys required)"""
    
    def __init__(self, cache_dir: str = None, use_proxies: bool = False):
        
        self.cache_dir = cache_dir or "/Users/cubiczan/.openclaw/workspace/cache/reddit_yars"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # YARS paths
        self.yars_path = "/Users/cubiczan/.openclaw/workspace/yars-reddit-scraper"
        self.src_path = os.path.join(self.yars_path, "src")
        
        # Rate limiting (important for no-API scraping)
        self.last_call_time = 0
        self.min_call_interval = 3.0  # 3 seconds between calls (avoid IP ban)
        self.daily_call_count = 0
        self.max_daily_calls = 500  # Conservative limit for no-API scraping
        
        # Proxies (optional, for IP rotation)
        self.use_proxies = use_proxies
        self.proxies = self._get_proxies() if use_proxies else None
        
        # User agents for rotation
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        # Load daily stats
        self._load_daily_stats()
        
        # Check YARS installation
        self._check_yars_installation()
    
    def scrape_subreddit(self, subreddit: str, category: str = "hot", 
                        limit: int = 100, time_filter: str = "all") -> Dict[str, Any]:
        """Scrape posts from a subreddit using YARS"""
        
        # Check cache first
        cache_key = f"subreddit_{subreddit}_{category}_{limit}_{time_filter}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                
                # Check if cache is fresh (less than 1 hour old)
                cache_time = datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))
                if (datetime.now() - cache_time).total_seconds() < 3600:
                    print(f"📄 Using cached subreddit data for r/{subreddit}")
                    return cached["data"]
            except:
                pass
        
        # Check rate limits
        if not self._check_rate_limits():
            return {"error": "Rate limit reached", "subreddit": subreddit}
        
        print(f"📊 Scraping r/{subreddit} ({category}, limit: {limit}, time: {time_filter})")
        
        try:
            # Import YARS
            sys.path.insert(0, self.src_path)
            from yars import YARS
            
            # Initialize YARS scraper
            miner = YARS()
            
            # Fetch posts
            posts = miner.fetch_subreddit_posts(
                subreddit=subreddit,
                limit=limit,
                category=category,
                time_filter=time_filter
            )
            
            # Convert to our format
            formatted_posts = self._format_yars_posts(posts, subreddit)
            
            data = {
                "success": True,
                "subreddit": subreddit,
                "category": category,
                "limit": limit,
                "time_filter": time_filter,
                "total_posts": len(formatted_posts),
                "posts": formatted_posts,
                "timestamp": datetime.now().isoformat(),
                "source": "yars"
            }
            
            # Cache the result
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            # Update stats
            self._update_call_stats()
            
            return data
            
        except Exception as e:
            print(f"❌ YARS error for r/{subreddit}: {e}")
            
            # Fallback to direct Reddit JSON API
            return self._fallback_scrape_subreddit(subreddit, category, limit, time_filter)
    
    def search_reddit(self, query: str, limit: int = 100, 
                     sort: str = "relevance", time_filter: str = "all") -> Dict[str, Any]:
        """Search Reddit using YARS"""
        
        # Check cache first
        cache_key = f"search_{hash(query)}_{limit}_{sort}_{time_filter}"
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
        
        print(f"🔍 Searching Reddit for '{query}' (limit: {limit}, sort: {sort})")
        
        try:
            # Import YARS
            sys.path.insert(0, self.src_path)
            from yars import YARS
            
            # Initialize YARS scraper
            miner = YARS()
            
            # Search Reddit
            results = miner.search_reddit(
                query=query,
                limit=limit
            )
            
            # Convert to our format
            formatted_posts = self._format_yars_posts(results, "search")
            
            data = {
                "success": True,
                "query": query,
                "limit": limit,
                "sort": sort,
                "time_filter": time_filter,
                "total_results": len(formatted_posts),
                "results": formatted_posts,
                "timestamp": datetime.now().isoformat(),
                "source": "yars"
            }
            
            # Cache the result
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            # Update stats
            self._update_call_stats()
            
            return data
            
        except Exception as e:
            print(f"❌ YARS search error: {e}")
            
            # Fallback to direct Reddit JSON API
            return self._fallback_search_reddit(query, limit, sort, time_filter)
    
    def scrape_user(self, username: str, limit: int = 100) -> Dict[str, Any]:
        """Scrape user data using YARS"""
        
        # Check cache first
        cache_key = f"user_{username}_{limit}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                
                # Check if cache is fresh (less than 6 hours old)
                cache_time = datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))
                if (datetime.now() - cache_time).total_seconds() < 21600:
                    print(f"📄 Using cached user data for u/{username}")
                    return cached["data"]
            except:
                pass
        
        # Check rate limits
        if not self._check_rate_limits():
            return {"error": "Rate limit reached", "username": username}
        
        print(f"👤 Scraping u/{username} (limit: {limit})")
        
        try:
            # Import YARS
            sys.path.insert(0, self.src_path)
            from yars import YARS
            
            # Initialize YARS scraper
            miner = YARS()
            
            # Scrape user data
            user_data = miner.scrape_user_data(
                username=username,
                limit=limit
            )
            
            # Convert to our format
            formatted_data = self._format_yars_user_data(user_data, username)
            
            data = {
                "success": True,
                "username": username,
                "limit": limit,
                "user_data": formatted_data,
                "timestamp": datetime.now().isoformat(),
                "source": "yars"
            }
            
            # Cache the result
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            # Update stats
            self._update_call_stats()
            
            return data
            
        except Exception as e:
            print(f"❌ YARS user error: {e}")
            return {
                "success": False,
                "username": username,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def scrape_post_details(self, post_url: str) -> Dict[str, Any]:
        """Scrape detailed post information including comments"""
        
        # Extract post ID from URL
        import re
        post_id_match = re.search(r'/comments/([^/]+)', post_url)
        if not post_id_match:
            return {
                "success": False,
                "post_url": post_url,
                "error": "Invalid Reddit post URL",
                "timestamp": datetime.now().isoformat()
            }
        
        post_id = post_id_match.group(1)
        
        # Check cache first
        cache_key = f"post_{post_id}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                
                # Check if cache is fresh (less than 1 hour old)
                cache_time = datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))
                if (datetime.now() - cache_time).total_seconds() < 3600:
                    print(f"📄 Using cached post data for {post_id}")
                    return cached["data"]
            except:
                pass
        
        # Check rate limits
        if not self._check_rate_limits():
            return {"error": "Rate limit reached", "post_url": post_url}
        
        print(f"📝 Scraping post details: {post_id}")
        
        try:
            # Import YARS
            sys.path.insert(0, self.src_path)
            from yars import YARS
            
            # Initialize YARS scraper
            miner = YARS()
            
            # Extract permalink from URL
            permalink = post_url.split('reddit.com')[1] if 'reddit.com' in post_url else post_url
            
            # Scrape post details
            post_details = miner.scrape_post_details(permalink)
            
            if post_details:
                data = {
                    "success": True,
                    "post_id": post_id,
                    "post_url": post_url,
                    "details": post_details,
                    "timestamp": datetime.now().isoformat(),
                    "source": "yars"
                }
                
                # Cache the result
                cache_data = {
                    "timestamp": datetime.now().isoformat(),
                    "data": data
                }
                
                with open(cache_file, 'w') as f:
                    json.dump(cache_data, f, indent=2)
                
                # Update stats
                self._update_call_stats()
                
                return data
            else:
                return {
                    "success": False,
                    "post_url": post_url,
                    "error": "Failed to scrape post details",
                    "timestamp": datetime.now().isoformat()
                }
            
        except Exception as e:
            print(f"❌ YARS post error: {e}")
            return {
                "success": False,
                "post_url": post_url,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def find_business_leads(self, keywords: List[str], subreddits: List[str] = None, 
                           limit_per_sub: int = 50) -> Dict[str, Any]:
        """Find business leads on Reddit based on keywords"""
        
        if not subreddits:
            # Default business-related subreddits
            subreddits = [
                "smallbusiness", "entrepreneur", "startups", "business",
                "marketing", "sales", "SideProject", "EntrepreneurRideAlong",
                "advancedentrepreneur", "SaaS", "ecommerce", "digitalnomad"
            ]
        
        all_leads = []
        
        for subreddit in subreddits:
            print(f"🔍 Searching r/{subreddit} for business leads...")
            
            # Get hot posts from subreddit
            subreddit_data = self.scrape_subreddit(
                subreddit=subreddit,
                category="hot",
                limit=limit_per_sub,
                time_filter="week"
            )
            
            if subreddit_data.get("success"):
                posts = subreddit_data.get("posts", [])
                
                # Filter posts by keywords
                for post in posts:
                    post_text = f"{post.get('title', '')} {post.get('selftext', '')}".lower()
                    
                    # Check if any keyword is in post
                    for keyword in keywords:
                        if keyword.lower() in post_text:
                            # Enrich as lead
                            lead = self._enrich_as_lead(post, keyword, subreddit)
                            all_leads.append(lead)
                            break  # Don't add same post multiple times
            
            # Respect rate limits
            time.sleep(3)
        
        # Sort by relevance/score
        all_leads.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return {
            "success": True,
            "keywords": keywords,
            "subreddits": subreddits,
            "total_leads": len(all_leads),
            "leads": all_leads,
            "timestamp": datetime.now().isoformat(),
            "source": "yars_reddit_scraper"
        }
    
    def find_investment_leads(self, limit_per_sub: int = 30) -> Dict[str, Any]:
        """Find investment-related leads on Reddit"""
        
        investment_subreddits = [
            "investing", "stocks", "wallstreetbets", "options",
            "pennystocks", "ValueInvesting", "SecurityAnalysis",
            "financialindependence", "fatFIRE", "realestateinvesting"
        ]
        
        investment_keywords = [
            "invest", "stock", "trade", "portfolio", "dividend",
            "ETF", "mutual fund", "401k", "IRA", "retirement",
            "real estate", "property", "mortgage", "loan",
            "funding", "capital", "venture", "angel", "seed",
            "acquisition", "merger", "IPO", "public offering"
        ]
        
        return self.find_business_leads(
            keywords=investment_keywords,
            subreddits=investment_subreddits,
            limit_per_sub=limit_per_sub
        )
    
    def find_section125_leads(self, limit_per_sub: int = 30) -> Dict[str, Any]:
        """Find Section 125 wellness plan leads on Reddit"""
        
        section125_subreddits = [
            "smallbusiness", "entrepreneur", "humanresources", "hr",
            "healthinsurance", "benefits", "personalfinance", "financialplanning"
        ]
        
        section125_keywords = [
            "section 125", "cafeteria plan", "flexible spending",
            "FSA", "HSA", "employee benefits", "health benefits",
            "wellness program", "pre-tax benefits", "tax advantage",
            "healthcare plan", "benefits package", "HR benefits"
        ]
        
        return self.find_business_leads(
            keywords=section125_keywords,
            subreddits=section125_subreddits,
            limit_per_sub=limit_per_sub
        )
    
    def _format_yars_posts(self, yars_posts: List[Dict], source: str) -> List[Dict[str, Any]]:
        """Convert YARS post format to our standard format"""
        formatted_posts = []
        
        for post in yars_posts:
            formatted = {
                "id": post.get("id", ""),
                "title": post.get("title", ""),
                "author": post.get("author", ""),
                "subreddit": post.get("subreddit", source),
                "score": post.get("score", 0),
                "upvote_ratio": post.get("upvote_ratio", 0.0),
                "num_comments": post.get("num_comments", 0),
                "created_utc": post.get("created_utc", 0),
                "permalink": f"https://reddit.com{post.get('permalink', '')}",
                "url": post.get("url", ""),
                "selftext": post.get("selftext", ""),
                "is_self": post.get("is_self", False),
                "over_18": post.get("over_18", False),
                "spoiler": post.get("spoiler", False),
                "thumbnail_url": post.get("thumbnail_url", ""),
                "image_url": post.get("image_url", ""),
                "source": "yars"
            }
            formatted_posts.append(formatted)
        
        return formatted_posts
    
    def _format_yars_user_data(self, user_data: Dict, username: str) -> Dict[str, Any]:
        """Convert YARS user data to our standard format"""
        formatted = {
            "username": username,
            "total_posts": len(user_data.get("posts", [])),
            "total_comments": len(user_data.get("comments", [])),
            "posts": self._format_yars_posts(user_data.get("posts", []), f"user_{username}"),
            "comments": user_data.get("comments", []),
            "timestamp": datetime.now().isoformat()
        }
        return formatted
    
    def _enrich_as_lead(self, post: Dict[str, Any], keyword: str, subreddit: str) -> Dict[str, Any]:
        """Enrich a Reddit post as a business lead"""
        
        lead = post.copy()
        
        # Add lead-specific fields
        lead["lead_type"] = "reddit_business_lead"
        lead["keyword_matched"] = keyword
        lead["subreddit_source"] = subreddit
        lead["relevance_score"] = self._calculate_relevance_score(post, keyword)
        lead["contact_potential"] = self._estimate_contact_potential(post)
        lead["business_indicators"] = self._extract_business_indicators(post)
        lead["enriched_timestamp"] = datetime.now().isoformat()
        
        return lead
    
    def _calculate_relevance_score(self, post: Dict[str, Any], keyword: str) -> float:
        """Calculate relevance score for lead"""
        score = 0.0
        
        # Base score for having keyword
        score += 0.3
        
        # Higher score for more engagement
        score += min(post.get("score", 0) / 1000, 0.3)  # Max 0.3 for high engagement
        
        # Score for comments (discussion potential)
        score += min(post.get("num_comments", 0) / 500, 0.2)  # Max 0.2 for many comments
        
        # Score for recency (newer is better)
        created_time = post.get("created_utc", 0)
        if created_time:
            age_days = (time.time() - created_time) / 86400
            if age_days < 1:
                score += 0.2  # Less than 1 day old
            elif age_days < 7:
                score += 0.1  # Less than 1 week old
        
        # Cap at 1.0
        return min(1.0, score)
    
    def _estimate_contact_potential(self, post: Dict[str, Any]) -> float:
        """Estimate potential for making contact"""
        potential = 0.0
        
        # Has author (not deleted)
        if post.get("author") and post["author"] != "[deleted]":
            potential += 0.4
        
        # Has substantial content
        text_length = len(f"{post.get('title', '')} {post.get('selftext', '')}")
        if text_length > 100:
            potential += 0.3
        
        # Recent activity
        created_time = post.get("created_utc", 0)
        if created_time and (time.time() - created_time) < 604800:  # 1 week
            potential += 0.2
        
        # Engagement (more engagement = more active user)
        if post.get("num_comments", 0) > 0:
            potential += 0.1
        
        return min(1.0, potential)
    
    def _extract_business_indicators(self, post: Dict[str, Any]) -> List[str]:
        """Extract business-related indicators from post"""
        indicators = []
        
        text = f"{post.get('title', '')} {post.get('selftext', '')}".lower()
        
        business_terms = [
            "business", "company", "startup", "entrepreneur",
            "product", "service", "customer", "client",
            "revenue", "profit", "sales", "marketing",
            "funding", "investment", "investor", "VC",
            "hiring", "team", "co-founder", "CEO",
            "launch", "release", "beta", "alpha"
        ]
        
        for term in business_terms:
            if term in text:
                indicators.append(term)
        
        return indicators
    
    def _fallback_scrape_subreddit(self, subreddit: str, category: str, 
                                  limit: int, time_filter: str) -> Dict[str, Any]:
        """Fallback method using Reddit's public JSON API"""
        
        print(f"🔄 Using fallback method for r/{subreddit}")
        
        try:
            # Build Reddit JSON URL
            base_url = f"https://www.reddit.com/r/{subreddit}/{category}.json"
            params = {
                "limit": min(limit, 100),  # Reddit API max is 100 per request
                "t": time_filter
            }
            
            # Make request with headers
            headers = {
                "User-Agent": self.user_agents[0]
            }
            
            response = requests.get(base_url, params=params, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get("data", {}).get("children", [])
                
                formatted_posts = []
                for post_data in posts[:limit]:
                    post = post_data.get("data", {})
                    formatted = {
                        "id": post.get("id", ""),
                        "title": post.get("title", ""),
                        "author": post.get("author", ""),
                        "subreddit": post.get("subreddit", subreddit),
                        "score": post.get("score", 0),
                        "upvote_ratio": post.get("upvote_ratio", 0.0),
                        "num_comments": post.get("num_comments", 0),
                        "created_utc": post.get("created_utc", 0),
                        "permalink": f"https://reddit.com{post.get('permalink', '')}",
                        "url": post.get("url", ""),
                        "selftext": post.get("selftext", ""),
                        "is_self": post.get("is_self", False),
                        "over_18": post.get("over_18", False),
                        "spoiler": post.get("spoiler", False),
                        "thumbnail_url": post.get("thumbnail", ""),
                        "source": "reddit_json_api"
                    }
                    formatted_posts.append(formatted)
                
                result = {
                    "success": True,
                    "subreddit": subreddit,
                    "category": category,
                    "limit": len(formatted_posts),
                    "time_filter": time_filter,
                    "total_posts": len(formatted_posts),
                    "posts": formatted_posts,
                    "timestamp": datetime.now().isoformat(),
                    "source": "reddit_json_fallback"
                }
                
                return result
            else:
                return {
                    "success": False,
                    "subreddit": subreddit,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"❌ Fallback error: {e}")
            return {
                "success": False,
                "subreddit": subreddit,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _fallback_search_reddit(self, query: str, limit: int, 
                               sort: str, time_filter: str) -> Dict[str, Any]:
        """Fallback search using Reddit's public JSON API"""
        
        print(f"🔄 Using fallback search for '{query}'")
        
        try:
            # Build Reddit search URL
            encoded_query = query.replace(" ", "%20")
            base_url = f"https://www.reddit.com/search.json"
            params = {
                "q": encoded_query,
                "limit": min(limit, 100),
                "sort": sort,
                "t": time_filter
            }
            
            # Make request with headers
            headers = {
                "User-Agent": self.user_agents[1]
            }
            
            response = requests.get(base_url, params=params, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get("data", {}).get("children", [])
                
                formatted_posts = []
                for post_data in posts[:limit]:
                    post = post_data.get("data", {})
                    formatted = {
                        "id": post.get("id", ""),
                        "title": post.get("title", ""),
                        "author": post.get("author", ""),
                        "subreddit": post.get("subreddit", ""),
                        "score": post.get("score", 0),
                        "upvote_ratio": post.get("upvote_ratio", 0.0),
                        "num_comments": post.get("num_comments", 0),
                        "created_utc": post.get("created_utc", 0),
                        "permalink": f"https://reddit.com{post.get('permalink', '')}",
                        "url": post.get("url", ""),
                        "selftext": post.get("selftext", ""),
                        "is_self": post.get("is_self", False),
                        "over_18": post.get("over_18", False),
                        "spoiler": post.get("spoiler", False),
                        "thumbnail_url": post.get("thumbnail", ""),
                        "source": "reddit_json_api"
                    }
                    formatted_posts.append(formatted)
                
                result = {
                    "success": True,
                    "query": query,
                    "limit": len(formatted_posts),
                    "sort": sort,
                    "time_filter": time_filter,
                    "total_results": len(formatted_posts),
                    "results": formatted_posts,
                    "timestamp": datetime.now().isoformat(),
                    "source": "reddit_json_fallback"
                }
                
                return result
            else:
                return {
                    "success": False,
                    "query": query,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"❌ Fallback search error: {e}")
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _check_yars_installation(self):
        """Check if YARS is properly installed"""
        yars_init = os.path.join(self.src_path, "yars", "__init__.py")
        
        if not os.path.exists(yars_init):
            print(f"⚠️  YARS not found at {self.src_path}")
            print("   Repository cloned, but may need installation")
            print("   Run: cd /Users/cubiczan/.openclaw/workspace/yars-reddit-scraper && pip install -e .")
            return False
        
        # Check for dependencies
        try:
            import requests
            print("✅ Requests library available")
        except ImportError:
            print("⚠️  Requests not installed. Install with: pip install requests")
        
        return True
    
    def _get_proxies(self) -> List[Dict[str, str]]:
        """Get proxy list for IP rotation (optional)"""
        # This would be populated with actual proxy servers
        # For now, return empty list
        return []
    
    def _check_rate_limits(self) -> bool:
        """Check if we can make another API call"""
        current_time = time.time()
        
        # Check minimum interval (important for no-API scraping)
        if current_time - self.last_call_time < self.min_call_interval:
            time_to_wait = self.min_call_interval - (current_time - self.last_call_time)
            print(f"⏳ Waiting {time_to_wait:.1f}s to avoid IP ban...")
            time.sleep(time_to_wait)
        
        # Check daily limit
        if self.daily_call_count >= self.max_daily_calls:
            print(f"⚠️  Daily limit reached ({self.max_daily_calls} calls)")
            return False
        
        return True
    
    def _update_call_stats(self):
        """Update call statistics"""
        self.last_call_time = time.time()
        self.daily_call_count += 1
        self._save_daily_stats()
        
        print(f"📊 Reddit calls today: {self.daily_call_count}/{self.max_daily_calls}")
    
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
    
    def export_leads_to_csv(self, leads_data: Dict[str, Any], filename: str = None):
        """Export leads to CSV file"""
        import csv
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reddit_yars_leads_{timestamp}.csv"
        
        filepath = os.path.join(self.cache_dir, filename)
        
        leads = leads_data.get("leads", [])
        if not leads:
            print("❌ No leads to export")
            return None
        
        # Define CSV fields for leads
        fieldnames = [
            "id", "title", "author", "subreddit", "score", "num_comments",
            "created_utc", "permalink", "keyword_matched", "relevance_score",
            "contact_potential", "business_indicators", "timestamp"
        ]
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for lead in leads:
                    row = {
                        "id": lead.get("id", ""),
                        "title": lead.get("title", ""),
                        "author": lead.get("author", ""),
                        "subreddit": lead.get("subreddit_source", lead.get("subreddit", "")),
                        "score": lead.get("score", 0),
                        "num_comments": lead.get("num_comments", 0),
                        "created_utc": lead.get("created_utc", 0),
                        "permalink": lead.get("permalink", ""),
                        "keyword_matched": lead.get("keyword_matched", ""),
                        "relevance_score": lead.get("relevance_score", 0),
                        "contact_potential": lead.get("contact_potential", 0),
                        "business_indicators": ", ".join(lead.get("business_indicators", [])),
                        "timestamp": lead.get("enriched_timestamp", datetime.now().isoformat())
                    }
                    writer.writerow(row)
            
            print(f"✅ Exported {len(leads)} leads to {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error exporting to CSV: {e}")
            return None


# Test the integration
def test_yars_integration():
    """Test YARS Reddit scraper integration"""
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
    
    print(f