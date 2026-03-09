#!/usr/bin/env python3
"""
Crude & Gasoline War Monitor for Kalshi Trading
Monitors geopolitical risks and price movements for trading opportunities
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
import time

def load_env_file():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    if line.startswith('export '):
                        line = line[7:]
                    key, value = line.split('=', 1)
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    os.environ[key.strip()] = value.strip()
        return True
    return False

def get_crude_prices():
    """Get current crude oil prices"""
    # In production, use actual API like EIA, Bloomberg, or trading APIs
    # For now, return mock data with realistic war-driven volatility
    
    prices = {
        "WTI": {
            "current": 78.50,
            "change": +2.30,  # +3.0%
            "volatility": "HIGH",
            "support": 76.00,
            "resistance": 80.00,
            "news_catalyst": "Middle East tensions escalating"
        },
        "Brent": {
            "current": 82.75,
            "change": +2.15,  # +2.7%
            "volatility": "HIGH",
            "support": 80.00,
            "resistance": 85.00,
            "news_catalyst": "OPEC emergency meeting called"
        },
        "Gasoline_RBOB": {
            "current": 2.65,  # $/gallon
            "change": +0.12,  # +4.7%
            "volatility": "VERY HIGH",
            "support": 2.50,
            "resistance": 2.75,
            "news_catalyst": "Refinery disruptions reported"
        }
    }
    
    return prices

def get_war_news(api_key):
    """Get news about geopolitical tensions affecting oil prices"""
    if not api_key:
        return []
    
    try:
        # NewsAPI for war/conflict news
        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": api_key,
            "q": "crude oil OR gasoline prices OR war conflict OR middle east OR ukraine OR opec",
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": 10
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return articles[:5]  # Return top 5 articles
    except Exception as e:
        print(f"⚠️  News API error: {e}")
    
    return []

def analyze_kalshi_opportunities(crude_prices, news_articles):
    """Analyze Kalshi trading opportunities based on crude/gasoline prices"""
    
    opportunities = []
    
    # 1. Gasoline Price Opportunities
    gasoline_price = crude_prices["Gasoline_RBOB"]["current"]
    
    # Kalshi gasoline markets typically track RBOB futures
    # Common thresholds: $2.50, $2.75, $3.00, $3.25, $3.50
    
    thresholds = [2.50, 2.75, 3.00, 3.25, 3.50]
    current_threshold = None
    next_threshold = None
    
    for i, threshold in enumerate(thresholds):
        if gasoline_price < threshold:
            current_threshold = thresholds[i-1] if i > 0 else 2.25
            next_threshold = threshold
            break
    
    if current_threshold and next_threshold:
        # Calculate probabilities based on momentum and news
        momentum = crude_prices["Gasoline_RBOB"]["change"]
        volatility = crude_prices["Gasoline_RBOB"]["volatility"]
        
        if volatility == "VERY HIGH" and momentum > 0:
            # Bullish scenario - prices rising rapidly
            confidence = 75
            recommendation = f"BUY YES on Gasoline >${next_threshold}"
            rationale = f"War-driven volatility with strong upward momentum (+{momentum:.2f})"
        elif volatility == "VERY HIGH" and momentum < 0:
            # Bearish scenario - prices falling rapidly
            confidence = 70
            recommendation = f"BUY NO on Gasoline >${next_threshold}"
            rationale = f"High volatility with downward pressure"
        else:
            # Neutral/mixed signals
            confidence = 55
            recommendation = f"WAIT for clearer signal near ${next_threshold}"
            rationale = "Mixed signals, monitor closely"
        
        opportunities.append({
            "market": f"Gasoline >${next_threshold}/gallon",
            "type": "YES/NO",
            "current_price": gasoline_price,
            "threshold": next_threshold,
            "distance": abs(gasoline_price - next_threshold),
            "confidence": confidence,
            "recommendation": recommendation,
            "rationale": rationale,
            "timeframe": "1-7 days",
            "urgency": "HIGH" if volatility == "VERY HIGH" else "MEDIUM",
            "category": "GASOLINE"
        })
    
    # 2. Crude Oil Opportunities
    wti_price = crude_prices["WTI"]["current"]
    crude_thresholds = [75, 80, 85, 90]
    
    for threshold in crude_thresholds:
        if abs(wti_price - threshold) < 3.0:  # Within $3 of threshold
            direction = "ABOVE" if wti_price > threshold else "BELOW"
            confidence = 65 if crude_prices["WTI"]["volatility"] == "HIGH" else 50
            
            opportunities.append({
                "market": f"WTI Crude ${threshold}/barrel",
                "type": "YES/NO",
                "current_price": wti_price,
                "threshold": threshold,
                "distance": abs(wti_price - threshold),
                "confidence": confidence,
                "recommendation": f"BUY YES if bullish, BUY NO if bearish near ${threshold}",
                "rationale": f"War volatility creates binary opportunities at key levels",
                "timeframe": "1-5 days",
                "urgency": "HIGH",
                "category": "CRUDE"
            })
    
    # 3. News-based opportunities
    war_keywords = ["attack", "strike", "sanctions", "embargo", "tensions", "escalat", "conflict"]
    high_impact_news = []
    
    for article in news_articles:
        title = article.get("title", "").lower()
        description = article.get("description", "").lower()
        
        for keyword in war_keywords:
            if keyword in title or keyword in description:
                high_impact_news.append({
                    "title": article.get("title", "No title"),
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "impact": "HIGH",
                    "trading_implication": "Expect increased volatility and price spikes"
                })
                break
    
    # Add news-based opportunity if high-impact news found
    if high_impact_news:
        opportunities.append({
            "market": "Volatility Spike Trade",
            "type": "SPECIAL",
            "current_price": "N/A",
            "threshold": "N/A",
            "confidence": 80,
            "recommendation": "BUY volatility (YES on extreme moves)",
            "rationale": f"{len(high_impact_news)} high-impact war news items detected",
            "timeframe": "1-3 days",
            "urgency": "VERY HIGH",
            "category": "NEWS_DRIVEN",
            "news_count": len(high_impact_news)
        })
    
    return opportunities, high_impact_news

def main():
    print("🛢️  CRUDE & GASOLINE WAR MONITOR")
    print("=" * 70)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Focus: Kalshi trading opportunities from geopolitical risks")
    print("")
    
    # Load environment
    if not load_env_file():
        print("⚠️  No .env file found")
    
    # Get API keys
    news_api_key = os.environ.get("NEWS_API_KEY")
    
    if news_api_key:
        print(f"✅ NewsAPI key loaded: {news_api_key[:10]}...")
    else:
        print("❌ NEWS_API_KEY not found - news monitoring limited")
    
    print("")
    
    # Get current prices
    print("📊 CURRENT ENERGY PRICES:")
    print("-" * 70)
    crude_prices = get_crude_prices()
    
    for commodity, data in crude_prices.items():
        change_emoji = "📈" if data["change"] > 0 else "📉" if data["change"] < 0 else "➡️"
        print(f"{commodity}: ${data['current']:.2f} {change_emoji} {data['change']:+.2f}")
        print(f"   Volatility: {data['volatility']} | Catalyst: {data['news_catalyst']}")
        print(f"   Support: ${data['support']:.2f} | Resistance: ${data['resistance']:.2f}")
        print("")
    
    # Get war news
    print("📰 GEOPOLITICAL NEWS MONITOR:")
    print("-" * 70)
    news_articles = get_war_news(news_api_key)
    
    if news_articles:
        print(f"✅ {len(news_articles)} relevant articles found")
    else:
        print("⚠️  No news articles retrieved (API issue or no relevant news)")
    
    print("")
    
    # Analyze Kalshi opportunities
    print("🎯 KALSHI TRADING OPPORTUNITIES:")
    print("-" * 70)
    opportunities, high_impact_news = analyze_kalshi_opportunities(crude_prices, news_articles)
    
    if not opportunities:
        print("❌ No clear opportunities identified")
        print("   Monitor for price breaks or news catalysts")
    else:
        total_confidence = 0
        high_urgency_count = 0
        
        for i, opp in enumerate(opportunities, 1):
            urgency_emoji = "🚨" if opp.get("urgency") == "VERY HIGH" else "⚠️" if opp.get("urgency") == "HIGH" else "📊"
            category_emoji = "🛢️" if opp["category"] == "CRUDE" else "⛽" if opp["category"] == "GASOLINE" else "📰"
            
            print(f"{i}. {urgency_emoji} {category_emoji} {opp['market']}")
            print(f"   📈 Type: {opp['type']}")
            if opp['type'] != 'SPECIAL':
                print(f"   📊 Current: ${opp['current_price']:.2f} | Target: ${opp['threshold']:.2f}")
            else:
                print(f"   📊 Current: {opp['current_price']} | Target: {opp['threshold']}")
            print(f"   🎯 Recommendation: {opp['recommendation']}")
            print(f"   💪 Confidence: {opp['confidence']}%")
            print(f"   ⏰ Timeframe: {opp['timeframe']}")
            print(f"   📝 Rationale: {opp['rationale']}")
            print("")
            
            total_confidence += opp['confidence']
            if opp.get('urgency') in ["HIGH", "VERY HIGH"]:
                high_urgency_count += 1
        
        avg_confidence = total_confidence / len(opportunities) if opportunities else 0
        
        print("=" * 70)
        print(f"📈 OPPORTUNITIES FOUND: {len(opportunities)}")
        print(f"🎯 AVERAGE CONFIDENCE: {avg_confidence:.1f}%")
        print(f"🚨 HIGH URGENCY: {high_urgency_count}")
        print(f"⏰ NEXT UPDATE: In 2 hours (continuous monitoring)")
        print("=" * 70)
    
    # High-impact news summary
    if high_impact_news:
        print("")
        print("🚨 HIGH-IMPACT NEWS DETECTED:")
        print("-" * 70)
        for i, news in enumerate(high_impact_news[:3], 1):
            print(f"{i}. {news['title'][:80]}...")
            print(f"   Source: {news['source']} | Impact: {news['impact']}")
            print(f"   Trading: {news['trading_implication']}")
            print("")
    
    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "crude_prices": crude_prices,
        "opportunities_found": len(opportunities),
        "high_impact_news": len(high_impact_news),
        "opportunities": opportunities,
        "news_samples": high_impact_news[:3] if high_impact_news else []
    }
    
    os.makedirs("logs/war_monitor", exist_ok=True)
    output_file = f"logs/war_monitor/war-monitor-{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ Monitor complete - results saved to {output_file}")
    
    # Create alert if high urgency opportunities
    if high_urgency_count > 0:
        print("")
        print("🚨 IMMEDIATE ACTION RECOMMENDED:")
        print("-" * 70)
        print("1. Check Kalshi for corresponding markets")
        print("2. Set alerts for price threshold breaks")
        print("3. Consider small position to test thesis")
        print("4. Monitor news for further developments")

if __name__ == "__main__":
    main()