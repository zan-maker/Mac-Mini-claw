# OpenClaw Documentation Index

Reference guides for advanced OpenClaw configuration and operations.

---

## Quick Links

| Document | Description | When to Use |
|----------|-------------|-------------|
| [MODEL_ROUTING.md](MODEL_ROUTING.md) | Intelligent model selection (GLM-5 primary, Grok for deep research) | When you need to switch models or optimize costs |
| [SECURITY_OPERATIONS.md](SECURITY_OPERATIONS.md) | Security hardening with open-source tools | When setting up or reviewing security |
| [SECURITY_GUIDELINES.md](SECURITY_GUIDELINES.md) | Comprehensive security checklist and CVE details | Monthly security reviews |
| [TASK_DASHBOARD_SPEC.md](TASK_DASHBOARD_SPEC.md) | Self-hosted Kanban dashboard architecture | When setting up task tracking |
| [TASK_DASHBOARD_MEMORY_SYNC.md](TASK_DASHBOARD_MEMORY_SYNC.md) | How to permanently connect dashboard to memory | Critical for task tracking persistence |
| [PERSISTENT_MEMORY_GUIDE.md](PERSISTENT_MEMORY_GUIDE.md) | Memory configuration, compaction defense, backup | When configuring memory or preventing data loss |

---

## Your Current Model Stack

**Primary:** GLM-5 (Z.AI) — routine tasks, 80% of work  
**Deep Research:** Grok-4 (xAI) — complex reasoning, debugging, architecture

**Switch to Grok-4:** `/model xai/grok-4` or say "Use Grok for this"  
**Switch back to GLM-5:** `/model zai/glm-5` or say "Switch back to GLM"

---

## Security Status

✅ Gateway bound to localhost  
✅ Gateway auth enabled  
⚠️ Review exec approvals and sandbox mode  
⚠️ Verify file permissions on `~/.openclaw/`  

Run monthly security checklist from [SECURITY_GUIDELINES.md](SECURITY_GUIDELINES.md).

---

## Task Dashboard

If setting up the self-hosted Kanban:

1. Read [TASK_DASHBOARD_SPEC.md](TASK_DASHBOARD_SPEC.md) for architecture
2. Follow setup instructions in the spec
3. **Critical:** Copy the memory entry from [TASK_DASHBOARD_MEMORY_SYNC.md](TASK_DASHBOARD_MEMORY_SYNC.md) to MEMORY.md
4. Verify integration with test tasks

---

## Memory Maintenance

- **Daily:** Agent writes to `memory/YYYY-MM-DD.md` automatically (if memoryFlush enabled)
- **Weekly:** Review MEMORY.md, remove outdated info
- **Monthly:** Audit memory files for unexpected entries
- **Backup:** Push to GitHub daily via cron

See [PERSISTENT_MEMORY_GUIDE.md](PERSISTENT_MEMORY_GUIDE.md) for detailed configuration.

---

## File Locations

```
~/.openclaw/
├── openclaw.json          # Main configuration
├── workspace/
│   └── docs/              # These reference guides
│       ├── MODEL_ROUTING.md
│       ├── SECURITY_OPERATIONS.md
│       ├── SECURITY_GUIDELINES.md
│       ├── TASK_DASHBOARD_SPEC.md
│       ├── TASK_DASHBOARD_MEMORY_SYNC.md
│       └── PERSISTENT_MEMORY_GUIDE.md
└── agents/
    └── main/
        ├── MEMORY.md      # Long-term curated memory
        ├── memory/        # Daily logs
        ├── SOUL.md        # Agent personality
        └── USER.md        # User preferences
```

---

*All guides customized for your deployment: Mac Mini · Discord · GLM-5 primary + Grok-4 deep research*
