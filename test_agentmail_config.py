#!/usr/bin/env python3
"""
Test AgentMail configuration with 3 accounts
"""

import json
import os

print("="*80)
print("Testing AgentMail Configuration")
print("="*80)

# Load configuration
config_path = "/Users/cubiczan/.openclaw/workspace/agentmail_config.json"

if not os.path.exists(config_path):
    print("❌ Configuration file not found")
    exit(1)

with open(config_path, 'r') as f:
    config = json.load(f)

print(f"\n📋 Configuration loaded from: {config_path}")
print(f"   Rotation strategy: {config.get('rotation_strategy', 'N/A')}")
print(f"   Daily total limit: {config.get('daily_total_limit', 'N/A')}")

# Check accounts
accounts = config.get('agentmail_accounts', [])
enabled_accounts = [a for a in accounts if a.get('enabled', False)]

print(f"\n👥 AgentMail Accounts:")
print(f"   Total configured: {len(accounts)}")
print(f"   Enabled: {len(enabled_accounts)}")

for i, account in enumerate(accounts, 1):
    status = "✅ ENABLED" if account.get('enabled', False) else "❌ DISABLED"
    print(f"\n   {i}. {account.get('name', 'Unnamed')} - {status}")
    print(f"      API Key: {account.get('api_key', '')[:20]}...")
    print(f"      From: {account.get('from_name', 'N/A')} <{account.get('from_email', 'N/A')}>")
    print(f"      Priority: {account.get('priority', 'N/A')}")
    print(f"      Daily limit: {account.get('daily_limit', 'N/A')}")

# Verify the new account
print(f"\n🔍 Verifying new account (Zan King):")
zan_account = next((a for a in accounts if a.get('from_email') == 'zanking@agentmail.to'), None)

if zan_account:
    print(f"   ✅ Found: {zan_account.get('name')}")
    print(f"   API Key valid: {'am_us_' in zan_account.get('api_key', '')}")
    print(f"   Enabled: {zan_account.get('enabled', False)}")
    print(f"   Priority: {zan_account.get('priority', 'N/A')}")
else:
    print("   ❌ Account not found in configuration")

# Test configuration
print(f"\n🧪 Configuration test:")
print(f"   Primary account: {next((a for a in enabled_accounts if a.get('priority') == 1), {}).get('name', 'Not found')}")
print(f"   Secondary account: {next((a for a in enabled_accounts if a.get('priority') == 2), {}).get('name', 'Not found')}")
print(f"   Backup account: {next((a for a in enabled_accounts if a.get('priority') == 3), {}).get('name', 'Not found')}")

# Create simple load balancer test
print(f"\n⚖️ Load balancing test (simulated):")
from datetime import datetime
import random

# Simulate account selection
strategies = ['round_robin', 'random', 'least_used', 'priority']
for strategy in strategies:
    print(f"\n   Strategy: {strategy}")
    
    # Simulate 10 selections
    selections = []
    for _ in range(10):
        if strategy == 'round_robin':
            # Simple round robin
            account = enabled_accounts[_ % len(enabled_accounts)]
        elif strategy == 'random':
            account = random.choice(enabled_accounts)
        elif strategy == 'priority':
            # Sort by priority
            sorted_accounts = sorted(enabled_accounts, key=lambda x: x.get('priority', 999))
            account = sorted_accounts[0]
        else:  # least_used (simplified)
            account = enabled_accounts[0]
        
        selections.append(account['name'])
    
    # Count selections
    from collections import Counter
    counts = Counter(selections)
    for account_name, count in counts.items():
        print(f"      {account_name}: {count} times")

print(f"\n" + "="*80)
print("✅ Configuration test complete!")
print("="*80)

print(f"\n🚀 To use the new configuration:")
print(f"   1. Run: python3 bdev_ai_agentmail_advanced_complete.py --limit 10")
print(f"   2. Check: logs/bdev_ai_advanced/ for detailed logs")
print(f"   3. Monitor: bdev_ai_agentmail_summary.json for results")

print(f"\n📅 Scheduled pipelines:")
print(f"   • 9:00 AM: Basic Bdev.ai (50 messages)")
print(f"   • 9:15 AM: Basic pipeline (AI + AgentMail)")
print(f"   • 9:30 AM: Advanced pipeline (3 accounts, load balancing)")