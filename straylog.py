#!/usr/bin/env python3
"""straylog: find stray debug/log statements left in source code."""

import argparse
import json
import sys
from pathlib import Path

from patterns import IGNORED_DIRS, patterns_for_ext, is_ignored_path
from reporter import format_human


def scan_file(path, patterns):
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        # skip full-line comments heuristically
        if stripped.startswith("#") or stripped.startswith("//"):
            continue
        for name, regex in patterns.items():
            if regex.search(line):
                findings.append({
                    "file": str(path),
                    "line": i,
                    "kind": name,
                    "text": stripped,
                })
    return findings


def scan(root, exts, ignores):
    all_findings = []
    root = Path(root)
    if root.is_file():
        pats = patterns_for_ext(root.suffix)
        if pats:
            all_findings.extend(scan_file(root, pats))
        return all_findings
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if is_ignored_path(p.parts, ignores):
            continue
        if p.suffix.lower() not in exts:
            continue
        pats = patterns_for_ext(p.suffix)
        if not pats:
            continue
        all_findings.extend(scan_file(p, pats))
    return all_findings


def main():
    ap = argparse.ArgumentParser(
        prog="straylog", description="Find stray debug/log statements.")
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--ext", help="comma-separated extensions (e.g. py,js)")
    ap.add_argument("--ignore", help="comma-separated extra ignore dirs")
    args = ap.parse_args()

    if args.ext:
        exts = {e.strip() for e in args.ext.split(",") if e.strip()}
        exts = {e if e.startswith(".") else "." + e for e in exts}
    else:
        exts = {".py", ".js", ".jsx", ".ts", ".tsx", ".mjs",
                ".go", ".rs", ".java", ".rb", ".php"}

    ignores = set(IGNORED_DIRS)
    if args.ignore:
        ignores |= {d.strip() for d in args.ignore.split(",") if d.strip()}

    findings = scan(args.path, exts, ignores)

    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        print(format_human(findings))

    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
