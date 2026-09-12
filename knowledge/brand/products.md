# Product Catalog

> Last updated: 2026-09-12  
> Owner: Brett Sjoberg  
> Scope: All products and services offered under the Brett Sjoberg / Contents Generator Workforce umbrella

---

## 1. Contents Generator Workforce

**Tagline:** A dependency-driven workforce of 20+ AI agents for content marketing.

**Description:** The core product — an orchestrated system of specialized AI agents that handle the entire content pipeline from trend discovery through research, production, QA, publishing, analytics, and optimisation. Each agent has defined roles, skills, MCP tools, data access, upstream dependencies, and downstream consumers.

**Key Features:**
- 20 specialized agents across three dependency layers (Discovery, Production, Distribution/Learning)
- Strict dependency enforcement: research → production → QA → publish → analytics → optimise
- MCP server exposing all tools via FastAPI endpoints
- Ollama-based local LLM inference
- Composio integration for external tools
- Airtable, Obsidian, and Google Drive integrations
- Automated workflow orchestration via Master Orchestrator

**Target Audience:** Content marketers, agency owners, and business operators who need to scale content production with quality control.

**URL:** `~/contents-generator-workforce`

---

## 2. Fair Dinkum Publishing

**Tagline:** Authentic Australian publishing.

**Description:** A publishing operation focused on producing quality ebooks and digital publications. Fair Dinkum Publishing runs a specialized agent workforce that handles the entire ebook lifecycle: market research, opportunity scoring, outlining, authoring, editorial, cover design, production, sales copy, and launch strategy.

**Key Features:**
- Dual-format EPUB 3 + PDF publishing pipeline
- Agent-based ebook production workforce (15+ specialized agents)
- Google Drive integration for manuscript and artifact versioning
- Stripe integration for fulfillment and commissions
- HF Space deployment for flipbook previews
- Automated QC pipeline (EpubCheck, PDF page-budget, accessibility metadata)
- Obsidian vault for manuscript management

**Target Audience:** Authors, indie publishers, and content creators looking to produce and sell professional ebooks.

**URL:** `~/fair-dinkum-publishing-agent-workforce`

---

## 3. AgentForge

**Tagline:** Build and deploy AI agent workflows.

**Description:** A framework for building, composing, and deploying autonomous AI agent systems. AgentForge provides the scaffolding for creating custom agent pipelines with defined roles, tools, permissions, and dependency chains.

**Key Features:**
- Modular agent architecture with BaseAgent pattern
- MCP server for tool exposure and inter-agent communication
- Dependency graph management for agent workflows
- Configurable permissions (read/write, tool access)
- Composio MCP integration for extended capabilities
- Python-based agent definitions with async execution

**Target Audience:** Developers and technical operators building AI agent systems for specific use cases.

**URL:** Referenced in skill files and Obsidian vault notes

---

## 4. Ebook Hub

**Tagline:** Your ebook publishing command center.

**Description:** A centralised platform for managing ebook production workflows, including manuscript tracking, agent task assignment, quality control gates, and publication scheduling. Ebook Hub serves as the operational dashboard for Fair Dinkum Publishing operations.

**Key Features:**
- Project management for ebook workflows
- Agent task dispatch and status tracking
- QC pipeline orchestration
- Publication scheduling
- Integration with Obsidian, Google Drive, and Airtable
- HF Space staging for flipbook previews

**Target Audience:** Ebook publishers, production managers, and editorial teams.

---

## 5. Trifecta Pro (FormFav MCP)

**Tagline:** AI-powered Australian Gallops trifecta predictions.

**Description:** An MCP server and prediction system for Australian horse racing trifecta betting. Uses FormFav API data combined with weighted scoring models that account for distance-specific factors, form quality, class, barrier, jockey, and track conditions.

**Key Features:**
- FormFav API integration (meetings, race form, predictions)
- Distance-specific weight profiles (sprint, middle, staying)
- Weighted scoring model covering 11 factors
- Discord bot integration for prediction delivery
- HF Space deployment for prediction interfaces
- Historical form data and race archives
- Daily prediction runs with automated scheduling

**Target Audience:** Australian horse racing enthusiasts, punters, and racing analysts.

**URL:** `~/mcp-command-centre/trifecta_agent_server.py`

---

## 6. Agent Intelligence Suite

**Tagline:** Platform intelligence for smarter content.

**Description:** A collection of specialized intelligence agents that monitor and analyse trends across major social platforms: Reddit, X (Twitter), TikTok, Facebook, and LinkedIn. Each platform intelligence agent feeds into the Audience Intelligence agent, which combines platform data into a unified audience model.

**Key Features:**
- Per-platform trend detection and conversation analysis
- Audience sentiment and interest mapping
- Cross-platform correlation
- Content strategy inputs based on what's trending
- Automated intelligence reports

**Target Audience:** Content strategists, social media managers, and marketing analysts.

---

## 7. Repurposing Engine

**Tagline:** One article, entire campaign.

**Description:** A production agent that takes a single long-form article and generates an entire multi-platform content campaign — social media posts, video scripts, SEO-optimised variants, and platform-specific adaptations.

**Key Features:**
- Input: single article or research brief
- Output: platform-adapted social posts, video scripts, SEO variants, email sequences
- Platform-aware formatting (character limits, hashtag strategies, visual specs)
- Automatic content calendar generation
- Approval workflow integration

**Target Audience:** Content teams, social media managers, and publishers.

---

## Product Comparison Matrix

| Product | Type | Primary Users | Core Value |
|---------|------|---------------|------------|
| Contents Generator Workforce | Platform | Content marketers, agencies | Full content pipeline automation |
| Fair Dinkum Publishing | Publisher | Authors, indie publishers | Automated ebook production |
| AgentForge | Framework | Developers | Agent system scaffolding |
| Ebook Hub | Dashboard | Publishers, editors | Production workflow management |
| Trifecta Pro | Predictions | Racing enthusiasts | AI-powered racing analysis |
| Agent Intelligence Suite | Intelligence | Strategists, analysts | Cross-platform trend awareness |
| Repurposing Engine | Production | Content teams | Article-to-campaign conversion |

---

## Product Relationships

```
AgentForge (framework)
    ├── Contents Generator Workforce (content marketing)
    │       ├── Fair Dinkum Publishing (ebook production)
    │       │       └── Ebook Hub (workflow dashboard)
    │       ├── Agent Intelligence Suite (trend/discovery)
    │       ├── Repurposing Engine (content adaptation)
    │       └── Trifecta Pro (racing predictions)
    └── Other agent systems (custom deployments)
```

---

## Notes

- All products share the same brand voice, rules, and quality standards
- Cross-product content should reference the originating product clearly
- Each product may have additional platform-specific rules (see `knowledge/platform_rules/`)
- Product updates should be reflected in this file and the relevant skill files
