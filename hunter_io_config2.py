#!/usr/bin/env python3
"""
Hunter.io API Client Configuration - Second API Key
"""

import requests
import time
from typing import Dict, List, Optional, Any

class HunterIOClient2:
    """Hunter.io API Client for second API key"""
    
    BASE_URL = "https://api.hunter.io/v2"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request with error handling"""
        if params is None:
            params = {}
        
        params['api_key'] = self.api_key
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "data": None,
                "errors": [f"Request error: {str(e)}"]
            }
    
    def domain_search(self, domain: str, limit: int = 10, **kwargs) -> Dict:
        """Search for emails by domain"""
        params = {
            "domain": domain,
            "limit": limit,
            **kwargs
        }
        return self._make_request("domain-search", params)
    
    def email_finder(self, domain: str, first_name: str, last_name: str) -> Dict:
        """Find email for specific person"""
        params = {
            "domain": domain,
            "first_name": first_name,
            "last_name": last_name
        }
        return self._make_request("email-finder", params)
    
    def email_verifier(self, email: str) -> Dict:
        """Verify email address"""
        params = {"email": email}
        return self._make_request("email-verifier", params)
    
    def get_account_info(self) -> Dict:
        """Get account information and credits"""
        return self._make_request("account")

# Create client with second API key
hunter_client2 = HunterIOClient2("601920a0b5d6b80f9131d4ae588065f694840081")