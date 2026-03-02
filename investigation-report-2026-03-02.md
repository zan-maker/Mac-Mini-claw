# Investigation Report: Failed Cron Jobs & GitHub Secret Alert
# Date: 2026-03-02

## 1. GitHub Secret Scanning Alert

**Issue:** GitHub detected an exposed API key in the repository
**Secret:** AgentMail API key (`am_us_6aa957b36fb69693140cb0787c894d90ec2e65ffe937049634b685b911c1ac14`)
**Location:** `/workspace/scripts/send-remaining-leads.sh`
**Status:** GitHub has blocked the secret

**Action Required:**
1. **Visit GitHub:** Go to the link in the system message to manage the secret
2. **Revoke Key:** If possible, revoke the exposed AgentMail API key
3. **Fix Code:** Move API keys to environment variables
4. **Clean History:** Use `git filter-branch` or BFG to remove from history

**Immediate Fix:**
```bash
# Replace hardcoded API key with environment variable
export AGENTMAIL_API_KEY="your_new_key_here"
```

## 2. Failed Cron Jobs

### A. Dorada Outreach Waves (SIGTERM failures)
**Issue:** One wave failing with SIGTERM signal
**Possible Causes:**
- Memory limit exceeded
- Timeout
- API rate limiting
- Script errors

**Investigation Steps:**
1. Check which specific wave is failing
2. Review script logs
3. Check memory usage
4. Verify API quotas

### B. Miami Hotels Outreach (Timing out)
**Issue:** Cron jobs timing out
**Possible Causes:**
- Network issues
- API timeouts
- Script taking too long
- Resource constraints

### C. Mining Lead Gen (Needs repurposing)
**Status:** Should be switched to enhanced expense reduction outreach

## 3. Tastytrade Automation

**Current Status:** Active (generated recommendations today at 8:00 AM)
**User Request:** "leave the Tastytrade automation for now"
**Interpretation:** Pause/disable the automation

**Action:** Disable Tastytrade cron job(s)

## 4. Other Issues from MEMORY.md

### A. API Key Exposure Risks
- AgentMail API key in scripts
- Tavily API key in memory/docs
- Bright Data API key documented
- Various other credentials

### B. Cron Job Maintenance Needed
- 31 active cron jobs
- Some need model specification fixes (`glm-5` → `zai/glm-5`)
- Regular health checks required

## Recommended Actions

### Immediate (Today):
1. **GitHub Secret:** Address the blocked secret via GitHub interface
2. **API Keys:** Move all hardcoded API keys to environment variables
3. **Tastytrade:** Disable the automation cron job
4. **Failed Jobs:** Identify and disable the failing Dorada wave

### Short-term (This Week):
1. **Cron Audit:** Review all 31 cron jobs for failures
2. **Error Logging:** Implement better error tracking
3. **Resource Monitoring:** Check memory/CPU usage
4. **API Quotas:** Verify all API limits and quotas

### Long-term:
1. **Secret Management:** Implement proper secret management (Vault, AWS Secrets Manager, etc.)
2. **Cron Monitoring:** Set up alerts for failed jobs
3. **Documentation:** Update cron job registry with current status
4. **Testing:** Add pre-production testing for cron scripts

## Files to Fix

1. `scripts/send-remaining-leads.sh` - Exposed AgentMail API key
2. `scripts/dorada-wave2-outreach.py` - May have similar issues
3. `scripts/expense-reduction-agentmail.py` - Check for exposed keys
4. All other scripts with hardcoded credentials

## Security Recommendations

1. **Never commit secrets** to version control
2. **Use environment variables** or secret managers
3. **Regularly rotate API keys**
4. **Monitor GitHub secret scanning alerts**
5. **Implement pre-commit hooks** to prevent secret commits

## Next Steps

1. User needs to visit GitHub link to unblock/manage the secret
2. I can help fix the code to use environment variables
3. We should audit all scripts for exposed credentials
4. Cron jobs need systematic review and debugging
