#!/usr/bin/env python3
"""
Gas Price Trade Monitor
Tracks news and data for Kalshi gas price trade
"""

import requests
import json
from datetime import datetime, timedelta
import time

# API Keys
NEWS_API_KEY = "4eb2186b017a49c38d6f6ded502dd55b"
NEWSDATA_API_KEY = "pub_fb29ca627ef54173a0675b2413523744"
SERPER_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"

def get_gas_price_news():
    """Get news about gas prices"""
    articles = []
    
    # 1. News API
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": NEWS_API_KEY,
            "q": "gas prices OR gasoline prices OR oil prices",
            "pageSize": 10,
            "sortBy": "relevancy",
            "language": "en"
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                for article in data.get("articles", []):
                    articles.append({
                        "title": article.get("title", ""),
                        "source": article.get("source", {}).get("name", ""),
                        "url": article.get("url", ""),
                        "published": article.get("publishedAt", ""),
                        "api": "newsapi"
                    })
    except Exception as e:
        print(f"News API error: {e}")
    
    # 2. Newsdata.io
    try:
        url = "https://newsdata.io/api/1/news"
        params = {
            "apikey": NEWSDATA_API_KEY,
            "q": "gasoline price",
            "country": "us",
            "category": "business",
            "language": "en",
            "size": 10
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                for article in data.get("results", []):
                    articles.append({
                        "title": article.get("title", ""),
                        "source": article.get("source_id", ""),
                        "url": article.get("link", ""),
                        "published": article.get("pubDate", ""),
                        "api": "newsdata"
                    })
    except Exception as e:
        print(f"Newsdata.io error: {e}")
    
    return articles

def get_current_gas_price():
    """Get current US gas price (simulated - would use API in production)"""
    # In production, would use: AAA Gas Prices API, EIA API, or GasBuddy API
    # For now, return simulated data
    return {
        "national_average": 3.42,  # Example: $3.42/gallon
        "last_updated": datetime.now().isoformat(),
        "trend": "up",  # up, down, stable
        "source": "simulated",
        "note": "In production, connect to real gas price API"
    }

def analyze_trade_risk(articles, current_price):
    """Analyze risk for the gas price trade"""
    bullish_signals = 0
    bearish_signals = 0
    neutral_signals = 0
    
    # Keywords analysis
    bullish_keywords = ["rise", "increase", "spike", "surge", "higher", "up", "shortage", "OPEC", "cut", "tension", "conflict", "Iran"]
    bearish_keywords = ["fall", "drop", "decline", "lower", "down", "glut", "surplus", "inventory", "build", "peace", "deal"]
    
    for article in articles:
        title = article["title"].lower()
        
        # Check for keywords
        bull_count = sum(1 for word in bullish_keywords if word in title)
        bear_count = sum(1 for word in bearish_keywords if word in title)
        
        if bull_count > bear_count:
            bullish_signals += 1
        elif bear_count > bull_count:
            bearish_signals += 1
        else:
            neutral_signals += 1
    
    # Price analysis
    target_price = 3.50
    current = current_price["national_average"]
    distance_to_target = target_price - current
    
    # Risk assessment
    if distance_to_target <= 0.05:  # Within 5 cents
        price_risk = "LOW - Near target"
    elif distance_to_target <= 0.15:  # Within 15 cents
        price_risk = "MEDIUM - Getting close"
    else:
        price_risk = "HIGH - Needs significant move"
    
    # Overall sentiment
    total_signals = bullish_signals + bearish_signals + neutral_signals
    if total_signals > 0:
        sentiment_score = (bullish_signals - bearish_signals) / total_signals
    else:
        sentiment_score = 0
    
    if sentiment_score > 0.3:
        sentiment = "BULLISH"
    elif sentiment_score < -0.3:
        sentiment = "BEARISH"
    else:
        sentiment = "NEUTRAL"
    
    return {
        "current_price": current,
        "target_price": target_price,
        "distance_to_target": distance_to_target,
        "price_risk": price_risk,
        "bullish_articles": bullish_signals,
        "bearish_articles": bearish_signals,
        "neutral_articles": neutral_signals,
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "analysis_time": datetime.now().isoformat()
    }

def generate_recommendation(analysis):
    """Generate trading recommendation based on analysis"""
    current = analysis["current_price"]
    target = analysis["target_price"]
    sentiment = analysis["sentiment"]
    distance = analysis["distance_to_target"]
    
    if current >= target:
        return {
            "action": "HOLD - Already above target",
            "confidence": "HIGH",
            "reasoning": f"Current price ${current:.2f} already above target ${target:.2f}",
            "urgency": "LOW"
        }
    elif sentiment == "BULLISH" and distance <= 0.10:
        return {
            "action": "HOLD - Bullish and close to target",
            "confidence": "MEDIUM-HIGH",
            "reasoning": f"Bullish news sentiment, only ${distance:.2f} from target",
            "urgency": "MEDIUM"
        }
    elif sentiment == "BEARISH" and distance > 0.10:
        return {
            "action": "CONSIDER EXITING - Bearish and far from target",
            "confidence": "MEDIUM",
            "reasoning": f"Bearish news sentiment, ${distance:.2f} from target",
            "urgency": "HIGH"
        }
    else:
        return {
            "action": "MONITOR - Wait for clearer signals",
            "confidence": "LOW-MEDIUM",
            "reasoning": f"Mixed signals, ${distance:.2f} from target",
            "urgency": "LOW"
        }

def main():
    print("=" * 70)
    print("GAS PRICE TRADE MONITOR")
    print(f"Trade: $25 YES on Gas prices above $3.50")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    # Get current gas price
    print("⛽ Fetching gas price data...")
    current_price = get_current_gas_price()
    print(f"   Current US average: ${current_price['national_average']:.2f}/gallon")
    print(f"   Target: $3.50/gallon")
    print(f"   Need: +${3.50 - current_price['national_average']:.2f} increase")
    
    # Get news
    print("\n📰 Scanning gas price news...")
    articles = get_gas_price_news()
    print(f"   Found {len(articles)} relevant articles")
    
    # Analyze risk
    print("\n🔍 Analyzing trade risk...")
    analysis = analyze_trade_risk(articles, current_price)
    
    print(f"   News Sentiment: {analysis['sentiment']} (score: {analysis['sentiment_score']:.2f})")
    print(f"   Bullish articles: {analysis['bullish_articles']}")
    print(f"   Bearish articles: {analysis['bearish_articles']}")
    print(f"   Neutral articles: {analysis['neutral_articles']}")
    print(f"   Price Risk: {analysis['price_risk']}")
    
    # Generate recommendation
    print("\n🎯 Trade Recommendation:")
    recommendation = generate_recommendation(analysis)
    print(f"   Action: {recommendation['action']}")
    print(f"   Confidence: {recommendation['confidence']}")
    print(f"   Reasoning: {recommendation['reasoning']}")
    print(f"   Urgency: {recommendation['urgency']}")
    
    # Show recent news
    print("\n📋 RECENT GAS PRICE NEWS:")
    print("-" * 70)
    for i, article in enumerate(articles[:5], 1):
        print(f"{i}. {article['title'][:80]}...")
        print(f"   Source: {article['source']}")
        print()
    
    # Trade summary
    print("=" * 70)
    print("💰 TRADE SUMMARY:")
    print("=" * 70)
    print(f"Investment: $25")
    print(f"Target Price: $3.50/gallon")
    print(f"Current Price: ${current_price['national_average']:.2f}/gallon")
    print(f"Distance to Target: ${analysis['distance_to_target']:.2f}")
    
    if current_price['national_average'] >= 3.50:
        print(f"✅ STATUS: ALREADY WINNING")
        potential_payout = 25 * 1.93  # 1.93x multiplier
        profit = potential_payout - 25
        print(f"Potential Payout: ${potential_payout:.2f}")
        print(f"Potential Profit: ${profit:.2f} ({profit/25*100:.0f}% return)")
    else:
        needed_increase = 3.50 - current_price['national_average']
        percent_needed = (needed_increase / current_price['national_average']) * 100
        print(f"📈 Needed Increase: ${needed_increase:.2f} ({percent_needed:.1f}%)")
        print(f"Days to Settlement: {(datetime(2026, 3, 31) - datetime.now()).days} days")
    
    print()
    print("⏰ Next update: 1 hour")
    print("📊 Monitor: Geopolitical news, OPEC decisions, inventory reports")

if __name__ == "__main__":
    main()
