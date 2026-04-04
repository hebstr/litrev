"""Import format parsers: BibTeX, RIS, CSV Scopus, TSV WoS, PMID list, DOI list.

Each parser is a pure function (str → list[dict]) producing normalised records
matching the shared result schema. No I/O — callers handle file reading.
"""

import csv
import io
import re
from typing import Literal

_DOI_RE = re.compile(r"10\.\d{4,}/[^\s>,\"'}\]]+")
_PMID_RE = re.compile(r"^\d{5,9}$")

Format = Literal["bibtex", "ris", "scopus_csv", "wos_tsv", "pmid_list", "doi_list"]


def detect_format(text: str) -> Format:
    stripped = text.lstrip()
    if stripped.startswith("@"):
        return "bibtex"
    if stripped.startswith("TY  -"):
        return "ris"
    first_line = stripped.split("\n", 1)[0]
    if "\t" in first_line and any(h in first_line for h in ("AU", "TI", "DI", "PT")):
        return "wos_tsv"
    if "," in first_line and any(
        h in first_line for h in ("Authors", "Title", "DOI", "Source title")
    ):
        return "scopus_csv"
    non_empty = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    if non_empty and all(_PMID_RE.match(ln) for ln in non_empty):
        return "pmid_list"
    if non_empty and all(_DOI_RE.match(ln) for ln in non_empty):
        return "doi_list"
    raise ValueError(
        "Cannot detect import format. Supported: BibTeX, RIS, "
        "Scopus CSV, WoS TSV, PMID list, DOI list."
    )


def parse(text: str, fmt: Format | None = None) -> list[dict]:
    if fmt is None:
        fmt = detect_format(text)
    dispatcher: dict[Format, object] = {
        "bibtex": parse_bibtex,
        "ris": parse_ris,
        "scopus_csv": parse_scopus_csv,
        "wos_tsv": parse_wos_tsv,
        "pmid_list": parse_pmid_list,
        "doi_list": parse_doi_list,
    }
    return dispatcher[fmt](text)


_BIB_ENTRY_RE = re.compile(r"@(\w+)\{([^,]*),", re.IGNORECASE)
_BIB_FIELD_RE = re.compile(
    r"(\w+)\s*=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|\"([^\"]*)\"|(\d+))",
    re.DOTALL,
)


def _unescape_bibtex(value: str) -> str:
    value = re.sub(r"\\[&%#_$]", lambda m: m.group(0)[1], value)
    value = value.replace(r"\textasciitilde{}", "~")
    value = value.replace(r"\textasciicircum{}", "^")
    value = re.sub(r"\{(.+?)\}", r"\1", value)
    return value.strip()


def _bibtex_authors(raw: str) -> list[str]:
    parts = re.split(r"\s+and\s+", raw)
    authors = []
    for p in parts:
        name = _unescape_bibtex(p).strip()
        if name:
            authors.append(name)
    return authors


def parse_bibtex(text: str) -> list[dict]:
    entries = re.split(r"(?=@\w+\{)", text)
    records: list[dict] = []
    for entry in entries:
        header = _BIB_ENTRY_RE.search(entry)
        if not header:
            continue
        fields: dict[str, str] = {}
        for m in _BIB_FIELD_RE.finditer(entry):
            key = m.group(1).lower()
            val = (
                m.group(2)
                if m.group(2) is not None
                else (m.group(3) or m.group(4) or "")
            )
            fields[key] = val

        title = _unescape_bibtex(fields.get("title", ""))
        if not title:
            continue

        authors = _bibtex_authors(fields.get("author", ""))
        doi = fields.get("doi", "").strip().lower()
        pmid = fields.get("pmid", "").strip()
        year = fields.get("year", "")

        record: dict = {
            "title": title,
            "authors": authors,
            "year": year,
            "doi": doi,
            "pmid": pmid,
            "journal": _unescape_bibtex(fields.get("journal", "")),
            "abstract": _unescape_bibtex(fields.get("abstract", "")),
            "citations": 0,
            "url": "",
            "source": "import-bibtex",
        }
        if authors:
            record["first_author"] = re.split(r"[,\s]", authors[0])[0]
        if fields.get("volume"):
            record["volume"] = fields["volume"]
        if fields.get("pages"):
            record["pages"] = fields["pages"]
        records.append(record)
    return records


_RIS_TAG_RE = re.compile(r"^([A-Z][A-Z0-9])\s{2}-\s?(.*)")


def parse_ris(text: str) -> list[dict]:
    records: list[dict] = []
    current_fields: dict[str, list[str]] = {}

    def _flush():
        if not current_fields:
            return
        title = " ".join(current_fields.get("TI", current_fields.get("T1", [])))
        if not title:
            return
        authors = current_fields.get("AU", current_fields.get("A1", []))
        doi = " ".join(current_fields.get("DO", [])).strip()
        pmid_raw = " ".join(current_fields.get("AN", []))
        pmid = pmid_raw.strip() if pmid_raw.strip().isdigit() else ""
        year_raw = " ".join(current_fields.get("PY", current_fields.get("Y1", [])))
        year = (
            re.match(r"(\d{4})", year_raw).group(1)
            if re.match(r"(\d{4})", year_raw)
            else ""
        )
        journal = " ".join(
            current_fields.get(
                "JO", current_fields.get("JF", current_fields.get("T2", []))
            )
        )
        abstract = " ".join(current_fields.get("AB", current_fields.get("N2", [])))
        record: dict = {
            "title": title,
            "authors": authors,
            "year": year,
            "doi": doi,
            "pmid": pmid,
            "journal": journal,
            "abstract": abstract,
            "citations": 0,
            "url": " ".join(current_fields.get("UR", [])),
            "source": "import-ris",
        }
        if authors:
            record["first_author"] = re.split(r"[,\s]", authors[0])[0]
        vol = " ".join(current_fields.get("VL", []))
        if vol:
            record["volume"] = vol
        pages_start = " ".join(current_fields.get("SP", []))
        pages_end = " ".join(current_fields.get("EP", []))
        if pages_start:
            record["pages"] = f"{pages_start}-{pages_end}" if pages_end else pages_start
        records.append(record)

    for line in text.splitlines():
        tag_match = _RIS_TAG_RE.match(line)
        if tag_match:
            tag, value = tag_match.group(1), tag_match.group(2).strip()
            if tag == "ER":
                _flush()
                current_fields = {}
            else:
                current_fields.setdefault(tag, []).append(value)
    _flush()
    return records


_SCOPUS_COL_MAP = {
    "Authors": "authors",
    "Author full names": "authors_full",
    "Title": "title",
    "Year": "year",
    "DOI": "doi",
    "Source title": "journal",
    "Abstract": "abstract",
    "Cited by": "citations",
    "PubMed ID": "pmid",
    "Volume": "volume",
    "Page start": "page_start",
    "Page end": "page_end",
    "Link": "url",
    "Document Type": "type",
}


def parse_scopus_csv(text: str) -> list[dict]:
    reader = csv.DictReader(io.StringIO(text))
    records: list[dict] = []
    for row in reader:
        mapped = {v: row.get(k, "") for k, v in _SCOPUS_COL_MAP.items()}
        title = (mapped.get("title") or "").strip()
        if not title:
            continue

        authors_raw = mapped.get("authors_full") or mapped.get("authors") or ""
        authors = [a.strip() for a in authors_raw.split(";") if a.strip()]
        try:
            citations = int(mapped.get("citations") or 0)
        except (ValueError, TypeError):
            citations = 0

        record: dict = {
            "title": title,
            "authors": authors,
            "year": (mapped.get("year") or "").strip(),
            "doi": (mapped.get("doi") or "").strip().lower(),
            "pmid": (mapped.get("pmid") or "").strip(),
            "journal": (mapped.get("journal") or "").strip(),
            "abstract": (mapped.get("abstract") or "").strip(),
            "citations": citations,
            "url": (mapped.get("url") or "").strip(),
            "source": "import-scopus",
        }
        if authors:
            record["first_author"] = re.split(r"[,\s]", authors[0])[0]
        if mapped.get("volume"):
            record["volume"] = mapped["volume"].strip()
        ps = (mapped.get("page_start") or "").strip()
        pe = (mapped.get("page_end") or "").strip()
        if ps:
            record["pages"] = f"{ps}-{pe}" if pe else ps
        if mapped.get("type"):
            record["type"] = mapped["type"].strip()
        records.append(record)
    return records


_WOS_COL_MAP = {
    "AU": "authors",
    "AF": "authors_full",
    "TI": "title",
    "PY": "year",
    "DI": "doi",
    "SO": "journal",
    "AB": "abstract",
    "TC": "citations",
    "PM": "pmid",
    "VL": "volume",
    "BP": "page_start",
    "EP": "page_end",
    "UT": "ut",
    "DT": "type",
}


def parse_wos_tsv(text: str) -> list[dict]:
    reader = csv.DictReader(io.StringIO(text), delimiter="\t")
    records: list[dict] = []
    for row in reader:
        mapped = {v: row.get(k, "") for k, v in _WOS_COL_MAP.items()}
        title = (mapped.get("title") or "").strip()
        if not title:
            continue

        authors_raw = mapped.get("authors_full") or mapped.get("authors") or ""
        authors = [a.strip() for a in authors_raw.split(";") if a.strip()]
        try:
            citations = int(mapped.get("citations") or 0)
        except (ValueError, TypeError):
            citations = 0

        record: dict = {
            "title": title,
            "authors": authors,
            "year": (mapped.get("year") or "").strip(),
            "doi": (mapped.get("doi") or "").strip().lower(),
            "pmid": (mapped.get("pmid") or "").strip(),
            "journal": (mapped.get("journal") or "").strip(),
            "abstract": (mapped.get("abstract") or "").strip(),
            "citations": citations,
            "url": "",
            "source": "import-wos",
        }
        if mapped.get("ut"):
            record["url"] = (
                f"https://www.webofscience.com/wos/woscc/full-record/{mapped['ut'].strip()}"
            )
        if authors:
            record["first_author"] = re.split(r"[,\s]", authors[0])[0]
        if mapped.get("volume"):
            record["volume"] = mapped["volume"].strip()
        ps = (mapped.get("page_start") or "").strip()
        pe = (mapped.get("page_end") or "").strip()
        if ps:
            record["pages"] = f"{ps}-{pe}" if pe else ps
        if mapped.get("type"):
            record["type"] = mapped["type"].strip()
        records.append(record)
    return records


def parse_pmid_list(text: str) -> list[dict]:
    records: list[dict] = []
    for line in text.strip().splitlines():
        pmid = line.strip()
        if not pmid:
            continue
        records.append(
            {
                "title": "",
                "authors": [],
                "year": "",
                "doi": "",
                "pmid": pmid,
                "journal": "",
                "abstract": "",
                "citations": 0,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "source": "import-pmid",
            }
        )
    return records


def parse_doi_list(text: str) -> list[dict]:
    records: list[dict] = []
    for line in text.strip().splitlines():
        doi = line.strip()
        if not doi:
            continue
        records.append(
            {
                "title": "",
                "authors": [],
                "year": "",
                "doi": doi,
                "pmid": "",
                "journal": "",
                "abstract": "",
                "citations": 0,
                "url": f"https://doi.org/{doi}",
                "source": "import-doi",
            }
        )
    return records
