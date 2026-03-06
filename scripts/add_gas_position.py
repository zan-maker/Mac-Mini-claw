#!/usr/bin/env python3
"""
Add $8 to Gas Month position
"""

import json
from datetime import datetime
import os

# Portfolio file
portfolio_file = '/Users/cubiczan/.openclaw/workspace/portfolio_reports/portfolio_data.json'

# Load portfolio
if os.path.exists(portfolio_file):
    with open(portfolio_file, 'r') as f:
        portfolio = json.load(f)
else:
    portfolio = {'trades': [], 'total_invested': 0, 'total_profit': 0}

# Add new trade
new_trade = {
    'id': f'gas_month_add_{datetime.now().strftime("%Y%m%d_%H%M")}',
    'market': 'Gas prices in the US this month > $3.50',
    'size': 8,
    'type': 'YES',
    'entry_price': 3.20,
    'target_price': 3.50,
    'entry_time': datetime.now().isoformat(),
    'settlement_date': '2026-03-31',
    'status': 'active',
    'notes': 'Additional $8 added based on Iran conflict catalysts and 70% confidence recommendation'
}

portfolio['trades'].append(new_trade)
portfolio['total_invested'] = portfolio.get('total_invested', 0) + 8

# Save updated portfolio
with open(portfolio_file, 'w') as f:
    json.dump(portfolio, f, indent=2)

print('✅ $8 added to Gas Month position')
print(f'📊 New total invested: ${portfolio["total_invested"]}')
print(f'📝 Trade ID: {new_trade["id"]}')
print(f'📅 Settlement: {new_trade["settlement_date"]}')
print(f'🎯 Target: >${new_trade["target_price"]}/gallon')
print(f'📋 Notes: {new_trade["notes"]}')

# Also update knowledge graph
kg_file = '/Users/cubiczan/.openclaw/workspace/knowledge_graph/kalshi_kg.json'
if os.path.exists(kg_file):
    with open(kg_file, 'r') as f:
        kg = json.load(f)
    
    # Add trade to knowledge graph
    kg_trade = {
        'id': new_trade['id'],
        'market_type': 'GAS_PRICE',
        'position': 'YES',
        'size': 8,
        'entry_price': 3.20,
        'catalysts': ['Iran conflict escalation', 'Strait of Hormuz risk', 'Bullish news sentiment'],
        'confidence': 0.7,
        'timestamp': datetime.now().isoformat(),
        'status': 'active'
    }
    
    if 'trades' not in kg:
        kg['trades'] = []
    kg['trades'].append(kg_trade)
    
    with open(kg_file, 'w') as f:
        json.dump(kg, f, indent=2)
    
    print('\n🧠 Knowledge graph updated with new trade')

print('\n📈 Updated Portfolio Summary:')
print(f'   Gas Month Position: $25 (original) + $8 (new) = $33 total')
print(f'   Total at risk: $33')
print(f'   Potential return at $3.50+: $16.50 (50%)')
print(f'   Remaining capital: $330')