#!/usr/bin/env python3
"""
Kalshi Daily Scanner - Main Script
Runs catalyst detection and generates Kalshi recommendations
To be called by cron jobs throughout the day
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
import time

# Add workspace to path
sys.path.append('/Users/cubiczan/.openclaw/workspace')

# API Keys (from environment or config)
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "4eb2186b017a49c38d6f6ded502dd55b")
NEWSDATA_API_KEY = os.environ.get("NEWSDATA_API_KEY", "pub_fb29ca627ef54173a0675b2413523744")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "cac43a248afb1cc1ec004370df2e0282a67eb420")

def get_time_based_news(time_of_day):
    """Get news based on time of day"""
    if time_of_day == "premarket":
        # Focus on overnight news, earnings, economic data
        categories = ["business", "technology"]
        keywords = ["earnings", "fed", "cpi", "jobs", "premarket", "futures"]
    elif time_of_day == "midday":
        # Focus on breaking news, market moves
        categories = ["business", "general"]
        keywords = ["breaking", "alert", "surge", "plunge", "announcement"]
    elif time_of_day == "postmarket":
        # Focus on after-hours, earnings, guidance
        categories = ["business"]
        keywords = ["after hours", "guidance", "conference call", "analyst"]
    else:
        categories = ["business"]
        keywords = []
    
    return categories, keywords

def fetch_news_from_multiple_sources(time_of_day):
    """Fetch news from multiple APIs"""
    all_articles = []
    
    # Get time-based focus
    categories, keywords = get_time_based_news(time_of_day)
    
    # 1. News API
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": NEWS_API_KEY,
            "country": "us",
            "category": "business",
            "pageSize": 20
        }
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                articles = data.get("articles", [])
                for article in articles:
                    article["source_api"] = "newsapi"
                all_articles.extend(articles)
    except Exception as e:
        print(f"News API error: {e}")
    
    # 2. Newsdata.io
    try:
        url = "https://newsdata.io/api/1/news"
        params = {
            "apikey": NEWSDATA_API_KEY,
            "country": "us",
            "category": "business,politics",
            "language": "en",
            "size": 20
        }
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                articles = data.get("results", [])
                for article in articles:
                    article["source_api"] = "newsdata"
                    # Convert to similar format
                    article["title"] = article.get("title", "")
                    article["description"] = article.get("description", "")
                    article["url"] = article.get("link", "")
                    article["publishedAt"] = article.get("pubDate", "")
                    article["source"] = {"name": article.get("source_id", "Unknown")}
                all_articles.extend(articles)
    except Exception as e:
        print(f"Newsdata.io error: {e}")
    
    # 3. Serper API for specific searches
    try:
        for keyword in keywords[:3]:  # Top 3 keywords
            url = "https://google.serper.dev/search"
            headers = {
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            }
            payload = {
                "q": f"{keyword} news today",
                "gl": "us",
                "hl": "en",
                "num": 10
            }
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if "news" in data:
                    for news_item in data["news"]:
                        article = {
                            "title": news_item.get("title", ""),
                            "description": news_item.get("snippet", ""),
                            "url": news_item.get("link", ""),
                            "publishedAt": datetime.now().isoformat(),
                            "source": {"name": "Google Search"},
                            "source_api": "serper",
                            "search_keyword": keyword
                        }
                        all_articles.append(article)
    except Exception as e:
        print(f"Serper API error: {e}")
    
    return all_articles

def analyze_for_kalshi_catalysts(articles, time_of_day):
    """Analyze articles for Kalshi-relevant catalysts"""
    catalysts = []
    
    # Kalshi market categories and their keywords
    kalshi_categories = {
        "POLITICAL": ["election", "senate", "house", "congress", "biden", "trump", "vote", "bill", "policy"],
        "ECONOMIC": ["fed", "rate", "inflation", "cpi", "ppi", "jobs", "employment", "gdp", "retail sales"],
        "EARNINGS": ["earnings", "quarterly", "results", "guidance", "analyst", "upgrade", "downgrade"],
        "SPORTS": ["championship", "super bowl", "world series", "nba", "nfl", "mlb", "playoffs"],
        "ENTERTAINMENT": ["oscars", "grammys", "emmys", "awards", "box office", "movie", "album"],
        "WEATHER": ["hurricane", "storm", "drought", "flood", "temperature", "weather"],
        "TECH": ["apple", "google", "microsoft", "amazon", "meta", "tesla", "ai", "artificial intelligence"]
    }
    
    for article in articles:
        title = article.get("title", "").lower()
        description = article.get("description", "").lower()
        content = f"{title} {description}"
        
        # Check which Kalshi categories this article relates to
        matched_categories = []
        for category, keywords in kalshi_categories.items():
            if any(keyword in content for keyword in keywords):
                matched_categories.append(category)
        
        if matched_categories:
            catalysts.append({
                "title": article.get("title", "No title"),
                "description": article.get("description", "")[:200],
                "categories": matched_categories,
                "source": article.get("source", {}).get("name", "Unknown"),
                "source_api": article.get("source_api", "unknown"),
                "url": article.get("url", "#"),
                "published": article.get("publishedAt", ""),
                "time_of_day": time_of_day,
                "analysis_timestamp": datetime.now().isoformat()
            })
    
    return catalysts

def generate_kalshi_recommendations(catalysts, time_of_day):
    """Generate specific Kalshi trade recommendations"""
    recommendations = []
    
    # Priority based on time of day
    if time_of_day == "premarket":
        priority_categories = ["ECONOMIC", "EARNINGS", "POLITICAL"]
    elif time_of_day == "midday":
        priority_categories = ["ECONOMIC", "POLITICAL", "TECH"]
    else:  # postmarket
        priority_categories = ["EARNINGS", "ECONOMIC", "SPORTS"]
    
    for catalyst in catalysts:
        # Check if catalyst matches priority categories
        for category in catalyst["categories"]:
            if category in priority_categories:
                # Generate recommendation based on category
                rec = generate_recommendation_for_category(catalyst, category, time_of_day)
                if rec:
                    recommendations.append(rec)
                break  # Only generate one recommendation per catalyst
    
    return recommendations

def generate_recommendation_for_category(catalyst, category, time_of_day):
    """Generate specific recommendation based on category"""
    
    # Market mappings
    category_to_markets = {
        "POLITICAL": [
            "HOUSE-2024-CONTROL",
            "SENATE-2024-CONTROL", 
            "PRESIDENT-2024-WINNER",
            "SUPREME-COURT-CASES"
        ],
        "ECONOMIC": [
            "FED-2024-MAR-RATE",
            "CPI-2024-FEB",
            "NFP-2024-MAR",
            "GDP-2024-Q1"
        ],
        "EARNINGS": [
            "EARNINGS-AAPL-2024-Q1",
            "EARNINGS-MSFT-2024-Q1",
            "EARNINGS-NVDA-2024-Q1",
            "EARNINGS-AMZN-2024-Q1"
        ],
        "SPORTS": [
            "NBA-CHAMPIONSHIP-2024",
            "SUPERBOWL-2025-WINNER",
            "WORLD-SERIES-2024",
            "STANLEY-CUP-2024"
        ]
    }
    
    if category not in category_to_markets:
        return None
    
    # Select appropriate market
    markets = category_to_markets[category]
    market = markets[0]  # Use first market for now
    
    # Determine action based on sentiment (simple heuristic)
    title_lower = catalyst["title"].lower()
    positive_words = ["strong", "beat", "rise", "gain", "approve", "win", "surge"]
    negative_words = ["weak", "miss", "fall", "drop", "reject", "lose", "plunge"]
    
    sentiment = "NEUTRAL"
    if any(word in title_lower for word in positive_words):
        sentiment = "POSITIVE"
    elif any(word in title_lower for word in negative_words):
        sentiment = "NEGATIVE"
    
    # Generate recommendation
    recommendation = {
        "market": market,
        "action": "BUY YES" if sentiment == "POSITIVE" else "BUY NO",
        "catalyst": catalyst["title"],
        "reasoning": f"{category} catalyst: {catalyst['title'][:100]}...",
        "confidence": "HIGH" if sentiment != "NEUTRAL" else "MEDIUM",
        "entry_price_range": "50-70¢" if sentiment != "NEUTRAL" else "40-60¢",
        "target_price": "75-85¢" if sentiment != "NEUTRAL" else "65-75¢",
        "stop_loss": "40¢" if sentiment != "NEUTRAL" else "35¢",
        "risk_reward": "1:2.5" if sentiment != "NEUTRAL" else "1:2",
        "timeframe": "1-3 days" if category in ["ECONOMIC", "EARNINGS"] else "1-4 weeks",
        "source": catalyst["source"],
        "url": catalyst["url"],
        "analysis_time": time_of_day,
        "timestamp": datetime.now().isoformat()
    }
    
    return recommendation

def save_results(catalysts, recommendations, time_of_day):
    """Save results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"/Users/cubiczan/.openclaw/workspace/kalshi-scan-{time_of_day}-{timestamp}.json"
    
    results = {
        "scan_time": time_of_day,
        "timestamp": datetime.now().isoformat(),
        "catalysts_found": len(catalysts),
        "recommendations_generated": len(recommendations),
        "catalysts": catalysts,
        "recommendations": recommendations
    }
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    return filename

def send_discord_alert(recommendations, time_of_day):
    """Send alert to Discord (simplified - would need webhook)"""
    if not recommendations:
        return
    
    print(f"\n🚨 KALSHI ALERT - {time_of_day.upper()} SCAN")
    print("=" * 60)
    
    for i, rec in enumerate(recommendations[:3], 1):  # Top 3 only
        print(f"\n{i}. {rec['market']}")
        print(f"   Action: {rec['action']}")
        print(f"   Catalyst: {rec['catalyst'][:80]}...")
        print(f"   Entry: {rec['entry_price_range']}")
        print(f"   Target: {rec['target_price']}")
        print(f"   Stop: {rec['stop_loss']}")
        print(f"   R:R: {rec['risk_reward']}")
        print(f"   Confidence: {rec['confidence']}")

def main():
    """Main function"""
    # Get time of day from command line or determine
    if len(sys.argv) > 1:
        time_of_day = sys.argv[1]
    else:
        hour = datetime.now().hour
        if hour < 12:
            time_of_day = "premarket"
        elif hour < 16:
            time_of_day = "midday"
        else:
            time_of_day = "postmarket"
    
    print(f"⏰ Kalshi Scanner - {time_of_day.upper()} Run")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Step 1: Fetch news
    print("\n📰 Fetching news from multiple sources...")
    articles = fetch_news_from_multiple_sources(time_of_day)
    print(f"   Found {len(articles)} articles")
    
    # Step 2: Analyze for catalysts
    print("🔍 Analyzing for Kalshi catalysts...")
    catalysts = analyze_for_kalshi_catalysts(articles, time_of_day)
    print(f"   Found {len(catalysts)} potential catalysts")
    
    # Step 3: Generate recommendations
    print("🎯 Generating Kalshi trade recommendations...")
    recommendations = generate_kalshi_recommendations(catalysts, time_of_day)
    print(f"   Generated {len(recommendations)} recommendations")
    
    # Step 4: Save results
    print("💾 Saving results...")
    filename = save_results(catalysts, recommendations, time_of_day)
    print(f"   Saved to: {filename}")
    
    # Step 5: Send alerts
    print("📢 Sending alerts...")
    send_discord_alert(recommendations, time_of_day)
    
    print("\n" + "=" * 60)
    print("✅ Scan complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
