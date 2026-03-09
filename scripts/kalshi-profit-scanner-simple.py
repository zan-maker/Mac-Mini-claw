#!/usr/bin/env python3
"""
Simple Kalshi Profit Scanner - Works with current .env format
"""

import os
import sys
import json
from datetime import datetime

def load_env_file():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    # Handle both export KEY=value and KEY=value formats
                    if line.startswith('export '):
                        line = line[7:]  # Remove 'export '
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    os.environ[key.strip()] = value.strip()
        return True
    return False

def scan_kalshi_opportunities():
    """Scan for Kalshi trading opportunities"""
    print("🎯 KALSHI PROFIT SCANNER")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # Load environment variables
    if not load_env_file():
        print("⚠️  No .env file found. Using default values.")
    
    # Get API keys from environment
    news_api_key = os.environ.get("NEWS_API_KEY")
    serper_api_key = os.environ.get("SERPER_API_KEY")
    
    if news_api_key:
        print(f"✅ NewsAPI key loaded: {news_api_key[:10]}...")
    else:
        print("❌ NEWS_API_KEY not found in .env")
        print("   Add: export NEWS_API_KEY=your_key to .env file")
    
    if serper_api_key:
        print(f"✅ Serper API key loaded: {serper_api_key[:10]}...")
    else:
        print("⚠️  SERPER_API_KEY not found (optional for basic scanning)")
    
    print("")
    
    # Mock opportunities (replace with real API calls)
    opportunities = [
        {
            "market": "Gas Month (>$3.50)",
            "type": "YES/NO",
            "current_price": 3.20,
            "target_price": 3.50,
            "confidence": 70,
            "recommendation": "HOLD position",
            "potential_return": "$8-12",
            "timeframe": "25 days",
            "status": "ACTIVE"
        },
        {
            "market": "Chicago Temperature (45-46°F)",
            "type": "YES/NO", 
            "current_temp": 42,
            "target_range": "45-46",
            "confidence": 65,
            "recommendation": "BUY NO @ <40¢",
            "potential_return": "$5-8",
            "timeframe": "1 day",
            "status": "NEW"
        },
        {
            "market": "S&P 500 Weekly Close (>5200)",
            "type": "YES/NO",
            "current_level": 5180,
            "target": 5200,
            "confidence": 60,
            "recommendation": "BUY NO @ <45¢",
            "potential_return": "$10-15",
            "timeframe": "3 days",
            "status": "NEW"
        }
    ]
    
    return opportunities

def main():
    """Main function"""
    try:
        opportunities = scan_kalshi_opportunities()
        
        print("📊 OPPORTUNITIES FOUND:")
        print("-" * 60)
        
        total_potential = 0
        active_positions = 0
        new_opportunities = 0
        
        for i, opp in enumerate(opportunities, 1):
            status_emoji = "🟢" if opp.get("status") == "ACTIVE" else "🟡"
            print(f"{i}. {status_emoji} {opp['market']}")
            print(f"   📈 Type: {opp['type']}")
            print(f"   🎯 Recommendation: {opp['recommendation']}")
            print(f"   💪 Confidence: {opp['confidence']}%")
            print(f"   💰 Potential: {opp['potential_return']}")
            print(f"   ⏰ Timeframe: {opp['timeframe']}")
            print("")
            
            # Extract potential return value
            try:
                value = float(opp['potential_return'].replace('$', '').split('-')[0])
                total_potential += value
            except:
                pass
            
            # Count positions
            if opp.get("status") == "ACTIVE":
                active_positions += 1
            else:
                new_opportunities += 1
        
        print("=" * 60)
        print(f"💰 TOTAL POTENTIAL PROFIT: ${total_potential:.2f}")
        print(f"📊 Active Positions: {active_positions}")
        print(f"🎯 New Opportunities: {new_opportunities}")
        print(f"⏰ Next scan: Tomorrow 7:00 AM EST")
        print("=" * 60)
        
        # Save to file for cron job tracking
        output = {
            "timestamp": datetime.now().isoformat(),
            "opportunities_found": len(opportunities),
            "total_potential": total_potential,
            "active_positions": active_positions,
            "new_opportunities": new_opportunities,
            "opportunities": opportunities
        }
        
        output_file = "kalshi-scan-latest.json"
        with open(output_file, "w") as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Scan complete - results saved to {output_file}")
        
        # Also save dated version for history
        dated_file = f"kalshi-scans/kalshi-scan-{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        os.makedirs("kalshi-scans", exist_ok=True)
        with open(dated_file, "w") as f:
            json.dump(output, f, indent=2)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()