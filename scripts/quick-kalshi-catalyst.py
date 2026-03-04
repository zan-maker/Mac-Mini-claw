#!/usr/bin/env python3
"""
Quick Kalshi Catalyst Scanner
Check current news and match with Kalshi markets
"""

import requests
import json
from datetime import datetime, timedelta
import os

# API Keys
NEWS_API_KEY = "4eb2186b017a49c38d6f6ded502dd55b"
NEWSDATA_API_KEY = "pub_fb29ca627ef54173a0675b2413523744"

def get_breaking_news():
    """Get breaking news from News API"""
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": NEWS_API_KEY,
        "country": "us",
        "category": "business",
        "pageSize": 10
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("status") == "ok":
            return data.get("articles", [])
        else:
            print(f"News API error: {data.get('message', 'Unknown error')}")
            return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def get_newsdata_news():
    """Get news from Newsdata.io"""
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWSDATA_API_KEY,
        "country": "us",
        "category": "business,politics",
        "language": "en",
        "size": 10
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("status") == "success":
            return data.get("results", [])
        else:
            print(f"Newsdata.io error: {data.get('message', 'Unknown error')}")
            return []
    except Exception as e:
        print(f"Error fetching newsdata: {e}")
        return []

def analyze_catalysts(news_articles):
    """Analyze news for trading catalysts"""
    catalysts = []
    
    # Keywords that indicate market-moving events
    catalyst_keywords = [
        # Economic
        "fed", "rate", "inflation", "cpi", "jobs", "employment", "gdp",
        "earnings", "quarterly", "results", "guidance",
        # Political
        "election", "senate", "house", "congress", "biden", "trump",
        "policy", "regulation", "fda", "approval",
        # Events
        "summit", "meeting", "conference", "deadline", "vote",
        # Company specific
        "merger", "acquisition", "buyout", "lawsuit", "settlement"
    ]
    
    for article in news_articles:
        title = article.get("title", "").lower()
        description = article.get("description", "").lower()
        content = title + " " + description
        
        # Check for catalyst keywords
        found_keywords = [kw for kw in catalyst_keywords if kw in content]
        
        if found_keywords:
            catalysts.append({
                "title": article.get("title", "No title"),
                "source": article.get("source", {}).get("name", "Unknown"),
                "url": article.get("url", "#"),
                "keywords": found_keywords,
                "published": article.get("publishedAt", "")
            })
    
    return catalysts

def generate_kalshi_recommendations(catalysts):
    """Generate Kalshi trade recommendations based on catalysts"""
    recommendations = []
    
    # Map catalysts to potential Kalshi markets
    catalyst_to_market = {
        "fed": "FED-",
        "rate": "FED-",
        "inflation": "CPI-",
        "cpi": "CPI-",
        "jobs": "NFP-",
        "employment": "NFP-",
        "election": "SENATE-",
        "senate": "SENATE-",
        "house": "HOUSE-",
        "congress": "CONGRESS-",
        "earnings": "EARNINGS-"
    }
    
    for catalyst in catalysts[:5]:  # Top 5 catalysts
        for keyword in catalyst["keywords"]:
            if keyword in catalyst_to_market:
                market_prefix = catalyst_to_market[keyword]
                
                # Create recommendation
                rec = {
                    "market_type": market_prefix[:-1],  # Remove trailing dash
                    "catalyst": catalyst["title"],
                    "reasoning": f"Breaking news: {catalyst['title']}. Expected to move {market_prefix[:-1]} markets.",
                    "recommended_action": "BUY YES if news is positive, BUY NO if negative",
                    "confidence": "High" if keyword in ["fed", "cpi", "earnings"] else "Medium",
                    "timeframe": "Next 1-3 trading days",
                    "source": catalyst["source"],
                    "url": catalyst["url"]
                }
                
                recommendations.append(rec)
                break  # Only use first matching keyword per catalyst
    
    return recommendations

def main():
    print("=" * 60)
    print("KALSHI CATALYST SCANNER - LIVE ANALYSIS")
    print("=" * 60)
    print()
    
    # Get news from both sources
    print("📰 Scanning breaking news...")
    news_api_articles = get_breaking_news()
    newsdata_articles = get_newsdata_news()
    
    all_articles = news_api_articles + newsdata_articles
    print(f"   Found {len(all_articles)} news articles")
    
    # Analyze for catalysts
    print("🔍 Analyzing for trading catalysts...")
    catalysts = analyze_catalysts(all_articles)
    print(f"   Found {len(catalysts)} potential catalysts")
    
    # Generate Kalshi recommendations
    print("🎯 Generating Kalshi trade recommendations...")
    recommendations = generate_kalshi_recommendations(catalysts)
    
    # Display results
    print()
    print("=" * 60)
    print("ACTIONABLE KALSHI RECOMMENDATIONS")
    print("=" * 60)
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['market_type']} MARKETS")
            print(f"   📰 Catalyst: {rec['catalyst'][:80]}...")
            print(f"   🎯 Action: {rec['recommended_action']}")
            print(f"   📊 Confidence: {rec['confidence']}")
            print(f"   ⏰ Timeframe: {rec['timeframe']}")
            print(f"   🔗 Source: {rec['source']}")
            print(f"   📈 Reasoning: {rec['reasoning']}")
    else:
        print("\n❌ No strong catalysts found for immediate Kalshi trades.")
        print("   Checking alternative opportunities...")
        
        # Fallback: Common Kalshi markets to monitor
        print("\n📊 Monitor these Kalshi markets today:")
        print("   • FED- (Federal Reserve decisions)")
        print("   • CPI- (Inflation reports)")
        print("   • NFP- (Jobs reports)")
        print("   • SENATE- (Election predictions)")
        print("   • EARNINGS- (Major company earnings)")
    
    print()
    print("=" * 60)
    print(f"Analysis complete: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    main()
