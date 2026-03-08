"""Shared BibTeX utilities."""

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


_NO_ESCAPE_FIELDS = {"doi", "url", "eprint"}


def build_bibtex_entry(entry_type, key, fields):
    """Build a BibTeX entry string from type, key, and an ordered dict of fields.

    Fields with empty/None values are skipped.
    Values are escaped except for fields in _NO_ESCAPE_FIELDS.
    """
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
    """Return 'a', 'b', ... 'z', '27', '28', ... for n = 1, 2, ..."""
    return chr(ord('a') - 1 + n) if n <= 26 else str(n)


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

    renamed = None
    if f"{key}a" not in seen_keys:
        seen_keys.add(f"{key}a")
        renamed = (key, f"{key}a")

    n = 1
    while True:
        candidate = f"{key}{_next_suffix(n)}"
        if candidate not in seen_keys:
            seen_keys.add(candidate)
            return candidate, renamed
        n += 1
