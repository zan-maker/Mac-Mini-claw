# Enhanced Lead Generation Process v2.0

## Improvements Using New Tools

### Current vs Enhanced

| Step | Current | Enhanced |
|------|---------|----------|
| Lead Discovery | Basic web search | Serper + Zembra (Yellow Pages) + Google Maps |
| Data Enrichment | Hunter.io only | Hunter.io + ZeroBounce validation |
| Lead Storage | Markdown files | **Supabase database** |
| Lead Scoring | Simple points | AI-powered + behavioral scoring |
| Email Validation | None | **ZeroBounce** before sending |
| Outreach | Single email | **Multi-touch sequence** |
| Hot Lead Action | None | **Vapi phone call** + PDF report |
| Voice | None | **Edge-TTS** for voice messages |
| Tracking | Manual | **Supabase real-time** |

---

## Enhanced Daily Flow

### 8:00 AM - Lead Discovery (Enhanced)
```
┌─────────────────────────────────────────────────────────────┐
│                    LEAD DISCOVERY                           │
├─────────────────────────────────────────────────────────────┤
│ 1. Serper API → Google search for target industries        │
│ 2. Zembra API → Yellow Pages business listings             │
│ 3. Web Search → Recent funding, expansion news             │
│ 4. Dedupe → Check Supabase for existing leads              │
│                                                             │
│ NEW: 50-70 leads discovered daily (vs 15-20)               │
└─────────────────────────────────────────────────────────────┘
```

### 9:00 AM - Lead Enrichment & Scoring
```
┌─────────────────────────────────────────────────────────────┐
│                 LEAD ENRICHMENT                             │
├─────────────────────────────────────────────────────────────┤
│ 1. Hunter.io → Find email addresses                        │
│ 2. ZeroBounce → Validate emails (remove invalid)           │
│ 3. Calculate potential savings                             │
│ 4. Score lead (0-100)                                      │
│                                                             │
│ 5. Store in Supabase with:                                 │
│    - Lead data                                              │
│    - Enrichment data                                        │
│    - Score                                                  │
│    - Source                                                 │
│    - Created timestamp                                      │
└─────────────────────────────────────────────────────────────┘
```

### 10:00 AM - Lead Routing
```
┌─────────────────────────────────────────────────────────────┐
│                   LEAD ROUTING                              │
├─────────────────────────────────────────────────────────────┤
│ Score 80-100 (HOT):                                         │
│   → Immediate Vapi phone call                              │
│   → Generate PDF savings report                            │
│   → Priority email sequence                                │
│   → Discord alert                                          │
│                                                             │
│ Score 60-79 (WARM):                                         │
│   → Standard email sequence                                │
│   → Add to nurture                                         │
│                                                             │
│ Score 40-59 (NURTURE):                                      │
│   → Weekly newsletter                                      │
│   → Monthly touch                                          │
│                                                             │
│ Score <40 (COLD):                                           │
│   → Monthly newsletter only                                │
└─────────────────────────────────────────────────────────────┘
```

### 2:00 PM - Outreach Execution
```
┌─────────────────────────────────────────────────────────────┐
│                 OUTREACH EXECUTION                          │
├─────────────────────────────────────────────────────────────┤
│ 1. Query Supabase for leads needing outreach               │
│ 2. ZeroBounce validate (again) before sending              │
│ 3. Generate personalized email with DeepSeek               │
│ 4. Send via AgentMail                                      │
│ 5. Update Supabase status                                  │
│                                                             │
│ FOR HOT LEADS:                                              │
│   - Attach PDF savings report                              │
│   - Schedule Vapi call if no response in 24h               │
└─────────────────────────────────────────────────────────────┘
```

---

## New Cron Jobs to Add

### 1. Hot Lead Voice Follow-up (11 AM)
Triggers Vapi calls for leads scored 80+ that haven't responded to email.

### 2. Lead Nurturing Sequence (10 AM)
Sends Day 4, 7, 14 follow-ups based on Supabase tracking.

### 3. Weekly Performance Report (Friday 5 PM)
Generates report from Supabase data, posts to Discord.

---

*Enhanced lead generation process v2.0*
