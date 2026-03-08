#!/usr/bin/env python3
"""
Weekly Metals Trading Outlook
"""

import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3

OUTLOOK_DIR = os.path.expanduser('~/.openclaw/workspace/metals_monitoring')
DB_PATH = os.path.join(OUTLOOK_DIR, "metals_prices.db")

def generate_weekly_outlook():
    """Generate weekly trading outlook"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get last week's data for each metal
    metals = ["copper", "gold", "silver", "gas"]
    outlook = {}
    
    for metal in metals:
        cursor.execute('''
            SELECT price, timestamp 
            FROM metal_prices 
            WHERE metal = ? 
            AND timestamp >= datetime('now', '-7 days')
            ORDER BY timestamp
        ''', (metal,))
        
        prices = cursor.fetchall()
        
        if not prices:
            continue
        
        # Calculate metrics
        price_values = [p[0] for p in prices]
        current_price = price_values[-1]
        week_high = max(price_values)
        week_low = min(price_values)
        week_change = ((current_price - price_values[0]) / price_values[0]) * 100
        
        # Determine trend
        if len(price_values) >= 5:
            last_5_avg = sum(price_values[-5:]) / 5
            first_5_avg = sum(price_values[:5]) / 5
            trend = "bullish" if last_5_avg > first_5_avg else "bearish"
        else:
            trend = "neutral"
        
        # Generate outlook
        outlook[metal] = {
            "current_price": round(current_price, 2),
            "week_high": round(week_high, 2),
            "week_low": round(week_low, 2),
            "week_change_percent": round(week_change, 2),
            "trend": trend,
            "volatility": round((week_high - week_low) / week_low * 100, 2),
            "recommendation": "hold"  # Default
        }
        
        # Generate trading recommendation
        if abs(week_change) > 3:
            outlook[metal]["recommendation"] = "monitor closely"
        if week_change > 5 and trend == "bullish":
            outlook[metal]["recommendation"] = "consider buying"
        elif week_change < -5 and trend == "bearish":
            outlook[metal]["recommendation"] = "consider selling"
    
    conn.close()
    
    # Generate report
    report_date = datetime.now().strftime('%Y-%m-%d')
    report = f"""# Weekly Metals Trading Outlook
## Week of {report_date}

### Summary
Weekly analysis of Copper, Gold, Silver, and Gas prices for Kalshi trading opportunities.

"""
    
    for metal, data in outlook.items():
        report += f"""### {metal.upper()}
- **Current Price:** ${data['current_price']}
- **Week Range:** ${data['week_low']} - ${data['week_high']}
- **Weekly Change:** {data['week_change_percent']}%
- **Trend:** {data['trend'].upper()}
- **Volatility:** {data['volatility']}%
- **Recommendation:** **{data['recommendation'].upper()}**

"""
    
    report += """### Trading Strategy
1. **Copper:** Monitor China demand and supply disruptions
2. **Gold:** Watch USD strength and interest rate expectations
3. **Silver:** Follow gold but with higher volatility
4. **Gas:** Track inventory reports and geopolitical events

### Kalshi Opportunities
Look for weekly prediction markets with:
- Clear catalysts (economic data, geopolitical events)
- High probability setups (>70% confidence)
- Favorable risk/reward (minimum 2:1)

### Risk Management
- Maximum 5% of capital per trade
- Use stop-losses on all positions
- Diversify across metals
- Monitor correlations

---
*Report generated automatically by Metals Monitoring System*
"""
    
    return report

if __name__ == "__main__":
    print(f"📈 Weekly Metals Outlook - {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    outlook = generate_weekly_outlook()
    
    # Save to file
    outlook_file = os.path.join(OUTLOOK_DIR, f"weekly_outlook_{datetime.now().strftime('%Y%m%d')}.md")
    with open(outlook_file, 'w') as f:
        f.write(outlook)
    
    print(outlook)
    print(f"\n✅ Outlook saved: {outlook_file}")
