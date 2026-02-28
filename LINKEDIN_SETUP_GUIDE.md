# 🔗 LinkedIn API Setup Guide

## 🎯 **QUICK START**

### **Step 1: Get Authorization Code**
```bash
cd /Users/cubiczan/.openclaw/workspace
python3 linkedin_integration.py
```

**Select option 1** - Get OAuth authorization URL
- Redirect URI: `https://localhost:8000` (default)
- Open in browser: Yes

### **Step 2: Authorize App**
1. LinkedIn will ask you to authorize the app
2. Grant `w_member_social` permission (posting access)
3. You'll be redirected to `https://localhost:8000?code=AUTHORIZATION_CODE`
4. **Copy the code parameter** from the URL

### **Step 3: Exchange Code for Token**
**Back in the script, select option 2**
- Paste the authorization code
- Use same redirect URI (`https://localhost:8000`)
- Enter Page ID if posting to company page

### **Step 4: Test Connection**
**Select option 3** - Test API connection
- Should show your LinkedIn profile

---

## 📋 **CREDENTIALS YOU PROVIDED:**

### **LinkedIn App Credentials:**
- **Client ID:** `78doynwi86n2js`
- **Client Secret:** `WPL_AP1.cxC0h4KruYgMBDFe.r9aIBg==`

### **What We Still Need:**
1. **Access Token** (via OAuth flow)
2. **Page ID** (optional - for company page posting)

---

## 🔧 **LINKEDIN APP CONFIGURATION**

### **Required App Settings:**
1. **OAuth 2.0 Settings:**
   - Redirect URLs: `https://localhost:8000`
   - Scopes: `w_member_social`
   - App permissions: Post on user's behalf

2. **API Products:**
   - Marketing Developer Platform
   - Share on LinkedIn
   - Sign In with LinkedIn

### **To Verify App Settings:**
1. Go to: https://www.linkedin.com/developers/apps
2. Select your app (`78doynwi86n2js`)
3. Check **Auth** tab for redirect URIs
4. Check **Products** tab for enabled APIs

---

## 🚀 **AUTOMATION READY**

### **Files Created:**
1. `linkedin_integration.py` - Complete LinkedIn API integration
2. `config/linkedin_tokens.json` - Token storage (after auth)
3. Updated `social_media_config.json` - LinkedIn configuration

### **Capabilities:**
- ✅ Post to personal LinkedIn profile
- ✅ Post to company pages
- ✅ Get user profile information
- ✅ List administered pages
- ✅ Token management and refresh

### **Integration with Social Media System:**
```python
from linkedin_integration import LinkedInIntegration

# Initialize
linkedin = LinkedInIntegration()

# Post to personal profile
linkedin.post_to_personal("AI-powered business automation is transforming industries! #AI #Automation")

# Post to company page
linkedin.post_to_page("New blog post: Lead Generation Strategies", page_id="12345678")
```

---

## 📝 **OAUTH FLOW DETAILS**

### **Authorization URL:**
```
https://www.linkedin.com/oauth/v2/authorization?
  response_type=code&
  client_id=78doynwi86n2js&
  redirect_uri=https://localhost:8000&
  scope=w_member_social&
  state=linkedin_auth_state
```

### **Token Exchange:**
```
POST https://www.linkedin.com/oauth/v2/accessToken
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=AUTHORIZATION_CODE&
redirect_uri=https://localhost:8000&
client_id=78doynwi86n2js&
client_secret=WPL_AP1.cxC0h4KruYgMBDFe.r9aIBg==
```

### **Access Token:**
- **Validity:** 60 days
- **Permissions:** `w_member_social` (posting)
- **Storage:** Encrypted in `linkedin_tokens.json`
- **Refresh:** Manual re-auth needed after expiry

---

## 🎯 **POSTING CAPABILITIES**

### **Personal Profile Posts:**
```python
# Text-only post
linkedin.post_to_personal("Sharing insights on AI automation #Tech")

# With visibility control
linkedin.post_to_personal("Internal update", visibility="CONNECTIONS")
```

### **Company Page Posts:**
```python
# Need page ID from LinkedIn URL
# URL: linkedin.com/company/12345678/
# Page ID: 12345678

linkedin.post_to_page(
    "Company announcement: New AI features!",
    page_id="12345678"
)
```

### **Post Types Supported:**
1. **Text posts** - Standard updates
2. **Article shares** - With links
3. **Image posts** - With media (needs additional setup)
4. **Video posts** - With video content

---

## 🔒 **SECURITY & COMPLIANCE**

### **Token Security:**
- Tokens stored in `config/linkedin_tokens.json`
- Never committed to GitHub
- Local storage only
- Manual refresh every 60 days

### **Posting Limits:**
- **Rate limits:** Varies by plan
- **Daily limits:** Check LinkedIn API docs
- **Best practice:** 2-3 posts per day
- **Optimal times:** 8:30 AM, 12:30 PM, 5:30 PM

### **Content Guidelines:**
- Professional tone only
- No spam or excessive posting
- Respect LinkedIn community guidelines
- Add value with each post

---

## 🚀 **INTEGRATION WITH AI SYSTEM**

### **AI-Powered Content:**
```python
from unified_ai_generator import UnifiedAIGenerator
from linkedin_integration import LinkedInIntegration

# Generate AI content (uses Google Gemini first)
ai = UnifiedAIGenerator()
linkedin = LinkedInIntegration()

# Generate LinkedIn post
result = ai.generate_content(
    "Create a professional LinkedIn post about AI automation for businesses"
)

# Post to LinkedIn
if result["success"]:
    linkedin.post_to_personal(result["content"])
```

### **Scheduled Posting:**
```python
# Can be integrated with cron jobs
# Daily LinkedIn posting at optimal times
# AI-generated content + automated posting
```

### **Multi-Platform Integration:**
- Same AI content for LinkedIn, Twitter, Facebook
- Platform-specific formatting
- Cross-posting with variations
- Performance tracking

---

## 🛠️ **TROUBLESHOOTING**

### **Common Issues:**

#### **1. "Invalid redirect_uri"**
- Check app settings: https://www.linkedin.com/developers/apps
- Ensure `https://localhost:8000` is in redirect URIs
- No trailing slashes

#### **2. "Invalid authorization code"**
- Code expires quickly (minutes)
- Get fresh code from OAuth flow
- Ensure same redirect_uri used

#### **3. "Insufficient scope"**
- Need `w_member_social` permission
- Re-authorize with correct scope
- Check app product permissions

#### **4. "Page not found"**
- Verify page ID from LinkedIn URL
- Ensure you're admin of the page
- Check page visibility settings

### **Debug Commands:**
```bash
# Test connection
python3 linkedin_integration.py
# Select option 3

# Check tokens
cat config/linkedin_tokens.json

# Test posting
python3 -c "
from linkedin_integration import LinkedInIntegration
l = LinkedInIntegration()
l.post_to_personal('Test post from automation system')
"
```

---

## 📊 **PERFORMANCE MONITORING**

### **Metrics to Track:**
1. **Post success rate** - % of successful posts
2. **Engagement rate** - Likes, comments, shares
3. **Token validity** - Days until expiry
4. **API response time** - Speed of operations

### **Logging:**
- All API calls logged
- Errors captured with details
- Performance metrics stored
- Daily summary reports

---

## 🎉 **READY FOR PRODUCTION**

### **Current Status:**
- ✅ LinkedIn integration script created
- ✅ OAuth flow implemented
- ✅ Token management system ready
- ✅ Configuration updated
- 🔧 **Awaiting:** Access token via OAuth

### **Next Steps:**
1. **Run setup script:** `python3 linkedin_integration.py`
2. **Get authorization code** (option 1)
3. **Exchange for access token** (option 2)
4. **Test posting** (option 6 or 7)
5. **Integrate with AI system**

### **Expected Timeline:**
- **Setup:** 5-10 minutes (OAuth flow)
- **Testing:** 2-3 minutes
- **Integration:** 5 minutes
- **Production:** Immediate after testing

---

## 📞 **SUPPORT**

### **LinkedIn Resources:**
- **API Documentation:** https://learn.microsoft.com/en-us/linkedin/
- **App Management:** https://www.linkedin.com/developers/apps
- **Community:** LinkedIn Developer Forums

### **System Integration Help:**
```bash
# Check system status
python3 update_social_credentials.py

# Test LinkedIn integration
python3 linkedin_integration.py

# View logs
ls -la logs/linkedin_*.log
```

### **Getting Help:**
1. Check error logs in `logs/` directory
2. Verify app settings in LinkedIn Developer Portal
3. Test with simple post first
4. Contact for persistent issues

---

## 🚀 **QUICK START COMMAND:**

```bash
cd /Users/cubiczan/.openclaw/workspace
python3 linkedin_integration.py
```

**Follow the prompts to:**
1. Get authorization URL
2. Authorize app in browser
3. Exchange code for token
4. Test connection
5. Start posting!

**Your LinkedIn automation is ready to go!** 🎉