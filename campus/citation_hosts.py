"""Hosts named in imported citations. The page may show these URLs as text."""

from __future__ import annotations

import re

HOSTS = frozenset({
    "ai.google.dev",
    "ai.meta.com",
    "airc.nist.gov",
    "arxiv.org",
    "aws.amazon.com",
    "cisco.com",
    "cloud.google.com",
    "cs50.harvard.edu",
    "developer.meta.com",
    "developers.llamaindex.ai",
    "developers.openai.com",
    "docs.anthropic.com",
    "docs.aws.amazon.com",
    "docs.langchain.com",
    "docs.pinecone.io",
    "docs.x.ai",
    "elastic.co",
    "gdpr-info.eu",
    "genai.owasp.org",
    "github.com",
    "help.webex.com",
    "learn.microsoft.com",
    "modelcontextprotocol.io",
    "nist.gov",
    "oag.ca.gov",
    "openai.com",
    "opentelemetry.io",
    "pcisecuritystandards.org",
    "platform.openai.com",
})


def url_allowed(url: str) -> bool:
    if "w3.org" in url or "127.0.0.1" in url:
        return True
    if url.startswith("https://github.com/cipher0x9/"):
        return True
    if url.startswith("https://cipher0x9.github.io/ai-lab-free-university-mesmerizing/"):
        return True
    host = re.sub(r"^https?://", "", url).split("/")[0].split(":")[0].lower()
    if host.startswith("www."):
        host = host[4:]
    return host in HOSTS
