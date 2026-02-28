#!/usr/bin/env python3
"""
X (Twitter) API Integration with Bearer Token
Supports read operations and search for content strategy
"""

import os
import json
import requests
from datetime import datetime, timedelta
import time

class XAPIIntegration:
    """X (Twitter) API integration for content strategy and analytics"""
    
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.1  # seconds (respect rate limits)
        
    def make_request(self, endpoint, params=None, method="GET"):
        """Make API request with rate limiting"""
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=params)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            self.last_request_time = time.time()
            
            # Check rate limits
            if 'x-rate-limit-remaining' in response.headers:
                remaining = int(response.headers['x-rate-limit-remaining'])
                if remaining < 10:
                    print(f"⚠️  Low rate limit: {remaining} requests remaining")
            
            return response
            
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return None
    
    def search_tweets(self, query, max_results=10, days_back=7):
        """Search for recent tweets"""
        print(f"🔍 Searching tweets: '{query}'...")
        
        # Calculate date range
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days_back)
        
        params = {
            "query": f"{query} -is:retweet",
            "max_results": min(max_results, 100),
            "start_time": start_time.isoformat("T") + "Z",
            "end_time": end_time.isoformat("T") + "Z",
            "tweet.fields": "created_at,public_metrics,author_id,context_annotations,entities",
            "user.fields": "name,username,public_metrics,verified",
            "expansions": "author_id"
        }
        
        response = self.make_request("tweets/search/recent", params)
        
        if response and response.status_code == 200:
            data = response.json()
            tweets = data.get("data", [])
            users = {user["id"]: user for user in data.get("includes", {}).get("users", [])}
            
            print(f"✅ Found {len(tweets)} tweets")
            
            # Process tweets
            processed_tweets = []
            for tweet in tweets:
                author = users.get(tweet.get("author_id", ""), {})
                
                processed = {
                    "id": tweet.get("id"),
                    "text": tweet.get("text", ""),
                    "created_at": tweet.get("created_at", ""),
                    "author": {
                        "username": author.get("username", ""),
                        "name": author.get("name", ""),
                        "verified": author.get("verified", False),
                        "followers": author.get("public_metrics", {}).get("followers_count", 0)
                    },
                    "metrics": tweet.get("public_metrics", {}),
                    "engagement_rate": self.calculate_engagement_rate(
                        tweet.get("public_metrics", {}),
                        author.get("public_metrics", {}).get("followers_count", 0)
                    ),
                    "hashtags": self.extract_hashtags(tweet),
                    "urls": self.extract_urls(tweet)
                }
                
                processed_tweets.append(processed)
            
            return processed_tweets
        else:
            error_msg = response.text if response else "No response"
            print(f"❌ Search failed: {error_msg}")
            return []
    
    def get_trending_topics(self, location="worldwide", count=10):
        """Get trending topics (requires different endpoint)"""
        print(f"📈 Getting trending topics for {location}...")
        
        # Note: Twitter API v2 doesn't have direct trending endpoint
        # We'll use search for popular topics instead
        popular_queries = [
            "business", "technology", "AI", "marketing", "startup",
            "finance", "crypto", "entrepreneur", "leadership", "innovation"
        ]
        
        all_trends = []
        for query in popular_queries[:3]:  # Limit to 3 queries to avoid rate limits
            tweets = self.search_tweets(query, max_results=5, days_back=1)
            
            for tweet in tweets:
                trend = {
                    "topic": query,
                    "tweet_count": len(tweets),
                    "sample_tweet": tweet["text"][:100],
                    "engagement": tweet["metrics"].get("like_count", 0) + tweet["metrics"].get("retweet_count", 0),
                    "influencers": [tweet["author"]["username"]],
                    "hashtags": tweet["hashtags"]
                }
                all_trends.append(trend)
            
            time.sleep(1)  # Be nice to the API
        
        # Sort by engagement
        all_trends.sort(key=lambda x: x["engagement"], reverse=True)
        
        print(f"✅ Found {len(all_trends)} trending topics")
        return all_trends[:count]
    
    def analyze_competitor(self, username, max_tweets=20):
        """Analyze competitor's Twitter activity"""
        print(f"🎯 Analyzing competitor: @{username}...")
        
        # First get user ID
        user_response = self.make_request(f"users/by/username/{username}")
        
        if not user_response or user_response.status_code != 200:
            print(f"❌ Could not find user @{username}")
            return None
        
        user_data = user_response.json().get("data", {})
        user_id = user_data.get("id")
        
        # Get user tweets
        params = {
            "max_results": min(max_tweets, 100),
            "tweet.fields": "created_at,public_metrics,context_annotations",
            "exclude": "retweets,replies"
        }
        
        tweets_response = self.make_request(f"users/{user_id}/tweets", params)
        
        if not tweets_response or tweets_response.status_code != 200:
            print(f"❌ Could not get tweets for @{username}")
            return None
        
        tweets_data = tweets_response.json()
        tweets = tweets_data.get("data", [])
        
        # Analyze tweets
        analysis = {
            "username": username,
            "user_id": user_id,
            "total_tweets_analyzed": len(tweets),
            "time_period": "recent",
            "metrics": {
                "total_likes": 0,
                "total_retweets": 0,
                "total_replies": 0,
                "avg_engagement": 0,
                "best_performing_tweet": None
            },
            "content_analysis": {
                "common_hashtags": {},
                "posting_times": [],
                "content_themes": [],
                "avg_tweet_length": 0
            },
            "recommendations": []
        }
        
        if tweets:
            best_tweet = None
            best_engagement = 0
            total_length = 0
            
            for tweet in tweets:
                metrics = tweet.get("public_metrics", {})
                likes = metrics.get("like_count", 0)
                retweets = metrics.get("retweet_count", 0)
                replies = metrics.get("reply_count", 0)
                engagement = likes + retweets + replies
                
                analysis["metrics"]["total_likes"] += likes
                analysis["metrics"]["total_retweets"] += retweets
                analysis["metrics"]["total_replies"] += replies
                
                total_length += len(tweet.get("text", ""))
                
                # Track best performing tweet
                if engagement > best_engagement:
                    best_engagement = engagement
                    best_tweet = {
                        "id": tweet.get("id"),
                        "text": tweet.get("text", "")[:200],
                        "engagement": engagement,
                        "created_at": tweet.get("created_at", "")
                    }
                
                # Extract hashtags
                entities = tweet.get("entities", {})
                hashtags = entities.get("hashtags", [])
                for tag in hashtags:
                    tag_text = tag.get("tag", "").lower()
                    analysis["content_analysis"]["common_hashtags"][tag_text] = \
                        analysis["content_analysis"]["common_hashtags"].get(tag_text, 0) + 1
                
                # Track posting time
                created_at = tweet.get("created_at", "")
                if created_at:
                    analysis["content_analysis"]["posting_times"].append(created_at)
            
            # Calculate averages
            analysis["metrics"]["avg_engagement"] = (
                analysis["metrics"]["total_likes"] + 
                analysis["metrics"]["total_retweets"] + 
                analysis["metrics"]["total_replies"]
            ) / len(tweets)
            
            analysis["content_analysis"]["avg_tweet_length"] = total_length / len(tweets)
            analysis["metrics"]["best_performing_tweet"] = best_tweet
            
            # Generate recommendations
            analysis["recommendations"] = self.generate_recommendations(analysis)
        
        print(f"✅ Competitor analysis complete for @{username}")
        return analysis
    
    def generate_content_ideas(self, topics, max_ideas=5):
        """Generate content ideas based on trending topics"""
        print(f"💡 Generating content ideas for {len(topics)} topics...")
        
        content_ideas = []
        
        for topic in topics[:3]:  # Limit to 3 topics
            # Search for tweets about this topic
            tweets = self.search_tweets(topic, max_results=5, days_back=3)
            
            if tweets:
                # Analyze what's working
                popular_tweets = sorted(tweets, key=lambda x: x["engagement_rate"], reverse=True)[:3]
                
                for i, tweet in enumerate(popular_tweets):
                    idea = {
                        "topic": topic,
                        "inspiration_tweet": tweet["text"][:150],
                        "engagement_rate": tweet["engagement_rate"],
                        "author": tweet["author"]["username"],
                        "content_angle": self.generate_content_angle(tweet),
                        "suggested_hashtags": tweet["hashtags"][:5] + ["#" + topic.replace(" ", "")],
                        "platform_suggestions": ["twitter", "linkedin", "instagram"],
                        "estimated_engagement": int(tweet["engagement_rate"] * 1000)
                    }
                    content_ideas.append(idea)
            
            time.sleep(1)  # Rate limiting
        
        print(f"✅ Generated {len(content_ideas)} content ideas")
        return content_ideas[:max_ideas]
    
    def calculate_engagement_rate(self, metrics, followers):
        """Calculate engagement rate for a tweet"""
        if followers == 0:
            return 0
        
        total_engagement = (
            metrics.get("like_count", 0) +
            metrics.get("retweet_count", 0) +
            metrics.get("reply_count", 0) +
            metrics.get("quote_count", 0)
        )
        
        return total_engagement / followers if followers > 0 else 0
    
    def extract_hashtags(self, tweet):
        """Extract hashtags from tweet"""
        entities = tweet.get("entities", {})
        hashtags = entities.get("hashtags", [])
        return [tag.get("tag", "") for tag in hashtags]
    
    def extract_urls(self, tweet):
        """Extract URLs from tweet"""
        entities = tweet.get("entities", {})
        urls = entities.get("urls", [])
        return [url.get("expanded_url", "") for url in urls]
    
    def generate_content_angle(self, tweet):
        """Generate content angle based on tweet analysis"""
        text = tweet["text"].lower()
        
        angles = []
        
        if any(word in text for word in ["how to", "tutorial", "guide"]):
            angles.append("Educational/How-to")
        
        if any(word in text for word in ["announcing", "launch", "new", "release"]):
            angles.append("Announcement")
        
        if any(word in text for word in ["case study", "results", "achieved"]):
            angles.append("Case Study/Results")
        
        if any(word in text for word in ["question", "ask", "what do you think"]):
            angles.append("Question/Engagement")
        
        if any(word in text for word in ["tip", "advice", "recommend"]):
            angles.append("Tips/Advice")
        
        return angles[0] if angles else "General Discussion"
    
    def generate_recommendations(self, analysis):
        """Generate recommendations based on competitor analysis"""
        recommendations = []
        
        metrics = analysis["metrics"]
        content = analysis["content_analysis"]
        
        # Engagement recommendations
        if metrics["avg_engagement"] < 10:
            recommendations.append("Increase engagement by asking questions in tweets")
            recommendations.append("Use more visual content (images/videos)")
        
        # Hashtag recommendations
        if content["common_hashtags"]:
            top_hashtags = sorted(content["common_hashtags"].items(), key=lambda x: x[1], reverse=True)[:3]
            recommendations.append(f"Use popular hashtags: {', '.join([f'#{tag}' for tag, _ in top_hashtags])}")
        
        # Timing recommendations
        if len(content["posting_times"]) > 5:
            recommendations.append("Analyze posting times to find optimal schedule")
        
        # Content recommendations
        if content["avg_tweet_length"] < 50:
            recommendations.append("Consider longer, more detailed tweets for better engagement")
        elif content["avg_tweet_length"] > 200:
            recommendations.append("Consider shorter, more concise tweets")
        
        # General recommendations
        recommendations.append("Engage with comments and replies promptly")
        recommendations.append("Cross-promote content on other platforms")
        recommendations.append("Use Twitter threads for complex topics")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def save_analysis(self, data, filename):
        """Save analysis to file"""
        output_dir = "/Users/cubiczan/.openclaw/workspace/results"
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"📁 Analysis saved to: {filepath}")
        return filepath

def main():
    """Main function"""
    print("X (Twitter) API Integration for Content Strategy")
    print("="*60)
    
    # Load token from config
    config_path = "/Users/cubiczan/.openclaw/workspace/config/social_media_config.json"
    
    if not os.path.exists(config_path):
        print("❌ Config file not found")
        return
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    bearer_token = config.get("platforms", {}).get("twitter_x", {}).get("credentials", {}).get("bearer_token", "")
    
    if not bearer_token:
        print("❌ Bearer Token not found in config")
        return
    
    print(f"🔑 Bearer Token loaded")
    
    # Initialize integration
    x_api = XAPIIntegration(bearer_token)
    
    # Menu
    print("\n📋 OPTIONS:")
    print("1. Search tweets for content ideas")
    print("2. Get trending topics")
    print("3. Analyze competitor")
    print("4. Generate content ideas")
    print("5. Run all analyses")
    print("6. Exit")
    
    choice = input("\nSelect option (1-6): ")
    
    if choice == "1":
        query = input("Enter search query: ") or "business automation"
        tweets = x_api.search_tweets(query, max_results=10)
        
        if tweets:
            x_api.save_analysis(tweets, f"twitter_search_{query.replace(' ', '_')}.json")
            print(f"\n📊 Top 3 tweets by engagement:")
            for i, tweet in enumerate(sorted(tweets, key=lambda x: x["engagement_rate"], reverse=True)[:3], 1):
                print(f"\n{i}. @{tweet['author']['username']}:")
                print(f"   {tweet['text'][:100]}...")
                print(f"   Engagement rate: {tweet['engagement_rate']:.4f}")
                print(f"   Likes: {tweet['metrics'].get('like_count', 0)}")
    
    elif choice == "2":
        trends = x_api.get_trending_topics(count=8)
        
        if trends:
            x_api.save_analysis(trends, "twitter_trends.json")
            print(f"\n📈 Top trending topics:")
            for i, trend in enumerate(trends, 1):
                print(f"\n{i}. {trend['topic'].title()}:")
                print(f"   Sample: {trend['sample_tweet']}...")
                print(f"   Engagement: {trend['engagement']}")
                print(f"   Hashtags: {', '.join(trend['hashtags'][:3])}")
    
    elif choice == "3":
        username = input("Enter competitor username