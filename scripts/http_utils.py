"""Shared HTTP utilities for literature review scripts."""

import time

import requests

_SESSION = requests.Session()
_SESSION.headers.update({"User-Agent": "LiteratureReviewSkill/1.0"})


def request_with_retry(method, url, max_retries=3, session=None, **kwargs):
    kwargs.setdefault("timeout", 10)
    s = session or _SESSION
    response = None
    for attempt in range(max_retries):
        try:
            response = s.request(method, url, **kwargs)
        except requests.RequestException as e:
            print(f"  Request error ({e}), retrying ({attempt + 1}/{max_retries})...")
            time.sleep(2 ** attempt)
            continue
        if response.status_code == 429 or response.status_code >= 500:
            try:
                wait = int(response.headers.get("Retry-After", 2 ** attempt))
            except (ValueError, TypeError):
                wait = 2 ** attempt
            label = "Rate limited (429)" if response.status_code == 429 else f"Server error ({response.status_code})"
            print(f"  {label}, retrying in {wait}s...")
            time.sleep(wait)
            continue
        return response
    if response is None:
        raise requests.ConnectionError(f"All {max_retries} attempts failed for {url}")
    print(f"  Retries exhausted for {url} (last status: {response.status_code})")
    response.raise_for_status()
