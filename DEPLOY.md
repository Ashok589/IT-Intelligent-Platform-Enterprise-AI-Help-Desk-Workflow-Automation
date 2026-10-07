# 🚀 Enterprise IT Intelligence Platform — Deployment Guide

> **MNC-Grade Production Deployment for Recruiters & Evaluators**

---

## ⚡ Option 1: Run Locally in 5 Minutes (Recommended for Demo)

### Prerequisites
- Python 3.11+
- Google Gemini API Key ([Get free key](https://aistudio.google.com/app/apikey))

### Steps

```powershell
# 1. Navigate to project
cd "Enterprise IT Intelligence Platform using Hybrid RAG and Agentic AI"

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Install dependencies (if not already done)
pip install -r requirements.txt

# 4. Ensure API key is set in .env
# .env should contain: GOOGLE_API_KEY=your_key_here

# 5. Launch the platform
python startup.py
```

**Open** → http://localhost:8501

> ℹ️ The vectorstore is already initialized. You can start chatting immediately.

---

## ☁️ Option 2: Streamlit Community Cloud (Free Public URL)

Deploy to get a **shareable public URL** for recruiters.

### Steps

1. **Push to GitHub** (public or private repo)
   ```bash
   git init
   git add .
   git commit -m "Enterprise IT Intelligence Platform v1.0.0"
   git remote add origin https://github.com/YOUR_USERNAME/enterprise-it-platform.git
   git push -u origin main
   ```

2. **Add secrets on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click **New app** → select your repo
   - Set **Main file path**: `SRC/app.py`
   - Under **Advanced settings → Secrets**, add:
     ```toml
     GOOGLE_API_KEY = "your_gemini_api_key_here"
     ```

3. **Deploy** → Get your public URL like:
   `https://your-app-name.streamlit.app`

> ⚠️ **Note**: Streamlit Cloud free tier has 1 GB RAM. The Cross-Encoder and
> embedding models need ~800 MB. If you hit limits, set `TOP_K_RERANK=1` in secrets.

---

## 🐳 Option 3: Docker (Full Production)

```powershell
# Build
docker build -t enterprise-it-platform:1.0.0 .

# Run
docker run -d `
  --name enterprise-it-platform `
  -p 8501:8501 `
  --env-file .env `
  -v ${PWD}/DATA:/app/DATA `
  -v ${PWD}/vectorstore:/app/vectorstore `
  -v ${PWD}/enterprise_it_checkpoints.db:/app/enterprise_it_checkpoints.db `
  enterprise-it-platform:1.0.0
```

**Or with Docker Compose (recommended):**
```powershell
docker-compose up -d
# View logs
docker-compose logs -f app
# Health check
curl http://localhost:8501/_stcore/health
```

---

## 🏗️ Option 4: Cloud VM (AWS/Azure/GCP)

For MNC-level deployment on a cloud VM:

```bash
# On Ubuntu 22.04 VM (t3.medium or equivalent)

# Install dependencies
sudo apt update && sudo apt install -y python3.11 python3.11-venv git

# Clone repo
git clone https://github.com/YOUR_USERNAME/enterprise-it-platform.git
cd enterprise-it-platform

# Setup
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set env
echo "GOOGLE_API_KEY=your_key_here" > .env

# Run with PM2 (process manager)
npm install -g pm2
pm2 start "python startup.py" --name enterprise-it-platform
pm2 save && pm2 startup
```

---

## 🌐 Nginx Reverse Proxy (HTTPS)

Uncomment the nginx section in `docker-compose.yml` and add your SSL certs
to `nginx/certs/` for HTTPS access.

---

## ✅ Post-Deploy Checklist

```
□  Platform loads at http://localhost:8501 (or your public URL)
□  Portfolio page visible at /00_Portfolio
□  AI Assistant responds to queries
□  Human-in-the-Loop triggers on P1 incident creation
□  Dashboard shows query analytics
□  Audit Log captures all interactions
□  Incidents page shows CRUD with SLA tracking
□  Memory page shows session history
□  Architecture page shows Mermaid diagram
```

---

## 🎯 Recruiter Demo Script

### 1. Open AI Assistant (💬)
Ask: **"VPN connects but internal apps are unreachable"**
→ Demonstrates: Hybrid RAG + IT Knowledge Agent + source citations

### 2. Ask a Policy Question
Ask: **"What is the enterprise password policy?"**
→ Demonstrates: Policy Agent + document retrieval

### 3. Trigger Human-in-the-Loop
Ask: **"Create a P1 critical incident — production database is completely down"**
→ Demonstrates: Incident Agent + LangGraph HITL interrupt + Approve/Reject panel

### 4. Visit Dashboard (📊)
→ See live query analytics, routing charts, tool usage frequency

### 5. Visit Incidents (🚨)
→ Manage the P1 incident: update status, add notes, view SLA countdown

### 6. Visit Audit Log (📋)
→ Inspect compliance trail of all AI interactions

### 7. Visit Memory (🧠)
→ Replay the full conversation with route and source metadata

### 8. Visit Architecture (⚙️)
→ Interactive LangGraph diagram, agent components, full tech stack

---

## 📊 Platform Architecture Summary

```
Streamlit UI (6 pages)
       │
LangGraph Multi-Agent Workflow
       │
   ┌───┴───┐
Memory   Supervisor (Gemini routing)
   │         │
   └─────────┼──────────────────────┐
         IT Knowledge    Policy    Incident    General
         Agent           Agent     Agent       Agent
             └─────────────┴──────────┘
                          │
                   HITL (P1/P2 only)
                          │
                     Audit Node
                          │
              Hybrid RAG Pipeline
           Dense(ChromaDB) + Sparse(BM25)
                    + RRF Fusion
               + Cross-Encoder Reranking
```

---

*Enterprise IT Intelligence Platform v1.0.0 — Built with LangGraph, Hybrid RAG, and Google Gemini*
