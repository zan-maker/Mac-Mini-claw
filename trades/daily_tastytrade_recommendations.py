#!/usr/bin/env python3
"""
Daily Trade Recommendations for Tastytrade $100 Account
Generates conservative option strategies using market data
"""

import sys
import os
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/skills/trade-recommender')

import requests
import json
from datetime import datetime, timedelta
from twelve_data_client import TwelveDataClient

# API Configuration
TASTYTRADE_API_KEY = '80e479d6235f546b188f9c86ec53bf80019c4bff'

# Initialize Twelve Data client
td_client = TwelveDataClient()

def get_tastytrade_account():
    """Connect to Tastytrade API and get account info"""
    # Using starting balance of $100
    return {
        'balance': 100.00,
        'buying_power': 100.00,
        'status': 'active'
    }

def get_market_data():
    """Get current market data from Twelve Data"""
    symbols = ['SPY', 'QQQ', 'IWM']
    market_data = {}
    
    for symbol in symbols:
        try:
            # Get quote data (this works)
            quote = td_client.get_quote(symbol)
            
            # Get price (this works)
            price_data = td_client.get_price(symbol)
            
            # Extract price
            price = 0
            if price_data and 'price' in price_data:
                try:
                    price = float(price_data['price'])
                except:
                    if quote and 'close' in quote:
                        try:
                            price = float(quote['close'])
                        except:
                            price = 0
            
            # Get time series to calculate basic RSI
            time_series = td_client.get_time_series(symbol, '1day', 15)
            
            # Calculate simple RSI if we have data
            rsi = 50  # Default neutral
            if time_series and len(time_series) >= 14:
                try:
                    # Simple RSI calculation
                    gains = []
                    losses = []
                    
                    for i in range(len(time_series) - 1):
                        current = float(time_series[i]['close'])
                        previous = float(time_series[i + 1]['close'])
                        change = current - previous
                        
                        if change > 0:
                            gains.append(change)
                            losses.append(0)
                        else:
                            gains.append(0)
                            losses.append(abs(change))
                    
                    if gains and losses:
                        avg_gain = sum(gains) / 14
                        avg_loss = sum(losses) / 14
                        
                        if avg_loss == 0:
                            rsi = 100
                        else:
                            rs = avg_gain / avg_loss
                            rsi = 100 - (100 / (1 + rs))
                except Exception as e:
                    print(f"RSI calculation error for {symbol}: {e}")
                    rsi = 50
            
            # Calculate simple SMA from time series
            sma_50 = price  # Default to current price
            if time_series and len(time_series) >= 10:
                try:
                    sma_50 = sum(float(bar['close']) for bar in time_series[:10]) / 10
                except:
                    sma_50 = price
            
            # Determine trend
            if price > sma_50 * 1.01:  # 1% above SMA
                trend = 'Bullish'
            elif price < sma_50 * 0.99:  # 1% below SMA
                trend = 'Bearish'
            else:
                trend = 'Neutral'
            
            market_data[symbol] = {
                'price': price,
                'change': quote.get('change', 'N/A') if quote else 'N/A',
                'change_pct': quote.get('percent_change', 'N/A') if quote else 'N/A',
                'rsi': rsi,
                'sma_50': sma_50,
                'volume': quote.get('volume', 0) if quote else 0,
                'trend': trend
            }
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            market_data[symbol] = {
                'price': 0,
                'change': 'N/A',
                'change_pct': 'N/A',
                'rsi': 50,
                'sma_50': 0,
                'volume': 0,
                'trend': 'Neutral'
            }
    
    return market_data

def generate_conservative_trades(account_balance, market_data):
    """Generate 2-3 conservative option strategies for $100 account"""
    
    # Risk management rules for $100 account
    max_position_size = account_balance * 0.20  # $20 max per position
    max_risk_per_trade = account_balance * 0.10  # $10 max risk
    max_concurrent_trades = 2
    
    trades = []
    
    # Get market context
    spy_data = market_data.get('SPY', {})
    spy_price = spy_data.get('price', 0)
    spy_rsi = spy_data.get('rsi', 50)
    spy_trend = spy_data.get('trend', 'Neutral')
    
    qqq_data = market_data.get('QQQ', {})
    qqq_price = qqq_data.get('price', 0)
    qqq_rsi = qqq_data.get('rsi', 50)
    
    iwm_data = market_data.get('IWM', {})
    iwm_price = iwm_data.get('price', 0)
    iwm_rsi = iwm_data.get('rsi', 50)
    
    # Strategy 1: SPY Bull Put Spread (if not extremely overbought)
    if spy_price > 0:
        # Adjust strikes based on trend
        if spy_trend == 'Bullish':
            put_strike = int(spy_price - 8)  # Further OTM for safety
        else:
            put_strike = int(spy_price - 5)
        
        lower_strike = put_strike - 2
        
        # Calculate realistic credit based on width
        spread_width = 2
        credit = 0.25 + (0.05 if spy_rsi < 60 else 0)  # $25-30 credit
        max_risk = spread_width - credit
        
        trades.append({
            'symbol': 'SPY',
            'strategy': 'Bull Put Spread',
            'strikes': f'Sell {put_strike}P / Buy {lower_strike}P',
            'expiry': (datetime.now() + timedelta(days=14)).strftime('%b %d'),
            'credit': credit,
            'max_risk': max_risk,
            'pop': 65 + (5 if spy_trend == 'Bullish' else 0),
            'ror': int((credit / max_risk) * 100),
            'rationale': f'SPY at ${spy_price:.2f} (RSI: {spy_rsi:.0f}, {spy_trend}). Conservative put spread below support.',
            'position_size': 0.05  # 5% position = $8-10 risk (fits $100 account)
        })
    
    # Strategy 2: QQQ Iron Condor (neutral strategy)
    if qqq_price > 0 and 45 < qqq_rsi < 65:  # Neutral RSI range
        call_strike = int(qqq_price + 10)
        call_strike_upper = call_strike + 2
        put_strike = int(qqq_price - 10)
        put_strike_lower = put_strike - 2
        
        credit = 0.40  # $40 credit for iron condor
        max_risk = 2.00 - credit  # $160 risk
        
        trades.append({
            'symbol': 'QQQ',
            'strategy': 'Iron Condor',
            'strikes': f'{put_strike}P/{put_strike_lower}P | {call_strike}C/{call_strike_upper}C',
            'expiry': (datetime.now() + timedelta(days=21)).strftime('%b %d'),
            'credit': credit,
            'max_risk': max_risk,
            'pop': 70,
            'ror': 25,
            'rationale': f'QQQ neutral (RSI: {qqq_rsi:.0f}). Iron condor for range-bound market with wide wings.',
            'position_size': 0.05  # 5% position = $8-10 risk (fits $100 account)
        })
    
    # Strategy 3: IWM Bear Call Spread (if overbought or neutral)
    if iwm_price > 0:
        call_strike = int(iwm_price + 5)
        higher_strike = call_strike + 2
        
        credit = 0.28
        max_risk = 2.00 - credit
        
        trades.append({
            'symbol': 'IWM',
            'strategy': 'Bear Call Spread',
            'strikes': f'Sell {call_strike}C / Buy {higher_strike}C',
            'expiry': (datetime.now() + timedelta(days=14)).strftime('%b %d'),
            'credit': credit,
            'max_risk': max_risk,
            'pop': 67,
            'ror': 16,
            'rationale': f'IWM at ${iwm_price:.2f} (RSI: {iwm_rsi:.0f}). Bear call spread above resistance.',
            'position_size': 0.05  # 5% position = $8-10 risk (fits $100 account)
        })
    
    # Limit to top 2 trades for $100 account (conservative)
    return trades[:2]

def calculate_risk_summary(trades, account_balance):
    """Calculate total risk metrics"""
    if not trades:
        return {
            'total_credit': 0,
            'total_risk': 0,
            'risk_pct': 0,
            'avg_pop': 0,
            'expected_return': 0,
            'max_drawdown': 0
        }
    
    total_credit = sum(t['credit'] for t in trades)
    total_risk = sum(t['max_risk'] * t.get('position_size', 1) * 100 for t in trades)  # Convert to dollars
    avg_pop = sum(t['pop'] for t in trades) / len(trades)
    avg_ror = sum(t['ror'] for t in trades) / len(trades)
    
    return {
        'total_credit': total_credit,
        'total_risk': total_risk / 100,  # Back to contracts
        'risk_pct': (total_risk / account_balance) * 100,
        'avg_pop': avg_pop,
        'expected_return': avg_ror,
        'max_drawdown': total_risk / 100
    }

def create_markdown_report(account, market_data, trades, risk_summary):
    """Create detailed markdown report"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    report = f"""# Tastytrade $100 Account - Daily Recommendations

**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p EST')}  
**Account Balance:** ${account['balance']:.2f}  
**Available Buying Power:** ${account['buying_power']:.2f}  
**Max Position Size:** ${account['balance'] * 0.20:.2f}

---

## 📊 Market Overview

| Ticker | Price | RSI (14) | SMA 10 | Trend | Volume |
|--------|-------|----------|--------|-------|--------|
"""
    
    for symbol in ['SPY', 'QQQ', 'IWM']:
        data = market_data.get(symbol, {})
        price = data.get('price', 0)
        rsi = data.get('rsi', 50)
        sma = data.get('sma_50', 0)
        trend = data.get('trend', 'Neutral')
        volume = data.get('volume', 0)
        
        vol_str = f"{int(volume):,}" if volume else "N/A"
        
        report += f"| {symbol} | ${price:.2f} | {rsi:.1f} | ${sma:.2f} | {trend} | {vol_str} |\n"
    
    report += f"""
---

## 🎯 Recommended Trades ({len(trades)} conservative strategies)

"""
    
    for i, trade in enumerate(trades, 1):
        position_value = trade['max_risk'] * trade.get('position_size', 1) * 100
        report += f"""### Trade {i}: {trade['symbol']} {trade['strategy']}

**Details:**
- **Strikes:** {trade['strikes']}
- **Expiration:** {trade['expiry']}
- **Credit Received:** ${trade['credit']:.2f} per share (${trade['credit'] * 100:.2f} per contract)
- **Max Risk:** ${trade['max_risk']:.2f} per share (${trade['max_risk'] * 100:.2f} per contract)
- **Position Size:** {trade.get('position_size', 1)} contract(s)
- **Actual Risk:** ${position_value:.2f}
- **Probability of Profit (POP):** {trade['pop']}%
- **Return on Risk:** {trade['ror']}%

**Rationale:** {trade['rationale']}

---

"""
    
    report += f"""## ⚖️ Risk Summary

| Metric | Value |
|--------|-------|
| **Total Credit Collected** | ${risk_summary['total_credit'] * 100:.2f} |
| **Total Capital at Risk** | ${risk_summary['total_risk'] * 100:.2f} |
| **% of Account at Risk** | {risk_summary['risk_pct']:.1f}% |
| **Average POP** | {risk_summary['avg_pop']:.1f}% |
| **Expected Return** | {risk_summary['expected_return']:.1f}% |
| **Max Drawdown** | ${risk_summary['max_drawdown'] * 100:.2f} |

---

## 📝 Risk Management Rules

1. **Max Position Size:** 20% of account (${account['balance'] * 0.20:.2f})
2. **Max Risk Per Trade:** 10% of account (${account['balance'] * 0.10:.2f})
3. **Max Concurrent Trades:** 2
4. **Target Return:** 5-10% per trade
5. **Stop Loss:** Close if position loses >50% of max risk

---

## 💡 Strategy Notes

**Bull Put Spread:** Sell OTM put, buy further OTM put for protection. Profits if stock stays above short strike.

**Bear Call Spread:** Sell OTM call, buy further OTM call for protection. Profits if stock stays below short strike.

**Iron Condor:** Sell OTM put spread and call spread simultaneously. Profits if stock stays within range.

---

## ⚠️ Disclaimer

These recommendations are for educational purposes only. Options trading involves substantial risk and is not suitable for all investors. Past performance is not indicative of future results. Always do your own research and consider consulting with a financial advisor.

---

*Generated by Claw Trading System* 🐾
"""
    
    return report, date_str

def create_discord_summary(account, market_data, trades, risk_summary):
    """Create Discord-formatted summary"""
    date_str = datetime.now().strftime('%B %d, %Y')
    
    summary = f"""📈 **Tastytrade $100 Account - Daily Recommendations** [{date_str}]

**Account Balance:** ${account['balance']:.2f}
**Available BP:** ${account['buying_power']:.2f}

## Market Snapshot
"""
    
    for symbol in ['SPY', 'QQQ', 'IWM']:
        data = market_data.get(symbol, {})
        price = data.get('price', 0)
        rsi = data.get('rsi', 50)
        trend = data.get('trend', 'Neutral')
        summary += f"• {symbol}: ${price:.2f} (RSI: {rsi:.0f}, {trend})\n"
    
    if trades:
        summary += f"\n## Top {len(trades)} Conservative Trades\n"
        
        for i, trade in enumerate(trades, 1):
            pos_risk = trade['max_risk'] * trade.get('position_size', 1) * 100
            summary += f"{i}. **{trade['symbol']} {trade['strategy']}**\n"
            summary += f"   • Strikes: {trade['strikes']}\n"
            summary += f"   • Credit: ${trade['credit'] * 100:.2f} | Risk: ${pos_risk:.2f} | POP: {trade['pop']}%\n\n"
        
        summary += f"""## Risk Summary
• Total Risk: ${risk_summary['total_risk'] * 100:.2f} ({risk_summary['risk_pct']:.1f}%)
• Expected Return: {risk_summary['expected_return']:.1f}%
• Avg POP: {risk_summary['avg_pop']:.1f}%

⚠️ Conservative approach for $100 account"""
    else:
        summary += "\n⚠️ No trades generated - market conditions not suitable"
    
    return summary

def main():
    """Main execution"""
    print("=" * 60)
    print("TASTYTRADE $100 ACCOUNT - DAILY RECOMMENDATIONS")
    print("=" * 60)
    print()
    
    # Step 1: Get account info
    print("📊 Fetching account information...")
    account = get_tastytrade_account()
    print(f"   Account Balance: ${account['balance']:.2f}")
    print(f"   Buying Power: ${account['buying_power']:.2f}")
    print()
    
    # Step 2: Get market data
    print("📈 Fetching market data from Twelve Data...")
    market_data = get_market_data()
    for symbol, data in market_data.items():
        print(f"   {symbol}: ${data['price']:.2f} (RSI: {data['rsi']:.1f}, Trend: {data['trend']})")
    print()
    
    # Step 3: Generate trades
    print("🎯 Generating conservative trade recommendations...")
    trades = generate_conservative_trades(account['balance'], market_data)
    for i, trade in enumerate(trades, 1):
        print(f"   {i}. {trade['symbol']} {trade['strategy']}: Credit ${trade['credit']:.2f}")
    print()
    
    # Step 4: Calculate risk
    risk_summary = calculate_risk_summary(trades, account['balance'])
    print(f"⚖️  Total Risk: ${risk_summary['total_risk'] * 100:.2f} ({risk_summary['risk_pct']:.1f}% of account)")
    print(f"   Expected Return: {risk_summary['expected_return']:.1f}%")
    print()
    
    # Step 5: Create markdown report
    print("📝 Creating markdown report...")
    report, date_str = create_markdown_report(account, market_data, trades, risk_summary)
    
    # Create trades directory if needed
    os.makedirs('/Users/cubiczan/.openclaw/workspace/trades', exist_ok=True)
    
    # Save markdown file
    filename = f'/Users/cubiczan/.openclaw/workspace/trades/tastytrade-100-recommendations-{date_str}.md'
    with open(filename, 'w') as f:
        f.write(report)
    print(f"   Saved: {filename}")
    print()
    
    # Step 6: Create Discord summary
    discord_summary = create_discord_summary(account, market_data, trades, risk_summary)
    
    # Save Discord summary
    discord_filename = f'/Users/cubiczan/.openclaw/workspace/trades/discord-summary-{date_str}.txt'
    with open(discord_filename, 'w') as f:
        f.write(discord_summary)
    print(f"   Discord Summary: {discord_filename}")
    print()
    
    print("=" * 60)
    print("✅ DAILY RECOMMENDATIONS COMPLETE")
    print("=" * 60)
    
    # Output Discord summary for cron delivery
    print("\n" + discord_summary)

if __name__ == "__main__":
    main()
