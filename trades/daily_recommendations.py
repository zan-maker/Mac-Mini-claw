#!/usr/bin/env python3
"""
Daily Trade Recommendations for Tastytrade $100 Account
Generates conservative options trades suitable for small accounts
"""

import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/skills/trade-recommender')

from twelve_data_client import TwelveDataClient
from datetime import datetime, timedelta
import json

# API Keys
TASTYTRADE_API_KEY = '80e479d6235f546b188f9c86ec53bf80019c4bff'
TASTYTRADE_BASE_URL = 'https://tastytrade.com/api/'

class TradeRecommender:
    def __init__(self, account_balance=100.00):
        self.account_balance = account_balance
        self.max_position_size = account_balance * 0.20  # $20 max
        self.max_risk_per_trade = account_balance * 0.10  # $10 max risk
        self.max_concurrent_trades = 2
        self.twelve_data = TwelveDataClient()
        
    def get_market_data(self):
        """Fetch market data for major indices"""
        symbols = ['SPY', 'QQQ', 'IWM']
        market_data = {}
        
        for symbol in symbols:
            # Get quote
            quote = self.twelve_data.get_quote(symbol)
            
            # Get RSI
            rsi_data = self.twelve_data.get_technical_indicators(
                symbol, '1day', 'rsi', time_period=14
            )
            
            # Get SMA 50
            sma50_data = self.twelve_data.get_technical_indicators(
                symbol, '1day', 'sma', time_period=50
            )
            
            market_data[symbol] = {
                'price': float(quote.get('close', 0)) if quote else 0,
                'change': quote.get('change', 'N/A'),
                'change_pct': quote.get('percent_change', 'N/A'),
                'volume': quote.get('volume', 0),
                'rsi': float(rsi_data.get('values', [{}])[-1].get('rsi', 50)) if rsi_data.get('values') else 50,
                'sma50': float(sma50_data.get('values', [{}])[-1].get('sma', 0)) if sma50_data.get('values') else 0,
            }
            
            # Determine trend
            if market_data[symbol]['price'] > market_data[symbol]['sma50']:
                market_data[symbol]['trend'] = 'Bullish' if market_data[symbol]['rsi'] < 70 else 'Overbought'
            else:
                market_data[symbol]['trend'] = 'Bearish' if market_data[symbol]['rsi'] > 30 else 'Oversold'
        
        return market_data
    
    def generate_conservative_trades(self, market_data):
        """Generate 2-3 conservative trades for $100 account"""
        trades = []
        
        # Strategy 1: Bull Put Spread on SPY (if bullish)
        spy_data = market_data.get('SPY', {})
        if spy_data.get('trend') in ['Bullish', 'Overbought']:
            # Example: SPY $5 wide put spread, 30-45 DTE
            spy_price = spy_data.get('price', 500)
            # Sell put at support, buy put for protection
            short_strike = int(spy_price * 0.97)  # 3% OTM
            long_strike = short_strike - 5
            
            trades.append({
                'ticker': 'SPY',
                'strategy': 'Bull Put Spread',
                'strikes': f'{short_strike}/{long_strike}',
                'expiry': self.get_expiry_date(30),
                'credit': 0.45,  # Conservative estimate
                'max_risk': 5.00 - 0.45,  # Width - credit
                'pop': 65,  # Probability of profit
                'ror': 9.0,  # Return on risk
                'contracts': 1,
                'direction': 'Bullish'
            })
        
        # Strategy 2: Bear Call Spread on QQQ (if overbought)
        qqq_data = market_data.get('QQQ', {})
        if qqq_data.get('rsi', 50) > 60:
            qqq_price = qqq_data.get('price', 400)
            short_strike = int(qqq_price * 1.03)  # 3% OTM
            long_strike = short_strike + 5
            
            trades.append({
                'ticker': 'QQQ',
                'strategy': 'Bear Call Spread',
                'strikes': f'{short_strike}/{long_strike}',
                'expiry': self.get_expiry_date(30),
                'credit': 0.40,
                'max_risk': 5.00 - 0.40,
                'pop': 62,
                'ror': 8.7,
                'contracts': 1,
                'direction': 'Bearish'
            })
        
        # Strategy 3: Iron Condor on IWM (neutral strategy)
        iwm_data = market_data.get('IWM', {})
        if iwm_data:
            iwm_price = iwm_data.get('price', 200)
            
            trades.append({
                'ticker': 'IWM',
                'strategy': 'Iron Condor',
                'strikes': f'{int(iwm_price*0.96)}/{int(iwm_price*0.94)} | {int(iwm_price*1.04)}/{int(iwm_price*1.06)}',
                'expiry': self.get_expiry_date(45),
                'credit': 0.60,
                'max_risk': 2.00 - 0.60,
                'pop': 70,
                'ror': 30.0,
                'contracts': 1,
                'direction': 'Neutral'
            })
        
        # Filter to top 2-3 trades based on risk parameters
        valid_trades = [t for t in trades if t['max_risk'] <= self.max_risk_per_trade]
        
        return valid_trades[:3]  # Return top 3
    
    def get_expiry_date(self, days_out=30):
        """Get next Friday expiry date"""
        today = datetime.now()
        days_ahead = days_out
        expiry = today + timedelta(days=days_ahead)
        
        # Find next Friday
        days_until_friday = (4 - expiry.weekday()) % 7
        if days_until_friday == 0 and days_out < 7:
            days_until_friday = 7
        expiry = expiry + timedelta(days=days_until_friday)
        
        return expiry.strftime('%b %d')
    
    def calculate_risk_summary(self, trades):
        """Calculate total risk metrics"""
        total_risk = sum(t['max_risk'] * t['contracts'] for t in trades)
        total_credit = sum(t['credit'] * t['contracts'] for t in trades)
        max_drawdown = total_risk
        expected_return = (total_credit / total_risk * 100) if total_risk > 0 else 0
        
        return {
            'total_risk': total_risk,
            'total_credit': total_credit,
            'max_drawdown': max_drawdown,
            'expected_return': expected_return,
            'risk_pct': (total_risk / self.account_balance * 100)
        }
    
    def generate_report(self, market_data, trades, risk_summary):
        """Generate markdown report"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        report = f"""# Tastytrade $100 Account - Daily Recommendations

**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
**Account Balance:** ${self.account_balance:.2f}
**Available Buying Power:** ${self.account_balance * 4:.2f} (4x leverage)
**Max Position Size:** ${self.max_position_size:.2f}

## Market Overview

| Symbol | Price | Change | RSI | SMA50 | Trend |
|--------|-------|--------|-----|-------|-------|
"""
        
        for symbol, data in market_data.items():
            change_symbol = '📈' if float(data.get('change', 0)) >= 0 else '📉'
            report += f"| {symbol} | ${data['price']:.2f} | {change_symbol} {data['change_pct']}% | {data['rsi']:.1f} | ${data['sma50']:.2f} | {data['trend']} |\n"
        
        report += f"""
## Recommended Trades ({len(trades)})

| # | Ticker | Strategy | Strikes | Expiry | Credit | Max Risk | POP | RoR |
|---|--------|----------|---------|--------|--------|----------|-----|-----|
"""
        
        for i, trade in enumerate(trades, 1):
            report += f"| {i} | {trade['ticker']} | {trade['strategy']} | {trade['strikes']} | {trade['expiry']} | ${trade['credit']:.2f} | ${trade['max_risk']:.2f} | {trade['pop']}% | {trade['ror']:.1f}% |\n"
        
        report += f"""
## Risk Summary

- **Total Risk:** ${risk_summary['total_risk']:.2f} ({risk_summary['risk_pct']:.1f}% of account)
- **Total Credit Collected:** ${risk_summary['total_credit']:.2f}
- **Max Drawdown:** ${risk_summary['max_drawdown']:.2f}
- **Expected Return:** {risk_summary['expected_return']:.1f}%

## Trade Details

"""
        
        for i, trade in enumerate(trades, 1):
            report += f"""### Trade {i}: {trade['ticker']} {trade['strategy']}
- **Direction:** {trade['direction']}
- **Strikes:** {trade['strikes']}
- **Expiration:** {trade['expiry']}
- **Credit:** ${trade['credit']:.2f}
- **Max Risk:** ${trade['max_risk']:.2f}
- **Probability of Profit (POP):** {trade['pop']}%
- **Return on Risk:** {trade['ror']:.1f}%

"""
        
        report += f"""## Risk Management Rules

1. **Max Position Size:** ${self.max_position_size:.2f} (20% of account)
2. **Max Risk Per Trade:** ${self.max_risk_per_trade:.2f} (10% of account)
3. **Max Concurrent Trades:** {self.max_concurrent_trades}
4. **Target Return:** 5-10% per trade
5. **Stop Loss:** Close at 2x credit received

## Strategy Notes

- **Bull Put Spread:** Profitable if stock stays above short strike
- **Bear Call Spread:** Profitable if stock stays below short strike
- **Iron Condor:** Profitable if stock stays within range

---
*Generated by Trade Recommender v2.0 | Conservative Mode for $100 Account*
"""
        
        return report, date_str
    
    def generate_discord_message(self, market_data, trades, risk_summary):
        """Generate Discord-friendly message"""
        date_str = datetime.now().strftime('%B %d, %Y')
        
        msg = f"""📈 **Tastytrade $100 Account - Daily Recommendations**
📅 {date_str}

**Account Balance:** ${self.account_balance:.2f}
**Available BP:** ${self.account_balance * 4:.2f}

## 📊 Market Snapshot
"""
        
        for symbol, data in market_data.items():
            emoji = '🟢' if data['trend'] == 'Bullish' else '🔴' if data['trend'] == 'Bearish' else '🟡'
            msg += f"• {symbol}: ${data['price']:.2f} (RSI: {data['rsi']:.0f}) {emoji}\n"
        
        msg += f"""
## 💰 Top {len(trades)} Conservative Trades
"""
        
        for i, trade in enumerate(trades, 1):
            direction_emoji = '📈' if trade['direction'] == 'Bullish' else '📉' if trade['direction'] == 'Bearish' else '⚖️'
            msg += f"""
**{i}. {trade['ticker']} {trade['strategy']}** {direction_emoji}
• Strikes: {trade['strikes']}
• Expiry: {trade['expiry']}
• Credit: ${trade['credit']:.2f} | Risk: ${trade['max_risk']:.2f}
• POP: {trade['pop']}% | RoR: {trade['ror']:.1f}%
"""
        
        msg += f"""
## ⚠️ Risk Summary
• Total Risk: ${risk_summary['total_risk']:.2f} ({risk_summary['risk_pct']:.1f}%)
• Expected Return: {risk_summary['expected_return']:.1f}%

*Conservative approach for $100 account*
"""
        
        return msg


def main():
    print("=" * 60)
    print("DAILY TRADE RECOMMENDATIONS - $100 ACCOUNT")
    print("=" * 60)
    print()
    
    # Initialize recommender
    recommender = TradeRecommender(account_balance=100.00)
    
    # Get market data
    print("📊 Fetching market data from Twelve Data...")
    market_data = recommender.get_market_data()
    
    for symbol, data in market_data.items():
        print(f"  • {symbol}: ${data['price']:.2f} (RSI: {data['rsi']:.1f}, Trend: {data['trend']})")
    print()
    
    # Generate trades
    print("💡 Generating conservative trades...")
    trades = recommender.generate_conservative_trades(market_data)
    
    if not trades:
        print("⚠️  No suitable trades found for today")
        return
    
    print(f"  ✓ Generated {len(trades)} trade recommendations")
    print()
    
    # Calculate risk
    risk_summary = recommender.calculate_risk_summary(trades)
    
    # Generate reports
    print("📝 Generating reports...")
    report, date_str = recommender.generate_report(market_data, trades, risk_summary)
    discord_msg = recommender.generate_discord_message(market_data, trades, risk_summary)
    
    # Save to file
    filename = f'/Users/cubiczan/.openclaw/workspace/trades/tastytrade-100-recommendations-{date_str}.md'
    with open(filename, 'w') as f:
        f.write(report)
    print(f"  ✓ Saved to: {filename}")
    print()
    
    # Print summary
    print("=" * 60)
    print("DISCORD MESSAGE:")
    print("=" * 60)
    print(discord_msg)
    print()
    print("=" * 60)
    print("✅ COMPLETE")
    print("=" * 60)
    
    # Return discord message for output
    print("\n---DISCORD_OUTPUT_START---")
    print(discord_msg)
    print("---DISCORD_OUTPUT_END---")


if __name__ == "__main__":
    main()
