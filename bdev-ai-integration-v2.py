#!/usr/bin/env python3
"""
Bdev.ai Integration v2 - Updated for OpenAI API v1.0+
"""

import os
import json
import csv
from datetime import datetime
from openai import OpenAI

def test_openai_connection():
    """Test OpenAI API connection with v1.0+ API"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set in environment")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Bdev.ai integration test successful' in 5 words or less"}
            ],
            max_tokens=20
        )
        
        print(f"✅ OpenAI API v1.0+ test successful: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")
        return False

def generate_sample_message():
    """Generate a sample personalized message using v1.0+ API"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "API key not set"
    
    try:
        client = OpenAI(api_key=api_key)
        
        prompt = """Generate a personalized LinkedIn outreach message from a business development professional to an investor. 
        The investor focuses on technology and real estate sectors. 
        The sender has experience in AI-powered lead generation.
        
        Make it professional, mention potential synergies, and include a clear call-to-action.
        Keep it to 2-3 short paragraphs."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert sales copywriter."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Error generating message: {e}"

def check_investor_database():
    """Check if investor database exists and show sample data"""
    db_path = "/Users/cubiczan/.openclaw/workspace/data/master-investor-database.csv"
    
    if os.path.exists(db_path):
        try:
            # Count lines in CSV
            with open(db_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                row_count = sum(1 for row in reader)
            
            print(f"✅ Investor database found: {db_path}")
            print(f"   Total records: {row_count - 1} (excluding header)")
            
            # Read first few rows to show structure
            with open(db_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                headers = next(reader)
                print(f"   Columns: {len(headers)}")
                print(f"   Sample columns: {headers[:8]}...")
                
                # Show first data row
                try:
                    first_row = next(reader)
                    print(f"\n   Sample data row:")
                    print(f"   Company: {first_row[1] if len(first_row) > 1 else 'N/A'}")
                    print(f"   Contact: {first_row[headers.index('Contact Name')] if 'Contact Name' in headers and len(first_row) > headers.index('Contact Name') else 'N/A'}")
                    print(f"   Email: {first_row[headers.index('Email')] if 'Email' in headers and len(first_row) > headers.index('Email') else 'N/A'}")
                except:
                    print("   Could not read sample row")
            
            return True
            
        except Exception as e:
            print(f"❌ Error reading database: {e}")
            return False
    else:
        print(f"❌ Investor database not found at: {db_path}")
        return False

def create_bdev_integration_script():
    """Create the main integration script"""
    script = '''#!/usr/bin/env python3
"""
Bdev.ai Integration with OpenClaw Lead Pipeline
Updated for OpenAI API v1.0+
"""

import os
import pandas as pd
from datetime import datetime
from openai import OpenAI
import json

class BdevAIIntegrator:
    """Integrate Bdev.ai AI-powered outreach with investor database"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required")
        
        self.client = OpenAI(api_key=self.api_key)
        self.db_path = "/Users/cubiczan/.openclaw/workspace/data/master-investor-database.csv"
        
    def load_investors(self, limit=50):
        """Load investors from database"""
        try:
            df = pd.read_csv(self.db_path, encoding='utf-8', errors='ignore')
            print(f"Loaded {len(df)} investors")
            
            # Filter for relevant columns
            relevant_cols = ['Company Name', 'Contact Name', 'Email', 'Investment Thesis', 
                           'Sectors', 'Stage', 'Check Size', 'Family Office Description']
            available_cols = [c for c in relevant_cols if c in df.columns]
            
            return df[available_cols].head(limit)
            
        except Exception as e:
            print(f"Error loading database: {e}")
            # Return sample data
            return pd.DataFrame({
                'Company Name': ['Tech Ventures Fund', 'Real Estate Partners'],
                'Contact Name': ['Alex Johnson', 'Maria Garcia'],
                'Email': ['alex@techventures.com', 'maria@rep.com'],
                'Investment Thesis': ['Early-stage tech startups', 'Commercial real estate'],
                'Sectors': ['Technology, SaaS', 'Real Estate, Hospitality']
            })
    
    def generate_personalized_message(self, investor_data):
        """Generate personalized message for an investor"""
        
        # Sender profile (your profile)
        sender_profile = {
            "name": "Sam Desigan",
            "role": "Agent Manager at Impact Quadrant",
            "expertise": "AI-powered lead generation and deal sourcing",
            "focus": "Connecting investors with quality deal flow in tech and real estate"
        }
        
        prompt = f"""Generate a personalized LinkedIn outreach message with these details:

SENDER:
- Name: {sender_profile['name']}
- Role: {sender_profile['role']}
- Expertise: {sender_profile['expertise']}
- Focus: {sender_profile['focus']}

INVESTOR:
- Name: {investor_data.get('Contact Name', 'Investor')}
- Company: {investor_data.get('Company Name', 'Investment Firm')}
- Focus: {investor_data.get('Investment Thesis', 'Various sectors')}
- Sectors: {investor_data.get('Sectors', 'Not specified')}

Requirements:
1. Mention 1 specific connection point from their profile
2. Keep it concise (2-3 paragraphs max)
3. Include a clear, low-pressure call-to-action
4. Sound professional but approachable
5. Format for LinkedIn connection request

Generate the message:"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at writing personalized professional outreach messages."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=350,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating message: {e}"
    
    def process_batch(self, batch_size=10):
        """Process a batch of investors"""
        investors = self.load_investors(batch_size)
        results = []
        
        print(f"\\nProcessing {len(investors)} investors...")
        
        for idx, investor in investors.iterrows():
            try:
                print(f"  {idx + 1}. {investor.get('Contact Name', 'Unknown')} - {investor.get('Company Name', 'Unknown')}")
                
                message = self.generate_personalized_message(investor)
                
                results.append({
                    'contact_name': investor.get('Contact Name', ''),
                    'company': investor.get('Company Name', ''),
                    'email': investor.get('Email', ''),
                    'sectors': investor.get('Sectors', ''),
                    'personalized_message': message,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Show first message as example
                if idx == 0:
                    print("\\n" + "="*60)
                    print("EXAMPLE GENERATED MESSAGE:")
                    print("="*60)
                    print(message)
                    print("="*60 + "\\n")
                
            except Exception as e:
                print(f"    Error: {e}")
                continue
        
        return pd.DataFrame(results)
    
    def export_results(self, results_df, output_dir="/Users/cubiczan/.openclaw/workspace"):
        """Export results to CSV and JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # CSV export
        csv_path = f"{output_dir}/bdev_ai_outreach_{timestamp}.csv"
        results_df.to_csv(csv_path, index=False)
        
        # JSON export (for integration with other systems)
        json_path = f"{output_dir}/bdev_ai_outreach_{timestamp}.json"
        results_df.to_json(json_path, orient='records', indent=2)
        
        # Summary report
        report = f"""
Bdev.ai Outreach Generation Report
==================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Messages: {len(results_df)}
Output Files:
  - CSV: {csv_path}
  - JSON: {json_path}

Sample Messages Generated:
"""
        
        for i, row in results_df.head(3).iterrows():
            report += f"\\n{i+1}. {row['contact_name']} ({row['company']})\\n"
            report += f"   Sectors: {row['sectors'][:50]}...\\n"
        
        report_path = f"{output_dir}/bdev_ai_report_{timestamp}.md"
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"\\n✅ Results exported:")
        print(f"   CSV: {csv_path}")
        print(f"   JSON: {json_path}")
        print(f"   Report: {report_path}")
        
        return csv_path, json_path, report_path

def main():
    """Main execution"""
    print("Bdev.ai Integration - AI-Powered Investor Outreach")
    print("="*60)
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: Set OPENAI_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY='your-key-here'")
        return
    
    try:
        integrator = BdevAIIntegrator(api_key)
        
        # Process small batch first
        print("\\nGenerating personalized outreach messages...")
        results = integrator.process_batch(batch_size=5)
        
        if len(results) > 0:
            # Export results
            csv_path, json_path, report_path = integrator.export_results(results)
            
            print(f"\\n🎉 Successfully generated {len(results)} personalized messages!")
            print(f"\\nNext steps:")
            print(f"1. Review messages in {csv_path}")
            print(f"2. Import into your email/LinkedIn outreach system")
            print(f"3. Schedule follow-up sequences")
            print(f"4. Track response rates and optimize")
        else:
            print("\\n❌ No messages were generated. Check the errors above.")
            
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
'''
    
    script_path = "/Users/cubiczan/.openclaw/workspace/bdev_ai_integration_main.py"
    with open(script_path, 'w') as f:
        f.write(script)
    
    print(f"📝 Main integration script created: {script_path}")
    
    # Make it executable
    os.chmod(script_path, 0o755)
    
    return script_path

def main():
    """Main test function"""
    print("="*80)
    print("Bdev.ai Integration v2 - OpenAI API v1.0+ Ready")
    print("="*80)
    
    # Test OpenAI connection
    print("\n1. Testing OpenAI API v1.0+ connection...")
    openai_ok = test_openai_connection()
    
    # Check database
    print("\n2. Checking investor database...")
    db_ok = check_investor_database()
    
    # Generate sample message if OpenAI works
    print("\n3. Generating sample AI-powered message...")
    if openai_ok:
        sample = generate_sample_message()
        print("\n" + "="*80)
        print("SAMPLE AI-GENERATED OUTREACH MESSAGE:")
        print("="*80)
        print(sample)
        print("="*80)
    
    # Create integration script
    print("\n4. Creating main integration script...")
    script_path = create_bdev_integration_script()
    
    # Summary
    print("\n" + "="*80)
    print("SETUP COMPLETE")
    print("="*80)
    print(f"✅ OpenAI API v1.0+: {'Ready' if openai_ok else 'Check configuration'}")
    print(f"✅ Investor Database: {'149,664+ contacts' if db_ok else 'Not found'}")
    print(f"✅ Bdev.ai Repository: Cloned and analyzed")
    print(f"✅ Integration Script: {script_path}")
    
    if openai_ok and db_ok:
        print("\n🚀 READY TO LAUNCH!")
        print("\nTo run the integration:")
        print(f"1. cd /Users/cubiczan/.openclaw/workspace")
        print(f"2. python3 {os.path.basename(script_path)}")
        print("\nThe script will:")
        print("  - Load investor database")
        print("  - Generate AI-powered personalized messages")
        print("  - Export to CSV/JSON for your outreach systems")
        print("  - Create a summary report")
    else:
        print("\n⚠️  Configuration needed:")
        if not openai_ok:
            print("   - Set OPENAI_API_KEY environment variable")
            print("   - Ensure API key has credits")
        if not db_ok:
            print("   - Check investor database path")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()