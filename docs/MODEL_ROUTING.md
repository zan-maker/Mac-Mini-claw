# OpenClaw Model Routing (Customized)

Route thinking problems to **Grok (xAI)**, routine work to **Z.AI (GLM-5)**, and never burn expensive tokens on simple tasks.

---

## Your Current Model Stack

Based on your `openclaw.json` configuration:

| Tier | Model | Use Case | Context | Notes |
|------|-------|----------|---------|-------|
| **Primary** | **zai/glm-5** | Routine tasks, general work, conversations | 204.8K | Daily driver — handles 80% of tasks |
| **Deep Research** | **xai/grok-4** | Complex reasoning, debugging, multi-step analysis | 131K | Use for thinking-heavy tasks |
| **Research Alt** | **xai/grok-2** | Alternative research model | 128K | Fallback for deep research |
| **Fallbacks** | GLM variants | If primary models rate-limited | — | Auto-fallback configured |

---

## Model Selection Decision Tree

```
Is the task sensitive/confidential?
├── YES → Use local Ollama only (if available)
└── NO
    │
    Does it require multi-step reasoning, debugging, or architecture?
    ├── YES → Switch to Grok-4 (Tier 1: Thinking)
    │         /model xai/grok-4
    │         Or: "Use Grok for this — I need deep reasoning."
    └── NO
        │
        Is it a heartbeat, health check, or simple status?
        ├── YES → GLM-5 is fine — lightweight enough
        └── NO
            │
            Routine task → GLM-5 (default primary)
```

---

## When to Switch Models

### Switch to Grok-4 for:
- Multi-step debugging or troubleshooting
- Architectural decisions and system design
- Complex analysis with multiple variables
- Novel problem-solving with no clear precedent
- Mathematical proofs or formal logic
- Deep research requiring synthesis of many sources

**Command:** `/model xai/grok-4`  
**Or say:** "Switch to Grok for this task — I need deep reasoning."

### Stay on GLM-5 for:
- General conversations and quick questions
- Email drafting and summarization
- Simple tool calls and file operations
- Web browsing and information retrieval
- Routine scheduling and organization
- Most day-to-day agent interactions

### Example Usage

```
You: "Switch to Grok and debug why the commissioning script fails at step 3"
[Agent switches to xai/grok-4 and performs deep analysis]

You: "Switch back to GLM and draft an email about the meeting"
[Agent returns to zai/glm-5 for routine work]
```

---

## Manual Model Override

### During Conversation

```
/model xai/grok-4        # Switch to deep research
/model xai/grok-2        # Alternative research model
/model zai/glm-5         # Return to primary daily driver
/model zai/glm-4.7       # Alternative GLM variant
/model zai/glm-4.7-flash # Fastest GLM option
```

### System Prompt Addition (Optional)

Add to your SOUL.md or MEMORY.md:

```
## Model Awareness

You are currently running on GLM-5 (Z.AI) as the daily driver.

If you encounter a task that requires:
- Multi-step reasoning or debugging
- Architectural decisions
- Complex analysis with multiple variables
- Deep research requiring synthesis

Then suggest: "This task would benefit from Grok-4's reasoning capabilities. Should I switch?"
```

---

## Cost Optimization

Your current setup is already cost-optimized:

| Model | Input Cost | Output Cost | Best For |
|-------|-----------|-------------|----------|
| GLM-5 (Z.AI) | Low | Low | 80% of daily tasks |
| Grok-4 (xAI) | Moderate | Moderate | Complex reasoning |
| Grok-2 (xAI) | Moderate | Moderate | Alternative research |

**Key principle:** Use GLM-5 by default, switch to Grok only when you need deep thinking. The manual switch keeps you in control of when higher-cost models are used.

---

## Data Sovereignty Notes

Both Z.AI (GLM) and xAI (Grok) are external APIs:

| Data Classification | Routing Rule |
|---------------------|--------------|
| PUBLIC (general research) | Any model OK |
| INTERNAL (non-sensitive work) | GLM or Grok OK |
| CONFIDENTIAL (financials, contracts) | Local only or US-hosted |
| RESTRICTED (API keys, credentials) | Never send to any external API |

For sensitive work, consider:
- Keeping confidential data out of agent conversations entirely
- Using local models (Ollama) if available
- Reviewing what context gets sent to external APIs

---

## Model Aliases (Your Setup)

These aliases are configured in your system:

| Alias | Full Model | Use |
|-------|-----------|-----|
| `GLM` | `zai/glm-5` | Primary daily driver |
| `Grok` | `xai/grok-4` | Deep research |
| `Grok (Deep Research)` | `xai/grok-2` | Alternative research |

You can use aliases or full model IDs interchangeably.

---

## Quick Reference

**Default:** GLM-5 handles most tasks automatically

**Switch to Grok-4 when you need:**
- Deep analysis
- Complex debugging
- Architectural thinking
- Multi-step reasoning

**Switch back to GLM-5 for:**
- Routine work
- Quick questions
- Simple tasks
- General conversation

**Command:** `/model <model-name>` or just ask the agent to switch.

---

## Your Configuration

Current model settings from `openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "zai/glm-5"
      },
      "models": {
        "xai/grok-2": { "alias": "Grok (Deep Research)" },
        "openai/gpt-5.1-codex": { "alias": "GPT" },
        "xai/grok-4": { "alias": "Grok" },
        "zai/glm-5": { "alias": "GLM" }
      }
    }
  }
}
```

No changes needed — your setup already follows the intelligent routing pattern. Just remember to manually switch to Grok when you need deep reasoning.

---

*Customized for your deployment: GLM-5 (primary) + Grok-4 (deep research)*
