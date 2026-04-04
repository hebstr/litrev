"""Metadata enrichment for imported records.

Sparse records (bare PMIDs/DOIs) get full metadata from PubMed and CrossRef.
Complete records (BibTeX/RIS imports) only fill missing abstracts and citation counts.
"""

import re
import sys
import xml.etree.ElementTree as ET

from .http import (
    request_with_retry,
    ncbi_params,
    OA_CLIENT,
    LITREV_EMAIL,
    _CROSSREF_CLIENT,
)
from .pubmed import fetch_abstracts_from_pubmed, EFETCH_URL

ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
CROSSREF_WORKS_URL = "https://api.crossref.org/works"
OA_WORKS_URL = "https://api.openalex.org/works"
BATCH_SIZE = 200


def _is_sparse(record: dict) -> bool:
    return not record.get("title")


def _extract_year(date_str: str) -> str:
    m = re.match(r"(\d{4})", date_str or "")
    return m.group(1) if m else ""


def _extract_doi_from_articleids(articleids: list[dict]) -> str:
    for aid in articleids:
        if aid.get("idtype") == "doi":
            return aid.get("value", "")
    return ""


def _enrich_pmids_from_pubmed(records: list[dict]) -> None:
    sparse_pmids = [r["pmid"] for r in records if r.get("pmid") and _is_sparse(r)]
    if not sparse_pmids:
        return

    summaries: dict[str, dict] = {}
    for start in range(0, len(sparse_pmids), BATCH_SIZE):
        batch = sparse_pmids[start : start + BATCH_SIZE]
        ids = ",".join(batch)
        try:
            resp = request_with_retry(
                "GET",
                ESUMMARY_URL,
                params=ncbi_params({"db": "pubmed", "retmode": "json", "id": ids}),
                timeout=30,
            )
            resp.raise_for_status()
            result = resp.json().get("result", {})
            for pmid in batch:
                if pmid in result:
                    summaries[pmid] = result[pmid]
        except Exception as e:
            print(f"  Warning: PubMed esummary batch failed: {e}", file=sys.stderr)

    abstracts = fetch_abstracts_from_pubmed(sparse_pmids)

    for r in records:
        pmid = r.get("pmid", "")
        if not pmid or not _is_sparse(r):
            continue
        doc = summaries.get(pmid)
        if not doc:
            continue
        r["title"] = doc.get("title", "")
        authors_raw = doc.get("authors") or []
        r["authors"] = [a.get("name", "") for a in authors_raw if a.get("name")]
        r["year"] = _extract_year(doc.get("pubdate", ""))
        r["doi"] = r["doi"] or _extract_doi_from_articleids(doc.get("articleids") or [])
        r["journal"] = doc.get("fulljournalname", "")
        r["abstract"] = abstracts.get(pmid, "")
        if r["authors"]:
            r["first_author"] = re.split(r"[,\s]", r["authors"][0])[0]


def _enrich_dois_from_crossref(records: list[dict]) -> None:
    sparse_dois = [r for r in records if r.get("doi") and _is_sparse(r)]
    if not sparse_dois:
        return

    for r in sparse_dois:
        doi = r["doi"]
        try:
            resp = request_with_retry(
                "GET",
                f"{CROSSREF_WORKS_URL}/{doi}",
                client=_CROSSREF_CLIENT,
                timeout=15,
            )
            if resp.status_code != 200:
                continue
            work = resp.json().get("message", {})
        except Exception as e:
            print(f"  Warning: CrossRef lookup failed for {doi}: {e}", file=sys.stderr)
            continue

        title_parts = work.get("title") or []
        r["title"] = title_parts[0] if title_parts else ""

        authors_raw = work.get("author") or []
        r["authors"] = [
            f"{a.get('family', '')}, {a.get('given', '')}".strip(", ")
            for a in authors_raw
        ]

        issued = work.get("issued") or {}
        date_parts = (issued.get("date-parts") or [[]])[0]
        r["year"] = str(date_parts[0]) if date_parts else ""

        container = work.get("container-title") or []
        r["journal"] = container[0] if container else ""

        r["abstract"] = re.sub(r"<[^>]+>", "", work.get("abstract", ""))

        r["citations"] = work.get("is-referenced-by-count") or 0

        if r["authors"]:
            r["first_author"] = re.split(r"[,\s]", r["authors"][0])[0]


def _fill_missing_abstracts(records: list[dict]) -> None:
    need_abstract = [r for r in records if not r.get("abstract") and r.get("pmid")]
    if not need_abstract:
        return
    pmids = [r["pmid"] for r in need_abstract]
    abstracts = fetch_abstracts_from_pubmed(pmids)
    for r in need_abstract:
        ab = abstracts.get(r["pmid"], "")
        if ab:
            r["abstract"] = ab


def _fill_citation_counts(records: list[dict]) -> None:
    need_counts = [r for r in records if not r.get("citations") and r.get("doi")]
    if not need_counts:
        return

    for batch_start in range(0, len(need_counts), 50):
        batch = need_counts[batch_start : batch_start + 50]
        doi_filter = "|".join(f"https://doi.org/{r['doi']}" for r in batch)
        params: dict = {
            "filter": f"doi:{doi_filter}",
            "select": "doi,cited_by_count",
            "per_page": 50,
        }
        if LITREV_EMAIL:
            params["mailto"] = LITREV_EMAIL

        try:
            resp = request_with_retry(
                "GET",
                OA_WORKS_URL,
                params=params,
                timeout=15,
                client=OA_CLIENT,
            )
            if resp.status_code != 200:
                continue
            results = resp.json().get("results") or []
        except Exception as e:
            print(
                f"  Warning: OpenAlex citation count batch failed: {e}", file=sys.stderr
            )
            continue

        doi_to_count: dict[str, int] = {}
        for w in results:
            raw_doi = (w.get("doi") or "").replace("https://doi.org/", "").lower()
            if raw_doi:
                doi_to_count[raw_doi] = w.get("cited_by_count") or 0

        for r in batch:
            count = doi_to_count.get(r["doi"].lower())
            if count:
                r["citations"] = count


def enrich_records(records: list[dict]) -> dict:
    """Enrich imported records with metadata from PubMed, CrossRef, OpenAlex.

    Modifies records in place and returns enrichment stats.
    """
    before_sparse = sum(1 for r in records if _is_sparse(r))

    _enrich_pmids_from_pubmed(records)
    _enrich_dois_from_crossref(records)
    _fill_missing_abstracts(records)
    _fill_citation_counts(records)

    after_sparse = sum(1 for r in records if _is_sparse(r))

    return {
        "total": len(records),
        "enriched": before_sparse - after_sparse,
        "still_sparse": after_sparse,
        "with_abstract": sum(1 for r in records if r.get("abstract")),
        "with_citations": sum(1 for r in records if r.get("citations")),
    }
