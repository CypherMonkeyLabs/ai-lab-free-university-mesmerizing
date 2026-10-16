"""Sources opened in October 2026. Unreadable pages stay in the list as confirm, with no URL."""

from __future__ import annotations

import html

CHECKED = "2026-10"


def _source(title: str, url: str, kind: str, status: str = "opened", note: str = "") -> dict:
    return {
        "title": title,
        "url": url,
        "kind": kind,
        "status": status,
        "note": note,
        "last_checked": CHECKED,
    }


CATALOG = {
    "attn": _source("Vaswani and co-authors, Attention Is All You Need, 2017", "https://arxiv.org/abs/1706.03762", "paper"),
    "gpt3": _source("Brown and co-authors, Language Models are Few-Shot Learners, 2020", "https://arxiv.org/abs/2005.14165", "paper"),
    "rag": _source("Lewis and co-authors, Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, 2020", "https://arxiv.org/abs/2005.11401", "paper"),
    "dpr": _source("Karpukhin and co-authors, Dense Passage Retrieval for Open-Domain Question Answering, 2020", "https://arxiv.org/abs/2004.04906", "paper"),
    "react": _source("Yao and co-authors, ReAct: Synergizing Reasoning and Acting in Language Models, 2022", "https://arxiv.org/abs/2210.03629", "paper"),
    "toolformer": _source("Schick and co-authors, Toolformer: Language Models Can Teach Themselves to Use Tools, 2023", "https://arxiv.org/abs/2302.04761", "paper"),
    "nist": _source("NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework", "spec"),
    "owasp": _source("OWASP Top 10 for Large Language Model Applications", "https://owasp.org/projects/top-10-for-large-language-model-applications", "community"),
    "mcp": _source("Model Context Protocol specification, 2025-06-18", "https://modelcontextprotocol.io/specification/2025-06-18", "spec"),
    "mcp-docs": _source("What is the Model Context Protocol (MCP)?", "https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro", "spec"),
    "mcp-gh": _source("Model Context Protocol organization on GitHub", "https://github.com/modelcontextprotocol", "community"),
    "mdn": _source("MDN Web Docs, Web Speech API", "https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API", "community"),
    "speech": _source("Web Speech API community draft", "https://webaudio.github.io/web-speech-api/", "community"),
    "speech-tr": _source(
        "W3C /TR/speech-api/",
        "https://www.w3.org/TR/speech-api/",
        "spec",
        "confirm",
        "This URL returned 404 on 2026-10. The community draft above is the page that opened.",
    ),
    "rfc9110": _source("RFC 9110, HTTP Semantics", "https://www.rfc-editor.org/rfc/rfc9110", "spec"),
    "rfc8259": _source("RFC 8259, The JSON Data Interchange Format", "https://www.rfc-editor.org/rfc/rfc8259", "spec"),
    "rfc3261": _source("RFC 3261, SIP: Session Initiation Protocol", "https://www.rfc-editor.org/rfc/rfc3261", "spec"),
    "otlp": _source("OpenTelemetry OTLP specification", "https://opentelemetry.io/docs/specs/otlp/", "spec"),
    "iana": _source("IANA service name and port number registry", "https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml", "spec"),
    "ollama": _source(
        "Ollama repository",
        "https://github.com/ollama/ollama",
        "community",
        "confirm",
        "The response on 2026-10 did not include a readable project title.",
    ),
    "py": _source("Python 3 tutorial", "https://docs.python.org/3/tutorial/", "vendor"),
    "py-community": _source("Python.org community", "https://www.python.org/community/", "community"),
    "git": _source("Git reference", "https://git-scm.com/docs", "vendor"),
    "h100": _source("NVIDIA H100 GPU product page. Confirm any number before quoting it.", "https://www.nvidia.com/en-us/data-center/h100/", "vendor"),
    "xai": _source("xAI public site", "https://x.ai/", "vendor", "confirm", "The site root returned 403 on 2026-10."),
    "xai-colossus": _source(
        "Colossus supercomputer page on the xAI site",
        "https://x.ai/colossus",
        "vendor",
        "confirm",
        "This URL returned 403 on 2026-10, so it is not linked.",
    ),
    "agents": _source("Anthropic, Building effective agents", "https://www.anthropic.com/engineering/building-effective-agents", "vendor"),
    "aws": _source("Amazon Bedrock overview", "https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html", "vendor"),
    "azure": _source(
        "Azure OpenAI documentation path",
        "https://learn.microsoft.com/en-us/azure/ai-services/openai/",
        "vendor",
        "confirm",
        "On 2026-10 this URL opened a Microsoft Foundry models page, not a page titled Azure OpenAI.",
    ),
    "gcp": _source(
        "Vertex AI documentation path",
        "https://cloud.google.com/vertex-ai/docs",
        "vendor",
        "confirm",
        "On 2026-10 this URL opened Gemini Enterprise Agent Platform docs, not a page titled Vertex AI.",
    ),
    "wcag": _source("W3C, Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "spec"),
    "mit": _source("MIT License", "https://opensource.org/license/mit", "spec"),
    "apache": _source("Apache License 2.0", "https://www.apache.org/licenses/LICENSE-2.0", "spec"),
    "bsd": _source("BSD 3-Clause License", "https://opensource.org/license/bsd-3-clause", "spec"),
    "cc": _source("Creative Commons Attribution-NonCommercial-ShareAlike 4.0", "https://creativecommons.org/licenses/by-nc-sa/4.0/", "spec"),
    "wiki-http": _source("HTTP — Wikipedia", "https://en.wikipedia.org/wiki/HTTP", "wikipedia"),
    "wiki-json": _source("JSON — Wikipedia", "https://en.wikipedia.org/wiki/JSON", "wikipedia"),
    "wiki-llm": _source("Large language model — Wikipedia", "https://en.wikipedia.org/wiki/Large_language_model", "wikipedia"),
    "wiki-attn": _source("Attention Is All You Need — Wikipedia", "https://en.wikipedia.org/wiki/Attention_Is_All_You_Need", "wikipedia"),
    "wiki-rag": _source("Retrieval-augmented generation — Wikipedia", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "wikipedia"),
    "wiki-py": _source("Python (programming language) — Wikipedia", "https://en.wikipedia.org/wiki/Python_(programming_language)", "wikipedia"),
    "wiki-git": _source("Git — Wikipedia", "https://en.wikipedia.org/wiki/Git", "wikipedia"),
    "wiki-tts": _source("Speech synthesis — Wikipedia", "https://en.wikipedia.org/wiki/Speech_synthesis", "wikipedia"),
    "wiki-asr": _source("Speech recognition — Wikipedia", "https://en.wikipedia.org/wiki/Speech_recognition", "wikipedia"),
    "wiki-a11y": _source("Web accessibility — Wikipedia", "https://en.wikipedia.org/wiki/Web_accessibility", "wikipedia"),
    "wiki-gpu": _source("Graphics processing unit — Wikipedia", "https://en.wikipedia.org/wiki/Graphics_processing_unit", "wikipedia"),
    "wiki-h100": _source(
        "Hopper (microarchitecture) — Wikipedia",
        "https://en.wikipedia.org/wiki/Nvidia_H100",
        "wikipedia",
        "opened",
        "The H100 title redirects to the Hopper page.",
    ),
    "wiki-prompt": _source("Prompt engineering — Wikipedia", "https://en.wikipedia.org/wiki/Prompt_engineering", "wikipedia"),
    "wiki-embed": _source("Word embedding — Wikipedia", "https://en.wikipedia.org/wiki/Word_embedding", "wikipedia"),
    "wiki-cloud": _source("Cloud computing — Wikipedia", "https://en.wikipedia.org/wiki/Cloud_computing", "wikipedia"),
    "wiki-mcp": _source("Model Context Protocol — Wikipedia", "https://en.wikipedia.org/wiki/Model_Context_Protocol", "wikipedia"),
}

DEEPER = {
    "T1-R1": ["wiki-a11y"],
    "T1-R2": ["py-community", "git", "wiki-py", "wiki-git"],
    "T1-R3": ["py-community", "wiki-py"],
    "T1-R4": ["wiki-http", "wiki-json"],
    "T1-R5": ["wiki-llm"],
    "T1-R6": ["py-community", "wiki-py"],
    "T2-R1": ["wiki-attn", "wiki-llm"],
    "T2-R2": ["wiki-llm", "wiki-attn"],
    "T2-R3": ["wiki-llm"],
    "T2-R4": ["wiki-llm"],
    "T2-R5": ["wiki-llm"],
    "T2-R6": ["wiki-llm"],
    "T3-R1": ["wiki-prompt"],
    "T3-R2": ["wiki-prompt"],
    "T3-R3": ["wiki-json"],
    "T3-R4": ["wiki-llm"],
    "T3-R5": ["wiki-py"],
    "T3-R6": ["wiki-prompt"],
    "T4-R1": ["wiki-rag"],
    "T4-R2": ["wiki-rag"],
    "T4-R3": ["wiki-embed", "wiki-rag"],
    "T4-R4": ["wiki-rag"],
    "T4-R5": ["wiki-rag"],
    "T4-R6": ["wiki-rag"],
    "T5-R1": ["wiki-llm"],
    "T5-R2": ["wiki-llm"],
    "T5-R3": ["wiki-llm"],
    "T5-R4": ["wiki-llm"],
    "T5-R5": ["wiki-llm"],
    "T5-R6": ["wiki-llm"],
    "T6-R1": ["mcp-docs", "mcp-gh", "wiki-mcp"],
    "T6-R2": ["mcp-docs", "mcp-gh", "wiki-mcp"],
    "T6-R3": ["mcp-docs", "mcp-gh", "wiki-mcp"],
    "T6-R4": ["mcp-docs", "rfc9110", "wiki-mcp", "wiki-http"],
    "T6-R5": ["mcp-docs", "mcp-gh", "wiki-mcp"],
    "T6-R6": ["mcp-docs", "wiki-mcp", "wiki-rag"],
    "T7-R1": ["wiki-llm"],
    "T7-R2": ["speech", "speech-tr", "wiki-tts", "wiki-asr"],
    "T7-R3": ["speech", "wiki-tts"],
    "T7-R4": ["wiki-llm"],
    "T7-R5": ["wiki-llm"],
    "T7-R6": ["wiki-llm"],
    "T8-R1": ["wiki-gpu", "wiki-h100"],
    "T8-R2": ["xai-colossus", "wiki-gpu", "wiki-h100"],
    "T8-R3": ["wiki-cloud"],
    "T8-R4": ["wiki-cloud"],
    "T8-R5": ["wiki-llm"],
    "T8-R6": ["wiki-llm"],
}

SHEET_KEYS = {
    "five-minute-path": ["nist", "wcag", "wiki-a11y"],
    "tokens-sampling": ["attn", "gpt3", "wiki-attn", "wiki-llm"],
    "rag-checklist": ["rag", "dpr", "wiki-rag"],
    "agent-loop": ["react", "toolformer", "agents", "wiki-llm"],
    "mcp-map": ["mcp", "mcp-docs", "mcp-gh", "rfc8259", "wiki-mcp"],
    "voice-budget": ["mdn", "speech", "speech-tr", "wiki-tts"],
    "handoff-packet": ["agents", "nist", "wiki-llm"],
    "glossary-sheet": ["attn", "rfc9110", "rfc8259", "mcp", "rag", "wiki-llm"],
}

TEMPLATE_KEYS = {
    "lab-notebook": ["py", "git", "wiki-py"],
    "eval-card": ["nist", "gpt3", "wiki-llm"],
    "agent-trace": ["react", "agents", "wiki-llm"],
    "channel-router": ["nist", "mdn", "wiki-llm"],
    "rag-checklist-form": ["rag", "wiki-rag"],
}

OVERVIEW_KEYS = {
    "overview-omni": ["nist", "wiki-llm"],
    "overview-rag": ["rag", "wiki-rag"],
    "overview-agent": ["react", "agents", "wiki-llm"],
    "overview-mcp": ["mcp", "mcp-docs", "wiki-mcp"],
    "overview-handoff": ["agents", "nist", "wiki-llm"],
    "overview-latency": ["mdn", "speech", "wiki-tts"],
    "overview-glossary": ["attn", "rfc8259", "wiki-llm"],
    "overview-certs": ["nist", "cc", "wiki-llm"],
}

CAMPUS_SHEET_KEYS = {
    "ports-protocols": ["rfc3261", "otlp", "iana", "mcp", "rfc9110", "ollama", "wiki-http"],
    "call-flows": ["rag", "react", "mdn", "wiki-rag", "wiki-asr"],
    "config-checklist": ["owasp", "py", "wiki-llm"],
    "troubleshooting": ["rag", "nist", "mdn", "wiki-rag"],
    "migration": ["nist", "owasp", "wiki-llm"],
    "security-gates": ["nist", "owasp", "wiki-llm"],
    "eval-card": ["nist", "gpt3", "wiki-llm"],
    "glossary-card": ["attn", "rag", "rfc8259", "wiki-llm"],
    "read-a-ladder": ["rfc3261", "wiki-http"],
    "career-path": ["attn", "rag", "nist", "wiki-llm"],
    "flashcards": ["attn", "rfc9110", "rfc8259", "mcp", "rag", "wiki-llm"],
    "index": ["nist", "mcp", "wiki-llm"],
}


def entries(keys: list[str]) -> list[dict]:
    chosen: list[dict] = []
    seen: set[str] = set()
    for key in keys:
        if key in seen:
            continue
        seen.add(key)
        item = dict(CATALOG[key])
        if item["status"] != "opened":
            item.pop("url", None)
        chosen.append({"id": key, **item})
    return chosen


def esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def go_deeper_html(keys: list[str], json_href: str = "", anchor: str = "") -> str:
    """Visible citation block. Opened pages are links. Unopenable pages say confirm and carry no URL."""
    items = []
    for item in entries(keys):
        note = f" {esc(item['note'])}" if item.get("note") else ""
        if item["status"] == "opened" and item.get("url"):
            title = f'<a href="{esc(item["url"])}">{esc(item["title"])}</a>'
            confirm = ""
        else:
            title = f'<span class="source-title">{esc(item["title"])}</span>'
            confirm = " <strong>confirm</strong>"
        items.append(
            f"<li>{title}"
            f' <span class="source-kind">{esc(item["kind"])}</span>'
            f"{confirm}{note}"
            f' <span class="source-checked">last checked {esc(item["last_checked"])}</span></li>'
        )
    json_link = f'<p><a href="{esc(json_href)}">sources.json</a></p>' if json_href else ""
    anchor_attr = f' id="{esc(anchor)}"' if anchor else ""
    return (
        f'<section class="go-deeper"{anchor_attr} data-read data-menu="learn">'
        "<h2>Sources and go deeper</h2>"
        f'<ul class="cite-list">{"".join(items)}</ul>'
        f"{json_link}"
        "</section>"
    )


def room_keys(room_id: str, cite_keys: list[str]) -> list[str]:
    extra = [key for key in DEEPER.get(room_id, []) if key not in cite_keys]
    return list(cite_keys) + extra


def source_lines(keys: list[str]) -> list[str]:
    lines = ["Sources and go deeper"]
    for item in entries(keys):
        mark = " confirm" if item["status"] != "opened" else ""
        lines.append(f'{item["title"]} ({item["kind"]}){mark}')
        if item["note"]:
            lines.append(item["note"])
        lines.append(f'last checked {item["last_checked"]}')
        if item["status"] == "opened" and item.get("url"):
            lines.append(item["url"])
    return lines
