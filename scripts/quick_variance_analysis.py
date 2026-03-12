#!/usr/bin/env python3
"""
Quick probabilistic variance analysis for Kalshi trades
"""

import os
import sys
import json
from datetime import datetime

def analyze_variance():
    """Analyze current probabilistic variance opportunities"""
    print("🎯 KALSHI PROBABILISTIC VARIANCE ANALYSIS")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("💰 Available Capital: $47.00")
    print("=" * 60)
    
    # Current portfolio status
    portfolio_path = "/Users/cubiczan/.openclaw/workspace/portfolio_reports/portfolio_data.json"
    if os.path.exists(portfolio_path):
        with open(portfolio_path, 'r') as f:
            portfolio = json.load(f)
        
        total_invested = portfolio.get('total_invested', 0)
        available = 47 - total_invested
        print(f"\n📊 PORTFOLIO STATUS:")
        print(f"  Invested: ${total_invested}")
        print(f"  Available: ${available}")
        print(f"  Active Trades: {portfolio.get('active_trades_count', 0)}")
        print(f"  Total Profit: ${portfolio.get('total_profit', 0):.2f}")
    else:
        available = 47
        print("\n📊 PORTFOLIO STATUS: No portfolio file found")
        print(f"  Available: ${available}")
    
    print("\n🔍 PROBABILISTIC VARIANCE OPPORTUNITIES:")
    print("-" * 40)
    
    opportunities = []
    
    # 1. Gas Price Variance Analysis
    print("\n1. ⛽ GAS PRICE VARIANCE:")
    
    # Current gas prices from different sources (simulated)
    gas_sources = {
        "AAA National": 3.198,  # From portfolio
        "EIA Weekly": 3.21,
        "GasBuddy Avg": 3.22,
        "OPIS Wholesale": 3.19,
        "Bloomberg": 3.205,
    }
    
    # Calculate statistics
    prices = list(gas_sources.values())
    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)
    variance = max_price - min_price
    
    print(f"   Sources: {len(gas_sources)}")
    print(f"   Average: ${avg_price:.3f}")
    print(f"   Range: ${min_price:.3f} - ${max_price:.3f}")
    print(f"   Variance: ${variance:.3f}")
    
    # Kalshi comparison
    kalshi_target = 3.50
    needed = kalshi_target - avg_price
    variance_pct = (variance / avg_price) * 100
    
    print(f"\n   🎯 Kalshi Gas Month Target: ${kalshi_target:.3f}")
    print(f"   Current Avg: ${avg_price:.3f}")
    print(f"   Needed: ${needed:.3f}")
    print(f"   Source Variance: {variance_pct:.1f}%")
    
    if variance > 0.03 and needed > 0.15:
        confidence = min(100, variance_pct * 15 + needed * 100)
        opp = {
            "type": "gas_price_variance",
            "confidence": confidence,
            "recommendation": "BUY YES on Gas Month >$3.50",
            "position": "$8-12",
            "reason": f"${variance:.3f} variance across sources, ${needed:.3f} to target"
        }
        opportunities.append(opp)
        print(f"   ✅ OPPORTUNITY: Confidence {confidence:.0f}%")
    
    # 2. Weather Forecast Variance
    print("\n2. 🌤️ WEATHER FORECAST VARIANCE:")
    
    # Chicago temperature forecasts
    chi_forecasts = [45, 46, 44, 45, 47]  # Different sources
    chi_avg = sum(chi_forecasts) / len(chi_forecasts)
    chi_variance = max(chi_forecasts) - min(chi_forecasts)
    chi_target = 45.5
    
    print(f"   Chicago Forecasts: {chi_avg:.1f}°F avg")
    print(f"   Forecast Variance: {chi_variance}°F")
    print(f"   Kalshi Target: {chi_target}°F")
    print(f"   Difference: {chi_target - chi_avg:.1f}°F")
    
    if chi_variance >= 2 and chi_avg < chi_target - 0.5:
        confidence = min(100, (3 - chi_variance) * 25)
        opp = {
            "type": "weather_variance_chicago",
            "confidence": confidence,
            "recommendation": "BUY NO on Chicago >45.5°F",
            "position": "$5-8",
            "reason": f"{chi_variance}°F forecast variance, avg {chi_avg:.1f}°F below target"
        }
        opportunities.append(opp)
        print(f"   ✅ OPPORTUNITY: Confidence {confidence:.0f}%")
    
    # Miami temperature forecasts
    mia_forecasts = [82, 83, 81, 82, 84]
    mia_avg = sum(mia_forecasts) / len(mia_forecasts)
    mia_variance = max(mia_forecasts) - min(mia_forecasts)
    mia_target = 82.5
    
    print(f"\n   Miami Forecasts: {mia_avg:.1f}°F avg")
    print(f"   Forecast Variance: {mia_variance}°F")
    print(f"   Kalshi Target: {mia_target}°F")
    print(f"   Difference: {mia_target - mia_avg:.1f}°F")
    
    if mia_variance >= 2 and mia_avg < mia_target - 0.5:
        confidence = min(100, (3 - mia_variance) * 25)
        opp = {
            "type": "weather_variance_miami",
            "confidence": confidence,
            "recommendation": "BUY NO on Miami >82.5°F",
            "position": "$5-8",
            "reason": f"{mia_variance}°F forecast variance, avg {mia_avg:.1f}°F below target"
        }
        opportunities.append(opp)
        print(f"   ✅ OPPORTUNITY: Confidence {confidence:.0f}%")
    
    # 3. News Sentiment Variance
    print("\n3. 📰 NEWS SENTIMENT VARIANCE:")
    
    # Simulated news sentiment
    news_sources = {
        "Reuters": 0.7,
        "Bloomberg": 0.6,
        "CNBC": 0.8,
        "WSJ": 0.5,
        "FT": 0.65,
    }
    
    sentiments = list(news_sources.values())
    avg_sentiment = sum(sentiments) / len(sentiments)
    sentiment_variance = max(sentiments) - min(sentiments)
    
    print(f"   Sources: {len(news_sources)}")
    print(f"   Avg Sentiment: {avg_sentiment:.2f}")
    print(f"   Sentiment Variance: {sentiment_variance:.2f}")
    print(f"   Iran Articles: 5 (simulated)")
    
    if sentiment_variance > 0.2 and avg_sentiment > 0.6:
        confidence = min(100, avg_sentiment * 100)
        opp = {
            "type": "news_sentiment_variance",
            "confidence": confidence,
            "recommendation": "BUY YES on gas/oil markets",
            "position": "$10-15",
            "reason": f"High sentiment variance ({sentiment_variance:.2f}) with bullish avg ({avg_sentiment:.2f})"
        }
        opportunities.append(opp)
        print(f"   ✅ OPPORTUNITY: Confidence {confidence:.0f}%")
    
    # 4. Portfolio Concentration Variance
    print("\n4. 📊 PORTFOLIO CONCENTRATION VARIANCE:")
    
    if 'portfolio' in locals():
        trades = portfolio.get('trades', [])
        gas_trades = [t for t in trades if "gas" in t.get('market', '').lower()]
        gas_investment = sum(t.get('size', 0) for t in gas_trades if t.get('status') == 'active')
        gas_pct = (gas_investment / total_invested * 100) if total_invested > 0 else 0
        
        print(f"   Gas Concentration: {gas_pct:.0f}%")
        print(f"   Available for Diversification: ${available}")
        
        if gas_pct > 70 and available > 10:
            confidence = 60
            opp = {
                "type": "portfolio_diversification",
                "confidence": confidence,
                "recommendation": "Diversify into weather/political markets",
                "position": f"${min(10, available)}",
                "reason": f"High gas concentration ({gas_pct:.0f}%), reduce variance"
            }
            opportunities.append(opp)
            print(f"   ✅ OPPORTUNITY: Confidence {confidence:.0f}%")
    
    # Generate overall recommendation
    print("\n" + "=" * 60)
    print("🎯 OVERALL RECOMMENDATION")
    print("=" * 60)
    
    if not opportunities:
        print("\n❌ No strong probabilistic variance opportunities found")
        print("\n💡 Consider:")
        print("  • Wait for better price discrepancies")
        print("  • Monitor breaking news")
        print("  • Small position ($5) in weather if confident")
        return
    
    # Sort by confidence
    opportunities.sort(key=lambda x: x['confidence'], reverse=True)
    
    print(f"\n📈 Found {len(opportunities)} variance opportunities:")
    
    for i, opp in enumerate(opportunities, 1):
        print(f"\n{i}. {opp['type'].replace('_', ' ').title()}:")
        print(f"   Confidence: {opp['confidence']:.0f}%")
        print(f"   Recommendation: {opp['recommendation']}")
        print(f"   Position: {opp['position']}")
        print(f"   Reason: {opp['reason']}")
    
    # Calculate overall metrics
    avg_confidence = sum(o['confidence'] for o in opportunities) / len(opportunities)
    best_opp = opportunities[0]
    
    print(f"\n📊 OVERALL METRICS:")
    print(f"   Average Confidence: {avg_confidence:.0f}%")
    print(f"   Best Opportunity: {best_opp['type'].replace('_', ' ').title()}")
    print(f"   Best Confidence: {best_opp['confidence']:.0f}%")
    
    # Determine action
    if avg_confidence >= 65:
        action = "STRONG BUY"
        position = best_opp['position']
    elif avg_confidence >= 50:
        action = "MODERATE BUY"
        position = best_opp['position']
    elif avg_confidence >= 40:
        action = "SMALL BUY or HOLD"
        position = "$5"
    else:
        action = "HOLD"
        position = "$0"
    
    print(f"\n🎯 FINAL RECOMMENDATION:")
    print(f"   Action: {action}")
    print(f"   Position: {position}")
    print(f"   Focus: {best_opp['recommendation']}")
    
    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "opportunities": opportunities,
        "overall_recommendation": {
            "action": action,
            "position": position,
            "avg_confidence": avg_confidence,
            "best_opportunity": best_opp['type']
        }
    }
    
    output_file = "/Users/cubiczan/.openclaw/workspace/variance_analysis.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Analysis saved to: {output_file}")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Review detailed analysis above")
    print("2. Check current market prices on Kalshi")
    print("3. Verify forecasts with real-time data")
    print("4. Execute trade if confidence > 60%")
    print("5. Set stop-loss at 20-30% of position")

if __name__ == "__main__":
    analyze_variance()