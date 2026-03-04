#!/usr/bin/env python3
"""
Kalshi Discrepancy Analyzer
Compares Kalshi market odds against current news to find trading opportunities
"""

import re
import json
import requests
from datetime import datetime
from collections import defaultdict

# API Keys
NEWS_API_KEY = "4eb2186b017a49c38d6f6ded502dd55b"
NEWSDATA_API_KEY = "pub_fb29ca627ef54173a0675b2413523744"

def parse_kalshi_data(text):
    """Parse the Kalshi market data from text"""
    markets = []
    
    # Split by market sections
    lines = text.split('\n')
    current_market = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # Look for market headers (contains $ and vol)
        if '$' in line and 'vol' in line:
            # This is a market header
            # Find the question (previous lines)
            question = ""
            for j in range(i-1, max(i-4, -1), -1):
                if lines[j].strip() and '$' not in lines[j] and 'vol' not in lines[j]:
                    question = lines[j].strip()
                    break
            
            if question and '?' in question:
                # Parse volume
                vol_match = re.search(r'\$([\d,]+)', line)
                volume = int(vol_match.group(1).replace(',', '')) if vol_match else 0
                
                current_market = {
                    'question': question,
                    'volume': volume,
                    'options': []
                }
                markets.append(current_market)
        
        # Look for options (contains x and %)
        elif current_market and ('x' in line or '%' in line):
            # Parse option line like "Fed maintains rate 1.02x 98%"
            parts = line.split()
            if len(parts) >= 3:
                # Find the multiplier and probability
                multiplier = None
                probability = None
                option_text = []
                
                for part in parts:
                    if 'x' in part and part.replace('x', '').replace('.', '').isdigit():
                        multiplier = float(part.replace('x', ''))
                    elif '%' in part and part.replace('%', '').replace('.', '').isdigit():
                        probability = float(part.replace('%', ''))
                    else:
                        option_text.append(part)
                
                if multiplier and probability:
                    option = {
                        'text': ' '.join(option_text),
                        'multiplier': multiplier,
                        'probability': probability,
                        'implied_probability': 100 / multiplier if multiplier > 0 else 0
                    }
                    current_market['options'].append(option)
    
    return markets

def get_news_for_topic(topic):
    """Get news articles for a specific topic"""
    try:
        # Try News API first
        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": NEWS_API_KEY,
            "q": topic,
            "pageSize": 5,
            "sortBy": "relevancy",
            "language": "en"
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                articles = data.get("articles", [])
                return [{
                    "title": a.get("title", ""),
                    "description": a.get("description", ""),
                    "source": a.get("source", {}).get("name", ""),
                    "url": a.get("url", ""),
                    "published": a.get("publishedAt", "")
                } for a in articles]
    except:
        pass
    
    return []

def analyze_sentiment(text, articles):
    """Analyze sentiment based on news articles"""
    if not articles:
        return "NEUTRAL", 0
    
    text_lower = text.lower()
    
    # Keywords for positive/negative sentiment
    positive_words = ["strong", "beat", "rise", "gain", "approve", "win", "surge", "increase", "up", "positive", "good", "bullish", "optimistic"]
    negative_words = ["weak", "miss", "fall", "drop", "reject", "lose", "plunge", "decrease", "down", "negative", "bad", "bearish", "pessimistic"]
    
    # Check articles for sentiment
    positive_count = 0
    negative_count = 0
    total_relevant = 0
    
    for article in articles:
        content = (article["title"] + " " + article["description"]).lower()
        
        # Check if article is relevant to the topic
        if any(word in content for word in text_lower.split()[:5]):
            total_relevant += 1
            
            # Count positive/negative words
            pos = sum(1 for word in positive_words if word in content)
            neg = sum(1 for word in negative_words if word in content)
            
            positive_count += pos
            negative_count += neg
    
    if total_relevant == 0:
        return "NEUTRAL", 0
    
    sentiment_score = (positive_count - negative_count) / total_relevant
    
    if sentiment_score > 0.5:
        return "STRONGLY_POSITIVE", sentiment_score
    elif sentiment_score > 0.1:
        return "POSITIVE", sentiment_score
    elif sentiment_score < -0.5:
        return "STRONGLY_NEGATIVE", sentiment_score
    elif sentiment_score < -0.1:
        return "NEGATIVE", sentiment_score
    else:
        return "NEUTRAL", sentiment_score

def find_discrepancies(market, sentiment, sentiment_score):
    """Find discrepancies between market odds and news sentiment"""
    discrepancies = []
    
    for option in market['options']:
        market_prob = option['probability']
        implied_prob = option['implied_probability']
        
        # Calculate expected probability based on sentiment
        if sentiment == "STRONGLY_POSITIVE":
            expected_prob = min(90, market_prob + 30)
        elif sentiment == "POSITIVE":
            expected_prob = min(80, market_prob + 20)
        elif sentiment == "STRONGLY_NEGATIVE":
            expected_prob = max(10, market_prob - 30)
        elif sentiment == "NEGATIVE":
            expected_prob = max(20, market_prob - 20)
        else:
            expected_prob = market_prob  # Neutral
        
        # Calculate discrepancy
        discrepancy = expected_prob - market_prob
        
        if abs(discrepancy) > 15:  # Significant discrepancy
            confidence = min(90, abs(discrepancy) * 2)
            
            # Determine trade recommendation
            if discrepancy > 0:
                action = "BUY YES" if "YES" in option['text'].upper() else "BUY"
                reasoning = f"News sentiment ({sentiment}) suggests higher probability than market ({market_prob}% → expected {expected_prob:.1f}%)"
            else:
                action = "BUY NO" if "NO" in option['text'].upper() else "SELL"
                reasoning = f"News sentiment ({sentiment}) suggests lower probability than market ({market_prob}% → expected {expected_prob:.1f}%)"
            
            discrepancies.append({
                'market_question': market['question'],
                'option': option['text'],
                'market_probability': market_prob,
                'expected_probability': expected_prob,
                'discrepancy': discrepancy,
                'sentiment': sentiment,
                'sentiment_score': sentiment_score,
                'action': action,
                'reasoning': reasoning,
                'confidence': confidence,
                'volume': market['volume'],
                'multiplier': option['multiplier']
            })
    
    return discrepancies

def main():
    print("=" * 80)
    print("KALSHI DISCREPANCY ANALYZER")
    print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    # Read the Kalshi data file
    try:
        with open('/Users/cubiczan/.openclaw/media/inbound/21cb8e01-a5c3-417d-a27c-144a726518a7.txt', 'r') as f:
            kalshi_text = f.read()
    except:
        print("Error reading Kalshi data file")
        return
    
    # Parse markets
    print("📊 Parsing Kalshi market data...")
    markets = parse_kalshi_data(kalshi_text)
    print(f"   Found {len(markets)} markets with options")
    
    # Filter for high-volume markets
    high_volume_markets = [m for m in markets if m['volume'] > 1000000]
    print(f"   {len(high_volume_markets)} markets with volume > $1M")
    
    print()
    print("📰 Analyzing news sentiment for top markets...")
    
    all_discrepancies = []
    
    # Analyze top 10 high-volume markets
    for i, market in enumerate(high_volume_markets[:10], 1):
        print(f"   {i}. {market['question'][:60]}... (${market['volume']:,})")
        
        # Get news for this market
        topic = market['question'].split('?')[0]
        articles = get_news_for_topic(topic)
        
        # Analyze sentiment
        sentiment, score = analyze_sentiment(topic, articles)
        
        # Find discrepancies
        discrepancies = find_discrepancies(market, sentiment, score)
        
        if discrepancies:
            all_discrepancies.extend(discrepancies)
            print(f"     Found {len(discrepancies)} discrepancies")
        else:
            print(f"     No significant discrepancies")
    
    print()
    print("=" * 80)
    print("🎯 HIGH-CONFIDENCE TRADE RECOMMENDATIONS")
    print("=" * 80)
    
    if all_discrepancies:
        # Sort by confidence and discrepancy size
        all_discrepancies.sort(key=lambda x: (x['confidence'], abs(x['discrepancy'])), reverse=True)
        
        # Show top 5 recommendations
        for i, disc in enumerate(all_discrepancies[:5], 1):
            print(f"\n{i}. {disc['market_question'][:70]}...")
            print(f"   📈 Option: {disc['option']}")
            print(f"   📊 Market Probability: {disc['market_probability']}%")
            print(f"   🎯 Expected Probability: {disc['expected_probability']:.1f}%")
            print(f"   ⚖️ Discrepancy: {disc['discrepancy']:+.1f}%")
            print(f"   😊 Sentiment: {disc['sentiment']} (score: {disc['sentiment_score']:.2f})")
            print(f"   🎯 Action: {disc['action']}")
            print(f"   💰 Multiplier: {disc['multiplier']}x")
            print(f"   📈 Volume: ${disc['volume']:,}")
            print(f"   ✅ Confidence: {disc['confidence']:.0f}%")
            print(f"   📝 Reasoning: {disc['reasoning']}")
            
            # Calculate expected value
            if disc['action'].startswith("BUY"):
                cost_per_contract = 100  # $1 per contract
                potential_payout = cost_per_contract * disc['multiplier']
                expected_value = (disc['expected_probability'] / 100) * potential_payout - cost_per_contract
                print(f"   💵 Expected Value: ${expected_value:.2f} per $1 bet")
    
    else:
        print("\n❌ No significant discrepancies found.")
        print("   Markets appear efficiently priced relative to current news.")
    
    print()
    print("=" * 80)
    print("📋 ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"Markets analyzed: {len(high_volume_markets[:10])}")
    print(f"Discrepancies found: {len(all_discrepancies)}")
    print(f"Top recommendation confidence: {all_discrepancies[0]['confidence'] if all_discrepancies else 0:.0f}%")
    print()
    print("💡 TRADING STRATEGY:")
    print("1. Focus on highest confidence discrepancies (>70%)")
    print("2. Consider market volume for liquidity")
    print("3. Monitor news for sentiment changes")
    print("4. Use appropriate position sizing")
    print()
    print(f"Next update: {datetime.now().strftime('%H:%M')}")

if __name__ == "__main__":
    main()
