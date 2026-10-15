# FAQ

**Last updated:** 2026-10-13

## What is this?

A free offline course: a shell page plus one module per track. Fourteen tracks cover models, prompting, local and hosted APIs, retrieval, agents, MCP, coding agents, evals, fine-tuning, safety, and product judgment. The proof habit is a run, a trace, a metric, and an artifact.

## How do I start?

Download [ai-lab-university.html.zip](../downloads/ai-lab-university.html.zip), unzip, and serve that folder (`python3 -m http.server 8000`, then open `http://127.0.0.1:8000/ai-lab-university.html`). Or open the published site. A disk path cannot load the tracks. Details are in [HOW-TO-GET.md](./HOW-TO-GET.md).

The catalog has **593 study pages**. That is 128 course lessons, 453 imported pages (19 long rooms, 333 glossary entries, 101 interview drills), and 12 ecosystem pages. The 581 count is the first two groups, checked by id. Reading time includes the short glossary pages. The longer plan is [HOW-TO-USE.md](./HOW-TO-USE.md).

## Do I need an API key or a GPU?

No, not to read the course or to run the labs. Add a local model or a hosted key only when you choose to run a live call, and only with data you are allowed to send. Lab 01 says `mock` when no local runner is listening. That is honest, and it still counts.

## Does the page send my progress anywhere?

No. It does not load remote fonts, scripts, or images. Marks stay in this browser's local storage.

## Is there a certificate or a PDF?

No certificate. The capstone — tasks, a safety page, a trace, and a scorecard — is what you can show. You can print a lesson to PDF from the browser. There is no separate textbook.

## Is this only for software engineers?

No. The product track is for people who specify and measure the work. The early tracks assume you can read carefully, not that you already ship models. A small laptop is enough to start.

## Can I remix it?

Yes. Free to use, share and remix under the MIT license. Lesson source is in `campus/`. Run `python3 -m campus.build_campus`, then `python3 scripts/rebuild_zips.py`. Keep the copyright notice. Model weights and other people's data are not covered by this license. The layout is in [REMIX.md](./REMIX.md) and [CONTRIBUTING.md](../CONTRIBUTING.md).

## Where is the voice course?

[UC Lab Free University](https://cipher0x9.github.io/uc-lab-free-university-mesmerizing/) is a separate campus. This course teaches voice only as an interface choice: latency, a transcript, and a handoff to a person (lesson `12-06` and `labs/08-voice-latency-budget.py`).

## How do I report an error?

Open an issue with the lesson id, the sentence, and the correction. If the fact depends on a vendor or a spec, include a source and the date. Model names change.

## Safety?

Educational material. No warranty. Do not commit secrets. Do not let a tool send, pay, delete, or push without a person approving that action.
