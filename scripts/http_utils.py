"""Shared HTTP utilities for literature review scripts."""

import os
import sys
import time

import requests

NCBI_EMAIL = os.environ.get("NCBI_EMAIL", "literature-review-skill@example.com")
NCBI_TOOL = "LiteratureReviewSkill"
NCBI_API_KEY = os.environ.get("NCBI_API_KEY", "")

_SESSION = requests.Session()
_SESSION.headers.update({"User-Agent": "LiteratureReviewSkill/1.0"})

_CROSSREF_SESSION = requests.Session()
_CROSSREF_SESSION.headers.update({
    "User-Agent": f"LiteratureReviewSkill/1.0 (mailto:{NCBI_EMAIL})",
})

_last_ncbi_call = 0.0
_NCBI_MIN_INTERVAL = 0.1 if NCBI_API_KEY else 0.34


def _ncbi_throttle():
    global _last_ncbi_call
    now = time.monotonic()
    elapsed = now - _last_ncbi_call
    if elapsed < _NCBI_MIN_INTERVAL:
        time.sleep(_NCBI_MIN_INTERVAL - elapsed)
    _last_ncbi_call = time.monotonic()


def ncbi_params(extra: dict | None = None) -> dict:
    params = {"tool": NCBI_TOOL, "email": NCBI_EMAIL}
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    if extra:
        params.update(extra)
    return params


def request_with_retry(method, url, max_retries=3, session=None, **kwargs):
    kwargs.setdefault("timeout", 10)

    is_ncbi = "ncbi.nlm.nih.gov" in url
    is_crossref = "crossref.org" in url

    if is_ncbi:
        _ncbi_throttle()
    if is_crossref:
        s = session or _CROSSREF_SESSION
    else:
        s = session or _SESSION

    response = None
    for attempt in range(max_retries):
        try:
            response = s.request(method, url, **kwargs)
        except requests.RequestException as e:
            print(f"  Request error ({e}), retrying ({attempt + 1}/{max_retries})...", file=sys.stderr)
            time.sleep(2 ** attempt)
            continue
        if response.status_code == 429 or response.status_code >= 500:
            try:
                wait = int(response.headers.get("Retry-After", 2 ** attempt))
            except (ValueError, TypeError):
                wait = 2 ** attempt
            label = "Rate limited (429)" if response.status_code == 429 else f"Server error ({response.status_code})"
            print(f"  {label}, retrying in {wait}s...", file=sys.stderr)
            time.sleep(wait)
            if is_ncbi:
                _ncbi_throttle()
            continue
        return response
    if response is None:
        raise requests.ConnectionError(f"All {max_retries} attempts failed for {url}")
    print(f"  Retries exhausted for {url} (last status: {response.status_code})", file=sys.stderr)
    response.raise_for_status()
    return response
