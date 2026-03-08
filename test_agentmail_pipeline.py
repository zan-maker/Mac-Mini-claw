#!/usr/bin/env python3
"""
Test AgentMail Pipeline with sample data
"""

import os
import sys
import json
import pandas as pd
import requests
from datetime import datetime
import time

class TestAgentMailPipeline:
    """Test pipeline with sample data"""
    
    def __init__(self):
        # Load AgentMail configuration
        config_path = "/Users/cubiczan/.openclaw/workspace/agentmail_config.json"
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize account tracking
        self.accounts = [a for a in self.config['agentmail_accounts'] if a['enabled']]
        
        print("="*80)
        print("🧪 Test AgentMail Pipeline")
        print("="*80)
        print(f"📧 AgentMail Accounts: {len(self.accounts)} enabled")
        for account in self.accounts:
            print(f"   • {account['name']}: {account['from_email']}")
        print("="*80)
        
        # AgentMail API configuration
        self.base_url = "https://api.agentmail.to/v0"
    
    def create_test_data(self, count: int = 10) -> pd.DataFrame:
        """Create test data with sample email addresses"""
        print(f"\n📝 Creating test data ({count} sample investors)...")
        
        # Sample investor data
        sample_data = []
        for i in range(count):
            sample_data.append({
                'contact_name': f'Test Investor {i+1}',
                'company': f'Test Investment Firm {i+1}',
                'email': f'test.investor{i+1}@example.com',  # Using example.com for testing
                'sectors': 'Technology, SaaS',
                'investment_thesis': 'Early-stage tech startups',
                'personalized_message': f"""Hi Test Investor {i+1},

This is a test message from the Bdev.ai Advanced Pipeline.

We're testing our AgentMail integration with 3 accounts to ensure reliable email delivery.

Best regards,
Sam Desigan
Agent Manager, Impact Quadrant""",
                'generated_at': datetime.now().isoformat(),
                'ai_model': 'test'
            })
        
        df = pd.DataFrame(sample_data)
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f"/Users/cubiczan/.openclaw/workspace/test_agentmail_data_{timestamp}.csv"
        df.to_csv(csv_path, index=False)
        
        print(f"   💾 Test data saved to: {csv_path}")
        print(f"   📊 Created {len(df)} test records")
        
        return df, csv_path
    
    def send_test_email(self, account: Dict, to_email: str) -> Dict:
        """Send test email via AgentMail"""
        headers = {
            "Authorization": f"Bearer {account['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inbox_id": account['from_email'],
            "to": [to_email],
            "subject": "Test: Bdev.ai AgentMail Integration",
            "text": f"""This is a test email from the Bdev.ai Advanced Pipeline.

Account: {account['name']}
From: {account['from_name']} <{account['from_email']}>
Time: {datetime.now().isoformat()}

This email confirms that the AgentMail integration is working correctly.

Best regards,
Test System"""
        }
        
        try:
            print(f"   🔄 Sending test email via {account['name']}...")
            response = requests.post(
                f"{self.base_url}/inboxes/{account['from_email']}/messages/send",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success! Message ID: {result.get('message_id', 'N/A')}")
                return {
                    'success': True,
                    'message_id': result.get('message_id'),
                    'account': account['name'],
                    'status': 'sent'
                }
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text[:200]}",
                    'account': account['name'],
                    'status': 'failed'
                }
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'account': account['name'],
                'status': 'error'
            }
    
    def test_all_accounts(self):
        """Test all AgentMail accounts"""
        print(f"\n🧪 Testing all AgentMail accounts...")
        
        test_email = "test@example.com"  # Using example.com for testing
        
        results = []
        for account in self.accounts:
            print(f"\n📧 Testing {account['name']} ({account['from_email']})...")
            result = self.send_test_email(account, test_email)
            results.append(result)
            
            # Brief pause between tests
            time.sleep(1)
        
        # Print summary
        print(f"\n" + "="*80)
        print("📊 TEST RESULTS SUMMARY")
        print("="*80)
        
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        
        print(f"Accounts Tested: {total_count}")
        print(f"✅ Successful: {success_count}")
        print(f"❌ Failed: {total_count - success_count}")
        
        for result in results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['account']}: {result.get('status', 'unknown')}")
            if not result['success']:
                print(f"   Error: {result.get('error', 'Unknown error')}")
        
        print("="*80)
        
        return results
    
    def run_pipeline_test(self, count: int = 5):
        """Run complete pipeline test"""
        print(f"\n🚀 Running complete pipeline test...")
        
        # Step 1: Create test data
        df, csv_path = self.create_test_data(count)
        
        # Step 2: Test all accounts
        results = self.test_all_accounts()
        
        # Step 3: Create report
        self.create_test_report(df, csv_path, results)
        
        return True
    
    def create_test_report(self, df: pd.DataFrame, csv_path: str, results: list):
        """Create test report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"/Users/cubiczan/.openclaw/workspace/test_agentmail_report_{timestamp}.md"
        
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)
        
        report = f"""# AgentMail Pipeline Test Report

## Test Execution
- **Timestamp**: {datetime.now().isoformat()}
- **Test Data**: {len(df)} sample investors
- **AgentMail Accounts**: {total_count} tested

## Test Results
- **✅ Successful Accounts**: {success_count}/{total_count}
- **❌ Failed Accounts**: {total_count - success_count}/{total_count}
- **📈 Success Rate**: {(success_count/total_count*100):.1f}%

## Account Details
"""
        
        for result in results:
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            report += f"""
### {result['account']} - {status}
- **Status**: {result.get('status', 'unknown')}
- **Message ID**: {result.get('message_id', 'N/A')}
"""
            if not result['success']:
                report += f"- **Error**: {result.get('error', 'Unknown error')}\n"
        
        report += f"""
## Test Data
- **CSV File**: {csv_path}
- **Records**: {len(df)}
- **Sample Emails**: {', '.join(df['email'].head(3).tolist())}...

## Configuration
- **Rotation Strategy**: {self.config.get('rotation_strategy', 'round_robin')}
- **Daily Total Limit**: {self.config.get('daily_total_limit', 3000)}
- **Rate Limit**: {self.config.get('rate_limit_per_minute', 60)}/minute

## Recommendations
"""
        
        if success_count == total_count:
            report += "✅ All accounts are working correctly. Ready for production use.\n"
        elif success_count > 0:
            report += f"⚠️ {success_count}/{total_count} accounts working. Check failed accounts.\n"
        else:
            report += "❌ No accounts working. Check API keys and configuration.\n"
        
        report += f"""
## Next Steps
1. Review failed accounts and fix configuration
2. Test with real email addresses
3. Run full pipeline with actual investor data
4. Monitor delivery rates and bounce rates

---
*Generated by AgentMail Pipeline Test*
*Test timestamp: {datetime.now().isoformat()}*
"""
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"\n📄 Test report saved to: {report_path}")
        print("="*80)
        print("🧪 Test complete!")
        print("="*80)

def main():
    """Main execution"""
    print("Starting AgentMail Pipeline Test...")
    
    pipeline = TestAgentMailPipeline()
    pipeline.run_pipeline_test(count=5)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())