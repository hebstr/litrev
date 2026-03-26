# litrev

A Claude Code skill suite that conducts systematic, scoping, narrative, rapid, and meta-analytic literature reviews on medical and health research topics.
Searches PubMed, Semantic Scholar, OpenAlex and other databases, screens articles, extracts claims, writes a thematic synthesis with Pandoc citations, and verifies every reference against CrossRef and PubMed.

## Architecture

The skill is decomposed into 7 standalone, self-contained sub-skills — each specialized in one phase of the review process.
The orchestrator (`litrev`) handles planning, sequencing, and quality gates. All domain work is delegated to sub-skills.

```
litrev/                     ← orchestrator (sequencing + gates)
litrev-search/              ← Phase 2: multi-database search, aggregation
litrev-screen/              ← Phase 3: title/abstract/full-text screening
litrev-snowball/            ← Phase 3b: citation chaining (backward/forward)
litrev-extract/             ← Phase 4: claim extraction + quality assessment
litrev-synthesize/          ← Phase 5: constrained thematic writing
litrev-verify/              ← Phase 6: citation verification, BibTeX, claims audit
```

### Design principles

- **Self-contained**: each sub-skill ships its own scripts, references, and Python dependencies — no cross-references between skills
- **Interface contracts**: skills communicate through well-defined JSON and markdown files in a shared `review/` directory
- **Lightweight orchestrator**: no domain-execution logic, just sequencing and gate checks
- **Session resumable**: the pipeline persists state to `review/` files, so a review can be resumed across sessions

### Pipeline flow

```
Planning → Search → Screen → Snowball (optional) → Extract → Synthesize → Verify → Final QC
```

| Phase | Skill | What it does |
|-------|-------|--------------|
| 1 | `litrev` | Define research question (PICO/PEO/SPIDER), scope, inclusion/exclusion criteria |
| 2 | `litrev-search` | Query PubMed, Semantic Scholar, OpenAlex; deduplicate and rank results |
| 3a | `litrev-screen` | Multi-pass title/abstract/full-text screening with PRISMA counts |
| 3b | `litrev-snowball` | Backward and forward citation chaining via Semantic Scholar and OpenAlex |
| 4 | `litrev-extract` | Quantitative/qualitative claim extraction, study quality assessment, theme assignment |
| 5 | `litrev-synthesize` | Constrained thematic writing — every claim traced to source or flagged unverified |
| 6 | `litrev-verify` | DOI/PMID validation, retraction check, BibTeX generation, numerical claims audit |
| 7 | `litrev` | Final quality checklist (10 items) |

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
- Python >= 3.11 with [uv](https://docs.astral.sh/uv/) (for sub-skill script dependencies)
- Internet access (PubMed, Semantic Scholar, OpenAlex, CrossRef, doi.org APIs)

### Install from marketplace

```bash
claude skills install litrev
```

This installs all 7 skills (`litrev`, `litrev-search`, `litrev-screen`, `litrev-snowball`, `litrev-extract`, `litrev-synthesize`, `litrev-verify`) into `~/.claude/skills/`.

### Install Python dependencies

Each sub-skill that uses Python scripts has its own `pyproject.toml`. Install dependencies once per skill:

```bash
for skill in litrev-search litrev-screen litrev-snowball litrev-extract litrev-verify; do
  cd ~/.claude/skills/$skill
  uv venv .venv && uv pip install -e . --python .venv/bin/python
done
```

`litrev-synthesize` has no Python dependencies (LLM-driven writing only).

### Optional: NCBI API key

PubMed queries work without authentication but are rate-limited to 3 requests/second.
For higher throughput, set your NCBI API key:

```bash
export NCBI_API_KEY=your_key_here
```

Get one for free at https://www.ncbi.nlm.nih.gov/account/settings/

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

### Individual phases (standalone)

Each sub-skill can be invoked independently. For example, to run only the search phase:

```
/litrev-search
```

Or to verify citations on an existing review document:

```
/litrev-verify
```

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

The review document can be compiled to PDF, DOCX, or HTML with Pandoc:

```bash
cd review
pandoc <topic>_review.md --citeproc --bibliography=references.bib --csl=vancouver.csl -o review.pdf
```

## Example

See [example/](example/) for a complete end-to-end run (PRISE scoping review on rotator cuff comorbidities and shoulder pain).
