#!/usr/bin/env python3
"""
Update portfolio totals after adding new position
"""

import json
import os

portfolio_file = '/Users/cubiczan/.openclaw/workspace/portfolio_reports/portfolio_data.json'

if os.path.exists(portfolio_file):
    with open(portfolio_file, 'r') as f:
        portfolio = json.load(f)
    
    # Calculate correct total invested (include all active trades)
    total_invested = 0
    active_trades = []
    
    for trade in portfolio.get('trades', []):
        if trade.get('status') == 'active':
            total_invested += trade.get('size', 0)
            active_trades.append(trade)
    
    portfolio['total_invested'] = total_invested
    portfolio['active_trades_count'] = len(active_trades)
    
    with open(portfolio_file, 'w') as f:
        json.dump(portfolio, f, indent=2)
    
    print(f'✅ Portfolio updated:')
    print(f'   Total invested: ${total_invested}')
    print(f'   Active trades: {len(active_trades)}')
    
    # Show active trades
    print(f'\n📊 Active Positions:')
    for trade in active_trades:
        print(f'   • {trade["market"]}: ${trade["size"]} {trade["type"]}')
        print(f'     Entry: ${trade.get("entry_price", "N/A")}, Target: ${trade.get("target_price", "N/A")}')
        print(f'     Settlement: {trade.get("settlement_date", "N/A")}')
    
    # Calculate remaining capital (assuming $413 total capital)
    total_capital = 413  # $338 remaining + $75 invested
    remaining_capital = total_capital - total_invested
    
    print(f'\n💰 Capital Summary:')
    print(f'   Total capital: ${total_capital}')
    print(f'   Total invested: ${total_invested}')
    print(f'   Remaining: ${remaining_capital}')
    print(f'   Invested %: {(total_invested/total_capital)*100:.1f}%')
    
else:
    print('❌ Portfolio file not found')