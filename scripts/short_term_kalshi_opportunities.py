#!/usr/bin/env python3
"""
Short-Term Kalshi Opportunities (<30 days settlement)
Focus on markets that settle within 30 days for quicker turnaround
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta

# API Keys
NEWS_API_KEY = "4eb2186b017a49c38d6f6ded502dd55b"
NEWSDATA_API_KEY = "pub_fb29ca627ef54173a0675b2413523744"

# Available capital
AVAILABLE_CAPITAL = 220

def fetch_short_term_catalysts():
    """Fetch news for short-term trading catalysts (next 30 days)"""
    print("📰 Fetching short-term news catalysts...")
    all_articles = []
    
    # Focus on events happening in next 30 days
    time_periods = [
        ("this week", 7),
        ("next week", 14),
        ("this month", 30),
        ("March", 25),  # Rest of March
        ("by April", 30)
    ]
    
    # News API - search for time-bound events
    for time_period, days in time_periods:
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "apiKey": NEWS_API_KEY,
                "q": f"{time_period} deadline decision vote report earnings",
                "pageSize": 10,
                "sortBy": "relevancy",
                "language": "en"
            }
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ok":
                    articles = data.get("articles", [])
                    for article in articles:
                        article["time_period"] = time_period
                        article["days_horizon"] = days
                        article["source_api"] = "newsapi"
                    all_articles.extend(articles)
                    print(f"✅ {time_period} ({days} days): {len(articles)} articles")
            time.sleep(1)
        except Exception as e:
            print(f"❌ News API error for {time_period}: {e}")
    
    # Newsdata.io - specific short-term categories
    try:
        url = "https://newsdata.io/api/1/news"
        params = {
            "apikey": NEWSDATA_API_KEY,
            "category": "business,politics",
            "language": "en",
            "size": 20,
            "timeframe": "48"  # Last 48 hours
        }
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                articles = data.get("results", [])
                for article in articles:
                    article["source_api"] = "newsdata"
                    article["title"] = article.get("title", "")
                    article["description"] = article.get("description", "")
                    article["url"] = article.get("link", "")
                    article["publishedAt"] = article.get("pubDate", "")
                    article["source"] = {"name": article.get("source_id", "Unknown")}
                    article["time_period"] = "short-term"
                    article["days_horizon"] = 14  # Default 2 weeks
                all_articles.extend(articles)
                print(f"✅ Newsdata.io (48h): {len(articles)} articles")
    except Exception as e:
        print(f"❌ Newsdata.io error: {e}")
    
    print(f"📊 Total short-term articles: {len(all_articles)}")
    return all_articles

def identify_short_term_markets(articles):
    """Identify Kalshi markets with <30 day settlement"""
    print("\n🔍 Identifying <30 day markets...")
    
    short_term_categories = {
        "WEEKLY_SETTLEMENTS": {
            "keywords": ["this week", "weekly", "Friday close", "end of week", "weekend"],
            "timeframe": "3-7 days",
            "probability": 0.75,
            "examples": [
                "Will [event] happen this week?",
                "Will [metric] close above [level] on Friday?",
                "Weekly economic data reports"
            ]
        },
        "BIWEEKLY": {
            "keywords": ["next week", "two weeks", "fortnight", "by next Friday"],
            "timeframe": "7-14 days",
            "probability": 0.70,
            "examples": [
                "Will [bill] pass by next week?",
                "Will [report] be released within 2 weeks?",
                "Short-term political decisions"
            ]
        },
        "MONTH_END": {
            "keywords": ["end of month", "March", "by April", "monthly", "EOY"],
            "timeframe": "15-30 days",
            "probability": 0.65,
            "examples": [
                "Will [target] be reached by month-end?",
                "Monthly economic indicators",
                "End-of-month deadlines"
            ]
        },
        "IMMINENT_EVENTS": {
            "keywords": ["tomorrow", "today", "imminent", "urgent", "deadline", "hours"],
            "timeframe": "1-3 days",
            "probability": 0.80,
            "examples": [
                "Will [announcement] happen today/tomorrow?",
                "Immediate market reactions",
                "Breaking news outcomes"
            ]
        }
    }
    
    opportunities = []
    
    for article in articles:
        title = article.get("title", "") or ""
        description = article.get("description", "") or ""
        content = f"{title.lower()} {description.lower()}"
        time_period = article.get("time_period", "")
        days_horizon = article.get("days_horizon", 30)
        
        # Skip if horizon > 30 days
        if days_horizon > 30:
            continue
        
        for category, info in short_term_categories.items():
            score = 0
            matched_keywords = []
            
            for keyword in info["keywords"]:
                if keyword.lower() in content or keyword.lower() in time_period.lower():
                    score += 2  # Higher weight for timeframe keywords
                    matched_keywords.append(keyword)
            
            # Also check for specific short-term indicators
            short_term_indicators = ["deadline", "vote", "decision", "report", "earnings", "meeting"]
            for indicator in short_term_indicators:
                if indicator in content:
                    score += 1
                    matched_keywords.append(indicator)
            
            if score >= 3:  # Good match for short-term
                confidence = info["probability"]
                
                # Boost for very short timeframes
                if info["timeframe"] == "1-3 days":
                    confidence *= 1.3
                elif info["timeframe"] == "3-7 days":
                    confidence *= 1.2
                elif info["timeframe"] == "7-14 days":
                    confidence *= 1.1
                
                # Source reliability
                source = article.get("source", {}).get("name", "").lower()
                reliable_sources = ["reuters", "bloomberg", "cnbc", "wsj", "financial times"]
                if any(rel_source in source for rel_source in reliable_sources):
                    confidence *= 1.15
                
                opportunity = {
                    "category": category,
                    "timeframe": info["timeframe"],
                    "days_horizon": days_horizon,
                    "title": title[:150],
                    "confidence": min(confidence, 0.95),
                    "matched_keywords": matched_keywords,
                    "market_examples": info["examples"],
                    "news_source": source,
                    "published": article.get("publishedAt", "")[:10]
                }
                opportunities.append(opportunity)
                break  # Only assign to one category
    
    # Sort by timeframe (shortest first) then confidence
    opportunities.sort(key=lambda x: (x["days_horizon"], -x["confidence"]))
    
    print(f"🎯 Found {len(opportunities)} short-term (<30 day) opportunities")
    return opportunities[:8]  # Top 8

def create_short_term_trading_plan(opportunities, available_capital):
    """Create trading plan for short-term opportunities"""
    print("\n💰 Creating short-term trading plan...")
    
    trading_plan = {
        "available_capital": available_capital,
        "timeframe": "<30 days",
        "total_allocated": 0,
        "opportunities": []
    }
    
    # Group by timeframe
    timeframe_groups = {}
    for opp in opportunities:
        timeframe = opp["timeframe"]
        if timeframe not in timeframe_groups:
            timeframe_groups[timeframe] = []
        timeframe_groups[timeframe].append(opp)
    
    # Allocate capital by timeframe (shorter = more capital)
    timeframe_allocation = {
        "1-3 days": 0.40,   # 40% to 1-3 day trades
        "3-7 days": 0.30,   # 30% to weekly trades
        "7-14 days": 0.20,  # 20% to biweekly trades
        "15-30 days": 0.10  # 10% to month-end trades
    }
    
    capital_by_timeframe = {}
    for timeframe, percentage in timeframe_allocation.items():
        capital_by_timeframe[timeframe] = available_capital * percentage
    
    # Distribute opportunities
    for timeframe, opps in timeframe_groups.items():
        if timeframe not in capital_by_timeframe:
            capital_by_timeframe[timeframe] = available_capital * 0.10  # Default 10%
        
        capital_available = capital_by_timeframe[timeframe]
        num_opps = len(opps)
        
        if num_opps > 0:
            capital_per_opp = capital_available / num_opps
            
            for i, opp in enumerate(opps):
                # Adjust allocation based on confidence
                allocation = capital_per_opp * (opp["confidence"] / 0.7)  # Scale around 70% baseline
                allocation = min(allocation, available_capital * 0.25)  # Max 25% per trade
                allocation = round(allocation, 2)
                
                trade = {
                    "timeframe": opp["timeframe"],
                    "days": opp["days_horizon"],
                    "category": opp["category"],
                    "confidence": opp["confidence"],
                    "allocation": allocation,
                    "title": opp["title"],
                    "market_examples": opp["market_examples"][:2],  # Top 2 examples
                    "keywords": opp["matched_keywords"][:5]
                }
                
                trading_plan["opportunities"].append(trade)
                trading_plan["total_allocated"] += allocation
    
    # Ensure we don't overallocate
    if trading_plan["total_allocated"] > available_capital:
        scale_factor = available_capital / trading_plan["total_allocated"]
        for trade in trading_plan["opportunities"]:
            trade["allocation"] = round(trade["allocation"] * scale_factor, 2)
        trading_plan["total_allocated"] = available_capital
    
    return trading_plan

def main():
    """Main function"""
    print("======================================================================")
    print("🎯 SHORT-TERM KALSHI OPPORTUNITIES (<30 DAYS)")
    print("======================================================================")
    print(f"💰 Available Capital: ${AVAILABLE_CAPITAL}")
    print(f"⏰ Timeframe: Less than 30 days to settlement")
    print(f"📅 Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Fetch short-term catalysts
    articles = fetch_short_term_catalysts()
    
    if not articles:
        print("❌ No articles fetched. Exiting.")
        return
    
    # Step 2: Identify short-term markets
    opportunities = identify_short_term_markets(articles)
    
    if not opportunities:
        print("❌ No short-term opportunities identified.")
        print("   Consider waiting for next week's gas price trades.")
        return
    
    # Step 3: Create trading plan
    trading_plan = create_short_term_trading_plan(opportunities, AVAILABLE_CAPITAL)
    
    # Step 4: Display results
    print("\n" + "="*70)
    print("📊 SHORT-TERM TRADING PLAN")
    print("="*70)
    
    print(f"\n💰 CAPITAL ALLOCATION:")
    print(f"   Available: ${AVAILABLE_CAPITAL}")
    print(f"   To Deploy: ${trading_plan['total_allocated']:.2f}")
    print(f"   To Reserve: ${AVAILABLE_CAPITAL - trading_plan['total_allocated']:.2f}")
    
    print("\n🎯 OPPORTUNITIES BY TIMEFRAME:")
    print("-"*70)
    
    # Group by timeframe for display
    by_timeframe = {}
    for trade in trading_plan["opportunities"]:
        timeframe = trade["timeframe"]
        if timeframe not in by_timeframe:
            by_timeframe[timeframe] = []
        by_timeframe[timeframe].append(trade)
    
    for timeframe in ["1-3 days", "3-7 days", "7-14 days", "15-30 days"]:
        if timeframe in by_timeframe:
            trades = by_timeframe[timeframe]
            total_allocated = sum(t["allocation"] for t in trades)
            
            print(f"\n⏰ {timeframe.upper()} (${total_allocated:.2f}):")
            for trade in trades:
                print(f"   • ${trade['allocation']} - {trade['title'][:80]}...")
                print(f"     Confidence: {trade['confidence']*100:.0f}% | Keywords: {', '.join(trade['keywords'][:3])}")
    
    print("\n" + "="*70)
    print("⚡ QUICK ACTION PLAN:")
    print("="*70)
    
    print("\n1. SEARCH KALSHI FOR:")
    print("   • 'this week' markets")
    print("   • 'next week' markets")
    print("   • 'end of month' markets")
    print("   • Weekly settlement markets")
    
    print("\n2. PRIORITIZE MARKETS THAT:")
    print("   • Settle within 30 days")
    print("   • Have clear yes/no outcomes")
    print("   • Match news catalysts")
    print("   • Have good liquidity")
    
    print("\n3. CAPITAL ALLOCATION:")
    for timeframe, percentage in [("1-3 days", "40%"), ("3-7 days", "30%"), ("7-14 days", "20%"), ("15-30 days", "10%")]:
        amount = AVAILABLE_CAPITAL * {"40%": 0.4, "30%": 0.3, "20%": 0.2, "10%": 0.1}[percentage]
        print(f"   • {timeframe}: ${amount:.2f} ({percentage})")
    
    print("\n4. GAS PRICE TRADES (Next Week):")
    print("   • Wait for Monday 6 AM reminder")
    print("   • Check AAA gas price Monday morning")
    print("   • Look for weekly gas price markets")
    print("   • Consider range trades ($3.15-$3.35)")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    results_file = f"/Users/cubiczan/.openclaw/workspace/kalshi_opportunities/short_term_{timestamp}.json"
    
    results_data = {
        "timestamp": datetime.now().isoformat(),
        "available_capital": AVAILABLE_CAPITAL,
        "timeframe": "<30 days",
        "trading_plan": trading_plan,
        "opportunities_found": len(opportunities)
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
    
    if trading_plan["total_allocated"] > 0:
        print(f"\n🎯 ACTION: Deploy ${trading_plan['total_allocated']:.2f} in short-term trades")
        print(f"⏰ FOCUS: Markets settling within 30 days")
        print(f"📊 TARGET: Quick 20-40% returns")
    else:
        print(f"\n⚠️  CONSIDER: Waiting for next week's gas price trades")
        print(f"📅 NEXT: Monday 6 AM gas trading reminder")
        print(f"💰 PREPARE: $220 ready for Monday deployment")

if __name__ == "__main__":
    main()