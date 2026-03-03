#!/usr/bin/env python3
"""
Hunter.io API Configuration
API Key loaded from environment variable HUNTER_IO_API_KEY
"""

import os
import requests
import json
import time
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("HunterIO")

class HunterIOClient:
    """Client for Hunter.io API"""
    
    def __init__(self, api_key: str = None):
        # Get API key from environment variable if not provided
        self.api_key = api_key or os.environ.get("HUNTER_IO_API_KEY")
        if not self.api_key:
            raise ValueError("Hunter.io API key not provided. Set HUNTER_IO_API_KEY environment variable.")
        
        self.base_url = "https://api.hunter.io/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def domain_search(self, domain: str, limit: int = 100) -> Dict:
        """Search for emails associated with a domain"""
        url = f"{self.base_url}/domain-search"
        params = {
            "domain": domain,
            "api_key": self.api_key,
            "limit": limit
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching domain {domain}: {e}")
            return {"data": None, "errors": [str(e)]}
    
    def email_finder(self, domain: str, first_name: str = None, last_name: str = None) -> Dict:
        """Find email for a specific person"""
        url = f"{self.base_url}/email-finder"
        params = {
            "domain": domain,
            "api_key": self.api_key
        }
        
        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name
            
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error finding email for {first_name} {last_name} at {domain}: {e}")
            return {"data": None, "errors": [str(e)]}
    
    def email_verifier(self, email: str) -> Dict:
        """Verify an email address"""
        url = f"{self.base_url}/email-verifier"
        params = {
            "email": email,
            "api_key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error verifying email {email}: {e}")
            return {"data": None, "errors": [str(e)]}
    
    def get_account_info(self) -> Dict:
        """Get account information and remaining credits"""
        url = f"{self.base_url}/account"
        params = {"api_key": self.api_key}
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting account info: {e}")
            return {"data": None, "errors": [str(e)]}

# Initialize client with environment variable
try:
    hunter_client = HunterIOClient()
    logger.info("Hunter.io client initialized successfully")
except ValueError as e:
    logger.warning(f"Hunter.io client not initialized: {e}")
    hunter_client = None