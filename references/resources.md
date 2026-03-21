# Resources

## Bundled Resources

**Scripts:**
- `scripts/verify_citations.py`: Verify DOIs and PMIDs, check for retractions, generate JSON verification report
- `scripts/process_results.py`: Process, deduplicate, format search results (markdown, JSON, BibTeX, RIS — no API calls)
- `scripts/generate_bib.py`: Generate BibTeX bibliography by resolving DOIs via APIs (doi.org → CrossRef → PubMed) with cross-verification
- `scripts/extract_abstracts.py`: Extract abstracts for selected articles by row number or DOI (no API calls)
- `scripts/extract_data.py`: Extract quantitative claims from article abstracts into structured JSON (single source of truth for numbers)
- `scripts/verify_claims.py`: Cross-verify numerical claims in a review against extracted data, produce audit report
- `scripts/fetch_fulltext.py`: Fetch full-text articles (PMC → Unpaywall → Publisher → Sci-Hub) and enrich extracted claims
- `scripts/citation_chaining.py`: Backward/forward citation chaining via Semantic Scholar and OpenAlex APIs, with deduplication and merge
- `scripts/bibtex_keys.py`: Shared BibTeX key collision handling (used internally)
- `scripts/http_utils.py`: Shared HTTP retry logic (used internally by `verify_citations.py`, `generate_bib.py`, `citation_chaining.py`)

**References:**
- `references/bibtex_format.md`: BibTeX entry types, field conventions, formatting guide
- `references/database_strategies.md`: Comprehensive database search strategies
- `references/json_schema.md`: JSON schema for combined search results
- `references/paper_prioritization.md`: Citation thresholds, journal tiers, author assessment
- `references/best_practices.md`: Best practices and common pitfalls

**Assets:**
- `assets/review_template.md`: Complete literature review template
- `assets/vancouver.csl`: Vancouver (NLM/ICMJE) citation style

## External Resources

**Guidelines:**
- PRISMA (Systematic Reviews): http://www.prisma-statement.org/
- Cochrane Handbook: https://training.cochrane.org/handbook
- AMSTAR 2 (Review Quality): https://amstar.ca/

**Tools:**
- MeSH Browser: https://meshb.nlm.nih.gov/search
- PubMed Advanced Search: https://pubmed.ncbi.nlm.nih.gov/advanced/
- Boolean Search Guide: https://www.ncbi.nlm.nih.gov/books/NBK3827/

## Dependencies

**Python Packages:** `requests` is declared in `pyproject.toml`; `uv sync` installs it.

**System Tools:**
- Python >= 3.11
- uv (manages dependencies via `pyproject.toml`)
- pdftotext (from poppler-utils, used by `fetch_fulltext.py` for PDF conversion)

## Running Tests

```bash
uv run -m pytest tests/ -v
```
