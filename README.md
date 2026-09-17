# 🤖 Agentic AI Projects — Beginners to Advance

> **30 production-grade Agentic AI systems**, structured as a 4-phase engineering roadmap — from your first tool call to enterprise-scale autonomous infrastructure.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-State%20Machines-1C3C3C)](https://langchain-ai.github.io/langgraph/)
[![LlamaIndex](https://img.shields.io/badge/LlamaIndex-RAG-6E56CF)](https://www.llamaindex.ai/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Demos-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 📌 About This Repository

Most "AI agent" tutorials stop at a chat wrapper around an LLM. This repository does not.

**Agentic-AI-Projects-Beginners-to-Advance** is a curated, progressively-difficult curriculum of **30 complete, deployable agentic systems**. Each project is built as a standalone application with its own source tree, dependency manifest, environment contract, and documentation — not as a notebook snippet.

The roadmap is deliberately sequenced so that every phase introduces a _new class of agentic capability_, and every project reuses the primitives you learned in the one before it:

| Phase       | Level           | Projects    | The Capability You Unlock                                                                                          |
| :---------- | :-------------- | :---------- | :----------------------------------------------------------------------------------------------------------------- |
| **Phase 1** | 🟢 Beginner     | `#01 – #07` | Giving an LLM **hands** — tool calling, structured outputs, ReAct loops, basic RAG                                 |
| **Phase 2** | 🟡 Intermediate | `#08 – #15` | Giving an agent **memory and control flow** — LangGraph state machines, reflection, HITL, vision & audio           |
| **Phase 3** | 🟠 Advanced     | `#16 – #23` | Giving agents **colleagues** — multi-agent swarms, hierarchical supervisors, long-term memory, sandboxed execution |
| **Phase 4** | 🔴 Enterprise   | `#24 – #30` | Giving agents **production hardening** — GraphRAG, self-healing infra, realtime streaming, gateways & guardrails   |

> **Philosophy:** an agent is not a prompt. It is a _system_ — with a control loop, a tool boundary, a validation layer, a failure mode, and an observability story. Every README in this repo documents all five.

---

## 🚀 Live Deployments

Deployed applications you can use right now, without cloning anything.

| #       | Project                                 | Live App                                                        | Status         |
| :------ | :-------------------------------------- | :-------------------------------------------------------------- | :------------- |
| **#01** | Smart Weather & Travel Advice Assistant | **[🔗 Launch App](https://smart-weather-agent.streamlit.app/)** | ✅ Live        |
| #02     | Automated Financial Calculator Agent    | —                                                               | 🚧 In Progress |
| #03     | Web-Search Summarizer Agent             | —                                                               | 🚧 In Progress |
| #04     | SQL Query & Analytics Assistant         | —                                                               | 📋 Planned     |

_Deployment links are added to this table as each project ships. Watch ⭐ the repo to get notified._

---

## 🗺️ The Complete Roadmap

### 🟢 Phase 1 — Foundations & Tool-Calling Agents (Beginner)

> **Goal:** Move from "the LLM answers" to "the LLM acts." You will learn to expose deterministic functions to a model, validate everything it returns, and build a reasoning loop from first principles.

| #      | Project                                                                        | Tech Stack                                                       | Core Concepts                                                                               |
| :----- | :----------------------------------------------------------------------------- | :--------------------------------------------------------------- | :------------------------------------------------------------------------------------------ |
| **01** | **[Smart Weather & Travel Advice Assistant](projects/01-smart-weather-agent)** | Python, OpenAI / Gemini API, Streamlit, Pydantic, Open-Meteo API | Basic Tool Calling · System Prompting · Structured Outputs · Input Validation               |
| **02** | Automated Financial Calculator Agent                                           | FastMCP / LangChain, Python, FastAPI, React                      | Mathematical Reasoning · Tool Router Pattern · Deterministic Execution · Input Sanitization |
| **03** | Web-Search Summarizer Agent                                                    | LangGraph / LlamaIndex, OpenAI, Tavily API, Next.js              | Search Tool Integration · Context Window Management · Web Scraping · Citation Generation    |
| **04** | SQL Query & Analytics Assistant                                                | LangChain, PostgreSQL / SQLite, Streamlit                        | Text-to-SQL · Dynamic Tool Execution · Schema Inspection · Read-Only Guardrails             |
| **05** | Automated GitHub Issue Resolver & Summarizer                                   | Python, GitHub REST API, FastAPI, Groq / Claude 3.5 Sonnet       | REST API Tool Binding · Event-driven Agents · GitHub Webhooks · Automated Triage            |
| **06** | Interactive Document Q&A Agent (Basic RAG)                                     | LlamaIndex / LangChain, ChromaDB / Qdrant, Streamlit             | Agentic RAG · Vector Search · Corrective RAG (CRAG) Fallback · Chunking Strategies          |
| **07** | ReAct Pattern Search & Reason Agent (From Scratch)                             | Pure Python, OpenAI / Anthropic API, FastAPI                     | Pure ReAct Pattern · Custom Parsing · Loop Termination Logic · State Management             |

---

### 🟡 Phase 2 — State Machines, Memory & Multi-Step Workflows (Intermediate)

> **Goal:** Replace fragile prompt chains with explicit graphs. You will learn persistence, conditional routing, self-critique, and how to put a human in the loop without breaking automation.

| #      | Project                                             | Tech Stack                                                           | Core Concepts                                                                                     |
| :----- | :-------------------------------------------------- | :------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------ |
| **08** | Stateful Customer Support Ticket Routing Agent      | LangGraph, Pinecone, FastAPI, Next.js                                | Graph State Management · Human-in-the-Loop (HITL) · Conditional Edges · Workflow Persistence      |
| **09** | Autonomous Code Reviewer & Refactorer               | LangGraph, Flake8 / SonarQube CLI, Claude 3.5 Sonnet, GitHub Actions | AST Parsing Tools · Self-Correction Loops · Multi-Tool Pipelines · Automated Testing              |
| **10** | Autonomous Blog & Social Media Content Engine       | CrewAI / LangGraph, OpenAI DALL·E 3 / Flux API, Next.js              | Sequential Pipelines · Cross-Platform Transformation · Multimodal Generation · Style Alignment    |
| **11** | Multi-Format Document Parser & Extractor Agent      | LlamaIndex, GPT-4o / Claude 3.5 Sonnet, Pydantic, Streamlit          | Multimodal Function Calling · Schema Validation · Extraction Repair · OCR Integration             |
| **12** | Smart Email Summarizer & Action Item Tracker        | Python, Gmail API, Notion API, LangChain, Cron Jobs                  | OAuth2 Tooling · Persistent Memory · Periodic Cron Triggers · Task Automation                     |
| **13** | Research Assistant with Iterative Self-Correction   | LangGraph, Tavily Search, FastAPI, React                             | Reflection Pattern · Critique-and-Refine Loop · Fact Verification · Autonomous Editing            |
| **14** | E-Commerce Product Recommendation & Concierge Agent | LlamaIndex, Qdrant / Pgvector, Next.js, Tailwind CSS                 | Hybrid Search (BM25 + Dense Vector) · Conversational Memory · Dynamic Filtering · Personalization |
| **15** | Automated Meeting Notes & Action Item Dispatcher    | OpenAI Whisper, LangChain, Slack API, FastAPI                        | Audio Processing Tooling · Speaker Diarization · Structured Extraction · Notification Dispatch    |

---

### 🟠 Phase 3 — Multi-Agent Collaboration & Complex Planning (Advanced)

> **Goal:** Coordinate many specialized agents safely. You will learn hand-off protocols, supervisor hierarchies, sandboxing, constraint-satisfaction planning, and domain guardrails.

| #      | Project                                                 | Tech Stack                                                      | Core Concepts                                                                                         |
| :----- | :------------------------------------------------------ | :-------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| **16** | Multi-Agent Software Engineering Team (Dev, Tester, PM) | CrewAI / AutoGen / LangGraph, Docker Container Runtime, Python  | Multi-Agent Hand-off · Tool Sandboxing · Iterative Debugging Loops · Role Specialization              |
| **17** | Autonomous Market & Competitor Intelligence System      | LangGraph Supervisor, Playwright, Claude 3.5 Sonnet, FastAPI    | Hierarchical Supervisor Pattern · Parallel Agent Execution · Data Synthesis · Scraping Infrastructure |
| **18** | Medical Research & Clinical Trial Matching Agent        | LlamaIndex, BioBERT / MedCPT Embeddings, Qdrant, Streamlit      | Domain-Specific RAG · NeMo / Llama Guardrails · Entity Disambiguation · Safety Auditing               |
| **19** | Personal AI Chief of Staff with Long-Term Memory        | Mem0 / Zep, LangGraph, OpenAI GPT-4o, Next.js                   | Dual Memory Architecture (Short + Long Term) · Memory Reflection · Semantic Consolidation             |
| **20** | Automated Security Vulnerability & Pen-Test Agent       | AutoGen, Docker Code Execution Sandbox, Nmap / ZAP CLI, FastAPI | Safe Sandboxed Execution · Multi-Step Planning · Risk Scoring · Penetration Automation                |
| **21** | Real-Time Financial Trading Strategy Backtester Agent   | LangGraph, Python Exec Engine, Yahoo Finance API, Streamlit     | Dynamic Code Generation · Multimodal Chart Analysis · Quantitative Analytics · Financial Modeling     |
| **22** | Autonomous Travel & Itinerary Booking Orchestrator      | CrewAI, Amadeus Travel API, Google Maps API, Next.js            | Constraint Satisfaction Planning · Parallel API Calls · Agent Negotiation · Itinerary Optimization    |
| **23** | Customer Onboarding & KYC Automation Pipeline           | LangGraph, Tesseract / AWS Textract, FastAPI, React             | HITL Escalation · OCR Vision Processing · Workflow Orchestration · Risk Assessment                    |

---

### 🔴 Phase 4 — Enterprise-Grade & Autonomous Production Systems (Enterprise)

> **Goal:** Ship agents that survive contact with production. You will learn graph-augmented retrieval, autonomous remediation, realtime streaming, auditability, and cost/PII governance.

| #      | Project                                             | Tech Stack                                                                 | Core Concepts                                                                                            |
| :----- | :-------------------------------------------------- | :------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------- |
| **24** | Enterprise RAG & Agentic Knowledge Graph (GraphRAG) | LlamaIndex, Neo4j, Pinecone, LangSmith / Arize Phoenix, FastAPI            | GraphRAG · Knowledge Graph Construction · Hybrid Vector-Graph Search · Multi-Hop Reasoning               |
| **25** | Self-Healing DevOps & Cloud Infrastructure Agent    | Python, AWS SDK (Boto3), Kubernetes Python API, LangGraph, Datadog         | Autonomous Diagnostics · Infrastructure Control Tools · Action Confirmation Guardrails · Incident Repair |
| **26** | Multi-Modal E-Commerce Customer Support Agent       | OpenAI Realtime API / LiveKit, WebSockets, FastAPI, PostgreSQL, React      | WebSockets Audio Streaming · Multimodal Speech-to-Speech · Database Tooling · Real-time Processing       |
| **27** | Enterprise Compliance & Regulatory Audit Agent      | LangChain / LlamaIndex, OpenTelemetry, Arize Phoenix, Next.js              | Large Context Retrieval · Regulatory Rule Matching · Auditable Traceability · Observability              |
| **28** | Autonomous SQL Query Optimizer & DBA Agent          | LangGraph, PostgreSQL Admin APIs, Docker Test Sandbox, FastAPI             | Database Tuning · Safe DDL Script Execution · Performance Analytics · Isolated Replica Testing           |
| **29** | Distributed Multi-Agent Simulation Platform         | Ray / Celery, LangGraph / AutoGen, Redis, ClickHouse, Grafana              | Agent-Based Modeling (ABM) · Asynchronous Parallel Execution · Distributed State · Telemetry Analytics   |
| **30** | Production Agentic Gateway & Router (LLM Firewall)  | FastMCP / Rust / Go / Python (FastAPI), LiteLLM Core, Redis, Guardrails AI | Semantic Routing · Cost Optimization · PII Anonymization · Fallback Routing · Enterprise Security        |

---

## 🧱 Repository Structure

Every project is fully self-contained. You never need to install dependencies for project #24 in order to run project #01.

```
Agentic-AI-Projects-Beginners-to-Advance/
│
├── projects/
│   ├── 01-smart-weather-agent/
│   │   ├── app.py                 # Streamlit entrypoint
│   │   ├── agent.py               # Tool-calling loop & system prompt
│   │   ├── tools.py               # Open-Meteo tool definitions
│   │   ├── schemas.py             # Pydantic I/O contracts
│   │   ├── requirements.txt
│   │   ├── .env.example
│   │   └── README.md
│   │
│   ├── 02-financial-calculator-agent/
│   ├── 03-web-search-summarizer/
│   └── ...                        # through 30-agentic-gateway-router
│
├── docs/
│   └── agentic_ai_roadmap.pdf     # Master roadmap: all 30 system overviews
│
├── .gitignore
├── LICENSE
└── README.md                      # ← you are here
```

---

## ⚙️ Local Setup

### Prerequisites

| Requirement | Version | Notes                                                              |
| :---------- | :------ | :----------------------------------------------------------------- |
| Python      | `3.10+` | Required by modern LangGraph / Pydantic v2                         |
| Git         | any     | For cloning                                                        |
| Docker      | `24+`   | Only needed for sandboxed projects (#16, #20, #28)                 |
| LLM API Key | —       | OpenAI, Google Gemini, Anthropic, or Groq depending on the project |

### 1. Clone the repository

```bash
git clone https://github.com/sheefanaaz123/Agentic-AI-Projects-Beginners-to-Advance.git
cd Agentic-AI-Projects-Beginners-to-Advance
```

### 2. Move into the project you want to run

```bash
cd projects/01-smart-weather-agent
```

### 3. Create an isolated virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install that project's dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure your environment

```bash
cp .env.example .env
```

Then open `.env` and fill in the keys listed in that project's own README.

### 6. Run it

```bash
# Streamlit projects
streamlit run app.py

# FastAPI projects
uvicorn main:app --reload --port 8000
```

> ⚠️ **Never commit your `.env` file.** It is already covered by `.gitignore`. Rotate any key that has ever touched a commit.

---

## 🧠 Recommended Learning Path

1. **Do not skip Phase 1.** Project #07 (ReAct from scratch) is the single most important project in this repository — every framework in Phases 2–4 is an abstraction over that loop.
2. **Build, then read the source of the framework.** After #08, read LangGraph's `Pregel` loop. After #16, read CrewAI's hand-off implementation.
3. **Break each agent on purpose.** Feed it a malformed location, an empty document, a hostile prompt. The failure modes _are_ the curriculum.
4. **Add observability early.** Even in Phase 1, log every tool call, its arguments, and its latency.

---

## 🤝 Contributing

Contributions, issue reports, and project suggestions are genuinely welcome.

1. Fork the repository
2. Create a feature branch — `git checkout -b feat/project-04-improvements`
3. Commit using conventional commits — `git commit -m "feat(04): add schema inspection cache"`
4. Push and open a Pull Request describing _what agentic behaviour changed_

Please keep each PR scoped to a single project folder.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 👤 Author

**Sheefa Naaz**

- 💼 GitHub: [@sheefanaaz123](https://github.com/sheefanaaz123)
- 📘 Roadmap: _Agentic AI Master Roadmap — 30 Production-Grade Projects with Deep System Overviews_

---

<p align="center">
  <b>If this roadmap helped you, please ⭐ the repository — it genuinely helps others find it.</b>
</p>
