#!/usr/bin/env python3
"""Check exact terms across final text surfaces without printing matched values."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import unicodedata


def normalize(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold()


def load_terms(path: Path) -> list[str]:
    terms = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    return [term for term in terms if term]


def count_matches(text: str, terms: list[str]) -> int:
    normalized = normalize(text)
    return sum(normalize(term) in normalized for term in terms)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check final text files for exact forbidden terms."
    )
    parser.add_argument("--terms-file", required=True, type=Path)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    try:
        terms = load_terms(args.terms_file)
    except OSError as exc:
        print(json.dumps({"status": "ERROR", "reason": str(exc)}))
        return 2

    if not terms:
        print(json.dumps({"status": "ERROR", "reason": "terms file is empty"}))
        return 2

    failures: list[dict[str, object]] = []
    for path in args.paths:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(json.dumps({"status": "ERROR", "path": str(path), "reason": str(exc)}))
            return 2
        matches = count_matches(text, terms)
        if matches:
            failures.append({"path": str(path), "matched_term_count": matches})

    payload = {
        "status": "FAIL" if failures else "PASS",
        "files_checked": len(args.paths),
        "failures": failures,
    }
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
