"""MCP tool: keyword search on PubMed via NCBI E-utilities."""

import json
import os
import re
import sys

from ..lib.http import NCBI_API_KEY, ncbi_params, request_with_retry
from ..lib.pubmed import fetch_abstracts_from_pubmed

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
BATCH_SIZE = 200


def _extract_doi(articleids: list[dict]) -> str:
    for aid in articleids:
        if aid.get("idtype") == "doi":
            return aid.get("value", "")
    return ""


def _extract_year(pubdate: str) -> str:
    m = re.match(r"(\d{4})", pubdate or "")
    return m.group(1) if m else ""


def _summary_to_record(pmid: str, doc: dict, abstract: str) -> dict | None:
    title = doc.get("title", "")
    if not title:
        return None
    authors_raw = doc.get("authors") or []
    authors = [a.get("name", "") for a in authors_raw if a.get("name")]
    record = {
        "title": title,
        "authors": authors,
        "year": _extract_year(doc.get("pubdate", "")),
        "doi": _extract_doi(doc.get("articleids") or []),
        "pmid": pmid,
        "journal": doc.get("fulljournalname", ""),
        "abstract": abstract,
        "citations": 0,
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        "source": "PubMed-search",
        "publication_type": doc.get("pubtype") or [],
    }
    if authors:
        record["first_author"] = re.split(r"[,\s]", authors[0])[0]
    return record


def search_pubmed(
    query: str,
    *,
    date_start: str | None = None,
    date_end: str | None = None,
    limit: int = 200,
    output_path: str | None = None,
) -> dict:
    search_params = {
        "db": "pubmed",
        "retmode": "json",
        "retmax": limit,
        "sort": "relevance",
        "term": query,
    }
    if date_start or date_end:
        search_params["datetype"] = "pdat"
        if date_start:
            search_params["mindate"] = date_start
        if date_end:
            search_params["maxdate"] = date_end

    try:
        resp = request_with_retry(
            "GET",
            ESEARCH_URL,
            params=ncbi_params(search_params),
            timeout=15,
        )
        resp.raise_for_status()
        body = resp.json()
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "has_api_key": bool(NCBI_API_KEY),
            "results": [],
            "total_in_pubmed": 0,
        }

    esearch = body.get("esearchresult", {})
    total = int(esearch.get("count", 0))
    pmids = esearch.get("idlist", [])

    if not pmids:
        return {
            "status": "ok",
            "has_api_key": bool(NCBI_API_KEY),
            "query": query,
            "total_in_pubmed": total,
            "returned": 0,
            "output_path": output_path,
            "results": [],
        }

    summaries: dict[str, dict] = {}
    for start in range(0, len(pmids), BATCH_SIZE):
        batch = pmids[start : start + BATCH_SIZE]
        ids = ",".join(batch)
        try:
            resp = request_with_retry(
                "GET",
                ESUMMARY_URL,
                params=ncbi_params({"db": "pubmed", "retmode": "json", "id": ids}),
                timeout=15,
            )
            resp.raise_for_status()
            result = resp.json().get("result", {})
            for pmid in batch:
                if pmid in result:
                    summaries[pmid] = result[pmid]
        except Exception as e:
            print(
                f"  Warning: esummary batch failed ({len(batch)} PMIDs): {e}",
                file=sys.stderr,
            )
            continue

    abstracts = fetch_abstracts_from_pubmed(pmids)

    records = []
    for pmid in pmids:
        doc = summaries.get(pmid)
        if not doc:
            continue
        rec = _summary_to_record(pmid, doc, abstracts.get(pmid, ""))
        if rec:
            records.append(rec)

    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

    return {
        "status": "ok",
        "has_api_key": bool(NCBI_API_KEY),
        "query": query,
        "total_in_pubmed": total,
        "returned": len(records),
        "output_path": output_path,
        "results": records if not output_path else [],
    }
