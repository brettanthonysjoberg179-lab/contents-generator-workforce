# Research Templates

> Last updated: 2026-09-12  
> Owner: Brett Sjoberg  
> Scope: Structured output formats for all research produced by the Contents Generator Workforce

---

## 1. Structured JSON Format for Research Findings

All research outputs from the workforce follow this JSON schema. This ensures consistency, machine-readability, and integration with downstream agents.

### 1.1 Top-Level Structure

```json
{
  "research_id": "string — unique identifier",
  "timestamp": "ISO 8601 datetime",
  "agent_id": "string — which agent produced this",
  "topic": "string — research subject",
  "query": "string — original search query or prompt",
  "status": "complete | partial | incomplete | failed",
  "confidence_score": "number 0.0–1.0",
  "sections": {
    "key_findings": [],
    "audience_questions": [],
    "trends": [],
    "sources": [],
    "claims": [],
    "metadata": {}
  },
  "quality_flags": [],
  "next_steps": []
}
```

### 1.2 Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `research_id` | String | Yes | Unique identifier (e.g., "research-20260912-001") |
| `timestamp` | String | Yes | ISO 8601 datetime (e.g., "2026-09-12T10:30:00+10:00") |
| `agent_id` | String | Yes | ID of the agent that produced this research |
| `topic` | String | Yes | The research subject |
| `query` | String | Yes | The original search query or prompt |
| `status` | String | Yes | Complete, partial, incomplete, or failed |
| `confidence_score` | Number | Yes | Overall confidence 0.0–1.0 |
| `sections` | Object | Yes | All research sections |
| `quality_flags` | Array | Yes | List of quality concerns |
| `next_steps` | Array | Yes | Recommended follow-up actions |

---

## 2. Key Findings Format

Each research output must include a structured key findings section.

### 2.1 Structure

```json
{
  "key_findings": [
    {
      "id": "findings-1",
      "finding": "string — the core finding",
      "significance": "high | medium | low",
      "evidence_level": "primary | secondary | tertiary | anecdotal",
      "source_refs": ["string — source IDs or URLs"],
      "confidence": "number 0.0–1.0",
      "implications": "string — what this means for strategy",
      "validated": "boolean",
      "notes": "string — additional context"
    }
  ]
}
```

### 2.2 Rules

- Maximum 5 key findings per research session
- Each finding must have at least one source reference
- Significance levels must be justified in the notes
- Evidence levels must be honest — don't overstate
- Confidence scores below 0.5 must be flagged as "low confidence"
- Findings must be actionable — not just observations

### 2.3 Example

```json
{
  "key_findings": [
    {
      "id": "findings-1",
      "finding": "AI-generated content receives 23% less organic reach on LinkedIn compared to human-written content when not disclosed",
      "significance": "high",
      "evidence_level": "secondary",
      "source_refs": ["https://example.com/study-2026", "research-20260912-001"],
      "confidence": 0.75,
      "implications": "Always include AI disclosure on LinkedIn posts to mitigate reach penalties",
      "validated": true,
      "notes": "Study was conducted in 2026 with 500 posts per group; sample size is adequate"
    }
  ]
}
```

---

## 3. Audience Questions Format

Research should identify and categorize audience questions and curiosities.

### 3.1 Structure

```json
{
  "audience_questions": [
    {
      "id": "q-1",
      "question": "string — the question the audience is asking",
      "source": "string — where this question was observed",
      "platform": "string — platform where it appeared",
      "volume": "high | medium | low",
      "sentiment": "positive | neutral | negative | mixed",
      "category": "string — topic category",
      "related_topics": ["string"],
      "content_opportunity": "string — what content could answer this",
      "priority": "must-address | nice-to-have | optional"
    }
  ]
}
```

### 3.2 Rules

- Questions must be sourced from real observations (comments, searches, discussions)
- Volume must be estimated based on evidence, not speculation
- Sentiment should be backed by context
- Each question should map to a content opportunity
- "Must-address" questions should be addressed in the next content cycle

---

## 4. Trends Format

Research must identify and document trends relevant to the content strategy.

### 4.1 Structure

```json
{
  "trends": [
    {
      "id": "trend-1",
      "name": "string — trend name",
      "description": "string — what the trend is about",
      "platform": "string — where the trend is observed",
      "growth_rate": "number — percentage increase in mentions/engagement",
      "trajectory": "rising | stable | declining | peaking",
      "relevance": "high | medium | low",
      "estimated_lifespan": "string — how long the trend may last",
      "content_opportunity": "string — how to leverage this trend",
      "source": "string — where the data comes from",
      "confidence": "number 0.0–1.0",
      "first_observed": "date",
      "last_observed": "date"
    }
  ]
}
```

### 4.2 Rules

- Growth rates must be backed by data (mentions, engagement metrics)
- Trajectory must be based on at least 2 data points over time
- Estimated lifespan is a best-guess and should be labeled as such
- Low-confidence trends should be marked and monitored, not acted on immediately
- Each trend should have at least one associated content opportunity

---

## 5. Sources Format

All research must include properly formatted source citations.

### 5.1 Structure

```json
{
  "sources": [
    {
      "id": "src-1",
      "url": "string — full URL",
      "title": "string — page/article title",
      "publisher": "string — author or publication",
      "date_published": "string — ISO date",
      "date_accessed": "string — ISO date",
      "type": "article | report | study | data | social | forum | video | podcast",
      "credibility_tier": 1 | 2 | 3 | 4,
      "domain_authority": "string — if applicable",
      "summary": "string — brief summary of key takeaways",
      "used_for": "string — which findings this source supports",
      "verified": "boolean",
      "access_status": "open | paywall | restricted | archived"
    }
  ]
}
```

### 5.2 Credibility Tiers

| Tier | Source Type | Examples |
|------|-------------|----------|
| 1 | Primary / Original | Government data, academic papers, official reports |
| 2 | Reputable journalism | Major news outlets, industry publications |
| 3 | Industry sources | Expert blogs, company communications, verified social |
| 4 | Community sources | Forums, social media comments, user-generated |

### 5.3 Rules

- Every factual claim must have at least one source
- At least 50% of sources should be Tier 1 or Tier 2
- Tier 4 sources must be clearly flagged as anecdotal
- Paywall sources must be noted with access_status: "paywall"
- All URLs must be verified and accessible at time of research
- Sources should be checked for accuracy before being used

---

## 6. Claims Format

Every claim made in research must be tracked and categorized.

### 6.1 Structure

```json
{
  "claims": [
    {
      "id": "claim-1",
      "claim": "string — the exact claim being made",
      "type": "factual | opinion | prediction | inference | hypothesis",
      "status": "verified | unverified | partially-verified | disputed",
      "source_refs": ["string — source IDs"],
      "confidence": "number 0.0–1.0",
      "verification_method": "string — how this was verified",
      "counter_evidence": ["string"],
      "fact_check_agent_notes": "string",
      "published": "boolean",
      "publication_context": "string — where this claim appears"
    }
  ]
}
```

### 6.2 Claim Types

| Type | Description | Verification Required |
|------|-------------|----------------------|
| **Factual** | Objective, verifiable statement | Must be verified by Fact Check agent |
| **Opinion** | Subjective perspective | Labeled as opinion, not presented as fact |
| **Prediction** | Forward-looking statement | Confidence score required, labeled as prediction |
| **Inference** | Conclusion drawn from data | Method must be explained |
| **Hypothesis** | Proposed explanation | Labeled as hypothesis, not fact |

### 6.3 Claim Rules

- Factual claims MUST be verified before publication
- Opinions must be clearly labeled and attributed
- Predictions must include confidence scores
- Disputed claims must have counter-evidence documented
- No claim with confidence below 0.4 should be published
- Every claim must have a source reference or be flagged as original analysis

---

## 7. Confidence Scoring Methodology

All research outputs include confidence scores for findings, trends, and claims.

### 7.1 Confidence Scale

| Score Range | Level | Meaning |
|-------------|-------|---------|
| 0.9–1.0 | Very High | Multiple primary sources confirm |
| 0.7–0.89 | High | Strong secondary sources, consistent evidence |
| 0.5–0.69 | Medium | Some evidence, possible bias or limitation |
| 0.3–0.49 | Low | Limited evidence, speculative |
| 0.0–0.29 | Very Low | Minimal evidence, highly speculative |

### 7.2 Scoring Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| **Source quality** | 30% | Tier 1–4 credibility weighting |
| **Sample size** | 20% | Larger samples increase confidence |
| **Recency** | 15% | More recent data increases confidence |
| **Consistency** | 15% | Multiple sources agreeing increases confidence |
| **Methodology** | 10% | Sound methodology increases confidence |
| **Verification** | 10% | Fact-checked or peer-reviewed increases confidence |

### 7.3 Confidence Calculation

```
Confidence = (SourceQuality × 0.30) + (SampleSize × 0.20) + (Recency × 0.15) + 
             (Consistency × 0.15) + (Methodology × 0.10) + (Verification × 0.10)
```

Each factor is scored 0–1, then weighted and summed.

### 7.4 Minimum Confidence Thresholds

| Research Output | Minimum Confidence |
|-----------------|-------------------|
| Key Finding | 0.5 |
| Trend Identification | 0.6 |
| Claim (factual) | 0.7 |
| Claim (opinion) | 0.3 |
| Claim (prediction) | 0.5 |
| Audience Question | 0.4 (based on observed volume) |

### 7.5 Low Confidence Handling

- Research with overall confidence below 0.5 is flagged as "incomplete"
- Low-confidence findings are marked and require additional research
- Content based on low-confidence research must include disclaimers
- Low-confidence findings should not be used as the sole basis for strategy decisions

---

## 8. Research Template Variants

### 8.1 Quick Research Template

For fast, focused research (1–2 agent calls):

```json
{
  "research_id": "quick-YYYYMMDD-NNN",
  "timestamp": "ISO 8601",
  "agent_id": "string",
  "topic": "string",
  "query": "string",
  "status": "complete | partial",
  "key_findings": [
    {
      "finding": "string",
      "significance": "high | medium | low",
      "source_refs": [],
      "confidence": 0.0–1.0
    }
  ],
  "sources": [],
  "quality_flags": [],
  "next_steps": []
}
```

### 8.2 Deep Research Template

For comprehensive research projects (full agent pipeline):

```json
{
  "research_id": "deep-YYYYMMDD-NNN",
  "timestamp": "ISO 8601",
  "agent_id": "string",
  "topic": "string",
  "query": "string",
  "status": "complete | partial | incomplete",
  "confidence_score": 0.0–1.0,
  "key_findings": [],
  "audience_questions": [],
  "trends": [],
  "sources": [],
  "claims": [],
  "metadata": {
    "platforms_researched": [],
    "time_spent_minutes": 0,
    "agents_involved": [],
    "fact_check_passed": false,
    "qa_passed": false
  },
  "quality_flags": [],
  "next_steps": []
}
```

### 8.3 Competitive Analysis Template

```json
{
  "research_id": "comp-YYYYMMDD-NNN",
  "timestamp": "ISO 8601",
  "agent_id": "string",
  "topic": "string",
  "query": "string",
  "competitors": [
    {
      "name": "string",
      "url": "string",
      "strengths": [],
      "weaknesses": [],
      "content_gap": "string",
      "opportunity": "string"
    }
  ],
  "key_findings": [],
  "trends": [],
  "sources": [],
  "claims": [],
  "quality_flags": [],
  "next_steps": []
}
```

### 8.4 Trend Analysis Template

```json
{
  "research_id": "trend-YYYYMMDD-NNN",
  "timestamp": "ISO 8601",
  "agent_id": "string",
  "topic": "string",
  "query": "string",
  "trends": [
    {
      "name": "string",
      "description": "string",
      "platform": "string",
      "growth_rate": 0.0–1.0,
      "trajectory": "rising | stable | declining | peaking",
      "relevance": "high | medium | low",
      "estimated_lifespan": "string",
      "content_opportunity": "string",
      "source": "string",
      "confidence": 0.0–1.0
    }
  ],
  "key_findings": [],
  "sources": [],
  "quality_flags": [],
  "next_steps": []
}
```

---

## 9. Research Output Validation

### 9.1 Mandatory Fields Check

Every research output must pass these checks before being accepted:

- [ ] `research_id` is unique and formatted correctly
- [ ] `timestamp` is in ISO 8601 format
- [ ] `agent_id` matches a registered agent
- [ ] `topic` and `query` are non-empty strings
- [ ] `status` is one of the allowed values
- [ ] `confidence_score` is a number between 0.0 and 1.0
- [ ] At least one source is included (if factual claims are made)
- [ ] All claims have a `type` and `status`
- [ ] All sources have a `credibility_tier`
- [ ] `quality_flags` array is present (even if empty)
- [ ] `next_steps` array is present (even if empty)

### 9.2 Quality Gates

| Gate | Check | Fails If |
|------|-------|----------|
| **Research Gate** | All required fields present | Missing any mandatory field |
| **Fact Check Gate** | All claims verified or flagged | Unverified factual claims |
| **QA Gate** | Format compliance | Format doesn't match schema |
| **Confidence Gate** | Confidence thresholds met | Any finding below minimum confidence |
| **Source Gate** | Sources valid and accessible | Dead links or unverified sources |

---

## 10. Notes

- All templates are machine-readable — designed for agent consumption
- JSON schema should be validated before processing
- Research IDs follow the format: `{type}-YYYYMMDD-{NNN}`
- Timestamps are always in Australian Eastern Time (AEST/AEDT)
- Research files are stored in the Obsidian vault under `Research/`
- The Fact Check agent validates all claims before publication
- Confidence scores are recalculated when new evidence becomes available
- Template variants can be combined (e.g., a deep research can include competitive analysis)
- All templates are stored in `knowledge/research/research_templates.md` and the Obsidian vault
