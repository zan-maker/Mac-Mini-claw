# Local Model Cost Optimization

## 🎯 Goal
Reduce API token costs by using local Ollama model for simple tasks while maintaining API for complex tasks.

## 🏗️ Architecture

### **Hybrid Model Routing**
```
Simple Tasks → Local Model (tinyllama:latest) → Free
Complex Tasks → API (DeepSeek/GLM-5) → Paid
```

### **Task Classification**

| Task Type | Model | Cost | Examples |
|-----------|-------|------|----------|
| **Simple** | Local (tinyllama) | Free | Heartbeat, monitoring, notifications |
| **Complex** | API (DeepSeek) | ~$0.001-0.01 | Research, analysis, email composition |

## 📊 Cost Savings Analysis

### **Current (API Only)**
- Heartbeat: 5 checks × $0.001 = $0.005
- Daily (30 checks): $0.15
- Monthly: $4.50

### **Hybrid (Local + API)**
- Local: 4 checks × $0 = $0
- API: 1 check × $0.001 = $0.001
- Daily (30 checks): $0.03
- Monthly: $0.90

### **Monthly Savings: $3.60 (80% reduction)**

## 🛠️ Implementation

### **1. Local Model Setup**
```bash
# Service management
./scripts/manage-local-model.sh start
./scripts/manage-local-model.sh status

# Test model
python3 scripts/use-local-model.py
```

### **2. Hybrid Heartbeat**
```bash
# Run hybrid check
python3 scripts/hybrid-heartbeat.py

# Output:
# Local model checks: 4 (free)
# API checks: 1 (cost: ~$0.001)
# Estimated savings: $0.004 this check
```

### **3. Cron Job Updates**

**Current heartbeat cron job** (to be updated):
- Runs every 30 minutes
- Uses API for all checks
- Cost: ~$0.005 per run

**New hybrid cron job:**
- Same schedule (every 30 min)
- Uses local model for simple checks
- Falls back to API when needed
- Cost: ~$0.001 per run (80% savings)

## 📁 Files Created

### **Configuration:**
- `config/local-model-config.json` - OpenClaw local model config
- `docs/HUNTER_IO_SETUP.md` - API key documentation

### **Scripts:**
- `scripts/setup-local-model.sh` - Complete setup script
- `scripts/use-local-model.py` - Local model client
- `scripts/hybrid-heartbeat.py` - Hybrid cost-optimized check
- `scripts/manage-local-model.sh` - Service management

### **Logs:**
- `logs/heartbeat-cost-savings.json` - Cost savings tracking

## 🔄 Cron Job Migration

### **Step 1: Test Hybrid Approach**
```bash
# Manual test
python3 /Users/cubiczan/.openclaw/workspace/scripts/hybrid-heartbeat.py
```

### **Step 2: Update Existing Cron Jobs**
Identify cron jobs that can use local model:
1. **Heartbeat checks** (already implemented)
2. **Token monitor** (simple status)
3. **API usage check** (budget monitoring)
4. **File backup notifications** (simple alerts)
5. **System status checks** (basic monitoring)

### **Step 3: Create New Hybrid Cron Jobs**
For each simple task, create a version that:
1. Tries local model first
2. Falls back to API if local fails
3. Logs cost savings

## 📈 Monitoring

### **Cost Savings Dashboard**
```json
{
  "timestamp": "2026-03-08T16:08:00",
  "local_checks": 4,
  "api_checks": 1,
  "estimated_savings": 0.004,
  "total_checks": 5
}
```

### **Monthly Report**
- Total checks: 1,500 (30/day × 50 days)
- Local checks: 1,200 (80%)
- API checks: 300 (20%)
- Cost: $0.90 (vs $4.50 API-only)
- Savings: $3.60 (80% reduction)

## 🚀 Next Steps

### **Immediate:**
1. ✅ Install local model (tinyllama:latest)
2. ✅ Create hybrid heartbeat script
3. ✅ Test cost savings

### **Short-term:**
1. Update token monitor cron job to use local model
2. Update API usage check to use local model
3. Create dashboard for cost savings visualization

### **Long-term:**
1. Add more local models for different task types
2. Implement smart routing based on task complexity
3. Expand to other cron jobs (lead gen, outreach, etc.)

## ⚠️ Considerations

### **Performance:**
- Local model: Slower but free
- API: Faster but costs money
- Tradeoff: Acceptable for non-time-critical tasks

### **Reliability:**
- Local model may fail/be unavailable
- Always have API fallback
- Monitor local model health

### **Quality:**
- Local model: Good for simple, structured responses
- API: Better for complex, nuanced tasks
- Match task complexity to model capability

## 💡 Optimization Tips

1. **Batch simple tasks** to single local model call
2. **Cache frequent checks** to avoid重复 calls
3. **Monitor model performance** and adjust routing
4. **Regularly update** local models for improvements
5. **Track actual costs** vs estimates for accuracy

---

**Last Updated:** 2026-03-08
**Status:** ✅ Hybrid heartbeat implemented and tested
**Next Action:** Update token monitor and API usage cron jobs
