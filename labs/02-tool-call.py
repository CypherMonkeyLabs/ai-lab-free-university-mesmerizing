#!/usr/bin/env python3
"""Lab 02 — call a calculator and a glossary, then speak only from tool results."""

from __future__ import annotations

import ast
import json
import operator
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "labs" / "artifacts" / "02-tool-call.json"

GLOSSARY = {
    "rtma": "Run, Trace, Metric, Artifact",
    "token": "A chunk of text a model reads or writes",
    "mcp": "Model Context Protocol — a way to advertise tools to an agent",
}

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_UNARY_OPS = {ast.USub: operator.neg}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return float(_UNARY_OPS[type(node.op)](_eval_node(node.operand)))
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        return float(_BIN_OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right)))
    raise ValueError("unsupported expression")


def calc(expression: str) -> float:
    tree = ast.parse(expression, mode="eval")
    return _eval_node(tree)


def glossary_lookup(term: str) -> str:
    key = term.strip().lower()
    if key not in GLOSSARY:
        raise KeyError(key)
    return GLOSSARY[key]


def main() -> int:
    product = calc("6*7")
    meaning = glossary_lookup("rtma")
    calls = [
        {"tool": "calc", "args": {"expr": "6*7"}, "result": product},
        {"tool": "glossary_lookup", "args": {"term": "rtma"}, "result": meaning},
    ]
    answer = f"6*7 = {product:.0f}. RTMA means {meaning}."
    if "42" not in answer or "Run" not in answer:
        raise SystemExit("tool results did not ground the answer")
    artifact = {
        "lab": "02-tool-call",
        "run": "python3 labs/02-tool-call.py",
        "trace": calls,
        "metric": {"tool_calls": len(calls), "invented_facts": 0},
        "artifact": str(ARTIFACT.relative_to(ROOT)),
        "answer": answer,
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(answer)
    print(f"tool_calls={len(calls)} artifact={artifact['artifact']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
