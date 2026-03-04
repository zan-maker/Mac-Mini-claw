#!/usr/bin/env python3
"""
Daily Trade Recommendations for Tastytrade $100 Account
Generates conservative options strategies suitable for small accounts
"""

import sys
import os
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/skills/trade-recommender')

from twelve_data_client import TwelveDataClient
from datetime import datetime, timedelta
import json

class TastytradeRecommender:
    def __init__(self, account_balance=100.00):
        self.account_balance = account_balance
        self.max_position_size = account_balance * 0.20  # $20 max
        self.max_risk_per_trade = account_balance * 0.10  # $10 max
        self.max_concurrent_trades = 2
        self.twelve_data = TwelveDataClient()
        
    def get_market_data(self, symbols=['SPY', 'QQQ', 'IWM']):
        """Fetch current market data for major indices"""
        market_data = {}
        
        for symbol in symbols:
            try:
                quote = self.twelve_data.get_quote(symbol)
                rsi_data = self.twelve_data.get_technical_indicators(
                    symbol, '1day', 'rsi', period=14
                )
                
                if quote and 'close' in quote:
                    price = float(quote.get('close', 0))
                    change_pct = float(quote.get('percent_change', 0).replace('%', '') if quote.get('percent_change') else 0)
                    
                    # Extract RSI value
                    rsi_value = None
                    if rsi_data and 'values' in rsi_data and len(rsi_data['values']) > 0:
                        try:
                            rsi_value = float(rsi_data['values'][0].get('rsi', 50))
                        except:
                            rsi_value = 50
                    
                    # Determine trend
                    if rsi_value:
                        if rsi_value < 30:
                            trend = "Oversold"
                        elif rsi_value > 70:
                            trend = "Overbought"
                        elif change_pct > 0.5:
                            trend = "Bullish"
                        elif change_pct < -0.5:
                            trend = "Bearish"
                        else:
                            trend = "Neutral"
                    else:
                        trend = "Neutral"
                    
                    market_data[symbol] = {
                        'price': price,
                        'change_pct': change_pct,
                        'rsi': rsi_value if rsi_value else 50,
                        'trend': trend,
                        'volume': quote.get('volume', 0)
                    }
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                continue
        
        return market_data
    
    def generate_conservative_trades(self, market_data):
        """Generate conservative options trades suitable for $100 account"""
        recommendations = []
        
        for symbol, data in market_data.items():
            price = data['price']
            rsi = data['rsi']
            trend = data['trend']
            
            # Skip if price too high for our account
            if price > 500:
                continue
            
            # Generate strategies based on market conditions
            if trend == "Oversold" or (rsi < 40 and trend != "Bearish"):
                # Bullish strategies
                rec = self._create_bull_put_spread(symbol, price)
                if rec:
                    recommendations.append(rec)
                    
            elif trend == "Overbought" or (rsi > 60 and trend != "Bullish"):
                # Bearish strategies
                rec = self._create_bear_call_spread(symbol, price)
                if rec:
                    recommendations.append(rec)
                    
            else:
                # Neutral strategies - Iron Condor
                rec = self._create_iron_condor(symbol, price)
                if rec:
                    recommendations.append(rec)
        
        # Sort by POP (probability of profit) and limit to top trades
        recommendations.sort(key=lambda x: x['pop'], reverse=True)
        return recommendations[:3]  # Top 3 trades
    
    def _create_bull_put_spread(self, symbol, current_price):
        """Create a bull put spread (bullish)"""
        # Sell put at lower strike, buy put at even lower strike
        # Works best in bullish/neutral markets
        
        # Calculate strikes (5-10% OTM)
        short_strike = round(current_price * 0.92, 0)  # 8% OTM
        long_strike = round(short_strike - 5, 0)  # $5 wide
        
        # Estimate credit (conservative)
        credit = 0.30  # $30 credit for $5 wide spread
        max_risk = 5.00 - credit  # $4.70 max risk
        
        # Check if fits our risk parameters
        if max_risk > self.max_risk_per_trade:
            return None
        
        # POP estimation (simplified)
        pop = 70  # Conservative estimate for OTM spread
        
        return {
            'symbol': symbol,
            'strategy': 'Bull Put Spread',
            'strikes': f'{int(short_strike)}/{int(long_strike)}P',
            'expiry': self._get_expiry(),
            'credit': credit,
            'max_risk': max_risk,
            'pop': pop,
            'ror': (credit / max_risk) * 100,
            'direction': 'Bullish/Neutral'
        }
    
    def _create_bear_call_spread(self, symbol, current_price):
        """Create a bear call spread (bearish)"""
        # Sell call at higher strike, buy call at even higher strike
        
        # Calculate strikes (5-10% OTM)
        short_strike = round(current_price * 1.08, 0)  # 8% OTM
        long_strike = round(short_strike + 5, 0)  # $5 wide
        
        # Estimate credit (conservative)
        credit = 0.25  # $25 credit for $5 wide spread
        max_risk = 5.00 - credit  # $4.75 max risk
        
        if max_risk > self.max_risk_per_trade:
            return None
        
        pop = 68  # Conservative estimate
        
        return {
            'symbol': symbol,
            'strategy': 'Bear Call Spread',
            'strikes': f'{int(short_strike)}/{int(long_strike)}C',
            'expiry': self._get_expiry(),
            'credit': credit,
            'max_risk': max_risk,
            'pop': pop,
            'ror': (credit / max_risk) * 100,
            'direction': 'Bearish/Neutral'
        }
    
    def _create_iron_condor(self, symbol, current_price):
        """Create an iron condor (neutral)"""
        # Combine bull put spread + bear call spread
        
        # Strikes
        put_short = round(current_price * 0.94, 0)
        put_long = round(put_short - 3, 0)
        call_short = round(current_price * 1.06, 0)
        call_long = round(call_short + 3, 0)
        
        # Estimate credit
        credit = 0.40  # $40 total credit
        max_risk = 3.00 - credit  # $2.60 max risk per side
        
        if max_risk > self.max_risk_per_trade:
            return None
        
        pop = 75  # Higher POP for iron condors
        
        return {
            'symbol': symbol,
            'strategy': 'Iron Condor',
            'strikes': f'{int(put_long)}/{int(put_short)}P {int(call_short)}/{int(call_long)}C',
            'expiry': self._get_expiry(),
            'credit': credit,
            'max_risk': max_risk,
            'pop': pop,
            'ror': (credit / max_risk) * 100,
            'direction': 'Neutral'
        }
    
    def _get_expiry(self):
        """Get next Friday expiry date"""
        today = datetime.now()
        days_until_friday = (4 - today.weekday() + 7) % 7
        if days_until_friday == 0:
            days_until_friday = 7  # If today is Friday, get next Friday
        
        # For $100 account, target 7-14 DTE (days to expiration)
        if days_until_friday < 3:
            days_until_friday += 7
        
        expiry = today + timedelta(days=days_until_friday)
        return expiry.strftime('%b %d')
    
    def generate_report(self, market_data, recommendations):
        """Generate markdown report"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        report = f"""# Tastytrade $100 Account - Daily Recommendations

**Date:** {datetime.now().strftime('%A, %B %d, %Y')}
**Account Balance:** ${self.account_balance:.2f}
**Max Position Size:** ${self.max_position_size:.2f}
**Max Risk Per Trade:** ${self.max_risk_per_trade:.2f}

---

## Market Overview

| Symbol | Price | Change | RSI | Trend |
|--------|-------|--------|-----|-------|
"""
        
        for symbol, data in market_data.items():
            change_sign = '+' if data['change_pct'] >= 0 else ''
            report += f"| {symbol} | ${data['price']:.2f} | {change_sign}{data['change_pct']:.2f}% | {data['rsi']:.1f} | {data['trend']} |\n"
        
        report += f"""
---

## Recommended Trades ({len(recommendations)})

"""
        
        for i, rec in enumerate(recommendations, 1):
            report += f"""### Trade {i}: {rec['symbol']} {rec['strategy']}

- **Direction:** {rec['direction']}
- **Strikes:** {rec['strikes']}
- **Expiry:** {rec['expiry']}
- **Credit:** ${rec['credit']:.2f}
- **Max Risk:** ${rec['max_risk']:.2f}
- **Probability of Profit (POP):** {rec['pop']}%
- **Return on Risk:** {rec['ror']:.1f}%

"""
        
        # Risk summary
        total_risk = sum(rec['max_risk'] for rec in recommendations[:2])  # Max 2 concurrent
        total_credit = sum(rec['credit'] for rec in recommendations[:2])
        avg_ror = sum(rec['ror'] for rec in recommendations[:2]) / len(recommendations[:2]) if recommendations else 0
        
        report += f"""---

## Risk Summary

- **Total Risk (2 trades):** ${total_risk:.2f} ({(total_risk/self.account_balance)*100:.1f}% of account)
- **Total Credit Collected:** ${total_credit:.2f}
- **Average Return on Risk:** {avg_ror:.1f}%
- **Max Concurrent Trades:** 2 (conservative approach)

---

## Strategy Notes

**For $100 accounts, focus on:**
- ✅ Credit spreads (defined risk)
- ✅ Wide strikes for higher POP
- ✅ 7-14 DTE (days to expiration)
- ✅ Small position sizing ($10-20 per trade)
- ❌ Avoid naked options
- ❌ Avoid undefined risk strategies
- ❌ Avoid expensive underlyings (> $500)

**Risk Management Rules:**
1. Never risk more than 10% per trade
2. Limit to 2 concurrent positions
3. Target 60%+ POP (probability of profit)
4. Cut losses at 2x credit received

---

*Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return report, date_str
    
    def generate_discord_summary(self, market_data, recommendations):
        """Generate Discord-friendly summary"""
        date_str = datetime.now().strftime('%b %d, %Y')
        
        summary = f"📈 **Tastytrade $100 Account - Daily Recommendations** [{date_str}]\n\n"
        summary += f"**Account Balance:** ${self.account_balance:.2f}\n"
        summary += f"**Max Position:** ${self.max_position_size:.2f}\n\n"
        
        summary += "**Market Snapshot**\n"
        for symbol, data in market_data.items():
            change_sign = '+' if data['change_pct'] >= 0 else ''
            summary += f"• {symbol}: ${data['price']:.2f} ({change_sign}{data['change_pct']:.2f}%) RSI: {data['rsi']:.1f}\n"
        
        summary += f"\n**Top {min(2, len(recommendations))} Conservative Trades**\n"
        for i, rec in enumerate(recommendations[:2], 1):
            summary += f"{i}. {rec['symbol']} {rec['strategy']} - Credit: ${rec['credit']:.2f}, Risk: ${rec['max_risk']:.2f}, POP: {rec['pop']}%\n"
        
        if recommendations:
            total_risk = sum(rec['max_risk'] for rec in recommendations[:2])
            total_credit = sum(rec['credit'] for rec in recommendations[:2])
            avg_pop = sum(rec['pop'] for rec in recommendations[:2]) / len(recommendations[:2])
            
            summary += f"\n**Risk Summary**\n"
            summary += f"• Total Risk: ${total_risk:.2f} ({(total_risk/self.account_balance)*100:.0f}%)\n"
            summary += f"• Expected Return: {(total_credit/self.account_balance)*100:.1f}%\n"
            summary += f"• Avg POP: {avg_pop:.0f}%\n"
        
        summary += "\n⚠️ Conservative approach for $100 account"
        
        return summary


def main():
    """Main execution"""
    print("=" * 60)
    print("TASTYTRADE $100 ACCOUNT - DAILY RECOMMENDATIONS")
    print("=" * 60)
    print()
    
    # Initialize recommender
    recommender = TastytradeRecommender(account_balance=100.00)
    
    # Get market data
    print("📊 Fetching market data...")
    market_data = recommender.get_market_data(['SPY', 'QQQ', 'IWM'])
    
    if not market_data:
        print("❌ Error: Unable to fetch market data")
        return None
    
    print(f"✅ Retrieved data for {len(market_data)} symbols")
    print()
    
    # Display market data
    print("MARKET SNAPSHOT:")
    print("-" * 60)
    for symbol, data in market_data.items():
        change_sign = '+' if data['change_pct'] >= 0 else ''
        print(f"{symbol}: ${data['price']:.2f} ({change_sign}{data['change_pct']:.2f}%) | RSI: {data['rsi']:.1f} | {data['trend']}")
    print()
    
    # Generate recommendations
    print("🎯 Generating conservative trade recommendations...")
    recommendations = recommender.generate_conservative_trades(market_data)
    
    if not recommendations:
        print("⚠️ No suitable trades found for current market conditions")
        return None
    
    print(f"✅ Generated {len(recommendations)} recommendations")
    print()
    
    # Display recommendations
    print("TOP RECOMMENDATIONS:")
    print("-" * 60)
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"\n{i}. {rec['symbol']} {rec['strategy']}")
        print(f"   Strikes: {rec['strikes']}")
        print(f"   Expiry: {rec['expiry']}")
        print(f"   Credit: ${rec['credit']:.2f} | Risk: ${rec['max_risk']:.2f}")
        print(f"   POP: {rec['pop']}% | RoR: {rec['ror']:.1f}%")
    
    print()
    print("=" * 60)
    
    # Generate reports
    markdown_report, date_str = recommender.generate_report(market_data, recommendations)
    discord_summary = recommender.generate_discord_summary(market_data, recommendations)
    
    # Save markdown report
    output_file = f'/Users/cubiczan/.openclaw/workspace/trades/tastytrade-100-recommendations-{date_str}.md'
    with open(output_file, 'w') as f:
        f.write(markdown_report)
    print(f"✅ Report saved to: {output_file}")
    
    # Return data for Discord posting
    return {
        'market_data': market_data,
        'recommendations': recommendations,
        'discord_summary': discord_summary,
        'report_file': output_file
    }


if __name__ == "__main__":
    result = main()
    if result:
        print("\n" + "=" * 60)
        print("DISCORD SUMMARY:")
        print("=" * 60)
        print(result['discord_summary'])
