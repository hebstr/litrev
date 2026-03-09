#!/usr/bin/env python3
"""
Citation Verification Script
Verifies DOIs, PMIDs, and citation metadata for accuracy.
Checks for retracted publications via NCBI E-utilities.
"""

import argparse
import json
import os
import re
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(__file__))
from bibtex_keys import strip_code_blocks as _strip_code_blocks, extract_doi_matches as _extract_doi_matches
from http_utils import request_with_retry as _request_with_retry

class CitationVerifier:
    def __init__(self, timeout=10, max_retries=3):
        self.timeout = timeout
        self.max_retries = max_retries

    def _http(self, method, url, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        return _request_with_retry(method, url, max_retries=self.max_retries, **kwargs)

    def extract_dois(self, text: str) -> list[str]:
        """Extract all DOIs from text (excluding fenced code blocks, keeping bibtex)."""
        text = _strip_code_blocks(text, keep_bibtex=True)
        return _extract_doi_matches(text)

    def verify_doi(self, doi: str) -> tuple[bool, dict]:
        """
        Verify a DOI and retrieve metadata.
        Returns (is_valid, metadata)
        """
        try:
            url = f"https://doi.org/api/handles/{doi}"
            response = self._http("GET", url)

            if response.status_code == 200:
                time.sleep(0.35)
                metadata = self._get_crossref_metadata(doi)
                return True, metadata
            else:
                print(f"  DOI handle lookup failed (HTTP {response.status_code}): {doi}")
                return False, {}
        except (requests.RequestException, ValueError, KeyError, json.JSONDecodeError) as e:
            print(f"  DOI verification error for {doi}: {e}")
            return False, {"error": str(e)}

    def _get_crossref_metadata(self, doi: str) -> dict:
        """Get metadata from CrossRef API."""
        try:
            url = f"https://api.crossref.org/works/{doi}"
            response = self._http("GET", url)

            if response.status_code == 200:
                data = response.json()
                message = data.get('message', {})

                # Extract key metadata
                metadata = {
                    'title': message.get('title', [''])[0],
                    'authors': self._format_authors(message.get('author', [])),
                    'year': self._extract_year(message),
                    'journal': message.get('container-title', [''])[0],
                    'volume': message.get('volume', ''),
                    'pages': message.get('page', ''),
                    'doi': doi
                }
                return metadata
            print(f"  CrossRef metadata lookup failed (HTTP {response.status_code}): {doi}")
            return {}
        except (requests.RequestException, ValueError, KeyError, json.JSONDecodeError) as e:
            print(f"  CrossRef metadata error for {doi}: {e}")
            return {"error": str(e)}

    def _format_authors(self, authors: list[dict]) -> str:
        """Format author list."""
        if not authors:
            return ""

        formatted = []
        for author in authors[:3]:
            given = author.get('given', '')
            family = author.get('family', '')
            name = author.get('name', '')
            if family:
                formatted.append(f"{family}, {given[0]}." if given else family)
            elif name:
                formatted.append(name)

        if len(authors) > 3:
            formatted.append("et al.")

        return ", ".join(formatted)

    def _extract_year(self, message: dict) -> str:
        """Extract publication year (published → published-print → published-online)."""
        for field in ("published", "published-print", "published-online"):
            date_parts = message.get(field, {}).get('date-parts', [[]])
            if date_parts and date_parts[0]:
                return str(date_parts[0][0])
        return ""

    def verify_pmid(self, pmid: str) -> tuple[bool, dict]:
        """
        Verify a PMID via NCBI E-utilities.
        Returns (is_valid, metadata)
        """
        try:
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            response = self._http(
                "GET", url,
                params={"db": "pubmed", "id": pmid, "retmode": "json"}
            )

            if response.status_code == 200:
                data = response.json()
                result = data.get('result', {}).get(str(pmid), {})
                if 'error' in result:
                    return False, {}

                authors_list = [a.get('name', '') for a in result.get('authors', [])]
                if len(authors_list) > 3:
                    authors_str = ', '.join(authors_list[:3]) + ', et al.'
                else:
                    authors_str = ', '.join(authors_list)
                metadata = {
                    'title': result.get('title', ''),
                    'authors': authors_str,
                    'year': m.group() if (m := re.search(r'\d{4}', result.get('pubdate', ''))) else '',
                    'journal': result.get('fulljournalname', ''),
                    'volume': result.get('volume', ''),
                    'pages': result.get('pages', ''),
                    'doi': next(
                        (aid['value'] for aid in result.get('articleids', [])
                         if aid.get('idtype') == 'doi'), ''
                    ),
                    'pmid': pmid,
                }
                return True, metadata
            print(f"  PMID lookup failed (HTTP {response.status_code}): {pmid}")
            return False, {}
        except (requests.RequestException, ValueError, KeyError, json.JSONDecodeError) as e:
            print(f"  PMID verification error for {pmid}: {e}")
            return False, {"error": str(e)}

    def _pmid_from_doi(self, doi: str) -> str:
        try:
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            response = self._http(
                "GET", url,
                params={"db": "pubmed", "term": f"{doi}[doi]", "retmode": "json"}
            )
            if response.status_code == 200:
                ids = response.json().get("esearchresult", {}).get("idlist", [])
                if ids:
                    return ids[0]
        except (requests.RequestException, ValueError, KeyError, json.JSONDecodeError) as e:
            print(f"  PMID-from-DOI lookup error for {doi}: {e}")
        return ""

    def check_retraction(self, pmid: str) -> bool:
        """
        Check if a PMID has been retracted via NCBI E-utilities.
        Searches both "Retracted Publication" (tagged on the article)
        and "Retraction of Publication" (the retraction notice) types.
        Returns True if retracted.
        """
        try:
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            term = (
                f"(retracted publication[pt] OR retraction of publication[pt]) "
                f"AND {pmid}[pmid]"
            )
            response = self._http(
                "GET", url,
                params={"db": "pubmed", "term": term, "retmode": "json"}
            )

            if response.status_code == 200:
                data = response.json()
                count = int(data.get('esearchresult', {}).get('count', 0))
                return count > 0
            print(f"  Retraction check failed (HTTP {response.status_code}): PMID {pmid}")
            return False
        except (requests.RequestException, ValueError, KeyError, json.JSONDecodeError) as e:
            print(f"  Retraction check error for PMID {pmid}: {e}")
            return False

    def extract_pmids(self, text: str) -> list[str]:
        """Extract all PMIDs from text (PMID: 12345678 and pmid = {12345678} patterns)."""
        pmids = re.findall(r'PMID:\s*(\d+)', text)
        pmids += re.findall(r'pmid\s*=\s*\{(\d+)\}', text, re.IGNORECASE)
        return list(dict.fromkeys(pmids))

    def verify_citations_in_file(self, filepath: str, check_retractions: bool = True) -> dict:
        """
        Verify all citations in a markdown file.
        Returns a report of verification results.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        dois = self.extract_dois(content)
        pmids = self.extract_pmids(content)

        report = {
            'total_dois': len(dois),
            'total_pmids': len(pmids),
            'verified': [],
            'failed': [],
            'retracted': [],
            'retraction_unchecked': [],
            'metadata': {}
        }

        seen_pmids = set()

        for doi in dois:
            print(f"Verifying DOI: {doi}")
            is_valid, metadata = self.verify_doi(doi)

            if is_valid:
                report['verified'].append(doi)
                report['metadata'][doi] = metadata
                if check_retractions:
                    pmid = self._pmid_from_doi(doi)
                    if pmid:
                        seen_pmids.add(pmid)
                        time.sleep(0.3)
                        print(f"Checking retraction status: DOI {doi} (PMID {pmid})")
                        if self.check_retraction(pmid):
                            report['retracted'].append(doi)
                            print(f"  WARNING: {doi} has been RETRACTED")
                    else:
                        report['retraction_unchecked'].append(doi)
                        print(f"  Retraction check skipped (no PMID found): {doi}")
            else:
                report['failed'].append(doi)

            time.sleep(0.5)

        for pmid in pmids:
            if pmid in seen_pmids:
                print(f"Skipping PMID {pmid} (already verified via DOI)")
                continue
            print(f"Verifying PMID: {pmid}")
            is_valid, metadata = self.verify_pmid(pmid)

            if is_valid:
                report['verified'].append(f"PMID:{pmid}")
                report['metadata'][f"PMID:{pmid}"] = metadata

                if check_retractions:
                    time.sleep(0.3)
                    print(f"Checking retraction status: PMID {pmid}")
                    if self.check_retraction(pmid):
                        report['retracted'].append(f"PMID:{pmid}")
                        print(f"  WARNING: PMID {pmid} has been RETRACTED")
            else:
                report['failed'].append(f"PMID:{pmid}")

            time.sleep(0.5)

        return report

def main():
    """Command-line interface for citation verification."""
    parser = argparse.ArgumentParser(description="Verify DOIs, PMIDs, and citation metadata.")
    parser.add_argument("file", help="Markdown file to verify")
    parser.add_argument("--output", help="Output path for JSON report (default: <file>_citation_report.json)")
    parser.add_argument("--timeout", type=int, default=10, help="HTTP timeout in seconds (default: 10)")
    parser.add_argument("--no-retractions", action="store_true", help="Skip retraction checks")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        parser.error(f"File not found: {args.file}")

    verifier = CitationVerifier(timeout=args.timeout)

    print(f"Verifying citations in: {args.file}")
    report = verifier.verify_citations_in_file(args.file, check_retractions=not args.no_retractions)

    print("\n" + "="*60)
    print("CITATION VERIFICATION REPORT")
    print("="*60)
    print(f"\nTotal DOIs found: {report['total_dois']}")
    print(f"Total PMIDs found: {report['total_pmids']}")
    print(f"Verified: {len(report['verified'])}")
    print(f"Failed: {len(report['failed'])}")
    print(f"Retracted: {len(report['retracted'])}")
    print(f"Retraction unchecked (DOIs without PMID): {len(report['retraction_unchecked'])}")

    if report['retraction_unchecked']:
        print("\nRetraction check skipped (no PMID found):")
        for ref in report['retraction_unchecked']:
            print(f"  - {ref}")

    if report['retracted']:
        print("\nWARNING - RETRACTED PUBLICATIONS:")
        for ref in report['retracted']:
            print(f"  ** {ref} **")

    if report['failed']:
        print("\nFailed identifiers:")
        for ref in report['failed']:
            print(f"  - {ref}")

    output_file = args.output or os.path.splitext(args.file)[0] + "_citation_report.json"
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\nDetailed report saved to: {output_file}")

    if report['retracted'] or report['failed']:
        sys.exit(1)

if __name__ == "__main__":
    main()
