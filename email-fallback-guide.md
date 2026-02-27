# Email Fallback Guide - AgentMail API Down

**Issue Date:** 2026-02-22
**Status:** CRITICAL - AgentMail POST endpoints returning 404
**Impact:** All email outreach campaigns blocked

---

## Confirmed Issue

AgentMail API is responding to GET requests but POST endpoints fail:

```bash
# GET /v0/inboxes - WORKS ✅
curl -X GET "https://api.agentmail.to/v0/inboxes" -H "Authorization: Bearer am_..."
# Returns: {"count":2,"inboxes":[...]}

# POST /v0/inboxes/{inbox}/messages - FAILS ❌
curl -X POST "https://api.agentmail.to/v0/inboxes/zander@agentmail.to/messages" \
  -H "Authorization: Bearer am_..." \
  -H "Content-Type: application/json" \
  -d '{"to":"test@example.com","subject":"Test","text":"Test"}'
# Returns: {"name":"NotFoundError","message":"Route not found"}
```

**Endpoint tested:**
- `/v0/inboxes/{inbox}/messages` - 404
- `/v1/emails` - 404
- `/v0/send` - 404
- `/v1/send` - 404

---

## Option 1: Gmail SMTP with App Password (RECOMMENDED)

### Setup Steps

1. **Enable 2FA on Gmail account** (required for app passwords)
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Mac" (or "Other")
   - Copy the 16-character password

3. **Python Script Template**

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_via_gmail(to_email, subject, body_text, body_html=None):
    """
    Send email via Gmail SMTP with app password.
    
    Gmail account: zan@impactquadrant.info
    Sender: sam@impactquadrant.info (reply-to)
    """
    
    # Gmail SMTP settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    gmail_user = "zan@impactquadrant.info"  # Your Gmail
    gmail_app_password = "xxxx xxxx xxxx xxxx"  # 16-char app password (NEEDS SETUP)
    
    # Create message
    msg = MIMEMultipart("alternative")
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg["Reply-To"] = "sam@impactquadrant.info"
    msg["Cc"] = "sam@impactquadrant.info"
    
    # Add text body
    msg.attach(MIMEText(body_text, "plain"))
    
    # Add HTML body if provided
    if body_html:
        msg.attach(MIMEText(body_html, "html"))
    
    # Send
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(gmail_user, gmail_app_password)
        
        # Include CC in recipients
        recipients = [to_email, "sam@impactquadrant.info"]
        server.sendmail(gmail_user, recipients, msg.as_string())
        server.quit()
        
        return {"success": True, "message": f"Email sent to {to_email}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Usage
result = send_email_via_gmail(
    to_email="jablin@cressetcapital.com",
    subject="Legacy wellness asset in Costa Rica",
    body_text="Dear Mr. Ablin...",
    body_html="<p>Dear Mr. Ablin...</p>"
)
print(result)
```

### Credentials Needed
- **Gmail account:** zan@impactquadrant.info (already exists)
- **App password:** NEEDS TO BE GENERATED
- **Generate at:** https://myaccount.google.com/apppasswords

---

## Option 2: SendGrid API

### Pricing
- Free tier: 100 emails/day
- Paid: $14.95/month for 50K emails

### Setup
```python
import requests

def send_via_sendgrid(to_email, subject, body_text, body_html):
    api_key = "SG.xxxxx"  # Needs account
    url = "https://api.sendgrid.com/v3/mail/send"
    
    data = {
        "personalizations": [{
            "to": [{"email": to_email}],
            "cc": [{"email": "sam@impactquadrant.info"}]
        }],
        "from": {"email": "sam@impactquadrant.info"},
        "subject": subject,
        "content": [
            {"type": "text/plain", "value": body_text},
            {"type": "text/html", "value": body_html}
        ]
    }
    
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=data
    )
    
    return {"success": response.status_code == 202, "status": response.status_code}
```

---

## Option 3: Mailgun API

### Pricing
- Free tier: 5,000 emails/month (first 3 months)
- Pay-as-you-go: $0.80/1000 emails

### Setup
```python
import requests

def send_via_mailgun(to_email, subject, body_text, body_html):
    api_key = "key-xxxxx"  # Needs account
    domain = "mg.impactquadrant.info"  # Needs DNS setup
    
    response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": "Sam Desigan <sam@impactquadrant.info>",
            "to": to_email,
            "cc": "sam@impactquadrant.info",
            "subject": subject,
            "text": body_text,
            "html": body_html
        }
    )
    
    return {"success": response.status_code == 200, "response": response.json()}
```

---

## Pending Emails (Ready to Send)

### Dorada Resort - Wave 1
| Contact | Email | Status |
|---------|-------|--------|
| Jack Ablin (Cresset) | jablin@cressetcapital.com | ⏳ Ready to send |

### Miami Hotels - Wave 1
| Contact | Email | Status |
|---------|-------|--------|
| Tim Swanson (Marsh McLennan) | tim.swanson@marshmma.com | ⏳ Ready to send (API failed) |
| Jon Flood (Roseview) | jon.flood@madisonmarquette.com | ⏳ Ready to send |

---

## Recommendation

**Immediate:** Generate Gmail app password for zan@impactquadrant.info
**Short-term:** Contact AgentMail support to check API status
**Long-term:** Consider SendGrid/Mailgun as backup provider

---

*Created: 2026-02-24 2:00 AM EST*
*Author: Claw (autonomous session)*
