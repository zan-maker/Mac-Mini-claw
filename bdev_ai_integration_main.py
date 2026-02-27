#!/usr/bin/env python3
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
        
        print(f"\nProcessing {len(investors)} investors...")
        
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
                    print("\n" + "="*60)
                    print("EXAMPLE GENERATED MESSAGE:")
                    print("="*60)
                    print(message)
                    print("="*60 + "\n")
                
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
            report += f"\n{i+1}. {row['contact_name']} ({row['company']})\n"
            report += f"   Sectors: {row['sectors'][:50]}...\n"
        
        report_path = f"{output_dir}/bdev_ai_report_{timestamp}.md"
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"\n✅ Results exported:")
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
        print("\nGenerating personalized outreach messages...")
        results = integrator.process_batch(batch_size=5)
        
        if len(results) > 0:
            # Export results
            csv_path, json_path, report_path = integrator.export_results(results)
            
            print(f"\n🎉 Successfully generated {len(results)} personalized messages!")
            print(f"\nNext steps:")
            print(f"1. Review messages in {csv_path}")
            print(f"2. Import into your email/LinkedIn outreach system")
            print(f"3. Schedule follow-up sequences")
            print(f"4. Track response rates and optimize")
        else:
            print("\n❌ No messages were generated. Check the errors above.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
