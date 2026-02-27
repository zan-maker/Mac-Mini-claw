# Model Configuration

**Last Updated:** 2026-02-13

---

## Model Routing Strategy

### Primary Agent (Main)
**Model:** DeepSeek Chat
**Provider:** custom-api-deepseek-com
**Use Case:** Routine conversations, quick questions, daily tasks

**Characteristics:**
- Context: 128K tokens
- Cost: Lower than GLM-5
- Speed: Fast responses
- Best for: General chat, simple queries, coordination

**Alias:** `deepseek`
**Full ID:** `custom-api-deepseek-com/deepseek-chat`

---

### Sub-Agents

All sub-agents use **GLM-5** for larger context windows needed in research and analysis.

#### 1. Trade Recommender
**Model:** GLM-5
**Provider:** Z.AI
**Use Case:** Stock market analysis, trading opportunities, arbitrage detection

**Why GLM-5:**
- Context: 204.8K tokens
- Handles complex market research
- Multi-source analysis
- Evidence-based recommendations

---

#### 2. ROI Analyst
**Model:** GLM-5
**Provider:** Z.AI
**Use Case:** Revenue opportunity analysis, cost tracking, business evaluation

**Why GLM-5:**
- Large context for financial analysis
- Complex reasoning for ROI calculations
- Multi-factor evaluation
- Evidence grading framework

---

#### 3. Lead Generator
**Model:** GLM-5
**Provider:** Z.AI
**Use Case:** SMB lead qualification, prospect research, pipeline tracking

**Why GLM-5:**
- Research-heavy tasks
- Large context for company analysis
- Multi-source verification
- Complex qualification frameworks

---

## Switching Models Manually

### To DeepSeek (Primary)
```
/model deepseek
```
or
```
/model custom-api-deepseek-com/deepseek-chat
```

### To GLM-5 (Research)
```
/model glm
```
or
```
/model zai/glm-5
```

---

## When to Use Which Model

| Task Type | Model | Reason |
|-----------|-------|--------|
| Quick questions | DeepSeek | Fast, cheap |
| Daily coordination | DeepSeek | Routine tasks |
| Market research | GLM-5 | Large context needed |
| Financial analysis | GLM-5 | Complex reasoning |
| Lead research | GLM-5 | Multiple sources |
| Deep research | GLM-5 | Evidence synthesis |

---

## Cost Optimization

**DeepSeek** (Primary):
- Lower cost per token
- Optimized for routine work
- Good for high-volume daily use

**GLM-5** (Sub-Agents):
- Higher cost but larger context
- Reserved for research-heavy tasks
- Cost justified by complexity of work

**Estimated Savings:**
- Routine tasks: 60-70% cheaper on DeepSeek
- Research tasks: GLM-5 worth the cost for quality

---

## Configuration File

**Location:** `/Users/cubiczan/.openclaw/openclaw.json`

**Key Settings:**
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "custom-api-deepseek-com/deepseek-chat"
      }
    },
    "list": [
      {
        "id": "main",
        "model": "custom-api-deepseek-com/deepseek-chat"
      },
      {
        "id": "trade-recommender",
        "model": "zai/glm-5"
      },
      {
        "id": "roi-analyst", 
        "model": "zai/glm-5"
      },
      {
        "id": "lead-generator",
        "model": "zai/glm-5"
      }
    ]
  }
}
```

---

## Restart Required

After changing model configuration:
```bash
openclaw gateway restart
```

Or wait for next session start to pick up changes.

---

## API Endpoints

**DeepSeek:**
- Base URL: `https://api.deepseek.com`
- API Key: Configured in openclaw.json

**GLM-5 (Z.AI):**
- Base URL: `https://api.z.ai/api/paas/v4`
- API Key: Configured in auth profiles

---

**Version:** 1.0
**Strategy:** Cost-optimized routing (DeepSeek for routine, GLM-5 for research)
