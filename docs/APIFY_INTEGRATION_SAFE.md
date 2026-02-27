# Apify LinkedIn Search API Integration Guide

**API Token:** `[REDACTED - Set as environment variable]`  
**User ID:** `[REDACTED]`  
**Dashboard:** https://console.apify.com/  
**Status:** ✅ API connection successful  
**Plan:** FREE ($5 monthly credits)  
**Last Tested:** 2026-02-27 00:03 EST

---

## 📋 Overview

Apify is a web scraping and automation platform with specialized actors for LinkedIn data extraction. Perfect for mining investor research.

## 🔧 Setup Instructions

### **1. Set Environment Variables:**
```bash
# Set in your shell or .env file
export APIFY_API_TOKEN="your_api_token_here"
export APIFY_USER_ID="your_user_id_here"
```

### **2. Test Connection:**
```bash
python3 scripts/test-apify-linkedin-safe.py
```

### **3. Monitor Usage:**
```bash
python3 scripts/apify-usage-monitor-safe.py
```

## 🎯 Available Features (FREE Tier)

### **✅ Included:**
- **ACTORS** - Run built-in actors
- **STORAGE** - Store datasets and key-value stores
- **SCHEDULER** - Schedule actor runs
- **PROXY** - Limited proxy access
- **PROXY_RESIDENTIAL** - Residential proxies
- **PROXY_SERPS** - Search engine proxies
- **WEBHOOKS** - Webhook support
- **ACTORS_PUBLIC_ALL** - Access to public actors

### **❌ Not Included (FREE Tier):**
- **PROXY_EXTERNAL_ACCESS** - External proxy access
- **ACTORS_PUBLIC_DEVELOPER** - Selected public actors for developers

## 🛠️ Built-in Actors Available

### **1. web-scraper**
- **Purpose:** General web scraping
- **Use Case:** Mining conference websites, news sites
- **Input:** URLs, CSS selectors
- **Output:** Extracted data

### **2. puppeteer-scraper**
- **Purpose:** JavaScript-rendered page scraping
- **Use Case:** Dynamic websites, SPAs
- **Input:** URLs, interaction scripts
- **Output:** Rendered page content

### **3. cheerio-scraper**
- **Purpose:** Fast HTML parsing
- **Use Case:** Static websites, large-scale scraping
- **Input:** URLs, jQuery-like selectors
- **Output:** Parsed data

## 🎯 Mining Investor Research Plan

### **Phase 1: Data Collection**
- **Sources:** PDAC, Diggers & Dealers, Mining Journal, Northern Miner
- **Tools:** Apify web-scraper, puppeteer-scraper
- **Target:** 200+ investor mentions

### **Phase 2: Data Processing**
- **Tasks:** Extract names, titles, companies, match with database
- **Tools:** Python processing, fuzzy matching
- **Target:** Enrich 300+ existing contacts

### **Phase 3: LinkedIn Research**
- **Approach:** Manual search with collected data
- **Tools:** LinkedIn Sales Navigator, Boolean search
- **Target:** Find 100+ LinkedIn profiles

### **Phase 4: Database Enhancement**
- **Tasks:** Add LinkedIn URLs, enrich profiles, categorize
- **Target:** 500+ enhanced contacts ready for outreach

## 📊 Usage Monitoring

### **FREE Tier Limits:**
- **Monthly Credits:** $5
- **Actor Compute Units:** 625/month
- **Residential Proxy:** 20GB/month
- **SERP Requests:** 50,000/month
- **Data Retention:** 7 days

### **Cost Estimates:**
| Activity | Estimated Cost | Credits Used |
|----------|----------------|--------------|
| Web scraping (100 pages) | $0.50-$1.00 | 10-20% |
| Data processing | $1.00-$2.00 | 20-40% |
| Monthly monitoring | $1.00-$2.00 | 20-40% |
| **Total Monthly** | **$2.50-$5.00** | **50-100%** |

## 🚀 Quick Start

### **1. Test Connection:**
```python
import os
import requests

APIFY_API_TOKEN = os.environ.get("APIFY_API_TOKEN")

headers = {
    "Authorization": f"Bearer {APIFY_API_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.get(
    "https://api.apify.com/v2/users/me",
    headers=headers
)
```

### **2. Run Web Scraper:**
```python
# Example: Scrape mining conference site
actor_input = {
    "startUrls": [{"url": "https://www.pdac.ca/convention"}],
    "pageFunction": """async ({ page, request }) => {
        // Extract investor information
        return await page.evaluate(() => {
            return Array.from(document.querySelectorAll('.attendee')).map(el => ({
                name: el.querySelector('.name').textContent,
                company: el.querySelector('.company').textContent,
                title: el.querySelector('.title').textContent
            }));
        });
    }"""
}
```

### **3. Process Results:**
```python
def process_apify_results(results):
    """Process Apify scraping results"""
    contacts = []
    
    for item in results:
        contact = {
            "name": item.get("name"),
            "company": item.get("company"),
            "title": item.get("title"),
            "source": "Apify Scraping",
            "date_collected": datetime.now().strftime("%Y-%m-%d")
        }
        contacts.append(contact)
    
    return contacts
```

## 📁 Files Created

### **Safe Scripts (No API Keys):**
- `scripts/apify-usage-monitor-safe.py` - Usage monitoring
- `scripts/test-apify-linkedin-safe.py` - Connection testing
- `scripts/apify-practical-implementation-safe.py` - Implementation

### **Documentation:**
- `docs/APIFY_INTEGRATION_SAFE.md` - This guide
- `docs/APIFY_LINKEDIN_INTEGRATION.md` - Detailed guide (contains API keys - local only)

### **Data Files:**
- `mining-investors-enriched-20260227-000318.csv` - Enhanced database (500 contacts)
- `junior-mining-investors-enhanced-20260226-235710.csv` - Original enhanced database

## ⚡ Next Steps

### **Immediate:**
1. Set environment variables with API credentials
2. Test connection with safe scripts
3. Run usage monitor to check current usage
4. Plan first web scraping tasks

### **This Week:**
1. Scrape PDAC conference website for attendees
2. Extract mining news for investor mentions
3. Enrich existing database with new data
4. Monitor Apify usage and costs

### **Next 2 Weeks:**
1. Scale scraping to multiple mining sites
2. Implement data processing pipeline
3. Begin LinkedIn manual research
4. Launch outreach campaign with enriched data

## 🔒 Security Notes

### **API Key Protection:**
- Never commit API keys to version control
- Use environment variables or secret management
- GitHub push protection will block commits with keys
- Rotate keys periodically

### **Data Privacy:**
- Respect website terms of service
- Implement rate limiting
- Cache results to minimize requests
- Anonymize sensitive data

## 📞 Resources

### **Apify Documentation:**
- **Dashboard:** https://console.apify.com/
- **API Docs:** https://docs.apify.com/api/
- **Actor Docs:** https://docs.apify.com/actors/
- **Support:** support@apify.com

### **Mining Industry Resources:**
- **PDAC:** https://www.pdac.ca/
- **Diggers & Dealers:** https://www.diggersndealers.com.au/
- **Mining Journal:** https://www.mining-journal.com/
- **Northern Miner:** https://www.northernminer.com/

---

**Status:** Ready for implementation  
**Priority:** High - Valuable for investor research  
**Monthly Budget:** $5 (FREE tier) - monitor carefully  
**Next Action:** Set environment variables and test connection

*Last updated: 2026-02-27 00:03 EST*