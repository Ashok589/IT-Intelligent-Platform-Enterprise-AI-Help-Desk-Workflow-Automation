# 🏢 Enterprise IT Intelligence Platform

> **Hybrid RAG · Agentic AI · LangGraph · Gemini 2.5 Flash**
>
> An MNC-grade, production-ready IT support intelligence platform that combines
> Hybrid Retrieval-Augmented Generation (RAG) with a multi-agent LangGraph workflow
> to deliver intelligent, context-aware answers from enterprise IT documentation,
> policies, and incident history — with full Human-in-the-Loop oversight.

---

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Prerequisites](#-prerequisites)
- [Quick Start — Local](#-quick-start--local)
- [Docker Deployment](#-docker-deployment)
- [Environment Configuration](#-environment-configuration)
- [Document Ingestion](#-document-ingestion)
- [Running Tests](#-running-tests)
- [Project Structure](#-project-structure)
- [Agent Capabilities](#-agent-capabilities)
- [Incident Management](#-incident-management)
- [Human-in-the-Loop](#-human-in-the-loop)
- [Audit & Compliance](#-audit--compliance)
- [IT Team Onboarding](#-it-team-onboarding)

---

## 🏗️ Architecture Overview

```
                    ┌─────────────────────────────────────────┐
                    │         ENTERPRISE IT PLATFORM           │
                    │         Streamlit Web Interface           │
                    └────────────────┬────────────────────────┘
                                     │
                    ┌────────────────▼────────────────────────┐
                    │            LANGGRAPH WORKFLOW            │
                    │                                          │
                    │  ┌──────────┐    ┌──────────────────┐  │
                    │  │  Memory  │───▶│    Supervisor    │  │
                    │  │  Node    │    │    (Router)      │  │
                    │  └──────────┘    └────────┬─────────┘  │
                    │                           │              │
                    │         ┌─────────────────┼──────────┐  │
                    │         │                 │          │   │
                    │    ┌────▼────┐  ┌────────▼──┐  ┌───▼──┤  │
                    │    │IT Know. │  │  Policy   │  │Inc.  │  │
                    │    │ Agent   │  │  Agent    │  │Agent │  │
                    │    └────┬────┘  └────────┬──┘  └───┬──┘  │
                    │         └────────┬────────┘         │    │
                    │                  │                   │    │
                    │         ┌────────▼────────┐          │    │
                    │         │  Human Review   │◀─────────┘    │
                    │         │  (HITL / Pause) │               │
                    │         └────────┬────────┘               │
                    │                  │                         │
                    │         ┌────────▼────────┐               │
                    │         │   Audit Node    │               │
                    │         │  (Compliance)   │               │
                    │         └─────────────────┘               │
                    └─────────────────────────────────────────┘
                                     │
                    ┌────────────────▼────────────────────────┐
                    │            HYBRID RAG PIPELINE           │
                    │                                          │
                    │  ChromaDB          BM25 Keyword Search   │
                    │  (Dense/Semantic)  (Sparse)               │
                    │         └──────────┬──────────┘          │
                    │                    │                      │
                    │              RRF Fusion                   │
                    │                    │                      │
                    │           Cross-Encoder Reranker          │
                    └─────────────────────────────────────────┘
```

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Hybrid RAG** | ChromaDB dense search + BM25 sparse retrieval + Cross-encoder reranking |
| 🤖 **Multi-Agent AI** | LangGraph supervisor routing to 4 specialist agents |
| 👤 **Human-in-the-Loop** | LangGraph interrupt-based pause for P1/P2 approval |
| 🎫 **Incident Management** | Full P1–P4 CRUD with SLA tracking and timeline |
| 📋 **Audit Trail** | Append-only compliance log for every AI interaction |
| 🧠 **Session Memory** | Multi-turn conversation context across turns |
| 📊 **Analytics Dashboard** | Query routing, incident KPIs, tool usage charts |
| 🔐 **Production Ready** | Docker, health checks, non-root user, volume persistence |

---

## 🛠️ Technology Stack

### AI / ML
| Component | Technology |
|-----------|------------|
| LLM | Google Gemini 2.5 Flash |
| Framework | LangChain |
| Orchestration | LangGraph |
| State Persistence | LangGraph SQLite Checkpointer |

### Retrieval (Hybrid RAG)
| Component | Technology |
|-----------|------------|
| Vector Store | ChromaDB |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Keyword Search | BM25Okapi |
| Reranking | Cross-Encoder (ms-marco-MiniLM-L-6-v2) |

### Application
| Component | Technology |
|-----------|------------|
| Web UI | Streamlit |
| Backend | Python 3.11+ |
| Data Persistence | JSON files + SQLite |
| Deployment | Docker / Docker Compose |

---

## 📦 Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.11+ |
| Docker | 24.0+ (for containerized deployment) |
| Google API Key | Gemini API access |
| RAM | ≥ 4 GB recommended |
| Storage | ≥ 2 GB for vectorstore + models |

---

## 🚀 Quick Start — Local

### 1. Clone / Navigate to Project

```bash
cd "Enterprise IT Intelligence Platform using Hybrid RAG and Agentic AI"
```

### 2. Create and Activate Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the example env file and edit it
copy .env.example .env     # Windows
cp .env.example .env       # Linux/macOS

# Edit .env with your API key:
# GOOGLE_API_KEY=your_gemini_api_key_here
```

### 5. Ingest Documents

```bash
python scripts/ingest_documents.py
```

### 6. Start the Platform

```bash
python startup.py
```

Open your browser at **http://localhost:8501**

---

## 🐳 Docker Deployment

### Build the Image

```bash
docker build -t enterprise-it-platform:1.0.0 .
```

### Run with Docker

```bash
docker run -d \
  --name enterprise-it-platform \
  -p 8501:8501 \
  --env-file .env \
  -v $(pwd)/DATA:/app/DATA \
  -v $(pwd)/vectorstore:/app/vectorstore \
  -v $(pwd)/enterprise_it_checkpoints.db:/app/enterprise_it_checkpoints.db \
  enterprise-it-platform:1.0.0
```

### Run with Docker Compose (Recommended for Production)

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop
docker-compose down
```

### Health Check

```bash
curl http://localhost:8501/_stcore/health
```

---

## ⚙️ Environment Configuration

Create a `.env` file in the project root:

```env
# ============================================
# REQUIRED
# ============================================

GOOGLE_API_KEY=your_gemini_api_key_here

# ============================================
# APPLICATION (optional — defaults shown)
# ============================================

APP_ENV=production
APP_HOST=0.0.0.0
APP_PORT=8501
DEBUG=false

# ============================================
# GEMINI LLM (optional)
# ============================================

GEMINI_MODEL=gemini-2.5-flash
GEMINI_TEMPERATURE=0.1

# ============================================
# HYBRID RAG (optional)
# ============================================

TOP_K_DENSE=5
TOP_K_SPARSE=5
TOP_K_RERANK=3

# ============================================
# INCIDENT SLA HOURS (optional)
# ============================================

SLA_P1_HOURS=1
SLA_P2_HOURS=4
SLA_P3_HOURS=24
SLA_P4_HOURS=72

# ============================================
# LOGGING (optional)
# ============================================

LOG_LEVEL=INFO
```

---

## 📥 Document Ingestion

Place enterprise documents in the appropriate `DATA/` sub-directories:

| Directory | Content Type |
|-----------|-------------|
| `DATA/it_sop/` | IT Standard Operating Procedures |
| `DATA/it_policies/` | Security, access, and compliance policies |
| `DATA/technical_docs/` | Network diagrams, runbooks, guides |
| `DATA/incident_reports/` | Historical incident post-mortems |

Supported formats: **PDF, TXT, Markdown (.md), DOCX**

### Ingest Commands

```bash
# Ingest all categories
python scripts/ingest_documents.py

# Ingest specific category only
python scripts/ingest_documents.py --category it_sop
python scripts/ingest_documents.py --category it_policies

# Preview without ingesting
python scripts/ingest_documents.py --dry-run

# Force re-ingest (overwrite existing)
python scripts/ingest_documents.py --force

# View current vectorstore stats
python scripts/ingest_documents.py --stats
```

---

## 🧪 Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run full test suite
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ -v --cov=SRC --cov-report=html

# Run only smoke tests (fast — no LLM required)
python -m pytest tests/test_graph_smoke.py -v

# Run specific module tests
python -m pytest tests/test_incident_manager.py -v
python -m pytest tests/test_audit_log.py -v
python -m pytest tests/test_session_memory.py -v
```

---

## 📁 Project Structure

```
Enterprise IT Intelligence Platform/
│
├── SRC/                          ← Application source
│   ├── app.py                    ← Streamlit UI (6 pages)
│   ├── agents/
│   │   ├── graph.py              ← LangGraph workflow builder
│   │   ├── nodes.py              ← Agent node implementations
│   │   └── state.py              ← AgentState TypedDict
│   ├── tools/
│   │   └── agentic_tools.py      ← LangChain @tool definitions
│   ├── retrieval/
│   │   ├── hybrid_retriever.py   ← Hybrid RAG (Dense + BM25)
│   │   ├── reranker.py           ← Cross-encoder reranking
│   │   └── vector_store.py       ← ChromaDB setup
│   ├── memory/
│   │   ├── session_memory.py     ← Per-session conversation history
│   │   └── audit_log.py          ← Compliance audit trail
│   └── incidents/
│       └── incident_manager.py   ← Incident CRUD + SLA
│
├── DATA/                         ← Enterprise documents & persistence
│   ├── it_sop/                   ← IT Standard Operating Procedures
│   ├── it_policies/              ← Enterprise policies
│   ├── technical_docs/           ← Technical documentation
│   ├── incident_reports/         ← Historical incident reports
│   ├── incidents/                ← Active incidents (auto-created)
│   ├── audit/                    ← Audit log (auto-created)
│   └── memory/                   ← Session memory (auto-created)
│
├── vectorstore/                  ← ChromaDB persistence
├── tests/                        ← Unit test suite
│   ├── test_incident_manager.py
│   ├── test_audit_log.py
│   ├── test_session_memory.py
│   └── test_graph_smoke.py
│
├── scripts/
│   └── ingest_documents.py       ← Document ingestion pipeline
│
├── config.py                     ← Centralized configuration
├── startup.py                    ← Production startup script
├── Dockerfile                    ← Multi-stage production build
├── docker-compose.yml            ← Production stack
├── Makefile                      ← Developer commands
├── requirements.txt              ← Python dependencies
└── .env                          ← Environment variables (not in git)
```

---

## 🤖 Agent Capabilities

### 💡 IT Knowledge Agent
Answers questions about VPN, network, DNS, software, and hardware issues by searching enterprise IT SOPs and technical documentation.

**Example queries:**
- "VPN connects but internal apps are unreachable"
- "How to configure split tunneling on Cisco AnyConnect?"
- "DNS resolution failing for internal domains"

### 📜 Policy Agent
Retrieves and interprets enterprise IT security policies, access control procedures, and compliance requirements.

**Example queries:**
- "What is the enterprise password policy?"
- "MFA requirements for remote access"
- "Data classification policy for customer data"

### 🚨 Incident Agent
Investigates historical incidents, performs root-cause analysis, and creates new incident tickets when required.

**Example queries:**
- "What caused the VPN outage last month?"
- "Create a P2 incident for database connectivity failure"
- "Root cause analysis for the authentication service issue"

### 💬 General Agent
Handles broad IT questions and can invoke any available tool for maximum flexibility.

---

## 🎫 Incident Management

### Severity Levels

| Severity | Label | SLA Target | Use Case |
|----------|-------|-----------|---------|
| P1 | Critical | 1 hour | Complete service outage, data breach |
| P2 | High | 4 hours | Major functionality impaired |
| P3 | Medium | 24 hours | Partial degradation, workaround exists |
| P4 | Low | 72 hours | Minor issue, enhancement request |

### Incident Lifecycle

```
Open → In Progress → Resolved → Closed
                ↓
           Escalated
```

### SLA Monitoring

The platform automatically monitors SLA compliance and displays:
- 🟢 **On Track** — SLA has ample remaining time
- 🟡 **At Risk** — 50% of SLA time consumed
- 🟠 **Critical** — 25% of SLA time remaining
- 🔴 **Breached** — SLA deadline exceeded
- ✅ **Met** — Resolved within SLA target

---

## 👤 Human-in-the-Loop

The platform implements **LangGraph interrupt-based HITL** for high-stakes decisions:

**When is human review triggered?**
- P1 (Critical) incident creation
- P2 (High) incident creation
- Proposed actions affecting multiple systems
- Escalations flagged by the Incident Agent

**Review Options:**
| Decision | Outcome |
|----------|---------|
| ✅ Approve | Agent proceeds with proposed action |
| ❌ Reject | Action is cancelled, reason logged |
| 🚨 Escalate | Case escalated to L3 / senior engineer |

---

## 📋 Audit & Compliance

Every AI interaction is logged to `DATA/audit/audit_log.json`:

```json
{
  "entry_id": "AUDIT-20260923-0001",
  "timestamp": "2026-09-23T10:30:45.123456",
  "session_id": "SESSION_20260923_103045_A1B2C3D4",
  "query": "VPN connects but apps are unreachable",
  "route": "it_knowledge",
  "tools_called": ["search_it_knowledge_tool"],
  "answer_preview": "When VPN connects but internal applications...",
  "sources_count": 3,
  "sources": [{"file_name": "vpn_sop.pdf", "page": 4, "score": 0.923}],
  "human_review_required": false,
  "incident_id": null,
  "duration_ms": 1842
}
```

---

## 👥 IT Team Onboarding

### For IT Support Analysts (L1/L2)

1. Open the platform at http://your-server:8501
2. Navigate to **💬 AI Assistant**
3. Type your IT question in the chat box
4. Review the AI answer and cited sources
5. If the platform raises a **Human Review** alert:
   - Read the proposed action carefully
   - Choose **Approve**, **Reject**, or **Escalate**
6. Check the **🚨 Incidents** page to track active tickets

### For IT Managers

1. Use the **📊 Dashboard** page for:
   - Query volume and routing analytics
   - SLA compliance overview
   - Tool usage frequency
2. Use the **📋 Audit Log** to review all AI interactions
3. Use the **🚨 Incidents** page to manage P1/P2 critical incidents

### For Platform Administrators

1. Set `GOOGLE_API_KEY` in `.env`
2. Run `python scripts/ingest_documents.py` after adding new docs
3. Monitor logs in `logs/` directory
4. Use `docker-compose logs -f app` for container logs
5. Update `.env` SLA hours if organizational SLAs change

---

## 🛡️ Security Notes

- API keys are loaded from `.env` — **never commit `.env` to git**
- Docker image runs as a **non-root user** (`appuser`)
- XSRF protection is enabled in production Streamlit config
- Audit log is **append-only** for compliance integrity
- Consider adding `streamlit-authenticator` for user authentication in sensitive deployments

---

## 📞 Support

For platform issues:
1. Check `logs/` directory for error details
2. Review the **⚙️ Architecture** page for system status
3. Run `python -m pytest tests/ -v` to verify components

---

*Enterprise IT Intelligence Platform v1.0.0 — Built with LangGraph, Hybrid RAG, and Google Gemini*
