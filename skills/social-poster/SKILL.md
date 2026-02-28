# Social Poster Skill for OpenClaw

Post to Facebook and Instagram using Facebook Graph API.

## 🚀 Quick Start

### 1. Prerequisites
- Facebook Developer Account
- Facebook Page connected to Instagram Business Account
- App with `pages_manage_posts` and `instagram_content_publish` permissions

### 2. Configuration
Create `/Users/cubiczan/.openclaw/workspace/social_config.json`:
```json
{
  "access_token": "YOUR_TOKEN_HERE",
  "page_id": "YOUR_PAGE_ID",
  "instagram_id": "YOUR_INSTAGRAM_ID"
}
```

### 3. Get Credentials
1. **Access Token:** https://developers.facebook.com/tools/explorer/
2. **Page ID:** Check page settings or use Graph API
3. **Instagram ID:** Connect Instagram to Facebook Page, then get from API

## 📋 Commands

### Test Connection
```bash
python /Users/cubiczan/.openclaw/workspace/scripts/facebook_instagram_poster.py --test
```

### Get Page Info
```bash
python /Users/cubiczan/.openclaw/workspace/scripts/facebook_instagram_poster.py --page-info
```

### Post to Facebook
```bash
python /Users/cubiczan/.openclaw/workspace/scripts/facebook_instagram_poster.py --facebook "Your message here"
```

### Post to Instagram
```bash
python /Users/cubiczan/.openclaw/workspace/scripts/facebook_instagram_poster.py --instagram "Your caption" --image /path/to/image.jpg
```

## 🎯 OpenClaw Integration

### As a Skill
Add to OpenClaw skills directory and use via:
```bash
openclaw social-post --platform facebook --message "Hello from OpenClaw!"
```

### In Agent Sessions
```bash
# Post to Facebook
/social-post facebook "Your message"

# Post to Instagram  
/social-post instagram "Your caption" /path/to/image.jpg
```

### Cron Job Example
Create `/Users/cubiczan/.openclaw/workspace/scripts/daily_post.sh`:
```bash
#!/bin/bash
cd /Users/cubiczan/.openclaw/workspace
python scripts/facebook_instagram_poster.py --facebook "Daily update from OpenClaw! 🤖"
```

## 🔧 API Reference

### Required Permissions
- `pages_manage_posts` - Post to Facebook Page
- `pages_read_engagement` - Read page insights
- `instagram_basic` - Access Instagram account
- `instagram_content_publish` - Post to Instagram

### Endpoints Used
- `GET /me` - Test connection
- `GET /{page-id}` - Get page info
- `POST /{page-id}/feed` - Post to Facebook
- `POST /{page-id}/photos` - Post photo to Facebook
- `POST /{instagram-id}/media` - Create Instagram media
- `POST /{instagram-id}/media_publish` - Publish Instagram post

## 🖼️ Image Requirements

### Facebook
- **Formats:** JPG, PNG, GIF
- **Max Size:** 4MB
- **Aspect Ratio:** 1:1 to 16:9

### Instagram
- **Format:** JPG (recommended)
- **Size:** 1080x1080 pixels (square)
- **Max Size:** 8MB
- **Aspect Ratio:** 1:1 (square), 1.91:1 (landscape), 4:5 (portrait)

## 🚨 Troubleshooting

### Common Issues
1. **Invalid Token:** Token expired or missing permissions
2. **Page Not Found:** Incorrect page ID
3. **Instagram Not Connected:** Instagram not linked to Facebook Page
4. **Image Issues:** Wrong format or size

### Debugging
```bash
# Enable verbose logging
export SOCIAL_POSTER_DEBUG=1
python scripts/facebook_instagram_poster.py --test

# Check logs
tail -f /Users/cubiczan/.openclaw/workspace/logs/posts_*.json
```

## 📈 Monitoring

### Log Files
- `logs/posts_YYYY-MM.json` - Successful posts
- `logs/errors_YYYY-MM.json` - Failed posts

### Sample Log Entry
```json
{
  "timestamp": "2026-02-27T18:30:00",
  "platform": "facebook",
  "post_id": "123456789012345",
  "message": "Hello from OpenClaw!...",
  "image": "post.jpg",
  "status": "success"
}
```

## 🔄 Token Management

### Long-lived Tokens
1. Get short-lived token (2 hours)
2. Exchange for long-lived token (60 days)
3. Set up token refresh automation

### Auto-refresh Script
```python
# scripts/refresh_token.py
import requests

def refresh_token(app_id, app_secret, short_token):
    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token
    }
    response = requests.get(url, params=params)
    return response.json().get("access_token")
```

## 🎯 Best Practices

### 1. Rate Limiting
- Facebook: 200 posts per hour per page
- Instagram: 25 posts per day per account
- Implement delays between posts

### 2. Error Handling
- Retry failed posts (max 3 times)
- Log all errors for debugging
- Notify on persistent failures

### 3. Content Strategy
- Post at optimal times (9 AM, 1 PM, 7 PM)
- Mix content types (text, images, videos)
- Engage with comments

## 📚 Resources

### Documentation
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [OpenClaw Skills](https://docs.openclaw.ai/skills)

### Tools
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
- [Page ID Finder](https://findmyfbid.com/)

## 🆘 Support

### Getting Help
1. Check error logs in `/Users/cubiczan/.openclaw/workspace/logs/`
2. Test API connection with `--test` flag
3. Verify permissions in Facebook Developer Portal

### Common Solutions
- **Token expired:** Get new token from Graph API Explorer
- **Missing permissions:** Add required permissions in App Dashboard
- **Instagram not posting:** Ensure Business account is connected to Page

---

**Ready to post?** Start with:
```bash
python scripts/facebook_instagram_poster.py --test
```

Then update your config file with real credentials! 🚀