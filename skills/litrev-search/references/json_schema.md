# JSON Schema for Search Results

Combined search results must be stored as a JSON array of objects in `review/combined_results.json`.

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | yes | Article title |
| `authors` | list[str] | yes | Author names (normalized to list by `deduplicate_results`) |
| `year` | string or int | yes | Publication year |
| `doi` | string | no | DOI identifier |
| `pmid` | string or int | no | PubMed ID |
| `journal` | string | no | Journal name |
| `volume` | string | no | Volume number |
| `pages` | string | no | Page range |
| `abstract` | string | no | Abstract text |
| `source` | string | no | Database(s) of origin, comma-separated if found in multiple (e.g. "PubMed", "PubMed, OpenAlex") |
| `study_type` | string | no | Study design (e.g. "rct", "cohort", "meta-analysis") |
| `publication_type` | string | no | Publication type |
| `citations` | int | no | Citation count |
| `relevance_score` | float | no | Relevance score |
| `type` | string | no | BibTeX entry type (default: "article") |
| `first_author` | string | no | First author last name (used for BibTeX key) |
| `url` | string | no | Article URL |
