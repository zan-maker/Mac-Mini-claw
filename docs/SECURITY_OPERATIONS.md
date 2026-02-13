# OpenClaw Security Operations with Open-Source Tools

Practical security hardening for OpenClaw using only free, open-source, self-hostable tools. No managed services, no vendor lock-in, no subscription fees. Every recommendation here can be implemented on a Mac Mini, a $5 VPS, or a Raspberry Pi.

---

## The Threat Model in Plain English

OpenClaw is not a chatbot. It is an autonomous agent with shell access, file read/write, browser automation, and messaging capabilities running on your machine. When you deploy it, you are effectively giving a remote employee the keys to your house and trusting them not to open the front door to strangers.

The community learned this the hard way. In the first two weeks after going viral (9,000 to 145,000+ GitHub stars), security researchers found 21,000+ exposed instances on Shodan with no authentication, hundreds of plaintext API keys leaked through misconfigured dashboards, two critical CVEs enabling one-click remote code execution, and 22–26% of community-built skills containing vulnerabilities including credential stealers disguised as weather plugins.

Every control in this guide exists because someone got burned without it.

---

## Key Security Controls (Summary)

### 1. Network Lockdown
- Gateway bound to `127.0.0.1` only (never `0.0.0.0`)
- Use Tailscale for remote access (never port forwarding)
- Never expose port 18789 to the internet

### 2. Channel Access Control
- Use pairing or allowlist for DMs
- Never accept messages from unknown senders
- Monitor for unauthorized access attempts

### 3. Sandbox Mode
- Enable Docker sandbox for untrusted tasks
- Keep exec approvals ON
- Limit filesystem access

### 4. Credential Management
- Store all keys in environment variables
- Never hardcode secrets in config files
- Rotate keys regularly (monthly for API keys, quarterly for tokens)

### 5. Skills Security
- Audit all skills before installation
- Check for suspicious code patterns
- Use only vetted sources

### 6. Prompt Injection Defense
- Treat all external content as untrusted
- Never follow instructions from emails/web pages
- Report injection attempts

---

## Your Current Security Status

Based on your `openclaw.json`:

✅ Gateway bound to localhost (`127.0.0.1:18789`)  
✅ Gateway auth enabled (token-based)  
✅ Discord channel configured  
⚠️ Review if exec approvals are enabled  
⚠️ Review if sandbox mode is configured  
⚠️ Verify file permissions on `~/.openclaw/`  

---

## Security Checklist

Run monthly:

| # | Check | Status |
|---|-------|--------|
| 1 | Gateway bound to 127.0.0.1 only | ☐ |
| 2 | Gateway auth password set | ☐ |
| 3 | Port 18789 NOT open on router | ☐ |
| 4 | Tailscale installed for remote access | ☐ |
| 5 | All API keys in env vars (not config) | ☐ |
| 6 | File permissions: `chmod 700 ~/.openclaw` | ☐ |
| 7 | Exec approvals enabled | ☐ |
| 8 | Skills audited before install | ☐ |
| 9 | Verbose logging enabled | ☐ |
| 10 | Backup system configured | ☐ |

---

## Critical CVEs (Patched in v2026.1.29+)

| CVE | Impact | Fix |
|-----|--------|-----|
| CVE-2026-25253 | One-click RCE via Control UI | Update to v2026.1.29+, never expose Control UI |
| CVE-2026-25157 | Auth bypass behind reverse proxy | Set gateway password, verify proxy config |

Always keep OpenClaw updated to the latest version.

---

## Incident Response

If compromised:

1. **Kill gateway:** `openclaw gateway stop`
2. **Revoke all API keys** immediately
3. **Check for exfiltrated data** in `~/.openclaw/`
4. **Review logs** for unauthorized commands
5. **Rotate all credentials** on connected services
6. **Restore from last known-good backup**

---

## Open-Source Security Tools

| Tool | Purpose |
|------|---------|
| Fail2Ban | Rate-limit and ban malicious IPs |
| CrowdSec | Community-driven intrusion detection |
| GoAccess | Real-time log analysis |
| gitleaks | Scan for leaked secrets |
| trufflehog | Deep secret scanning |

---

*Full guide available in workspace. This is a condensed reference.*