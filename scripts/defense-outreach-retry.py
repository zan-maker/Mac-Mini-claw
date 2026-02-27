#!/usr/bin/env python3
"""
Defense Sector Outreach - Clean Version
Finds emails using Hunter.io and sends outreach via AgentMail
"""

import sys
import json
import time
import requests
from datetime import datetime

# Import Hunter.io client
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace')
from hunter_io_config import hunter_client

# AgentMail configuration
AGENTMAIL_API_KEY = "am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f"
FROM_EMAIL = "Zane@agentmail.to"
CC_EMAIL = "sam@impactquadrant.info"

# Standard signature
STANDARD_SIGNATURE = """Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""

# Defense companies from the report
COMPANIES = [
    # Defense Companies
    {"name": "Helsing", "domain": "helsing.ai", "sector": "AI & Battlefield Software", "score": 92, "type": "company"},
    {"name": "Quantum Systems", "domain": "quantum-systems.com", "sector": "Autonomous ISR Drones", "score": 88, "type": "company"},
    {"name": "Comand AI", "domain": "comand.ai", "sector": "AI-Powered Targeting Systems", "score": 85, "type": "company"},
    {"name": "BforeAI", "domain": "bfore.ai", "sector": "Cyber Threat Intelligence", "score": 82, "type": "company"},
    {"name": "VIZGARD", "domain": "vizgard.com", "sector": "AI-Powered Optical Security", "score": 80, "type": "company"},
    {"name": "RobCo", "domain": "rob.co", "sector": "AI-Powered Industrial Robotics", "score": 75, "type": "company"},
    {"name": "XRF.ai", "domain": "xrf.ai", "sector": "Advanced Radar & Signal Processing", "score": 72, "type": "company"},
    {"name": "Perciv AI", "domain": "perciv.ai", "sector": "Radar Perception Systems", "score": 70, "type": "company"},
    {"name": "Drone Defense", "domain": "dronedefense.co.uk", "sector": "Counter-Drone / Airspace Security", "score": 68, "type": "company"},
    {"name": "Novadem", "domain": "novadem.com", "sector": "Tactical Drones", "score": 65, "type": "company"},
    
    # PE/VC Funds
    {"name": "MASNA Ventures", "domain": "masna.vc", "sector": "Defense-focused VC", "score": 95, "type": "investor"},
    {"name": "Raphe mPhibr Investors", "domain": "raphe.co.in", "sector": "Drone manufacturing, defense systems", "score": 88, "type": "investor"},
    {"name": "iDEX Ecosystem Investors", "domain": "idex.gov.in", "sector": "Government-backed defense innovation", "score": 85, "type": "investor"},
    {"name": "General Atlantic", "domain": "generalatlantic.com", "sector": "Technology, defense tech", "score": 82, "type": "investor"},
    {"name": "Blackstone", "domain": "blackstone.com", "sector": "Technology, infrastructure", "score": 80, "type": "investor"},
]

def find_best_email(domain):
    """Find the best email for a domain using Hunter.io"""
    try:
        result = hunter_client.domain_search(domain, limit=10)
        
        if result.get('data') and result['data'].get('emails'):
            emails = result['data']['emails']
            
            # Filter for high-confidence emails
            high_conf = [e for e in emails if e.get('confidence', 0) >= 70]
            
            if not high_conf:
                return None
            
            # Prefer personal emails
            personal = [e for e in high_conf if e.get('type') == 'personal']
            if personal:
                # Get highest confidence personal email
                best = max(personal, key=lambda x: x.get('confidence', 0))
                return {
                    'email': best['value'],
                    'type': best['type'],
                    'confidence': best['confidence'],
                    'position': best.get('position', ''),
                    'sources': len(best.get('sources', []))
                }
            else:
                # Use any high-confidence email
                best = max(high_conf, key=lambda x: x.get('confidence', 0))
                return {
                    'email': best['value'],
                    'type': best['type'],
                    'confidence': best['confidence'],
                    'position': best.get('position', ''),
                    'sources': len(best.get('sources', []))
                }
    
    except Exception as e:
        print(f"Error finding email for {domain}: {str(e)}")
    
    return None

def send_agentmail_email(to_email, subject, body):
    """Send email via AgentMail API"""
    url = "https://api.agentmail.to/v1/emails"
    
    headers = {
        "Authorization": f"Bearer {AGENTMAIL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "cc": [CC_EMAIL],
        "subject": subject,
        "body": body
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return True, response.json()
    except Exception as e:
        return False, str(e)

def generate_email(company, email_info):
    """Generate personalized email"""
    
    if company['type'] == 'investor':
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

{STANDARD_SIGNATURE}"""
    
    else:  # company
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

{STANDARD_SIGNATURE}"""
    
    return subject, body

def main():
    """Main execution"""
    print("=" * 70)
    print("DEFENSE SECTOR OUTREACH - RETRY WITH NEW HUNTER.IO KEY")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Check Hunter.io credits
    print("\n📊 Checking Hunter.io account...")
    account_info = hunter_client.get_account_info()
    if account_info.get('data'):
        credits = account_info['data'].get('calls', {}).get('available', 0)
        print(f"   ✅ Credits available: {credits}")
    else:
        print(f"   ❌ Could not check account info")
        return
    
    # Find emails and send outreach
    print(f"\n🔍 Finding emails for {len(COMPANIES)} companies/funds...")
    print("-" * 70)
    
    results = []
    sent_count = 0
    
    for i, company in enumerate(COMPANIES, 1):
        print(f"\n[{i}/{len(COMPANIES)}] {company['name']} ({company['domain']})")
        
        # Find email
        email_info = find_best_email(company['domain'])
        
        if not email_info:
            print(f"   ❌ No email found")
            results.append({
                'company': company['name'],
                'domain': company['domain'],
                'status': 'no_email',
                'timestamp': datetime.now().isoformat()
            })
            continue
        
        print(f"   ✅ Found: {email_info['email']} ({email_info['confidence']}% confidence)")
        
        # Generate email
        subject, body = generate_email(company, email_info)
        
        # Send email via AgentMail
        print(f"   📧 Sending outreach...")
        success, response = send_agentmail_email(email_info['email'], subject, body)
        
        if success:
            print(f"   ✅ Email sent successfully")
            sent_count += 1
            status = 'sent'
        else:
            print(f"   ❌ Failed to send: {response}")
            status = 'failed'
        
        results.append({
            'company': company['name'],
            'domain': company['domain'],
            'email': email_info['email'],
            'confidence': email_info['confidence'],
            'type': company['type'],
            'status': status,
            'subject': subject,
            'timestamp': datetime.now().isoformat(),
            'error': response if not success else None
        })
        
        # Rate limiting
        if i < len(COMPANIES):
            time.sleep(3)  # 3 second delay
    
    # Save results
    output_file = f"/Users/cubiczan/.openclaw/workspace/defense-leads/outreach-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            'summary': {
                'total': len(COMPANIES),
                'emails_found': len([r for r in results if r.get('email')]),
                'emails_sent': sent_count,
                'success_rate': f"{sent_count/len(COMPANIES)*100:.1f}%" if COMPANIES else "0%"
            },
            'results': results,
            'timestamp': datetime.now().isoformat()
        }, f, indent=2)
    
    # Update outreach log
    log_file = "/Users/cubiczan/.openclaw/workspace/defense-leads/outreach-log-2026-02-26.md"
    with open(log_file, 'a') as f:
        f.write(f"\n\n## Outreach Retry - {datetime.now().strftime('%H:%M')}\n")
        f.write(f"**Status:** ✅ COMPLETED - {sent_count}/{len(COMPANIES)} emails sent\n")
        f.write(f"**Hunter.io Credits:** Used {len(COMPANIES)} searches\n")
        f.write(f"**Method:** AgentMail API\n")
        f.write(f"**Results file:** {output_file}\n")
    
    print("\n" + "=" * 70)
    print("✅ OUTREACH COMPLETE!")
    print("=" * 70)
    print(f"\nSummary:")
    print(f"  • Total companies/funds: {len(COMPANIES)}")
    print(f"  • Emails found: {len([r for r in results if r.get('email')])}")
    print(f"  • Emails sent: {sent_count}")
    print(f"  • Success rate: {sent_count/len(COMPANIES)*100:.1f}%" if COMPANIES else "0%")
    print(f"\nFiles:")
    print(f"  • Results: {output_file}")
    print(f"  • Log updated: {log_file}")
    print(f"\nAll emails CC'd to: {CC_EMAIL}")
    print("=" * 70)

if __name__ == "__main__":
    main()