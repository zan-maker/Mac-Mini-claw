#!/usr/bin/env python3
"""
Brevo Email Client
Free: 9,000 emails/month
Replaces: AgentMail + Gmail SMTP
"""

import os
import json
import requests
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmailRecipient:
    """Email recipient"""
    email: str
    name: Optional[str] = None

@dataclass
class EmailAttachment:
    """Email attachment"""
    content: str  # base64 encoded
    name: str

@dataclass
class EmailResult:
    """Email sending result"""
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
    response: Optional[Dict] = None

class BrevoClient:
    """Brevo email client"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize Brevo client
        
        Args:
            config_path: Path to configuration file
        """
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.api_key = config.get('api_key')
            self.sender_email = config.get('sender_email', 'sam@impactquadrant.info')
            self.sender_name = config.get('sender_name', 'Agent Manager')
        else:
            # Try environment variable
            self.api_key = os.getenv('BREVO_API_KEY')
            self.sender_email = 'sam@impactquadrant.info'
            self.sender_name = 'Agent Manager'
        
        if not self.api_key:
            raise ValueError("Brevo API key not found in config or environment")
        
        self.base_url = "https://api.brevo.com/v3"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": self.api_key
        }
        
        # Test connection
        self.test_connection()
    
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            response = requests.get(
                f"{self.base_url}/account",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Connected to Brevo: {data.get('email')}")
                logger.info(f"   Plan: {data.get('plan')}, Credits: {data.get('credits')}")
                return True
            else:
                logger.error(f"❌ Connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            return False
    
    def send_email(
        self,
        to: Union[List[EmailRecipient], EmailRecipient, str],
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        cc: Optional[Union[List[EmailRecipient], EmailRecipient, str]] = None,
        bcc: Optional[Union[List[EmailRecipient], EmailRecipient, str]] = None,
        reply_to: Optional[EmailRecipient] = None,
        attachments: Optional[List[EmailAttachment]] = None,
        tags: Optional[List[str]] = None,
        **kwargs
    ) -> EmailResult:
        """
        Send email via Brevo
        
        Args:
            to: Recipient(s)
            subject: Email subject
            html_content: HTML content
            text_content: Plain text content (optional)
            cc: CC recipient(s)
            bcc: BCC recipient(s)
            reply_to: Reply-to address
            attachments: List of attachments
            tags: Email tags for tracking
            **kwargs: Additional Brevo API parameters
            
        Returns:
            EmailResult with success status
        """
        # Prepare recipients
        def prepare_recipients(recipients):
            if isinstance(recipients, str):
                return [{"email": recipients}]
            elif isinstance(recipients, EmailRecipient):
                return [{"email": recipients.email, "name": recipients.name}]
            elif isinstance(recipients, list):
                result = []
                for r in recipients:
                    if isinstance(r, str):
                        result.append({"email": r})
                    elif isinstance(r, EmailRecipient):
                        result.append({"email": r.email, "name": r.name})
                return result
            return []
        
        # Build payload
        payload = {
            "sender": {
                "email": self.sender_email,
                "name": self.sender_name
            },
            "to": prepare_recipients(to),
            "subject": subject,
            "htmlContent": html_content,
            **kwargs
        }
        
        # Add optional fields
        if text_content:
            payload["textContent"] = text_content
        
        if cc:
            payload["cc"] = prepare_recipients(cc)
        
        if bcc:
            payload["bcc"] = prepare_recipients(bcc)
        
        if reply_to:
            if isinstance(reply_to, EmailRecipient):
                payload["replyTo"] = {"email": reply_to.email, "name": reply_to.name}
            elif isinstance(reply_to, str):
                payload["replyTo"] = {"email": reply_to}
        
        if attachments:
            payload["attachment"] = [
                {"content": att.content, "name": att.name}
                for att in attachments
            ]
        
        if tags:
            payload["tags"] = tags
        
        try:
            logger.info(f"📧 Sending email to {len(payload['to'])} recipient(s)")
            logger.info(f"   Subject: {subject}")
            
            response = requests.post(
                f"{self.base_url}/smtp/email",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 201:
                data = response.json()
                message_id = data.get("messageId")
                logger.info(f"✅ Email sent successfully: {message_id}")
                
                return EmailResult(
                    success=True,
                    message_id=message_id,
                    response=data
                )
            else:
                error_msg = f"Send failed: {response.status_code} - {response.text}"
                logger.error(f"❌ {error_msg}")
                
                return EmailResult(
                    success=False,
                    error=error_msg,
                    response=response.json() if response.text else None
                )
                
        except Exception as e:
            error_msg = f"Exception during send: {e}"
            logger.error(f"❌ {error_msg}")
            
            return EmailResult(
                success=False,
                error=error_msg
            )
    
    def send_template_email(
        self,
        template_id: int,
        to: Union[List[EmailRecipient], EmailRecipient, str],
        params: Optional[Dict] = None,
        **kwargs
    ) -> EmailResult:
        """
        Send email using a Brevo template
        
        Args:
            template_id: Brevo template ID
            to: Recipient(s)
            params: Template parameters
            **kwargs: Additional parameters
            
        Returns:
            EmailResult
        """
        # Prepare recipients (same as send_email)
        def prepare_recipients(recipients):
            if isinstance(recipients, str):
                return [{"email": recipients}]
            elif isinstance(recipients, EmailRecipient):
                return [{"email": recipients.email, "name": recipients.name}]
            elif isinstance(recipients, list):
                result = []
                for r in recipients:
                    if isinstance(r, str):
                        result.append({"email": r})
                    elif isinstance(r, EmailRecipient):
                        result.append({"email": r.email, "name": r.name})
                return result
            return []
        
        payload = {
            "templateId": template_id,
            "to": prepare_recipients(to),
            "sender": {
                "email": self.sender_email,
                "name": self.sender_name
            },
            **kwargs
        }
        
        if params:
            payload["params"] = params
        
        try:
            logger.info(f"📧 Sending template email (ID: {template_id})")
            
            response = requests.post(
                f"{self.base_url}/smtp/email",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 201:
                data = response.json()
                message_id = data.get("messageId")
                logger.info(f"✅ Template email sent: {message_id}")
                
                return EmailResult(
                    success=True,
                    message_id=message_id,
                    response=data
                )
            else:
                error_msg = f"Template send failed: {response.status_code} - {response.text}"
                logger.error(f"❌ {error_msg}")
                
                return EmailResult(
                    success=False,
                    error=error_msg
                )
                
        except Exception as e:
            error_msg = f"Exception during template send: {e}"
            logger.error(f"❌ {error_msg}")
            
            return EmailResult(
                success=False,
                error=error_msg
            )
    
    def get_account_info(self) -> Dict:
        """Get account information"""
        try:
            response = requests.get(
                f"{self.base_url}/account",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def get_statistics(self) -> Dict:
        """Get email statistics"""
        try:
            response = requests.get(
                f"{self.base_url}/smtp/statistics",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    # Initialize client
    client = BrevoClient(config_path="/Users/cubiczan/.openclaw/workspace/config/brevo_config.json")
    
    # Test connection
    if not client.test_connection():
        print("❌ Connection test failed")
        exit(1)
    
    # Get account info
    account = client.get_account_info()
    print(f"✅ Account: {account.get('email')}")
    print(f"   Plan: {account.get('plan')}")
    print(f"   Credits: {account.get('credits')}")
    
    # Test sending email
    print("\n🧪 Testing email sending...")
    result = client.send_email(
        to="test@example.com",  # Replace with actual test email
        subject="Test from Brevo Client",
        html_content="<h1>Test Email</h1><p>This is a test from the Brevo client.</p>",
        text_content="Test Email: This is a test from the Brevo client."
    )
    
    if result.success:
        print("✅ Test email sent successfully!")
        print(f"   Message ID: {result.message_id}")
    else:
        print(f"❌ Test email failed: {result.error}")
