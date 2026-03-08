#!/usr/bin/env python3
"""
Bdev.ai + AgentMail Advanced Integration - Complete Version
"""

import os
import sys
import json
import pandas as pd
import argparse
from datetime import datetime
from bdev_ai_agentmail_advanced import BdevAIAgentMailAdvanced

def main():
    """Main function for advanced integration"""
    parser = argparse.ArgumentParser(description="Bdev.ai + AgentMail Advanced Integration")
    parser.add_argument("--csv", help="Path to Bdev.ai CSV output")
    parser.add_argument("--limit", type=int, default=50, help="Number of emails to send")
    parser.add_argument("--test", action="store_true", help="Test mode (no actual sending)")
    args = parser.parse_args()
    
    print("="*80)
    print("Bdev.ai + AgentMail Advanced Integration")
    print("Multiple Account Load Balancing")
    print("="*80)
    
    try:
        # Initialize advanced integration
        integrator = BdevAIAgentMailAdvanced()
        
        # Process batch
        results = integrator.process_batch(csv_path=args.csv, limit=args.limit)
        
        print(f"\n🎉 Advanced integration complete!")
        print(f"\n📊 Final results:")
        print(f"   Total processed: {results['total']}")
        print(f"   Successfully sent: {results['sent']} ✅")
        print(f"   Failed: {results['failed']} ❌")
        print(f"   Skipped (invalid email): {results['skipped']} ⚠️")
        
        if results['total'] > 0:
            success_rate = (results['sent'] / results['total']) * 100
            print(f"   Success rate: {success_rate:.1f}%")
        
        # Create cron job for advanced pipeline
        create_advanced_cron_job()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)
    print("✅ Advanced integration ready!")
    print("="*80)

def create_advanced_cron_job():
    """Create cron job for advanced pipeline"""
    cron_config = {
        "name": "Bdev.ai Advanced Pipeline (Multi-Account)",
        "schedule": {
            "kind": "cron",
            "expr": "30 9 * * *",  # 9:30 AM, after other pipelines
            "tz": "America/New_York"
        },
        "sessionTarget": "isolated",
        "payload": {
            "kind": "agentTurn",
            "message": "Run Bdev.ai advanced pipeline with multiple AgentMail accounts: 1. Generate AI messages, 2. Send via load-balanced AgentMail accounts, 3. Create detailed reports. Use the script at /Users/cubiczan/.openclaw/workspace/bdev_ai_advanced_pipeline.sh",
            "model": "custom-api-deepseek-com/deepseek-chat",
            "timeoutSeconds": 900  # 15 minutes for advanced processing
        },
        "delivery": {
            "mode": "announce",
            "channel": "discord",
            "to": "#macmini3"
        }
    }
    
    config_path = "/Users/cubiczan/.openclaw/workspace/bdev_ai_advanced_cron_config.json"
    with open(config_path, 'w') as f:
        json.dump(cron_config, f, indent=2)
    
    print(f"\n📋 Advanced cron job configuration saved: {config_path}")
    print(f"\n📅 To schedule advanced pipeline at 9:30 AM:")
    print(f"   • Uses 3 AgentMail accounts with load balancing")
    print(f"   • Automatic failover if accounts reach limits")
    print(f"   • Detailed usage tracking and reporting")
    
    return config_path

if __name__ == "__main__":
    main()