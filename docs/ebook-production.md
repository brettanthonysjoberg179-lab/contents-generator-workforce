# Ebook Production Pipeline — Project Documentation

> For the full strategy document, see Obsidian: "Ebook Production Strategy"

## Quick Reference

- **Project:** Ebook Production Pipeline
- **Business:** Fair Dinkum Publishing (Aussie Agent Workflowz)
- **Formats:** EPUB 3.3 + PDF/X-UA (dual-format)
- **Pipeline:** `src/agents/pagination.py`
- **QA Module:** `src/ebook_builder_mcp/qc.py`
- **Existing Ebooks:** 7 published (Smart Home Automation, Aboriginal Dot Painting, etc.)

### Pipeline Stages
1. Research & Strategy → Content Strategy Agent
2. Content Creation → Article/Chapter Agent
3. Editorial & Formatting → Editing/SEO Agent
4. Dual-Format Build → Pagination Module
5. Quality Control → QA Agent
6. Cover & Assets → Cover Design (Pillow)
7. Publishing & Distribution → Publishing Agent

### Format Specifications
- **EPUB 3.3:** Reflowable XHTML5, `orphans: 2; widows: 2;`, responsive images
- **PDF/X-UA:** Fixed A4, paged media CSS, running headers/footers
- **Pricing:** $9.99–$49.99 AUD depending on length

### Current Status
- ✅ Dual-format pipeline implemented and verified
- ✅ Pagination system working (`src/agents/pagination.py`)
- ✅ QA module functional (`src/ebook_builder_mcp/qc.py`)
- ✅ 7 ebooks published
- ✅ Obsidian vault with market research notes
- ✅ Fair Dinkum Book Hub operational
- 🔲 Ebook-specific agent prompts pending
- 🔲 Stripe payment integration pending
- 🔲 First agent-produced ebook pending