<p align="center">
  <img src="docs/assets/hero.svg" alt="AI Lab Free University: learn to build AI systems you can test" width="100%"/>
</p>

# AI Lab Free University

A free offline course for people who want to build with models and be able to show their work. It covers how models behave, prompting, local and hosted APIs, retrieval, agents, the Model Context Protocol (MCP), coding agents, evals, fine-tuning, safety, and the product skills behind a shippable feature.

One HTML file. No account. No API key required to read it. No remote fonts, scripts, or images.

**Free to use, share and remix.** MIT license. No warranty.

<p align="center">
  <a href="downloads/ai-lab-university.html.zip"><strong>Download the campus (.zip)</strong></a>
  &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="campus/ai-lab-university.html"><strong>Open the HTML</strong></a>
</p>

Direct download from GitHub: [ai-lab-university.html.zip](https://github.com/cipher0x9/ai-lab-free-university-mesmerizing/raw/main/downloads/ai-lab-university.html.zip)

---

## What you get

| | |
|---|---|
| Course | `campus/ai-lab-university.html` — 14 tracks, **128 lessons**, about 19 hours of reading |
| File | One page. Progress stays in your browser. Works offline after you open it. |
| Labs | `labs/` — zero-key Python. A missing local model is reported as mock. |
| Proof | Every practice asks for a run, a trace, a metric, and an artifact |
| Updated | October 2026. Pin the model id you call; names move. |

![Home dashboard in the dark theme, with the animated path](docs/assets/home.png)

![An agent lesson, with the step-through flow and the previous and next controls](docs/assets/lesson.png)

![Agent loop, paused on the step that runs the handler](docs/assets/diagram.png)

![The same home page in the light theme](docs/assets/light.png)

![Home on a phone-width screen](docs/assets/mobile.png)

![Retrieval track hub, with its poster, narration, and lesson cards](docs/assets/hub.png)

![Studio toy tokenizer](docs/assets/studio.png)

![High contrast on the MCP lesson](docs/assets/contrast.png)

## Pictures in the file

Counted from the built HTML. These are floors the generator enforces, and the current file is above them.

| Asset | Count | What it is |
|---|---:|---|
| Inline SVG elements | 841 | Icons, heroes, flows, plates, the map, and the six architecture figures |
| Distinct `data-art` ids | 806 | Header icon, sidebar icon, and hub-card icon are separate drawings of the same lesson |
| Animated flows | 147 | One per lesson (128), one per track hub (17), plus home and the studio |
| Hero illustrations | 146 | One per lesson, one per track hub, and the home poster |
| Diagram plates | 128 | One per lesson, under the prose |
| Lesson icons | 128 | Numbered badge in the lesson header |
| Audio clips | 19 | Home, each track, glossary, interview, questions, and the studio. Generated tones stored in the file, with a transcript |
| Interactive demos | 21 | Tokenizer, cosine, attention, retrieval, sampling, context cost, loss, latency, scorecard, and the 2D embedding map. Eleven sit on the lesson they teach. All ten also live in the studio |

Every flow has play, pause, previous, next, a speed control, a timeline, a highlighted stage, and a plain-English caption. Toy math is labeled as toy. Example prices are not a quote.

---

## What you'll learn

| Track | Lessons | You will be able to |
|---|---:|---|
| Start here | 6 | Use the course, keep proof, and apply the safety rules |
| How models work | 8 | Explain tokens, context, sampling, hallucination, and 2026 model roles |
| Prompting | 7 | Write a job, an output shape, and a test for the next change |
| Local models | 7 | Run an open-weight model that fits your machine, and keep data apart from weights |
| APIs and cost | 6 | Call a hosted model without leaking the key, and read the bill |
| Retrieval | 7 | Cite a real passage, and measure whether retrieval found it |
| Agents | 7 | Design a tool loop with a schema, a step cap, and a trace |
| MCP | 6 | Connect a tool server without granting it silent access |
| Coding agents | 6 | Review a repository edit against the diff and the tests |
| Evals | 7 | Gate a change on quality, safety, latency, and cost |
| Fine-tuning | 5 | Decide when LoRA is warranted, and compare it to the base model |
| Safety | 5 | Write a one-page policy for data, tools, and human approval |
| Product skills | 6 | Specify a feature a product manager and an engineer can measure |
| Capstone | 5 | Finish a small grounded assistant on notes you are allowed to use |

Glossary, interview practice, and course questions sit beside the tracks.

## Learning path

```mermaid
flowchart TD
  startHere[Start here] --> models[How models work]
  models --> prompting[Prompting]
  prompting --> localModels[Local models]
  prompting --> apis[APIs and cost]
  localModels --> retrieval[Retrieval]
  apis --> retrieval
  retrieval --> agents[Agents]
  agents --> mcp[MCP]
  agents --> evals[Evals]
  mcp --> coding[Coding agents]
  coding --> evals
  evals --> safety[Safety]
  evals --> finetune[Fine-tuning only if the score says so]
  safety --> product[Product skills]
  product --> capstone[Capstone]
```

Four shorter routes are on the home page: new to AI, a grounded assistant, coding-agent work, and product judgment.

---

## How to use it

1. Download [ai-lab-university.html.zip](downloads/ai-lab-university.html.zip).
2. Unzip it.
3. Open `ai-lab-university.html` in Chrome, Safari, Edge, or Firefox. Use the full browser app. In-app browsers often block a local file.
4. On iPhone: download the file, then open it from Files in Chrome or Safari.

Study a lesson, do the practice, then use **Next**. **Mark complete** stores progress only in that browser. Search is in the sidebar. Each lesson opens with an animated flow: play, pause, step, and speed, with the current stage highlighted and a caption under the picture. **Studio** in the sidebar runs the toy demos with no key. The sun and moon button switches the light and dark themes. **HC** is a separate high-contrast switch. `/` focuses search. `[` and `]` move between lessons.

A desktop browser is the most comfortable. A phone is enough to read.

You do not need a GPU or an API key to study. Add a local model or a hosted key only when a practice asks for a live call, and only with data you are allowed to send. The short page is [campus/golden-slice.html](campus/golden-slice.html). A month of study, interview drills, and a class plan are in [docs/HOW-TO-USE.md](docs/HOW-TO-USE.md).

More detail: [docs/START-HERE.md](docs/START-HERE.md) · [docs/HOW-TO-GET.md](docs/HOW-TO-GET.md) · [docs/DOWNLOADS.md](docs/DOWNLOADS.md) · [docs/FAQ.md](docs/FAQ.md)

## Remix

The campus is generated so the lessons stay reviewable:

```bash
git clone https://github.com/cipher0x9/ai-lab-free-university-mesmerizing.git
cd ai-lab-free-university-mesmerizing
python3 -m campus.build_campus
python3 scripts/rebuild_zips.py
```

That rewrites `campus/ai-lab-university.html`, `docs/assets/hero.svg`, and the zip in `downloads/`. Lesson text lives in `campus/`. The built file is what you open and what the zip contains. The checklist is [docs/REMIX.md](docs/REMIX.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

You may copy, change, and redistribute the course under the [MIT license](LICENSE). Keep the copyright notice. Do not present model weights, vendor docs, or someone else's data as part of this license. If you publish a remix, say what you changed, and do not add a CDN dependency to the HTML file.

`campus/golden-slice.html` is the short starter. The course is the full HTML file.

## FAQ

**Is this free?**  
Yes. Free to use, share and remix under MIT. There is no account and no certificate. The capstone folder is the evidence.

**Does the page phone home?**  
No. It does not load remote assets. Progress is local storage in your browser.

**Which model should I install?**  
A small instruct model whose license you have read, in a size that fits your memory. The course teaches the decision. It does not crown a vendor.

**Can I use it at work?**  
You can use the text. Your employer's data rules and the model license still apply. Do not paste secrets or customer data into a hosted model because a lesson mentioned an API.

**How do I report a mistake?**  
Open an issue with the lesson id (for example `07-01`), the sentence, and the correction. Specs and model names move. A dated source helps.

## Related

Voice and contact-center material lives in a separate course, [UC Lab Free University](https://github.com/cipher0x9/uc-lab-free-university-mesmerizing). This campus does not try to be that course. See [docs/SIBLINGS.md](docs/SIBLINGS.md).

## Author

**CYPHER0X9** · [cipher0x9](https://github.com/cipher0x9)

Educational material. No warranty. Lab safely, and do not upload secrets.
