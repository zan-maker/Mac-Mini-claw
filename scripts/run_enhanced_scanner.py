#!/usr/bin/env python3
"""
Enhanced Kalshi Profit Scanner with Pinchtab Integration
Main execution file
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.enhanced_profit_scanner import EnhancedProfitScanner

def main():
    """Main function to run enhanced profit scanner"""
    print("🎯 ENHANCED PROFIT SCANNER WITH PINCHTAB")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("💰 Available Capital: $47.00")
    print("=" * 60)
    
    # Create scanner instance
    scanner = EnhancedProfitScanner()
    
    try:
        # Run enhanced scan
        print("\n🚀 Starting enhanced scan with Pinchtab integration...")
        results = scanner.run_enhanced_scan()
        
        if "error" in results:
            print(f"\n❌ Scan failed: {results['error']}")
            return 1
        
        # Display detailed results
        print("\n" + "=" * 60)
        print("📈 DETAILED ANALYSIS")
        print("=" * 60)
        
        # Show recommendation
        rec = results.get("final_recommendation", {})
        print(f"\n🎯 FINAL RECOMMENDATION:")
        print(f"   Score: {rec.get('score', 0)}/100")
        print(f"   Action: {rec.get('recommendation', 'N/A')}")
        print(f"   Position: ${rec.get('position_size', '0')}")
        print(f"   Confidence: {rec.get('confidence', 'N/A')}")
        print(f"   Reasoning: {rec.get('reasoning', 'N/A')}")
        
        # Show insights
        analysis = results.get("combined_analysis", {})
        if analysis:
            print(f"\n🔍 KEY INSIGHTS:")
            for key, insight in analysis.items():
                if key == "gas_price_analysis":
                    print(f"   ⛽ Gas Price: ${insight.get('average_price', 0):.2f}")
                    print(f"     Target: ${insight.get('target', 0):.2f}")
                    print(f"     Discrepancy: ${insight.get('discrepancy', 0):.3f}")
                    print(f"     Recommendation: {insight.get('recommendation', 'N/A')}")
                elif key == "news_analysis":
                    print(f"   📰 News Analysis:")
                    print(f"     Catalysts: {insight.get('catalyst_count', 0)}")
                    print(f"     Intensity: {insight.get('total_intensity', 0)}")
                    print(f"     Iran News: {'✅' if insight.get('has_iran_news') else '❌'}")
                    print(f"     Sentiment: {insight.get('recommendation', 'N/A')}")
        
        # Show scan statistics
        print(f"\n📊 SCAN STATISTICS:")
        print(f"   Method: {results.get('scan_method', 'N/A')}")
        print(f"   Pinchtab Sources: {results.get('pinchtab_sources', 0)}")
        print(f"   API Opportunities: {results.get('api_opportunities', 0)}")
        
        # Save results
        output_file = "/Users/cubiczan/.openclaw/workspace/enhanced_scan_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        # Next steps
        print("\n🎯 NEXT STEPS:")
        print("1. Review detailed analysis in enhanced_scan_results.json")
        print("2. Consider executing recommended trade")
        print("3. Schedule enhanced scans every 2 hours")
        print("4. Monitor gas prices and news for changes")
        
        # Integration with trading bot
        print("\n🤖 INTEGRATION WITH TRADING BOT:")
        print("To automate trading based on this scan:")
        print("  python3 scripts/run_kalshi_bot.py")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error in enhanced scanner: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())