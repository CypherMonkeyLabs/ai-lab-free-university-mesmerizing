#!/usr/bin/env python3
"""Lab 03 — score a fixed 10-question suite. The default answerer is a fixture."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE_PATH = ROOT / "labs" / "evals" / "golden10.json"
REPORT_PATH = ROOT / "labs" / "reports" / "golden10-report.md"


def score_item(keywords: list[str], answer: str) -> bool:
    haystack = answer.lower()
    return all(keyword.lower() in haystack for keyword in keywords)


def main() -> int:
    suite = json.loads(SUITE_PATH.read_text(encoding="utf-8"))
    items = suite["items"]
    threshold = float(suite["threshold"])
    rows: list[str] = []
    passed = 0
    for item in items:
        answer = str(item["fixture_answer"])
        ok = score_item(list(item["keywords"]), answer)
        passed += int(ok)
        rows.append(
            f"| {item['id']} | {'pass' if ok else 'fail'} | {answer.replace('|', '/')} |"
        )
    rate = passed / len(items)
    status = "PASS" if rate >= threshold else "FAIL"
    report = "\n".join(
        [
            "# Golden-10 report",
            "",
            f"- Backend: fixture (no API key, no network)",
            f"- Passed: {passed} / {len(items)}",
            f"- Pass rate: {rate:.0%}",
            f"- Threshold: {threshold:.0%}",
            f"- Status: {status}",
            "",
            "Swap the fixture answers for a model later. Keep this file and this threshold.",
            "",
            "| ID | Result | Answer |",
            "|---|---|---|",
            *rows,
            "",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"{status} {passed}/{len(items)} ({rate:.0%}) report={REPORT_PATH.relative_to(ROOT)}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
