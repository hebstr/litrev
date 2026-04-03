"""BibTeX key management, DOI extraction, and entry building.

Unified from verify version (most robust code block parsing).
"""

import os
import re


_DOI_PATTERN = re.compile(r'10\.\d{4,}/[^\s>,"\'}?#\]\}]+')

_BIBTEX_SPECIAL = str.maketrans(
    {
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "$": r"\$",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
)

_ALREADY_ESCAPED = re.compile(r"\\[&%#_$~^]")


def escape_bibtex(value: str) -> str:
    parts = _ALREADY_ESCAPED.split(value)
    escaped_parts = [p.translate(_BIBTEX_SPECIAL) for p in parts]
    separators = _ALREADY_ESCAPED.findall(value)
    result = escaped_parts[0]
    for sep, part in zip(separators, escaped_parts[1:]):
        result += sep + part
    return result


def _strip_trailing_parens(doi: str) -> str:
    while doi.endswith(")") and doi.count(")") > doi.count("("):
        doi = doi[:-1]
    return doi


def extract_doi_matches(text: str) -> list[str]:
    return list(
        dict.fromkeys(
            _strip_trailing_parens(doi.rstrip(".,;:"))
            for doi in _DOI_PATTERN.findall(text)
        )
    )


_CODE_BLOCK_RE = re.compile(r"^(`{3,})(\w*)\s*\n.*?\n\1\s*$", re.DOTALL | re.MULTILINE)


def strip_code_blocks(text: str, keep_bibtex: bool = False) -> str:
    if keep_bibtex:
        return _CODE_BLOCK_RE.sub(
            lambda m: m.group(0) if m.group(2).lower() == "bibtex" else "", text
        )
    return _CODE_BLOCK_RE.sub("", text)


_BIB_ENTRY_PATTERN = re.compile(r"@\w+\{([\w-]+),")
_BIB_DOI_PATTERN = re.compile(r"doi\s*=\s*\{([^}]+)\}", re.IGNORECASE)
_BIB_PMID_PATTERN = re.compile(r"pmid\s*=\s*\{(\d+)\}", re.IGNORECASE)


def extract_pmid_entries(text: str) -> dict[str, dict]:
    entries = re.split(r"(?=@\w+\{)", text)
    pmid_map: dict[str, dict] = {}
    for entry in entries:
        key_match = _BIB_ENTRY_PATTERN.search(entry)
        pmid_match = _BIB_PMID_PATTERN.search(entry)
        if key_match and pmid_match:
            doi_match = _BIB_DOI_PATTERN.search(entry)
            year_m = re.search(r"year\s*=\s*\{?(\d{4})", entry)
            author_m = re.search(r"author\s*=\s*\{(.+?)\}", entry, re.DOTALL)
            title_m = re.search(r"title\s*=\s*\{(.+?)\}", entry, re.DOTALL)
            first_author = ""
            if author_m:
                first_author = re.split(
                    r"[,\s]", author_m.group(1).split(" and ")[0].strip()
                )[0]
            pmid_map[pmid_match.group(1)] = {
                "key": key_match.group(1),
                "has_doi": bool(doi_match),
                "author": first_author,
                "year": year_m.group(1) if year_m else "",
                "title": title_m.group(1).strip() if title_m else "",
            }
    return pmid_map


def parse_bib_keys_to_doi(bib_path: str) -> dict[str, str]:
    if not os.path.isfile(bib_path):
        return {}
    with open(bib_path, "r", encoding="utf-8") as f:
        content = f.read()
    entries = re.split(r"(?=@\w+\{)", content)
    key_to_doi: dict[str, str] = {}
    for entry in entries:
        key_match = _BIB_ENTRY_PATTERN.search(entry)
        doi_match = _BIB_DOI_PATTERN.search(entry)
        if key_match and doi_match:
            key_to_doi[key_match.group(1)] = doi_match.group(1).strip().lower()
    return key_to_doi


_NO_ESCAPE_FIELDS = {"doi", "url", "eprint"}


def build_bibtex_entry(entry_type: str, key: str, fields: dict) -> str:
    key = re.sub(r"[^a-zA-Z0-9_\-]", "", key)
    lines = [f"@{entry_type}{{{key},"]
    for name, value in fields.items():
        if not value:
            continue
        value = str(value)
        if name not in _NO_ESCAPE_FIELDS:
            value = escape_bibtex(value)
        lines.append(f"  {name}={{{value}}},")
    if lines[-1].endswith(","):
        lines[-1] = lines[-1][:-1]
    lines.append("}")
    return "\n".join(lines)


def _next_suffix(n: int) -> str:
    return chr(ord("a") - 1 + n)


def unique_key(key: str, seen_keys: set) -> tuple[str, tuple[str, str] | None]:
    if key not in seen_keys:
        seen_keys.add(key)
        return key, None

    renamed = None
    if f"{key}a" not in seen_keys:
        seen_keys.add(f"{key}a")
        renamed = (key, f"{key}a")

    for n in range(1, 27):
        candidate = f"{key}{_next_suffix(n)}"
        if candidate not in seen_keys:
            seen_keys.add(candidate)
            return candidate, renamed
    raise RuntimeError(f"Could not generate unique key for '{key}' after 26 suffixes")


def make_bibtex_key(article: dict) -> str:
    last_name = article.get("first_author", "")
    if not last_name:
        authors = article.get("authors", "")
        if isinstance(authors, list):
            parts = authors[0].split() if authors else []
            if parts:
                last_name = parts[0].rstrip(",")
        elif authors:
            first_entry = authors.split(";")[0].split(",")[0].strip()
            parts = first_entry.split()
            if parts:
                last_name = parts[0]
    if not last_name:
        last_name = "Unknown"
    last_name = last_name.replace(" ", "")
    year = str(article.get("year", "0000"))
    return f"{last_name}_{year}"


def deduplicate_keys(keys: list[str]) -> list[str]:
    seen: set[str] = set()
    first_index: dict[str, int] = {}
    result: list[str] = []
    for base_key in keys:
        new_key, renamed = unique_key(base_key, seen)
        if renamed:
            old_name, new_name = renamed
            idx = first_index.pop(old_name)
            result[idx] = new_name
            first_index[new_name] = idx
        first_index[new_key] = len(result)
        result.append(new_key)
    return result
