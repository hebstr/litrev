"""Shared BibTeX utilities."""

import os
import re


_DOI_PATTERN = re.compile(r'10\.\d{4,}/[^\s>,"\'}?#\]\}]+')


_BIBTEX_SPECIAL = str.maketrans({
    '&': r'\&',
    '%': r'\%',
    '#': r'\#',
    '_': r'\_',
    '$': r'\$',
    '~': r'\textasciitilde{}',
    '^': r'\textasciicircum{}',
})


_ALREADY_ESCAPED = re.compile(r'\\[&%#_$~^]')


def escape_bibtex(value):
    """Escape LaTeX/BibTeX special characters in a field value.

    Skips characters that are already escaped to avoid double-escaping.
    Split/rejoin on already-escaped sequences, then translate each fragment.
    Safe: \textasciitilde{} contains no literal '~' (U+007E), so translate
    won't corrupt it. Function is idempotent (verified).
    """
    parts = _ALREADY_ESCAPED.split(value)
    escaped_parts = [p.translate(_BIBTEX_SPECIAL) for p in parts]
    separators = _ALREADY_ESCAPED.findall(value)
    result = escaped_parts[0]
    for sep, part in zip(separators, escaped_parts[1:]):
        result += sep + part
    return result


def _strip_trailing_parens(doi):
    """Remove unbalanced trailing parentheses from a DOI."""
    while doi.endswith(')') and doi.count(')') > doi.count('('):
        doi = doi[:-1]
    return doi


def extract_doi_matches(text):
    """Extract DOIs from text, handling parenthesized DOIs correctly."""
    return list(dict.fromkeys(
        _strip_trailing_parens(doi.rstrip('.,;:'))
        for doi in _DOI_PATTERN.findall(text)
    ))


def strip_code_blocks(text, keep_bibtex=False):
    """Remove fenced code blocks from text, optionally keeping bibtex blocks."""
    if keep_bibtex:
        return re.sub(r'```(?!bibtex\b).*?```', '', text, flags=re.DOTALL)
    return re.sub(r'```.*?```', '', text, flags=re.DOTALL)


_BIB_ENTRY_PATTERN = re.compile(r"@\w+\{([\w-]+),")
_BIB_DOI_PATTERN = re.compile(r"doi\s*=\s*\{([^}]+)\}", re.IGNORECASE)


def parse_bib_keys_to_doi(bib_path):
    """Parse a .bib file and return a dict mapping BibTeX keys to lowercase DOIs."""
    if not os.path.isfile(bib_path):
        return {}
    with open(bib_path, "r", encoding="utf-8") as f:
        content = f.read()
    entries = re.split(r"(?=@\w+\{)", content)
    key_to_doi = {}
    for entry in entries:
        key_match = _BIB_ENTRY_PATTERN.search(entry)
        doi_match = _BIB_DOI_PATTERN.search(entry)
        if key_match and doi_match:
            key_to_doi[key_match.group(1)] = doi_match.group(1).strip().lower()
    return key_to_doi


_NO_ESCAPE_FIELDS = {"doi", "url", "eprint"}


def build_bibtex_entry(entry_type, key, fields):
    """Build a BibTeX entry string from type, key, and an ordered dict of fields.

    Fields with empty/None values are skipped.
    Values are escaped except for fields in _NO_ESCAPE_FIELDS.
    """
    # Each resolver (doi.org, CrossRef, PubMed) parses author names differently
    # to build an initial key. This sanitizer is the single guarantee that the
    # final key is valid BibTeX (no spaces, no special chars).
    key = re.sub(r'[^a-zA-Z0-9_\-]', '', key)
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


def _next_suffix(n):
    """Return 'a', 'b', ... 'z' for n = 1..26."""
    return chr(ord('a') - 1 + n)


def unique_key(key, seen_keys):
    """Return a unique BibTeX key, renaming with a/b/c suffixes on collision.

    On first occurrence, the key is stored as-is.
    On second occurrence (first collision), the original is retroactively
    renamed to ``key + 'a'`` and the new entry gets ``key + 'b'``.
    Subsequent collisions get 'c', 'd', etc.

    Returns (new_key, renamed_pair) where renamed_pair is (old, new) if the
    first occurrence was retroactively suffixed, or None.
    """
    if key not in seen_keys:
        seen_keys.add(key)
        return key, None

    # NOTE: the bare key stays in seen_keys intentionally — removing it would
    # cause a later call with the same base key to miss the collision.
    renamed = None
    if f"{key}a" not in seen_keys:
        seen_keys.add(f"{key}a")
        renamed = (key, f"{key}a")

    # In practice, rarely more than 3-5 homonymes per key in a literature review.
    for n in range(1, 11):
        candidate = f"{key}{_next_suffix(n)}"
        if candidate not in seen_keys:
            seen_keys.add(candidate)
            return candidate, renamed
    raise RuntimeError(f"Could not generate unique key for '{key}' after 10 suffixes")
