#!/usr/bin/env python3
"""
Test People Data Labs API integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.people_data_labs_integration import PeopleDataLabsEnrichment

def main():
    """Test the People Data Labs integration"""
    print('🔧 Testing People Data Labs API Integration')
    print('='*60)
    
    # Your API key
    api_key = 'fa5b2ea6dee53ad4f40b71bd51fc1d48d8c3efeea44faf342e7561be83772093'
    
    # Initialize
    pdl = PeopleDataLabsEnrichment(api_key=api_key)
    
    # Test connection
    print('\n🔌 Testing API connection...')
    if not pdl.test_connection():
        print('❌ API connection failed')
        return
    
    print('✅ API connection successful!')
    
    # Test company enrichment
    print('\n🏢 Testing company enrichment...')
    test_companies = ['Apple', 'Google', 'Microsoft']
    
    for company in test_companies:
        print(f'\n📊 Enriching {company}...')
        data = pdl.enrich_company(company_name=company)
        
        if data:
            print(f'✅ {company} data retrieved:')
            print(f'   Industry: {data.get("industry", "N/A")}')
            print(f'   Employees: {data.get("employee_count", "N/A")}')
            print(f'   Location: {data.get("location", {}).get("name", "N/A")}')
            print(f'   Website: {data.get("website", "N/A")}')
        else:
            print(f'❌ Failed to retrieve {company} data')
    
    # Test employee search
    print('\n👥 Testing employee search...')
    employees = pdl.get_company_employees('Apple', size=2)
    
    if employees:
        print(f'✅ Found {len(employees)} Apple employees:')
        for emp in employees:
            print(f'   - {emp.get("full_name", "Unknown")}: {emp.get("job_title", "Unknown")}')
    else:
        print('❌ No employees found')
    
    print('\n' + '='*60)
    print('🎯 People Data Labs Integration Test Complete!')
    print('='*60)
    print('\n📊 API Status: ✅ ACTIVE')
    print('🔑 API Key: Configured')
    print('📈 Rate Limit: 100 requests/day (free tier)')
    print('🎯 Ready for lead enrichment!')

if __name__ == '__main__':
    main()