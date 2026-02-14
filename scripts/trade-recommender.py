#!/usr/bin/env python3
"""
Trade Recommender - Combines defeatbeta-api fundamental data with Alpha Vantage technical indicators
"""

import requests
import json
import time
from datetime import datetime

# Alpha Vantage API Key
ALPHA_VANTAGE_API_KEY = "T0Z2YW467F7PNA9Z"
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

def get_alpha_vantage_data(symbol, function, **params):
    """Fetch data from Alpha Vantage API"""
    params['function'] = function
    params['symbol'] = symbol
    params['apikey'] = ALPHA_VANTAGE_API_KEY
    
    response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
    return response.json()

def get_rsi(symbol, interval='daily', time_period=14):
    """Get RSI indicator"""
    return get_alpha_vantage_data(symbol, 'RSI', interval=interval, time_period=time_period)

def get_macd(symbol, interval='daily'):
    """Get MACD indicator"""
    return get_alpha_vantage_data(symbol, 'MACD', interval=interval)

def get_sma(symbol, interval='daily', time_period=50):
    """Get Simple Moving Average"""
    return get_alpha_vantage_data(symbol, 'SMA', interval=interval, time_period=time_period)

def get_daily_prices(symbol):
    """Get daily price data"""
    return get_alpha_vantage_data(symbol, 'TIME_SERIES_DAILY', outputsize='compact')

def get_quote(symbol):
    """Get real-time quote"""
    return get_alpha_vantage_data(symbol, 'GLOBAL_QUOTE')

def get_company_overview(symbol):
    """Get company fundamentals from Alpha Vantage"""
    return get_alpha_vantage_data(symbol, 'OVERVIEW')

def analyze_technicals(symbol):
    """Analyze technical indicators and return score"""
    score = 0
    signals = []
    
    # Get RSI
    try:
        rsi_data = get_rsi(symbol)
        time.sleep(1.2)  # Rate limit: 1 request per second
        if 'Technical Analysis: RSI' in rsi_data:
            latest_rsi = float(list(rsi_data['Technical Analysis: RSI'].values())[0]['RSI'])
            if latest_rsi < 30:
                score += 20
                signals.append(f"RSI: {latest_rsi:.1f} (Oversold - Bullish)")
            elif latest_rsi > 70:
                score += 0
                signals.append(f"RSI: {latest_rsi:.1f} (Overbought - Bearish)")
            else:
                score += 10
                signals.append(f"RSI: {latest_rsi:.1f} (Neutral)")
    except Exception as e:
        signals.append(f"RSI: Error - {e}")
    
    # Get MACD
    try:
        macd_data = get_macd(symbol)
        time.sleep(1.2)  # Rate limit
        if 'Technical Analysis: MACD' in macd_data:
            latest = list(macd_data['Technical Analysis: MACD'].values())[0]
            macd = float(latest['MACD'])
            signal = float(latest['MACD_Signal'])
            if macd > signal:
                score += 20
                signals.append(f"MACD: {macd:.4f} > Signal {signal:.4f} (Bullish)")
            else:
                score += 5
                signals.append(f"MACD: {macd:.4f} < Signal {signal:.4f} (Bearish)")
    except Exception as e:
        signals.append(f"MACD: Error - {e}")
    
    # Get SMA 50 and 200
    try:
        sma50_data = get_sma(symbol, time_period=50)
        sma200_data = get_sma(symbol, time_period=200)
        
        if 'Technical Analysis: SMA' in sma50_data and 'Technical Analysis: SMA' in sma200_data:
            sma50 = float(list(sma50_data['Technical Analysis: SMA'].values())[0]['SMA'])
            sma200 = float(list(sma200_data['Technical Analysis: SMA'].values())[0]['SMA'])
            
            if sma50 > sma200:
                score += 20
                signals.append(f"Golden Cross: SMA50 ({sma50:.2f}) > SMA200 ({sma200:.2f}) (Bullish)")
            else:
                score += 5
                signals.append(f"Death Cross: SMA50 ({sma50:.2f}) < SMA200 ({sma200:.2f}) (Bearish)")
    except Exception as e:
        signals.append(f"SMA: Error - {e}")
    
    # Get current price
    try:
        quote = get_quote(symbol)
        if 'Global Quote' in quote:
            price = float(quote['Global Quote']['05. price'])
            signals.append(f"Current Price: ${price:.2f}")
    except Exception as e:
        signals.append(f"Price: Error - {e}")
    
    return {
        'symbol': symbol,
        'score': score,
        'max_score': 60,
        'signals': signals,
        'timestamp': datetime.now().isoformat()
    }

def get_recommendation(technical_score, fundamental_score=None):
    """Generate trade recommendation based on scores"""
    if fundamental_score:
        combined = (fundamental_score * 0.6) + (technical_score * 0.4)
        max_combined = 100
        pct = (combined / max_combined) * 100
    else:
        pct = (technical_score / 60) * 100
    
    if pct >= 80:
        return "STRONG BUY", "🟢"
    elif pct >= 60:
        return "BUY", "🔵"
    elif pct >= 40:
        return "HOLD", "🟡"
    elif pct >= 20:
        return "SELL", "🟠"
    else:
        return "STRONG SELL", "🔴"

if __name__ == "__main__":
    import sys
    
    symbol = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    
    print(f"\n{'='*50}")
    print(f"Trade Analysis for {symbol}")
    print(f"{'='*50}\n")
    
    # Technical Analysis
    print("Technical Analysis (Alpha Vantage):")
    tech = analyze_technicals(symbol)
    for signal in tech['signals']:
        print(f"  • {signal}")
    
    # Recommendation
    rec, emoji = get_recommendation(tech['score'])
    print(f"\n{emoji} Technical Score: {tech['score']}/{tech['max_score']}")
    print(f"{emoji} Recommendation: {rec}")
    
    print(f"\n{'='*50}\n")
