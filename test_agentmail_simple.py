#!/usr/bin/env python3
"""
Simple AgentMail test with 3 accounts
"""

import json
import os
from datetime import datetime

def test_agentmail_config():
    """Test AgentMail configuration"""
    
    # Load configuration
    config_path = "/Users/cubiczan/.openclaw/workspace/agentmail_config.json"
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print("✅ AgentMail Configuration Test")
        print("=" * 50)
        
        # Show accounts
        accounts = config['agentmail_accounts']
        enabled = [a for a in accounts if a['enabled']]
        
        print(f"Total accounts: {len(accounts)}")
        print(f"Enabled accounts: {len(enabled)}")
        print()
        
        for i, account in enumerate(enabled, 1):
            print(f"Account {i}: {account['name']}")
            print(f"  Email: {account['from_email']}")
            print(f"  Name: {account['from_name']}")
            print(f"  Daily limit: {account['daily_limit']}")
            print(f"  Priority: {account['priority']}")
            print(f"  API Key: {account['api_key'][:20]}...")
            print()
        
        # Show rotation strategy
        print(f"Rotation strategy: {config['rotation_strategy']}")
        print(f"Daily total limit: {config['daily_total_limit']}")
        print(f"Rate limit: {config['rate_limit_per_minute']}/minute")
        print(f"Default sender: {config['default_sender']}")
        print(f"Tracking enabled: {config['tracking_enabled']}")
        
        print("\n" + "=" * 50)
        print("✅ Configuration test passed!")
        
        # Create a simple usage report
        report = {
            "test_timestamp": datetime.now().isoformat(),
            "accounts_tested": len(enabled),
            "account_names": [a['name'] for a in enabled],
            "total_daily_capacity": sum(a['daily_limit'] for a in enabled),
            "config_valid": True
        }
        
        # Save report
        report_path = "/Users/cubiczan/.openclaw/workspace/agentmail_test_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Report saved to: {report_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

if __name__ == "__main__":
    test_agentmail_config()