# 🔒 API Key Rotation Guide

## 🚨 URGENT: Rotate These Exposed API Keys

Based on security audit, these keys need immediate rotation:

### 1. Brevo (Email)
**Key:** `[MOVED TO .ENV FILE - Check BREVO_API_KEY]`
**Status:** ✅ MOVED TO .ENV FILE
**Rotation Steps:**
1. Go to: https://app.brevo.com/settings/keys/api
2. Generate new API key
3. Update `.env` file: `BREVO_API_KEY=new_key`
4. Test email sending

### 2. OpenRouter (LLM)
**Key:** `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`
**Rotation Steps:**
1. Go to: https://openrouter.ai/keys
2. Create new key
3. Update `config/.env`: `OPENROUTER_API_KEY=new_key`
4. Test API calls

### 3. Cloudinary (Image Hosting)
**Credentials:**
- Cloud Name: `dbanogbek`
- API Key: `145887913816272`
- API Secret: `VADg7OEYVn2sow73euwPisvMoL0`
**Rotation Steps:**
1. Go to: https://cloudinary.com/console/settings/security
2. Regenerate API key and secret
3. Update `config/.env`:
   ```
   CLOUDINARY_CLOUD_NAME=new_name
   CLOUDINARY_API_KEY=new_key
   CLOUDINARY_API_SECRET=new_secret
   CLOUDINARY_URL=cloudinary://new_key:new_secret@new_name
   ```
4. Test image upload

### 4. Stripe (Payments) - HIGH RISK
**Keys found in multiple files**
**Rotation Steps:**
1. Go to: https://dashboard.stripe.com/apikeys
2. Restrict old keys, create new ones
3. Update environment variables
4. Test payment flows

## 🔧 Secure Configuration Now Implemented

### New Secure System:
1. **Environment Variables Only**
   - All API keys in `config/.env`
   - Never in code or config files
   - `.env` excluded from git

2. **Secure Configuration Loader**
   ```python
   from secure_config_loader import SecureConfig
   config = SecureConfig.load_all()
   ```

3. **Automatic Security Audits**
   ```bash
   python3 scripts/security_audit.py
   ```

## 🛡️ Best Practices Going Forward

### DO:
- Store API keys in environment variables
- Use the secure config loader
- Run security audits regularly
- Rotate keys every 90 days
- Use different keys for dev/prod

### DO NOT:
- Hardcode API keys in files
- Commit `.env` to version control
- Share API keys in messages
- Use the same key everywhere

## 📞 Emergency Contacts

If keys are compromised:
1. **Immediately** rotate all exposed keys
2. Monitor for unauthorized usage
3. Contact service providers
4. Review access logs

## 🔄 Automated Rotation Script

Run monthly key rotation:
```bash
./scripts/rotate_api_keys.sh
```

**Last Security Audit:** $(date)
**Next Rotation Due:** 90 days from $(date)
