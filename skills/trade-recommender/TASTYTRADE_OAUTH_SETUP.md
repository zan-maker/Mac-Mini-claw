# Tastytrade OAuth Setup Guide

**Client ID:** `0c7b8898-a2f1-49bb-a23d-843e47b68631` ✅

---

## ⚠️ Additional Credentials Needed

OAuth requires **two** additional pieces of information:

### 1. Client Secret
- Found in your OAuth application settings
- Displayed when you created the application

### 2. Refresh Token
- Must be generated manually
- Never expires (can be reused indefinitely)

---

## 📝 How to Get Missing Credentials

### Step 1: Get Client Secret

1. **Visit:** https://my.tastytrade.com/app.html#/manage/api-access/oauth-applications
2. **Find** your application (Client ID: `0c7b8898-a2f1-49bb-a23d-843e47b68631`)
3. **Copy** the **Client Secret** (shown when you created it)

If you can't find it, you may need to create a new OAuth application.

---

### Step 2: Generate Refresh Token

1. **Stay on:** https://my.tastytrade.com/app.html#/manage/api-access/oauth-applications
2. **Click** "Manage" on your application
3. **Click** "Create Grant"
4. **Copy** the **Refresh Token** generated

This refresh token never expires and can be reused indefinitely.

---

## 🔧 Integration Code

Once you have both credentials, update the code:

### Python SDK

```python
from tastytrade import Session

# Create session with OAuth credentials
client_secret = "YOUR_CLIENT_SECRET"
refresh_token = "YOUR_REFRESH_TOKEN"

session = Session(client_secret, refresh_token)
```

### Bash Test

```bash
CLIENT_SECRET="your-client-secret"
REFRESH_TOKEN="your-refresh-token"

# Get session token
curl -X POST "https://api.tastyworks.com/oauth/token" \
  -H "Content-Type: application/json" \
  -d "{
    \"client_id\": \"0c7b8898-a2f1-49bb-a23d-843e47b68631\",
    \"client_secret\": \"$CLIENT_SECRET\",
    \"refresh_token\": \"$REFRESH_TOKEN\",
    \"grant_type\": \"refresh_token\"
  }"
```

---

## 📊 OAuth Flow Explanation

```
1. Client ID (public)
   ↓
2. Client Secret (private)
   ↓
3. Generate Refresh Token (one-time)
   ↓
4. Session Token (auto-refreshes every 15 min)
   ↓
5. API Requests
```

**Key Points:**
- Refresh token **never expires** (generate once, use forever)
- Session token expires in **15 minutes** (SDK auto-refreshes)
- Client ID is **public** (safe to share)
- Client Secret is **private** (never share)

---

## 🎯 What to Send Me

Please provide:
1. **Client Secret** - Found in OAuth app settings
2. **Refresh Token** - Generated via "Create Grant"

I'll update the integration and test the connection immediately.

---

## ✅ Ready to Use

Once you provide the credentials:
- Python SDK will connect automatically
- Session tokens refresh automatically
- Full API access enabled
- Ready for options recommendations

---

## 📚 Documentation Reference

- **OAuth Setup:** https://tastyworks-api.readthedocs.io/en/latest/sessions.html
- **Create App:** https://my.tastytrade.com/app.html#/manage/api-access/oauth-applications
- **Python SDK:** https://github.com/tastyware/tastytrade

---

**Status:** Awaiting client secret and refresh token
**Next Step:** Provide credentials → I'll test immediately
