"""Shared types for the offline campus builder."""

from __future__ import annotations


def lesson(lid, school, level, minutes, title, summary, blocks):
    return {
        "id": lid,
        "school": school,
        "level": level,
        "minutes": minutes,
        "title": title,
        "summary": summary,
        "blocks": blocks,
    }


def P(text):
    return {"t": "p", "text": text}


def H(text):
    return {"t": "h", "text": text}


def UL(items):
    return {"t": "ul", "items": items}


def OL(items):
    return {"t": "ol", "items": items}


def TB(headers, rows):
    return {"t": "table", "headers": headers, "rows": rows}


def PRE(text):
    return {"t": "pre", "text": text}


def FIG(fig_id, caption):
    return {"t": "diagram", "id": fig_id, "caption": caption}


def PR(text):
    return {"t": "practice", "text": text}


def CK(question, answer):
    return {"t": "check", "q": question, "a": answer}


def NT(title, text):
    return {"t": "note", "title": title, "text": text}


def WN(title, text):
    return {"t": "warn", "title": title, "text": text}


SCHOOLS = [
    {
        "id": "00",
        "name": "Start here",
        "outcome": "Learn how this course works, what to save as proof, and the safety rules that apply everywhere else.",
        "kind": "track",
    },
    {
        "id": "01",
        "name": "How models work",
        "outcome": "Explain tokens, context, sampling, hallucination, and the model families named in current job posts.",
        "kind": "track",
    },
    {
        "id": "02",
        "name": "Prompting",
        "outcome": "Write prompts as jobs with a done-check, an output shape, and a test for the next change.",
        "kind": "track",
    },
    {
        "id": "03",
        "name": "Local models",
        "outcome": "Run an open-weight model on your own machine, pick a size that fits, and keep data separate from weights.",
        "kind": "track",
    },
    {
        "id": "04",
        "name": "APIs and cost",
        "outcome": "Call a hosted model without leaking the key, and read a bill in tokens, cache, and retries.",
        "kind": "track",
    },
    {
        "id": "05",
        "name": "Retrieval",
        "outcome": "Build a retrieval pipeline that cites sources, and measure whether the right passage was found.",
        "kind": "track",
    },
    {
        "id": "06",
        "name": "Agents",
        "outcome": "Design a tool loop with a schema, a permission boundary, a step cap, and a trace.",
        "kind": "track",
    },
    {
        "id": "07",
        "name": "MCP",
        "outcome": "Explain the Model Context Protocol and connect tools without granting a server silent access.",
        "kind": "track",
    },
    {
        "id": "08",
        "name": "Coding agents",
        "outcome": "Review an agent that edits a repository: plan, diff, tests, and a human gate.",
        "kind": "track",
    },
    {
        "id": "09",
        "name": "Evals",
        "outcome": "Score quality, safety, latency, and cost on a versioned task set before you trust a change.",
        "kind": "track",
    },
    {
        "id": "10",
        "name": "Fine-tuning",
        "outcome": "Decide when LoRA is the right next step, and compare an adapter to the base model on the same tasks.",
        "kind": "track",
    },
    {
        "id": "11",
        "name": "Safety",
        "outcome": "Write a personal policy for data, tools, and the actions that always need a person.",
        "kind": "track",
    },
    {
        "id": "12",
        "name": "Product skills",
        "outcome": "Specify an AI feature the way a product manager and an engineer can build and measure together.",
        "kind": "track",
    },
    {
        "id": "13",
        "name": "Capstone",
        "outcome": "Finish a small grounded assistant with citations, one tool, ten eval tasks, and a safety note.",
        "kind": "track",
    },
    {
        "id": "14",
        "name": "Contact center",
        "outcome": "Place a voice agent on a queue you can transfer, cite, and turn off.",
        "kind": "track",
    },
    {
        "id": "GL",
        "name": "Glossary",
        "outcome": "Short definitions for the words this course uses.",
        "kind": "reference",
    },
    {
        "id": "IV",
        "name": "Interview practice",
        "outcome": "Answers you can say out loud for the skills hiring posts ask about.",
        "kind": "reference",
    },
    {
        "id": "FQ",
        "name": "Questions",
        "outcome": "Practical answers about this course.",
        "kind": "reference",
    },
]


PATHS = [
    {
        "id": "new",
        "name": "New to AI",
        "blurb": "Enough mechanism to stop treating the model as a search box.",
        "lessons": ["00-01", "01-01", "01-03", "01-05", "02-01", "03-01"],
    },
    {
        "id": "assistant",
        "name": "Grounded assistant",
        "blurb": "Retrieve, cite, call one tool, and prove the answers.",
        "lessons": ["05-01", "05-06", "06-01", "09-01", "09-02", "13-01"],
    },
    {
        "id": "coding",
        "name": "Coding agent work",
        "blurb": "The loop teams expect when a job post says coding agent or MCP.",
        "lessons": ["08-01", "08-04", "07-01", "07-05", "11-03", "09-05"],
    },
    {
        "id": "product",
        "name": "Product and PM",
        "blurb": "Spec, metrics, failure states, and the build-or-buy choice.",
        "lessons": ["12-01", "12-02", "12-03", "12-04", "10-01", "IV-01"],
    },
]
