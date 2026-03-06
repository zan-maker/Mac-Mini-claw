#!/usr/bin/env python3
"""
Setup complete portfolio with all gas positions
"""

import json
from datetime import datetime
import os

portfolio_file = '/Users/cubiczan/.openclaw/workspace/portfolio_reports/portfolio_data.json'

# Complete portfolio with all positions
portfolio = {
    'trades': [
        # Original Gas Month position (from earlier)
        {
            'id': 'gas_month_original_20260304',
            'market': 'Gas prices in the US this month > $3.50',
            'size': 25,
            'type': 'YES',
            'entry_price': 3.198,
            'target_price': 3.50,
            'entry_time': '2026-03-04T09:00:00',
            'settlement_date': '2026-03-31',
            'status': 'active',
            'notes': 'Original Gas Month position based on AAA price $3.198'
        },
        # New addition today
        {
            'id': 'gas_month_add_20260305_1801',
            'market': 'Gas prices in the US this month > $3.50',
            'size': 8,
            'type': 'YES',
            'entry_price': 3.20,
            'target_price': 3.50,
            'entry_time': datetime.now().isoformat(),
            'settlement_date': '2026-03-31',
            'status': 'active',
            'notes': 'Additional $8 added based on Iran conflict catalysts and 70% confidence recommendation'
        },
        # Gas Week position
        {
            'id': 'gas_week_original_20260304',
            'market': 'US gas prices this week > $3.310',
            'size': 50,
            'type': 'YES',
            'entry_price': 3.198,
            'target_price': 3.310,
            'entry_time': '2026-03-04T09:00:00',
            'settlement_date': '2026-03-08',
            'status': 'active',
            'notes': 'Gas Week position, needs +$0.112 to reach target'
        },
        # Completed Paxton trade
        {
            'id': 'paxton_trade_20260304',
            'market': 'Paxton short position',
            'size': 25,
            'type': 'SHORT',
            'entry_price': 0.25,
            'exit_price': 0.88,
            'entry_time': '2026-03-04T10:00:00',
            'exit_time': '2026-03-04T15:00:00',
            'profit': 88.00,
            'return_pct': 352.0,
            'status': 'completed',
            'notes': '352% return on Paxton political market'
        }
    ],
    'total_invested': 0,  # Will calculate
    'total_profit': 88.00,
    'active_trades_count': 0  # Will calculate
}

# Calculate totals
total_invested = 0
active_trades_count = 0

for trade in portfolio['trades']:
    if trade['status'] == 'active':
        total_invested += trade['size']
        active_trades_count += 1

portfolio['total_invested'] = total_invested
portfolio['active_trades_count'] = active_trades_count

# Save portfolio
os.makedirs(os.path.dirname(portfolio_file), exist_ok=True)
with open(portfolio_file, 'w') as f:
    json.dump(portfolio, f, indent=2)

print('✅ Complete portfolio setup:')
print(f'📊 Total invested (active): ${total_invested}')
print(f'📈 Total profit (completed): ${portfolio["total_profit"]}')
print(f'🔢 Active trades: {active_trades_count}')

print('\n📋 Active Positions:')
for trade in portfolio['trades']:
    if trade['status'] == 'active':
        print(f'   • {trade["market"]}: ${trade["size"]} {trade["type"]}')
        print(f'     Entry: ${trade["entry_price"]}, Target: ${trade["target_price"]}')
        print(f'     Days left: {(datetime.fromisoformat(trade["settlement_date"]) - datetime.now()).days}')

print('\n🏆 Completed Trades:')
for trade in portfolio['trades']:
    if trade['status'] == 'completed':
        print(f'   • {trade["market"]}: +${trade["profit"]} ({trade["return_pct"]}%)')

# Capital calculations
total_capital = 413  # Starting capital
remaining_capital = total_capital - total_invested

print(f'\n💰 Capital Summary:')
print(f'   Starting capital: ${total_capital}')
print(f'   Active investments: ${total_invested}')
print(f'   Completed profits: +${portfolio["total_profit"]}')
print(f'   Current total: ${total_capital + portfolio["total_profit"]}')
print(f'   Remaining for new trades: ${remaining_capital}')
print(f'   Invested %: {(total_invested/total_capital)*100:.1f}%')

print(f'\n📁 Portfolio saved to: {portfolio_file}')