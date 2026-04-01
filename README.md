# litrev

A Claude Code skill suite that conducts systematic, scoping, narrative, rapid, and meta-analytic literature reviews on medical and health research topics.
Searches PubMed/MEDLINE, Semantic Scholar, and OpenAlex, screens articles, extracts claims, writes a thematic synthesis with Pandoc citations, and verifies every reference against CrossRef and PubMed.

## Architecture

Hybrid architecture: **sub-skills** handle LLM reasoning (search strategy, screening decisions, synthesis writing), while a **MCP server** (`litrev-mcp`) handles deterministic execution (API calls, deduplication, BibTeX generation, claim verification). **Agents** handle post-pipeline quality audits.

The orchestrator (`litrev`) handles planning, sequencing, and quality gates.

```
litrev/                     ← orchestrator (sequencing + gates)
├── agents/
│   ├── audit_fidelity.md   ← Phase 8: fidelity audit (claims vs sources)
│   └── audit_methodology.md ← Phase 8: methodology audit (synthesis critique)
litrev-search/              ← Phase 2: search strategy (LLM) + MCP execution
litrev-screen/              ← Phase 3: screening decisions (LLM) + MCP abstract fetch
litrev-extract/             ← Phase 4: claim extraction (LLM) + MCP regex extraction
litrev-synthesize/          ← Phase 5: constrained thematic writing (LLM only)
litrev-mcp/                 ← MCP server: 8 deterministic tools
```

### MCP tools (`litrev-mcp`)

| Tool | Purpose |
|------|---------|
| `process_results` | Deduplicate, rank, filter, format search results |
| `deduplicate_results` | Deduplicate combined_results.json by PMID/DOI/title |
| `fetch_abstracts` | Retrieve missing abstracts from PubMed |
| `extract_claims_regex` | Quantitative claim extraction by regex |
| `citation_chain` | Backward/forward citation chaining via Semantic Scholar + OpenAlex |
| `verify_dois` | DOI/PMID validation + retraction check (CrossRef + PubMed) |
| `generate_bibliography` | BibTeX generation (3-level DOI resolution) |
| `audit_claims` | Cross-verify numerical claims vs source abstracts |

### Design principles

- **Hybrid**: LLM reasoning in skills, deterministic execution in MCP tools
- **Interface contracts**: phases communicate through well-defined JSON and markdown files in `review/`
- **Lightweight orchestrator**: sequencing and gate checks only, no domain logic
- **Session resumable**: pipeline state persisted to `review/` files
- **Double audit**: fidelity + methodology audits with interactive walkthrough before completion

### Pipeline flow

```
Planning → Search → Screen → Snowball (optional) → Extract → Synthesize → Verify → Final QC → Double Audit + Walkthrough
```

| Phase | Delegate | What it does |
|-------|----------|--------------|
| 1 | `litrev` | Define research question (PICO/PEO/SPIDER), scope, inclusion/exclusion criteria |
| 2 | Skill `litrev-search` + MCP `process_results`, `deduplicate_results` | Query databases, deduplicate and rank results |
| 3a | Skill `litrev-screen` + MCP `fetch_abstracts` | Multi-pass title/abstract/full-text screening with PRISMA counts |
| 3b | MCP `citation_chain` + inline screening | Backward and forward citation chaining |
| 4 | Skill `litrev-extract` + MCP `extract_claims_regex` | Claim extraction, quality assessment, theme assignment |
| 5 | Skill `litrev-synthesize` | Constrained thematic writing — every claim traced to source |
| 6 | MCP `verify_dois` + `generate_bibliography` + `audit_claims` | DOI validation, BibTeX generation, claims audit |
| 7 | `litrev` | Final quality checklist (10 items) |
| 8 | Agent `audit_fidelity` + Agent `audit_methodology` + `/review-walkthrough` | Fidelity + methodology audit, interactive walkthrough |

### Review types

| Type | Min. databases | Snowballing | Quality assessment | PRISMA |
|------|:-:|---|---|---|
| Systematic | 3 | Automatic (both directions) | Full (RoB/GRADE) | PRISMA 2020 |
| Meta-analysis | 3 | Automatic (both directions) | Full (RoB/GRADE) | PRISMA 2020 |
| Scoping | 3 | Suggested (both directions) | Optional (PRISMA-ScR) | PRISMA-ScR |
| Narrative | 2 | Suggested (backward only) | Simplified | Simplified |
| Rapid | 2 | Suggested (forward, cap 5 seeds) | Simplified | Simplified |

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed and authenticated
- Python >= 3.11 with [uv](https://docs.astral.sh/uv/)
- Internet access (PubMed, Semantic Scholar, OpenAlex, CrossRef, doi.org APIs)

### Install the MCP server

```bash
cd ~/.claude/skills/litrev-mcp
uv venv .venv && uv pip install -e . --python .venv/bin/python
```

The MCP server is configured in `~/.claude/.mcp.json`:

```json
{
  "litrev-mcp": {
    "type": "stdio",
    "command": "~/.claude/skills/litrev-mcp/.venv/bin/python",
    "args": ["-m", "litrev_mcp.server"],
    "env": {
      "LITREV_EMAIL": "you@example.com",
      "NCBI_API_KEY": "your-key-here",
      "S2_API_KEY": "your-key-here"
    }
  }
}
```

### Optional: environment variables

The litrev-mcp server works without these, but setting them improves rate limits and API compliance.
Configure them in your MCP client `env` block or shell environment.

| Variable | Effect |
|---|---|
| `LITREV_EMAIL` | Your email — activates polite pool (faster rates) for NCBI, CrossRef, OpenAlex. Falls back to `NCBI_EMAIL`. |
| `NCBI_API_KEY` | Raises PubMed rate limit from 3 to 10 req/s. Free at https://www.ncbi.nlm.nih.gov/account/settings/ |
| `S2_API_KEY` | Raises Semantic Scholar rate limit from ~1 to 100 req/s. Free at https://www.semanticscholar.org/product/api#api-key |

## Usage

### Full review (orchestrated)

Navigate to any directory where you want the review output, then ask Claude Code:

```
Fais-moi une revue systématique sur les probiotiques dans le traitement des infections récurrentes à C. difficile
```

```
What does the evidence say about rotator cuff comorbidities in shoulder pain?
```

```
Revue de la littérature sur l'impact du diabète sur la chirurgie de la coiffe des rotateurs
```

The orchestrator triggers automatically, guides you through planning, and runs each phase sequentially.
All output goes to `review/` in the current directory.

See [PROMPT_RECOS.md](PROMPT_RECOS.md) for tips on writing effective prompts (exclusion criteria, framework, review type, grey literature).

### Individual phases (standalone)

Each sub-skill can be invoked independently:

```
/litrev-search
/litrev-screen
/litrev-extract
/litrev-synthesize
```

MCP tools can also be called directly by the LLM when needed.

### Resuming a review

If a review is interrupted, simply re-invoke the skill in the same directory.
The orchestrator detects existing files in `review/` and resumes from the first incomplete phase.

## Output

All files are written to `review/` in the current working directory:

| File | Content |
|------|---------|
| `protocol.md` | Research question, framework, criteria, search strategy |
| `combined_results.json` | Aggregated, deduplicated search results |
| `search_results.md` | Ranked results table |
| `search_log.md` | Search documentation (queries, databases, counts) |
| `screening_log.md` | Screening decisions with PRISMA flow |
| `included_indices.json` | Indices of included articles |
| `extracted_claims.json` | Structured claims with quality ratings and themes |
| `<topic>_review.md` | The review document (Pandoc markdown with `[@citations]`) |
| `references.bib` | Verified BibTeX bibliography |
| `claims_audit.json` | Cross-verification of every numerical claim |
| `<topic>_review_citation_report.json` | DOI/PMID verification results |
| `vancouver.csl` | Citation style file |
| `audit_fidelity.md` | Fidelity audit report (claims vs sources) |
| `audit_methodology.md` | Methodology audit report (synthesis critique) |
| `DEFERRED.md` | Deferred findings with justifications (if any) |

The review document can be compiled to PDF, DOCX, or HTML with Pandoc:

```bash
cd review
pandoc <topic>_review.md --citeproc --bibliography=references.bib --csl=vancouver.csl -o review.pdf
```

## Example

See [example/](example/) for a complete end-to-end run (all 8 phases including double audit with walkthrough).
