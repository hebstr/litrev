"""Shared HTTP client with rate limiting and retry logic.

Handles NCBI, CrossRef, Semantic Scholar, and generic endpoints.
Uses httpx instead of requests for async compatibility.
"""

import os
import sys
import time

import httpx

LITREV_EMAIL = os.environ.get("LITREV_EMAIL") or os.environ.get("NCBI_EMAIL") or ""
NCBI_TOOL = "litrev-mcp"
NCBI_API_KEY = os.environ.get("NCBI_API_KEY", "")
S2_API_KEY = os.environ.get("S2_API_KEY", "")

_PLACEHOLDER_EMAIL = "litrev-mcp@example.com"
_EMAIL = LITREV_EMAIL or _PLACEHOLDER_EMAIL

if not LITREV_EMAIL:
    print(
        "Warning: LITREV_EMAIL not set — using placeholder. "
        "Set LITREV_EMAIL to your email to comply with NCBI/CrossRef/OpenAlex usage policies "
        "and get faster rate limits (polite pool).",
        file=sys.stderr,
    )

_UA = f"litrev-mcp/1.0 (mailto:{_EMAIL})"

_CLIENT = httpx.Client(
    headers={"User-Agent": _UA},
    timeout=15,
    follow_redirects=True,
)

_CROSSREF_CLIENT = httpx.Client(
    headers={"User-Agent": _UA},
    timeout=15,
    follow_redirects=True,
)

OA_CLIENT = httpx.Client(
    headers={"User-Agent": _UA},
    timeout=15,
    follow_redirects=True,
)

_last_ncbi_call = 0.0
_NCBI_MIN_INTERVAL = 0.1 if NCBI_API_KEY else 0.34

_S2_HEADERS: dict[str, str] = {"User-Agent": "litrev-mcp/1.0"}
if S2_API_KEY:
    _S2_HEADERS["x-api-key"] = S2_API_KEY

S2_CLIENT = httpx.Client(
    headers=_S2_HEADERS,
    timeout=15,
    follow_redirects=True,
)

_last_s2_call = 0.0
S2_RATE_INTERVAL = 0.05 if S2_API_KEY else 1.0

_TIPS = {
    "LITREV_EMAIL": "Set LITREV_EMAIL for faster NCBI/CrossRef/OpenAlex rate limits (polite pool).",
    "NCBI_API_KEY": "Set NCBI_API_KEY to raise PubMed rate limit from 3 to 10 req/s. Free: https://www.ncbi.nlm.nih.gov/account/settings/",
    "S2_API_KEY": "Set S2_API_KEY to speed up citation chaining (~100x). Free: https://www.semanticscholar.org/product/api#api-key",
}
_tips_shown: set[str] = set()


def env_tips(*var_names: str) -> list[str]:
    tips = []
    for name in var_names:
        if name in _tips_shown:
            continue
        if not os.environ.get(name, ""):
            tips.append(_TIPS[name])
            _tips_shown.add(name)
    return tips


def _ncbi_throttle():
    global _last_ncbi_call
    now = time.monotonic()
    elapsed = now - _last_ncbi_call
    if elapsed < _NCBI_MIN_INTERVAL:
        time.sleep(_NCBI_MIN_INTERVAL - elapsed)
    _last_ncbi_call = time.monotonic()


def s2_throttle():
    global _last_s2_call
    now = time.monotonic()
    elapsed = now - _last_s2_call
    if elapsed < S2_RATE_INTERVAL:
        time.sleep(S2_RATE_INTERVAL - elapsed)
    _last_s2_call = time.monotonic()


def ncbi_params(extra: dict | None = None) -> dict:
    params = {"tool": NCBI_TOOL, "email": _EMAIL}
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    if extra:
        params.update(extra)
    return params


def request_with_retry(
    method: str,
    url: str,
    *,
    max_retries: int = 3,
    client: httpx.Client | None = None,
    **kwargs,
) -> httpx.Response:
    kwargs.setdefault("timeout", 15)

    is_ncbi = "ncbi.nlm.nih.gov" in url
    is_crossref = "crossref.org" in url

    if is_ncbi:
        _ncbi_throttle()
    if is_crossref:
        c = client or _CROSSREF_CLIENT
    else:
        c = client or _CLIENT

    response = None
    for attempt in range(max_retries):
        try:
            response = c.request(method, url, **kwargs)
        except httpx.HTTPError as e:
            print(f"  Request error ({e}), retrying ({attempt + 1}/{max_retries})...", file=sys.stderr)
            time.sleep(2**attempt)
            continue
        if response.status_code == 429 or response.status_code >= 500:
            try:
                wait = int(response.headers.get("Retry-After", 2**attempt))
            except (ValueError, TypeError):
                wait = 2**attempt
            label = "Rate limited (429)" if response.status_code == 429 else f"Server error ({response.status_code})"
            print(f"  {label}, retrying in {wait}s...", file=sys.stderr)
            time.sleep(wait)
            if is_ncbi:
                _ncbi_throttle()
            continue
        return response
    if response is None:
        raise httpx.ConnectError(f"All {max_retries} attempts failed for {url}")
    print(f"  Retries exhausted for {url} (last status: {response.status_code})", file=sys.stderr)
    response.raise_for_status()
    return response
