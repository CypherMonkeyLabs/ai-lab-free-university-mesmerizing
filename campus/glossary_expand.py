"""Turn the thinnest glossary stubs into short lessons.

Only entries whose source text is under 45 words are expanded. The added
sentences teach a control. They do not add a price, a model id, or a product
step. Sentences carried from the 2026-10-14 draft stay marked as not re-fetched.
"""

from __future__ import annotations

from campus.schema import NT, OL, P

_NOTE = (
    "The one-line sense above was carried from the 2026-10-14 study draft and was not "
    "re-fetched on 2026-10-15. If that line names a price, a model id, or a product screen, "
    "open the vendor's current page before you repeat it."
)

# Longer teaching for the stubs that are easy to misuse. Keyed by glossary id.
_DEEP: dict[str, str] = {
    "GL-p140": (
        "Prompt injection means untrusted text tries to replace the instruction. "
        "The usual path is a retrieved page, a mail, or a tool result. "
        "A retrieval index and a fine-tune do not close it. "
        "Label that text as data, keep side effects behind a permission you wrote, and keep one injection case in the eval set."
    ),
    "GL-p141": (
        "Sensitive information disclosure means a secret, a card number, or private text leaves through the answer or the log. "
        "The control is to keep that text out of the prompt and out of the trace. "
        "A fluent answer that repeats a number from the pack is still a disclosure."
    ),
    "GL-p142": (
        "Supply chain here means the model file, the data, the package, and the plugin you did not write. "
        "Pin the id you call. A new id is a rescore, not a silent upgrade. "
        "This course does not certify a vendor's build."
    ),
    "GL-p143": (
        "Data and model poisoning means a training row, a fine-tune row, or an embedding source was manipulated. "
        "The index then returns the attacker's passage as if it were yours. "
        "Record the source hash. A changed hash is a reason to rebuild, not a reason to trust the new vector."
    ),
    "GL-p145": (
        "Excessive agency means the loop can call tools that do too much, too often, or without a person. "
        "Two agents that can both refund is this failure. "
        "The control is an allow-list, a step cap, and a person on send, pay, and delete."
    ),
    "GL-p146": (
        "System prompt leakage means the hidden instruction is repeated, including any secret that was stored in it. "
        "Do not put a key in the prompt. "
        "Treat a request to print the instructions as an injection case, not as a curiosity."
    ),
    "GL-p147": (
        "Vector and embedding weaknesses mean the nearest neighbor is not the true passage. "
        "A mixed embedding model, a missing filter, or a poisoned row all look like a fluent answer. "
        "Check the model id on the row and the audience filter before you blame the wording."
    ),
    "GL-p148": (
        "Misinformation here is a confident false sentence, with or without an attacker. "
        "If the span was not in the pack, the answer does not become true by sounding finished. "
        "Refuse, or fix the index. Do not raise temperature."
    ),
    "GL-p149": (
        "Unbounded consumption means tokens, tool loops, and retries have no ceiling you set. "
        "The bill and the latency are the symptom. "
        "Cap the steps, cap the retries so they cannot double-send, and keep the same tasks when you change the cap."
    ),
    "GL-p152": (
        "Measure means a test you can run before deployment and again while the system is in operation. "
        "The same cases, a written pass rule, and a count of safety failures. "
        "A demo is not that test."
    ),
    "GL-p153": (
        "Manage means someone can respond, recover, and say what happened. "
        "The kill switch lives here: the flag, the person who may throw it, and the old path you return to. "
        "A channel with no owner is not managed."
    ),
    "GL-p154": (
        "A kill switch disables the new path and restores the previous prompt hash or the previous tool list. "
        "Rehearse it before the wider cutover. "
        "A switch you have not thrown is a sentence, not a control."
    ),
    "GL-p043": (
        "Untrusted text is anything the model did not write as the instruction: retrieved pages, mail, and tool results. "
        "Label it as data. "
        "If that text can change which tool runs, the host failed, not the tone of the answer."
    ),
    "GL-p046": (
        "RAG in this course means retrieve a span you are allowed to store, then generate, then cite the id or refuse. "
        "Lewis et al. 2020 named the research setup. A production chat stack is not that paper. "
        "Cite the paper for the idea. Cite your trace for the run."
    ),
    "GL-p076": (
        "An MCP server declares tools. It does not become the authority for a side effect. "
        "The host executes, and only after a permission you wrote. "
        "Descriptions on the server are untrusted unless you trust that server. This campus cites the 2025-06-18 pin for the protocol, not a later draft date."
    ),
    "GL-p102": (
        "A CI gate fails the build when a pinned prompt or a tool path regresses on the same cases. "
        "The gate names quality, safety, latency, and cost. "
        "A green demo with no case file is not a gate."
    ),
}


def _words(item: dict) -> int:
    parts: list[str] = []
    for block in item["blocks"]:
        for value in block.values():
            if isinstance(value, str):
                parts.append(value)
            elif isinstance(value, list):
                parts.extend(str(part) for part in value)
    return len(" ".join(parts).split())


def expand_glossary(lessons: list[dict]) -> int:
    expanded = 0
    for item in lessons:
        if item.get("school") != "GL":
            continue
        if _words(item) >= 45:
            continue
        title = item["title"]
        summary = item["summary"].rstrip(".")
        deep = _DEEP.get(item["id"])
        if deep:
            body = deep
        else:
            body = (
                f"Use “{title}” when you can point at the object it names. "
                f"The short sense in this glossary is: {summary}. "
                "Write who may change that object and which test would show the term does not apply. "
                "If the test depends on a vendor screen, this course does not certify the screen."
            )
        item["blocks"].extend(
            [
                P(body),
                OL(
                    [
                        f"Restate {title} without copying the glossary line.",
                        "Name the log, config, or case that makes the term true or false.",
                        "Name one claim this course will not make about it.",
                    ]
                ),
                NT("Not re-fetched", _NOTE),
            ]
        )
        item["minutes"] = max(int(item["minutes"]), 8)
        expanded += 1
    return expanded
