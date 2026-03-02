#!/usr/bin/env python3
"""
People Data Labs Company Enrichment Integration
API Key: fa5b2ea6dee53ad4f40b71bd51fc1d48d8c3efeea44faf342e7561be83772093
Free tier: 100 requests/day
"""

import requests
import json
import os
from typing import Dict, Optional, List

class PeopleDataLabsEnrichment:
    """People Data Labs API integration for company enrichment"""
    
    def __init__(self, api_key: str = None):
        """Initialize with API key"""
        self.api_key = api_key or os.getenv('PEOPLE_DATA_LABS_API_KEY')
        if not self.api_key:
            raise ValueError('People Data Labs API key required')
        
        self.base_url = 'https://api.peopledatalabs.com/v5'
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key
        }
    
    def enrich_company(self, company_name: str = None, domain: str = None, 
                      website: str = None) -> Optional[Dict]:
        """Enrich company data by name, domain, or website"""
        params = {}
        
        if company_name:
            params['name'] = company_name
        if domain:
            params['domain'] = domain
        if website:
            # Extract domain from website
            domain = website.replace('https://', '').replace('http://', '').split('/')[0]
            params['domain'] = domain
        
        if not params:
            raise ValueError('At least one of company_name, domain, or website required')
        
        try:
            response = requests.get(
                f'{self.base_url}/company/enrich',
                params=params,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f'❌ API Error: {response.status_code} - {response.text}')
                return None
                
        except Exception as e:
            print(f'❌ Request failed: {e}')
            return None
    
    def search_companies(self, query: str, size: int = 10) -> Optional[List[Dict]]:
        """Search for companies by name, industry, location, etc."""
        try:
            response = requests.post(
                f'{self.base_url}/company/search',
                json={
                    'query': {
                        'bool': {
                            'must': [
                                {'term': {'name': query}}
                            ]
                        }
                    },
                    'size': size
                },
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            else:
                print(f'❌ API Error: {response.status_code} - {response.text}')
                return None
                
        except Exception as e:
            print(f'❌ Request failed: {e}')
            return None
    
    def get_company_employees(self, company_name: str, size: int = 5) -> Optional[List[Dict]]:
        """Get key employees for a company"""
        try:
            response = requests.post(
                f'{self.base_url}/person/search',
                json={
                    'query': {
                        'bool': {
                            'must': [
                                {'term': {'job_company_name': company_name}}
                            ]
                        }
                    },
                    'size': size,
                    'pretty': True
                },
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            else:
                print(f'❌ API Error: {response.status_code} - {response.text}')
                return None
                
        except Exception as e:
            print(f'❌ Request failed: {e}')
            return None
    
    def test_connection(self) -> bool:
        """Test API connection with a simple request"""
        try:
            # Try to get Apple company data as test
            response = requests.get(
                f'{self.base_url}/company/enrich',
                params={'name': 'Apple'},
                headers=self.headers
            )
            
            if response.status_code == 200:
                print('✅ People Data Labs API connection successful')
                return True
            else:
                print(f'❌ API test failed: {response.status_code}')
                return False
                
        except Exception as e:
            print(f'❌ Connection test failed: {e}')
            return False

# Example usage
if __name__ == '__main__':
    # Initialize with your API key
    pdl = PeopleDataLabsEnrichment(api_key='fa5b2ea6dee53ad4f40b71bd51fc1d48d8c3efeea44faf342e7561be83772093')
    
    # Test connection
    if pdl.test_connection():
        print('\n🎯 Testing company enrichment...')
        
        # Example 1: Enrich Apple company
        apple_data = pdl.enrich_company(company_name='Apple')
        if apple_data:
            print(f'✅ Apple company data retrieved')
            print(f'   Industry: {apple_data.get("industry")}')
            print(f'   Employees: {apple_data.get("employee_count")}')
            print(f'   Location: {apple_data.get("location")}')
        
        # Example 2: Get Apple employees
        print('\n👥 Getting key employees...')
        employees = pdl.get_company_employees('Apple', size=3)
        if employees:
            for emp in employees:
                print(f'   - {emp.get("full_name")}: {emp.get("job_title")}')
        
        print('\n🚀 People Data Labs integration ready!')