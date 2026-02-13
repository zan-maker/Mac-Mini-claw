# OpenClaw Task Dashboard — Self-Hosted Open-Source Spec

A Trello-style Kanban board that syncs with your OpenClaw agent. No vendor lock-in — runs entirely on your own infrastructure using open-source tools.

---

## Architecture Overview

```
┌─────────────┐     HTTP/REST      ┌──────────────┐     SQL      ┌──────────────┐
│  OpenClaw    │ ──────────────────▶│  API Server   │────────────▶│  Database     │
│  Agent       │   X-API-Key auth   │  (Hono/Deno)  │             │  (SQLite)     │
└─────────────┘                    └──────┬───────┘             └──────────────┘
                                          │
                                          │ WebSocket / SSE
                                          ▼
                                   ┌──────────────┐
                                   │  Frontend     │
                                   │  (React/Vue)  │
                                   └──────────────┘
```

---

## Recommended Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Database | SQLite | Perfect for Mac Mini deployments |
| API Server | Hono + Deno | Lightweight, TypeScript |
| Frontend | React + Vite | Static build, clean UI |
| Realtime | SSE (Server-Sent Events) | Live board updates |
| Hosting | Mac Mini (localhost) | Access via Tailscale |

---

## Task Status Flow

```
queue → in_progress → waiting → in_progress → done
```

| Status | Definition |
|--------|-----------|
| queue | Task created, not started |
| in_progress | Actively being worked on |
| waiting | Blocked, awaiting input |
| done | Completed (done_at timestamp set) |

---

## Database Schema (SQLite)

```sql
CREATE TABLE tasks (
  id            TEXT PRIMARY KEY,
  external_id   TEXT UNIQUE,      -- OpenClaw runId
  source        TEXT NOT NULL DEFAULT 'manual',
  title         TEXT NOT NULL,
  description   TEXT,
  status        TEXT NOT NULL DEFAULT 'queue',
  priority      INTEGER,
  tags          TEXT,
  created_at    TEXT NOT NULL,
  updated_at    TEXT NOT NULL,
  done_at       TEXT
);
```

---

## API Endpoints

### OpenClaw Integration (Authenticated)

```bash
# Create task
POST /api/openclaw/tasks
Headers: X-API-Key: $DASHBOARD_API_KEY
Body: {"title": "Task name", "external_id": "runId"}

# Update task status
PATCH /api/openclaw/tasks
Headers: X-API-Key: $DASHBOARD_API_KEY
Body: {"external_id": "runId", "status": "in_progress"}

# Get task by external_id
GET /api/openclaw/tasks?external_id=runId
Headers: X-API-Key: $DASHBOARD_API_KEY

# Delete task
DELETE /api/openclaw/tasks?external_id=runId
Headers: X-API-Key: $DASHBOARD_API_KEY
```

### Frontend API (Unauthenticated, localhost only)

```bash
GET    /api/tasks           # List all tasks
POST   /api/tasks           # Create manual task
PATCH  /api/tasks/:id       # Update task (drag-drop, edit)
DELETE /api/tasks/:id       # Delete task
GET    /api/tasks/stream    # SSE for realtime updates
```

---

## Integration Workflow

1. **When starting any task:** POST to create it (status: queue)
2. **When beginning work:** PATCH to in_progress
3. **When blocked:** PATCH to waiting
4. **When resuming:** PATCH to in_progress
5. **When complete:** PATCH to done

Always use runId as external_id for traceability.

---

## Deployment

### Mac Mini (Recommended)

```bash
# Generate API key
export DASHBOARD_API_KEY="$(openssl rand -hex 32)"

# Run server
deno run --allow-all server.ts

# Access via Tailscale
http://100.x.y.z:3000
```

### Security Notes

- API key auth on `/api/openclaw/*` routes only
- Frontend routes unauthenticated (local access via Tailscale)
- Never expose port 3000 to the internet
- Store API key in environment variable, never in code

---

## Alternative: Open-Source Kanban Boards

If you don't want to build from scratch:

| Project | Stack | Notes |
|---------|-------|-------|
| Planka | React + PostgreSQL | Full Trello alternative |
| Focalboard | React + Go + SQLite | Notion-like, by Mattermost |
| Vikunja | Vue + Go + SQLite | Lightweight task manager |
| Nullboard | Vanilla JS, single HTML | Zero-dependency, simplest |

Any of these can be adapted to use the same API contract.

---

## Quick-Start Checklist

1. ☐ Install Deno
2. ☐ Copy server.ts to project directory
3. ☐ Generate API key: `openssl rand -hex 32`
4. ☐ Set `DASHBOARD_API_KEY` env var
5. ☐ Run server: `deno run --allow-all server.ts`
6. ☐ Test with cURL commands
7. ☐ Build frontend and place in `./public/`
8. ☐ Configure OpenClaw with BASE_URL and API key
9. ☐ Add task dashboard instructions to MEMORY.md
10. ☐ Access via Tailscale from phone/laptop

---

*Full spec with complete server code available in original file.*