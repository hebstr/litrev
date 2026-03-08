# Resources

## Bundled Resources

**Scripts:**
- `scripts/verify_citations.py`: Verify DOIs and PMIDs, check for retractions, generate JSON verification report
- `scripts/process_results.py`: Process, deduplicate, format search results (markdown, JSON, BibTeX, RIS — no API calls)
- `scripts/generate_bib.py`: Generate BibTeX bibliography by resolving DOIs via APIs (doi.org → CrossRef → PubMed) with cross-verification
- `scripts/extract_abstracts.py`: Extract abstracts for selected articles by row number or DOI (no API calls)
- `scripts/bibtex_keys.py`: Shared BibTeX key collision handling (used internally)
- `scripts/http_utils.py`: Shared HTTP retry logic (used internally by `verify_citations.py`, `generate_bib.py`)

**References:**
- `references/bibtex_format.md`: BibTeX entry types, field conventions, formatting guide
- `references/database_strategies.md`: Comprehensive database search strategies
- `references/json_schema.md`: JSON schema for combined search results
- `references/paper_prioritization.md`: Citation thresholds, journal tiers, author assessment
- `references/best_practices.md`: Best practices and common pitfalls

**Assets:**
- `assets/review_template.md`: Complete literature review template
- `assets/vancouver.csl`: Vancouver (NLM/ICMJE) citation style for Quarto rendering

## External Resources

**Guidelines:**
- PRISMA (Systematic Reviews): http://www.prisma-statement.org/
- Cochrane Handbook: https://training.cochrane.org/handbook
- AMSTAR 2 (Review Quality): https://amstar.ca/

**Tools:**
- MeSH Browser: https://meshb.nlm.nih.gov/search
- PubMed Advanced Search: https://pubmed.ncbi.nlm.nih.gov/advanced/
- Boolean Search Guide: https://www.ncbi.nlm.nih.gov/books/NBK3827/

## Integration with Other Skills

- **quarto-authoring**: Render systematic reviews as `.qmd` to PDF/HTML/DOCX with `.bib` + `.csl`, cross-references, and embedded R/Python code chunks for reproducible forest/funnel plots

## Dependencies

**Python Packages:** Scripts needing `requests` (`verify_citations.py`, `generate_bib.py`) are invoked via `uv run --with requests` — no manual install needed.

**System Tools:**
- Python >= 3.10
- uv (manages `requests` dependency at runtime)
- Quarto >= 1.4 (rendering .qmd to PDF/HTML/DOCX)

## Running Tests

```bash
uv run --with requests -m unittest discover -s tests -v
```

The `--with requests` flag is required because `verify_citations.py` and `generate_bib.py` import `requests` at module level.
