#!/usr/bin/env python3
"""Test NewsAPI and Tomba with provided API keys"""

import sys
sys.path.insert(0, '/Users/cubiczan/.openclaw/workspace')

from public_apis_integration import PublicAPIsIntegration

def test_newsapi():
    """Test NewsAPI with provided key"""
    print("📰 Testing NewsAPI...")
    
    apis = PublicAPIsIntegration()
    
    # Test 1: Get business news
    print("\n1️⃣ Getting business news...")
    news_data = apis.get_news(
        category="business",
        page_size=3
    )
    
    print(f"   Success: {news_data.get('success', False)}")
    print(f"   Total results: {news_data.get('total_results', 0)}")
    
    if news_data.get("success") and news_data.get("articles"):
        for i, article in enumerate(news_data["articles"][:2]):
            print(f"   {i+1}. {article.get('title', 'No title')[:60]}...")
    
    # Test 2: Search for specific topic
    print("\n2️⃣ Searching for 'AI' news...")
    search_data = apis.get_news(
        query="artificial intelligence",
        page_size=2
    )
    
    print(f"   Success: {search_data.get('success', False)}")
    print(f"   Total results: {search_data.get('total_results', 0)}")
    
    if search_data.get("success") and search_data.get("articles"):
        for i, article in enumerate(search_data["articles"][:2]):
            print(f"   {i+1}. {article.get('title', 'No title')[:60]}...")
    
    return news_data.get("success", False)

def test_tomba():
    """Test Tomba email finder with provided key"""
    print("\n📧 Testing Tomba Email Finder...")
    
    apis = PublicAPIsIntegration()
    
    # Test with a known domain
    print("\n1️⃣ Finding emails for 'openai.com'...")
    email_data = apis.find_email(
        domain="openai.com",
        full_name="Sam Altman"  # Optional
    )
    
    print(f"   Success: {email_data.get('success', False)}")
    print(f"   Emails found: {email_data.get('emails_found', 0)}")
    
    if email_data.get("success") and email_data.get("emails"):
        for i, email in enumerate(email_data["emails"][:3]):
            print(f"   {i+1}. {email.get('email', 'No email')} - {email.get('first_name', '')} {email.get('last_name', '')}")
    
    # Test with another domain
    print("\n2️⃣ Finding emails for 'tesla.com'...")
    email_data2 = apis.find_email(
        domain="tesla.com"
    )
    
    print(f"   Success: {email_data2.get('success', False)}")
    print(f"   Emails found: {email_data2.get('emails_found', 0)}")
    
    return email_data.get("success", False)

def main():
    print("🧪 Testing NewsAPI and Tomba with provided API keys...")
    print("="*60)
    
    # Test NewsAPI
    news_success = test_newsapi()
    
    print("\n" + "="*60)
    
    # Test Tomba
    tomba_success = test_tomba()
    
    print("\n" + "="*60)
    print("📊 RESULTS:")
    print(f"   NewsAPI: {'✅ SUCCESS' if news_success else '❌ FAILED'}")
    print(f"   Tomba: {'✅ SUCCESS' if tomba_success else '❌ FAILED'}")
    
    if news_success and tomba_success:
        print("\n🎉 BOTH APIS ARE WORKING PERFECTLY!")
        print("   NewsAPI: Ready for market sentiment analysis")
        print("   Tomba: Ready for B2B email finding")
    else:
        print("\n⚠️  Some APIs need attention")
    
    # Show call statistics
    apis = PublicAPIsIntegration()
    stats = apis.get_call_stats()
    print(f"\n📈 API calls today:")
    for api, calls in stats.items():
        if api != "date":
            print(f"   {api}: {calls} calls")

if __name__ == "__main__":
    main()