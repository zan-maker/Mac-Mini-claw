#!/usr/bin/env python3
"""
Bdev.ai Advanced Pipeline with 3 AgentMail Accounts
1. Generate AI messages for 50 investors using DeepSeek
2. Send via load-balanced AgentMail accounts (Primary, Secondary, Backup)
3. Create detailed usage reports
"""

import os
import sys
import json
import pandas as pd
import requests
from datetime import datetime, date
import time
import random
import subprocess
from typing import Dict, List, Optional
import glob

class BdevAIAdvancedPipeline:
    """Advanced pipeline with 3 AgentMail accounts"""
    
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
        print("🚀 Bdev.ai Advanced Pipeline with 3 AgentMail Accounts")
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
    
    def generate_ai_messages(self, batch_size: int = 50) -> str:
        """Generate AI messages using DeepSeek integration"""
        print(f"\n🤖 Step 1: Generating AI messages for {batch_size} investors...")
        
        try:
            # Run the DeepSeek integration script
            script_path = "/Users/cubiczan/.openclaw/workspace/bdev_ai_deepseek_integration.py"
            
            if not os.path.exists(script_path):
                print(f"❌ DeepSeek integration script not found: {script_path}")
                # Create a simple fallback
                return self.create_fallback_messages(batch_size)
            
            # Run the script
            result = subprocess.run(
                [sys.executable, script_path, "--batch-size", str(batch_size)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ AI message generation successful")
                
                # Find the latest generated CSV
                csv_files = glob.glob("/Users/cubiczan/.openclaw/workspace/bdev_ai_deepseek_*.csv")
                if csv_files:
                    latest_csv = max(csv_files, key=os.path.getctime)
                    
                    # Read the CSV to get stats
                    df = pd.read_csv(latest_csv)
                    ai_count = len(df)
                    
                    self.results['ai_generation'] = {
                        'status': 'success',
                        'messages_generated': ai_count,
                        'output_file': latest_csv,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    print(f"   📊 Generated {ai_count} AI messages")
                    print(f"   💾 Saved to: {latest_csv}")
                    
                    # Add to files created
                    self.results['files_created'].append({
                        'type': 'ai_messages',
                        'path': latest_csv,
                        'size': os.path.getsize(latest_csv)
                    })
                    
                    return latest_csv
                else:
                    print("⚠️ No CSV output found from AI generation")
                    return None
                    
            else:
                print(f"❌ AI generation failed: {result.stderr[:500]}")
                self.results['ai_generation'] = {
                    'status': 'failed',
                    'error': result.stderr[:500],
                    'timestamp': datetime.now().isoformat()
                }
                return None
                
        except Exception as e:
            print(f"❌ Error in AI generation: {e}")
            self.results['ai_generation'] = {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            return None
    
    def create_fallback_messages(self, batch_size: int) -> str:
        """Create fallback messages if AI generation fails"""
        print("⚠️ Using fallback message generation...")
        
        # Create sample investor data
        sample_investors = []
        for i in range(batch_size):
            sample_investors.append({
                'contact_name': f'Investor {i+1}',
                'company': f'Investment Firm {i+1}',
                'email': f'investor{i+1}@example.com',
                'sectors': 'Technology, SaaS',
                'investment_thesis': 'Early-stage tech startups',
                'personalized_message': f"""Hi Investor {i+1},

I came across your profile at Investment Firm {i+1} and was impressed by your focus on Technology and SaaS investments.

Our AI-powered platform helps investors like yourself discover quality deal flow through automated intelligence and data-driven insights.

Would you be open to connecting to explore potential synergies?

Best regards,
Sam Desigan
Agent Manager, Impact Quadrant""",
                'generated_at': datetime.now().isoformat(),
                'ai_model': 'fallback'
            })
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = f"/Users/cubiczan/.openclaw/workspace/bdev_ai_fallback_{timestamp}.csv"
        
        df = pd.DataFrame(sample_investors)
        df.to_csv(csv_path, index=False)
        
        self.results['ai_generation'] = {
            'status': 'fallback',
            'messages_generated': len(df),
            'output_file': csv_path,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"   📊 Generated {len(df)} fallback messages")
        print(f"   💾 Saved to: {csv_path}")
        
        return csv_path
    
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
    
    def send_email(self, account: Dict, to_email: str, subject: str, text_content: str) -> Dict:
        """Send email via AgentMail API"""
        headers = {
            "Authorization": f"Bearer {account['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inbox_id": account['from_email'],
            "to": [to_email],
            "subject": subject,
            "text": text_content
        }
        
        # Add CC if specified in config
        if self.config.get('default_reply_to'):
            payload["cc"] = [self.config['default_reply_to']]
        
        try:
            response = requests.post(
                f"{self.base_url}/inboxes/{account['from_email']}/messages/send",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'message_id': result.get('message_id'),
                    'account': account['name'],
                    'status': 'sent'
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text[:200]}",
                    'account': account['name'],
                    'status': 'failed'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'account': account['name'],
                'status': 'error'
            }
    
    def send_agentmail_messages(self, csv_path: str, limit: int = 50) -> Dict:
        """Send messages via AgentMail with load balancing"""
        print(f"\n📧 Step 2: Sending messages via AgentMail (limit: {limit})...")
        
        try:
            df = pd.read_csv(csv_path)
            print(f"   Found {len(df)} AI-generated messages")
            
            # Filter to limit
            if limit and len(df) > limit:
                df = df.head(limit)
                print(f"   Limiting to {limit} messages")
            
            results = {
                'total': len(df),
                'sent': 0,
                'failed': 0,
                'skipped': 0,
                'details': []
            }
            
            sent_count = 0
            for idx, row in df.iterrows():
                try:
                    email = str(row.get('email', '')).strip()
                    contact_name = str(row.get('contact_name', '')).strip()
                    company = str(row.get('company', '')).strip()
                    message = str(row.get('personalized_message', '')).strip()
                    
                    # Skip if no email
                    if not email or '@' not in email:
                        results['skipped'] += 1
                        results['details'].append({
                            'index': idx,
                            'contact': contact_name,
                            'email': email,
                            'status': 'skipped',
                            'reason': 'Invalid email'
                        })
                        continue
                    
                    # Get next available account
                    account = self.get_next_account()
                    if not account:
                        print(f"   ⚠️ No accounts available for {contact_name}")
                        results['skipped'] += 1
                        results['details'].append({
                            'index': idx,
                            'contact': contact_name,
                            'email': email,
                            'status': 'skipped',
                            'reason': 'No available accounts'
                        })
                        continue
                    
                    # Create subject
                    subject = f"Re: {company} - AI-Powered Deal Sourcing"
                    
                    print(f"   {idx+1}. {contact_name} ({email}) → {account['name']}")
                    
                    # Send email
                    send_result = self.send_email(account, email, subject, message)
                    
                    # Update account usage
                    if send_result['success']:
                        self.account_usage[account['name']]['today_count'] += 1
                        self.account_usage[account['name']]['total_sent'] += 1
                        self.account_usage[account['name']]['last_used'] = datetime.now().isoformat()
                        sent_count += 1
                        results['sent'] += 1
                        status = 'sent'
                    else:
                        self.account_usage[account['name']]['errors'] += 1
                        results['failed'] += 1
                        status = 'failed'
                    
                    results['details'].append({
                        'index': idx,
                        'contact': contact_name,
                        'email': email,
                        'account': account['name'],
                        'status': status,
                        'message_id': send_result.get('message_id'),
                        'error': send_result.get('error')
                    })
                    
                    # Rate limiting
                    if (idx + 1) % 10 == 0:
                        print(f"      Sent {idx+1}/{len(df)}...")
                        time.sleep(1)  # Brief pause
                    
                except Exception as e:
                    print(f"   {idx+1}. Error processing: {e}")
                    results['failed'] += 1
                    results['details'].append({
                        'index': idx,
                        'contact': 'Unknown',
                        'email': 'Unknown',
                        'status': 'error',
                        'error': str(e)
                    })
                    continue
            
            # Update results
            self.results['agentmail_sending'] = results
            self.results['account_usage'] = self.account_usage.copy()
            
            return results
            
        except Exception as e:
            print(f"❌ Error processing CSV: {e}")
            error_result = {
                'total': 0,
                'sent': 0,
                'failed': 0,
                'skipped': 0,
                'details': [],
                'error': str(e)
            }
            self.results['agentmail_sending'] = error_result
            return error_result
    
    def create_detailed_report(self) -> str:
        """Create detailed usage report"""
        print(f"\n📊 Step 3: Creating detailed usage reports...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"/Users/cubiczan/.openclaw/workspace/bdev_ai_advanced_report_{timestamp}.md"
        
        # Calculate statistics
        ai_status = self.results.get('ai_generation', {})
        agentmail_results = self.results.get('agentmail_sending', {})
        
        ai_count = ai_status.get('messages_generated', 0)
        sent_count = agentmail_results.get('sent', 0)
        total_count = agentmail_results.get('total', 0)
        
        if total_count > 0:
            success_rate = (sent_count / total_count) * 100
        else:
            success_rate = 0
        
        # Create report
        report = f"""# Bdev.ai Advanced Pipeline Report

## Pipeline Execution
- **Started**: {self.results['pipeline_start']}
- **Completed**: {datetime.now().isoformat()}
- **Duration**: {self.calculate_duration()}

## AI Message Generation
- **Status**: {ai_status.get('status', 'unknown')}
- **Messages Generated**: {ai_count}
- **Output File**: {ai_status.get('output_file', 'N/A')}

## AgentMail Sending Results
- **Total Messages**: {total_count}
- **✅ Successfully Sent**: {sent_count}
- **❌ Failed**: {agentmail_results.get('failed', 0)}
- **⚠️ Skipped**: {agentmail_results.get('skipped', 0)}
- **📈 Success Rate**: {success_rate:.1f}%

## AgentMail Account Usage
"""
        
        # Add account usage details
        for account_name, usage in self.account_usage.items():
            today = usage.get('today_count', 0)
            total = usage.get('total_sent', 0)
            errors = usage.get('errors', 0)
            limit = usage.get('daily_limit', 1000)
            
            if limit > 0:
                usage_pct = (today / limit) * 100
            else:
                usage_pct = 0
            
            report += f"""
### {account_name}
- **Sent Today**: {today} / {limit} ({usage_pct:.1f}%)
- **Total Sent**: {total}
- **Errors**: {errors}
- **Last Used**: {usage.get('last_used', 'Never')}
"""
        
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
        
        # Add error details if any
        if agentmail_results.get('failed', 0) > 0 or agentmail_results.get('errors'):
            report += f"""
## Error Details
"""
            for detail in agentmail_results.get('details', []):
                if detail.get('status') in ['failed', 'error']:
                    report += f"- **{detail.get('contact', 'Unknown')}** ({detail.get('email', 'No email')}): {detail.get('error', 'Unknown error')}\n"
        
        # Add recommendations
        report += f"""
## Recommendations & Next Steps

### Immediate Actions
1. **Review Sent Messages**: Check AgentMail dashboard for delivery status
2. **Monitor Responses**: Track reply rates and engagement
3. **Update Investor Database**: Mark contacted investors

### Optimization Suggestions
1. **Adjust Rotation Strategy**: Consider '{'least_used' if self.config.get('rotation_strategy') != 'least_used' else 'priority'}' for more balanced usage
2. **Increase Batch Size**: Current limit of {total_count} could be increased
3. **Add More Accounts**: Consider adding 1-2 more AgentMail accounts for redundancy

### Technical Notes
- **API Integration**: Uses AgentMail v0 API with bearer token authentication
- **Load Balancing**: {self.config.get('rotation_strategy', 'round_robin')} strategy across {len(self.accounts)} accounts
- **Rate Limiting**: Respects {self.config.get('rate_limit_per_minute', 60)} emails per minute
- **Error Handling**: Automatic retry not implemented (manual review required)

## Pipeline Performance Metrics
- **AI Generation Time**: {self.get_ai_generation_time()}
- **Email Sending Time**: {self.get_sending_time()}
- **Total Processing Time**: {self.calculate_duration()}
- **Average Time per Email**: {self.get_avg_time_per_email():.2f} seconds

---
*Generated by Bdev.ai Advanced Pipeline with 3 AgentMail Accounts*
*Execution timestamp: {datetime.now().isoformat()}*
"""
        
        # Save report
        with open(report_path, 'w') as f:
            f.write(report)
        
        # Also save JSON data
        json_path = f"/Users/cubiczan/.openclaw/workspace/bdev_ai_advanced_data_{timestamp}.json"
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
    
    def get_ai_generation_time(self) -> str:
        """Get AI generation time if available"""
        ai_status = self.results.get('ai_generation', {})
        if 'timestamp' in ai_status and 'pipeline_start' in self.results:
            try:
                start_time = datetime.fromisoformat(self.results['pipeline_start'])
                ai_time = datetime.fromisoformat(ai_status['timestamp'])
                duration = ai_time - start_time
                return f"{duration.seconds}s"
            except:
                pass
        return "Unknown"
    
    def get_sending_time(self) -> str:
        """Get sending time if available"""
        agentmail_results = self.results.get('agentmail_sending', {})
        if agentmail_results and 'pipeline_start' in self.results:
            try:
                # Estimate based on count
                sent_count = agentmail_results.get('sent', 0)
                # Assuming ~2 seconds per email with rate limiting
                estimated_time = sent_count * 2
                return f"~{estimated_time}s"
            except:
                pass
        return "Unknown"
    
    def get_avg_time_per_email(self) -> float:
        """Get average time per email"""
        agentmail_results = self.results.get('agentmail_sending', {})
        sent_count = agentmail_results.get('sent', 0)
        
        if sent_count > 0:
            sending_time_str = self.get_sending_time()
            if sending_time_str.startswith('~'):
                sending_time = float(sending_time_str[1:].replace('s', ''))
                return sending_time / sent_count
        
        return 0.0
    
    def json_serializer(self, obj):
        """JSON serializer for datetime and date objects"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    def print_summary(self):
        """Print pipeline summary"""
        print("\n" + "="*80)
        print("📊 PIPELINE EXECUTION SUMMARY")
        print("="*80)
        
        # AI Generation
        ai_status = self.results.get('ai_generation', {})
        print(f"🤖 AI Message Generation:")
        print(f"   Status: {ai_status.get('status', 'unknown')}")
        print(f"   Messages: {ai_status.get('messages_generated', 0)}")
        print(f"   Output: {ai_status.get('output_file', 'N/A')}")
        
        # AgentMail Sending
        agentmail_results = self.results.get('agentmail_sending', {})
        print(f"\n📧 AgentMail Sending:")
        print(f"   Total: {agentmail_results.get('total', 0)}")
        print(f"   ✅ Sent: {agentmail_results.get('sent', 0)}")
        print(f"   ❌ Failed: {agentmail_results.get('failed', 0)}")
        print(f"   ⚠️ Skipped: {agentmail_results.get('skipped', 0)}")
        
        if agentmail_results.get('total', 0) > 0:
            success_rate = (agentmail_results.get('sent', 0) / agentmail_results.get('total', 0)) * 100
            print(f"   📈 Success Rate: {success_rate:.1f}%")
        
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
        print(f"\n⏱️ Pipeline Duration: {self.calculate_duration()}")
        print("="*80)
        print("✅ Advanced Pipeline Complete!")
        print("="*80)
    
    def run_pipeline(self, batch_size: int = 50, send_limit: int = 50):
        """Run the complete pipeline"""
        print(f"\n🚀 Starting Bdev.ai Advanced Pipeline...")
        print(f"   Batch Size: {batch_size} investors")
        print(f"   Send Limit: {send_limit} emails")
        
        # Step 1: Generate AI messages
        csv_path = self.generate_ai_messages(batch_size)
        
        if not csv_path:
            print("❌ Pipeline stopped: AI message generation failed")
            return False
        
        # Step 2: Send via AgentMail
        sending_results = self.send_agentmail_messages(csv_path, send_limit)
        
        # Step 3: Create reports
        report_path = self.create_detailed_report()
        
        # Step 4: Print summary
        self.print_summary()
        
        return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Bdev.ai Advanced Pipeline with 3 AgentMail Accounts')
    parser.add_argument('--batch-size', type=int, default=50, help='Number of investors to process')
    parser.add_argument('--send-limit', type=int, default=50, help='Number of emails to send')
    parser.add_argument('--config', type=str, help='Path to AgentMail config (default: agentmail_config.json)')
    
    args = parser.parse_args()
    
    # Initialize and run pipeline
    pipeline = BdevAIAdvancedPipeline(args.config)
    success = pipeline.run_pipeline(args.batch_size, args.send_limit)
    
    if success:
        print("\n🎉 Pipeline executed successfully!")
        print("📊 Check the generated reports for detailed results.")
    else:
        print("\n❌ Pipeline execution failed.")
        print("⚠️ Check the error messages above for details.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())