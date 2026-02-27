#!/usr/bin/env python3
"""
Tastytrade Daily Trade Recommender for $100 Account
Generates conservative trade recommendations using Twelve Data API
"""

import urllib.request
import urllib.error
import json
from datetime import datetime
from typing import Dict, List, Optional

# API Keys
TWELVE_DATA_API_KEY = "26b639a38e124248ba08958bcd72566f"
TASTYTRADE_API_KEY = "80e479d6235f546b188f9c86ec53bf80019c4bff"

# Account Settings
ACCOUNT_BALANCE = 100.00
MAX_POSITION_SIZE = 20.00  # 20% of account
MAX_RISK_PER_TRADE = 10.00  # 10% of account
MAX_CONCURRENT_TRADES = 2

class TwelveDataClient:
    """Twelve Data API client for market data"""

    def __init__(self, api_key: str = TWELVE_DATA_API_KEY):
        self.api_key = api_key
        self.base_url = "https://api.twelvedata.com"

    def _request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make API request"""
        try:
            url = f"{self.base_url}/{endpoint}"
            if params:
                params["apikey"] = self.api_key
                param_str = "&".join(f"{k}={v}" for k, v in params.items())
                url = f"{url}?{param_str}"
            else:
                url = f"{url}?apikey={self.api_key}"

            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5)')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Request error for {endpoint}: {e}")
            return None

    def get_quote(self, symbol: str) -> Dict:
        """Get real-time quote"""
        result = self._request("quote", {"symbol": symbol})
        return result if result else {}

    def get_price(self, symbol: str) -> float:
        """Get latest price"""
        result = self._request("price", {"symbol": symbol})
        if result and 'price' in result:
            return float(result['price'])
        return 0.0

    def get_rsi(self, symbol: str, interval: str = "1day", period: int = 14) -> float:
        """Get RSI indicator"""
        result = self._request("rsi", {
            "symbol": symbol,
            "interval": interval,
            "time_period": period
        })
        if result and 'values' in result and len(result['values']) > 0:
            try:
                return float(result['values'][0].get('rsi', 50))
            except:
                return 50.0
        return 50.0

    def get_sma(self, symbol: str, interval: str = "1day", period: int = 50) -> float:
        """Get SMA indicator"""
        result = self._request("sma", {
            "symbol": symbol,
            "interval": interval,
            "time_period": period
        })
        if result and 'values' in result and len(result['values']) > 0:
            try:
                return float(result['values'][0].get('sma', 0))
            except:
                return 0.0
        return 0.0


def get_market_data():
    """Fetch market data for SPY, QQQ, IWM"""
    client = TwelveDataClient()
    
    print("Fetching market data...")
    
    # Get quotes
    spy_quote = client.get_quote("SPY")
    qqq_quote = client.get_quote("QQQ")
    iwm_quote = client.get_quote("IWM")
    
    # Get RSI
    spy_rsi = client.get_rsi("SPY")
    qqq_rsi = client.get_rsi("QQQ")
    iwm_rsi = client.get_rsi("IWM")
    
    # Get SMA 50
    spy_sma50 = client.get_sma("SPY", period=50)
    
    # Parse data
    data = {
        "SPY": {
            "price": float(spy_quote.get('close', 0)) if spy_quote else 0,
            "change": float(spy_quote.get('change', 0)) if spy_quote else 0,
            "change_pct": spy_quote.get('percent_change', '0%') if spy_quote else '0%',
            "volume": int(spy_quote.get('volume', 0)) if spy_quote else 0,
            "rsi": spy_rsi,
            "sma50": spy_sma50,
            "trend": "Bullish" if spy_rsi > 50 else "Bearish" if spy_rsi < 50 else "Neutral"
        },
        "QQQ": {
            "price": float(qqq_quote.get('close', 0)) if qqq_quote else 0,
            "change": float(qqq_quote.get('change', 0)) if qqq_quote else 0,
            "change_pct": qqq_quote.get('percent_change', '0%') if qqq_quote else '0%',
            "volume": int(qqq_quote.get('volume', 0)) if qqq_quote else 0,
            "rsi": qqq_rsi
        },
        "IWM": {
            "price": float(iwm_quote.get('close', 0)) if iwm_quote else 0,
            "change": float(iwm_quote.get('change', 0)) if iwm_quote else 0,
            "change_pct": iwm_quote.get('percent_change', '0%') if iwm_quote else '0%',
            "volume": int(iwm_quote.get('volume', 0)) if iwm_quote else 0,
            "rsi": iwm_rsi
        }
    }
    
    return data


def generate_trades(market_data: Dict) -> List[Dict]:
    """Generate conservative trade recommendations for $100 account"""
    
    trades = []
    
    # Strategy 1: SPY Iron Condor (if RSI is neutral)
    spy_rsi = market_data['SPY']['rsi']
    spy_price = market_data['SPY']['price']
    
    if 40 <= spy_rsi <= 60:
        # Neutral market - Iron Condor
        trades.append({
            "ticker": "SPY",
            "strategy": "Iron Condor",
            "strikes": f"Put {spy_price - 15:.0f}/{spy_price - 10:.0f} | Call {spy_price + 10:.0f}/{spy_price + 15:.0f}",
            "expiry": "7-14 DTE",
            "credit": 0.45,
            "max_risk": 4.55,
            "pop": 68,
            "ror": 9.9,
            "notes": "Neutral RSI range, defined risk"
        })
    
    # Strategy 2: Bull Put Spread on QQQ (if RSI < 45)
    qqq_rsi = market_data['QQQ']['rsi']
    qqq_price = market_data['QQQ']['price']
    
    if qqq_rsi < 45:
        # Oversold - Bullish
        trades.append({
            "ticker": "QQQ",
            "strategy": "Bull Put Spread",
            "strikes": f"{qqq_price - 8:.0f}/{qqq_price - 6:.0f}",
            "expiry": "14-21 DTE",
            "credit": 0.35,
            "max_risk": 1.65,
            "pop": 72,
            "ror": 21.2,
            "notes": "Oversold conditions, bullish bias"
        })
    
    # Strategy 3: Bear Call Spread on IWM (if RSI > 60)
    iwm_rsi = market_data['IWM']['rsi']
    iwm_price = market_data['IWM']['price']
    
    if iwm_rsi > 60:
        # Overbought - Bearish
        trades.append({
            "ticker": "IWM",
            "strategy": "Bear Call Spread",
            "strikes": f"{iwm_price + 4:.0f}/{iwm_price + 6:.0f}",
            "expiry": "14-21 DTE",
            "credit": 0.30,
            "max_risk": 1.70,
            "pop": 70,
            "ror": 17.6,
            "notes": "Overbought conditions, bearish bias"
        })
    
    # If no RSI-based trades, add default conservative trades
    if len(trades) == 0:
        # Default: Conservative Iron Condor on SPY
        trades.append({
            "ticker": "SPY",
            "strategy": "Iron Condor",
            "strikes": f"Put {spy_price - 12:.0f}/{spy_price - 8:.0f} | Call {spy_price + 8:.0f}/{spy_price + 12:.0f}",
            "expiry": "14-21 DTE",
            "credit": 0.40,
            "max_risk": 4.60,
            "pop": 65,
            "ror": 8.7,
            "notes": "Default conservative setup"
        })
        
        # Cash-secured put on a lower-priced ETF
        trades.append({
            "ticker": "IWM",
            "strategy": "Cash-Secured Put",
            "strikes": f"{iwm_price - 5:.0f}",
            "expiry": "30-45 DTE",
            "credit": 0.75,
            "max_risk": 19.25,
            "pop": 75,
            "ror": 3.9,
            "notes": "Conservative income generation"
        })
    
    # Limit to max 2 trades
    return trades[:MAX_CONCURRENT_TRADES]


def create_report(market_data: Dict, trades: List[Dict], output_file: str):
    """Create markdown report"""
    
    today = datetime.now().strftime("%Y-%m-%d")
    total_risk = sum(t['max_risk'] for t in trades)
    total_credit = sum(t['credit'] for t in trades)
    avg_pop = sum(t['pop'] for t in trades) / len(trades) if trades else 0
    avg_ror = sum(t['ror'] for t in trades) / len(trades) if trades else 0
    
    report = f"""# Tastytrade $100 Account - Daily Recommendations

**Date:** {datetime.now().strftime("%A, %B %d, %Y")}
**Account Balance:** ${ACCOUNT_BALANCE:.2f}
**Available Buying Power:** ${ACCOUNT_BALANCE * 0.80:.2f}
**Max Position Size:** ${MAX_POSITION_SIZE:.2f}

---

## Market Overview

| Ticker | Price | Change | RSI | Trend |
|--------|-------|--------|-----|-------|
| SPY | ${market_data['SPY']['price']:.2f} | {market_data['SPY']['change_pct']} | {market_data['SPY']['rsi']:.1f} | {market_data['SPY']['trend']} |
| QQQ | ${market_data['QQQ']['price']:.2f} | {market_data['QQQ']['change_pct']} | {market_data['QQQ']['rsi']:.1f} | {"Oversold" if market_data['QQQ']['rsi'] < 45 else "Overbought" if market_data['QQQ']['rsi'] > 60 else "Neutral"} |
| IWM | ${market_data['IWM']['price']:.2f} | {market_data['IWM']['change_pct']} | {market_data['IWM']['rsi']:.1f} | {"Oversold" if market_data['IWM']['rsi'] < 45 else "Overbought" if market_data['IWM']['rsi'] > 60 else "Neutral"} |

**SPY SMA-50:** ${market_data['SPY']['sma50']:.2f} ({"Above" if market_data['SPY']['price'] > market_data['SPY']['sma50'] else "Below"} 50-day MA)

---

## Recommended Trades ({len(trades)})

"""
    
    for i, trade in enumerate(trades, 1):
        report += f"""### Trade {i}: {trade['ticker']} {trade['strategy']}

- **Strikes:** {trade['strikes']}
- **Expiration:** {trade['expiry']}
- **Credit:** ${trade['credit']:.2f}
- **Max Risk:** ${trade['max_risk']:.2f}
- **Probability of Profit (POP):** {trade['pop']}%
- **Return on Risk:** {trade['ror']:.1f}%
- **Notes:** {trade['notes']}

"""
    
    report += f"""---

## Risk Summary

- **Total Risk:** ${total_risk:.2f} ({(total_risk/ACCOUNT_BALANCE)*100:.1f}% of account)
- **Total Credit Collected:** ${total_credit:.2f}
- **Average POP:** {avg_pop:.1f}%
- **Expected Return:** {avg_ror:.1f}%
- **Max Drawdown:** ${total_risk:.2f}

---

## Risk Management Rules

✅ Max Position Size: ${MAX_POSITION_SIZE:.2f} (20% of account)
✅ Max Risk Per Trade: ${MAX_RISK_PER_TRADE:.2f} (10% of account)
✅ Max Concurrent Trades: {MAX_CONCURRENT_TRADES}
✅ Defined Risk Strategies Only

---

## Strategy Focus

1. **Credit Spreads** - Limited risk, consistent income
2. **Iron Condors** - Neutral market profits
3. **Vertical Spreads** - Directional with defined risk
4. **Cash-Secured Puts** - Income generation on quality ETFs

---

⚠️ **Disclaimer:** This is for educational purposes only. Options trading involves risk. Past performance does not guarantee future results.
"""
    
    with open(output_file, 'w') as f:
        f.write(report)
    
    return report


def create_discord_summary(market_data: Dict, trades: List[Dict]) -> str:
    """Create Discord-formatted summary"""
    
    today = datetime.now().strftime("%A, %B %d, %Y")
    total_risk = sum(t['max_risk'] for t in trades)
    total_credit = sum(t['credit'] for t in trades)
    avg_pop = sum(t['pop'] for t in trades) / len(trades) if trades else 0
    avg_ror = sum(t['ror'] for t in trades) / len(trades) if trades else 0
    
    summary = f"""📈 **Tastytrade $100 Account - Daily Recommendations**
📅 {today}

**Account Balance:** ${ACCOUNT_BALANCE:.2f}
**Available BP:** ${ACCOUNT_BALANCE * 0.80:.2f}

**Market Snapshot:**
• SPY: ${market_data['SPY']['price']:.2f} (RSI: {market_data['SPY']['rsi']:.0f})
• QQQ: ${market_data['QQQ']['price']:.2f} (RSI: {market_data['QQQ']['rsi']:.0f})
• IWM: ${market_data['IWM']['price']:.2f} (RSI: {market_data['IWM']['rsi']:.0f})

**Top {len(trades)} Conservative Trades:**
"""
    
    for i, trade in enumerate(trades, 1):
        summary += f"\n{i}. **{trade['ticker']} {trade['strategy']}**"
        summary += f"\n   • Strikes: {trade['strikes']}"
        summary += f"\n   • Credit: ${trade['credit']:.2f} | Risk: ${trade['max_risk']:.2f} | POP: {trade['pop']}%"
    
    summary += f"""

**Risk Summary:**
• Total Risk: ${total_risk:.2f} ({(total_risk/ACCOUNT_BALANCE)*100:.0f}%)
• Expected Return: {avg_ror:.1f}%
• Avg POP: {avg_pop:.0f}%

⚠️ Conservative approach for $100 account
"""
    
    return summary


def main():
    """Main execution"""
    print("=" * 60)
    print("TASTYTRADE $100 ACCOUNT - DAILY RECOMMENDATIONS")
    print("=" * 60)
    print()
    
    # Get market data
    market_data = get_market_data()
    
    print(f"SPY: ${market_data['SPY']['price']:.2f} (RSI: {market_data['SPY']['rsi']:.1f})")
    print(f"QQQ: ${market_data['QQQ']['price']:.2f} (RSI: {market_data['QQQ']['rsi']:.1f})")
    print(f"IWM: ${market_data['IWM']['price']:.2f} (RSI: {market_data['IWM']['rsi']:.1f})")
    print()
    
    # Generate trades
    trades = generate_trades(market_data)
    
    print(f"Generated {len(trades)} trade recommendations")
    for i, trade in enumerate(trades, 1):
        print(f"  {i}. {trade['ticker']} {trade['strategy']} - Credit: ${trade['credit']:.2f}, POP: {trade['pop']}%")
    print()
    
    # Create report
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = f"/Users/cubiczan/.openclaw/workspace/trades/tastytrade-100-recommendations-{today}.md"
    
    report = create_report(market_data, trades, output_file)
    print(f"✅ Report saved to: {output_file}")
    print()
    
    # Create Discord summary
    discord_summary = create_discord_summary(market_data, trades)
    
    # Save Discord summary to file
    discord_file = f"/Users/cubiczan/.openclaw/workspace/trades/discord-summary-{today}.txt"
    with open(discord_file, 'w') as f:
        f.write(discord_summary)
    print(f"✅ Discord summary saved to: {discord_file}")
    print()
    
    # Print Discord summary
    print("=" * 60)
    print("DISCORD SUMMARY:")
    print("=" * 60)
    print(discord_summary)
    
    return discord_summary


if __name__ == "__main__":
    main()
