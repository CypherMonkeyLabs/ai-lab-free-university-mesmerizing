# How to use AI Lab Free University

This guide is for a learner, a job-seeker, and a teacher. Builders who want to change the campus should read [REMIX.md](./REMIX.md) after this.

The campus is one HTML file. It does not phone home. Study ticks and the theme you pick are stored in that browser only. Clearing site data for a `file://` page clears your ticks.

## Every file, offline and on a phone

| File | Offline | On a phone |
|---|---|---|
| `campus/ai-lab-university.html` | Double-click, or open it from the full browser’s file picker. Search with the box. Open a track, then move with Previous and Next. Mark a lesson complete only when you can teach it. | Download the zip first. Open `ai-lab-university.html` in the **full** Chrome or Safari app. The track list is a menu. First open can take a few seconds. |
| `downloads/ai-lab-university.html.zip` | Unzip anywhere. You only need the HTML file inside. | Save to Files (iPhone) or Downloads (Android), unzip if the OS did not, then open in the full browser. |
| `campus/golden-slice.html` | The short path: the proof habit, a map, and a checklist. | Same rule. Easier on a small screen than the full campus. |
| `labs/*.py` | Run on a computer from a clone. They do not run inside the phone browser. | Read the lesson on the phone. Run the lab when you are back at a keyboard. |
| `docs/*.md` | Any text editor or the GitHub website. | Fine for the 30-day plan. The campus itself is still the HTML file. |

Desktop is the best place to study. A phone is a good place to review a lesson you already understand.

In-app browsers inside mail, chat, and social apps are the usual failure. If the page is blank or scripts are dead, move the file to Chrome, Safari, Edge, or Firefox.

Print any lesson with the browser’s Print → Save as PDF. There is no separate textbook.

## A 30-day study path

One hour a day is enough. Keep a single folder of artifacts. Use a synthetic problem from your own field. Do not paste private data into a prompt or a git repo.

Review each hard idea at **1 hour, 24 hours, 7 days, and 30 days**. At each review: say the rule, name one exception, and say what would prove you wrong.

| Days | Do this | Done when |
|---|---|---|
| 1 | Open the golden slice. Learn the four proof fields: run, trace, metric, artifact. | You can name the four fields without notes. |
| 2–3 | Tracks 00 and 01. Write your safety rule (no auto-send, no secrets in git). | The rule is a file, not a mood. |
| 4–7 | Track 03 and `python3 labs/01-local-hello.py`. Mock is allowed. Label it mock. | `labs/artifacts/01-local-hello.json` exists and you can explain the backend field. |
| 8–11 | Track 02. Rewrite one prompt as a job with an output shape. | You changed one variable and kept both outputs. |
| 12–15 | Track 06 and `python3 labs/02-tool-call.py`. | The answer quotes the tool result, not a guess. |
| 16–19 | Track 05. Then `python3 labs/06-rag-ablation.py`. | You can show the case where the wrong neighbor wins. |
| 20–23 | Track 09 and `python3 labs/03-golden-eval.py`. | `labs/reports/golden10-report.md` shows pass rate and threshold. |
| 24–27 | Tracks 07 (MCP), 08 (coding agents), and the stop rule in `06-01`. Run labs 07 and 08. Read `12-06` if speech is in scope. | You can name the tools that need a person, and the slow leg the average hides. |
| 28–29 | Track IV out loud, 30 seconds then 90 seconds per question. | A friend can follow the answer. |
| 30 | Track 13, especially `13-04` and `13-05`. One portfolio page: task, artifact, falsifier. | A stranger can open the file without you in the room. |

Skip a day rather than study with customer data.

## Interview prep

Use track **IV** as the question list. A strong answer has three beats:

1. The mechanism, in plain language.
2. The evidence (a command, a pass rate, a trace).
3. The failure you watch for.

Drill:

- Pick five IV lessons. Answer in 30 seconds, then again in 90 seconds with the artifact named.
- For “local or hosted?”, use `03-01` and `04-01`: where the prompt goes, and where the key lives.
- For “how do you stop an agent?”, use `06-01` and lab 07. Say the step cap before you say the model name.
- For “are you current?”, talk about MCP, coding-agent review, and evals that survive a model swap (`07-01`, `08-04`, `09-05`). Do not recite a secret model list.
- Bring the golden-10 report and one lab JSON. If the interviewer cannot open them, they are not proof.

Ignore certificate talk unless the role literally requires one. This campus does not issue one.

## Teach a class

You can teach from the HTML with no accounts and no install.

**60 minutes (lunch and learn)**

1. Project the golden slice. Teach the four proof fields. Skip any voice analogy if the room does not work in contact centers.
2. Run lab 01 on the projector. If it prints `mock`, celebrate the honesty.
3. Run lab 02. Ask the room what would have been invented without the tool.
4. Send people home with the zip, not a slide deck.

**Four evenings**

| Evening | Campus | Lab |
|---|---|---|
| 1 | Tracks 00 and 01 | None. They write a safety rule. |
| 2 | Track 03 | Lab 01 |
| 3 | Tracks 02 and 06 | Lab 02 |
| 4 | Tracks 09 and 07 | Lab 03, then one learner teaches `07-01` |

**Rules for the room**

- Synthetic data only.
- Marking complete is personal. Do not collect the browser’s local storage.
- Do not require an API key to finish.
- If you fork the campus, keep the MIT notice and run `python3 scripts/verify_campus.py`.
- Print to PDF per lesson if someone cannot run HTML. Do not republish their private notes.
