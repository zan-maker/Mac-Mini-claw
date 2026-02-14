# OpenClaw Memory Flush & Agent Memory Architecture

OpenClaw (formerly Clawdbot → Moltbot → OpenClaw) is an open-source, locally-running AI agent 
with 170K+ GitHub stars. Its defining innovation: treating context window limits as **persistence 
triggers** rather than compression problems.

**Source:** JIN, "Inside the Mind of AI: How Clawdbot's Memory Flush Solves the Context Window Crisis" (Medium, Feb 2026)

---

## 1. The Core Insight

> Bigger windows don't solve the compression problem; they only delay it.

Traditional approach: Context fills up → summarize → hope nothing critical is lost.

OpenClaw approach: Context fills up → **save everything critical to disk** → then summarize safely.

---

## 2. Two-Layer Memory Architecture

```
~/.openclaw/workspace/
├── MEMORY.md                   # Layer 2: Curated profile (long-term)
└── memory/
    ├── 2026-02-10.md           # Layer 1: Today's daily log (append-only)
    └── ...
```

- **Daily Notes:** Comprehensive activity logs — not summaries
- **Long-Term Memory (MEMORY.md):** Distilled understanding, preferences, lessons learned
- **Privacy:** MEMORY.md only loads in private/DM sessions, never in group contexts

---

## 3. Pre-Compaction Memory Flush

### How It Works

1. **Detection:** Token estimate crosses soft threshold
2. **Silent Agentic Turn:** System initiates invisible agent interaction
3. **Information Persistence:** Agent writes lasting notes to disk
4. **NO_REPLY Signal:** User never sees the flush happening
5. **Compaction Proceeds:** Only after info is safely on disk

### Configuration

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokensFloor": 20000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000,
          "systemPrompt": "Session nearing compaction. Store durable memories now.",
          "prompt": "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store."
        }
      }
    }
  }
}
```

---

## 4. Context Engineering Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| **Reduction** | Compress while preserving meaning | High recency, low density |
| **Offloading** | Move to external storage, keep references | High density, low recency |
| **Isolation** | Delegate to sub-agents | Large scope, specialized |
| **Memory Flush** | Persist to disk | Critical facts, any age |

---

## 5. Long-Term Memory Solutions

| System | Best For |
|--------|----------|
| **Mem0** | Managed service, best cost/accuracy tradeoff |
| **Letta** | Full control, self-hosted |
| **MemoryOS** | Structured multi-session workflows |
| **EverMemOS** | Research-grade |
| **OpenClaw Native** | Simple setups, full local control |

---

## 6. Known Gaps

### Manual Reset Gap (Issue #8185)
`/new` and `/reset` discard sessions without triggering Memory Flush.

**Workaround:** Before running `/new`, say: *"Save important context to memory before we reset."*

---

## 7. Best Practices

- Tell the agent explicitly: *"Remember that our API uses Rust"*
- Keep MEMORY.md curated — durable facts only
- Let daily logs be messy and comprehensive
- Never store credentials in memory files

---

## References

- [OpenClaw Memory Docs](https://docs.openclaw.ai/concepts/memory)
- [Mem0 Research Paper](https://arxiv.org/abs/2504.19413)
- [Anthropic Context Engineering Guide](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [GitHub Issue #8185](https://github.com/openclaw/openclaw/issues/8185)
