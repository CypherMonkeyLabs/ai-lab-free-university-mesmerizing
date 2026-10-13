#!/usr/bin/env python3
"""Lab 08 — stage timings where the average hides the slow leg."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "labs" / "artifacts" / "08-voice-latency.json"

# Milliseconds. The transport leg is the one a single average will hide.
STAGES = {
    "capture": [20, 22, 21, 19, 23],
    "stt": [80, 90, 85, 88, 92],
    "model": [140, 150, 145, 160, 155],
    "tts": [70, 75, 72, 74, 71],
    "transport": [40, 45, 42, 400, 44],
}


def percentile(values: list[int], pct: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("empty sample")
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * pct)))
    return float(ordered[index])


def main() -> int:
    rows = []
    slow_leg = ""
    slow_gap = -1.0
    for name, samples in STAGES.items():
        mean = sum(samples) / len(samples)
        p95 = percentile(samples, 0.95)
        gap = p95 - mean
        rows.append({"stage": name, "mean_ms": round(mean, 1), "p95_ms": p95, "gap_ms": round(gap, 1)})
        if gap > slow_gap:
            slow_gap = gap
            slow_leg = name
    artifact = {
        "lab": "08-voice-latency-budget",
        "run": "python3 labs/08-voice-latency-budget.py",
        "trace": rows,
        "metric": {"slow_leg": slow_leg, "p95_minus_mean_ms": round(slow_gap, 1)},
        "artifact": str(ARTIFACT.relative_to(ROOT)),
        "falsifier": "A single average that hides the slow transport sample.",
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(f"slow_leg={slow_leg} gap_ms={round(slow_gap, 1)} artifact={artifact['artifact']}")
    return 0 if slow_leg == "transport" else 1


if __name__ == "__main__":
    raise SystemExit(main())
