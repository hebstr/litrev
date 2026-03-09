"""Shared regex patterns and claim extraction logic for numerical data."""

import re


NUM_PATTERN = re.compile(
    r"(?<![A-Za-z\d/])"
    r"("
    r"\d+(?:[.,]\d+)?%"
    r"|\d+(?:[.,]\d+)?"
    r")"
    r"(?![A-Za-z\d])"
)

STAT_PATTERN_SRC = (
    r"("
    # Known limitation: the [\s] in the tail char class lets the match
    # traverse spaces and swallow adjacent bare numbers (e.g. "OR 2.35  500"
    # eats 500). Rare in real abstracts (words separate stats from numbers).
    # A structural fix (value + optional parenthesized block) exists but the
    # current pattern works well enough for medical literature.
    r"(?i:AOR|aOR|aHR|NNT|NNH|SMD|WMD|IRR|SIR)"
    r"[\s:=]*"
    r"[\d.,\-–\s()%]{1,80}"
    r"|(?<![a-zA-Z])(?:OR|HR|RR|RD)(?=[\s:=\d])"
    r"[\s:=]*"
    r"[\d.,\-–\s()%]{1,80}"
    r"|(?i:p)\s*[<=>\s]+\s*[\d.,]+"
    r"|(?:95\s*%?\s*(?i:CI))\s*[:=]?\s*[\[(][\d.,\-–\s]+[\])]"
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

    stat_spans = [(sm.start(), sm.end()) for sm in STAT_PATTERN.finditer(text)]

    for m in STAT_PATTERN.finditer(text):
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
            m.start() >= ss and m.end() <= se
            for ss, se in stat_spans
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
