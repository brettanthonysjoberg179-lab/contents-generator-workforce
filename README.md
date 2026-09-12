# Content Generator Workforce

A dependency-driven workforce of 20+ AI agents for content marketing. Built with Ollama (local LLM), Composio (tool infrastructure), MCP protocol, Airtable (structured database), and Obsidian (knowledge base).

## Architecture

```
                    ┌────────────────────┐
                    │ MASTER ORCHESTRATOR│
                    │  (Ollama LLM)      │
                    │  Planning/Routing  │
                    │  QA/Approval       │
                    └─────────┬──────────┘
                              │
                    ┌─────────┼──────────────────┐
                    ▼         ▼                  ▼
              RESEARCH     CREATION          PUBLISHING
               Agents     Agents            Agents
              ┌──────┐   ┌──────┐          ┌──────┐
              │Trend │   │Writer│          │Social│
              │Research│ │SEO   │          │Video │
              │Reddit│   │Article│         │Repurp│
              │X     │   │Social│          │FactCh│
              │TikTok│   │Video │          │QA    │
              │FB    │   │Repurp│          │Publish│
              │LinkedIn│  │      │          │Analytics│
              └──────┘   └──────┘          └──────┘
                    │         │                  │
                    └─────────┼──────────────────┘
                              ▼
                   ┌──────────────────┐
                   │    COMPOSIO      │
                   │  Tool + Auth     │
                   │  MCP Sessions    │
                   └────────┬─────────┘
                            │
               ┌────────────┼──────────────┐
               ▼              ▼              ▼
           AIRTABLE       OBSIDIAN      GOOGLE DRIVE
           State/DB       Knowledge     Files/Assets
               │              │              │
               └──────────────┼──────────────┘
                              ▼
                         ANALYTICS
                              │
                              ▼
                       LEARNING LOOP
```

## Core Design Principles

1. **One authority for decisions** — The Master Orchestrator controls all workflow decisions
2. **Specialist agents return structured results** — Never free-form prose
3. **Composio sits in the tool layer** — Not every agent manages its own credentials
4. **Files vs Database** — Obsidian/Google Drive for documents, Airtable for structured state
5. **Approval gates** — No automatic publishing from day one
6. **Learning loop** — Performance data feeds back into strategy

## Prerequisites

- Python 3.10+
- Ollama running (`ollama serve`) with at least one model pulled
- Composio API key
- Optional: Airtable API key and Base ID
- Optional: Google Drive credentials

## Quick Start

```bash
# 1. Clone the project
cd ~/contents-generator-workforce

# 2. Install dependencies
pip install -e .

# 3. Set environment variables
cp .env.example .env
# Edit .env with your API keys

# 4. Start Ollama (if not already running)
ollama serve &
ollama pull llama3.2:latest

# 5. Run the workforce
python3 run_workforce.py

# 6. Or start the MCP server
python3 mcp_server/main.py

# 7. Run tests
python3 -m pytest tests/ -v
```

## Running the MCP Server

```bash
# Start the FastAPI MCP server (default port 8000)
python3 run_workforce.py

# Or with custom settings
MCP_PORT=9000 python3 run_workforce.py
```

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with agent count |
| `/tools` | GET | List all MCP tools |
| `/tools/call` | POST | Call a specific tool |
| `/workflows/run` | POST | Run a complete workflow |
| `/agents` | GET | List all registered agents |

## Project Structure

```
contents-generator-workforce/
├── config/              # System, agent, platform, composio, ollama, airtable configs
├── agents/              # 20 specialist agents
├── shared/              # Base agent, Ollama client, Composio client, LLM agent
├── composio/            # Composio integration (client, sessions, tool registry, auth)
├── mcp_server/          # FastAPI MCP server
├── workflows/           # YAML workflow definitions
├── knowledge/           # Brand, audience, platform rules, research templates
├── files/               # incoming, working, approved, published, archive
├── scripts/             # Init, test, health check scripts
├── tests/               # Test suite
├── logs/                # Structured JSON logs
├── reports/             # Analytics reports
├── docker-compose.yml   # Multi-container setup
├── pyproject.toml       # Project dependencies
├── run_workforce.py     # Entry point
└── README.md            # This file
```

## Agent Overview

| # | Agent | Layer | Purpose |
|---|-------|-------|---------|
| 1 | Master Orchestrator | Control | Plans and controls everything |
| 2 | Trend Intelligence | Discovery | What topics are gaining attention |
| 3 | Research | Discovery | Turn topics into reliable research |
| 4 | Audience Intelligence | Discovery | Combine platforms into audience model |
| 5 | Content Strategy | Strategy | Determine what to produce |
| 6 | Article Writer | Production | Long-form content |
| 7 | Social Content | Production | Short-form social copy |
| 8 | Video Script | Production | Video scripts and storyboards |
| 9 | SEO | Production | Search optimization |
| 10 | Repurposing | Production | Turn 1 article into entire campaign |
| 11 | Fact Check | QA | Verify factual accuracy |
| 12 | QA | QA | Content readiness validation |
| 13 | Publishing | Distribution | Move content to platforms |
| 14 | Analytics | Learning | Collect performance metrics |
| 15 | Optimisation | Learning | Close the feedback loop |
| 16 | Reddit Intelligence | Discovery | Understand Reddit conversations |
| 17 | X Intelligence | Discovery | Understand X/Twitter trends |
| 18 | TikTok Intelligence | Discovery | Understand TikTok trends |
| 19 | Facebook Intelligence | Discovery | Understand Facebook trends |
| 20 | LinkedIn Intelligence | Discovery | Understand LinkedIn trends |

## Dependency Rules

1. **Research before production** — NO RESEARCH → NO ARTICLE
2. **Fact checking before approval** — NO FACT CHECK → NO APPROVAL
3. **QA before publishing** — NO QA PASS → NO PUBLISH
4. **Approval before external publishing** — DRAFT → QA → APPROVAL → PUBLISH
5. **Analytics feeds future strategy** — PUBLISHED → ANALYTICS → OPTIMISATION → STRATEGY

## Composio Integration

Composio provides the external tool layer. The workforce uses Composio sessions to discover, authenticate, and execute tools across platforms. Each agent gets a tool allowlist — the orchestrator gets broader permissions.

```python
from composio import Composio
from composio_integration import ComposioIntegration

# Initialize
composio = ComposioIntegration()

# Create a session for Reddit
session_id = composio.create_session("reddit")

# Execute a tool
result = composio.execute_tool(session_id, "reddit_search", {"query": "AI marketing"})
```

## Ollama Models

| Agent Type | Model | Use Case |
|-----------|-------|----------|
| Orchestrator | llama3.2:latest | Planning, routing, decisions |
| Research | llama3.2:latest | Deep analysis, synthesis |
| Writer | llama3.2:latest | Content generation |
| Video Script | llama3.2:1b | Fast inference |
| Classification | llama3.2:1b | Fast, lightweight tasks |

## Airtable Tables

| Table | Purpose |
|-------|---------|
| Campaigns | Content campaigns tracking goals, status, timeline |
| Content Ideas | Ideas with scores and status |
| Research | Research records with sources and confidence |
| Content | All content items with SEO scores and QA status |
| Assets | File references (Google Drive URLs, Obsidian paths) |
| Social Posts | Platform-specific post data |
| Agent Tasks | Agent execution tracking |
| Analytics | Performance metrics per post |

## Obsidian Vault Structure

```
ContentsVault/
├── 00_System/
├── 01_Brand/
├── 02_Audience/
├── 03_Content/
├── 04_Research/
├── 05_Campaigns/
├── 06_Agents/
├── 07_Workflows/
├── 08_Platform_Rules/
└── 99_Archive/
```

## Google Drive Structure

```
Content Workforce/
├── 01 Strategy/
├── 02 Research/
├── 03 Campaigns/
├── 04 Articles/
├── 05 Social/
├── 06 Videos/
├── 07 Images/
├── 08 Approved/
├── 09 Published/
├── 10 Analytics/
└── 99 Archive/
```

## Content ID System

Every content object gets a stable ID shared across Airtable, Obsidian, and Drive:

```
CNT-2026-000184
├── Airtable → CNT-2026-000184 (record)
├── Obsidian → CNT-2026-000184.md (note)
└── Drive → CNT-2026-000184/ (folder)
```

## Testing

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test
python3 -m pytest tests/test_workforce.py::test_orchestrator_registration -v

# Run with coverage
python3 -m pytest tests/ --cov=agents --cov=shared
```

## License

Fair Dinkum Publishing

---

*Last updated: 2026-09-12*