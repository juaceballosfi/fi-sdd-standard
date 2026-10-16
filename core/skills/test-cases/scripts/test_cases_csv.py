#!/usr/bin/env python3
"""Turn test-cases.md into the CSV that Azure Test Plans imports (test-cases, fi-sdd-standard). No AI.

Usage:
    python test_cases_csv.py <work item folder>/test-cases.md [--out test-cases.csv] [--area "<Area Path>"]
                             [--include-blocked]

One row per test case with its title, then one row per step (Test Step, Step Action, Step
Expected), the layout Azure DevOps uses to import test cases from CSV. Cases with
`Estado: Bloqueado` are left out unless --include-blocked. The CSV is UTF-8 with BOM so that Excel
and Azure DevOps read the accents. Exit code 0 = written, 1 = no cases or a case without steps.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

CASE = re.compile(r"^### +(TC-\d+) +· +(.+?)\s*$", re.M)
STEP = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", re.M)
FIELD = re.compile(r"\*\*Estado:\*\*\s*([^·\n]+)")


def parse(text: str) -> list[dict]:
    parts = CASE.split(text.split("<!-- sdd:test-cases -->", 1)[-1])
    cases = []
    for i in range(1, len(parts) - 2, 3):
        body = parts[i + 2]
        status = FIELD.search(body)
        cases.append({"id": parts[i], "title": parts[i + 1],
                      "status": status.group(1).strip() if status else "",
                      "steps": [(n, a, e) for n, a, e in STEP.findall(body) if a != "Acción"]})
    return cases


def main() -> int:
    ap = argparse.ArgumentParser(description="test-cases.md → CSV de Azure Test Plans")
    ap.add_argument("source", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--area", default="")
    ap.add_argument("--include-blocked", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cases = parse(args.source.read_text(encoding="utf-8-sig"))
    if not args.include_blocked:
        cases = [c for c in cases if not c["status"].lower().startswith("bloqueado")]
    empty = [c["id"] for c in cases if not c["steps"]]
    if not cases or empty:
        print("✗ " + ("no hay casos" if not cases else "casos sin pasos: " + ", ".join(empty)))
        return 1
    out = args.out or args.source.with_suffix(".csv")
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Work Item Type", "Title", "Test Step", "Step Action", "Step Expected", "Area Path", "State"])
        for c in cases:
            w.writerow(["", "Test Case", f"{c['id']} · {c['title']}", "", "", "", args.area, "Design"])
            for n, action, expected in c["steps"]:
                w.writerow(["", "", "", n, action, expected, "", ""])
    print(f"✓ {len(cases)} casos y {sum(len(c['steps']) for c in cases)} pasos en {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
