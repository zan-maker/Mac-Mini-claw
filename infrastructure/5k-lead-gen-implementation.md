# $5K Lead Gen System - Implementation Guide

Based on n8n lead generation workflows and our current stack.

---

## 🎯 What a $5K/Month Lead Gen System Does

### Core Components
1. **Lead Discovery** - Find prospects automatically
2. **Data Enrichment** - Get contact info
3. **Lead Qualification** - Score and filter
4. **Personalized Outreach** - AI-generated emails
5. **Follow-up Automation** - Sequence nurturing
6. **Tracking & Reporting** - Pipeline visibility

---

## ✅ What We Already Have

| Component | Tool | Status |
|-----------|------|--------|
| Lead Discovery | Cron jobs + Web search APIs | ✅ Running |
| Data Enrichment | Zembra, Serper, ZeroBounce | ✅ Connected |
| Lead Storage | Supabase | ✅ Connected |
| Outreach | AgentMail (2 inboxes) | ✅ Ready |
| Voice AI | Vapi (2 phone lines) | ✅ Connected |
| Forms | Formbricks | ✅ Ready |
| Chatbots | Typebot | ✅ API configured |
| Workflows | n8n | ✅ Installed |
| TTS | Edge-TTS | ✅ Working |
| PDF Generation | fpdf2 | ✅ Working |

---

## 🔧 Implementations from $5K System

### 1. Google Maps Lead Scraper
**What it does:** Scrapes business data (name, website, phone, email) from Google Maps

**Our implementation:**
- Use **Serper API** (Google search results)
- Use **Zembra** (Yellow Pages)
- Store in **Supabase**
- Validate emails with **ZeroBounce**

**n8n Workflow:**
```
[Schedule Trigger] → [Serper Search] → [Parse Results] 
    → [Enrich with Zembra] → [Validate Email] → [Save to Supabase]
```

### 2. AI Email Generator
**What it does:** Generates personalized cold emails using AI

**Our implementation:**
- Use **DeepSeek API** (cheaper than OpenAI)
- Generate subject + body
- Send via **AgentMail**
- Track opens/clicks

**n8n Workflow:**
```
[New Lead in Supabase] → [DeepSeek Generate Email] 
    → [AgentMail Send] → [Update Status]
```

### 3. Lead Qualification Agent
**What it does:** Scores leads based on criteria

**Our implementation:**
- Employee count scoring
- Industry matching
- Challenge text analysis
- Store score in Supabase

**Already built:** `/workspace/scripts/lead-integration.py`

### 4. Form-based Lead Machine
**What it does:** Web form → lead capture → automated outreach

**Our implementation:**
- **Formbricks** form embedded on website
- Webhook to n8n
- Process → Save → Email
- Discord notification

**Template ready:** `/workspace/templates/formbricks-landing.html`

### 5. Voice Follow-up
**What it does:** Automated phone calls to qualified leads

**Our implementation:**
- **Vapi** phone lines ready
- Lead qualification agent created
- n8n triggers call for hot leads

---

## 🚀 New Implementations to Add

### 1. Apollo.io Integration (Lead Source)
```bash
# Apollo provides verified B2B contacts
# Free tier: 50 credits/month
```

### 2. LinkedIn Lead Gen
- Use n8n + Apollo to pull LinkedIn leads
- Enrich with company data
- Personalized outreach

### 3. Multi-Channel Sequences
```
Day 1: Email (AgentMail)
Day 3: Follow-up email
Day 7: Phone call (Vapi)
Day 14: Break-up email
```

### 4. Lead Scoring Model
```python
def score_lead(lead):
    score = 0
    
    # Company size
    if lead.employees >= 100: score += 30
    elif lead.employees >= 50: score += 20
    
    # Industry match
    if lead.industry in target_industries: score += 25
    
    # Engagement
    if lead.email_opened: score += 10
    if lead.clicked_link: score += 15
    
    # Intent signals
    if lead.challenge_mentioned: score += 20
    
    return score
```

---

## 📊 Daily Lead Gen Targets

| Source | Daily Target | Monthly |
|--------|-------------|---------|
| Wellness 125 | 15-20 | 300-400 |
| Expense Reduction | 15-20 | 300-400 |
| Deal Origination | 10-15 | 200-300 |
| Referral Engine | 10-15 | 200-300 |
| **Total** | **50-70** | **1000-1400** |

---

## 💰 Revenue Model

| Deal Type | Avg Value | Close Rate | Monthly Deals | Revenue |
|-----------|-----------|------------|---------------|---------|
| Wellness 125 | $2,500 | 2% | 6-8 | $15-20K |
| Expense Reduction | $5,000 | 1.5% | 4-6 | $20-30K |
| Deal Origination | $150,000 | 0.5% | 0-1 | $0-150K |
| Referral Fees | $3,500 | 2% | 4-6 | $14-21K |
| **Total** | - | - | - | **$50-220K/mo** |

---

## ✅ Action Items

### Immediate (Today)
1. [ ] Create Supabase leads table
2. [ ] Create Formbricks form
3. [ ] Start n8n and import workflow

### This Week
1. [ ] Build Google Maps scraper in n8n
2. [ ] Connect DeepSeek for email generation
3. [ ] Set up lead scoring
4. [ ] Create multi-touch email sequence

### This Month
1. [ ] Integrate Apollo.io for B2B leads
2. [ ] Build LinkedIn automation
3. [ ] Create voice call sequences
4. [ ] Build reporting dashboard

---

## 🛠️ n8n Workflows to Build

1. **Lead Scraper Workflow**
   - Google Maps → Enrich → Validate → Store

2. **Email Generator Workflow**
   - New Lead → AI Generate → Send → Track

3. **Qualification Workflow**
   - Form Submit → Score → Route → Notify

4. **Sequence Workflow**
   - Day triggers → Check status → Send next touch

5. **Voice Follow-up Workflow**
   - Hot Lead → Trigger Vapi call → Log result

---

*Implementation guide for $5K/month lead generation system*
