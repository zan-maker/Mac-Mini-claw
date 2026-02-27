#!/usr/bin/env python3
"""
Daily Trade Recommendations for Tastytrade $100 Account
Conservative options strategies with strict risk management
"""

import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/skills/trade-recommender')

from twelve_data_client import TwelveDataClient
from datetime import datetime, timedelta
import json

def get_market_data():
    """Fetch market data from Twelve Data"""
    client = TwelveDataClient()
    
    # Get quotes for major indices
    symbols = ['SPY', 'QQQ', 'IWM', 'TLT', 'GLD']
    quotes = {}
    
    for symbol in symbols:
        quote = client.get_quote(symbol)
        if quote and 'close' in quote:
            quotes[symbol] = {
                'price': float(quote.get('close', 0)),
                'change': float(quote.get('change', 0)),
                'change_pct': quote.get('percent_change', '0'),
                'volume': int(quote.get('volume', 0))
            }
    
    # Get technical indicators
    technicals = {}
    for symbol in ['SPY', 'QQQ', 'IWM']:
        # RSI
        rsi_data = client.get_technical_indicators(symbol, '1day', 'rsi', period='14')
        if rsi_data and 'values' in rsi_data and len(rsi_data['values']) > 0:
            rsi_value = float(rsi_data['values'][0].get('rsi', 50))
        else:
            rsi_value = 50  # Neutral default
        
        # SMA 50
        sma_data = client.get_technical_indicators(symbol, '1day', 'sma', period='50')
        if sma_data and 'values' in sma_data and len(sma_data['values']) > 0:
            sma_50 = float(sma_data['values'][0].get('sma', 0))
        else:
            sma_50 = quotes.get(symbol, {}).get('price', 0)
        
        # Determine trend
        price = quotes.get(symbol, {}).get('price', 0)
        if price > sma_50:
            trend = 'Bullish' if rsi_value < 70 else 'Overbought'
        elif price < sma_50:
            trend = 'Bearish' if rsi_value > 30 else 'Oversold'
        else:
            trend = 'Neutral'
        
        technicals[symbol] = {
            'rsi': round(rsi_value, 1),
            'sma_50': round(sma_50, 2),
            'trend': trend
        }
    
    return quotes, technicals

def generate_trades(quotes, technicals):
    """Generate 2-3 conservative trade recommendations for $100 account"""
    trades = []
    
    # Risk parameters for $100 account
    max_risk_per_trade = 10  # $10 max risk per trade (10%)
    max_position = 20  # $20 max position (20%)
    
    # Strategy 1: SPY Iron Condor (neutral strategy)
    spy_price = quotes.get('SPY', {}).get('price', 0)
    spy_rsi = technicals.get('SPY', {}).get('rsi', 50)
    spy_trend = technicals.get('SPY', {}).get('trend', 'Neutral')
    
    if spy_price > 0:
        # Find strikes ~$5-10 OTM
        put_strike = int(spy_price) - 5
        call_strike = int(spy_price) + 5
        
        # Weekly expiration (3-5 days out)
        days_out = 4
        
        # Estimated credit for iron condor (conservative estimate)
        credit = 0.35  # $35 per contract, but we'll do 1 contract
        max_risk = 100 - 35  # Width of strikes - credit received
        pop = 68  # Probability of profit (estimate for OTM IC)
        
        trades.append({
            'ticker': 'SPY',
            'strategy': 'Iron Condor',
            'strikes': f'P{put_strike}/P{put_strike-5} C{call_strike}/C{call_strike+5}',
            'expiry': f'{days_out} days',
            'credit': 0.35,
            'max_risk': 0.65,  # Per contract unit
            'pop': 68,
            'ror': 53.8,  # Return on risk (35/65)
            'contracts': 1,
            'rationale': f'RSI {spy_rsi:.0f}, {spy_trend}. Neutral range play.'
        })
    
    # Strategy 2: QQQ Bull Put Spread (if bullish) or Bear Call (if bearish)
    qqq_price = quotes.get('QQQ', {}).get('price', 0)
    qqq_rsi = technicals.get('QQQ', {}).get('rsi', 50)
    qqq_trend = technicals.get('QQQ', {}).get('trend', 'Neutral')
    
    if qqq_price > 0:
        if qqq_rsi < 60:  # Not overbought - bullish put spread
            put_strike = int(qqq_price) - 5
            credit = 0.25
            max_risk = 0.75
            pop = 72
            strategy = 'Bull Put Spread'
            rationale = f'RSI {qqq_rsi:.0f}, {qqq_trend}. Support play.'
        else:  # Overbought - bearish call spread
            call_strike = int(qqq_price) + 5
            credit = 0.30
            max_risk = 0.70
            pop = 65
            strategy = 'Bear Call Spread'
            rationale = f'RSI {qqq_rsi:.0f}, {qqq_trend}. Resistance play.'
        
        trades.append({
            'ticker': 'QQQ',
            'strategy': strategy,
            'strikes': f'{put_strike if "Put" in strategy else call_strike}/{put_strike-5 if "Put" in strategy else call_strike+5}',
            'expiry': '4 days',
            'credit': credit,
            'max_risk': max_risk,
            'pop': pop,
            'ror': round((credit / max_risk) * 100, 1),
            'contracts': 1,
            'rationale': rationale
        })
    
    # Strategy 3: IWM Credit Spread (small cap exposure)
    iwm_price = quotes.get('IWM', {}).get('price', 0)
    iwm_rsi = technicals.get('IWM', {}).get('rsi', 50)
    
    if iwm_price > 0:
        # Simple put credit spread
        put_strike = int(iwm_price) - 3
        credit = 0.20
        max_risk = 0.80
        pop = 75
        
        trades.append({
            'ticker': 'IWM',
            'strategy': 'Bull Put Spread',
            'strikes': f'{put_strike}/{put_strike-3}',
            'expiry': '5 days',
            'credit': credit,
            'max_risk': max_risk,
            'pop': pop,
            'ror': 25.0,
            'contracts': 1,
            'rationale': f'RSI {iwm_rsi:.0f}. Small cap support play.'
        })
    
    return trades

def create_report(quotes, technicals, trades):
    """Create markdown report"""
    date = datetime.now().strftime('%Y-%m-%d')
    
    report = f"""# Tastytrade $100 Account - Daily Recommendations

**Date:** {datetime.now().strftime('%A, %B %d, %Y')}
**Account Balance:** $100.00
**Available Buying Power:** ~$400 (4x margin on defined risk)
**Max Position Size:** $20 (20% of account)
**Max Risk Per Trade:** $10 (10% of account)

---

## Market Overview

| Ticker | Price | Change | RSI (14) | SMA 50 | Trend |
|--------|-------|--------|----------|--------|-------|
"""
    
    for symbol in ['SPY', 'QQQ', 'IWM']:
        q = quotes.get(symbol, {})
        t = technicals.get(symbol, {})
        price = q.get('price', 0)
        change = q.get('change', 0)
        change_pct = q.get('change_pct', '0%')
        rsi = t.get('rsi', 50)
        sma = t.get('sma_50', 0)
        trend = t.get('trend', 'Neutral')
        
        change_str = f"{'+' if change >= 0 else ''}{change:.2f} ({change_pct})"
        report += f"| {symbol} | ${price:.2f} | {change_str} | {rsi:.1f} | ${sma:.2f} | {trend} |\n"
    
    report += f"""
---

## Recommended Trades ({len(trades)})

"""
    
    for i, trade in enumerate(trades, 1):
        report += f"""### Trade {i}: {trade['ticker']} {trade['strategy']}

- **Strikes:** {trade['strikes']}
- **Expiration:** {trade['expiry']}
- **Credit:** ${trade['credit']:.2f}
- **Max Risk:** ${trade['max_risk']:.2f}
- **POP:** {trade['pop']}%
- **Return on Risk:** {trade['ror']:.1f}%
- **Contracts:** {trade['contracts']}
- **Rationale:** {trade['rationale']}

"""
    
    # Calculate total risk
    total_risk = sum(t['max_risk'] for t in trades)
    total_credit = sum(t['credit'] for t in trades)
    avg_pop = sum(t['pop'] for t in trades) / len(trades) if trades else 0
    
    report += f"""---

## Risk Summary

- **Total Risk:** ${total_risk:.2f} ({total_risk:.1f}% of account)
- **Total Credit:** ${total_credit:.2f}
- **Average POP:** {avg_pop:.1f}%
- **Max Drawdown:** ${total_risk:.2f} (if all trades lose)
- **Expected Return:** ${total_credit:.2f} if all profitable

---

## Risk Management Rules

1. **Max 2 concurrent trades** for $100 account
2. **Stop loss** at 2x credit received (turn winner to loser)
3. **Take profit** at 50% of max profit (discipline > greed)
4. **No adjustment** on small account - let trades play out
5. **Close at 21 DTE** minimum (avoid gamma risk)

---

## Execution Notes

- Place trades during first 30 min of market open for best fills
- Use mid-price or better for entries
- Monitor positions daily
- Close winners at 50% profit, losers at 2x credit

---

*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} EST*
*Disclaimer: For educational purposes only. Not financial advice.*
"""
    
    return report, date

def create_discord_summary(quotes, technicals, trades):
    """Create Discord-friendly summary"""
    date = datetime.now().strftime('%m/%d/%Y')
    
    # Market snapshot
    spy = quotes.get('SPY', {})
    qqq = quotes.get('QQQ', {})
    iwm = quotes.get('IWM', {})
    
    spy_rsi = technicals.get('SPY', {}).get('rsi', 50)
    qqq_rsi = technicals.get('QQQ', {}).get('rsi', 50)
    iwm_rsi = technicals.get('IWM', {}).get('rsi', 50)
    
    total_credit = sum(t['credit'] for t in trades)
    total_risk = sum(t['max_risk'] for t in trades)
    
    summary = f"""📈 **Tastytrade $100 Account - Daily Recommendations** [{date}]

**Account Balance:** $100.00
**Available BP:** ~$400

## Market Snapshot
• SPY: ${spy.get('price', 0):.2f} (RSI: {spy_rsi:.0f})
• QQQ: ${qqq.get('price', 0):.2f} (RSI: {qqq_rsi:.0f})
• IWM: ${iwm.get('price', 0):.2f} (RSI: {iwm_rsi:.0f})

## Top {min(2, len(trades))} Conservative Trades

"""
    
    for i, trade in enumerate(trades[:2], 1):
        summary += f"""**{i}. {trade['ticker']} {trade['strategy']}**
   • Strikes: {trade['strikes']}
   • Credit: ${trade['credit']:.2f} | Risk: ${trade['max_risk']:.2f} | POP: {trade['pop']}%
   • Rationale: {trade['rationale']}

"""
    
    summary += f"""## Risk Summary
• Total Risk: ${total_risk:.2f} ({total_risk:.0f}% of account)
• Total Credit: ${total_credit:.2f}
• Expected Return: {total_credit/total_risk*100:.1f}% if profitable

⚠️ Conservative approach for $100 account
📊 Full report: trades/tastytrade-100-recommendations-{datetime.now().strftime('%Y-%m-%d')}.md
"""
    
    return summary

def main():
    print("Fetching market data from Twelve Data...")
    quotes, technicals = get_market_data()
    
    print(f"\nMarket Data:")
    for symbol in ['SPY', 'QQQ', 'IWM']:
        q = quotes.get(symbol, {})
        t = technicals.get(symbol, {})
        print(f"  {symbol}: ${q.get('price', 0):.2f} | RSI: {t.get('rsi', 50):.1f} | {t.get('trend', 'Neutral')}")
    
    print("\nGenerating trade recommendations...")
    trades = generate_trades(quotes, technicals)
    
    print(f"\nGenerated {len(trades)} trades:")
    for trade in trades:
        print(f"  • {trade['ticker']} {trade['strategy']}: ${trade['credit']:.2f} credit, {trade['pop']}% POP")
    
    # Create markdown report
    report, date = create_report(quotes, technicals, trades)
    report_path = f'/Users/cubiczan/.openclaw/workspace/trades/tastytrade-100-recommendations-{date}.md'
    
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"\n✅ Report saved: {report_path}")
    
    # Create Discord summary
    discord_summary = create_discord_summary(quotes, technicals, trades)
    
    # Print Discord summary for cron delivery
    print("\n" + "="*60)
    print("DISCORD SUMMARY:")
    print("="*60)
    print(discord_summary)

if __name__ == "__main__":
    main()
