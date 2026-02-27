#!/usr/bin/env python3
"""
Send 15 defense sector emails via Gmail SMTP
Using new Hunter.io API key for email finding
"""

import sys
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from datetime import datetime

# Import Hunter.io client
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace')
from hunter_io_config import hunter_client

# Gmail SMTP Configuration
CRON_GMAIL_EMAIL = "sam@cubiczan.com"
CRON_GMAIL_PASSWORD = "mwzh abbf ssih mjsf"
CRON_GMAIL_CC = "sam@impactquadrant.info"

STANDARD_SIGNATURE = """Best regards,

Zane
Agent Manager
Impact Quadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""

# Defense companies and funds
COMPANIES = [
    # Defense Companies (10)
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
    
    # PE/VC Funds (5)
    {"name": "MASNA Ventures", "domain": "masna.vc", "sector": "Defense-focused VC", "score": 95, "type": "investor"},
    {"name": "Raphe mPhibr Investors", "domain": "raphe.co.in", "sector": "Drone manufacturing, defense systems", "score": 88, "type": "investor"},
    {"name": "iDEX Ecosystem Investors", "domain": "idex.gov.in", "sector": "Government-backed defense innovation", "score": 85, "type": "investor"},
    {"name": "General Atlantic", "domain": "generalatlantic.com", "sector": "Technology, defense tech", "score": 82, "type": "investor"},
    {"name": "Blackstone", "domain": "blackstone.com", "sector": "Technology, infrastructure", "score": 80, "type": "investor"},
]

def find_best_email(domain):
    """Find the best email for a domain using Hunter.io"""
    try:
        result = hunter_client.domain_search(domain, limit=5)
        
        if result.get('data') and result['data'].get('emails'):
            emails = result['data']['emails']
            
            # Get highest confidence email
            best_email = max(emails, key=lambda x: x.get('confidence', 0))
            
            if best_email.get('confidence', 0) >= 70:
                return {
                    'email': best_email['value'],
                    'type': best_email.get('type', 'unknown'),
                    'confidence': best_email.get('confidence', 0),
                    'position': best_email.get('position', ''),
                }
    
    except Exception as e:
        print(f"Error finding email for {domain}: {str(e)}")
    
    return None

def send_gmail_email(to_email, subject, body):
    """Send email via Gmail SMTP"""
    try:
        # Prepare recipients
        to_list = [to_email] if isinstance(to_email, str) else to_email
        cc_list = [CRON_GMAIL_CC]
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f'Agent Manager <{CRON_GMAIL_EMAIL}>'
        msg['To'] = ', '.join(to_list)
        msg['Cc'] = ', '.join(cc_list)
        msg['Subject'] = subject
        
        # Add text version
        full_text = body
        text_part = MIMEText(full_text, 'plain')
        msg.attach(text_part)
        
        # Connect and send
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=context)
        server.login(CRON_GMAIL_EMAIL, CRON_GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True, "Email sent successfully"
        
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

def generate_email(company):
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
    print("DEFENSE SECTOR OUTREACH - SENDING 15 EMAILS")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Check Hunter.io credits
    print("\n📊 Checking Hunter.io account...")
    account_info = hunter_client.get_account_info()
    if account_info.get('data'):
        credits = account_info['data'].get('calls', {}).get('available', 0)
        print(f"   ✅ Credits available: {credits}")
    else:
        print(f"   ⚠️ Could not check account info, continuing anyway...")
    
    # Process each company
    print(f"\n🔍 Processing {len(COMPANIES)} companies/funds...")
    print("-" * 70)
    
    results = []
    sent_count = 0
    
    for i, company in enumerate(COMPANIES, 1):
        print(f"\n[{i}/{len(COMPANIES)}] {company['name']}")
        
        # Find email
        email_info = find_best_email(company['domain'])
        
        if not email_info:
            print(f"   ❌ No email found for {company['domain']}")
            results.append({
                'company': company['name'],
                'domain': company['domain'],
                'status': 'no_email',
                'timestamp': datetime.now().isoformat()
            })
            continue
        
        print(f"   ✅ Email: {email_info['email']} ({email_info['confidence']}% confidence)")
        
        # Generate email
        subject, body = generate_email(company)
        
        # Send email via Gmail
        print(f"   📧 Sending via Gmail SMTP...")
        success, message = send_gmail_email(email_info['email'], subject, body)
        
        if success:
            print(f"   ✅ Email sent successfully")
            sent_count += 1
            status = 'sent'
        else:
            print(f"   ❌ Failed: {message}")
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
            'error': message if not success else None
        })
        
        # Rate limiting
        if i < len(COMPANIES):
            time.sleep(3)  # 3 second delay between emails
    
    # Save results
    output_file = f"/Users/cubiczan/.openclaw/workspace/defense-leads/emails-sent-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
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
        f.write(f"\n\n## 📧 EMAILS SENT - {datetime.now().strftime('%H:%M')}\n")
        f.write(f"**Status:** ✅ COMPLETED - {sent_count}/{len(COMPANIES)} emails sent via Gmail SMTP\n")
        f.write(f"**Method:** Gmail SMTP ({CRON_GMAIL_EMAIL})\n")
        f.write(f"**CC:** {CRON_GMAIL_CC}\n")
        f.write(f"**Results:** {output_file}\n\n")
        
        # List sent emails
        f.write("### Emails Sent:\n")
        for result in results:
            if result.get('email') and result['status'] == 'sent':
                f.write(f"- **{result['company']}**: {result['email']} ({result['confidence']}% confidence)\n")
    
    print("\n" + "=" * 70)
    print("✅ MISSION ACCOMPLISHED!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"  • Total targets: {len(COMPANIES)}")
    print(f"  • Emails found: {len([r for r in results if r.get('email')])}")
    print(f"  • Emails sent: {sent_count}")
    print(f"  • Success rate: {sent_count/len(COMPANIES)*100:.1f}%" if COMPANIES else "0%")
    print(f"\n📁 Files:")
    print(f"  • Results: {output_file}")
    print(f"  • Log updated: {log_file}")
    print(f"\n📧 All emails CC'd to: {CRON_GMAIL_CC}")
    print(f"📧 Sent from: {CRON_GMAIL_EMAIL}")
    print("\n🎯 Defense sector outreach is now complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()