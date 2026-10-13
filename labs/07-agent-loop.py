#!/usr/bin/env python3
"""Lab 07 — a bounded tool loop that must stop, even after a bad guess."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "labs" / "artifacts" / "07-agent-loop.json"
MAX_STEPS = 4


def calc_product() -> int:
    return 6 * 7


def main() -> int:
    trace: list[dict[str, object]] = []
    guess = 40
    trace.append({"step": 1, "action": "guess", "value": guess, "note": "invented, not a tool"})
    tool_result = calc_product()
    trace.append({"step": 2, "action": "tool:calc", "expr": "6*7", "value": tool_result})
    corrected = tool_result
    trace.append({"step": 3, "action": "correct", "value": corrected, "replaced": guess})
    trace.append({"step": 4, "action": "stop", "reason": "tool result stored and step cap respected"})
    if len(trace) > MAX_STEPS:
        raise SystemExit("loop exceeded the step cap")
    if corrected != 42:
        raise SystemExit("correction did not use the tool result")
    artifact = {
        "lab": "07-agent-loop",
        "run": "python3 labs/07-agent-loop.py",
        "trace": trace,
        "metric": {"steps": len(trace), "cap": MAX_STEPS, "corrections": 1},
        "artifact": str(ARTIFACT.relative_to(ROOT)),
        "falsifier": "An invented 40 that is never corrected, or a loop with no stop.",
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(f"stopped at step {len(trace)} corrected={corrected} artifact={artifact['artifact']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
