"""Regex patterns and claim extraction for numerical data in medical text.

Unified from verify version (most robust, handles Unicode dashes).
"""

import re


NUM_PATTERN = re.compile(
    r"(?<![A-Za-z\d/])"
    r"("
    r"\d{1,3}(?:[\s\u00a0]\d{3})+(?:[.,]\d+)?%?"
    r"|\d+(?:[.,]\d+)?%"
    r"|\d+(?:[.,]\d+)?"
    r")"
    r"(?![A-Za-z\d])"
)

_STAT_VALUE = r"[\-\u2212\u2013]?\d+(?:[.,]\d+)?"

_STAT_TAIL = (
    r"[\s:=]*" + _STAT_VALUE + r"(?:\s*(?:\("
    r"[^)]{0,120}"
    r"\)|\["
    r"[^\]]{0,120}"
    r"\]))?"
    r"(?:,?\s*p\s*[<=>\s]+\s*[\d.,]+)?"
)

STAT_PATTERN_SRC = (
    r"("
    r"(?i:AOR|aOR|aHR|NNT|NNH|SMD|WMD|IRR|SIR)"
    + _STAT_TAIL
    + r"|(?<![a-zA-Z])(?:OR|HR|RR|RD)(?=[\s:=\d])"
    + _STAT_TAIL
    + r"|(?i:p)\s*[<=>\s]+\s*[\d.,]+"
    r"|(?:95\s*%?\s*(?i:CI))\s*[:=]?\s*[\[(][\d.,\-\u2212\u2013\s]+[\])]"
    r")"
)

STAT_PATTERN = re.compile(STAT_PATTERN_SRC)


def extract_context(text: str, start: int, end: int, window: int = 80) -> str:
    ctx_start = max(0, start - window)
    ctx_end = min(len(text), end + window)
    snippet = text[ctx_start:ctx_end].strip()
    snippet = re.sub(r"\s+", " ", snippet)
    if ctx_start > 0:
        snippet = "..." + snippet
    if ctx_end < len(text):
        snippet = snippet + "..."
    return snippet


def extract_claims(text: str, source: str = "") -> list[dict[str, str]]:
    if not text:
        return []

    claims: list[dict[str, str]] = []
    seen: set[str] = set()
    stat_spans: list[tuple[int, int]] = []

    for m in STAT_PATTERN.finditer(text):
        stat_spans.append((m.start(), m.end()))
        value = m.group(0).strip()
        if value in seen:
            continue
        seen.add(value)
        entry: dict[str, str] = {
            "type": "statistic",
            "value": value,
            "verbatim": extract_context(text, m.start(), m.end()),
        }
        if source:
            entry["source"] = source
        claims.append(entry)

    for m in NUM_PATTERN.finditer(text):
        value = m.group(0).strip()
        if value in seen or len(value) == 1:
            continue

        already_in_stat = any(
            m.start() >= ss and m.end() <= se for ss, se in stat_spans
        )
        if already_in_stat:
            continue

        seen.add(value)
        claim_type = "percentage" if "%" in value else "number"
        entry = {
            "type": claim_type,
            "value": value,
            "verbatim": extract_context(text, m.start(), m.end()),
        }
        if source:
            entry["source"] = source
        claims.append(entry)

    return claims
