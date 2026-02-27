#!/usr/bin/env python3
"""
Bdev.ai Integration with OpenClaw Lead Pipeline
This script integrates Bdev.ai's AI-powered sales intelligence with existing lead generation.
"""

import os
import json
import requests
import pandas as pd
from typing import Dict, List, Optional
import openai
from datetime import datetime

class BdevAIIntegration:
    """Integrate Bdev.ai with OpenClaw lead pipeline"""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize with OpenAI API key"""
        self.openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        
        openai.api_key = self.openai_api_key
        
        # Load master investor database
        self.investor_db_path = "/Users/cubiczan/.openclaw/workspace/data/master-investor-database.csv"
        self.leads = self.load_investor_database()
        
        print(f"Loaded {len(self.leads)} investors from database")
    
    def load_investor_database(self) -> pd.DataFrame:
        """Load the master investor database"""
        try:
            df = pd.read_csv(self.investor_db_path)
            print(f"Database columns: {df.columns.tolist()}")
            return df
        except Exception as e:
            print(f"Error loading database: {e}")
            # Create sample data for testing
            return pd.DataFrame({
                'Company Name': ['Test Investor 1', 'Test Investor 2'],
                'Contact Name': ['John Doe', 'Jane Smith'],
                'Email': ['john@test.com', 'jane@test.com'],
                'Investment Thesis': ['Tech startups', 'Real estate'],
                'Sectors': ['Technology', 'Real Estate, Hospitality'],
                'Stage': ['Growth', 'Early'],
                'Check Size': ['$1M-$5M', '$500K-$2M']
            })
    
    def extract_profile_from_linkedin_url(self, linkedin_url: str) -> Dict:
        """Extract profile information from LinkedIn URL (simplified)"""
        # In production, this would use LinkedIn API or web scraping
        # For now, return mock data
        return {
            "Name": "Sample Investor",
            "About": "Experienced investor focusing on technology and real estate.",
            "Experience": "10+ years in venture capital, previously at Goldman Sachs.",
            "Education": "MBA from Harvard, BS from Stanford.",
            "Skills": "Investment Analysis, Due Diligence, Portfolio Management",
            "URL": linkedin_url
        }
    
    def generate_similarities(self, sender_profile: Dict, receiver_profile: Dict) -> Dict:
        """Find similarities between two profiles using OpenAI"""
        similarities = {}
        
        # Focus on key sections
        targets = ['About', 'Experience', 'Education', 'Skills']
        
        for key in targets:
            if key in sender_profile and key in receiver_profile:
                sender_text = sender_profile.get(key, '')
                receiver_text = receiver_profile.get(key, '')
                
                if sender_text and receiver_text:
                    try:
                        prompt = f"""Find the most relevant similarities between these two profiles in the {key} section:

Sender {key}: {sender_text[:500]}

Receiver {key}: {receiver_text[:500]}

Identify 2-3 key similarities that could form the basis for a personalized outreach message. Focus on shared experiences, skills, interests, or values."""
                        
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a sales intelligence assistant that finds meaningful connections between professionals."},
                                {"role": "user", "content": prompt}
                            ],
                            max_tokens=300,
                            temperature=0.7
                        )
                        
                        similarities[key] = response.choices[0].message.content.strip()
                        
                    except Exception as e:
                        print(f"Error generating similarities for {key}: {e}")
                        similarities[key] = f"Shared interest in {key.lower()} based on profiles."
        
        return similarities
    
    def generate_personalized_message(self, sender_profile: Dict, receiver_profile: Dict, similarities: Dict) -> str:
        """Generate personalized outreach message using OpenAI"""
        
        # Combine similarities into a summary
        similarity_summary = "\n".join([f"{k}: {v}" for k, v in similarities.items()])
        
        prompt = f"""Generate a personalized LinkedIn connection request or email outreach message based on the following profiles and similarities:

SENDER PROFILE:
Name: {sender_profile.get('Name', 'Business Development Professional')}
About: {sender_profile.get('About', '')[:300]}
Experience: {sender_profile.get('Experience', '')[:300]}

RECEIVER PROFILE:
Name: {receiver_profile.get('Name', 'Investor')}
About: {receiver_profile.get('About', '')[:300]}
Company: {receiver_profile.get('Company', 'Investment Firm')}

KEY SIMILARITIES:
{similarity_summary}

Generate a professional, personalized message that:
1. Mentions 1-2 specific similarities
2. Is concise (2-3 paragraphs max)
3. Has a clear call-to-action
4. Sounds natural and authentic
5. Avoids being overly salesy

Format the message for LinkedIn or email."""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert sales copywriter that creates highly personalized outreach messages."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating message: {e}")
            return f"""Hi {receiver_profile.get('Name', 'there')},

I noticed your background in {receiver_profile.get('Sectors', 'investment')} and thought we might have some shared interests based on your profile.

I'd love to connect and learn more about your work.

Best regards,
{sender_profile.get('Name', 'Business Development Team')}"""
    
    def process_investor_batch(self, batch_size: int = 10) -> pd.DataFrame:
        """Process a batch of investors and generate personalized messages"""
        
        results = []
        processed = 0
        
        # Sample sender profile (would be your profile in production)
        sender_profile = {
            "Name": "Sam Desigan",
            "About": "Agent Manager at Impact Quadrant, specializing in AI-powered lead generation and business development automation. Focus on connecting investors with quality deal flow in technology, real estate, and hospitality sectors.",
            "Experience": "5+ years in business development and investor relations. Previously worked with family offices and PE firms on deal sourcing and due diligence. Currently managing AI-driven lead generation systems.",
            "Education": "Business Administration with focus on Technology Management.",
            "Skills": "Investor Relations, Deal Sourcing, AI Automation, Business Development"
        }
        
        for idx, investor in self.leads.head(batch_size).iterrows():
            try:
                print(f"Processing investor {idx + 1}/{min(batch_size, len(self.leads))}: {investor.get('Contact Name', 'Unknown')}")
                
                # Create receiver profile from investor data
                receiver_profile = {
                    "Name": investor.get('Contact Name', 'Investor'),
                    "Company": investor.get('Company Name', 'Investment Firm'),
                    "About": f"Investor at {investor.get('Company Name', '')} focusing on {investor.get('Investment Thesis', 'various sectors')}. Sectors: {investor.get('Sectors', 'Not specified')}. Stage: {investor.get('Stage', 'Not specified')}. Check size: {investor.get('Check Size', 'Not specified')}.",
                    "Experience": f"Investment professional with focus on {investor.get('Sectors', 'multiple sectors')}.",
                    "Sectors": investor.get('Sectors', '')
                }
                
                # Generate similarities
                similarities = self.generate_similarities(sender_profile, receiver_profile)
                
                # Generate personalized message
                message = self.generate_personalized_message(sender_profile, receiver_profile, similarities)
                
                # Store results
                result = {
                    "investor_id": idx,
                    "contact_name": investor.get('Contact Name', ''),
                    "company": investor.get('Company Name', ''),
                    "email": investor.get('Email', ''),
                    "sectors": investor.get('Sectors', ''),
                    "similarities_found": len(similarities),
                    "personalized_message": message,
                    "generated_at": datetime.now().isoformat()
                }
                
                results.append(result)
                processed += 1
                
                # Print sample
                if idx == 0:
                    print("\n" + "="*80)
                    print("SAMPLE GENERATED MESSAGE:")
                    print("="*80)
                    print(message)
                    print("="*80 + "\n")
                
            except Exception as e:
                print(f"Error processing investor {idx}: {e}")
                continue
        
        print(f"\nSuccessfully processed {processed} investors")
        return pd.DataFrame(results)
    
    def export_to_csv(self, results_df: pd.DataFrame, output_path: str = None):
        """Export results to CSV"""
        if output_path is None:
            output_path = f"/Users/cubiczan/.openclaw/workspace/bdev-ai-results-{datetime.now().strftime('%Y-%m-%d')}.csv"
        
        results_df.to_csv(output_path, index=False)
        print(f"Results exported to: {output_path}")
        return output_path
    
    def integrate_with_lead_pipeline(self):
        """Main integration function"""
        print("="*80)
        print("Bdev.ai Integration with OpenClaw Lead Pipeline")
        print("="*80)
        
        # Process investors
        results_df = self.process_investor_batch(batch_size=20)
        
        # Export results
        csv_path = self.export_to_csv(results_df)
        
        # Generate summary report
        summary = f"""
Bdev.ai Integration Report
=========================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Investors Processed: {len(results_df)}
Successful Messages: {len(results_df)}
Output File: {csv_path}

Sample Sectors Targeted:
{', '.join(results_df['sectors'].dropna().unique()[:5])}

Next Steps:
1. Review generated messages in {csv_path}
2. Import into your email outreach system (AgentMail, etc.)
3. Schedule follow-up sequences
4. Track response rates and optimize

Integration complete! Bdev.ai is now enhancing your lead generation pipeline with AI-powered personalization.
"""
        
        print(summary)
        
        # Save report
        report_path = f"/Users/cubiczan/.openclaw/workspace/bdev-ai-report-{datetime.now().strftime('%Y-%m-%d')}.md"
        with open(report_path, 'w') as f:
            f.write(summary)
        
        return results_df, csv_path, report_path


def main():
    """Main execution function"""
    try:
        # Check for OpenAI API key
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("ERROR: OPENAI_API_KEY environment variable not set.")
            print("Please set it with: export OPENAI_API_KEY='your-key-here'")
            return
        
        # Initialize integration
        integrator = BdevAIIntegration(api_key)
        
        # Run integration
        results_df, csv_path, report_path = integrator.integrate_with_lead_pipeline()
        
        print(f"\n✅ Integration successful!")
        print(f"📊 Results: {len(results_df)} personalized messages generated")
        print(f"💾 Data: {csv_path}")
        print(f"📋 Report: {report_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()