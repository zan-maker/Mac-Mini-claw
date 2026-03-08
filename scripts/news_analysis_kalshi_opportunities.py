#!/usr/bin/env python3
"""
News Analysis for Kalshi Trading Opportunities
Analyzes current news to identify high-probability non-sports trades
$220 cash available to deploy
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
import time

# API Keys (from kalshi-daily-scanner.py)
NEWS_API_KEY = "4eb2186b017a49c38d6f6ded502dd55b"
NEWSDATA_API_KEY = "pub_fb29ca627ef54173a0675b2413523744"
SERPER_API_KEY = "cac43a248afb1cc1ec004370df2e0282a67eb420"

# Available capital
AVAILABLE_CAPITAL = 220

def fetch_current_news():
    """Fetch current news from multiple sources"""
    print("📰 Fetching current news...")
    all_articles = []
    
    # 1. News API - Top headlines
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": NEWS_API_KEY,
            "country": "us",
            "pageSize": 30,
            "category": "business"
        }
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                articles = data.get("articles", [])
                for article in articles:
                    article["source_api"] = "newsapi"
                all_articles.extend(articles)
                print(f"✅ News API: {len(articles)} articles")
    except Exception as e:
        print(f"❌ News API error: {e}")
    
    # 2. Newsdata.io - Comprehensive news
    try:
        url = "https://newsdata.io/api/1/news"
        params = {
            "apikey": NEWSDATA_API_KEY,
            "country": "us",
            "category": "business,politics,technology,environment",
            "language": "en",
            "size": 30
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
                print(f"✅ Newsdata.io: {len(articles)} articles")
    except Exception as e:
        print(f"❌ Newsdata.io error: {e}")
    
    # 3. Serper API for specific Kalshi-relevant searches
    kalshi_keywords = [
        "Federal Reserve interest rates", "inflation CPI report", "jobs report unemployment",
        "election 2024 polls", "Supreme Court decision", "Congress bill vote",
        "hurricane forecast", "extreme weather", "temperature records",
        "tech earnings report", "Apple Microsoft Amazon", "oil prices OPEC",
        "geopolitical conflict", "international tensions"
    ]
    
    try:
        for keyword in kalshi_keywords[:3]:  # Top 3 most relevant
            url = "https://google.serper.dev/search"
            headers = {
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            }
            payload = {
                "q": f"{keyword} news",
                "num": 5
            }
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                news_items = data.get("news", [])
                if news_items:
                    for item in news_items:
                        item["source_api"] = "serper"
                        item["title"] = item.get("title", "")
                        item["description"] = item.get("snippet", "")
                        item["url"] = item.get("link", "")
                        item["publishedAt"] = ""
                        item["source"] = {"name": "Google Search"}
                    all_articles.extend(news_items)
                    print(f"✅ Serper ({keyword[:20]}...): {len(news_items)} articles")
                else:
                    print(f"⚠️  Serper ({keyword[:20]}...): No news items returned")
            else:
                print(f"⚠️  Serper API status: {response.status_code}")
            time.sleep(1)  # Rate limiting
    except Exception as e:
        print(f"❌ Serper API error: {e}")
    
    print(f"📊 Total articles collected: {len(all_articles)}")
    return all_articles

def analyze_news_for_kalshi_opportunities(articles):
    """Analyze news to identify Kalshi trading opportunities"""
    print("\n🔍 Analyzing news for Kalshi opportunities...")
    
    # Categories of Kalshi markets
    categories = {
        "POLITICAL": {
            "keywords": ["election", "Trump", "Biden", "Congress", "Senate", "House", "Supreme Court", 
                        "impeachment", "vote", "political", "policy", "legislation", "bill", "law"],
            "probability": 0.7,
            "timeframe": "days to weeks"
        },
        "ECONOMIC": {
            "keywords": ["Fed", "Federal Reserve", "interest rates", "inflation", "CPI", "jobs report",
                        "unemployment", "GDP", "retail sales", "manufacturing", "economic", "recession"],
            "probability": 0.65,
            "timeframe": "weeks to months"
        },
        "WEATHER_CLIMATE": {
            "keywords": ["hurricane", "storm", "temperature", "heat", "cold", "snow", "rain", "drought",
                        "flood", "wildfire", "climate", "weather", "forecast", "NOAA"],
            "probability": 0.8,
            "timeframe": "days"
        },
        "TECH_EARNINGS": {
            "keywords": ["earnings", "Apple", "Microsoft", "Amazon", "Google", "Meta", "Tesla", "NVIDIA",
                        "quarterly", "results", "guidance", "analyst", "price target", "upgrade", "downgrade"],
            "probability": 0.6,
            "timeframe": "days to weeks"
        },
        "ENERGY_COMMODITIES": {
            "keywords": ["oil", "gas", "OPEC", "energy", "prices", "crude", "petroleum", "natural gas",
                        "commodities", "supply", "demand", "inventory", "production"],
            "probability": 0.7,
            "timeframe": "weeks"
        },
        "INTERNATIONAL": {
            "keywords": ["war", "conflict", "tensions", "diplomacy", "sanctions", "trade", "tariffs",
                        "China", "Russia", "Iran", "North Korea", "Ukraine", "Middle East", "Asia"],
            "probability": 0.55,
            "timeframe": "weeks to months"
        },
        "HEALTH_SCIENCE": {
            "keywords": ["FDA", "approval", "clinical trial", "vaccine", "treatment", "drug", "study",
                        "research", "breakthrough", "discovery", "medical", "health"],
            "probability": 0.5,
            "timeframe": "months"
        }
    }
    
    opportunities = []
    
    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")
        
        # Handle None values
        if title is None:
            title = ""
        if description is None:
            description = ""
            
        title = title.lower()
        description = description.lower()
        content = f"{title} {description}"
        
        for category, info in categories.items():
            score = 0
            matched_keywords = []
            
            for keyword in info["keywords"]:
                if keyword.lower() in content:
                    score += 1
                    matched_keywords.append(keyword)
            
            if score >= 2:  # At least 2 keyword matches
                # Calculate confidence based on recency and source
                confidence = info["probability"]
                
                # Boost confidence for recent articles (last 24 hours)
                published_at = article.get("publishedAt", "")
                if published_at:
                    try:
                        pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                        hours_ago = (datetime.now(pub_date.tzinfo) - pub_date).total_seconds() / 3600
                        if hours_ago < 24:
                            confidence *= 1.2  # 20% boost for recent news
                    except:
                        pass
                
                # Source reliability boost
                source = article.get("source", {}).get("name", "").lower()
                reliable_sources = ["reuters", "bloomberg", "cnbc", "wsj", "financial times", "associated press"]
                if any(rel_source in source for rel_source in reliable_sources):
                    confidence *= 1.1  # 10% boost for reliable sources
                
                opportunity = {
                    "category": category,
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "url": article.get("url", ""),
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "published": article.get("publishedAt", ""),
                    "matched_keywords": matched_keywords,
                    "confidence": min(confidence, 0.95),  # Cap at 95%
                    "timeframe": info["timeframe"],
                    "potential_kalshi_markets": generate_kalshi_markets(category, content),
                    "recommended_action": generate_recommendation(category, confidence)
                }
                opportunities.append(opportunity)
    
    # Sort by confidence (highest first)
    opportunities.sort(key=lambda x: x["confidence"], reverse=True)
    
    print(f"🎯 Found {len(opportunities)} potential Kalshi opportunities")
    return opportunities[:10]  # Return top 10

def generate_kalshi_markets(category, content):
    """Generate potential Kalshi market ideas based on category and content"""
    markets = []
    
    if category == "POLITICAL":
        if "election" in content:
            markets.append("Election outcome markets (state/national)")
        if "Supreme Court" in content:
            markets.append("SCOTUS decision markets")
        if "Congress" in content or "bill" in content:
            markets.append("Legislation passage markets")
        markets.append("Political appointment/confirmation markets")
        
    elif category == "ECONOMIC":
        if "Fed" in content or "interest rates" in content:
            markets.append("Fed rate decision markets")
        if "inflation" in content or "CPI" in content:
            markets.append("Inflation data markets")
        if "jobs report" in content or "unemployment" in content:
            markets.append("Jobs report markets")
        markets.append("Economic indicator markets (GDP, retail sales)")
        
    elif category == "WEATHER_CLIMATE":
        if "hurricane" in content or "storm" in content:
            markets.append("Hurricane landfall/strength markets")
        if "temperature" in content:
            markets.append("Temperature record markets")
        if "drought" in content or "flood" in content:
            markets.append("Extreme weather event markets")
        markets.append("Seasonal weather prediction markets")
        
    elif category == "TECH_EARNINGS":
        markets.append("Tech earnings beat/miss markets")
        markets.append("Stock price movement markets")
        markets.append("Analyst rating change markets")
        
    elif category == "ENERGY_COMMODITIES":
        if "oil" in content or "gas" in content:
            markets.append("Oil/gas price movement markets")
        if "OPEC" in content:
            markets.append("OPEC production decision markets")
        markets.append("Energy inventory report markets")
        
    elif category == "INTERNATIONAL":
        markets.append("Geopolitical event markets")
        markets.append("Diplomatic outcome markets")
        markets.append("Conflict escalation/de-escalation markets")
        
    elif category == "HEALTH_SCIENCE":
        markets.append("FDA approval markets")
        markets.append("Clinical trial outcome markets")
        markets.append("Medical breakthrough markets")
    
    return markets

def generate_recommendation(category, confidence):
    """Generate trading recommendation based on category and confidence"""
    if confidence >= 0.8:
        size = "MEDIUM-LARGE"
        action = "STRONG BUY"
    elif confidence >= 0.7:
        size = "MEDIUM"
        action = "BUY"
    elif confidence >= 0.6:
        size = "SMALL-MEDIUM"
        action = "CONSIDER"
    else:
        size = "SMALL"
        action = "MONITOR"
    
    return f"{action} ({size} position)"

def create_trading_plan(opportunities, available_capital):
    """Create detailed trading plan with capital allocation"""
    print("\n💰 Creating trading plan...")
    
    trading_plan = {
        "available_capital": available_capital,
        "total_allocated": 0,
        "opportunities": [],
        "recommended_allocations": []
    }
    
    # Capital allocation strategy
    capital_per_opportunity = available_capital / min(len(opportunities), 5)  # Spread across top 5
    
    for i, opp in enumerate(opportunities[:5]):  # Top 5 opportunities
        # Determine position size based on confidence
        if opp["confidence"] >= 0.8:
            allocation = capital_per_opportunity * 1.2  # 20% more for high confidence
        elif opp["confidence"] >= 0.7:
            allocation = capital_per_opportunity
        elif opp["confidence"] >= 0.6:
            allocation = capital_per_opportunity * 0.8  # 20% less for medium confidence
        else:
            allocation = capital_per_opportunity * 0.5  # 50% less for lower confidence
        
        allocation = round(allocation, 2)
        
        trade = {
            "rank": i + 1,
            "category": opp["category"],
            "confidence": opp["confidence"],
            "allocation": allocation,
            "title": opp["title"][:100] + "..." if len(opp["title"]) > 100 else opp["title"],
            "potential_markets": opp["potential_kalshi_markets"][:3],  # Top 3 markets
            "action": opp["recommended_action"],
            "timeframe": opp["timeframe"]
        }
        
        trading_plan["opportunities"].append(trade)
        trading_plan["total_allocated"] += allocation
    
    # Ensure we don't overallocate
    if trading_plan["total_allocated"] > available_capital:
        scale_factor = available_capital / trading_plan["total_allocated"]
        for trade in trading_plan["opportunities"]:
            trade["allocation"] = round(trade["allocation"] * scale_factor, 2)
        trading_plan["total_allocated"] = available_capital
    
    # Create recommended allocations
    trading_plan["recommended_allocations"] = [
        {
            "opportunity": f"{trade['rank']}. {trade['category']}",
            "amount": f"${trade['allocation']}",
            "confidence": f"{trade['confidence']*100:.0f}%",
            "action": trade["action"]
        }
        for trade in trading_plan["opportunities"]
    ]
    
    return trading_plan

def main():
    """Main function"""
    print("======================================================================")
    print("🎯 KALSHI TRADING OPPORTUNITIES - NEWS ANALYSIS")
    print("======================================================================")
    print(f"💰 Available Capital: ${AVAILABLE_CAPITAL}")
    print(f"📅 Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Fetch current news
    articles = fetch_current_news()
    
    if not articles:
        print("❌ No articles fetched. Exiting.")
        return
    
    # Step 2: Analyze for Kalshi opportunities
    opportunities = analyze_news_for_kalshi_opportunities(articles)
    
    if not opportunities:
        print("❌ No Kalshi opportunities identified.")
        return
    
    # Step 3: Create trading plan
    trading_plan = create_trading_plan(opportunities, AVAILABLE_CAPITAL)
    
    # Step 4: Display results
    print("\n" + "="*70)
    print("📊 TRADING OPPORTUNITIES ANALYSIS")
    print("="*70)
    
    print(f"\n💰 CAPITAL ALLOCATION:")
    print(f"   Available: ${AVAILABLE_CAPITAL}")
    print(f"   Recommended: ${trading_plan['total_allocated']:.2f}")
    print(f"   Remaining: ${AVAILABLE_CAPITAL - trading_plan['total_allocated']:.2f}")
    
    print("\n🎯 TOP OPPORTUNITIES:")
    print("-"*70)
    
    for trade in trading_plan["opportunities"]:
        print(f"\n#{trade['rank']} - {trade['category']} ({trade['confidence']*100:.0f}% confidence)")
        print(f"   📰 {trade['title']}")
        print(f"   💰 Allocation: ${trade['allocation']}")
        print(f"   🎯 Action: {trade['action']}")
        print(f"   ⏰ Timeframe: {trade['timeframe']}")
        print(f"   📈 Potential Kalshi Markets:")
        for market in trade['potential_markets']:
            print(f"      • {market}")
    
    print("\n" + "="*70)
    print("🎯 RECOMMENDED TRADING PLAN:")
    print("="*70)
    
    print(f"\nTotal Capital: ${AVAILABLE_CAPITAL}")
    print(f"To Deploy: ${trading_plan['total_allocated']:.2f}")
    print(f"To Reserve: ${AVAILABLE_CAPITAL - trading_plan['total_allocated']:.2f}")
    
    print("\n📋 Allocation Summary:")
    for alloc in trading_plan["recommended_allocations"]:
        print(f"   {alloc['opportunity']}: {alloc['amount']} ({alloc['confidence']}) - {alloc['action']}")
    
    print("\n⚡ Quick Actions:")
    print("   1. Check Kalshi for specific markets matching these categories")
    print("   2. Review YES/NO prices for identified markets")
    print("   3. Place orders with recommended allocations")
    print("   4. Set reminders for timeframe-based monitoring")
    print("   5. Track news catalysts for each position")
    
    print("\n📅 Next Analysis:")
    print("   • Re-run this analysis in 24 hours")
    print("   • Monitor news for catalyst updates")
    print("   • Adjust positions based on new information")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    results_file = f"/Users/cubiczan/.openclaw/workspace/kalshi_opportunities/analysis_{timestamp}.json"
    
    results_data = {
        "timestamp": datetime.now().isoformat(),
        "available_capital": AVAILABLE_CAPITAL,
        "articles_analyzed": len(articles),
        "opportunities_found": len(opportunities),
        "trading_plan": trading_plan,
        "top_opportunities": opportunities[:5]
    }
    
    os.makedirs(os.path.dirname(results_file), exist_ok=True)
    try:
        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2)
        print(f"\n📄 Analysis saved to: {results_file}")
    except Exception as e:
        print(f"\n⚠️  Could not save results: {e}")
    
    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE")
    print("="*70)
    print(f"\n🎯 Next: Check Kalshi platform for specific markets")
    print(f"💰 Deploy: ${trading_plan['total_allocated']:.2f} across top opportunities")
    print(f"📊 Monitor: News catalysts and market movements")

if __name__ == "__main__":
    main()