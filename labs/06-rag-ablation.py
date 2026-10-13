#!/usr/bin/env python3
"""Lab 06 — a tiny retrieval ablation. Keywords hit; a naive neighbor search misses."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "labs" / "artifacts" / "06-rag-ablation.json"

DOCS = [
    {"id": "rtma", "text": "rtma means run trace metric artifact proof"},
    {"id": "neighbor", "text": "a fluent paragraph about the weather and a picnic"},
]


def keyword_hit(query: str) -> str:
    tokens = set(query.lower().split())
    best_id = DOCS[0]["id"]
    best_score = -1
    for doc in DOCS:
        score = len(tokens & set(doc["text"].split()))
        if score > best_score:
            best_score = score
            best_id = doc["id"]
    return best_id


def naive_neighbor(_: str) -> str:
    """Stand-in for a bad embedding that returns the nearest wrong chunk."""
    return "neighbor"


def main() -> int:
    query = "what does rtma mean"
    keyword_id = keyword_hit(query)
    neighbor_id = naive_neighbor(query)
    keyword_ok = keyword_id == "rtma"
    neighbor_ok = neighbor_id == "rtma"
    artifact = {
        "lab": "06-rag-ablation",
        "run": "python3 labs/06-rag-ablation.py",
        "trace": [
            {"retriever": "keyword", "doc": keyword_id},
            {"retriever": "naive-neighbor", "doc": neighbor_id},
        ],
        "metric": {
            "keyword_hit": keyword_ok,
            "naive_neighbor_hit": neighbor_ok,
            "hit_rate_delta": int(keyword_ok) - int(neighbor_ok),
        },
        "artifact": str(ARTIFACT.relative_to(ROOT)),
        "falsifier": "The wrong neighbor wins if you trust the naive retriever.",
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(
        f"keyword={keyword_id} naive_neighbor={neighbor_id} "
        f"delta={artifact['metric']['hit_rate_delta']} artifact={artifact['artifact']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
