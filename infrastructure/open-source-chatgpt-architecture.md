# Open-Source ChatGPT Clone Architecture

**Based on:** "Build Your Own ChatGPT with Lovable + n8n" tutorial
**Adapted:** All proprietary tools replaced with open-source alternatives

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Typebot)                          │
│              Chat interface, user interactions                  │
└──────────┬──────────────────────────────────┬───────────────────┘
           │                                  │
    ┌──────▼──────┐                    ┌──────▼──────┐
    │   WORKFLOW  │                    │  DATABASE   │
    │  (n8n self- │                    │ (Supabase)  │
    │   hosted)   │                    │             │
    │             │                    │ Chat logs   │
    │ • Webhooks  │                    │ Lead data   │
    │ • AI Agent  │◄───────────────────►│ Analytics   │
    │ • Logic     │                    │             │
    └──────┬──────┘                    └─────────────┘
           │
    ┌──────▼──────┐
    │    LLM      │
    │  (Ollama    │
    │  /DeepSeek) │
    │             │
    │ Llama 3     │
    │ Mistral     │
    │ DeepSeek    │
    └─────────────┘
```

---

## Tool Mapping: Proprietary → Open Source

| Original | Open Source Replacement | Status |
|----------|------------------------|--------|
| Lovable.dev | **Typebot** or **Appsmith** | 📋 Queued |
| n8n Cloud | **n8n (self-hosted)** | 📋 Queued |
| ChatGPT Plus | **DeepSeek API** or **Ollama** | ✅ API ready |
| SERP API | **Brave/Tavily/Serper** | ✅ Already integrated |

---

## Implementation Components

### 1. Frontend Options

#### Option A: Typebot (Recommended)
- **URL:** https://typebot.io
- **Type:** Open-source chatbot builder
- **Features:** Visual builder, logic flows, webhook integration
- **Deployment:** Docker or Railway
- **Best for:** Conversational UIs, lead magnets

#### Option B: Appsmith
- **URL:** https://appsmith.com
- **Type:** Low-code app builder
- **Features:** Drag-and-drop UI, API connections
- **Deployment:** Docker
- **Best for:** Full web apps, dashboards

#### Option C: ToolJet
- **URL:** https://tooljet.com
- **Type:** Low-code platform
- **Features:** Visual builder, enterprise ready
- **Deployment:** Docker
- **Best for:** Internal tools

### 2. Workflow Engine

#### n8n (Self-Hosted)
- **URL:** https://n8n.io
- **Type:** Workflow automation
- **Features:** 400+ integrations, visual builder
- **Deployment:** Docker
- **Cost:** $0 (self-hosted)

**Docker Setup:**
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### 3. LLM Options

#### Option A: DeepSeek API (Recommended)
- **API Key:** Already configured
- **Cost:** ~$0.27/1M tokens
- **Speed:** Fast
- **Quality:** High

#### Option B: Ollama (Local)
- **URL:** https://ollama.ai
- **Models:** Llama 3, Mistral, Gemma
- **Cost:** $0
- **Hardware:** GPU recommended

**Installation:**
```bash
# macOS
brew install ollama

# Pull model
ollama pull llama3

# Run API server
ollama serve
```

### 4. Database

#### Supabase
- **URL:** https://supabase.com
- **Features:** PostgreSQL, Auth, Real-time
- **Free Tier:** 500MB database
- **Use:** Store chat logs, lead data

**Alternative:** SQLite (local file)

### 5. Web Search APIs

Already integrated:
- Brave Search API ✅
- Tavily API ✅
- Serper API ✅

---

## Implementation Steps

### Step 1: Deploy n8n (Self-Hosted)

```bash
# Create n8n directory
mkdir -p ~/.openclaw/n8n

# Run n8n container
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.openclaw/n8n:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=secure123 \
  n8nio/n8n
```

Access at: http://localhost:5678

### Step 2: Configure AI Agent in n8n

1. Create new workflow
2. Add "On Webhook Call" trigger
   - Method: POST
   - Path: /chat
3. Add "AI Agent" node
   - Model: DeepSeek (via OpenAI-compatible API)
   - System Prompt: "You are a helpful assistant..."
4. Add web search tool (Brave/Tavily)
5. Add "Respond to Webhook" node

### Step 3: Deploy Typebot

```bash
# Docker Compose for Typebot
mkdir -p ~/.openclaw/typebot
cd ~/.openclaw/typebot

# Download docker-compose.yml
curl -o docker-compose.yml https://raw.githubusercontent.com/baptisteArno/typebot.io/main/docker-compose.yml

# Run
docker-compose up -d
```

Access at: http://localhost:3000

### Step 4: Connect Frontend to Backend

**Typebot Configuration:**
1. Create new bot
2. Add "Webhook" block
3. Set URL: http://localhost:5678/webhook/chat
4. Method: POST
5. Body: `{"message": "{{input}}"}`
6. Display response in chat

### Step 5: Add to OpenClaw

**n8n Workflow:**
- Webhook receives message
- AI Agent processes with DeepSeek
- Optional: Web search for live data
- Response sent back to frontend
- Log to Supabase

---

## Use Cases for Lead Generation

### 1. Lead Magnet Chatbot
- Ask qualifying questions
- Offer PDF report (WeasyPrint)
- Capture email → ZeroBounce validation
- Store in Supabase
- Trigger AgentMail follow-up

### 2. Business Advisor Bot
- Answer questions about selling business
- Qualify prospects (revenue, employees)
- Route to deal origination system
- Schedule consultation

### 3. Expense Reduction Bot
- Analyze company expenses
- Calculate potential savings
- Generate PDF report
- Request meeting

---

## File Structure

```
/workspace/
├── infrastructure/
│   ├── n8n/
│   │   └── workflows/
│   │       ├── chatbot-workflow.json
│   │       └── lead-capture-workflow.json
│   ├── typebot/
│   │   └── bots/
│   └── supabase/
│       └── migrations/
├── skills/
│   └── open-source-chatgpt/
│       └── SKILL.md
└── scripts/
    ├── start-n8n.sh
    └── start-typebot.sh
```

---

## Cost Comparison

| Component | Proprietary | Open Source |
|-----------|-------------|-------------|
| Frontend | Lovable ($20/mo) | Typebot ($0) |
| Workflow | n8n Cloud ($20/mo) | n8n self-hosted ($0) |
| LLM | ChatGPT Plus ($20/mo) | DeepSeek API ($0.27/1M tokens) |
| Database | Firebase (pay-as-you-go) | Supabase ($0 - 500MB) |
| **Total** | **$60+/month** | **~$1-5/month** |

---

## Next Steps

1. ✅ DeepSeek API - Already configured
2. 📋 Deploy n8n via Docker
3. 📋 Deploy Typebot via Docker
4. 📋 Set up Supabase project
5. 📋 Create n8n chatbot workflow
6. 📋 Build Typebot frontend
7. 📋 Connect and test

---

*Open-source implementation of the Lovable + n8n ChatGPT tutorial*
