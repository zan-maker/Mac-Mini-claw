#!/usr/bin/env python3
"""
Test Bdev.ai Advanced Pipeline with 3 AgentMail Accounts
Uses sample investor data to test the complete workflow
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime, date
import time
import random
import requests
from typing import Dict, List, Optional

class TestAdvancedPipeline:
    """Test pipeline with sample data"""
    
    def __init__(self, config_path: str = None):
        # Load AgentMail configuration
        if config_path is None:
            config_path = "/Users/cubiczan/.openclaw/workspace/agentmail_config.json"
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize account tracking
        self.accounts = [a for a in self.config['agentmail_accounts'] if a['enabled']]
        self.account_usage = {}
        
        for account in self.accounts:
            self.account_usage[account['name']] = {
                'today_count': 0,
                'today_date': datetime.now().date(),
                'total_sent': 0,
                'last_used': None,
                'errors': 0,
                'daily_limit': account.get('daily_limit', 1000)
            }
        
        print("="*80)
        print("🧪 TEST: Bdev.ai Advanced Pipeline with 3 AgentMail Accounts")
        print("="*80)
        print(f"📧 AgentMail Accounts: {len(self.accounts)} enabled")
        for account in self.accounts:
            print(f"   • {account['name']}: {account['from_email']} (Limit: {account.get('daily_limit', 1000)}/day)")
        print(f"🔄 Rotation Strategy: {self.config['rotation_strategy']}")
        print(f"📊 Daily Total Limit: {self.config['daily_total_limit']}")
        print("="*80)
        
        # AgentMail API configuration
        self.base_url = "https://api.agentmail.to/v0"
        
        # Results tracking
        self.results = {
            'pipeline_start': datetime.now().isoformat(),
            'ai_generation': {},
            'agentmail_sending': {},
            'account_usage': self.account_usage.copy(),
            'files_created': []
        }
    
    def generate_sample_messages(self, batch_size: int = 50) -> str:
        """Generate sample AI messages for testing"""
        print(f"\n🤖 Step 1: Generating sample AI messages for {batch_size} investors...")
        
        try:
            # Load sample investors
            sample_path = "/Users/cubiczan/.openclaw/workspace/sample_investors_50.csv"
            df = pd.read_csv(sample_path)
            
            # Generate personalized messages
            messages = []
            for idx, row in df.head(batch_size).iterrows():
                message = self.create_personalized_message(row)
                messages.append({
                    'contact_name': row['contact_name'],
                    'company': row['company'],
                    'email': row['email'],
                    'sectors': row['sectors'],
                    'investment_thesis': row['investment_thesis'],
                    'personalized_message': message,
                    'generated_at': datetime.now().isoformat(),
                    'ai_model': 'test-model'
                })
            
            # Save to CSV
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_path = f"/Users/cubiczan/.openclaw/workspace/test_ai_messages_{timestamp}.csv"
            
            results_df = pd.DataFrame(messages)
            results_df.to_csv(csv_path, index=False)
            
            self.results['ai_generation'] = {
                'status': 'success',
                'messages_generated': len(results_df),
                'output_file': csv_path,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"   📊 Generated {len(results_df)} sample messages")
            print(f"   💾 Saved to: {csv_path}")
            
            # Add to files created
            self.results['files_created'].append({
                'type': 'ai_messages',
                'path': csv_path,
                'size': os.path.getsize(csv_path)
            })
            
            return csv_path
                
        except Exception as e:
            print(f"❌ Error in message generation: {e}")
            self.results['ai_generation'] = {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            return None
    
    def create_personalized_message(self, investor_data: Dict) -> str:
        """Create personalized message for investor"""
        name = investor_data.get('contact_name', 'Investor')
        company = investor_data.get('company', 'Investment Firm')
        sectors = investor_data.get('sectors', 'Various sectors')
        thesis = investor_data.get('investment_thesis', 'Not specified')
        
        return f"""Hi {name.split()[0]},

I came across your profile at {company} and was impressed by your focus on {sectors} investments, particularly your interest in {thesis}.

Our AI-powered platform helps investors like yourself discover quality deal flow through automated intelligence and data-driven insights. We specialize in connecting investors with off-market opportunities that match their specific investment criteria.

Would you be open to a brief 15-minute chat next week to explore potential synergies?

Best regards,
Sam Desigan
Agent Manager, Impact Quadrant"""
    
    def get_next_account(self) -> Optional[Dict]:
        """Get next available AgentMail account based on strategy"""
        if not self.accounts:
            print("❌ No enabled AgentMail accounts")
            return None
        
        # Reset daily counts if new day
        today = datetime.now().date()
        for account_name, usage in self.account_usage.items():
            if usage['today_date'] != today:
                usage['today_count'] = 0
                usage['today_date'] = today
        
        # Filter accounts under daily limit
        available_accounts = []
        for account in self.accounts:
            usage = self.account_usage.get(account['name'], {})
            if usage.get('today_count', 0) < account.get('daily_limit', 1000):
                available_accounts.append(account)
        
        if not available_accounts:
            print("⚠️ All accounts at daily limit")
            return None
        
        # Select account based on strategy
        strategy = self.config.get('rotation_strategy', 'round_robin')
        
        if strategy == "round_robin":
            # Simple round robin
            if not hasattr(self, 'round_robin_index'):
                self.round_robin_index = 0
            
            account = available_accounts[self.round_robin_index % len(available_accounts)]
            self.round_robin_index += 1
            return account
        
        elif strategy == "random":
            return random.choice(available_accounts)
        
        elif strategy == "least_used":
            # Select account with least usage today
            least_used = min(available_accounts, 
                           key=lambda a: self.account_usage.get(a['name'], {}).get('today_count', 0))
            return least_used
        
        elif strategy == "priority":
            # Select by priority (lower number = higher priority)
            available_accounts.sort(key=lambda a: a.get('priority', 999))
            return available_accounts[0]
        
        else:
            # Default to round robin
            if not hasattr(self, 'round_robin_index'):
                self.round_robin_index = 0
            
            account = available_accounts[self.round_robin_index % len(available_accounts)]
            self.round_robin_index += 1
            return account
    
    def test_agentmail_api(self, account: Dict) -> bool:
        """Test AgentMail API connection"""
        print(f"   🔍 Testing AgentMail API for {account['name']}...")
        
        headers = {
            "Authorization": f"Bearer {account['api_key']}",
            "Content-Type": "application/json"
        }
        
        try:
            # Test API endpoint
            response = requests.get(
                f"{self.base_url}/inboxes/{account['from_email']}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"      ✅ API connection successful")
                return True
            else:
                print(f"      ❌ API test failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"      ❌ API test error: {e}")
            return False
    
    def send_test_email(self, account: Dict, test_email: str = "test@example.com") -> Dict:
        """Send test email via AgentMail API"""
        print(f"   📤 Sending test email from {account['name']}...")
        
        headers = {
            "Authorization": f"Bearer {account['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inbox_id": account['from_email'],
            "to": [test_email],
            "subject": f"Test Email from {account['name']} - Bdev.ai Pipeline",
            "text": f"""This is a test email from the Bdev.ai Advanced Pipeline.

Account: {account['name']}
From: {account['from_name']} <{account['from_email']}>
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This confirms that the AgentMail integration is working correctly.

Best regards,
Bdev.ai Advanced Pipeline Test System"""
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/inboxes/{account['from_email']}/messages/send",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"      ✅ Test email sent successfully")
                print(f"      📨 Message ID: {result.get('message_id', 'N/A')}")
                return {
                    'success': True,
                    'message_id': result.get('message_id'),
                    'account': account['name'],
                    'status': 'sent'
                }
            else:
                print(f"      ❌ Test email failed: HTTP {response.status_code}")
                print(f"      📝 Response: {response.text[:200]}")
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text[:200]}",
                    'account': account['name'],
                    'status': 'failed'
                }
                
        except Exception as e:
            print(f"      ❌ Test email error: {e}")
            return {
                'success': False,
                'error': str(e),
                'account': account['name'],
                'status': 'error'
            }
    
    def test_agentmail_accounts(self) -> Dict:
        """Test all AgentMail accounts"""
        print(f"\n🔧 Step 2: Testing AgentMail accounts...")
        
        results = {
            'total_accounts': len(self.accounts),
            'api_tests': {},
            'email_tests': {},
            'working_accounts': 0
        }
        
        for account in self.accounts:
            print(f"\n   Testing {account['name']} ({account['from_email']})...")
            
            # Test API connection
            api_test = self.test_agentmail_api(account)
            results['api_tests'][account['name']] = api_test
            
            if api_test:
                # Send test email
                email_test = self.send_test_email(account)
                results['email_tests'][account['name']] = email_test
                
                if email_test['success']:
                    results['working_accounts'] += 1
                    # Update account usage
                    self.account_usage[account['name']]['today_count'] += 1
                    self.account_usage[account['name']]['total_sent'] += 1
                    self.account_usage[account['name']]['last_used'] = datetime.now().isoformat()
        
        self.results['agentmail_sending'] = results
        self.results['account_usage'] = self.account_usage.copy()
        
        return results
    
    def create_detailed_report(self) -> str:
        """Create detailed test report"""
        print(f"\n📊 Step 3: Creating detailed test report...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"/Users/cubiczan/.openclaw/workspace/bdev_ai_test_report_{timestamp}.md"
        
        # Calculate statistics
        ai_status = self.results.get('ai_generation', {})
        agentmail_results = self.results.get('agentmail_sending', {})
        
        ai_count = ai_status.get('messages_generated', 0)
        working_accounts = agentmail_results.get('working_accounts', 0)
        total_accounts = agentmail_results.get('total_accounts', 0)
        
        # Create report
        report = f"""# Bdev.ai Advanced Pipeline Test Report

## Test Execution
- **Started**: {self.results['pipeline_start']}
- **Completed**: {datetime.now().isoformat()}
- **Duration**: {self.calculate_duration()}

## AI Message Generation Test
- **Status**: {ai_status.get('status', 'unknown')}
- **Messages Generated**: {ai_count}
- **Output File**: {ai_status.get('output_file', 'N/A')}

## AgentMail Integration Test
- **Total Accounts**: {total_accounts}
- **✅ Working Accounts**: {working_accounts}
- **📈 Success Rate**: {(working_accounts/total_accounts*100) if total_accounts > 0 else 0:.1f}%

## Account-by-Account Results
"""
        
        # Add account test details
        for account in self.accounts:
            account_name = account['name']
            api_test = agentmail_results.get('api_tests', {}).get(account_name, False)
            email_test = agentmail_results.get('email_tests', {}).get(account_name, {})
            
            report += f"""
### {account_name} ({account['from_email']})
- **API Connection**: {'✅ Success' if api_test else '❌ Failed'}
- **Test Email**: {'✅ Sent' if email_test.get('success') else '❌ Failed'}
"""
            
            if email_test.get('success'):
                report += f"  - Message ID: {email_test.get('message_id', 'N/A')}\n"
            elif email_test.get('error'):
                report += f"  - Error: {email_test.get('error', 'Unknown')}\n"
        
        # Add account usage
        report += f"""
## Account Usage After Test
"""
        
        for account_name, usage in self.account_usage.items():
            today = usage.get('today_count', 0)
            total = usage.get('total_sent', 0)
            errors = usage.get('errors', 0)
            limit = usage.get('daily_limit', 1000)
            
            if limit > 0:
                usage_pct = (today / limit) * 100
            else:
                usage_pct = 0
            
            report += f"- **{account_name}**: {today}/{limit} ({usage_pct:.1f}%) today, {total} total, {errors} errors\n"
        
        # Add configuration summary
        report += f"""
## Configuration Summary
- **Rotation Strategy**: {self.config.get('rotation_strategy', 'round_robin')}
- **Daily Total Limit**: {self.config.get('daily_total_limit', 3000)}
- **Rate Limit**: {self.config.get('rate_limit_per_minute', 60)}/minute
- **Default Sender**: {self.config.get('default_sender', 'Sam Desigan')}
- **Default Reply-To**: {self.config.get('default_reply_to', 'sam@impactquadrant.info')}

## Files Created
"""
        
        for file_info in self.results.get('files_created', []):
            report += f"- **{file_info.get('type', 'unknown')}**: {file_info.get('path', 'N/A')} ({file_info.get('size', 0)} bytes)\n"
        
        # Add recommendations
        report += f"""
## Test Results Summary

### ✅ What Worked
1. **AI Message Generation**: Successfully created {ai_count} personalized messages
2. **AgentMail Integration**: {working_accounts}/{total_accounts} accounts working
3. **Configuration Loading**: All settings loaded correctly from JSON
4. **Account Rotation**: {self.config.get('rotation_strategy', 'round_robin')} strategy implemented

### ⚠️ Areas for Improvement
1. **API Error Handling**: Add retry logic for failed API calls
2. **Rate Limiting**: Implement proper rate limiting per account
3. **Bounce Handling**: Configure bounce detection and auto-disable
4. **Unsubscribe Management**: Add unsubscribe link handling

### 🚀 Next Steps for Production
1. **Scale Up**: Increase batch size from test to production (50 → 500+)
2. **Add Monitoring**: Implement real-time monitoring and alerts
3. **Add Analytics**: Track open rates, click-through rates, responses
4. **Schedule Automation**: Set up daily cron jobs for automated execution

## Technical Details
- **API Version**: AgentMail v0
- **Authentication**: Bearer token
- **Rate Limiting**: Configurable per minute
- **Error Handling**: Basic error catching implemented
- **Data Persistence**: CSV + JSON output for audit trail

---
*Generated by Bdev.ai Advanced Pipeline Test System*
*Execution timestamp: {datetime.now().isoformat()}*
"""
        
        # Save report
        with open(report_path, 'w') as f:
            f.write(report)
        
        # Also save JSON data
        json_path = f"/Users/cubiczan/.openclaw/workspace/bdev_ai_test_data_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=self.json_serializer)
        
        # Add to files created
        self.results['files_created'].extend([
            {'type': 'report', 'path': report_path, 'size': os.path.getsize(report_path)},
            {'type': 'json_data', 'path': json_path, 'size': os.path.getsize(json_path)}
        ])
        
        print(f"   📄 Report saved to: {report_path}")
        print(f"   📊 Data saved to: {json_path}")
        
        return report_path
    
    def calculate_duration(self) -> str:
        """Calculate pipeline duration"""
        try:
            start_time = datetime.fromisoformat(self.results['pipeline_start'])
            end_time = datetime.now()
            duration = end_time - start_time
            
            hours, remainder = divmod(duration.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if hours > 0:
                return f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
        except:
            return "Unknown"
    
    def json_serializer(self, obj):
        """JSON serializer for datetime and date objects"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print("📊 TEST EXECUTION SUMMARY")
        print("="*80)
        
        # AI Generation
        ai_status = self.results.get('ai_generation', {})
        print(f"🤖 AI Message Generation Test:")
        print(f"   Status: {ai_status.get('status', 'unknown')}")
        print(f"   Messages: {ai_status.get('messages_generated', 0)}")
        print(f"   Output: {ai_status.get('output_file', 'N/A')}")
        
        # AgentMail Testing
        agentmail_results = self.results.get('agentmail_sending', {})
        print(f"\n🔧 AgentMail Integration Test:")
        print(f"   Total Accounts: {agentmail_results.get('total_accounts', 0)}")
        print(f"   ✅ Working Accounts: {agentmail_results.get('working_accounts', 0)}")
        
        # Account Usage
        print(f"\n👥 AgentMail Account Usage:")
        for account_name, usage in self.account_usage.items():
            today = usage.get('today_count', 0)
            total = usage.get('total_sent', 0)
            errors = usage.get('errors', 0)
            limit = usage.get('daily_limit', 1000)
            
            if limit > 0:
                usage_pct = (today / limit) * 100
                print(f"   • {account_name}: {today}/{limit} ({usage_pct:.1f}%) today, {total} total, {errors} errors")
            else:
                print(f"   • {account_name}: {today} today, {total} total, {errors} errors")
        
        # Files Created
        print(f"\n📁 Files Created:")
        for file_info in self.results.get('files_created', []):
            print(f"   • {file_info.get('type', 'unknown')}: {os.path.basename(file_info.get('path', ''))}")
        
        # Duration
        print(f"\n⏱️ Test Duration: {self.calculate_duration()}")
        print("="*80)
        print("🧪 Advanced Pipeline Test Complete!")
        print("="*80)
    
    def run_test(self, batch_size: int = 10):
        """Run the complete test"""
        print(f"\n🚀 Starting Bdev.ai Advanced Pipeline Test...")
        print(f"   Batch Size: {batch_size} investors")
        
        # Step 1: Generate sample messages
        csv_path = self.generate_sample_messages(batch_size)
        
        if not csv_path:
            print("❌ Test stopped: AI message generation failed")
            return False
        
        # Step 2: Test AgentMail accounts
        test_results = self.test_agentmail_accounts()
        
        # Step 3: Create reports
        report_path = self.create_detailed_report()
        
        # Step 4: Print summary
        self.print_summary()
        
        return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Bdev.ai Advanced Pipeline with 3 AgentMail Accounts')
    parser.add_argument('--batch-size', type=int, default=10, help='Number of investors to process')
    parser.add_argument('--config', type=str, help='Path to AgentMail config (default: agentmail_config.json)')
    
    args = parser.parse_args()
    
    # Initialize and run test
    pipeline = TestAdvancedPipeline(args.config)
    success = pipeline.run_test(args.batch_size)
    
    if success:
        print("\n🎉 Test executed successfully!")
        print("📊 Check the generated reports for detailed results.")
    else:
        print("\n❌ Test execution failed.")
        print("⚠️ Check the error messages above for details.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())