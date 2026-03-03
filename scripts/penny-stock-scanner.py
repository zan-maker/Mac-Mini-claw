#!/usr/bin/env python3
"""
Penny Stock Scanner - Daily Recommendations for Tasty Trade
Scans for penny stocks ($0.10-$5.00) with high potential
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import numpy as np

# Discord webhook for alerts
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1471852327978795091/YOUR_WEBHOOK_HERE"

# Penny stock criteria
MIN_PRICE = 0.10
MAX_PRICE = 5.00
MIN_VOLUME = 500000  # shares
MIN_DOLLAR_VOLUME = 500000  # $500k
MIN_MARKET_CAP = 50000000  # $50M
MAX_MARKET_CAP = 500000000  # $500M

def get_penny_stock_watchlist():
    """
    Get a list of penny stocks to scan
    In production, this would query a screening API
    For now, using a predefined watchlist of active penny stocks
    """
    
    # Common active penny stocks (example list)
    watchlist = [
        # Biotech
        "ATOS", "BNGO", "SENS", "OCGN", "INO",
        # Tech
        "SOS", "MARA", "RIOT", "MSTR", "HUT",
        # Energy
        "CEI", "MMAT", "EEENF", "UEC", "DNN",
        # Meme/Retail
        "AMC", "GME", "BB", "NOK", "BBBY",
        # Cannabis
        "TLRY", "CGC", "ACB", "SNDL", "CRON",
        # EV/Green Energy
        "NKLA", "WKHS", "RIDE", "GOEV", "FCEL",
    ]
    
    return watchlist

def analyze_stock(ticker):
    """Analyze a single stock for penny stock potential"""
    
    try:
        # Get stock data
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Basic checks
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        if not (MIN_PRICE <= current_price <= MAX_PRICE):
            return None
        
        market_cap = info.get('marketCap', 0)
        if not (MIN_MARKET_CAP <= market_cap <= MAX_MARKET_CAP):
            return None
        
        # Get historical data
        hist = stock.history(period="1mo", interval="1d")
        if len(hist) < 20:
            return None
        
        # Calculate metrics
        volume = hist['Volume'].iloc[-1]
        avg_volume = hist['Volume'].rolling(20).mean().iloc[-1]
        dollar_volume = volume * current_price
        
        if volume < MIN_VOLUME or dollar_volume < MIN_DOLLAR_VOLUME:
            return None
        
        # Technical indicators
        close_prices = hist['Close']
        
        # RSI
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        
        # Volume spike
        volume_spike = (volume / avg_volume) * 100 if avg_volume > 0 else 0
        
        # Price change
        price_change_1d = ((close_prices.iloc[-1] - close_prices.iloc[-2]) / close_prices.iloc[-2]) * 100
        price_change_5d = ((close_prices.iloc[-1] - close_prices.iloc[-5]) / close_prices.iloc[-5]) * 100
        
        # ATR (volatility)
        high_low = hist['High'] - hist['Low']
        high_close = np.abs(hist['High'] - hist['Close'].shift())
        low_close = np.abs(hist['Low'] - hist['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(14).mean().iloc[-1]
        atr_percent = (atr / current_price) * 100
        
        # Check for patterns
        pattern = identify_pattern(hist)
        
        # Score the opportunity
        score = calculate_score(
            rsi=rsi,
            volume_spike=volume_spike,
            price_change_1d=price_change_1d,
            price_change_5d=price_change_5d,
            atr_percent=atr_percent,
            pattern=pattern
        )
        
        if score < 60:  # Minimum score threshold
            return None
        
        # Get company info
        company_name = info.get('longName', ticker)
        sector = info.get('sector', 'Unknown')
        industry = info.get('industry', 'Unknown')
        
        # Calculate targets
        target_price, stop_loss = calculate_targets(
            current_price=current_price,
            atr=atr,
            pattern=pattern,
            rsi=rsi
        )
        
        upside = ((target_price - current_price) / current_price) * 100
        risk = ((current_price - stop_loss) / current_price) * 100
        risk_reward = upside / risk if risk > 0 else 0
        
        if risk_reward < 1.5:  # Minimum risk/reward
            return None
        
        return {
            'ticker': ticker,
            'company': company_name,
            'price': round(current_price, 2),
            'change_1d': round(price_change_1d, 1),
            'change_5d': round(price_change_5d, 1),
            'volume': f"{volume:,.0f}",
            'volume_spike': round(volume_spike, 0),
            'market_cap': f"${market_cap:,.0f}",
            'sector': sector,
            'industry': industry,
            'rsi': round(rsi, 1),
            'atr_percent': round(atr_percent, 1),
            'pattern': pattern,
            'score': round(score, 0),
            'target': round(target_price, 2),
            'stop': round(stop_loss, 2),
            'upside': round(upside, 1),
            'risk': round(risk, 1),
            'risk_reward': round(risk_reward, 2),
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error analyzing {ticker}: {e}")
        return None

def identify_pattern(hist):
    """Identify chart patterns"""
    
    close = hist['Close'].values
    high = hist['High'].values
    low = hist['Low'].values
    
    if len(close) < 10:
        return "No clear pattern"
    
    # Simple pattern detection
    recent_close = close[-5:]
    recent_high = high[-5:]
    recent_low = low[-5:]
    
    # Check for breakout
    if close[-1] > max(close[-10:-1]):
        return "Breakout"
    
    # Check for oversold bounce
    if close[-1] > close[-2] and close[-2] < close[-3] and close[-3] < close[-4]:
        return "Oversold bounce"
    
    # Check for momentum
    if all(close[i] > close[i-1] for i in range(-4, 0)):
        return "Uptrend"
    
    return "Consolidation"

def calculate_score(rsi, volume_spike, price_change_1d, price_change_5d, atr_percent, pattern):
    """Calculate opportunity score (0-100)"""
    
    score = 50  # Base score
    
    # RSI scoring (30-70 is ideal)
    if 30 <= rsi <= 70:
        score += 10
    elif 20 <= rsi <= 80:
        score += 5
    
    # Volume spike scoring
    if volume_spike > 150:
        score += 15
    elif volume_spike > 120:
        score += 10
    elif volume_spike > 100:
        score += 5
    
    # Price momentum
    if price_change_1d > 5:
        score += 10
    elif price_change_1d > 2:
        score += 5
    
    if price_change_5d > 10:
        score += 10
    elif price_change_5d > 5:
        score += 5
    
    # Volatility (ATR)
    if 5 <= atr_percent <= 15:
        score += 10  # Good volatility for swings
    
    # Pattern scoring
    pattern_scores = {
        "Breakout": 15,
        "Oversold bounce": 10,
        "Uptrend": 10,
        "Consolidation": 5
    }
    score += pattern_scores.get(pattern, 0)
    
    return min(score, 100)

def calculate_targets(current_price, atr, pattern, rsi):
    """Calculate target price and stop loss"""
    
    if pattern == "Breakout":
        target = current_price * 1.30  # 30% target
        stop = current_price * 0.85    # 15% stop
    elif pattern == "Oversold bounce":
        target = current_price * 1.25  # 25% target
        stop = current_price * 0.88    # 12% stop
    elif pattern == "Uptrend":
        target = current_price * 1.20  # 20% target
        stop = current_price * 0.90    # 10% stop
    else:
        target = current_price * 1.15  # 15% target
        stop = current_price * 0.92    # 8% stop
    
    # Adjust based on ATR
    target = max(target, current_price + (atr * 2))
    stop = min(stop, current_price - (atr * 1.5))
    
    # Adjust based on RSI
    if rsi > 60:
        target = target * 0.95  # Slightly lower target if overbought
    elif rsi < 40:
        stop = stop * 1.05  # Slightly wider stop if oversold
    
    return round(target, 2), round(stop, 2)

def send_discord_alert(stock_data):
    """Send penny stock alert to Discord"""
    
    embed = {
        "title": f"🎯 PENNY STOCK ALERT - {stock_data['ticker']}",
        "description": f"**{stock_data['company']}**",
        "color": 0x00ff00 if stock_data['change_1d'] > 0 else 0xff0000,
        "fields": [
            {
                "name": "📊 Price Action",
                "value": f"**Price:** ${stock_data['price']} ({stock_data['change_1d']}% today)\n"
                        f"**5-day Change:** {stock_data['change_5d']}%\n"
                        f"**Volume:** {stock_data['volume']} ({stock_data['volume_spike']}% of avg)",
                "inline": True
            },
            {
                "name": "📈 Technicals",
                "value": f"**RSI:** {stock_data['rsi']}\n"
                        f"**ATR:** {stock_data['atr_percent']}%\n"
                        f"**Pattern:** {stock_data['pattern']}\n"
                        f"**Score:** {stock_data['score']}/100",
                "inline": True
            },
            {
                "name": "🎯 Trade Setup",
                "value": f"**Target:** ${stock_data['target']} ({stock_data['upside']}%)\n"
                        f"**Stop:** ${stock_data['stop']} ({stock_data['risk']}%)\n"
                        f"**Risk/Reward:** 1:{stock_data['risk_reward']}",
                "inline": False
            },
            {
                "name": "🏢 Company Info",
                "value": f"**Sector:** {stock_data['sector']}\n"
                        f"**Industry:** {stock_data['industry']}\n"
                        f"**Market Cap:** {stock_data['market_cap']}",
                "inline": True
            }
        ],
        "footer": {
            "text": f"Penny Stock Scanner • {datetime.now().strftime('%Y-%m-%d %H:%M EST')}"
        }
    }
    
    # In production, would send via Discord webhook
    # For now, just print
    print("\n" + "="*60)
    print(f"PENNY STOCK ALERT: {stock_data['ticker']}")
    print("="*60)
    print(json.dumps(stock_data, indent=2))
    print("="*60)
    
    return True

def main():
    """Main execution"""
    
    print(f"\n{'='*60}")
    print(f"PENNY STOCK SCANNER - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")
    
    # Get watchlist
    watchlist = get_penny_stock_watchlist()
    print(f"Scanning {len(watchlist)} stocks...")
    
    # Analyze each stock
    recommendations = []
    
    for ticker in watchlist:
        print(f"  Analyzing: {ticker}")
        result = analyze_stock(ticker)
        if result:
            recommendations.append(result)
            print(f"    ✅ Potential opportunity (Score: {result['score']})")
        else:
            print(f"    ❌ No opportunity")
    
    # Sort by score
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    # Send top 3 recommendations
    top_picks = recommendations[:3]
    
    print(f"\n{'='*60}")
    print(f"TOP {len(top_picks)} PENNY STOCK PICKS")
    print(f"{'='*60}")
    
    for i, stock in enumerate(top_picks, 1):
        print(f"\n#{i}: {stock['ticker']} - {stock['company']}")
        print(f"   Price: ${stock['price']} | Score: {stock['score']}/100")
        print(f"   Target: ${stock['target']} ({stock['upside']}%)")
        print(f"   Stop: ${stock['stop']} ({stock['risk']}%)")
        print(f"   R/R: 1:{stock['risk_reward']}")
        
        # Send Discord alert
        send_discord_alert(stock)
    
    # Save results
    if top_picks:
        output_file = f"/Users/cubiczan/.openclaw/workspace/penny-stock-recommendations-{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w') as f:
            json.dump(top_picks, f, indent=2)
        print(f"\n✅ Recommendations saved to: {output_file}")
    else:
        print("\n⚠️ No penny stock opportunities found today")
    
    print(f"\n{'='*60}")
    print("SCAN COMPLETE")
    print(f"{'='*60}")
    
    return len(top_picks) > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
