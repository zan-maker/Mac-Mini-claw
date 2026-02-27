# Nimbleway API Integration Guide

**API Key:** `5b98a2e870df43059dfe1c39a23468db2e63e4e830dc4902a23501bf22706a31`  
**Dashboard:** https://online.nimbleway.com/account-settings/api-keys  
**Status:** API key obtained, endpoints not yet discovered  
**Last Tested:** 2026-02-26 23:50 EST

---

## 📋 Overview

Nimbleway appears to be a web scraping/browser automation service (similar to Bright Data, ScrapingBee, etc.). The API key has been obtained but endpoints are not yet active or discovered.

## 🔍 Discovery Attempts

### **Tested Endpoints (All returned 404):**
- `https://api.nimbleway.com/v1/search`
- `https://api.nimbleway.com/api/v1/search`
- `https://api.nimbleway.com/v1/browser`
- `https://api.nimbleway.com/v1/execute`
- `https://api.nimbleway.com/v1/search/web`
- `https://api.nimbleway.com/v1/query`
- `https://api.nimbleway.com/health`
- `https://api.nimbleway.com/status`

### **Authentication Methods Tested:**
1. Bearer token in Authorization header
2. API key in URL parameter
3. Various content types and payload formats

### **Root Endpoint Response:**
- `https://api.nimbleway.com/` returns Swagger UI
- Swagger UI is JavaScript-based, no accessible JSON spec found
- No active API endpoints discovered

---

## 🎯 Expected Use Cases

Based on similar services, Nimbleway likely provides:

### **1. Web Search & Scraping**
- Google/Bing search results
- Website content extraction
- SERP (Search Engine Results Page) scraping

### **2. Browser Automation**
- Headless browser control
- JavaScript rendering
- Form filling & interaction
- Screenshot capture

### **3. Data Extraction**
- Structured data from websites
- E-commerce product data
- News/article content
- Social media data

### **4. Monitoring**
- Website change detection
- Price monitoring
- Availability tracking
- Content updates

---

## 🔧 Integration Plan (When API Becomes Active)

### **Phase 1: API Discovery & Testing**
```python
# Template for API testing
import requests

NIMBLEWAY_API_KEY = "5b98a2e870df43059dfe1c39a23468db2e63e4e830dc4902a23501bf22706a31"
NIMBLEWAY_BASE_URL = "https://api.nimbleway.com"  # TBD

def test_nimbleway_api():
    """Test Nimbleway API once endpoints are discovered"""
    headers = {
        "Authorization": f"Bearer {NIMBLEWAY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Test endpoints (update when discovered)
    endpoints = {
        "search": "/v1/search",
        "browser": "/v1/browser",
        "scrape": "/v1/scrape",
        "execute": "/v1/execute"
    }
    
    for name, endpoint in endpoints.items():
        url = f"{NIMBLEWAY_BASE_URL}{endpoint}"
        try:
            response = requests.post(url, headers=headers, json={"query": "test"}, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name} endpoint active: {url}")
                return url, name
        except:
            continue
    
    return None, None
```

### **Phase 2: Search Integration**
```python
def nimbleway_search(query, num_results=10, search_engine="google"):
    """Search using Nimbleway API"""
    payload = {
        "query": query,
        "num_results": num_results,
        "search_engine": search_engine,
        # Additional parameters TBD
    }
    
    response = requests.post(
        f"{NIMBLEWAY_BASE_URL}/v1/search",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Nimbleway API error: {response.status_code}")
```

### **Phase 3: Web Scraping Integration**
```python
def nimbleway_scrape(url, selectors=None):
    """Scrape website content using Nimbleway"""
    payload = {
        "url": url,
        "extract_rules": selectors or {
            "title": "h1",
            "content": "article",
            "links": "a[href]"
        },
        "wait_for": 2000,  # milliseconds
        "javascript": True
    }
    
    response = requests.post(
        f"{NIMBLEWAY_BASE_URL}/v1/scrape",
        headers=headers,
        json=payload,
        timeout=60
    )
    
    return response.json()
```

### **Phase 4: Browser Automation**
```python
def nimbleway_browser_script(script):
    """Execute browser automation script"""
    payload = {
        "script": script,
        "language": "javascript",  # or "python"
        "timeout": 30000
    }
    
    response = requests.post(
        f"{NIMBLEWAY_BASE_URL}/v1/browser/execute",
        headers=headers,
        json=payload,
        timeout=90
    )
    
    return response.json()
```

---

## 🛠️ For Mining Investor Use Cases

### **1. LinkedIn Profile Scraping**
```javascript
// Nimbleway browser script for LinkedIn
const script = `
async function scrapeLinkedInInvestors() {
    await page.goto('https://www.linkedin.com/search/results/people/?keywords=junior%20mining%20investment%20canada');
    
    // Scroll to load more results
    await autoScroll(page);
    
    const investors = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('li.reusable-search__result-container')).map(el => ({
            name: el.querySelector('.entity-result__title-text a')?.textContent?.trim(),
            title: el.querySelector('.entity-result__primary-subtitle')?.textContent?.trim(),
            company: el.querySelector('.entity-result__secondary-subtitle')?.textContent?.trim(),
            location: el.querySelector('.entity-result__tertiary-subtitle')?.textContent?.trim(),
            profileUrl: el.querySelector('.entity-result__title-text a')?.href
        }));
    });
    
    return investors;
}

function autoScroll(page) {
    return page.evaluate(async () => {
        await new Promise((resolve) => {
            let totalHeight = 0;
            const distance = 100;
            const timer = setInterval(() => {
                const scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;
                
                if (totalHeight >= scrollHeight) {
                    clearInterval(timer);
                    resolve();
                }
            }, 100);
        });
    });
}
`;
```

### **2. Mining News & Deal Monitoring**
```python
def monitor_mining_deals():
    """Monitor mining deal announcements"""
    sources = [
        "https://www.mining-journal.com/finance/news",
        "https://www.northernminer.com/category/finance/",
        "https://www.mining.com/category/finance/"
    ]
    
    deals = []
    for url in sources:
        result = nimbleway_scrape(url, {
            "articles": "article.post",
            "titles": "h2 a",
            "dates": "time",
            "summaries": "div.excerpt"
        })
        deals.extend(result.get("data", []))
    
    return deals
```

### **3. Conference Attendee Extraction**
```python
def extract_pdac_attendees():
    """Extract PDAC conference attendees"""
    return nimbleway_scrape("https://www.pdac.ca/convention/attendees", {
        "attendees": "table.attendee-list tr",
        "name": "td.name",
        "company": "td.company",
        "title": "td.title",
        "email": "td.email"
    })
```

---

## 📊 Integration with Existing Tools

### **Current Search Stack:**
1. **Tavily API** - AI-optimized search (`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`)
2. **Bright Data** - Web scraping (`ff572e99-0217-4d64-8ef2-768ff4fdd142`)
3. **Nimbleway** - Browser automation (API key obtained, endpoints TBD)

### **Use Case Allocation:**
| Tool | Best For | Status |
|------|----------|--------|
| **Tavily** | Quick research, fact-finding, AI-optimized results | ✅ Active |
| **Bright Data** | Large-scale scraping, data extraction, monitoring | ✅ Active (plan ready) |
| **Nimbleway** | Browser automation, JavaScript sites, interaction | ⏳ Awaiting API |

### **Fallback Strategy:**
```python
def smart_search(query, use_case):
    """Intelligent search routing based on use case"""
    if use_case == "quick_facts":
        return tavily_search(query)
    elif use_case == "data_extraction":
        return brightdata_scrape(query)
    elif use_case == "browser_automation":
        # Try Nimbleway first, fallback to alternatives
        try:
            return nimbleway_browser_search(query)
        except:
            return fallback_browser_search(query)
    else:
        return tavily_search(query)  # Default
```

---

## 🔍 Next Steps for API Activation

### **1. Check Dashboard Configuration**
- Log into https://online.nimbleway.com/
- Check API key status (active/inactive)
- Look for "API Documentation" or "Getting Started"
- Check billing/credits status

### **2. Contact Support**
- Email support@nimbleway.com
- Ask for API documentation
- Request endpoint information
- Verify API key activation

### **3. Monitor for Updates**
- Check email for welcome/onboarding
- Watch dashboard for API status changes
- Test endpoints weekly

### **4. Alternative Discovery**
- Search GitHub for "nimbleway" examples
- Check npm/pip for SDKs
- Look for community discussions

---

## 📁 Files Created

### **Test Scripts:**
- `scripts/test-nimbleway-api.py` - Basic API testing
- `scripts/explore-nimbleway-api.py` - Endpoint exploration
- `scripts/test-nimble-browser.py` - Browser automation patterns

### **Documentation:**
- `docs/NIMBLEWAY_API_INTEGRATION.md` - This guide

### **Integration Ready:**
- API key stored in memory
- Test scripts ready to run
- Use cases defined
- Integration patterns prepared

---

## ⚡ Quick Start (When API Active)

### **Step 1: Test Connection**
```bash
python3 scripts/test-nimbleway-api.py
```

### **Step 2: Update Configuration**
```python
# Update in config.py or environment variables
NIMBLEWAY_API_KEY = "5b98a2e870df43059dfe1c39a23468db2e63e4e830dc4902a23501bf22706a31"
NIMBLEWAY_BASE_URL = "https://api.nimbleway.com"  # Update if different
```

### **Step 3: Run Integration Tests**
```bash
python3 scripts/test-nimble-browser.py
```

### **Step 4: Implement Use Cases**
1. LinkedIn investor scraping
2. Mining news monitoring
3. Conference attendee extraction
4. Website change detection

---

## 📞 Support & Resources

### **Nimbleway Resources:**
- **Dashboard:** https://online.nimbleway.com/
- **API Keys:** https://online.nimbleway.com/account-settings/api-keys
- **Documentation:** https://docs.nimbleway.com/ (JavaScript-heavy)
- **Support:** support@nimbleway.com

### **Similar Services for Reference:**
- **Bright Data:** https://brightdata.com/
- **ScrapingBee:** https://www.scrapingbee.com/
- **ScraperAPI:** https://www.scraperapi.com/
- **Apify:** https://apify.com/

### **Internal Contacts:**
- **Primary:** Sam Desigan (sam@cubiczan.com)
- **Technical:** Zane (via OpenClaw system)

---

**Status:** Awaiting API activation/endpoint discovery  
**Priority:** Medium - Alternative tools available (Tavily, Bright Data)  
**Last Updated:** 2026-02-26 23:50 EST  
**Next Check:** Test endpoints in 7 days or upon notification