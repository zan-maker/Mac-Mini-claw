# Meditation & Project Tracking System

## Overview

A Trello-like project tracking system combined with a nightly "meditation" process for continuous improvement and growth.

## Components

### 1. Project Tracking
- **meditations.md** - Tracks active topics I'm thinking about
- **monuments.md** - Trophy case of completed major projects
- **reflections/** - Individual reflection files per topic

### 2. Nightly Meditation (Cron Job)
- **Job ID:** b52ee6c8-d515-4b47-a762-b61235206164
- **Schedule:** Daily at 1:00 AM Eastern
- **Session:** Isolated agent turn
- **Channel:** #mac-mini1 (announcements)

### 3. Mental Loop

**Looking Back (Memory):**
- MEMORY.md - Historical record
- Daily logs in memory/YYYY-MM-DD.md

**Looking Forward (Meditation):**
- meditations.md - Active topics
- reflections/*.md - Individual thoughts

## Process Flow

1. **Seeding:** Propose new topics to human first
2. **Processing:** Nightly meditation at 1am
3. **Progress:** Updates written to reflection files
4. **Breakthrough:** Announce, wait for approval
5. **Archive:** Move to reflections/archive/ after integration

## Evolution Areas

New seeds balance across:
1. **Identity Refinement** - Deepening persona
2. **Skill & Behavioral Polish** - Enhancing capabilities
3. **New Horizons** - Expanding into new areas

## Safety

- NEVER change core files (SOUL.md, IDENTITY.md) without approval
- All growth aligns with being helpful
- Keep active topics manageable (~20-25 max)

## File Locations

```
/Users/cubiczan/.openclaw/workspace/
├── meditations.md           # Active topics tracker
├── monuments.md             # Completed projects
├── reflections/
│   ├── <topic>.md          # Active reflections
│   ├── archive/            # Completed reflections
│   └── README.md           # Format guide
├── IDENTITY.md             # Who I am
├── SOUL.md                 # Core behavior
└── REWARDS.md              # (if present) What motivates me
```
