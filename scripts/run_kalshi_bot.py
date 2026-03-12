#!/usr/bin/env python3
"""
Kalshi Trading Bot with Pinchtab Integration
Main execution file
"""

import os
import sys
import json
import time
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.kalshi_trading_bot import KalshiTradingBot

def main():
    """Main function to run the Kalshi trading bot"""
    print("🚀 KALSHI TRADING BOT WITH PINCHTAB")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💰 Available Capital: $47.00")
    print("=" * 60)
    
    # Create bot instance
    bot = KalshiTradingBot()
    
    try:
        # Setup bot
        print("\n1. Setting up Pinchtab browser automation...")
        if not bot.setup():
            print("❌ Failed to setup bot")
            return 1
        
        print("✅ Bot setup complete")
        
        # Run trading cycle
        print("\n2. Running trading analysis...")
        analysis = bot.run_trading_cycle()
        
        if "error" in analysis:
            print(f"❌ Analysis error: {analysis['error']}")
        else:
            print(f"✅ Analysis complete")
            print(f"   Opportunity Score: {analysis.get('opportunity_score', 0)}%")
            print(f"   Recommendation: {analysis.get('recommendation', 'N/A')}")
            print(f"   Position Size: ${analysis.get('position_size', 0):.2f}")
            print(f"   Confidence: {analysis.get('confidence', 'N/A')}")
        
        # Monitor active trades
        print("\n3. Monitoring active trades...")
        bot.monitor_active_trades()
        
        # Generate report
        print("\n4. Generating trading report...")
        report = bot.generate_report()
        
        print("\n📊 TRADING REPORT:")
        print("-" * 40)
        print(f"Available Capital: ${report.get('available_capital', 0):.2f}")
        print(f"Active Trades: {report.get('active_trades', 0)}")
        print(f"Closed Trades: {report.get('closed_trades', 0)}")
        print(f"Total Profit: ${report.get('total_profit', 0):.2f}")
        
        # Save report
        report_file = "/Users/cubiczan/.openclaw/workspace/kalshi_bot_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n📁 Report saved to: {report_file}")
        
        print("\n🎉 Trading bot execution complete!")
        
        # Suggest next actions
        print("\n🎯 NEXT ACTIONS:")
        print("1. Review analysis in kalshi_analysis.json")
        print("2. Check active trades in kalshi_trades.json")
        print("3. Schedule bot to run every 2 hours")
        print("4. Monitor gas prices and Iran news")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error in main execution: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up resources...")
        bot.cleanup()
        print("✅ Cleanup complete")

if __name__ == "__main__":
    sys.exit(main())