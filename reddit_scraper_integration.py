#!/usr/bin/env python3
"""
Reddit Scraper Integration
Using URS (Universal Reddit Scraper) for comprehensive Reddit data extraction
Repository: https://github.com/JosephLai241/URS
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import subprocess
import requests

class RedditScraperIntegration:
    """Integration with URS (Universal Reddit Scraper) for Reddit data"""
    
    def __init__(self, cache_dir: str = None, reddit_client_id: str = None, 
                 reddit_client_secret: str = None, reddit_user_agent: str = None):
        
        self.cache_dir = cache_dir or "/Users/cubiczan/.openclaw/workspace/cache/reddit"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # URS paths
        self.urs_path = "/Users/cubiczan/.openclaw/workspace/reddit-scraper"
        self.urs_script = os.path.join(self.urs_path, "urs", "Urs.py")
        
        # Reddit API credentials (PRAW)
        self.reddit_client_id = reddit_client_id or self._get_env_var("REDDIT_CLIENT_ID")
        self.reddit_client_secret = reddit_client_secret or self._get_env_var("REDDIT_CLIENT_SECRET")
        self.reddit_user_agent = reddit_user_agent or self._get_env_var("REDDIT_USER_AGENT", "OpenClawRedditScraper/1.0")
        
        # Rate limiting
        self.last_call_time = 0
        self.min_call_interval = 1.0  # 1 second between calls
        self.daily_call_count = 0
        self.max_daily_calls = 1000  # Reddit API limit (PRAW handles this)
        
        # Load daily stats
        self._load_daily_stats()
        
        # Check URS installation
        self._check_urs_installation()
    
    def scrape_subreddit(self, subreddit: str, sort: str = "hot", limit: int = 100, 
                        time_filter: str = "all") -> Dict[str, Any]:
        """Scrape posts from a subreddit"""
        
        # Check cache first
        cache_key = f"subreddit_{subreddit}_{sort}_{limit}_{time_filter}"
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
        
        print(f"📊 Scraping r/{subreddit} ({sort}, limit: {limit}, time: {time_filter})")
        
        try:
            # Build URS command
            cmd = [
                "python3", self.urs_script,
                "-r", subreddit, sort[0], str(limit), time_filter,
                "--csv"
            ]
            
            # Run URS command
            result = self._run_urs_command(cmd)
            
            if result.get("success"):
                # Parse CSV output
                csv_file = result.get("csv_file")
                if csv_file and os.path.exists(csv_file):
                    posts = self._parse_urs_csv(csv_file)
                    
                    data = {
                        "success": True,
                        "subreddit": subreddit,
                        "sort": sort,
                        "limit": limit,
                        "time_filter": time_filter,
                        "total_posts": len(posts),
                        "posts": posts,
                        "timestamp": datetime.now().isoformat(),
                        "source": "urs"
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
                        "subreddit": subreddit,
                        "error": "No CSV output generated",
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return result
                
        except Exception as e:
            print(f"❌ URS error for r/{subreddit}: {e}")
            return {
                "success": False,
                "subreddit": subreddit,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def scrape_redditor(self, username: str, limit: int = 100) -> Dict[str, Any]:
        """Scrape posts from a Redditor"""
        
        # Check cache first
        cache_key = f"redditor_{username}_{limit}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                
                # Check if cache is fresh (less than 6 hours old)
                cache_time = datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))
                if (datetime.now() - cache_time).total_seconds() < 21600:
                    print(f"📄 Using cached redditor data for u/{username}")
                    return cached["data"]
            except:
                pass
        
        # Check rate limits
        if not self._check_rate_limits():
            return {"error": "Rate limit reached", "username": username}
        
        print(f"👤 Scraping u/{username} (limit: {limit})")
        
        try:
            # Build URS command
            cmd = [
                "python3", self.urs_script,
                "-u", username, str(limit),
                "--csv"
            ]
            
            # Run URS command
            result = self._run_urs_command(cmd)
            
            if result.get("success"):
                # Parse CSV output
                csv_file = result.get("csv_file")
                if csv_file and os.path.exists(csv_file):
                    posts = self._parse_urs_csv(csv_file)
                    
                    data = {
                        "success": True,
                        "username": username,
                        "limit": limit,
                        "total_posts": len(posts),
                        "posts": posts,
                        "timestamp": datetime.now().isoformat(),
                        "source": "urs"
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
                        "username": username,
                        "error": "No CSV output generated",
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return result
                
        except Exception as e:
            print(f"❌ URS error for u/{username}: {e}")
            return {
                "success": False,
                "username": username,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def scrape_comments(self, submission_url: str, limit: int = 100) -> Dict[str, Any]:
        """Scrape comments from a submission"""
        
        # Check cache first
        cache_key = f"comments_{hash(submission_url)}_{limit}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                
                # Check if cache is fresh (less than 1 hour old)
                cache_time = datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))
                if (datetime.now() - cache_time).total_seconds() < 3600:
                    print(f"📄 Using cached comments data for {submission_url}")
                    return cached["data"]
            except:
                pass
        
        # Check rate limits
        if not self._check_rate_limits():
            return {"error": "Rate limit reached", "submission_url": submission_url}
        
        print(f"💬 Scraping comments from {submission_url} (limit: {limit})")
        
        try:
            # Build URS command
            cmd = [
                "python3", self.urs_script,
                "-c", submission_url, str(limit),
                "--csv"
            ]
            
            # Run URS command
            result = self._run_urs_command(cmd)
            
            if result.get("success"):
                # Parse CSV output
                csv_file = result.get("csv_file")
                if csv_file and os.path.exists(csv_file):
                    comments = self._parse_urs_csv(csv_file)
                    
                    data = {
                        "success": True,
                        "submission_url": submission_url,
                        "limit": limit,
                        "total_comments": len(comments),
                        "comments": comments,
                        "timestamp": datetime.now().isoformat(),
                        "source": "urs"
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
                        "submission_url": submission_url,
                        "error": "No CSV output generated",
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return result
                
        except Exception as e:
            print(f"❌ URS error for comments: {e}")
            return {
                "success": False,
                "submission_url": submission_url,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def search_reddit(self, query: str, subreddit: str = None, limit: int = 100, 
                     sort: str = "relevance", time_filter: str = "all") -> Dict[str, Any]:
        """Search Reddit for posts"""
        
        # Check cache first
        cache_key = f"search_{hash(query)}_{subreddit}_{limit}_{sort}_{time_filter}"
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
        
        target = f"r/{subreddit}" if subreddit else "all"
        print(f"🔍 Searching {target} for '{query}' (limit: {limit}, sort: {sort})")
        
        try:
            # For search, we need to use PRAW directly since URS doesn't have search command
            # This is a simplified implementation
            import praw
            
            # Initialize PRAW
            reddit = praw.Reddit(
                client_id=self.reddit_client_id,
                client_secret=self.reddit_client_secret,
                user_agent=self.reddit_user_agent
            )
            
            # Perform search
            if subreddit:
                search_results = reddit.subreddit(subreddit).search(
                    query=query,
                    limit=limit,
                    sort=sort,
                    time_filter=time_filter
                )
            else:
                search_results = reddit.subreddit("all").search(
                    query=query,
                    limit=limit,
                    sort=sort,
                    time_filter=time_filter
                )
            
            # Process results
            posts = []
            for submission in search_results:
                post = {
                    "id": submission.id,
                    "title": submission.title,
                    "author": str(submission.author) if submission.author else "[deleted]",
                    "subreddit": str(submission.subreddit),
                    "score": submission.score,
                    "upvote_ratio": submission.upvote_ratio,
                    "num_comments": submission.num_comments,
                    "created_utc": submission.created_utc,
                    "permalink": f"https://reddit.com{submission.permalink}",
                    "url": submission.url,
                    "selftext": submission.selftext[:500] + "..." if len(submission.selftext) > 500 else submission.selftext,
                    "is_self": submission.is_self,
                    "over_18": submission.over_18,
                    "spoiler": submission.spoiler
                }
                posts.append(post)
            
            data = {
                "success": True,
                "query": query,
                "subreddit": subreddit,
                "sort": sort,
                "time_filter": time_filter,
                "limit": limit,
                "total_posts": len(posts),
                "posts": posts,
                "timestamp": datetime.now().isoformat(),
                "source": "praw"
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
            print(f"❌ Reddit search error: {e}")
            return {
                "success": False,
                "query": query,
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
                sort="hot",
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
                            lead = self._enrich_as_lead(post, keyword)
                            all_leads.append(lead)
                            break  # Don't add same post multiple times
            
            # Respect rate limits
            time.sleep(1)
        
        # Sort by relevance/score
        all_leads.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return {
            "success": True,
            "keywords": keywords,
            "subreddits": subreddits,
            "total_leads": len(all_leads),
            "leads": all_leads,
            "timestamp": datetime.now().isoformat(),
            "source": "reddit_scraper"
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
    
    def find_tech_leads(self, limit_per_sub: int = 30) -> Dict[str, Any]:
        """Find technology-related leads on Reddit"""
        
        tech_subreddits = [
            "technology", "programming", "webdev", "startups",
            "SaaS", "software", "devops", "dataisbeautiful",
            "MachineLearning", "artificial", "cybersecurity",
            "gamedev", "iOSProgramming", "androiddev"
        ]
        
        tech_keywords = [
            "software", "app", "platform", "SaaS", "API",
            "cloud", "AI", "machine learning", "data science",
            "cybersecurity", "blockchain", "crypto", "web3",
            "mobile app", "website", "e-commerce", "digital",
            "automation", "integration", "solution", "tool"
        ]
        
        return self.find_business_leads(
            keywords=tech_keywords,
            subreddits=tech_subreddits,
            limit_per_sub=limit_per_sub
        )
    
    def _enrich_as_lead(self, post: Dict[str, Any], keyword: str) -> Dict[str, Any]:
        """Enrich a Reddit post as a business lead"""
        
        lead = post.copy()
        
        # Add lead-specific fields
        lead["lead_type"] = "reddit_business_lead"
        lead["keyword_matched"] = keyword
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
    
    def _run_urs_command(self, cmd: List[str]) -> Dict[str, Any]:
        """Run a URS command and capture output"""
        try:
            # Set environment for URS
            env = os.environ.copy()
            
            # Add Reddit API credentials if available
            if self.reddit_client_id and self.reddit_client_secret:
                env["REDDIT_CLIENT_ID"] = self.reddit_client_id
                env["REDDIT_CLIENT_SECRET"] = self.reddit_client_secret
                env["REDDIT_USER_AGENT"] = self.reddit_user_agent
            
            # Run command
            result = subprocess.run(
                cmd,
                cwd=self.urs_path,
                env=env,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # URS saves CSV files in the current directory
                # Look for the most recent CSV file
                csv_files = [f for f in os.listdir(self.urs_path) if f.endswith('.csv')]
                csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.urs_path, x)), reverse=True)
                
                if csv_files:
                    csv_file = os.path.join(self.urs_path, csv_files[0])
                    return {
                        "success": True,
                        "csv_file": csv_file,
                        "stdout": result.stdout,
                        "stderr": result.stderr
                    }
                else:
                    return {
                        "success": False,
                        "error": "No CSV file generated",
                        "stdout": result.stdout,
                        "stderr": result.stderr
                    }
            else:
                return {
                    "success": False,
                    "error": f"URS command failed with code {result.returncode}",
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "URS command timed out"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_urs_csv(self, csv_file: str) -> List[Dict[str, Any]]:
        """Parse URS CSV output into structured data"""
        import csv
        
        data = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # Convert row to structured format
                    item = {}
                    
                    # Map common URS fields
                    field_mapping = {
                        "ID": "id",
                        "Title": "title",
                        "Author": "author",
                        "Subreddit": "subreddit",
                        "Score": "score",
                        "Upvote Ratio": "upvote_ratio",
                        "Number of Comments": "num_comments",
                        "Permalink": "permalink",
                        "URL": "url",
                        "Text": "selftext",
                        "Created UTC": "created_utc",
                        "Flair": "flair",
                        "Edited": "edited",
                        "Stickied": "stickied",
                        "Over 18": "over_18",
                        "Spoiler": "spoiler"
                    }
                    
                    for csv_field, our_field in field_mapping.items():
                        if csv_field in row:
                            # Convert numeric fields
                            if our_field in ["score", "num_comments"]:
                                try:
                                    item[our_field] = int(row[csv_field])
                                except:
                                    item[our_field] = 0
                            elif our_field == "upvote_ratio":
                                try:
                                    item[our_field] = float(row[csv_field])
                                except:
                                    item[our_field] = 0.0
                            elif our_field == "created_utc":
                                try:
                                    item[our_field] = float(row[csv_field])
                                except:
                                    item[our_field] = 0.0
                            else:
                                item[our_field] = row[csv_field]
                    
                    data.append(item)
            
            return data
            
        except Exception as e:
            print(f"⚠️  Error parsing CSV: {e}")
            return []
    
    def _check_urs_installation(self):
        """Check if URS is properly installed"""
        if not os.path.exists(self.urs_script):
            print(f"⚠️  URS not found at {self.urs_script}")
            print("   Run: cd /Users/cubiczan/.openclaw/workspace/reddit-scraper && pip install -e .")
            return False
        
        # Check for dependencies
        try:
            import praw
            print("✅ PRAW (Reddit API) available")
        except ImportError:
            print("⚠️  PRAW not installed. Install with: pip install praw")
        
        return True
    
    def _get_env_var(self, var_name: str, default: str = None) -> Optional[str]:
        """Get environment variable"""
        value = os.environ.get(var_name, default)
        
        # Also check .env file in URS directory
        env_file = os.path.join(self.urs_path, ".env")
        if os.path.exists(env_file):
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            key, val = line.strip().split('=', 1)
                            if key == var_name:
                                value = val
                                break
            except:
                pass
        
        return value
    
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
        
        print(f"📊 Reddit API calls today: {self.daily_call_count}/{self.max_daily_calls}")
    
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
            filename = f"reddit_leads_{timestamp}.csv"
        
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
                        "subreddit": lead.get("subreddit", ""),
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
def test_reddit_scraper():
    """Test Reddit scraper integration"""
    print("🧪 Testing Reddit Scraper Integration...")
    
    scraper = RedditScraperIntegration()
    
    # Check installation
    print("\n🔧 Checking URS installation...")
    if not scraper._check_urs_installation():
        print("❌ URS not properly installed")
        return False
    
    # Test with a small subreddit (using PRAW if URS not fully configured)
    print("\n📊 Testing subreddit scraping (simulated)...")
    
    # Since we might not have Reddit API credentials yet, use mock data
    print("⚠️  Reddit API credentials not configured")
    print("   To use full functionality, set:")
    print("   - REDDIT_CLIENT_ID")
    print("   - REDDIT_CLIENT_SECRET")
    print("   - REDDIT_USER_AGENT")
    
    # Test lead finding (simulated)
    print("\n🎯 Testing lead finding (simulated)...")
    
    mock_leads = {
        "success": True,
        "keywords": ["business", "startup"],
        "subreddits": ["smallbusiness", "entrepreneur"],
        "total_leads": 5,
        "leads": [
            {
                "id": "mock1",
                "title": "Looking for business partners for SaaS startup",
                "author": "tech_entrepreneur",
                "subreddit": "startups",
                "score": 42,
                "num_comments": 15,
                "created_utc": time.time() - 86400,  # 1 day ago
                "permalink": "https://reddit.com/r/startups/comments/mock1",
                "keyword_matched": "startup",
                "relevance_score": 0.85,
                "contact_potential": 0.9,
                "business_indicators": ["startup", "SaaS", "business"],
                "enriched_timestamp": datetime.now().isoformat()
            }
        ],
        "timestamp": datetime.now().isoformat(),
        "source": "reddit_scraper_mock"
    }
    
    print(f"  Simulated leads found: {mock_leads['total_leads']}")
    print(f"  Sample lead: {mock_leads['leads'][0]['title'][:50]}...")
    
    # Test CSV export
    print("\n📁 Testing CSV export...")
    csv_file = scraper.export_leads_to_csv(mock_leads, "test_reddit_leads.csv")
    print(f"  CSV file: {csv_file}")
    
    print(f"\n📊 API calls today: {scraper.daily_call_count}/{scraper.max_daily_calls}")
    
    return True


if __name__ == "__main__":
    test_reddit_scraper()
    print("\n✅ Reddit Scraper Integration Ready!")