#!/usr/bin/env python3
# CRON JOB DEDICATED GMAIL ACCOUNT
CRON_GMAIL_EMAIL = "sam@cubiczan.com"
CRON_GMAIL_PASSWORD = "mwzh abbf ssih mjsf"
CRON_GMAIL_CC = "sam@impactquadrant.info"

STANDARD_SIGNATURE = """Best regards,

Agent Manager
Sam Desigan
Sam@impactquadrant.info
Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up"""

def send_cron_email(to_emails, subject, body_text, body_html=None, cc_emails=None):
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

# Email templates
CC_EMAIL = "sam@impactquadrant.info"

def create_prospect_email(firm_name, service_type, contact_name, contact_email, vertical):
    """Create email to prospect (business needing services)"""
    
    subject = f"Introduction — vetted {service_type} providers"
    
    text = f"""Hi {contact_name.split()[0] if contact_name else 'there'},

I noticed your company is in the {vertical} space. I run a network that connects growing companies with pre-vetted {service_type} providers.

We work with a curated list of {service_type} firms that have proven track records with companies like yours. If you're considering {service_type} services in the next 3-6 months, I'd be happy to make introductions.

Would a brief call make sense?

Best,
Zander
"""
    
    html = f"""<p>Hi {contact_name.split()[0] if contact_name else 'there'},</p>

<p>I noticed your company is in the {vertical} space. I run a network that connects growing companies with pre-vetted {service_type} providers.</p>

<p>We work with a curated list of {service_type} firms that have proven track records with companies like yours. If you're considering {service_type} services in the next 3-6 months, I'd be happy to make introductions.</p>

<p>Would a brief call make sense?</p>

<p>Best,<br>Zander</p>
"""
    
    return {"to": contact_email, "subject": subject, "text": text, "html": html, "cc": CC_EMAIL}

def create_provider_email(firm_name, service_type, contact_name, contact_email, vertical):
    """Create email to service provider (seeking referral partnership)"""
    
    subject = f"Referral partnership — qualified {vertical} leads"
    
    # Text version
    text = f"""Hi {contact_name.split()[0] if contact_name else 'there'},

I run a business advisory network that connects growing companies with vetted {service_type} providers. We're currently working with companies showing strong buying signals for {service_type}.

We'd like to explore a referral partnership where we introduce qualified prospects to your firm in exchange for a standard referral fee on closed engagements.

Our introductions are pre-qualified — we only connect companies that have demonstrated clear intent and fit for your services.

Would you be open to a 15-minute call this week to discuss terms?

Best,
Zander
"""
    
    # HTML version
    html = f"""<p>Hi {contact_name.split()[0] if contact_name else 'there'},</p>

<p>I run a business advisory network that connects growing companies with vetted {service_type} providers. We're currently working with companies showing strong buying signals for {service_type}.</p>

<p>We'd like to explore a <strong>referral partnership</strong> where we introduce qualified prospects to your firm in exchange for a standard referral fee on closed engagements.</p>

<p>Our introductions are pre-qualified — we only connect companies that have demonstrated clear intent and fit for your services.</p>

<p>Would you be open to a 15-minute call this week to discuss terms?</p>

<p>Best,<br>Zander</p>
"""
    
    return {"to": contact_email, "subject": subject, "text": text, "html": html, "cc": CC_EMAIL}

def send_prospect_outreach(prospect_data):
    """Send outreach to prospect"""
    email_data = create_prospect_email(
        prospect_data['firm_name'],
        prospect_data['service_type'],
        prospect_data['contact_name'],
        prospect_data['contact_email'],
        prospect_data['vertical']
    )
    
    return send_cron_email(
        email_data['to'],
        email_data['subject'],
        email_data['text'],
        email_data['html'],
        email_data['cc']
    )

def send_provider_outreach(provider_data):
    """Send outreach to service provider"""
    email_data = create_provider_email(
        provider_data['firm_name'],
        provider_data['service_type'],
        provider_data['contact_name'],
        provider_data['contact_email'],
        provider_data['vertical']
    )
    
    return send_cron_email(
        email_data['to'],
        email_data['subject'],
        email_data['text'],
        email_data['html'],
        email_data['cc']
    )

if __name__ == "__main__":
    # Test the functions
    print("Testing B2B Referral AgentMail System")
    
    # Test prospect email
    prospect_test = {
        'firm_name': 'Test Company',
        'service_type': 'accounting',
        'contact_name': 'John Doe',
        'contact_email': 'test@example.com',
        'vertical': 'technology'
    }
    
    print("\nCreating prospect email...")
    prospect_email = create_prospect_email(**prospect_test)
    print(f"Subject: {prospect_email['subject']}")
    
    # Test provider email
    provider_test = {
        'firm_name': 'Accounting Firm LLC',
        'service_type': 'accounting',
        'contact_name': 'Jane Smith',
        'contact_email': 'test@example.com',
        'vertical': 'technology'
    }
    
    print("\nCreating provider email...")
    provider_email = create_provider_email(**provider_test)
    print(f"Subject: {provider_email['subject']}")
    
    print("\n✅ System ready for use!")