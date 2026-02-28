#!/usr/bin/env python3
"""
Public APIs Integration Wrapper
Unified interface for 50+ free APIs from https://github.com/public-apis/public-apis
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import requests

class PublicAPIsIntegration:
    """Unified wrapper for multiple free public APIs"""
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or "/Users/cubiczan/.openclaw/workspace/cache/public_apis"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # API configurations (add your keys here)
        self.api_configs = {
            # Finance & Trading
            "marketstack": {
                "base_url": "http://api.marketstack.com/v1",
                "api_key": None,  # Get from APILayer
                "free_tier": 1000,
                "cache_duration": 3600  # 1 hour
            },
            "alphavantage": {
                "base_url": "https://www.alphavantage.co/query",
                "api_key": "T0Z2YW467F7PNA9Z",  # Already have
                "free_tier": 25,
                "cache_duration": 3600
            },
            "coingecko": {
                "base_url": "https://api.coingecko.com/api/v3",
                "api_key": None,
                "free_tier": "unlimited",
                "cache_duration": 300  # 5 minutes
            },
            
            # Business & Leads
            "tomba": {
                "base_url": "https://api.tomba.io/v1",
                "api_key": "ta_hsrcgwy0fwj29bbxm0ar3dns0nc6e5p2151pg",  # PROVIDED!
                "free_tier": 50,
                "cache_duration": 604800  # 1 week
            },
            
            # Validation
            "numverify": {
                "base_url": "http://apilayer.net/api/validate",
                "api_key": None,  # Get from APILayer
                "free_tier": 100,
                "cache_duration": 86400  # 1 day
            },
            "mailboxlayer": {
                "base_url": "http://apilayer.net/api/check",
                "api_key": None,  # Get from APILayer
                "free_tier": 100,
                "cache_duration": 86400
            },
            
            # News
            "newsapi": {
                "base_url": "https://newsapi.org/v2",
                "api_key": "4eb2186b017a49c38d6f6ded502dd55b",  # PROVIDED!
                "free_tier": 100,
                "cache_duration": 900  # 15 minutes
            },
            
            # Weather
            "weatherstack": {
                "base_url": "http://api.weatherstack.com",
                "api_key": None,  # Get from APILayer
                "free_tier": 1000,
                "cache_duration": 1800  # 30 minutes
            },
            
            # Currency
            "currencyfreaks": {
                "base_url": "https://api.currencyfreaks.com/v2.0",
                "api_key": None,  # Sign up at currencyfreaks.com
                "free_tier": 1000,
                "cache_duration": 3600
            },
            "fixer": {
                "base_url": "http://data.fixer.io/api",
                "api_key": None,  # Get from APILayer
                "free_tier": 100,
                "cache_duration": 3600
            }
        }
        
        # Rate limiting
        self.call_stats = {}
        self._load_call_stats()
        
        # User agents
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]
    
    # ==================== FINANCE & TRADING APIS ====================
    
    def get_stock_price(self, symbol: str, api: str = "marketstack") -> Dict[str, Any]:
        """Get current stock price"""
        if api == "marketstack":
            return self._marketstack_get_quote(symbol)
        elif api == "alphavantage":
            return self._alphavantage_get_quote(symbol)
        else:
            return {"error": f"Unsupported API: {api}"}
    
    def get_crypto_price(self, coin_id: str, vs_currency: str = "usd") -> Dict[str, Any]:
        """Get cryptocurrency price from CoinGecko"""
        cache_key = f"crypto_{coin_id}_{vs_currency}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if self._check_cache(cache_file, 300):  # 5 minutes cache
            return self._load_cache(cache_file)
        
        try:
            url = f"{self.api_configs['coingecko']['base_url']}/simple/price"
            params = {
                "ids": coin_id,
                "vs_currencies": vs_currency,
                "include_market_cap": "true",
                "include_24hr_vol": "true",
                "include_24hr_change": "true"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "success": True,
                    "coin_id": coin_id,
                    "vs_currency": vs_currency,
                    "price": data.get(coin_id, {}).get(vs_currency, 0),
                    "market_cap": data.get(coin_id, {}).get(f"{vs_currency}_market_cap", 0),
                    "volume_24h": data.get(coin_id, {}).get(f"{vs_currency}_24h_vol", 0),
                    "change_24h": data.get(coin_id, {}).get(f"{vs_currency}_24h_change", 0),
                    "timestamp": datetime.now().isoformat(),
                    "source": "coingecko"
                }
                
                self._save_cache(cache_file, result)
                self._update_call_stats("coingecko")
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_forex_rate(self, from_currency: str, to_currency: str, 
                      api: str = "currencyfreaks") -> Dict[str, Any]:
        """Get foreign exchange rate"""
        if api == "currencyfreaks":
            return self._currencyfreaks_get_rate(from_currency, to_currency)
        elif api == "fixer":
            return self._fixer_get_rate(from_currency, to_currency)
        else:
            return {"error": f"Unsupported API: {api}"}
    
    # ==================== BUSINESS & LEAD APIS ====================
    
    def find_email(self, domain: str, full_name: str = None) -> Dict[str, Any]:
        """Find email addresses for a domain/name using Tomba"""
        cache_key = f"email_{domain}_{hash(full_name) if full_name else 'any'}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if self._check_cache(cache_file, 604800):  # 1 week cache
            return self._load_cache(cache_file)
        
        api_key = self.api_configs["tomba"]["api_key"]
        if not api_key:
            return {
                "success": False,
                "error": "Tomba API key not configured",
                "timestamp": datetime.now().isoformat()
            }
        
        try:
            url = f"{self.api_configs['tomba']['base_url']}/domain-search"
            params = {"domain": domain}
            
            if full_name:
                params["name"] = full_name
            
            headers = {
                "X-Tomba-Key": api_key,
                "User-Agent": self.user_agents[0]
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "success": True,
                    "domain": domain,
                    "full_name": full_name,
                    "emails_found": len(data.get("data", {}).get("emails", [])),
                    "emails": data.get("data", {}).get("emails", []),
                    "timestamp": datetime.now().isoformat(),
                    "source": "tomba"
                }
                
                self._save_cache(cache_file, result)
                self._update_call_stats("tomba")
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_company_info(self, domain: str) -> Dict[str, Any]:
        """Get company information from Clearbit"""
        cache_key = f"company_{domain}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if self._check_cache(cache_file, 86400):  # 1 day cache
            return self._load_cache(cache_file)
        
        api_key = self.api_configs["clearbit"]["api_key"]
        if not api_key:
            return {
                "success": False,
                "error": "Clearbit API key not configured",
                "timestamp": datetime.now().isoformat()
            }
        
        try:
            url = f"{self.api_configs['clearbit']['base_url']}/companies/find"
            params = {"domain": domain}
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "User-Agent": self.user_agents[0]
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "success": True,
                    "domain": domain,
                    "company_name": data.get("name", ""),
                    "description": data.get("description", ""),
                    "logo": data.get("logo", ""),
                    "website": data.get("domain", ""),
                    "location": data.get("location", ""),
                    "employees": data.get("metrics", {}).get("employees", 0),
                    "industry": data.get("category", {}).get("industry", ""),
                    "timestamp": datetime.now().isoformat(),
                    "source": "clearbit"
                }
                
                self._save_cache(cache_file, result)
                self._update_call_stats("clearbit")
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    # ==================== VALIDATION APIS ====================
    
    def validate_phone(self, phone_number: str, country_code: str = None) -> Dict[str, Any]:
        """Validate phone number using Numverify"""
        cache_key = f"phone_{hash(phone_number)}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if self._check_cache(cache_file, 86400):  # 1 day cache
            return self._load_cache(cache_file)
        
        api_key = self.api_configs["numverify"]["api_key"]
        if not api_key:
            return {
                "success": False,
                "error": "Numverify API key not configured",
                "timestamp": datetime.now().isoformat()
            }
        
        try:
            url = self.api_configs["numverify"]["base_url"]
            params = {
                "access_key": api_key,
                "number": phone_number
            }
            
            if country_code:
                params["country_code"] = country_code
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "success": True,
                    "phone_number": phone_number,
                    "valid": data.get("valid", False),
                    "number": data.get("number", ""),
                    "local_format": data.get("local_format", ""),
                    "international_format": data.get("international_format", ""),
                    "country_prefix": data.get("country_prefix", ""),
                    "country_code": data.get("country_code", ""),
                    "country_name": data.get("country_name", ""),
                    "location": data.get("location", ""),
                    "carrier": data.get("carrier", ""),
                    "line_type": data.get("line_type", ""),
                    "timestamp": datetime.now().isoformat(),
                    "source": "numverify"
                }
                
                self._save_cache(cache_file, result)
                self._update_call_stats("numverify")
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def validate_email(self, email: str) -> Dict[str, Any]:
        """Validate email address using Mailboxlayer"""
        cache_key = f"email_validate_{hash(email)}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if self._check_cache(cache_file, 86400):  # 1 day cache
            return self._load_cache(cache_file)
        
        api_key = self.api_configs["mailboxlayer"]["api_key"]
        if not api_key:
            return {
                "success": False,
                "error": "Mailboxlayer API key not configured",
                "timestamp": datetime.now().isoformat()
            }
        
        try:
            url = self.api_configs["mailboxlayer"]["base_url"]
            params = {
                "access_key": api_key,
                "email": email,
                "smtp": 1,
                "format": 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "success": True,
                    "email": email,
                    "valid": data.get("format_valid", False),
                    "mx_found": data.get("mx_found", False),
                    "smtp_check": data.get("smtp_check", False),
                    "catch_all": data.get("catch_all", False),
                    "role": data.get("role", False),
                    "disposable": data.get("disposable", False),
                    "free": data.get("free", False),
                    "score": data.get("score", 0),
                    "timestamp": datetime.now().isoformat(),
                    "source": "mailboxlayer"
                }
                
                self._save_cache(cache_file, result)
                self._update_call_stats("mailboxlayer")
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    # ==================== NEWS APIS ====================
    
    def get_news(self, query: str = None, category: str = "business", 
                language: str = "en", country: str = "us", 
                page_size: int = 10) -> Dict[str, Any]:
        """Get news articles from NewsAPI"""
        cache_key = f"news_{hash(query) if query else category}_{language}_{country}_{page_size}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if self._check_cache(cache_file, 900):  # 15 minutes cache
            return self._load_cache(cache_file)
        
        api_key = self.api_configs["newsapi"]["api_key"]
        if not api_key:
            return {
                "success": False,
                "error": "NewsAPI key not configured",
                "timestamp": datetime.now().isoformat()
            }
        
        try:
            if query:
                url = f"{self.api_configs['newsapi']['base_url']}/everything"
                params = {
                    "q": query,
                    "pageSize": page_size,
                    "language": language,
                    "apiKey": api_key
                }
            else:
                url = f"{self.api_configs['newsapi']['base_url']}/top-headlines"
                params = {
                    "category": category,
                    "pageSize": page_size,
                    "language": language,
                    "country": country,
                    "apiKey": api_key
                }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                result =