#!/usr/bin/env python3
"""
Extract abstracts from combined_results.json for articles matching given DOIs or row numbers.
"""

import argparse
import json
import os
import sys


def extract_by_dois(results, dois):
    dois_lower = {d.lower().strip() for d in dois}
    return [r for r in results if r.get('doi', '').lower().strip() in dois_lower]


def extract_by_rows(results, rows):
    return [results[i] for i in rows if 0 <= i < len(results)]


def format_output(articles):
    lines = []
    for a in articles:
        title = a.get('title', 'Untitled')
        authors = a.get('authors', 'Unknown')
        if isinstance(authors, list):
            authors = ', '.join(authors[:3]) + (' et al.' if len(authors) > 3 else '')
        year = a.get('year', 'N/A')
        doi = a.get('doi', '')
        abstract = a.get('abstract', 'No abstract available')
        lines.append(f"## {title}")
        lines.append(f"**{authors} ({year})** | DOI: {doi}")
        lines.append(f"\n{abstract}\n")
        lines.append("---\n")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Extract abstracts from combined_results.json for selected articles."
    )
    parser.add_argument("file", help="Path to combined_results.json")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dois", nargs='+', help="DOIs to extract")
    group.add_argument("--rows", nargs='+', type=int, help="Row numbers (0-based, matching combined_results.json array indices)")
    parser.add_argument("--output", help="Output file (default: stdout)")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        parser.error(f"File not found: {args.file}")

    with open(args.file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    if args.dois:
        articles = extract_by_dois(results, args.dois)
    else:
        articles = extract_by_rows(results, args.rows)

    if not articles:
        print("No matching articles found.", file=sys.stderr)
        sys.exit(1)

    output = format_output(articles)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Extracted {len(articles)} abstracts to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
