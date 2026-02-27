#!/usr/bin/env python3
"""
Standardized Gmail SMTP Module for All Outreach
Use this instead of AgentMail for reliable email delivery.
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Union, Optional
import time

# Gmail Account Configuration
# Primary: sam@cubiczan.com
# Backup: sam@impactquadrant.info
# Backup: zan@impactquadrant.info

GMAIL_ACCOUNTS = [
    {
        "email": "sam@cubiczan.com",
        "password": "mwzh abbf ssih mjsf",  # App password
        "name": "Agent Manager"
    },
    {
        "email": "sam@impactquadrant.info",
        "password": "",  # Add app password when available
        "name": "Sam Desigan"
    },
    {
        "email": "zan@impactquadrant.info",
        "password": "",  # Add app password when available
        "name": "Zane"
    }
]

# Default CC for all emails
DEFAULT_CC = ["sam@impactquadrant.info"]

# Standard signature for all emails
STANDARD_SIGNATURE = """Best regards,

Agent Manager

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up."""

class GmailSender:
    """Standardized Gmail SMTP sender for all outreach"""
    
    def __init__(self, account_index=0, delay_seconds=2):
        """
        Initialize Gmail sender
        
        Args:
            account_index: Which Gmail account to use (0=sam@cubiczan.com)
            delay_seconds: Delay between emails to avoid rate limits
        """
        self.account = GMAIL_ACCOUNTS[account_index]
        self.delay_seconds = delay_seconds
        self.last_sent_time = 0
        
    def _wait_for_rate_limit(self):
        """Wait between emails to avoid rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_sent_time
        if time_since_last < self.delay_seconds:
            time.sleep(self.delay_seconds - time_since_last)
        self.last_sent_time = time.time()
    
    def send_email(
        self,
        to_emails: Union[str, List[str]],
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        cc_emails: Optional[Union[str, List[str]]] = None,
        bcc_emails: Optional[Union[str, List[str]]] = None
    ) -> dict:
        """
        Send email via Gmail SMTP
        
        Args:
            to_emails: Recipient email(s)
            subject: Email subject
            body_text: Plain text email body
            body_html: HTML email body (optional)
            cc_emails: CC email(s) (optional)
            bcc_emails: BCC email(s) (optional)
            
        Returns:
            dict: Result with success status and message
        """
        # Wait for rate limiting
        self._wait_for_rate_limit()
        
        try:
            # Prepare recipients
            if isinstance(to_emails, str):
                to_list = [to_emails]
            else:
                to_list = to_emails
            
            # Prepare CC (default to sam@impactquadrant.info)
            if cc_emails is None:
                cc_list = DEFAULT_CC.copy()
            elif isinstance(cc_emails, str):
                cc_list = [cc_emails]
            else:
                cc_list = cc_emails
            
            # Prepare BCC
            if bcc_emails is None:
                bcc_list = []
            elif isinstance(bcc_emails, str):
                bcc_list = [bcc_emails]
            else:
                bcc_list = bcc_emails
            
            # Add standard signature
            full_text = body_text + "\n\n" + STANDARD_SIGNATURE
            if body_html:
                full_html = body_html + "<br><br>" + STANDARD_SIGNATURE.replace('\n', '<br>')
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f'{self.account["name"]} <{self.account["email"]}>'
            msg['To'] = ', '.join(to_list)
            if cc_list:
                msg['Cc'] = ', '.join(cc_list)
            msg['Subject'] = subject
            
            # Add text version
            text_part = MIMEText(full_text, 'plain')
            msg.attach(text_part)
            
            # Add HTML version if provided
            if body_html:
                html_part = MIMEText(full_html, 'html')
                msg.attach(html_part)
            
            # Combine all recipients
            all_recipients = to_list + cc_list + bcc_list
            
            # Connect and send
            context = ssl.create_default_context()
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls(context=context)
            server.login(self.account["email"], self.account["password"])
            server.send_message(msg, from_addr=self.account["email"], to_addrs=all_recipients)
            server.quit()
            
            return {
                "success": True,
                "message": f"Email sent successfully from {self.account['email']}",
                "from": self.account["email"],
                "to": to_list,
                "cc": cc_list,
                "subject": subject
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "from": self.account["email"],
                "to": to_list
            }
    
    def send_batch(
        self,
        emails: List[dict],
        batch_size: int = 50,
        batch_delay: int = 60
    ) -> List[dict]:
        """
        Send batch of emails with rate limiting
        
        Args:
            emails: List of email dicts with keys: to, subject, body_text, body_html, cc
            batch_size: Number of emails per batch
            batch_delay: Delay between batches in seconds
            
        Returns:
            List of results for each email
        """
        results = []
        total_emails = len(emails)
        
        print(f"Sending {total_emails} emails in batches of {batch_size}...")
        
        for i, email_data in enumerate(emails, 1):
            try:
                result = self.send_email(**email_data)
                results.append(result)
                
                print(f"  [{i}/{total_emails}] {email_data['to']}: {'✅' if result['success'] else '❌'} {result.get('message', result.get('error', ''))}")
                
                # Batch delay
                if i % batch_size == 0 and i < total_emails:
                    print(f"  Waiting {batch_delay} seconds before next batch...")
                    time.sleep(batch_delay)
                    
            except Exception as e:
                results.append({
                    "success": False,
                    "error": str(e),
                    "to": email_data.get('to', 'Unknown')
                })
                print(f"  [{i}/{total_emails}] {email_data.get('to', 'Unknown')}: ❌ {str(e)}")
        
        return results

# Quick utility functions for common use cases
def send_single_email(to_email, subject, body_text, **kwargs):
    """Quick function to send a single email"""
    sender = GmailSender()
    return sender.send_email(to_email, subject, body_text, **kwargs)

def send_campaign_emails(emails, **kwargs):
    """Quick function to send campaign emails"""
    sender = GmailSender()
    return sender.send_batch(emails, **kwargs)

# Example usage
if __name__ == "__main__":
    # Test the Gmail sender
    print("Testing Gmail SMTP sender...")
    
    # Single email test
    test_result = send_single_email(
        to_email="test@example.com",
        subject="Test email from Gmail SMTP",
        body_text="This is a test email sent via Gmail SMTP."
    )
    
    if test_result["success"]:
        print("✅ Test email sent successfully!")
        print(f"   From: {test_result['from']}")
        print(f"   To: {test_result['to']}")
    else:
        print(f"❌ Test failed: {test_result['error']}")
    
    print("\nGmail SMTP module ready for use in all outreach scripts!")
