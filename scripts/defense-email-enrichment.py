#!/usr/bin/env python3
"""
Defense Sector Email Enrichment & Outreach
Using new Hunter.io API key
"""

import sys
import json
import time
from datetime import datetime
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace')

from hunter_io_config import hunter_client

# Defense companies from today's report
DEFENSE_COMPANIES = [
    {"name": "Helsing", "domain": "helsing.ai", "sector": "AI & Battlefield Software", "score": 92, "location": "Germany"},
    {"name": "Quantum Systems", "domain": "quantum-systems.com", "sector": "Autonomous ISR Drones", "score": 88, "location": "Germany"},
    {"name": "Comand AI", "domain": "comand.ai", "sector": "AI-Powered Targeting Systems", "score": 85, "location": "France"},
    {"name": "BforeAI", "domain": "bfore.ai", "sector": "Cyber Threat Intelligence", "score": 82, "location": "France/Global"},
    {"name": "VIZGARD", "domain": "vizgard.com", "sector": "AI-Powered Optical Security", "score": 80, "location": "UK"},
    {"name": "RobCo", "domain": "rob.co", "sector": "AI-Powered Industrial Robotics", "score": 75, "location": "Germany"},
    {"name": "XRF.ai", "domain": "xrf.ai", "sector": "Advanced Radar & Signal Processing", "score": 72, "location": "Europe"},
    {"name": "Perciv AI", "domain": "perciv.ai", "sector": "Radar Perception Systems", "score": 70, "location": "Europe"},
    {"name": "Drone Defense", "domain": "dronedefense.co.uk", "sector": "Counter-Drone / Airspace Security", "score": 68, "location": "UK"},
    {"name": "Novadem", "domain": "novadem.com", "sector": "Tactical Drones", "score": 65, "location": "France"},
]

# PE/VC Funds
PE_VC_FUNDS = [
    {"name": "MASNA Ventures", "domain": "masna.vc", "sector": "Defense-focused VC", "score": 95, "location": "Saudi Arabia"},
    {"name": "Raphe mPhibr Investors", "domain": "raphe.co.in", "sector": "Drone manufacturing, defense systems", "score": 88, "location": "India"},
    {"name": "iDEX Ecosystem Investors", "domain": "idex.gov.in", "sector": "Government-backed defense innovation", "score": 85, "location": "India"},
    {"name": "General Atlantic", "domain": "generalatlantic.com", "sector": "Technology, defense tech", "score": 82, "location": "Global/Middle East"},
    {"name": "Blackstone", "domain": "blackstone.com", "sector": "Technology, infrastructure", "score": 80, "location": "Global/Middle East"},
]

def find_emails_for_company(company):
    """Find emails for a company using Hunter.io"""
    print(f"\n🔍 Searching emails for: {company['name']} ({company['domain']})")
    
    try:
        # Domain search
        result = hunter_client.domain_search(company['domain'], limit=10)
        
        if result.get('data') and result['data'].get('emails'):
            emails = result['data']['emails']
            print(f"   ✅ Found {len(emails)} emails")
            
            # Filter for high-confidence emails
            high_confidence = [e for e in emails if e.get('confidence', 0) >= 70]
            if high_confidence:
                print(f"   High-confidence emails ({len(high_confidence)}):")
                for email in high_confidence[:3]:  # Show top 3
                    print(f"     • {email.get('value')} ({email.get('type', 'unknown')}, {email.get('confidence')}% confidence)")
                
                # Get the best email (highest confidence personal email)
                personal_emails = [e for e in high_confidence if e.get('type') == 'personal']
                if personal_emails:
                    best_email = max(personal_emails, key=lambda x: x.get('confidence', 0))
                    return {
                        'company': company['name'],
                        'domain': company['domain'],
                        'best_email': best_email['value'],
                        'email_type': best_email['type'],
                        'confidence': best_email['confidence'],
                        'all_emails': [e['value'] for e in high_confidence],
                        'found': True
                    }
                else:
                    # Use any high-confidence email
                    best_email = max(high_confidence, key=lambda x: x.get('confidence', 0))
                    return {
                        'company': company['name'],
                        'domain': company['domain'],
                        'best_email': best_email['value'],
                        'email_type': best_email['type'],
                        'confidence': best_email['confidence'],
                        'all_emails': [e['value'] for e in high_confidence],
                        'found': True
                    }
            else:
                print(f"   ⚠️ No high-confidence emails found")
                return {
                    'company': company['name'],
                    'domain': company['domain'],
                    'best_email': None,
                    'found': False,
                    'error': 'No high-confidence emails'
                }
        else:
            print(f"   ❌ No emails found or API error")
            return {
                'company': company['name'],
                'domain': company['domain'],
                'best_email': None,
                'found': False,
                'error': result.get('errors', ['No emails found'])[0]
            }
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return {
            'company': company['name'],
            'domain': company['domain'],
            'best_email': None,
            'found': False,
            'error': str(e)
        }

def generate_email_body(company, contact_email):
    """Generate personalized email body for defense sector outreach"""
    
    # Different templates based on company type
    if "Ventures" in company['name'] or "Investors" in company['name'] or "Fund" in company['sector']:
        # Investor template
        subject = f"Introduction: Defense Tech Investment Opportunities"
        
        body = f"""Dear {company['name']} Team,

I hope this message finds you well. I'm reaching out because your focus on {company['sector']} aligns perfectly with the defense technology opportunities we're currently working with.

We represent several high-growth defense tech companies in Europe and North America that are seeking strategic investment and partnership opportunities. These include:

• AI-powered battlefield software (Series B, €600M+ raised)
• Autonomous ISR drone systems ($200M+ funding)
• Counter-drone/C-UAS electronic warfare platforms
• Space-based defense/SAR satellite technology

Given {company['name']}'s expertise in {company['sector'].lower()}, I believe there could be strong alignment with our portfolio companies.

Would you be open to a brief introductory call to discuss potential investment opportunities? I'd be happy to share detailed profiles of companies that match your investment thesis.

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    else:
        # Defense company template
        subject = f"Introduction: Strategic Partnership Opportunities for {company['name']}"
        
        body = f"""Dear {company['name']} Team,

I hope this message finds you well. I'm reaching out because we've been following {company['name']}'s impressive work in {company['sector']} and believe there could be valuable partnership opportunities.

Our team specializes in connecting defense technology companies with strategic investors, government contracts, and international expansion opportunities. We've successfully facilitated partnerships for similar organizations in:

• European defense tech expansion to Middle East/Asian markets
• Government contract navigation and proposal support
• Strategic investor introductions for growth capital
• Technology licensing and joint venture opportunities

Given {company['name']}'s position in the {company['sector']} sector, I believe there could be significant synergy with our network of defense-focused investors and government partners.

Would you be open to a brief 15-minute call to explore potential areas of collaboration? I'd be happy to share specific examples of partnerships we've facilitated for similar defense technology companies.

Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""
    
    return subject, body

def send_email_via_agentmail(to_email, subject, body):
    """Send email via AgentMail API"""
    # This is a placeholder - in production, use AgentMail API
    print(f"   📧 Would send to: {to_email}")
    print(f"   Subject: {subject}")
    print(f"   Body preview: {body[:200]}...")
    return True

def main():
    """Main execution"""
    print("=" * 70)
    print("DEFENSE SECTOR EMAIL ENRICHMENT & OUTREACH")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    # Check Hunter.io account status
    print("\n📊 Checking Hunter.io account status...")
    account_info = hunter_client.get_account_info()
    if account_info.get('data'):
        credits = account_info['data'].get('calls', {}).get('available', 0)
        used = account_info['data'].get('calls', {}).get('used', 0)
        print(f"   ✅ Credits available: {credits}")
        print(f"   ✅ Credits used: {used}")
    else:
        print(f"   ❌ Could not get account info")
        return
    
    # Find emails for all companies
    print("\n" + "=" * 70)
    print("EMAIL ENRICHMENT PHASE")
    print("=" * 70)
    
    all_companies = DEFENSE_COMPANIES + PE_VC_FUNDS
    enriched_companies = []
    
    for i, company in enumerate(all_companies, 1):
        print(f"\n[{i}/{len(all_companies)}] ", end="")
        result = find_emails_for_company(company)
        
        if result['found']:
            enriched_companies.append({
                **company,
                'contact_email': result['best_email'],
                'confidence': result['confidence'],
                'email_type': result['email_type']
            })
        
        # Rate limiting - be gentle with Hunter.io API
        if i < len(all_companies):
            time.sleep(2)  # 2 second delay between requests
    
    # Summary of enrichment
    print("\n" + "=" * 70)
    print("ENRICHMENT SUMMARY")
    print("=" * 70)
    print(f"Total companies: {len(all_companies)}")
    print(f"Emails found: {len(enriched_companies)}")
    print(f"Success rate: {len(enriched_companies)/len(all_companies)*100:.1f}%")
    
    if enriched_companies:
        print("\n📋 Companies with emails found:")
        for company in enriched_companies:
            print(f"  • {company['name']}: {company['contact_email']} ({company['confidence']}% confidence)")
    
    # Outreach phase
    print("\n" + "=" * 70)
    print("OUTREACH PHASE")
    print("=" * 70)
    
    outreach_results = []
    for i, company in enumerate(enriched_companies, 1):
        print(f"\n[{i}/{len(enriched_companies)}] Preparing outreach for: {company['name']}")
        
        subject, body = generate_email_body(company, company['contact_email'])
        
        # In production, this would actually send the email
        # For now, we'll just simulate it
        success = send_email_via_agentmail(company['contact_email'], subject, body)
        
        outreach_results.append({
            'company': company['name'],
            'email': company['contact_email'],
            'subject': subject,
            'sent': success,
            'timestamp': datetime.now().isoformat()
        })
        
        print(f"   ✅ Outreach prepared")
    
    # Save results
    output_file = f"/Users/cubiczan/.openclaw/workspace/defense-leads/enrichment-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            'enriched_companies': enriched_companies,
            'outreach_results': outreach_results,
            'timestamp': datetime.now().isoformat(),
            'hunter_credits_used': len(all_companies)
        }, f, indent=2)
    
    print("\n" + "=" * 70)
    print("✅ PROCESS COMPLETE")
    print("=" * 70)
    print(f"\nSummary:")
    print(f"  • Companies processed: {len(all_companies)}")
    print(f"  • Emails found: {len(enriched_companies)}")
    print(f"  • Outreach prepared: {len(outreach_results)}")
    print(f"  • Results saved to: {output_file}")
    print(f"\nNext steps:")
    print(f"  1. Review the enriched contacts")
    print(f"  2. Send actual emails via AgentMail")
    print(f"  3. Follow up in 3-5 days")
    print("=" * 70)

if __name__ == "__main__":
    main()