# Apify Lead Generation Skill for OpenClaw

**Based on:** antigravity/apify-lead-generation skill from skills.sh
**Adapted for:** OpenClaw with available tools
**Status:** Workflow implementation (requires Apify account setup)

---

## Overview

This skill implements multi-platform lead generation using Apify Actors. Apify provides pre-built scraping tools (Actors) for platforms like Google Maps, Instagram, TikTok, Facebook, LinkedIn, and more. This skill enables automated lead discovery, enrichment, and data extraction at scale.

## Prerequisites

### **For Full Implementation (Required)**
- Apify Account (https://apify.com/)
- Apify API Token
- Understanding of target platforms and data needs
- Compliance with platform terms of service

### **For Workflow Testing (Current)**
- OpenClaw with exec tool access
- Basic understanding of web scraping concepts
- Data storage setup (Supabase, CSV, etc.)

---

## Core Workflows (Adapted from Apify Skill)

### 1. **Google Maps Lead Generation**

**Best Practices:**
- Use specific search queries (industry + location)
- Filter by business attributes (reviews, rating, years in business)
- Extract contact information (phone, website, email)
- Enrich with additional data sources

**Apify Actors:**
- `apify/google-maps-scraper` - Primary Google Maps scraper
- `apify/google-maps-scraper-v2` - Enhanced version with more features
- Custom configurations for specific industries

**Data Points to Extract:**
- Business name, address, phone
- Website, email (if available)
- Reviews, rating, review count
- Categories, services offered
- Hours of operation, photos
- Social media links

### 2. **Social Media Lead Generation**

**Platforms Supported:**
- **Instagram:** Business profiles, hashtag searches, location-based
- **TikTok:** Creator profiles, hashtag trends, location content
- **Facebook:** Business pages, groups, events
- **LinkedIn:** Company pages, professional profiles (with caution)

**Best Practices:**
- Respect platform rate limits
- Focus on business/creator accounts
- Extract publicly available information only
- Comply with platform terms of service

### 3. **Multi-Source Lead Enrichment**

**Workflow:**
1. Initial lead list from primary source (e.g., Google Maps)
2. Cross-reference with social media platforms
3. Enrich with additional data (email validation, company info)
4. Verify and deduplicate leads
5. Export to CRM/lead management system

**Enrichment Sources:**
- Email validation services (ZeroBounce, Hunter.io)
- Company databases (Clearbit, ZoomInfo alternatives)
- Social media profile aggregation
- Website scraping for additional contacts

---

## Implementation Options

### **Option A: Apify Platform (Recommended)**
```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")

# Run Google Maps scraper
run_input = {
    "searchStrings": ["restaurants New York"],
    "maxCrawledPlaces": 100,
    "language": "en",
}

run = client.actor("apify/google-maps-scraper").call(run_input=run_input)
```

### **Option B: Direct API Integration**
- Use Apify REST API directly
- Schedule recurring scrapes
- Webhook integration for real-time results
- Custom data processing pipelines

### **Option C: Hybrid Approach**
- Apify for data collection
- Custom scripts for processing/enrichment
- OpenClaw for workflow orchestration
- Existing tools (Tavily, Serper) for additional enrichment

---

## OpenClaw Integration

### **Skill Structure**
```
apify-lead-generation/
├── SKILL.md (this file)
├── scripts/
│   ├── apify-client.py (Base Apify client)
│   ├── google-maps-scraper.py (Google Maps workflow)
│   ├── social-media-scraper.py (Social media workflows)
│   ├── lead-enricher.py (Data enrichment)
│   └── export-leads.py (Export to various formats)
├── config/
│   └── apify-config.example.json
└── templates/
    ├── google-maps-queries.json
    └── industry-filters.json
```

### **Configuration File**
```json
{
  "apify_api_token": "YOUR_APIFY_API_TOKEN",
  "default_actor": "apify/google-maps-scraper",
  "rate_limit_delay": 2.0,
  "max_results_per_query": 1000,
  "data_storage": {
    "type": "supabase",  # or "csv", "json", "database"
    "supabase_url": "YOUR_SUPABASE_URL",
    "supabase_key": "YOUR_SUPABASE_KEY",
    "table_name": "leads"
  },
  "enrichment_services": {
    "email_validation": "zerobounce",  # or "hunter", "none"
    "zerobounce_key": "YOUR_ZEROBOUNCE_KEY",
    "company_data": "tavily",  # or "serper", "none"
    "tavily_key": "YOUR_TAVILY_KEY"
  }
}
```

---

## Rate Limits & Best Practices

### **Apify Platform Limits**
- **Free tier:** Limited runs and data storage
- **Paid plans:** Based on compute units and data points
- **Actor-specific:** Each actor has its own resource requirements

### **Platform Compliance**
1. **Google Maps:** Respect robots.txt, reasonable request rates
2. **Instagram/TikTok:** Use official APIs when available, respect TOS
3. **Facebook:** Business pages only, avoid personal data
4. **LinkedIn:** Strict terms, consider official Sales Navigator API

### **Best Practices**
1. **Data Quality:** Validate and clean extracted data
2. **Rate Limiting:** Implement delays between requests
3. **Error Handling:** Handle CAPTCHAs, blocks, and errors gracefully
4. **Storage:** Efficient data storage and deduplication
5. **Monitoring:** Track success rates and data quality

### **Legal & Ethical Considerations**
- Only scrape publicly available data
- Respect robots.txt and terms of service
- Implement opt-out mechanisms
- Store data securely and comply with regulations (GDPR, CCPA)
- Use for legitimate business purposes only

---

## Workflow Examples

### **Local Business Lead Generation**
```bash
# 1. Define target industries and locations
# 2. Run Google Maps scraper for each combination
# 3. Filter by business attributes (reviews, years open)
# 4. Enrich with website/email extraction
# 5. Validate emails and phone numbers
# 6. Export to CRM for outreach
```

### **Social Media Influencer Discovery**
```bash
# 1. Search Instagram/TikTok by hashtags/locations
# 2. Filter by follower count, engagement rate
# 3. Extract contact information (email in bio, website)
# 4. Enrich with additional platform data
# 5. Score leads based on relevance
# 6. Add to influencer database
```

### **Competitor Analysis**
```bash
# 1. Identify competitor businesses
# 2. Scrape their social media presence
# 3. Analyze customer reviews and sentiment
# 4. Monitor marketing activities
# 5. Extract pricing/service information
# 6. Generate competitive intelligence reports
```

### **Event-Based Lead Generation**
```bash
# 1. Identify upcoming industry events
# 2. Scrape attendee/exhibitor lists
# 3. Enrich with company/contact information
# 4. Create targeted outreach lists
# 5. Schedule pre/post-event campaigns
```

---

## Apify Actor Catalog

### **Primary Lead Generation Actors**
| Actor | Purpose | Key Features |
|-------|---------|--------------|
| `apify/google-maps-scraper` | Business listings | Reviews, contact info, categories |
| `apify/instagram-scraper` | Instagram profiles | Posts, followers, engagement |
| `apify/tiktok-scraper` | TikTok content | Videos, hashtags, user data |
| `apify/facebook-scraper` | Facebook pages | Posts, events, business info |
| `apify/linkedin-scraper` | Company profiles | Employees, posts, company data |

### **Supporting Actors**
| Actor | Purpose | Key Features |
|-------|---------|--------------|
| `apify/contact-info-scraper` | Email/phone extraction | Website scraping, contact forms |
| `apify/website-content-crawler` | General website scraping | Content extraction, link following |
| `apify/proxy-scraper` | Proxy management | Proxy rotation, anonymity |

### **Custom Configuration Examples**
```json
{
  "google_maps": {
    "searchStrings": ["coffee shops San Francisco"],
    "maxCrawledPlaces": 200,
    "includeReviews": true,
    "maxReviews": 5,
    "language": "en",
    "countryCode": "US"
  },
  "instagram": {
    "searchTerms": ["#smallbusiness"],
    "searchType": "hashtag",
    "resultsLimit": 100,
    "addParentData": true
  }
}
```

---

## Integration with Existing OpenClaw Setup

### **Current Lead Generation Stack**
- **Search:** Tavily API (primary), Serper (backup)
- **Email Validation:** ZeroBounce
- **Storage:** Supabase
- **Outreach:** AgentMail, Gmail SMTP
- **CRM:** Custom lead tracking

### **Apify Enhancement Areas**
1. **Deeper Business Data:** Google Maps provides richer business info
2. **Social Media Integration:** Connect leads with social presence
3. **Competitor Intelligence:** Monitor competitor activities
4. **Local Business Focus:** Better for location-based targeting
5. **Multi-Platform:** Single tool for multiple data sources

### **Workflow Integration**
```
Existing: Tavily Search → Email Validation → Supabase → Outreach
Enhanced: Apify Scraping → Tavily Enrichment → ZeroBounce → Supabase → Outreach
```

---

## Next Steps for Full Implementation

### **Phase 1: Setup (1 day)**
1. Create Apify account (https://apify.com/)
2. Generate API token
3. Test basic actor runs
4. Set up data storage integration

### **Phase 2: Core Features (3-5 days)**
1. Implement Google Maps scraping
2. Add social media scrapers
3. Create lead enrichment pipeline
4. Build export functionality

### **Phase 3: Integration (2-3 days)**
1. Integrate with existing OpenClaw lead generation
2. Add to cron job schedules
3. Create monitoring and reporting
4. Test end-to-end workflows

### **Phase 4: Advanced Features (Ongoing)**
1. Add more platform scrapers
2. Implement AI-powered lead scoring
3. Create real-time monitoring
4. Build predictive analytics

---

## Current Status

**✅ Completed:**
- Workflow documentation from Apify skill
- Best practices extraction
- Implementation options analysis
- OpenClaw integration plan

**⚡ In Progress:**
- Script creation for basic functionality
- Configuration template
- Actor configuration examples

**🔧 Needs Setup:**
- Apify account creation
- API token generation
- Testing with real data
- Integration with existing lead stack

---

## Files to Create

1. `scripts/apify-client.py` - Base Apify client with rate limiting
2. `scripts/google-maps-scraper.py` - Google Maps scraping workflow
3. `scripts/social-media-scraper.py` - Social media scraping
4. `scripts/lead-enricher.py` - Data enrichment pipeline
5. `config/apify-config.json` - Configuration template
6. `templates/industry-queries.json` - Pre-built search queries

---

## Cost Considerations

### **Apify Pricing**
- **Free tier:** Limited runs, good for testing
- **Personal plan:** $49/month, 100 compute units
- **Team plan:** $499/month, 1000 compute units
- **Enterprise:** Custom pricing

### **Compute Unit Estimates**
- Google Maps scraper: ~0.5 CU per 100 businesses
- Instagram scraper: ~0.3 CU per 100 profiles
- Data enrichment: ~0.1 CU per 100 leads

### **Cost Optimization**
- Batch similar queries together
- Cache results to avoid duplicate scraping
- Use efficient filtering to reduce data volume
- Monitor usage and adjust strategies

---

**Note:** This skill provides the framework and best practices. Full functionality requires Apify account setup and proper configuration. Always comply with platform terms of service and data protection regulations.
