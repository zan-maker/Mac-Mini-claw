---
name: no-code-lead-scraper
description: "No-code API scraper methodology for B2B lead generation. Uses Stevesie HAR export technique to scrape Craigslist business-for-sale listings and Reddit discussions. Use for: (1) finding car washes, laundromats, small businesses for sale, (2) scraping Reddit for business discussions, (3) building custom lead lists without coding."
---

# No-Code Lead Scraper - Stevesie Methodology

Scrape B2B leads from Craigslist and Reddit without coding using the HAR export technique.

## Stevesie Platform

### Craigslist Business Listings
**Source:** https://stevesie.com/apps/craigslist-api

**Use Cases:**
- Car washes for sale
- Laundromats for sale
- Small businesses for sale
- Equipment listings

**Method:**
1. Export HAR file from browser
2. Upload to Stevesie
3. Get instant API endpoint
4. Query programmatically

### Reddit Business Discussions
**Source:** https://stevesie.com/apps/reddit-api

**Use Cases:**
- Business owner discussions
- "Selling my business" posts
- Industry-specific subreddits
- Competitor research

## Craigslist API - Direct

**Endpoint:** `http://craigslist.demoz.co/api/{city}/{category}/{page}`

**Categories for Business:**
- `biz` - Business for sale
- `car` - Cars/trucks (auto businesses)
- `lab` - Labor/moving (service businesses)

**Example:**
```
GET /api/phoenix/biz/1
```

## Business-for-Sale Targets

### High-Value Categories:
- Car washes
- Laundromats
- HVAC companies
- Plumbing businesses
- Electrical contractors
- Landscaping companies
- Pool service businesses
- Cleaning services

### Search Patterns:
```
Craigslist Query Examples:
- "car wash" business for sale
- "laundromat" - real estate
- "HVAC" business
- "established" - recurring revenue
- "absentee owner" - turnkey
```

## Reddit Lead Mining

### Target Subreddits:
- r/smallbusiness
- r/entrepreneur
- r/businessforsale
- r/sellmybusiness
- r/buyabusiness

### Search Patterns:
```
- "selling my" [industry]
- "looking to sell"
- "business broker recommendations"
- "valuation help"
```

## Integration with Lead Systems

### Workflow:
1. **Craigslist:** Daily scrape of top 20 metros for business listings
2. **Reddit:** Monitor target subreddits for seller intent
3. **Enrichment:** Cross-reference with Google Maps, Yelp
4. **Validation:** ZeroBounce email verification
5. **Outreach:** AgentMail sequences

### Output Format:
```json
{
  "source": "craigslist|reddit",
  "business_type": "car_wash",
  "location": "Phoenix, AZ",
  "asking_price": "$250,000",
  "contact": "seller@email.com",
  "intent_score": 85,
  "notes": "Established 15 years, absentee owner"
}
```

## Daily Cron Integration

Add to existing lead gen systems:
- Deal Origination (business sellers)
- Referral Engine (prospects)
- Expense Reduction (companies for sale = expense reduction opportunity)

## Rate Limits

- Craigslist: Be respectful, avoid scraping too fast
- Reddit: 60 requests/minute via API
- Stevesie: Check plan limits
