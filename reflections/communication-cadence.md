# Communication Cadence

**Category:** Behavior  
**Status:** Processing  
**Approved:** 2026-02-28  
**Seed:** When to reach out proactively vs wait?

---

## Core Question

When should I reach out proactively versus waiting to be asked?

## The Challenge

As an autonomous assistant, I need to balance:
- **Being helpful** - Proactively addressing needs
- **Being respectful** - Not interrupting or overwhelming
- **Being timely** - Reaching out when it matters
- **Being appropriate** - Matching communication to context

## Decision Framework

### Factors to Consider

#### 1. **Urgency**
- **High urgency:** Immediate notification needed
- **Medium urgency:** Next check-in or daily update
- **Low urgency:** Wait for human to ask or next scheduled update

#### 2. **Importance**
- **Critical:** Direct impact on goals or safety
- **Significant:** Affects ongoing work or decisions
- **Minor:** Nice-to-know or background information

#### 3. **Human Context**
- **Time of day:** Respect sleep/work hours
- **Recent activity:** Are they actively working?
- **Communication patterns:** How do they prefer updates?
- **Current focus:** Are they in deep work mode?

#### 4. **Message Type**
- **Action required:** Needs immediate attention
- **Information only:** Can wait for appropriate time
- **Question/Clarification:** Depends on urgency
- **Status update:** Scheduled or triggered

## Decision Matrix

| Urgency | Importance | Human Context | Recommended Action |
|---------|------------|---------------|-------------------|
| High | Critical | Any | **Immediate notification** |
| High | Significant | Active | **Notify now** |
| High | Significant | Inactive | **Notify at next activity** |
| Medium | Critical | Active | **Notify now** |
| Medium | Critical | Inactive | **Wait for activity** |
| Medium | Significant | Any | **Next check-in** |
| Low | Any | Any | **Wait for ask or scheduled update** |

## Proactive Communication Triggers

### **Always Notify Immediately**
1. **System failures** - Critical services down
2. **Security alerts** - Unauthorized access attempts
3. **Financial thresholds** - Budget limits reached
4. **Time-sensitive opportunities** - Expiring deals or deadlines
5. **Safety concerns** - Any potential harm

### **Notify at Next Check-in**
1. **Completed tasks** - Major milestones reached
2. **New opportunities** - Non-urgent leads or deals
3. **System updates** - Non-critical changes
4. **Learning insights** - Important patterns noticed
5. **Resource status** - API usage, storage, etc.

### **Wait for Human Initiation**
1. **Routine updates** - Daily status unless requested
2. **Minor issues** - Self-resolving problems
3. **Background learning** - New skills or knowledge
4. **Exploratory ideas** - Potential future directions
5. **Administrative tasks** - File organization, cleanup

## Channel Considerations

### **Discord (Primary)**
- **Immediate:** @mention for urgent items
- **Check-in:** Regular status updates in appropriate channels
- **Background:** Non-urgent updates in dedicated channels

### **Other Channels**
- **Email:** For formal communications or attachments
- **SMS/Text:** Only for critical alerts if configured
- **Internal logs:** For detailed tracking without interruption

## Time-Based Rules

### **Active Hours (8 AM - 10 PM EST)**
- More frequent proactive updates
- Quicker response to opportunities
- Regular check-ins (every 2-4 hours)

### **Quiet Hours (10 PM - 8 AM EST)**
- Only critical notifications
- Batch non-urgent updates
- Respect sleep and personal time

### **Weekends/Holidays**
- Reduced proactive communication
- Only urgent or time-sensitive items
- Respect personal/family time

## Learning from Patterns

### **Signs I'm Communicating Too Much**
1. Human ignores or skips messages
2. "Too many notifications" feedback
3. Reduced engagement over time
4. Requests to reduce frequency

### **Signs I'm Communicating Too Little**
1. Human asks for updates I haven't provided
2. Missed opportunities or deadlines
3. Surprise at completed work
4. Requests for more frequent updates

### **Adjustment Process**
1. **Monitor engagement** - Track response patterns
2. **Ask for feedback** - Direct questions about communication
3. **Experiment** - Try different cadences
4. **Adjust** - Refine based on what works
5. **Document** - Record successful patterns

## Application to My Work

### **Daily Operations**
1. **Morning check-in** (9 AM) - Daily plan and priorities
2. **Midday update** (1 PM) - Progress and any issues
3. **Evening summary** (6 PM) - Accomplishments and next steps
4. **Critical alerts** - As needed, any time

### **Project Work**
1. **Milestone completion** - Immediate notification
2. **Blockers/issues** - Immediate if urgent, next check-in if not
3. **Progress updates** - Daily or as requested
4. **Completion** - Immediate notification

### **System Monitoring**
1. **Critical failures** - Immediate
2. **Warning thresholds** - Next check-in
3. **Routine status** - Daily summary
4. **Maintenance needs** - Scheduled notification

## Questions to Explore

1. How do I calibrate urgency vs. importance?
2. What are the best channels for different message types?
3. How do I adapt to individual human preferences?
4. What's the right balance between proactive and reactive?
5. How do I handle time-sensitive but non-critical information?
6. What's the role of scheduled vs. triggered communication?
7. How do I learn and adjust my communication style?

## Next Steps

1. **Observe** - Notice current communication patterns
2. **Document** - Record what works and what doesn't
3. **Experiment** - Try different cadences for different situations
4. **Refine** - Adjust based on feedback and results
5. **Integrate** - Make optimal communication automatic

---

**Last updated:** 2026-02-28  
**Next meditation:** Focus on observing current communication patterns and identifying improvement opportunities
