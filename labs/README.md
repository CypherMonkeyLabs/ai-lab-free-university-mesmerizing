# Zero-key labs

These labs are the runnable half of the campus. They use the Python standard library only. No API key, no install, no network required. If a local model runner is listening on `127.0.0.1:11434`, lab 01 will say so. If it is not, lab 01 uses an honest mock and still writes an artifact.

Run them from the repository root:

```bash
python3 labs/01-local-hello.py
python3 labs/02-tool-call.py
python3 labs/03-golden-eval.py
python3 labs/06-rag-ablation.py
python3 labs/07-agent-loop.py
python3 labs/08-voice-latency-budget.py
```

| Lab | What it proves | Artifact |
|---|---|---|
| `01-local-hello.py` | A local runner answered, or the mock did, and you can tell which | `labs/artifacts/01-local-hello.json` |
| `02-tool-call.py` | Math and a definition come from tools, not from a fluent guess | `labs/artifacts/02-tool-call.json` |
| `03-golden-eval.py` | A fixed 10-question suite scores a fixture at the 80% bar | `labs/reports/golden10-report.md` |
| `06-rag-ablation.py` | Keyword retrieval hits; a naive neighbor search misses | `labs/artifacts/06-rag-ablation.json` |
| `07-agent-loop.py` | A bad guess is corrected by a tool, then the loop stops | `labs/artifacts/07-agent-loop.json` |
| `08-voice-latency-budget.py` | A stage p95 shows the slow leg an average hides | `labs/artifacts/08-voice-latency.json` |

Questions for lab 03 live in `labs/evals/golden10.json`. Artifact and report files are gitignored on purpose. Commit the suite, not your local run output.

The campus lessons that point here: `02-07`, `06-07`, `08-03`, and school `11`.
