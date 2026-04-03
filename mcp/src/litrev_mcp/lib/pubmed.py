"""Shared PubMed efetch helpers."""

import xml.etree.ElementTree as ET

from .http import request_with_retry, ncbi_params


EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BATCH_SIZE = 200


def fetch_abstracts_from_pubmed(pmids: list[str]) -> dict[str, str]:
    if not pmids:
        return {}

    abstracts: dict[str, str] = {}
    pmid_list = list(pmids)

    for start in range(0, len(pmid_list), BATCH_SIZE):
        batch = pmid_list[start : start + BATCH_SIZE]
        ids = ",".join(str(p) for p in batch)

        try:
            resp = request_with_retry(
                "GET", EFETCH_URL,
                params=ncbi_params({"db": "pubmed", "retmode": "xml", "id": ids}),
                timeout=30,
            )
            resp.raise_for_status()
        except Exception:
            continue

        try:
            root = ET.fromstring(resp.content)
        except ET.ParseError:
            continue

        for article in root.findall(".//PubmedArticle"):
            pmid_el = article.find(".//PMID")
            if pmid_el is None or not pmid_el.text:
                continue
            pmid = pmid_el.text

            abstract_parts = []
            for ab in article.findall(".//AbstractText"):
                label = ab.get("Label", "")
                text = "".join(ab.itertext()).strip()
                if label:
                    abstract_parts.append(f"{label}: {text}")
                else:
                    abstract_parts.append(text)

            if abstract_parts:
                abstracts[pmid] = " ".join(abstract_parts)

    return abstracts
