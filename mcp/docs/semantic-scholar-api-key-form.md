# Semantic Scholar API Key Request

Application use

```
Public (Free / Nonprofit)
```

How do you plan to use Semantic Scholar API in your project? (50 words or more)

```
I am building an open-source MCP (Model Context Protocol) server for systematic literature reviews in medical and health research. The tool assists researchers with citation chaining — discovering related papers by following reference lists and citing works from seed articles.

Endpoints used: I use the Graph API v1 exclusively:

GET /graph/v1/paper/{paper_id}/references — fetch a paper's reference list (backward chaining)
GET /graph/v1/paper/{paper_id}/citations — fetch papers that cite a given paper (forward chaining)
Paper IDs are resolved via DOI or PMID identifiers (DOI:…, PMID:…).

Fields requested: title, authors, year, externalIds, journal, citationCount, abstract, url — only metadata needed for screening and deduplication, no full text.

Usage pattern: A single researcher runs the tool locally during a review project. A typical session chains 5–20 seed papers, each producing one references call and one citations call (so roughly 10–40 requests per session). Sessions are infrequent — a few times per week during active review phases. Only one user per instance. Requests are rate-limited client-side to stay well within the default unauthenticated tier; the API key is requested to improve reliability and avoid 429 errors, not to reach high throughput.
```

Which endpoints do you plan to use?

```
GET /graph/v1/paper/{paper_id}/references (Paper References); GET /graph/v1/paper/{paper_id}/citations (Paper Citations)
```

How many requests per day do you anticipate using?

```
50-100
```
