#!/bin/bash

# Setup Automated Metals Monitoring System
# Copper, Gold, Silver, and Gas prices with Kalshi trading integration

echo "🚀 Setting up Automated Metals Monitoring System"
echo "================================================"

# Create monitoring directory
MONITORING_DIR="$HOME/.openclaw/workspace/metals_monitoring"
mkdir -p "$MONITORING_DIR"
echo "✅ Created monitoring directory: $MONITORING_DIR"

# Create main monitoring script
cat > "$MONITORING_DIR/metals-monitor.py" << 'EOF'
#!/usr/bin/env python3
"""
Main Metals Monitoring Script - Run by cron jobs
"""

import sys
import os
from datetime import datetime

# Add workspace to path
sys.path.append(os.path.expanduser('~/.openclaw/workspace/scripts'))

try:
    from metals_monitoring_daemon import MetalsMonitoringDaemon
    
    print(f"🔍 Metals Monitoring - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Initialize daemon
    daemon = MetalsMonitoringDaemon()
    
    # Run monitoring
    daemon.monitor_all_metals()
    
    print("✅ Monitoring complete")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
EOF

chmod +x "$MONITORING_DIR/metals-monitor.py"

# Create daily report script
cat > "$MONITORING_DIR/daily-report.py" << 'EOF'
#!/usr/bin/env python3
"""
Daily Metals Trading Report
"""

import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add workspace to path
sys.path.append(os.path.expanduser('~/.openclaw/workspace/scripts'))

try:
    from metals_monitoring_daemon import MetalsMonitoringDaemon
    
    print(f"📊 Daily Metals Report - {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    # Initialize daemon
    daemon = MetalsMonitoringDaemon()
    
    # Generate report
    report = daemon.run_daily_report()
    
    # Save report
    report_file = Path(daemon.monitoring_dir) / f"daily_report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Report saved: {report_file}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
EOF

chmod +x "$MONITORING_DIR/daily-report.py"

# Create configuration file
cat > "$MONITORING_DIR/config.json" << 'EOF'
{
  "monitoring": {
    "interval_minutes": 15,
    "markets": ["copper", "gold", "silver", "gas"],
    "sources": {
      "copper": "COMEX/LME",
      "gold": "COMEX",
      "silver": "COMEX",
      "gas": "AAA National Average"
    }
  },
  "trading": {
    "capital_allocation": 500,
    "max_position_size_percent": 5,
    "min_confidence_threshold": 0.7,
    "max_trades_per_day": 3
  },
  "alerts": {
    "price_move_threshold_percent": 2,
    "volatility_threshold_percent": 3,
    "notification_channels": ["log", "discord"]
  },
  "kalshi_integration": {
    "enabled": true,
    "market_prefixes": {
      "copper": "COPPER",
      "gold": "GOLD",
      "silver": "SILVER",
      "gas": "GAS"
    },
    "timeframes": ["WEEKLY", "MONTHLY", "QUARTERLY"]
  },
  "discord": {
    "enabled": false,
    "webhook_url": "YOUR_DISCORD_WEBHOOK_HERE",
    "channel_id": "YOUR_CHANNEL_ID_HERE"
  }
}
EOF

echo "✅ Created configuration file"

# Create initial price database
cat > "$MONITORING_DIR/init_database.py" << 'EOF'
#!/usr/bin/env python3
"""
Initialize metals price database with historical data
"""

import sqlite3
import json
from datetime import datetime, timedelta
import random

DB_PATH = "metals_prices.db"

# Sample historical prices (March 2026)
historical_data = {
    "copper": [5.75, 5.78, 5.79, 5.77, 5.80, 5.82, 5.79, 5.81, 5.83, 5.79],
    "gold": [2180.50, 2182.75, 2185.50, 2183.25, 2186.00, 2188.50, 2185.50, 2187.25, 2189.00, 2185.50],
    "silver": [24.60, 24.65, 24.85, 24.70, 24.90, 24.95, 24.85, 24.88, 24.92, 24.85],
    "gas": [3.15, 3.18, 3.20, 3.19, 3.21, 3.22, 3.20, 3.198, 3.205, 3.198]
}

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS metal_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        metal TEXT NOT NULL,
        price REAL NOT NULL,
        change_percent REAL,
        source TEXT,
        metadata TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS trading_signals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        metal TEXT NOT NULL,
        signal_type TEXT NOT NULL,
        current_price REAL,
        target_price REAL,
        confidence REAL,
        position_size REAL,
        kalshi_market TEXT,
        kalshi_direction TEXT,
        executed BOOLEAN DEFAULT FALSE
    )
''')

# Insert historical data
base_date = datetime.now() - timedelta(days=9)

for i in range(10):
    timestamp = base_date + timedelta(days=i)
    
    for metal, prices in historical_data.items():
        price = prices[i]
        change = random.uniform(-0.5, 0.5)  # Simulated change
        
        cursor.execute('''
            INSERT INTO metal_prices (timestamp, metal, price, change_percent, source, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            timestamp.isoformat(),
            metal,
            price,
            change,
            "historical",
            json.dumps({"simulated": True})
        ))

conn.commit()
conn.close()

print(f"✅ Database initialized with 10 days of historical data for 4 metals")
print(f"   Database: {DB_PATH}")
print(f"   Metals: Copper, Gold, Silver, Gas")
print(f"   Records: {10 * 4} price entries")
EOF

chmod +x "$MONITORING_DIR/init_database.py"

# Run database initialization
cd "$MONITORING_DIR" && python3 init_database.py

# Create cron job setup script
cat > "$MONITORING_DIR/setup-cron-jobs.sh" << 'EOF'
#!/bin/bash

# Setup cron jobs for metals monitoring

echo "⏰ Setting up Metals Monitoring Cron Jobs"
echo "========================================="

CRON_JOBS=(
    # Every 15 minutes: Monitor all metals
    "*/15 * * * * cd $HOME/.openclaw/workspace/metals_monitoring && python3 metals-monitor.py >> monitoring.log 2>&1"
    
    # 9:00 AM daily: Morning metals report
    "0 9 * * * cd $HOME/.openclaw/workspace/metals_monitoring && python3 daily-report.py >> daily_reports.log 2>&1"
    
    # 4:00 PM daily: End of day summary
    "0 16 * * * cd $HOME/.openclaw/workspace/metals_monitoring && python3 daily-report.py --end-of-day >> eod_reports.log 2>&1"
    
    # Monday 6:00 AM: Weekly metals outlook
    "0 6 * * 1 cd $HOME/.openclaw/workspace/metals_monitoring && python3 weekly-outlook.py >> weekly_outlook.log 2>&1"
)

# Add to crontab
for job in "${CRON_JOBS[@]}"; do
    (crontab -l 2>/dev/null | grep -F "$job") || (crontab -l 2>/dev/null; echo "$job") | crontab -
    echo "✅ Added: $job"
done

echo ""
echo "📋 Cron Jobs Summary:"
echo "   1. Every 15 minutes: Real-time metals monitoring"
echo "   2. 9:00 AM daily: Morning trading report"
echo "   3. 4:00 PM daily: End-of-day summary"
echo "   4. Monday 6:00 AM: Weekly outlook"
echo ""
echo "📁 Log files in: $HOME/.openclaw/workspace/metals_monitoring/"
echo "   - monitoring.log (15-minute updates)"
echo "   - daily_reports.log (morning reports)"
echo "   - eod_reports.log (end-of-day)"
echo "   - weekly_outlook.log (weekly outlook)"
EOF

chmod +x "$MONITORING_DIR/setup-cron-jobs.sh"

# Create weekly outlook script
cat > "$MONITORING_DIR/weekly-outlook.py" << 'EOF'
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
EOF

chmod +x "$MONITORING_DIR/weekly-outlook.py"

echo ""
echo "🎉 Metals Monitoring System Setup Complete!"
echo "==========================================="
echo ""
echo "📁 Monitoring Directory: $MONITORING_DIR"
echo ""
echo "📋 Files Created:"
echo "   ✅ metals-monitor.py - Main monitoring script"
echo "   ✅ daily-report.py - Daily trading report"
echo "   ✅ weekly-outlook.py - Weekly outlook"
echo "   ✅ config.json - Configuration file"
echo "   ✅ init_database.py - Database initialization"
echo "   ✅ setup-cron-jobs.sh - Cron job setup"
echo ""
echo "🔧 Next Steps:"
echo "   1. Review and edit config.json with your preferences"
echo "   2. Run: cd $MONITORING_DIR && ./setup-cron-jobs.sh"
echo "   3. Monitor logs in: $MONITORING_DIR/"
echo "   4. Check daily reports for trading signals"
echo ""
echo "💰 Trading Integration:"
echo "   - System monitors Copper, Gold, Silver, Gas prices"
echo "   - Generates Kalshi trading recommendations"
echo "   - Provides position sizing based on confidence"
echo "   - Sends alerts for significant price moves"
echo ""
echo "📊 To start monitoring immediately:"
echo "   cd $MONITORING_DIR && python3 metals-monitor.py"
echo ""
echo "✅ Setup complete! Run ./setup-cron-jobs.sh to enable automated monitoring."