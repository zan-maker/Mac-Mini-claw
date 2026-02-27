# WORKFLOW_AUTO.md - Automated Workflow Protocols

## Daily Startup Sequence

1. **Read Identity Files:**
   - `SOUL.md` - Who you are
   - `USER.md` - Who you're helping  
   - `MEMORY.md` - Long-term context (main sessions only)

2. **Check Recent Memory:**
   - `memory/YYYY-MM-DD.md` - Today's log
   - `memory/YYYY-MM-DD.md` - Yesterday's log (if exists)

3. **System Status Check:**
   - Verify API connections
   - Check cron job status
   - Review campaign progress
   - Monitor resource usage

4. **Heartbeat Processing:**
   - Read `HEARTBEAT.md` if exists
   - Execute periodic checks
   - Report status or `HEARTBEAT_OK`

## Email Outreach Workflow

### Campaign Execution
1. **Lead Generation** (9:00 AM daily)
   - Brave Search API for company discovery
   - Tavily API as backup
   - Supabase storage for leads

2. **Contact Enrichment** (Parallel)
   - Hunter.io for email finding (when credits available)
   - Alternative methods when exhausted

3. **Email Outreach** (2:00 PM daily)
   - Gmail SMTP primary (dual account redundancy)
   - AgentMail as backup (when API working)
   - Standard signature with Sam Desigan CC

4. **Campaign Tracking**
   - Supabase for delivery tracking
   - Response monitoring
   - Follow-up scheduling

## Multi-Agent Orchestration

### Sub-Agent Management
1. **Trade Recommender** - Stock market opportunities
2. **ROI Analyst** - Revenue generation analysis  
3. **Lead Generator** - SMB lead qualification

### Coordination Protocol
- Primary orchestrator (main agent) coordinates sub-agents
- Sub-agents report results to orchestrator
- Scheduled workflows: daily, weekly, monthly
- GitHub backup after significant changes

## Crisis Management

### Email Outage Protocol
1. **Primary:** Gmail SMTP (dual accounts)
2. **Backup:** AgentMail API (when working)
3. **Fallback:** Manual intervention required

### API Rate Limit Protocol
1. **Primary:** Brave Search API
2. **Backup:** Tavily API
3. **Fallback:** Manual search if both limited

### Cron Job Failure Protocol
1. Check timeout settings (increase if needed)
2. Verify script dependencies
3. Review error logs
4. Manual restart if persistent

## Performance Monitoring

### Daily Checks
- Token usage (every 30 minutes)
- API budget (daily)
- Email deliverability
- Lead generation volume

### Weekly Reports
- Campaign performance
- Revenue pipeline
- System health
- Improvement recommendations

## Compliance & Security

### Data Handling
- Private data stays private
- No exfiltration of sensitive information
- Secure storage of API keys
- Regular backup to GitHub

### User Communication
- Respect quiet hours (23:00-08:00)
- Quality over quantity in group chats
- Proactive but not intrusive
- Clear escalation for critical issues

---
*Last updated: 2026-02-26*
*Auto-generated from system protocols*