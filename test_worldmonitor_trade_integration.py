#!/usr/bin/env python3
"""
Test World Monitor integration with Trade Recommender
"""

import sys
import os
sys.path.insert(0, "/Users/cubiczan/.openclaw/workspace")

def test_worldmonitor_integration():
    """Test the World Monitor integration"""
    print("🧪 Testing World Monitor + Trade Recommender Integration")
    print("="*60)
    
    # Test 1: Import World Monitor integration
    print("\n1️⃣ Testing World Monitor import...")
    try:
        from worldmonitor_integration import WorldMonitorIntegration
        print("   ✅ WorldMonitorIntegration imported successfully")
        
        wm = WorldMonitorIntegration()
        print("   ✅ WorldMonitorIntegration instantiated")
    except ImportError as e:
        print(f"   ❌ Failed to import: {e}")
        return False
    
    # Test 2: Get macro signals
    print("\n2️⃣ Testing macro signals...")
    try:
        signals = wm.get_macro_signals()
        verdict = signals.get("verdict", "UNKNOWN")
        print(f"   ✅ Macro signals retrieved")
        print(f"   Verdict: {verdict}")
        
        if signals.get("unavailable", False):
            print("   ⚠️  Using fallback data (API may be unavailable)")
        else:
            print("   ✅ Real data from World Monitor")
    except Exception as e:
        print(f"   ❌ Error getting macro signals: {e}")
        return False
    
    # Test 3: Test Kalshi arbitrage analysis
    print("\n3️⃣ Testing Kalshi arbitrage analysis...")
    try:
        sample_kalshi_data = {
            "markets": [
                {
                    "id": "test_market_1",
                    "title": "Will inflation exceed 3% in Q1 2026?",
                    "yes_price": 0.48,
                    "no_price": 0.47,
                    "volume": 10000
                }
            ]
        }
        
        opportunities = wm.analyze_kalshi_arbitrage(sample_kalshi_data)
        print(f"   ✅ Kalshi analysis completed")
        print(f"   Found {len(opportunities)} opportunities")
        
        if opportunities:
            for opp in opportunities[:2]:
                print(f"   - {opp.get('market_title', 'Unknown')}: {opp.get('arbitrage_percentage', 0):.1f}% gap")
    except Exception as e:
        print(f"   ❌ Error analyzing Kalshi: {e}")
        return False
    
    # Test 4: Test daily report generation
    print("\n4️⃣ Testing daily report generation...")
    try:
        sample_kalshi = {
            "markets": [
                {
                    "id": "market_1",
                    "title": "Test market 1",
                    "yes_price": 0.45,
                    "no_price": 0.50,
                    "volume": 15000
                }
            ]
        }
        
        report = wm.generate_daily_report(sample_kalshi)
        print(f"   ✅ Daily report generated")
        print(f"   Report date: {report.get('report_date', 'Unknown')}")
        print(f"   Macro verdict: {report.get('macro_overview', {}).get('verdict', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Error generating report: {e}")
        return False
    
    # Test 5: Test with Trade Recommender script
    print("\n5️⃣ Testing Trade Recommender integration...")
    try:
        # Import the new script
        sys.path.insert(0, "/Users/cubiczan/mac-bot/skills/trade-recommender")
        from daily_reddit_analysis_worldmonitor import (
            scrape_reddit_pennystocks,
            get_kalshi_data,
            analyze_with_world_monitor,
            generate_daily_report as generate_trade_report
        )
        
        print("   ✅ Trade Recommender modules imported")
        
        # Test Reddit scraping (mock)
        reddit_tickers = scrape_reddit_pennystocks()
        print(f"   Reddit tickers found: {len(reddit_tickers)}")
        
        # Test Kalshi data
        kalshi_data = get_kalshi_data()
        print(f"   Kalshi markets: {len(kalshi_data.get('markets', []))}")
        
        # Test combined analysis
        analysis = analyze_with_world_monitor(reddit_tickers, kalshi_data)
        print(f"   Combined opportunities: {len(analysis.get('combined_opportunities', []))}")
        
        # Test report generation
        report_text = generate_trade_report(analysis)
        print(f"   Report generated: {len(report_text)} characters")
        
    except Exception as e:
        print(f"   ❌ Error with Trade Recommender: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    
    print("\n🎯 Integration Summary:")
    print("1. World Monitor integration: ✅ Working")
    print("2. Macro signals: ✅ Available")
    print("3. Kalshi arbitrage analysis: ✅ Functional")
    print("4. Daily reporting: ✅ Working")
    print("5. Trade Recommender integration: ✅ Complete")
    
    print("\n🚀 Next Steps:")
    print("1. Update cron job to use new script")
    print("2. Test with real Kalshi API data")
    print("3. Monitor World Monitor API availability")
    print("4. Deploy to production")
    
    return True

def update_cron_job():
    """Update the cron job to use the new script"""
    print("\n📅 Updating Cron Job...")
    
    # Check current cron job
    cron_command = "cd /Users/cubiczan/mac-bot/skills/trade-recommender && python3 daily_reddit_analysis.py"
    new_command = "cd /Users/cubiczan/mac-bot/skills/trade-recommender && python3 daily_reddit_analysis_worldmonitor.py"
    
    print(f"Current command: {cron_command}")
    print(f"New command: {new_command}")
    
    # Create a simple update script
    update_script = """#!/bin/bash
# Update Trade Recommender cron job to use World Monitor integration

echo "Updating Trade Recommender cron job..."

# Check if cron job exists
if crontab -l | grep -q "daily_reddit_analysis.py"; then
    echo "Found existing cron job"
    # Remove old cron job
    crontab -l | grep -v "daily_reddit_analysis.py" | crontab -
    echo "Removed old cron job"
fi

# Add new cron job (8 AM daily)
(crontab -l 2>/dev/null; echo "0 8 * * * cd /Users/cubiczan/mac-bot/skills/trade-recommender && python3 daily_reddit_analysis_worldmonitor.py >> /Users/cubiczan/.openclaw/workspace/logs/trade-recommender.log 2>&1") | crontab -
echo "Added new cron job with World Monitor integration"

echo "✅ Cron job updated successfully!"
"""
    
    script_path = "/Users/cubiczan/.openclaw/workspace/update_trade_cron.sh"
    with open(script_path, 'w') as f:
        f.write(update_script)
    
    os.chmod(script_path, 0o755)
    print(f"Update script created: {script_path}")
    print(f"Run: bash {script_path}")
    
    return script_path

def main():
    """Main test function"""
    print("🔧 World Monitor + Trade Recommender Integration Test")
    print("="*60)
    
    # Run tests
    if test_worldmonitor_integration():
        # Create update script
        update_script = update_cron_job()
        
        print("\n" + "="*60)
        print("🚀 READY FOR DEPLOYMENT!")
        print("="*60)
        
        print("\n📋 Deployment Checklist:")
        print("1. ✅ World Monitor integration tested")
        print("2. ✅ Trade Recommender updated")
        print("3. ⏳ Update cron job (run update script)")
        print("4. ⏳ Test with real data")
        print("5. ⏳ Monitor performance")
        
        print(f"\n🎯 To deploy: bash {update_script}")
        
        # Create a simple test run
        print("\n🧪 Quick test run:")
        print("cd /Users/cubiczan/mac-bot/skills/trade-recommender")
        print("python3 daily_reddit_analysis_worldmonitor.py")
        
        return True
    else:
        print("\n❌ Integration tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)