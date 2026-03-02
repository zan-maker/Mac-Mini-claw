#!/usr/bin/env python3
# CRON JOB DEDICATED GMAIL ACCOUNT

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

# Gmail Rotation System
import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace/scripts')
from gmail_rotation_simple import send_email_with_rotation

CRON_GMAIL_EMAIL = "sam@cubiczan.com"
CRON_GMAIL_PASSWORD = "mwzh abbf ssih mjsf"
CRON_GMAIL_CC = "sam@impactquadrant.info"

STANDARD_SIGNATURE = """Best regards,

Agent Manager
Sam Desigan
Sam@impactquadrant.info
Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up"""

def send_email_with_rotation(to_emails, subject, body_text, body_html=None, cc_emails=None):
    """Send email using dedicated cron job Gmail account"""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import ssl
    
    try:
        # Prepare recipients
        if isinstance(to_emails, str):
            to_list = [to_emails]
        else:
            to_list = to_emails
        
        if cc_emails is None:
            cc_list = [CRON_GMAIL_CC]
        elif isinstance(cc_emails, str):
            cc_list = [cc_emails, CRON_GMAIL_CC]
        else:
            cc_list = cc_emails + [CRON_GMAIL_CC]
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = CRON_GMAIL_EMAIL
        msg['To'] = ', '.join(to_list)
        msg['Cc'] = ', '.join(cc_list)
        
        # Add body
        part1 = MIMEText(body_text + '\n\n' + STANDARD_SIGNATURE, 'plain')
        if body_html:
            part2 = MIMEText(body_html + '<br><br>' + STANDARD_SIGNATURE.replace('\n', '<br>'), 'html')
            msg.attach(part2)
        msg.attach(part1)
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(CRON_GMAIL_EMAIL, CRON_GMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email sent to {len(to_list)} recipients")
        return True
        
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False

# Email templates for expense reduction
def create_expense_reduction_email(company_name, contact_name, contact_email, industry, employee_count):
    """Create expense reduction outreach email"""
    
    subject = f"OPEX reduction opportunity for {company_name}"
    
    text = f"""Hi {contact_name.split()[0] if contact_name else 'there'},

I noticed {company_name} is in the {industry} space with approximately {employee_count} employees.

I specialize in technology-led expense reduction for companies with 20+ employees. We typically identify 15-30% savings across:
• SaaS/software subscriptions
• Telecom & internet services  
• Logistics & shipping
• Vendor contracts
• Insurance & benefits

Our process is data-driven and success-based (we only get paid on verified savings).

Would you be open to a 15-minute discovery call to see if there's a fit?

Best,
Zander
"""
    
    html = f"""<p>Hi {contact_name.split()[0] if contact_name else 'there'},</p>

<p>I noticed {company_name} is in the {industry} space with approximately {employee_count} employees.</p>

<p>I specialize in technology-led expense reduction for companies with 20+ employees. We typically identify 15-30% savings across:</p>

<ul>
<li>SaaS/software subscriptions</li>
<li>Telecom & internet services</li>
<li>Logistics & shipping</li>
<li>Vendor contracts</li>
<li>Insurance & benefits</li>
</ul>

<p>Our process is data-driven and success-based (we only get paid on verified savings).</p>

<p>Would you be open to a 15-minute discovery call to see if there's a fit?</p>

<p>Best,<br>Zander</p>
"""
    
    return {"to": contact_email, "subject": subject, "text": text, "html": html, "cc": CRON_GMAIL_CC}

def send_expense_reduction_outreach(company_data):
    """Send expense reduction outreach"""
    email_data = create_expense_reduction_email(
        company_data['company_name'],
        company_data['contact_name'],
        company_data['contact_email'],
        company_data['industry'],
        company_data['employee_count']
    )
    
    return send_email_with_rotation(
        email_data['to'],
        email_data['subject'],
        email_data['text'],
        email_data['html'],
        email_data['cc']
    )

if __name__ == "__main__":
    # Test the system
    print("Testing Expense Reduction AgentMail System")
    
    test_data = {
        'company_name': 'Test Corporation',
        'contact_name': 'John Doe',
        'contact_email': 'test@example.com',
        'industry': 'technology',
        'employee_count': '50'
    }
    
    print("\nCreating expense reduction email...")
    email = create_expense_reduction_email(**test_data)
    print(f"Subject: {email['subject']}")
    print(f"Preview: {email['text'][:100]}...")
    
    print("\n✅ System ready for use!")