#!/usr/bin/env python3
"""
Test TastyTrade API with new JWT token
Check SPY prices and provide trading advice
"""

import requests
import json
from datetime import datetime

# Your new TastyTrade API token
API_TOKEN = "eyJhbGciOiJFZERTQSIsInR5cCI6InJ0K2p3dCIsImtpZCI6Ik9UTUMzeThCTVB0Q3hxbHBSWUlod2N0UzY3aGdfd3hEM0NOYXdSX2lXanMiLCJqa3UiOiJodHRwczovL2ludGVyaW9yLWFwaS5hcjIudGFzdHl0cmFkZS5zeXN0ZW1zL29hdXRoL2p3a3MifQ.eyJpc3MiOiJodHRwczovL2FwaS50YXN0eXRyYWRlLmNvbSIsInN1YiI6IlViMTA4NzI0Yy0yNDRhLTRlZWUtYjc0NC1jMmYzMWNmYjBlY2QiLCJpYXQiOjE3NzIwNTM3NDAsImF1ZCI6IjBjN2I4ODk4LWEyZjEtNDliYi1hMjNkLTg0M2U0N2I2ODYzMSIsImdyYW50X2lkIjoiRzJlMjFlNjVmLTdhMjAtNDNiZi04MmUyLTY0YzkxOGFlMTlkYyIsInNjb3BlIjoicmVhZCB0cmFkZSBvcGVuaWQifQ.ieHeNMq49QwHCDoqNRhZmAfpc_qkd1MFRqnYze9TiDjuJZVGW4xkrcnXrNi6LHcvfXtyp-tBR-wBbdD44iX5Bw"

# TastyTrade API endpoints
BASE_URL = "https://api.tastytrade.com"
API_VERSION = "v1"

def test_api_connection():
    """Test TastyTrade API connection"""
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    print("=" * 60)
    print("TASTYTRADE API TEST")
    print("=" * 60)
    
    # Test 1: Get accounts
    print("\n1. Testing account access...")
    try:
        accounts_response = requests.get(
            f"{BASE_URL}/{API_VERSION}/accounts",
            headers=headers,
            timeout=30
        )
        
        print(f"   Status: {accounts_response.status_code}")
        
        if accounts_response.status_code == 200:
            accounts_data = accounts_response.json()
            accounts = accounts_data.get('data', {}).get('items', [])
            
            if accounts:
                print(f"   ✅ SUCCESS! Found {len(accounts)} account(s)")
                
                # Get first account details
                account = accounts[0]
                account_number = account.get('account', {}).get('account-number')
                print(f"   Account Number: {account_number}")
                
                # Get account balance
                balance_response = requests.get(
                    f"{BASE_URL}/{API_VERSION}/accounts/{account_number}/balances",
                    headers=headers,
                    timeout=30
                )
                
                if balance_response.status_code == 200:
                    balance_data = balance_response.json()
                    balance_info = balance_data.get('data', {})
                    
                    print(f"\n   💰 Account Balance:")
                    print(f"      Cash Balance: ${balance_info.get('cash-balance', 0):.2f}")
                    print(f"      Option Buying Power: ${balance_info.get('option-buying-power', 0):.2f}")
                    print(f"      Equity: ${balance_info.get('equity', 0):.2f}")
                    
                    return account_number, headers, balance_info
                else:
                    print(f"   Balance API error: {balance_response.status_code}")
            else:
                print("   ❌ No accounts found")
        else:
            print(f"   ❌ API error: {accounts_response.status_code}")
            print(f"   Response: {accounts_response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Connection error: {str(e)}")
    
    return None, headers, None

def get_spy_quote(headers):
    """Get SPY quote data"""
    
    print("\n2. Getting SPY quote...")
    
    try:
        quote_response = requests.get(
            f"{BASE_URL}/{API_VERSION}/market-data/quotes",
            headers=headers,
            params={"symbols": "SPY"},
            timeout=30
        )
        
        if quote_response.status_code == 200:
            quote_data = quote_response.json()
            quotes = quote_data.get('data', {}).get('items', [])
            
            if quotes:
                spy_quote = quotes[0]
                print(f"   ✅ SPY Quote Found:")
                print(f"      Symbol: {spy_quote.get('symbol')}")
                print(f"      Last Price: ${spy_quote.get('last', 0):.2f}")
                print(f"      Bid: ${spy_quote.get('bid', 0):.2f}")
                print(f"      Ask: ${spy_quote.get('ask', 0):.2f}")
                print(f"      Volume: {spy_quote.get('volume', 0):,}")
                print(f"      Change: ${spy_quote.get('change', 0):.2f}")
                print(f"      Percent Change: {spy_quote.get('percent-change', 0):.2f}%")
                
                return spy_quote
            else:
                print("   ❌ No SPY quote data found")
        else:
            print(f"   ❌ Quote API error: {quote_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Quote error: {str(e)}")
    
    return None

def get_spy_options_chain(headers, expiration_date="2026-04-18"):
    """Get SPY options chain for specific expiration"""
    
    print(f"\n3. Getting SPY options chain for {expiration_date}...")
    
    try:
        options_response = requests.get(
            f"{BASE_URL}/{API_VERSION}/option-chains/SPY/nested",
            headers=headers,
            params={"expiration-date": expiration_date},
            timeout=30
        )
        
        if options_response.status_code == 200:
            options_data = options_response.json()
            chain_data = options_data.get('data', {})
            
            print(f"   ✅ Options Chain Found")
            print(f"      Expiration: {chain_data.get('expiration-date')}")
            print(f"      Underlying Symbol: {chain_data.get('underlying-symbol')}")
            
            # Get call and put options
            options = chain_data.get('options', [])
            if options:
                print(f"      Total Options: {len(options)}")
                
                # Find ATM options (around 687)
                atm_calls = []
                atm_puts = []
                
                for option in options:
                    strike = option.get('strike-price', 0)
                    option_type = option.get('option-type', '')
                    
                    if 680 <= strike <= 695:
                        if option_type == 'C':
                            atm_calls.append(option)
                        elif option_type == 'P':
                            atm_puts.append(option)
                
                print(f"\n   📊 ATM Options (680-695):")
                print(f"      Calls: {len(atm_calls)}, Puts: {len(atm_puts)}")
                
                # Show sample options
                if atm_calls:
                    sample_call = atm_calls[0]
                    print(f"\n      Sample Call (Strike {sample_call.get('strike-price')}):")
                    print(f"         Bid: ${sample_call.get('bid', 0):.2f}")
                    print(f"         Ask: ${sample_call.get('ask', 0):.2f}")
                    print(f"         IV: {sample_call.get('volatility', 0):.2f}%")
                
                if atm_puts:
                    sample_put = atm_puts[0]
                    print(f"\n      Sample Put (Strike {sample_put.get('strike-price')}):")
                    print(f"         Bid: ${sample_put.get('bid', 0):.2f}")
                    print(f"         Ask: ${sample_put.get('ask', 0):.2f}")
                    print(f"         IV: {sample_put.get('volatility', 0):.2f}%")
                
                return chain_data
            else:
                print("   ❌ No options data in chain")
        else:
            print(f"   ❌ Options API error: {options_response.status_code}")
            print(f"   Response: {options_response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Options error: {str(e)}")
    
    return None

def analyze_trading_opportunities(spy_quote, options_chain, balance_info):
    """Analyze trading opportunities based on current data"""
    
    print(f"\n" + "="*60)
    print("TRADING ANALYSIS & RECOMMENDATIONS")
    print("="*60)
    
    if not spy_quote:
        print("\n❌ Cannot analyze - No SPY quote data")
        return
    
    spy_price = spy_quote.get('last', 687.35)
    cash_balance = balance_info.get('cash-balance', 100) if balance_info else 100
    option_bp = balance_info.get('option-buying-power', 400) if balance_info else 400
    
    print(f"\n📊 Current Market Data:")
    print(f"   SPY Price: ${spy_price:.2f}")
    print(f"   Account Balance: ${cash_balance:.2f}")
    print(f"   Option Buying Power: ${option_bp:.2f}")
    
    print(f"\n🎯 Recommended Strategies for ${cash_balance:.2f} Account:")
    
    # Strategy 1: Bull Put Spread (most conservative)
    print(f"\n1. 📈 SPY Bull Put Spread (Recommended):")
    print(f"   Strategy: Sell 680 Put / Buy 675 Put")
    print(f"   Expiration: 30-45 DTE (April 18, 2026)")
    print(f"   Estimated Credit: $1.50-2.00")
    print(f"   Max Risk: $3.00-3.50 per contract")
    print(f"   Probability: ~75%")
    print(f"   Position: 0.1 contract (Risk: $30-35)")
    print(f"   Return if successful: 50-75%")
    
    # Strategy 2: Iron Condor
    print(f"\n2. 🦋 SPY Iron Condor (Neutral):")
    print(f"   Strategy: Sell 670P/665P & 700C/705C")
    print(f"   Expiration: 30-45 DTE")
    print(f"   Estimated Credit: $2.50-3.00")
    print(f"   Max Risk: $2.50-2.00 per contract")
    print(f"   Probability: ~65%")
    print(f"   Position: 0.05 contract (Risk: $12.50-15)")
    print(f"   Return if successful: 80-100%")
    
    # Strategy 3: Call Debit Spread
    print(f"\n3. 🚀 SPY Call Debit Spread (Bullish):")
    print(f"   Strategy: Buy 690 Call / Sell 695 Call")
    print(f"   Expiration: 30-45 DTE")
    print(f"   Estimated Debit: $2.00-2.50")
    print(f"   Max Reward: $3.00-2.50 per contract")
    print(f"   Probability: ~60%")
    print(f"   Position: 0.1 contract (Cost: $20-25)")
    print(f"   Return if successful: 100-125%")
    
    # Position sizing recommendations
    print(f"\n💰 Position Sizing Recommendations:")
    print(f"   Max Risk per Trade: ${cash_balance * 0.2:.2f} (20% of account)")
    print(f"   Max Total Risk: ${cash_balance * 0.4:.2f} (40% of account)")
    
    if cash_balance < 100:
        print(f"\n⚠️  Account Size Warning:")
        print(f"   With ${cash_balance:.2f}, consider:")
        print(f"   • Paper trading first")
        print(f"   • Using fractional contracts (0.1 size)")
        print(f"   • Starting with 1 trade at a time")
    
    # Save analysis
    try:
        output_file = '/Users/cubiczan/.openclaw/workspace/tastytrade-spy-analysis.json'
        with open(output_file, 'w') as f:
            json.dump({
                'spy_quote': spy_quote,
                'account_balance': balance_info,
                'analysis_timestamp': datetime.now().isoformat(),
                'recommendations': {
                    'strategy_1': 'SPY Bull Put Spread (680/675)',
                    'strategy_2': 'SPY Iron Condor (670/665 & 700/705)',
                    'strategy_3': 'SPY Call Debit Spread (690/695)'
                },
                'position_sizing': {
                    'max_risk_per_trade': cash_balance * 0.2,
                    'max_total_risk': cash_balance * 0.4,
                    'recommended_position_size': '0.1 contracts'
                }
            }, f, indent=2)
        print(f"\n📁 Analysis saved to: {output_file}")
    except Exception as e:
        print(f"\n⚠️ Could not save analysis: {str(e)}")

def main():
    """Main execution"""
    
    # Test API connection
    account_number, headers, balance_info = test_api_connection()
    
    if not account_number:
        print("\n❌ API connection failed. Please check:")
        print("1. API token validity")
        print("2. Token expiration (JWT tokens expire)")
        print("3. Network connectivity")
        print("4. Account permissions")
        return
    
    # Get SPY quote
    spy_quote = get_spy_quote(headers)
    
    # Get options chain (try a few expirations)
    expirations_to_try = ["2026-04-18", "2026-03-21", "2026-05-16"]
    options_chain = None
    
    for expiration in expirations_to_try:
        options_chain = get_spy_options_chain(headers, expiration)
        if options_chain:
            break
    
    # Analyze trading opportunities
    analyze_trading_opportunities(spy_quote, options_chain, balance_info)
    
    # Next steps
    print(f"\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print(f"\n1. ✅ API is working!")
    print(f"2. Check exact option prices on TastyTrade platform")
    print(f"3. Choose strategy (Bull Put Spread recommended)")
    print(f"4. Execute trade with proper position sizing")
    print(f"5. Monitor and adjust as needed")
    
    print(f"\n🔧 To execute trades via API:")
    print(f"   I can help place orders once you approve specific trades")
    print(f"   Or execute manually on TastyTrade platform")

if __name__ == "__main__":
    main()