# litrev-mcp

MCP server for systematic literature reviews.
Provides search processing, screening support, citation chaining, claim extraction, verification, and bibliography generation — designed to be driven by an LLM client via the Model Context Protocol.

## Install

Requires Python ≥ 3.11 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync # install dependencies
uv sync --group dev # include pytest for development
```

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `LITREV_EMAIL` | **recommended** | Your email — used for NCBI, CrossRef, and OpenAlex polite pools (faster rate limits). Falls back to `NCBI_EMAIL` for backward compatibility. |
| `NCBI_API_KEY` | no | NCBI API key — raises rate limit from 3 to 10 req/s. Free key at [ncbi.nlm.nih.gov/account/settings](https://www.ncbi.nlm.nih.gov/account/settings/) (requires NCBI account). |
| `S2_API_KEY` | no | Semantic Scholar API key — raises rate limit from ~1 to 100 req/s. Free key available at [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api#api-key). |

## MCP tools

| Tool | Description |
|---|---|
| `process_results` | Deduplicate, rank, filter, and format search results |
| `deduplicate_results` | Deduplicate combined_results.json by PMID/DOI/title |
| `search_pubmed` | Search PubMed/MEDLINE via NCBI E-utilities |
| `search_s2` | Search Semantic Scholar Academic Graph API |
| `search_openalex` | Search OpenAlex works API |
| `fetch_abstracts` | Fetch missing abstracts from PubMed for screening |
| `fetch_fulltext` | Full-text retrieval via PMC/Unpaywall/S2 cascade |
| `get_section` | Extract a specific section from cached full text |
| `extract_claims_regex` | Regex-based quantitative claim extraction from abstracts |
| `citation_chain` | Backward/forward citation chaining via Semantic Scholar + OpenAlex |
| `verify_dois` | Validate DOIs/PMIDs and check for retractions |
| `generate_bibliography` | 3-level DOI resolution to BibTeX |
| `audit_claims` | Cross-verify numbers in review vs extracted claims |
| `validate_gate` | Mechanical gate validation for review pipeline phases |
| `import_corpus` | Import user-supplied bibliographic files (BibTeX, RIS, CSV, TSV, PMIDs, DOIs) |

## MCP client configuration

```json
{
  "mcpServers": {
    "litrev-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/litrev-mcp", "litrev-mcp"],
      "env": {
        "LITREV_EMAIL": "you@example.com",
        "S2_API_KEY": "your-key-here"
      }
    }
  }
}
```
