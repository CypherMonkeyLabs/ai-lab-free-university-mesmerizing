#!/usr/bin/env python3
"""Lab 01 — probe a local model runner, or say honestly that the mock answered."""

from __future__ import annotations

import json
import socket
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "labs" / "artifacts" / "01-local-hello.json"
HOST = "127.0.0.1"
PORT = 11434
TIMEOUT_SECONDS = 2.0


def probe_local_runner() -> tuple[str, float, list[str], str, str]:
    """Return backend, latency_ms, model names, error label, and the spoken answer."""
    url = f"http://{HOST}:{PORT}/api/tags"
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
        elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
        raw_models = payload.get("models", [])
        models = [str(item.get("name", "")) for item in raw_models if isinstance(item, dict)]
        answer = (
            "RTMA is Run, Trace, Metric, Artifact. "
            "A local runner responded on port 11434. This note lists tags; it is not a generated essay."
        )
        return "ollama", elapsed_ms, models, "ok", answer
    except (urllib.error.URLError, TimeoutError, socket.timeout, json.JSONDecodeError, OSError) as exc:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
        answer = (
            "RTMA is Run, Trace, Metric, Artifact. "
            "No local runner answered. This is the mock brain. Do not call it a model."
        )
        return "mock", elapsed_ms, [], type(exc).__name__, answer


def main() -> int:
    backend, latency_ms, models, error, answer = probe_local_runner()
    artifact = {
        "lab": "01-local-hello",
        "run": f"GET http://{HOST}:{PORT}/api/tags",
        "trace": [backend, error],
        "metric": {"latency_ms": latency_ms, "model_count": len(models)},
        "artifact": str(ARTIFACT.relative_to(ROOT)),
        "answer": answer,
        "models": models,
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(answer)
    print(f"backend={backend} latency_ms={latency_ms} artifact={artifact['artifact']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
