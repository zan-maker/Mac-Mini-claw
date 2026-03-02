# Twitter Automation Skill for OpenClaw

**Based on:** antigravity/twitter-automation skill from skills.sh
**Adapted for:** OpenClaw with available tools
**Status:** Workflow implementation (requires Twitter API setup)

---

## Overview

This skill implements Twitter/X automation workflows adapted from the Rube MCP skill. It provides best practices for social media automation while acknowledging that full implementation requires Twitter API access.

## Prerequisites

### **For Full Implementation (Required)**
- Twitter Developer Account (https://developer.twitter.com/)
- Twitter API v2 Access (Essential or Elevated tier)
- OAuth 2.0 Client ID and Secret
- User authentication (for posting)

### **For Workflow Testing (Current)**
- OpenClaw with exec tool access
- Basic understanding of Twitter automation concepts

---

## Core Workflows (Adapted from Rube MCP Skill)

### 1. **Post Creation Workflow**

**Best Practices:**
- Always get authenticated user info first
- Upload media before posting (if needed)
- Respect 280 weighted character limit
- Handle duplicate posting prevention

**Implementation Steps:**
1. Get user profile (requires authentication)
2. Upload media if applicable
3. Create post with proper formatting
4. Verify post was created
5. Log post details for tracking

**Pitfalls to Avoid:**
- Posting is NOT idempotent (retrying creates duplicates)
- Media IDs must be numeric strings, not integers
- Character counting uses weighted system (some chars count as 2)

### 2. **Search and Monitoring Workflow**

**Best Practices:**
- Use Twitter search operators effectively
- Respect rate limits (450 requests/15 min for Essential)
- Handle pagination properly
- Filter results by time, engagement, etc.

**Search Operators:**
- `from:username` - Tweets from specific user
- `to:username` - Tweets to specific user  
- `is:retweet` / `-is:retweet` - Include/exclude retweets
- `has:media` - Tweets with media
- `lang:en` - Language filter

**Implementation Steps:**
1. Construct search query with operators
2. Make API request with proper parameters
3. Parse and filter results
4. Handle pagination if needed
5. Store/search results for analysis

### 3. **User Engagement Workflow**

**Best Practices:**
- Personalize interactions
- Space out engagements to avoid spam detection
- Track engagement metrics
- Follow/unfollow strategically

**Actions:**
- Like posts
- Retweet (with or without comment)
- Reply to posts
- Send direct messages
- Follow/unfollow users

---

## Implementation Options

### **Option A: Direct Twitter API (Recommended)**
```python
# Example using tweepy library
import tweepy

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Create a tweet
response = client.create_tweet(text="Hello Twitter!")
```

### **Option B: Inference.sh CLI**
```bash
# Requires inference.sh account and login
infsh app run x/post-tweet --input '{"text": "Hello from inference.sh!"}'
```

### **Option C: Rube MCP (If OpenClaw supports MCP)**
- Configure MCP server: `https://rube.app/mcp`
- Use tools: `TWITTER_CREATION_OF_A_POST`, `TWITTER_RECENT_SEARCH`, etc.

---

## OpenClaw Integration

### **Skill Structure**
```
twitter-automation/
├── SKILL.md (this file)
├── scripts/
│   ├── twitter-auth.py (OAuth flow)
│   ├── twitter-post.py (Create posts)
│   ├── twitter-search.py (Search tweets)
│   └── twitter-engage.py (Engagement actions)
└── config/
    └── twitter-config.example.json
```

### **Configuration File**
```json
{
  "api_key": "YOUR_API_KEY",
  "api_secret": "YOUR_API_SECRET",
  "access_token": "USER_ACCESS_TOKEN",
  "access_secret": "USER_ACCESS_SECRET",
  "bearer_token": "BEARER_TOKEN",
  "rate_limit_delay": 1.0,
  "max_posts_per_day": 50,
  "auto_follow_back": false
}
```

---

## Rate Limits & Best Practices

### **Twitter API v2 Rate Limits**
- **Essential Access:** 50,000 tweets/month, 10,000 posts/month
- **Elevated Access:** 2,000,000 tweets/month, 300,000 posts/month
- **Academic Research:** 10,000,000 tweets/month

### **Best Practices**
1. **Respect Limits:** Implement delays between requests
2. **Error Handling:** Handle 429 (Too Many Requests) gracefully
3. **Data Storage:** Cache results to minimize API calls
4. **Monitoring:** Track usage against limits
5. **Backoff Strategy:** Exponential backoff for rate limits

### **Safety Guidelines**
- Never automate spam or harassment
- Disclose automated accounts if required
- Respect user privacy and preferences
- Comply with Twitter Developer Agreement
- Implement opt-out mechanisms

---

## Workflow Examples

### **Daily Content Posting**
```bash
# 1. Curate content (from RSS, news, etc.)
# 2. Schedule posts (space out throughout day)
# 3. Add relevant hashtags
# 4. Include media when possible
# 5. Engage with comments
```

### **Lead Generation via Twitter**
```bash
# 1. Search for prospects by keywords/hashtags
# 2. Filter by engagement metrics
# 3. Extract contact information
# 4. Add to CRM/lead database
# 5. Engage with relevant content
```

### **Brand Monitoring**
```bash
# 1. Monitor brand mentions
# 2. Track competitor activity
# 3. Analyze sentiment
# 4. Respond to customer inquiries
# 5. Report insights
```

---

## Next Steps for Full Implementation

### **Phase 1: Setup (1-2 days)**
1. Apply for Twitter Developer Account
2. Create App and get API credentials
3. Set up OAuth 2.0 authentication
4. Test basic API calls

### **Phase 2: Core Features (3-5 days)**
1. Implement posting functionality
2. Add search and monitoring
3. Create engagement tools
4. Build rate limit handling

### **Phase 3: Integration (2-3 days)**
1. Integrate with OpenClaw skill system
2. Add configuration management
3. Create documentation
4. Test end-to-end workflows

### **Phase 4: Advanced Features (Ongoing)**
1. Add analytics and reporting
2. Implement scheduling
3. Create content curation
4. Add AI-powered features

---

## Current Status

**✅ Completed:**
- Workflow documentation from Rube MCP skill
- Best practices extraction
- Implementation options analysis
- OpenClaw integration plan

**⚡ In Progress:**
- Script creation for basic functionality
- Configuration template
- Rate limit handling

**🔧 Needs Setup:**
- Twitter Developer Account
- API credentials
- OAuth configuration
- Testing environment

---

## Files to Create

1. `scripts/twitter-auth.py` - OAuth authentication flow
2. `scripts/twitter-api.py` - Base API client with rate limiting
3. `scripts/twitter-post.py` - Post creation and management
4. `scripts/twitter-search.py` - Search and monitoring
5. `config/twitter-config.json` - Configuration template

---

**Note:** This skill provides the framework and best practices. Full functionality requires Twitter API access and proper authentication setup.
